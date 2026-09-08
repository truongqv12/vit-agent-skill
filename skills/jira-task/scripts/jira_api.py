import os
import sys
import io
import time
import json
import base64
import requests
import urllib3

# Ensure UTF-8 output on Windows console
if sys.stdout and hasattr(sys.stdout, "buffer"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

urllib3.disable_warnings()


def find_env_file():
    """Find .env file in multiple likely locations: cwd, script dir, parent dir, or user home."""
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        os.path.expanduser("~/.gemini/config/skills/jira-task/.env"),
        "D:\\tools\\.env",
    ]
    for p in candidates:
        norm = os.path.normpath(p)
        if os.path.isfile(norm):
            return norm
    return None


def load_config(env_path=None):
    """Load configuration from .env or environment variables."""
    config = {}
    target_path = env_path or find_env_file()
    if target_path and os.path.exists(target_path):
        with open(target_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")

    # Priority: System env > .env file > default
    base_url = os.environ.get("JIRA_BASE_URL") or config.get("JIRA_BASE_URL") or "https://cntt.vnpt.vn"
    username = os.environ.get("JIRA_USERNAME") or config.get("JIRA_USERNAME") or ""
    password = os.environ.get("JIRA_PASSWORD") or config.get("JIRA_PASSWORD") or ""
    pat = os.environ.get("JIRA_PAT") or os.environ.get("JIRA_API_TOKEN") or config.get("JIRA_PAT") or config.get("JIRA_API_TOKEN") or ""
    cookie = os.environ.get("JIRA_COOKIE") or config.get("JIRA_COOKIE") or ""
    ignore_ssl = os.environ.get("IGNORE_SSL_WARNINGS", config.get("IGNORE_SSL_WARNINGS", "true")).lower() in ("true", "1", "yes")

    return {
        "base_url": base_url.rstrip("/"),
        "username": username,
        "password": password,
        "pat": pat,
        "cookie": cookie,
        "ignore_ssl": ignore_ssl,
        "env_file": target_path
    }


class JiraClient:
    """Robust Jira REST client with automatic rate-limit backoff and auth fallback."""

    def __init__(self, config=None, min_interval=1.0, max_retries=3):
        self.config = config or load_config()
        self.base_url = self.config["base_url"]
        self.username = self.config["username"]
        self.password = self.config["password"]
        self.pat = self.config["pat"]
        self.verify_ssl = not self.config["ignore_ssl"]
        self.min_interval = min_interval
        self.max_retries = max_retries
        self.last_request_time = 0.0

        self.session = requests.Session()
        self.session.verify = self.verify_ssl

        # Setup auth headers
        if self.pat and self.pat not in (self.password, "your_token"):
            self.session.headers.update({
                "Authorization": f"Bearer {self.pat}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            })
        elif self.config["cookie"]:
            self.session.cookies.set("JSESSIONID", self.config["cookie"])
            self.session.headers.update({
                "Content-Type": "application/json",
                "Accept": "application/json"
            })
        elif self.username and self.password:
            auth_str = f"{self.username}:{self.password}"
            auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            self.session.headers.update({
                "Authorization": f"Basic {auth_b64}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            })

    def _throttle(self):
        """Ensure minimum interval between requests to prevent triggering rate-limiting."""
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def request(self, method, endpoint, **kwargs):
        """Execute request with rate-limit detection and automatic retry."""
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", 30)

        for attempt in range(1, self.max_retries + 1):
            self._throttle()
            try:
                res = self.session.request(method, url, **kwargs)

                # Check if hit rate-limit or temporary 401
                if res.status_code == 401:
                    err_text = res.text
                    # Detect rate-limit cooldown
                    if "OTP_REQUIRED" in err_text or "rate limit" in err_text.lower():
                        if attempt < self.max_retries:
                            wait_sec = 15
                            print(f"[!] Jira VNPT rate-limit detected (401/OTP). Waiting {wait_sec}s before retry ({attempt}/{self.max_retries})...", file=sys.stderr)
                            time.sleep(wait_sec)
                            continue

                return res

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt < self.max_retries:
                    wait_sec = 3 * attempt
                    print(f"[!] Network warning: {e}. Retrying in {wait_sec}s...", file=sys.stderr)
                    time.sleep(wait_sec)
                else:
                    raise e

        return res

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def search_issues(self, jql, fields=None, max_results=50, start_at=0):
        params = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at
        }
        if fields:
            params["fields"] = fields if isinstance(fields, str) else ",".join(fields)

        res = self.get("/rest/api/2/search", params=params)
        if res.ok:
            return res.json()
        raise RuntimeError(f"Search failed ({res.status_code}): {res.text}")

    def get_issue(self, key, fields=None):
        params = {}
        if fields:
            params["fields"] = fields if isinstance(fields, str) else ",".join(fields)
        res = self.get(f"/rest/api/2/issue/{key}", params=params)
        if res.ok:
            return res.json()
        raise RuntimeError(f"Get issue {key} failed ({res.status_code}): {res.text}")

    def get_transitions(self, key):
        res = self.get(f"/rest/api/2/issue/{key}/transitions")
        if res.ok:
            return res.json().get("transitions", [])
        raise RuntimeError(f"Get transitions for {key} failed ({res.status_code}): {res.text}")

    def transition_issue(self, key, transition_id, fields=None, comment=None):
        payload = {
            "transition": {"id": str(transition_id)}
        }
        if fields:
            payload["fields"] = fields
        if comment:
            payload["update"] = {
                "comment": [{"add": {"body": comment}}]
            }
        res = self.post(f"/rest/api/2/issue/{key}/transitions", json=payload)
        if res.status_code in (200, 204):
            return True
        raise RuntimeError(f"Transition {key} to {transition_id} failed ({res.status_code}): {res.text}")

    def add_worklog(self, key, time_spent, comment="", started=None):
        payload = {
            "timeSpent": time_spent,
            "comment": comment
        }
        if started:
            payload["started"] = started
        res = self.post(f"/rest/api/2/issue/{key}/worklog", json=payload)
        if res.status_code in (200, 201):
            return res.json()
        raise RuntimeError(f"Add worklog to {key} failed ({res.status_code}): {res.text}")

    def get_worklogs(self, key):
        res = self.get(f"/rest/api/2/issue/{key}/worklog")
        if res.ok:
            return res.json().get("worklogs", [])
        raise RuntimeError(f"Get worklogs for {key} failed ({res.status_code}): {res.text}")

    def create_issue(self, project_key, summary, issue_type="Task", description="", assignee=None, priority=None, components=None, duedate=None, additional_fields=None):
        fields = {
            "project": {"key": project_key.upper()},
            "summary": summary,
            "issuetype": {"name": issue_type}
        }
        if description:
            fields["description"] = description
        if assignee:
            fields["assignee"] = {"name": assignee}
        if priority:
            fields["priority"] = {"name": priority}
        if duedate:
            fields["duedate"] = duedate
        if components:
            fields["components"] = [{"name": c} for c in components]
        if additional_fields:
            fields.update(additional_fields)

        res = self.post("/rest/api/2/issue", json={"fields": fields})
        if res.status_code in (200, 201):
            return res.json()
        raise RuntimeError(f"Create issue failed ({res.status_code}): {res.text}")

    def update_issue(self, key, fields):
        res = self.put(f"/rest/api/2/issue/{key}", json={"fields": fields})
        if res.status_code in (200, 204):
            return True
        raise RuntimeError(f"Update issue {key} failed ({res.status_code}): {res.text}")
