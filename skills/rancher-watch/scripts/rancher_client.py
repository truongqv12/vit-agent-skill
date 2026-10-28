"""Rancher / Kubernetes REST client chỉ đọc, dùng chung cho rancher.py (thư viện chuẩn Python 3.8+)."""

from __future__ import annotations

import io
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

if sys.stdout and hasattr(sys.stdout, "buffer") and (sys.stdout.encoding or "").lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SKILL_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
KEYS = ("RANCHER_URL", "RANCHER_TOKEN", "RANCHER_USER", "RANCHER_PASSWORD",
        "RANCHER_CLUSTER", "RANCHER_NAMESPACE", "RANCHER_INSECURE")


class RancherError(Exception):
    """Lỗi gọi Rancher; message không bao giờ chứa token."""


def _read_env_file(path: str) -> dict:
    values = {}
    if not os.path.isfile(path):
        return values
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            val = val.strip().strip('"').strip("'")
            if val:
                values[key.strip()] = val
    return values


def load_config(profile: str | None = None) -> dict:
    """Không profile: biến môi trường > .env ở thư mục đang đứng > .env của skill.

    Có profile (mỗi Rancher một profile, vd `prod`): chỉ đọc .env.<profile> của skill rồi của thư mục
    đang đứng, bỏ qua biến môi trường RANCHER_* để không lỡ trỏ sang Rancher khác.
    """
    profile = profile or os.environ.get("RANCHER_PROFILE") or None
    name = f".env.{profile}" if profile else ".env"
    merged = {"RANCHER_CLUSTER": "local"}
    found = [p for p in (os.path.join(SKILL_DIR, name), os.path.join(os.getcwd(), name)) if os.path.isfile(p)]
    for path in found:
        merged.update(_read_env_file(path))
    if profile and not found:
        raise RancherError(f"Không thấy file {name} cho profile '{profile}' (đặt trong thư mục skill).")
    if not profile:
        for key in KEYS:
            if os.environ.get(key):
                merged[key] = os.environ[key]
    if not merged.get("RANCHER_URL"):
        raise RancherError(f"Thiếu RANCHER_URL (đặt trong {name} của skill hoặc biến môi trường).")
    if not merged.get("RANCHER_TOKEN") and not (merged.get("RANCHER_USER") and merged.get("RANCHER_PASSWORD")):
        raise RancherError("Thiếu RANCHER_TOKEN (hoặc cặp RANCHER_USER/RANCHER_PASSWORD).")
    return merged


class RancherClient:
    def __init__(self, config: dict | None = None, profile: str | None = None):
        cfg = config or load_config(profile)
        self.base = cfg["RANCHER_URL"].rstrip("/")
        self.cluster = cfg["RANCHER_CLUSTER"]
        self.default_namespace = cfg.get("RANCHER_NAMESPACE", "")
        self._ctx = ssl._create_unverified_context() if cfg.get("RANCHER_INSECURE", "").lower() in ("1", "true", "yes") else None
        self._token = cfg.get("RANCHER_TOKEN") or self._login(cfg["RANCHER_USER"], cfg["RANCHER_PASSWORD"])
        self._temporary = not cfg.get("RANCHER_TOKEN")

    def _open(self, req: urllib.request.Request, timeout: int = 60):
        try:
            return urllib.request.urlopen(req, timeout=timeout, context=self._ctx)
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = json.loads(e.read().decode("utf-8")).get("message", "")
            except Exception:
                pass
            path = urllib.parse.urlsplit(req.full_url).path
            if e.code == 401:
                raise RancherError(f"{path} -> HTTP 401: token sai hoặc đã hết hạn.") from None
            if e.code == 403:
                raise RancherError(f"{path} -> HTTP 403: không có quyền. {detail}".strip()) from None
            if e.code == 404:
                raise RancherError(f"{path} -> HTTP 404: không tìm thấy. {detail}".strip()) from None
            raise RancherError(f"{path} -> HTTP {e.code}. {detail}".strip()) from None
        except urllib.error.URLError as e:
            raise RancherError(f"Không kết nối được {self.base}: {e.reason}") from None

    def _login(self, user: str, password: str) -> str:
        """Đăng nhập tài khoản local lấy token tạm (TTL 1 giờ); close() sẽ thu hồi."""
        body = json.dumps({"username": user, "password": password, "responseType": "json", "ttl": 3600000}).encode()
        req = urllib.request.Request(self.base + "/v3-public/localProviders/local?action=login", data=body,
                                     method="POST", headers={"Content-Type": "application/json"})
        with self._open(req) as r:
            return json.loads(r.read().decode("utf-8"))["token"]

    def close(self) -> None:
        if self._temporary:
            req = urllib.request.Request(self.base + "/v3/tokens?action=logout", data=b"{}", method="POST",
                                         headers={"Authorization": "Bearer " + self._token,
                                                  "Content-Type": "application/json"})
            try:
                self._open(req, timeout=15).close()
            except RancherError:
                pass

    def k8s(self, path: str, params: dict | None = None, raw: bool = False):
        """GET qua proxy Kubernetes của Rancher: /k8s/clusters/<cluster>/<path>."""
        url = f"{self.base}/k8s/clusters/{self.cluster}/{path.lstrip('/')}"
        if params:
            url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + self._token,
                                                   "Accept": "*/*" if raw else "application/json"})
        with self._open(req) as r:
            data = r.read().decode("utf-8", errors="replace")
        return data if raw else json.loads(data)
