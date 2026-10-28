"""Jenkins REST client dùng chung cho jenkins.py (chỉ thư viện chuẩn Python 3.8+)."""

from __future__ import annotations

import base64
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


class JenkinsError(Exception):
    """Lỗi gọi Jenkins; message không bao giờ chứa token."""


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


def load_config() -> dict:
    """Thứ tự ưu tiên: biến môi trường > .env ở thư mục đang đứng > .env của skill."""
    merged = {}
    merged.update(_read_env_file(os.path.join(SKILL_DIR, ".env")))
    merged.update(_read_env_file(os.path.join(os.getcwd(), ".env")))
    for key in ("JENKINS_URL", "JENKINS_USER", "JENKINS_API_TOKEN", "JENKINS_PASSWORD",
                "JENKINS_DEFAULT_VIEW", "JENKINS_INSECURE", "JENKINS_MANUAL_SQL_JOBS"):
        if os.environ.get(key):
            merged[key] = os.environ[key]
    if not merged.get("JENKINS_URL"):
        raise JenkinsError("Thiếu JENKINS_URL (đặt trong .env của skill hoặc biến môi trường).")
    if not merged.get("JENKINS_USER") or not (merged.get("JENKINS_API_TOKEN") or merged.get("JENKINS_PASSWORD")):
        raise JenkinsError("Thiếu JENKINS_USER và JENKINS_API_TOKEN (hoặc JENKINS_PASSWORD).")
    return merged


class JenkinsClient:
    def __init__(self, config: dict | None = None):
        cfg = config or load_config()
        self.base = cfg["JENKINS_URL"].rstrip("/")
        self.default_view = cfg.get("JENKINS_DEFAULT_VIEW", "")
        # Regex tên job deploy lên môi trường không tự chạy migration (Flyway tắt).
        self.manual_sql_jobs = cfg.get("JENKINS_MANUAL_SQL_JOBS", "")
        secret = cfg.get("JENKINS_API_TOKEN") or cfg.get("JENKINS_PASSWORD")
        self._auth = "Basic " + base64.b64encode(f"{cfg['JENKINS_USER']}:{secret}".encode()).decode()
        self._uses_password = not cfg.get("JENKINS_API_TOKEN")
        self._ctx = ssl._create_unverified_context() if cfg.get("JENKINS_INSECURE", "").lower() in ("1", "true", "yes") else None
        self._crumb: dict | None = None
        cookies = urllib.request.HTTPCookieProcessor()
        handlers = [cookies] + ([urllib.request.HTTPSHandler(context=self._ctx)] if self._ctx else [])
        self._opener = urllib.request.build_opener(*handlers)

    def url(self, path: str) -> str:
        return path if path.startswith("http") else self.base + "/" + path.lstrip("/")

    def _request(self, method: str, path: str, data: bytes | None = None, headers: dict | None = None):
        req = urllib.request.Request(self.url(path), data=data, method=method)
        req.add_header("Authorization", self._auth)
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        try:
            return self._opener.open(req, timeout=60)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise JenkinsError(f"{method} {path} -> HTTP {e.code}: sai tài khoản/token hoặc không có quyền.") from None
            if e.code == 404:
                raise JenkinsError(f"{method} {path} -> HTTP 404: không tìm thấy (sai tên job/view/số build?).") from None
            raise JenkinsError(f"{method} {path} -> HTTP {e.code}") from None
        except urllib.error.URLError as e:
            raise JenkinsError(f"Không kết nối được {self.base}: {e.reason}") from None

    def get_json(self, path: str, tree: str | None = None) -> dict:
        if tree:
            path += ("&" if "?" in path else "?") + "tree=" + urllib.parse.quote(tree, safe="[],")
        with self._request("GET", path) as r:
            return json.loads(r.read().decode("utf-8"))

    def get_text(self, path: str) -> str:
        with self._request("GET", path) as r:
            return r.read().decode("utf-8", errors="replace")

    def _crumb_header(self) -> dict:
        # API token được miễn CSRF; chỉ đăng nhập bằng mật khẩu mới cần crumb cùng phiên cookie.
        if not self._uses_password:
            return {}
        if self._crumb is None:
            c = self.get_json("crumbIssuer/api/json")
            self._crumb = {c["crumbRequestField"]: c["crumb"]}
        return self._crumb

    def post(self, path: str, form: dict | None = None):
        data = urllib.parse.urlencode(form or {}).encode()
        headers = {"Content-Type": "application/x-www-form-urlencoded", **self._crumb_header()}
        with self._request("POST", path, data=data, headers=headers) as r:
            return r.status, r.headers.get("Location", "")


def job_path(name: str) -> str:
    """'folder/job' -> 'job/folder/job/job'."""
    return "/".join("job/" + urllib.parse.quote(part) for part in name.strip("/").split("/"))
