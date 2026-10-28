#!/usr/bin/env python3
"""Theo dõi deploy trên Rancher (chỉ đọc): deployment, pod, chờ rollout, log, event.

  python scripts/rancher.py deployments [-n NS]
  python scripts/rancher.py pods [-n NS] [--deployment NAME]
  python scripts/rancher.py watch DEPLOY[=TAG] [DEPLOY[=TAG] ...] [--image-tag TAG] [--timeout 15] [--settle 60]
  python scripts/rancher.py logs TARGET [--since 30m] [--tail 200] [--previous] [--grep REGEX | --sql-errors]
  python scripts/rancher.py events [--for NAME] [--all]
  python scripts/rancher.py config DEPLOY [--grep REGEX]

TARGET là tên pod hoặc tên deployment (lấy log mọi pod của deployment). Thêm --json để máy đọc,
--profile NAME để dùng Rancher khác (.env.NAME).
Mã thoát: 0 = ổn, 1 = rollout lỗi, hết giờ hoặc log có lỗi SQL, 2 = lỗi cấu hình/kết nối/quyền.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time

from rancher_client import RancherClient, RancherError

# Trạng thái chờ của container mà rollout không tự hết được.
FATAL_WAITING = {"CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull", "InvalidImageName",
                 "CreateContainerConfigError", "CreateContainerError", "RunContainerError"}
# Container chết vì lý do này bao nhiêu lần thì coi là lỗi (tránh báo nhầm khi chỉ chết một lần lúc khởi động).
CRASH_RESTARTS = 2
ANSI = re.compile(r"\x1b\[[0-9;]*m")
# Tên biến/khoá gợi ý bí mật -> che giá trị; URL có user:pass@ -> che mật khẩu.
SENSITIVE_KEY = re.compile(r"pass|pwd|secret|token|credential|private|jwt|cert|licen[cs]e|(^|[_.-])key($|[_.-])"
                           r"|apikey|accesskey", re.I)
URL_PASSWORD = re.compile(r"(//[^/:@\s]+:)[^@/\s]+@")
# Giá trị trông như khoá/token dù tên biến vô hại: chuỗi dài liền mạch kiểu base64/hex có cả chữ lẫn số.
OPAQUE_VALUE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9+/=_.-]{24,}$")
PEM = re.compile(r"-----BEGIN [A-Z ]+-----")
# Khác hẳn mọi giá trị thật (kể cả "*" hay "***") để người đọc biết là đã che.
MASK = "<masked>"
# Lỗi schema/SQL lúc chạy: dấu hiệu bản mới cần migration mà DB chưa chạy (môi trường tắt Flyway).
SQL_ERROR = re.compile(
    r"BadSqlGrammarException|SQLGrammarException|SQLSyntaxErrorException|PSQLException"
    r"|relation \"[^\"]+\" does not exist|column \"?[\w.]+\"? (of relation \"[^\"]+\" )?does not exist"
    r"|no unique or exclusion constraint|Schema-validation:|FlywayValidateException"
    r"|Validate failed: Migrations|Detected (resolved|applied) migration not (applied|resolved)", re.I)
TIMESTAMP = re.compile(r"\d{4}-\d\d-\d\dT[\d:.]+(Z|[+-]\d\d:?\d\d)?\s*")
FLYWAY_SWITCH = re.compile(r"^(SPRING_)?FLYWAY_ENABLED$", re.I)
SQL_ERROR_LINES = 8


def mask_value(key: str, value: str | None) -> str | None:
    if value is None:
        return None
    if SENSITIVE_KEY.search(key) or PEM.search(value) or OPAQUE_VALUE.match(value.strip()):
        return MASK
    return URL_PASSWORD.sub(r"\1" + MASK + "@", value)


def parse_since(text: str | None) -> int | None:
    if not text:
        return None
    m = re.fullmatch(r"(\d+)([smhd]?)", text.strip())
    if not m:
        raise RancherError(f"--since sai dạng (vd 90s, 30m, 2h, 1d): {text}")
    return int(m.group(1)) * {"": 1, "s": 1, "m": 60, "h": 3600, "d": 86400}[m.group(2)]


def sql_errors(text: str, limit: int = SQL_ERROR_LINES) -> list[str]:
    """Dòng log lỗi SQL/schema, bỏ trùng (khác nhau mỗi timestamp/thread vẫn tính là một)."""
    seen, out = set(), []
    for line in text.splitlines():
        if not SQL_ERROR.search(line):
            continue
        clean = TIMESTAMP.sub("", line).strip()
        key = re.sub(r"\[[^\]]*\]|\d+", "", clean)
        if key not in seen:
            seen.add(key)
            out.append(clean[:400])
            if len(out) >= limit:
                break
    return out


def age_seconds(ts: str | None) -> int:
    if not ts:
        return 0
    start = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    return int((dt.datetime.now(dt.timezone.utc) - start).total_seconds())


def age(ts: str | None) -> str:
    if not ts:
        return "-"
    s = age_seconds(ts)
    if s < 3600:
        return f"{s // 60}m{s % 60:02d}s"
    if s < 86400:
        return f"{s // 3600}h{(s % 3600) // 60:02d}m"
    return f"{s // 86400}d{(s % 86400) // 3600}h"


def image_tag(image: str) -> str:
    return image.rsplit(":", 1)[-1] if ":" in image.rsplit("/", 1)[-1] else "latest"


def deployment_info(d: dict) -> dict:
    spec, st = d["spec"], d.get("status", {})
    containers = spec["template"]["spec"]["containers"]
    desired = spec.get("replicas", 1)
    cond = {c["type"]: c for c in st.get("conditions", [])}
    progressing = cond.get("Progressing", {})
    return {
        "name": d["metadata"]["name"],
        "image": containers[0]["image"],
        "tag": image_tag(containers[0]["image"]),
        "desired": desired,
        "updated": st.get("updatedReplicas", 0),
        "ready": st.get("readyReplicas", 0),
        "available": st.get("availableReplicas", 0),
        "unavailable": st.get("unavailableReplicas", 0),
        "total": st.get("replicas", 0),
        "generation": d["metadata"].get("generation", 0),
        "observed": st.get("observedGeneration", 0),
        "deadline_exceeded": progressing.get("reason") == "ProgressDeadlineExceeded",
        "progress_message": progressing.get("message", ""),
        "selector": spec["selector"].get("matchLabels", {}),
    }


def rollout_done(i: dict) -> bool:
    # Giống `kubectl rollout status`: đã quan sát spec mới, mọi pod lên bản mới, không còn pod cũ, đủ available.
    return (i["observed"] >= i["generation"] and i["updated"] == i["desired"]
            and i["total"] == i["updated"] and i["available"] == i["desired"] and i["unavailable"] == 0)


def pod_info(p: dict) -> dict:
    st = p.get("status", {})
    cs = (st.get("containerStatuses") or [{}])[0]
    waiting = (cs.get("state") or {}).get("waiting") or {}
    last_term = (cs.get("lastState") or {}).get("terminated") or {}
    return {
        "name": p["metadata"]["name"],
        "phase": st.get("phase"),
        "ready": bool(cs.get("ready")),
        "restarts": cs.get("restartCount", 0),
        "image": cs.get("image") or p["spec"]["containers"][0]["image"],
        "waiting_reason": waiting.get("reason"),
        "waiting_message": (waiting.get("message") or "")[:300],
        "last_exit_reason": last_term.get("reason"),
        "last_exit_code": last_term.get("exitCode"),
        "started": st.get("startTime"),
        "age": age(st.get("startTime")),
        "spec_image": p["spec"]["containers"][0]["image"],
    }


def pod_failure(pi: dict) -> str | None:
    if pi["waiting_reason"] in FATAL_WAITING:
        return f"{pi['waiting_reason']}: {pi['waiting_message']}".rstrip(": ")
    if pi["restarts"] >= CRASH_RESTARTS and pi["last_exit_reason"]:
        return f"container khởi động lại {pi['restarts']} lần (lần cuối {pi['last_exit_reason']}, exit {pi['last_exit_code']})"
    if pi["phase"] == "Failed":
        return "pod ở trạng thái Failed"
    return None


class Ops:
    def __init__(self, client: RancherClient, namespace: str):
        if not namespace:
            raise RancherError("Thiếu namespace: truyền -n hoặc đặt RANCHER_NAMESPACE.")
        self.c, self.ns = client, namespace

    def deployments(self) -> list[dict]:
        data = self.c.k8s(f"apis/apps/v1/namespaces/{self.ns}/deployments")
        return [deployment_info(d) for d in data.get("items", [])]

    def deployment(self, name: str) -> dict:
        return deployment_info(self.c.k8s(f"apis/apps/v1/namespaces/{self.ns}/deployments/{name}"))

    def pods(self, selector: dict | None = None) -> list[dict]:
        params = {"labelSelector": ",".join(f"{k}={v}" for k, v in selector.items())} if selector else None
        data = self.c.k8s(f"api/v1/namespaces/{self.ns}/pods", params)
        return [pod_info(p) for p in data.get("items", [])]

    def events(self, name: str | None = None, warnings_only: bool = True) -> list[dict]:
        fields = []
        if name:
            fields.append(f"involvedObject.name={name}")
        if warnings_only:
            fields.append("type=Warning")
        data = self.c.k8s(f"api/v1/namespaces/{self.ns}/events",
                          {"fieldSelector": ",".join(fields)} if fields else None)
        rows = []
        for e in data.get("items", []):
            when = e.get("lastTimestamp") or e.get("eventTime") or (e.get("metadata") or {}).get("creationTimestamp")
            rows.append({"when": when, "type": e.get("type"), "reason": e.get("reason"),
                         "object": e["involvedObject"].get("name"), "count": e.get("count", 1),
                         "message": (e.get("message") or "").strip()[:400]})
        return sorted(rows, key=lambda r: r["when"] or "")

    def log(self, pod: str, tail: int, since: int | None, previous: bool) -> str:
        text = self.c.k8s(f"api/v1/namespaces/{self.ns}/pods/{pod}/log",
                          {"tailLines": tail, "sinceSeconds": since, "timestamps": "true",
                           "previous": "true" if previous else None}, raw=True)
        return ANSI.sub("", text)

    def raw_deployment(self, name: str) -> dict:
        return self.c.k8s(f"apis/apps/v1/namespaces/{self.ns}/deployments/{name}")

    def configmap(self, name: str) -> dict:
        return self.c.k8s(f"api/v1/namespaces/{self.ns}/configmaps/{name}").get("data") or {}

    def secret_keys(self, name: str) -> list[str]:
        # Chỉ lấy tên key; giá trị secret không bao giờ được giữ lại hay in ra.
        return sorted((self.c.k8s(f"api/v1/namespaces/{self.ns}/secrets/{name}").get("data") or {}).keys())

    def flyway_disabled(self, name: str) -> bool:
        """True khi deployment đặt FLYWAY_ENABLED / SPRING_FLYWAY_ENABLED = false (env hoặc ConfigMap)."""
        values = []
        for c in self.raw_deployment(name)["spec"]["template"]["spec"]["containers"]:
            for e in c.get("env") or []:
                if FLYWAY_SWITCH.match(e["name"]):
                    ref = (e.get("valueFrom") or {}).get("configMapKeyRef")
                    values.append(self.configmap(ref["name"]).get(ref["key"]) if ref else e.get("value"))
            for ef in c.get("envFrom") or []:
                if "configMapRef" in ef:
                    try:
                        data = self.configmap(ef["configMapRef"]["name"])
                    except RancherError:
                        continue
                    values += [v for k, v in data.items() if FLYWAY_SWITCH.match(ef.get("prefix", "") + k)]
        return any(str(v).strip().lower() == "false" for v in values)

    def pods_of(self, target: str) -> list[dict]:
        """Tên pod cụ thể, hoặc tên deployment -> mọi pod của nó."""
        pods = self.pods()
        exact = [p for p in pods if p["name"] == target]
        if exact:
            return exact
        try:
            selector = self.deployment(target)["selector"]
        except RancherError:
            raise RancherError(f"Không thấy pod hay deployment tên '{target}' trong namespace {self.ns}.") from None
        return self.pods(selector)


def print_table(rows: list[dict], cols: list[tuple[str, str]]) -> None:
    widths = [max(len(h), *(len(str(r.get(k, ""))) for r in rows)) if rows else len(h) for k, h in cols]
    print("  ".join(h.ljust(w) for (_, h), w in zip(cols, widths)))
    for r in rows:
        print("  ".join(str(r.get(k, "")).ljust(w) for (k, _), w in zip(cols, widths)))


def cmd_deployments(ops: Ops, args) -> int:
    rows = ops.deployments()
    for r in rows:
        r["state"] = "OK" if rollout_done(r) else ("LỖI" if r["deadline_exceeded"] else "đang rollout")
        r["ready_col"] = f"{r['ready']}/{r['desired']}"
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    print(f"Namespace: {ops.ns}")
    print_table(rows, [("name", "DEPLOYMENT"), ("tag", "TAG"), ("ready_col", "READY"),
                       ("updated", "UPDATED"), ("state", "TRẠNG THÁI")])
    return 0


def cmd_pods(ops: Ops, args) -> int:
    rows = ops.pods(ops.deployment(args.deployment)["selector"]) if args.deployment else ops.pods()
    for r in rows:
        r["tag"] = image_tag(r["spec_image"])
        r["problem"] = pod_failure(r) or r["waiting_reason"] or ""
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    print_table(rows, [("name", "POD"), ("phase", "PHASE"), ("ready", "READY"), ("restarts", "RESTARTS"),
                       ("tag", "TAG"), ("age", "TUỔI"), ("problem", "VẤN ĐỀ")])
    return 0


def diagnose(ops: Ops, info: dict, log_tail: int) -> dict:
    """Gom pod lỗi + event Warning + log cuối của pod lỗi để báo nguyên nhân."""
    pods = ops.pods(info["selector"])
    new_pods = [p for p in pods if p["spec_image"] == info["image"]]
    bad = [(p, pod_failure(p)) for p in new_pods]
    bad = [(p, why) for p, why in bad if why] or [(p, "chưa ready") for p in new_pods if not p["ready"]]
    report = {"deployment": info["name"], "progress_message": info["progress_message"], "pods": []}
    for p, why in bad:
        entry = {"pod": p["name"], "reason": why, "events": ops.events(p["name"]), "log": ""}
        try:
            entry["log"] = ops.log(p["name"], log_tail, None, previous=p["restarts"] > 0)
        except RancherError as e:
            entry["log"] = f"(không đọc được log: {e})"
        report["pods"].append(entry)
    report["deployment_events"] = ops.events(info["name"])
    return report


def print_diagnosis(rep: dict) -> None:
    if rep["progress_message"]:
        print(f"  deployment: {rep['progress_message']}")
    for ev in rep["deployment_events"][-5:]:
        print(f"  [event] {ev['when']} {ev['reason']}: {ev['message']}")
    for p in rep["pods"]:
        print(f"  pod {p['pod']}: {p['reason']}")
        for ev in p["events"][-8:]:
            print(f"    [event] {ev['when']} {ev['reason']} x{ev['count']}: {ev['message']}")
        if p["log"].strip():
            print("    --- log cuối ---")
            for line in p["log"].rstrip().splitlines():
                print("    " + line)


def cmd_watch(ops: Ops, args) -> int:
    deadline = time.time() + args.timeout * 60
    # "deploy=tag" chờ đúng tag riêng; tên trơn dùng --image-tag chung (nếu có).
    pending = {}
    for item in args.deployments:
        name, _, tag = item.partition("=")
        pending[name] = tag or args.image_tag
    results = {}
    last_line = {}
    while pending:
        for name, want_tag in list(pending.items()):
            info = ops.deployment(name)
            if want_tag and info["tag"] != want_tag:
                state = f"chờ image tag {want_tag} (đang {info['tag']})"
            else:
                failure = None
                if info["deadline_exceeded"]:
                    failure = "ProgressDeadlineExceeded"
                else:
                    for p in ops.pods(info["selector"]):
                        if p["spec_image"] == info["image"] and pod_failure(p):
                            failure = pod_failure(p)
                            break
                if failure:
                    results[name] = {"status": "FAILED", "reason": failure, "info": info,
                                     "diagnosis": diagnose(ops, info, args.log_tail)}
                    del pending[name]
                    continue
                if rollout_done(info):
                    results[name] = {"status": "OK", "info": info}
                    del pending[name]
                    continue
                state = (f"rollout {info['tag']}: updated {info['updated']}/{info['desired']}, "
                         f"ready {info['ready']}/{info['desired']}, còn {info['total'] - info['updated']} pod cũ")
            if not args.json and last_line.get(name) != state:
                print(f"  … {name}: {state}", flush=True)
                last_line[name] = state
        if pending and time.time() >= deadline:
            for name, want_tag in pending.items():
                info = ops.deployment(name)
                reason = (f"image vẫn là tag {info['tag']}, chưa đổi sang {want_tag} (job deploy chưa chạy?)"
                          if want_tag and info["tag"] != want_tag else "rollout chưa xong khi hết giờ")
                results[name] = {"status": "TIMEOUT", "reason": reason, "info": info,
                                 "diagnosis": diagnose(ops, info, args.log_tail)}
            break
        if pending:
            time.sleep(args.interval)

    scan_sql_errors(ops, results, args, deadline)
    ok = all(r["status"] == "OK" for r in results.values())
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
        return 0 if ok else 1
    for name, r in results.items():
        i = r["info"]
        print(f"{name}: {r['status']} | tag {i['tag']} | ready {i['ready']}/{i['desired']}"
              + (f" | {r['reason']}" if r.get("reason") else ""))
        for line in r.get("sql_errors", []):
            print(f"  [sql] {line}")
        if r.get("manual_migrations"):
            print("  lưu ý: deployment tắt Flyway, migration phải chạy SQL tay"
                  + (" — kiểm migration mới của service này đã chạy trên DB chưa." if r["status"] == "SQL_ERROR"
                     else f"; {args.settle}s đầu chưa thấy lỗi SQL."))
        for note in r.get("notes", []):
            print(f"  lưu ý: {note}")
        if r["status"] in ("FAILED", "TIMEOUT"):
            print_diagnosis(r["diagnosis"])
    return 0 if ok else 1


def scan_sql_errors(ops: Ops, results: dict, args, deadline: float) -> None:
    """Pod Ready chưa đủ: môi trường tắt Flyway vẫn lên bản mới dù DB thiếu migration, lỗi chỉ hiện trong log.

    Chờ pod mới chạy đủ --settle giây (không quá hạn --timeout) rồi quét log tìm lỗi SQL/schema.
    """
    done = {n: r for n, r in results.items() if r["status"] == "OK"}
    if not done:
        return
    pods = {n: [p for p in ops.pods(r["info"]["selector"]) if p["spec_image"] == r["info"]["image"]]
            for n, r in done.items()}
    youngest = min((age_seconds(p["started"]) for ps in pods.values() for p in ps), default=args.settle)
    wait = min(args.settle - youngest, deadline - time.time())
    if wait > 0:
        if not args.json:
            print(f"  … chờ {int(wait)}s cho pod mới chạy đủ {args.settle}s rồi quét log lỗi SQL", flush=True)
        time.sleep(wait)
    for name, r in done.items():
        try:
            r["manual_migrations"] = ops.flyway_disabled(name)
        except RancherError as e:
            r.setdefault("notes", []).append(f"không đọc được cấu hình Flyway: {e}")
        text = []
        for p in pods[name]:
            try:
                text.append(ops.log(p["name"], args.scan_tail, None, previous=False))
            except RancherError as e:
                r.setdefault("notes", []).append(f"không đọc được log {p['name']}: {e}")
        errors = sql_errors("\n".join(text))
        if errors:
            r.update(status="SQL_ERROR", reason="log pod mới có lỗi SQL/schema", sql_errors=errors)


def env_source(e: dict) -> dict:
    vf = e.get("valueFrom")
    if not vf:
        return {"name": e["name"], "source": "value", "value": mask_value(e["name"], e.get("value", ""))}
    if "configMapKeyRef" in vf:
        ref = vf["configMapKeyRef"]
        return {"name": e["name"], "source": f"configmap {ref['name']}/{ref['key']}", "ref": ("configmap", ref["name"], ref["key"])}
    if "secretKeyRef" in vf:
        ref = vf["secretKeyRef"]
        return {"name": e["name"], "source": f"secret {ref['name']}/{ref['key']}", "value": MASK}
    if "fieldRef" in vf:
        return {"name": e["name"], "source": "field " + vf["fieldRef"]["fieldPath"]}
    if "resourceFieldRef" in vf:
        return {"name": e["name"], "source": "resource " + vf["resourceFieldRef"]["resource"]}
    return {"name": e["name"], "source": "khác"}


def collect_config(ops: Ops, name: str) -> dict:
    d = ops.raw_deployment(name)
    pod_spec = d["spec"]["template"]["spec"]
    cm_cache: dict[str, dict] = {}

    def cm(n: str) -> dict:
        if n not in cm_cache:
            try:
                cm_cache[n] = ops.configmap(n)
            except RancherError as e:
                cm_cache[n] = {"__error__": str(e)}
        return cm_cache[n]

    out = {"deployment": name, "namespace": ops.ns, "replicas": d["spec"].get("replicas", 1), "containers": []}
    volumes = {v["name"]: v for v in pod_spec.get("volumes") or []}
    for c in pod_spec["containers"]:
        env = []
        for e in c.get("env") or []:
            row = env_source(e)
            ref = row.pop("ref", None)
            if ref:
                data = cm(ref[1])
                row["value"] = mask_value(e["name"], data.get(ref[2])) if "__error__" not in data else "(không đọc được)"
            env.append(row)
        env_from = []
        for ef in c.get("envFrom") or []:
            prefix = ef.get("prefix", "")
            if "configMapRef" in ef:
                n = ef["configMapRef"]["name"]
                data = cm(n)
                env_from.append({"kind": "configmap", "name": n, "prefix": prefix,
                                 "values": {k: mask_value(k, v) for k, v in data.items() if k != "__error__"},
                                 "error": data.get("__error__")})
            elif "secretRef" in ef:
                n = ef["secretRef"]["name"]
                try:
                    keys, err = ops.secret_keys(n), None
                except RancherError as e:
                    keys, err = [], str(e)
                env_from.append({"kind": "secret", "name": n, "prefix": prefix, "keys": keys, "error": err})
        mounts = []
        for m in c.get("volumeMounts") or []:
            v = volumes.get(m["name"], {})
            kind = next((k for k in ("configMap", "secret", "persistentVolumeClaim", "emptyDir", "hostPath") if k in v), "khác")
            ref = (v.get(kind) or {}).get("name") or (v.get(kind) or {}).get("secretName") or (v.get(kind) or {}).get("claimName") or ""
            mounts.append({"path": m["mountPath"], "kind": kind, "ref": ref, "readOnly": bool(m.get("readOnly"))})
        probe = c.get("readinessProbe") or {}
        out["containers"].append({
            "name": c["name"],
            "image": c["image"],
            "command": c.get("command"),
            "args": c.get("args"),
            "ports": [p.get("containerPort") for p in c.get("ports") or []],
            "resources": c.get("resources") or {},
            "readiness": (probe.get("httpGet") or {}).get("path") or ("tcp" if "tcpSocket" in probe else None),
            "env": env,
            "envFrom": env_from,
            "mounts": mounts,
        })
    return out


def cmd_config(ops: Ops, args) -> int:
    cfg = collect_config(ops, args.deployment)
    if args.grep:
        rx = re.compile(args.grep, re.I)
        for c in cfg["containers"]:
            c["env"] = [e for e in c["env"] if rx.search(e["name"])]
            for ef in c["envFrom"]:
                if "values" in ef:
                    ef["values"] = {k: v for k, v in ef["values"].items() if rx.search(k)}
                if "keys" in ef:
                    ef["keys"] = [k for k in ef["keys"] if rx.search(k)]
    if args.json:
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
        return 0
    print(f"{cfg['namespace']}/{cfg['deployment']} (replicas {cfg['replicas']})")
    for c in cfg["containers"]:
        print(f"\n[container {c['name']}] {c['image']}")
        if c["command"] or c["args"]:
            print(f"  command: {' '.join((c['command'] or []) + (c['args'] or []))}")
        if c["ports"]:
            print(f"  ports: {', '.join(map(str, c['ports']))}   readiness: {c['readiness'] or '-'}")
        if c["resources"]:
            print(f"  resources: {json.dumps(c['resources'])}")
        if c["env"]:
            print(f"  env ({len(c['env'])}):")
            for e in c["env"]:
                src = "" if e["source"] == "value" else f"   ← {e['source']}"
                print(f"    {e['name']}={e.get('value') if e.get('value') is not None else ''}{src}")
        for ef in c["envFrom"]:
            if ef.get("error"):
                print(f"  envFrom {ef['kind']} {ef['name']}: {ef['error']}")
            elif ef["kind"] == "configmap":
                print(f"  envFrom configmap {ef['name']}" + (f" (prefix {ef['prefix']})" if ef["prefix"] else "") + ":")
                for k, v in ef["values"].items():
                    print(f"    {k}={v}")
            else:
                print(f"  envFrom secret {ef['name']} — {len(ef['keys'])} key (ẩn giá trị): {', '.join(ef['keys'])}")
        for m in c["mounts"]:
            print(f"  mount {m['path']} ← {m['kind']} {m['ref']}{' (ro)' if m['readOnly'] else ''}")
    return 0


def cmd_logs(ops: Ops, args) -> int:
    since = parse_since(args.since)
    rx = SQL_ERROR if args.sql_errors else re.compile(args.grep, re.I) if args.grep else None
    for p in ops.pods_of(args.target):
        text = ops.log(p["name"], args.tail, since, args.previous)
        lines = [ln for ln in text.splitlines() if not rx or rx.search(ln)]
        print(f"===== {p['name']} ({'container trước' if args.previous else 'đang chạy'}, {len(lines)} dòng) =====")
        print("\n".join(lines))
    return 0


def cmd_events(ops: Ops, args) -> int:
    rows = ops.events(args.for_name, warnings_only=not args.all)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    for r in rows[-args.limit:]:
        print(f"{r['when']} {r['type']:<7} {r['object']}: {r['reason']} x{r['count']} — {r['message']}")
    if not rows:
        print("(không có event" + (" Warning" if not args.all else "") + ")")
    return 0


def main() -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-n", "--namespace", help="namespace (mặc định RANCHER_NAMESPACE)")
    common.add_argument("--json", action="store_true", help="in JSON")
    common.add_argument("--profile", help="Rancher khác: đọc .env.<profile> (mặc định RANCHER_PROFILE hoặc .env)")
    ap = argparse.ArgumentParser(description="Rancher: theo dõi deploy, chỉ đọc.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub_parser = lambda name, **kw: sub.add_parser(name, parents=[common], **kw)  # noqa: E731

    sub_parser("deployments", help="liệt kê deployment, image tag, trạng thái rollout")

    p = sub_parser("pods", help="liệt kê pod và vấn đề")
    p.add_argument("--deployment", help="chỉ pod của deployment này")

    p = sub_parser("watch", help="chờ rollout xong; lỗi thì báo nguyên nhân + log")
    p.add_argument("deployments", nargs="+", help="tên deployment, hoặc deployment=TAG để chờ đúng tag")
    p.add_argument("--image-tag", help="tag chung cho các deployment không ghi =TAG (vd Build tag của Jenkins)")
    p.add_argument("--timeout", type=int, default=15, help="phút chờ tối đa (mặc định 15)")
    p.add_argument("--interval", type=int, default=10, help="giây giữa hai lần hỏi (mặc định 10)")
    p.add_argument("--log-tail", type=int, default=60, help="số dòng log in kèm khi lỗi")
    p.add_argument("--settle", type=int, default=60,
                   help="giây pod mới phải chạy trước khi quét log lỗi SQL (mặc định 60, 0 = quét ngay)")
    p.add_argument("--scan-tail", type=int, default=3000, help="số dòng log cuối mỗi pod để quét lỗi SQL")

    p = sub_parser("logs", help="log pod hoặc mọi pod của deployment")
    p.add_argument("target")
    p.add_argument("--since", help="vd 30m, 2h")
    p.add_argument("--tail", type=int, default=200)
    p.add_argument("--previous", action="store_true", help="log của container trước khi restart")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--grep", help="chỉ giữ dòng khớp regex (không phân biệt hoa thường)")
    group.add_argument("--sql-errors", action="store_true", help="chỉ giữ dòng lỗi SQL/schema (như watch quét)")

    p = sub_parser("config", help="cấu hình đang áp dụng: env, envFrom, mount (che secret)")
    p.add_argument("deployment")
    p.add_argument("--grep", help="chỉ giữ biến/khoá có tên khớp regex")

    p = sub_parser("events", help="event của namespace (mặc định chỉ Warning)")
    p.add_argument("--for", dest="for_name", help="tên pod/deployment")
    p.add_argument("--all", action="store_true", help="lấy cả event Normal")
    p.add_argument("--limit", type=int, default=30)

    args = ap.parse_args()
    client = None
    try:
        client = RancherClient(profile=args.profile)
        ops = Ops(client, args.namespace or client.default_namespace)
        return {"deployments": cmd_deployments, "pods": cmd_pods, "watch": cmd_watch,
                "logs": cmd_logs, "events": cmd_events, "config": cmd_config}[args.cmd](ops, args)
    except RancherError as e:
        print(f"LỖI: {e}", file=sys.stderr)
        return 2
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    sys.exit(main())
