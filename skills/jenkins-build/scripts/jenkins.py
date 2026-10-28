#!/usr/bin/env python3
"""Xem job, kích build và chờ kết quả trên Jenkins.

  python scripts/jenkins.py views
  python scripts/jenkins.py jobs [--view CCDT-DEV]
  python scripts/jenkins.py status JOB [--build N]
  python scripts/jenkins.py build JOB [JOB ...] [-p KEY=VALUE] [--wait] [--timeout 40]
  python scripts/jenkins.py wait JOB --build N [--timeout 40]
  python scripts/jenkins.py log JOB [--build N] [--tail 80] [--grep REGEX]

Thêm --json để lấy kết quả máy đọc được. Mã thoát: 0 = thành công, 1 = build không SUCCESS
hoặc hết giờ chờ, 2 = lỗi cấu hình/kết nối/quyền.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time

from jenkins_client import JenkinsClient, JenkinsError, job_path

BUILD_TREE = ("number,url,result,building,timestamp,duration,estimatedDuration,"
              "actions[lastBuiltRevision[SHA1,branch[name]],parameters[name,value],causes[shortDescription]]")
MARKERS = re.compile(r"^\s*(Build tag|Image name)\s*:\s*(\S+)", re.M)
CHECKOUT = re.compile(r"Checking out Revision ([0-9a-f]{7,40}) \(([^)]+)\)")
PROD_JOB = re.compile(r"(^|[_\-/])PROD([_\-/]|$)", re.I)
DEMO_JOB = re.compile(r"(^|[_\-/])DEMO([_\-/]|$)", re.I)


def fmt_time(ms: int | None) -> str:
    if not ms:
        return "-"
    return dt.datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M:%S")


def fmt_dur(ms: int | None) -> str:
    if not ms:
        return "-"
    s = int(ms / 1000)
    return f"{s // 60}m{s % 60:02d}s"


def summarize(client: JenkinsClient, job: str, build: dict, with_markers: bool = True) -> dict:
    out = {
        "job": job,
        "number": build.get("number"),
        "result": "BUILDING" if build.get("building") else build.get("result"),
        "started": fmt_time(build.get("timestamp")),
        "duration": fmt_dur(build.get("duration") or None),
        "url": build.get("url"),
        "revision": None,
        "branch": None,
        "parameters": {},
        "cause": None,
        "markers": {},
    }
    for action in build.get("actions") or []:
        rev = action.get("lastBuiltRevision")
        if rev:
            out["revision"] = rev.get("SHA1")
            out["branch"] = ", ".join(b["name"] for b in rev.get("branch") or [])
        for p in action.get("parameters") or []:
            out["parameters"][p["name"]] = p.get("value")
        for c in action.get("causes") or []:
            out["cause"] = c.get("shortDescription")
    if with_markers and not build.get("building"):
        text = client.get_text(f"{job_path(job)}/{build['number']}/consoleText")
        out["markers"] = {k: v for k, v in MARKERS.findall(text)}
        if not out["revision"]:
            m = CHECKOUT.search(text)
            if m:
                out["revision"], out["branch"] = m.group(1), m.group(2)
    return out


def print_summary(s: dict) -> None:
    line = f"{s['job']} #{s['number']} {s['result']} | bắt đầu {s['started']} | {s['duration']}"
    print(line)
    if s["revision"]:
        print(f"  commit {s['revision'][:12]} ({s['branch']})")
    for k, v in s["markers"].items():
        print(f"  {k}: {v}")
    if s["parameters"]:
        print("  tham số: " + ", ".join(f"{k}={v}" for k, v in s["parameters"].items()))
    if s["cause"]:
        print(f"  kích bởi: {s['cause']}")


def tail_log(client: JenkinsClient, job: str, number: int, lines: int, grep: str | None = None) -> str:
    text = client.get_text(f"{job_path(job)}/{number}/consoleText")
    rows = text.splitlines()
    if grep:
        rx = re.compile(grep, re.I)
        rows = [r for r in rows if rx.search(r)]
    return "\n".join(rows[-lines:])


def cmd_jobs(client: JenkinsClient, args) -> int:
    view = args.view or client.default_view
    base = f"view/{view}/" if view else ""
    data = client.get_json(base + "api/json",
                           "jobs[name,color,lastBuild[number,result,building,timestamp,duration]]")
    rows = []
    for j in data.get("jobs", []):
        b = j.get("lastBuild") or {}
        rows.append({
            "job": j["name"],
            "number": b.get("number"),
            "result": "BUILDING" if b.get("building") else b.get("result"),
            "started": fmt_time(b.get("timestamp")),
            "duration": fmt_dur(b.get("duration")),
        })
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    width = max((len(r["job"]) for r in rows), default=10)
    print(f"View: {view or '(gốc)'}")
    for r in rows:
        print(f"  {r['job']:<{width}}  #{r['number'] or '-':<5} {str(r['result']):<9} {r['started']}  {r['duration']}")
    return 0


def cmd_views(client: JenkinsClient, args) -> int:
    views = client.get_json("api/json", "views[name,jobs[name]]").get("views", [])
    rows = [{"view": v["name"], "jobs": [j["name"] for j in v.get("jobs", [])]} for v in views]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    for r in rows:
        print(f"{r['view']} ({len(r['jobs'])} job)")
    return 0


def get_build(client: JenkinsClient, job: str, number: int | None) -> dict:
    ref = str(number) if number else "lastBuild"
    return client.get_json(f"{job_path(job)}/{ref}/api/json", BUILD_TREE)


def cmd_status(client: JenkinsClient, args) -> int:
    s = summarize(client, args.job, get_build(client, args.job, args.build))
    if args.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
    else:
        print_summary(s)
    return 0 if s["result"] in ("SUCCESS", "BUILDING") else 1


def resolve_queue(client: JenkinsClient, location: str, deadline: float) -> int:
    """Chờ hàng đợi Jenkins giao số build cho lần kích."""
    while time.time() < deadline:
        item = client.get_json(location.rstrip("/") + "/api/json", "cancelled,why,executable[number]")
        if item.get("cancelled"):
            raise JenkinsError("Build bị huỷ khi còn trong hàng đợi.")
        if item.get("executable"):
            return item["executable"]["number"]
        time.sleep(3)
    raise JenkinsError("Hết giờ chờ hàng đợi Jenkins giao số build.")


def wait_build(client: JenkinsClient, job: str, number: int, deadline: float, quiet: bool) -> dict:
    last = None
    while True:
        b = get_build(client, job, number)
        if not b.get("building"):
            return b
        if time.time() >= deadline:
            return b
        if not quiet:
            elapsed = int((time.time() * 1000 - b["timestamp"]) / 1000)
            msg = f"  … {job} #{number} đang build ({elapsed // 60}m{elapsed % 60:02d}s"
            if b.get("estimatedDuration", -1) > 0:
                msg += f" / ước tính {fmt_dur(b['estimatedDuration'])}"
            msg += ")"
            if msg != last:
                print(msg, flush=True)
                last = msg
        time.sleep(15)


def finish_report(client: JenkinsClient, summaries: list[dict], as_json: bool, fail_tail: int) -> int:
    ok = all(s["result"] == "SUCCESS" for s in summaries)
    if as_json:
        print(json.dumps(summaries, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    for s in summaries:
        print_summary(s)
        if s["result"] not in ("SUCCESS", "BUILDING"):
            print(f"  --- {fail_tail} dòng log cuối ---")
            print(tail_log(client, s["job"], s["number"], fail_tail))
        elif s["result"] == "BUILDING":
            print("  (hết giờ chờ, build vẫn đang chạy)")
    return 0 if ok else 1


def cmd_build(client: JenkinsClient, args) -> int:
    params = {}
    for p in args.param or []:
        if "=" not in p:
            raise JenkinsError(f"Tham số sai dạng KEY=VALUE: {p}")
        k, v = p.split("=", 1)
        params[k] = v
    prod = [j for j in args.jobs if PROD_JOB.search(j) and not DEMO_JOB.search(j)]
    if prod and not args.allow_prod:
        raise JenkinsError("Job production cần --allow-prod (chỉ dùng khi người dùng yêu cầu rõ build production): "
                           + ", ".join(prod))
    manual_sql = [j for j in args.jobs if client.manual_sql_jobs and re.search(client.manual_sql_jobs, j, re.I)]
    if manual_sql and not args.json:
        print("CHÚ Ý: môi trường của " + ", ".join(manual_sql) + " không tự chạy migration. Bản mới có migration "
              "mà chưa chạy SQL tay thì pod vẫn Ready nhưng lỗi SQL lúc chạy; kiểm deploy bằng rancher-watch `watch`.",
              flush=True)
    deadline = time.time() + args.timeout * 60
    started = []
    for job in args.jobs:
        defs = client.get_json(job_path(job) + "/api/json", "property[parameterDefinitions[name]]")
        has_params = any(prop.get("parameterDefinitions") for prop in defs.get("property") or [])
        if params and not has_params:
            raise JenkinsError(f"{job} không khai báo tham số nhưng lệnh có -p.")
        endpoint = "buildWithParameters" if has_params else "build"
        status, location = client.post(f"{job_path(job)}/{endpoint}", params if has_params else None)
        if status not in (200, 201) or "/queue/item/" not in location:
            raise JenkinsError(f"{job}: Jenkins không nhận lệnh build (HTTP {status}).")
        number = resolve_queue(client, location, deadline)
        print(f"Đã kích {job} -> #{number}", flush=True)
        started.append((job, number))
    if not args.wait:
        return 0
    summaries = []
    for job, number in started:
        b = wait_build(client, job, number, deadline, args.json)
        summaries.append(summarize(client, job, b))
    return finish_report(client, summaries, args.json, args.fail_tail)


def cmd_wait(client: JenkinsClient, args) -> int:
    deadline = time.time() + args.timeout * 60
    b = wait_build(client, args.job, args.build, deadline, args.json)
    return finish_report(client, [summarize(client, args.job, b)], args.json, args.fail_tail)


def cmd_log(client: JenkinsClient, args) -> int:
    number = args.build or get_build(client, args.job, None)["number"]
    print(tail_log(client, args.job, number, args.tail, args.grep))
    return 0


def main() -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="in JSON")
    ap = argparse.ArgumentParser(description="Jenkins: xem job, kích build, chờ kết quả.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub_parser = lambda name, **kw: sub.add_parser(name, parents=[common], **kw)  # noqa: E731

    sub_parser("views", help="liệt kê view (thường mỗi view là một môi trường)")

    p = sub_parser("jobs", help="liệt kê job và build cuối")
    p.add_argument("--view", help="tên view (mặc định JENKINS_DEFAULT_VIEW)")

    p = sub_parser("status", help="chi tiết một build")
    p.add_argument("job")
    p.add_argument("--build", type=int, help="số build (mặc định build cuối)")

    p = sub_parser("build", help="kích build (thao tác GHI)")
    p.add_argument("jobs", nargs="+")
    p.add_argument("-p", "--param", action="append", help="KEY=VALUE cho job có tham số")
    p.add_argument("--wait", action="store_true", help="chờ build xong rồi báo kết quả")
    p.add_argument("--timeout", type=int, default=40, help="phút chờ tối đa (mặc định 40)")
    p.add_argument("--fail-tail", type=int, default=60, help="số dòng log in ra khi build lỗi")
    p.add_argument("--allow-prod", action="store_true", help="cho phép job production (tên có PROD, không có DEMO)")

    p = sub_parser("wait", help="chờ một build đang chạy")
    p.add_argument("job")
    p.add_argument("--build", type=int, required=True)
    p.add_argument("--timeout", type=int, default=40)
    p.add_argument("--fail-tail", type=int, default=60)

    p = sub_parser("log", help="đoạn cuối log build")
    p.add_argument("job")
    p.add_argument("--build", type=int)
    p.add_argument("--tail", type=int, default=80)
    p.add_argument("--grep", help="chỉ giữ dòng khớp regex (không phân biệt hoa thường)")

    args = ap.parse_args()
    try:
        client = JenkinsClient()
        return {"views": cmd_views, "jobs": cmd_jobs, "status": cmd_status, "build": cmd_build,
                "wait": cmd_wait, "log": cmd_log}[args.cmd](client, args)
    except JenkinsError as e:
        print(f"LỖI: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
