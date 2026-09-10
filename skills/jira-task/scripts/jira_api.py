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


def load_config(env_path=None):
    """Load configuration with layered fallback: skill base .env -> workspace .env -> environment variables."""
    config = {}
    skill_dir_env = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))
    user_skill_env = os.path.normpath(os.path.expanduser("~/.gemini/config/skills/jira-task/.env"))
    cwd_env = os.path.normpath(os.path.join(os.getcwd(), ".env"))

    env_paths = [user_skill_env, skill_dir_env]
    if cwd_env not in env_paths and os.path.isfile(cwd_env):
        env_paths.append(cwd_env)
    if env_path and os.path.isfile(env_path):
        env_paths.append(os.path.normpath(env_path))

    last_loaded_path = None
    for p in env_paths:
        if os.path.isfile(p):
            last_loaded_path = p
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        val = v.strip().strip('"').strip("'")
                        if val:
                            config[k.strip()] = val

    # Priority: System env > loaded config > default
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
        "env_file": last_loaded_path
    }


class JiraClient:
    """Robust Jira REST client with automatic rate-limit backoff and auth fallback."""

    def __init__(self, config=None, min_interval=1.0, max_retries=4):
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

        # Standard browser headers to avoid automated bot fingerprinting by WAF and bypass XSRF
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/secure/Tempo.jspa",
            "X-Atlassian-Token": "no-check",
            "X-Requested-With": "XMLHttpRequest"
        })

        # Setup auth headers & cookies
        if self.config.get("cookie"):
            from urllib.parse import urlparse
            host = urlparse(self.base_url).hostname
            raw_cookie = self.config["cookie"].strip()

            # Handle full cookie header (e.g. JSESSIONID=...; other=...) vs single value
            if "=" in raw_cookie:
                for part in raw_cookie.split(";"):
                    part = part.strip()
                    if "=" in part:
                        ck, cv = part.split("=", 1)
                        self.session.cookies.set(ck.strip(), cv.strip(), domain=host, path="/")
            else:
                self.session.cookies.set("JSESSIONID", raw_cookie, domain=host, path="/")

        elif self.pat and self.pat not in (self.password, "your_token"):
            self.session.headers.update({
                "Authorization": f"Bearer {self.pat}"
            })
        elif self.username and self.password:
            if not self._load_cached_session():
                self._login_web()

    def _get_cache_file(self):
        import tempfile
        return os.path.join(tempfile.gettempdir(), f".jira_session_{self.username}.json")

    def _load_cached_session(self):
        cache_file = self._get_cache_file()
        if os.path.isfile(cache_file):
            try:
                # Valid for 2 hours
                if time.time() - os.path.getmtime(cache_file) < 7200:
                    with open(cache_file, "r") as f:
                        cookies = json.load(f)
                    # Must be logged in token
                    xsrf = cookies.get("atlassian.xsrf.token", "")
                    if xsrf.endswith("_lin"):
                        from urllib.parse import urlparse
                        host = urlparse(self.base_url).hostname
                        for k, v in cookies.items():
                            self.session.cookies.set(k, v, domain=host, path="/")
                        return True
            except Exception:
                pass
        return False

    def _login_web(self):
        if not (self.username and self.password):
            return False
        try:
            res = self.session.post(
                f"{self.base_url}/login.jsp",
                data={"os_username": self.username, "os_password": self.password},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=15
            )
            cookies = self.session.cookies.get_dict()
            xsrf = cookies.get("atlassian.xsrf.token", "")
            if xsrf.endswith("_lin") or res.ok:
                try:
                    with open(self._get_cache_file(), "w") as f:
                        json.dump(cookies, f)
                except Exception:
                    pass
                return True
            return False
        except Exception:
            return False

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

                # If unauthorized, try refreshing session via login.jsp once
                if res.status_code == 401 and self.username and self.password and attempt == 1:
                    if self._login_web():
                        continue

                # Check if hit rate-limit or temporary burst restriction (429, 503, or real rate-limiting)
                if res.status_code in (401, 429, 503):
                    err_text = res.text
                    triggers = [
                        "rate limit",
                        "ratelimit",
                        "Too Many Requests"
                    ]
                    if res.status_code in (429, 503) or any(t in err_text or t in err_text.lower() for t in triggers):
                        if attempt < self.max_retries:
                            wait_sec = 15 * attempt
                            self.min_interval = max(self.min_interval, 4.0)
                            print(
                                f"[!] Jira VNPT rate-limit detected (HTTP {res.status_code}). "
                                f"Waiting {wait_sec}s cooldown before retry ({attempt}/{self.max_retries})...",
                                file=sys.stderr
                            )
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

        res = self.get("/rest/api/latest/search", params=params)
        if res.ok:
            return res.json()
        raise RuntimeError(f"Search failed ({res.status_code}): {res.text}")

    def get_issue(self, key, fields=None):
        params = {}
        if fields:
            params["fields"] = fields if isinstance(fields, str) else ",".join(fields)
        res = self.get(f"/rest/api/latest/issue/{key}", params=params)
        if res.ok:
            return res.json()
        raise RuntimeError(f"Get issue {key} failed ({res.status_code}): {res.text}")

    def get_transitions(self, key):
        res = self.get(f"/rest/api/latest/issue/{key}/transitions")
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
        res = self.post(f"/rest/api/latest/issue/{key}/transitions", json=payload)
        if res.status_code in (200, 204):
            return True
        raise RuntimeError(f"Transition {key} to {transition_id} failed ({res.status_code}): {res.text}")

    def add_worklog(self, key, time_spent, comment="", started=None):
        # Convert time_spent string to seconds (e.g. '4h', '8h', '1d', '30m')
        def parse_seconds(ts):
            sec = 0
            for part in str(ts).lower().replace(" ", "").split():
                val = ""
                for ch in part:
                    if ch.isdigit() or ch == '.':
                        val += ch
                    elif ch == 'h':
                        sec += int(float(val or 1) * 3600)
                        val = ""
                    elif ch == 'd':
                        sec += int(float(val or 1) * 8 * 3600)
                        val = ""
                    elif ch == 'm':
                        sec += int(float(val or 1) * 60)
                        val = ""
            if sec == 0:
                try:
                    sec = int(float(ts) * 3600)
                except Exception:
                    sec = 14400
            return sec

        # Try Tempo Timesheets endpoint first (works with Jira VNPT session cookie directly)
        date_started = started[:19] + ".000" if started else datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000")
        tempo_payload = {
            "issue": {"key": key.upper(), "remainingEstimateSeconds": 0},
            "timeSpentSeconds": parse_seconds(time_spent),
            "dateStarted": date_started,
            "comment": comment,
            "author": {"name": self.username}
        }
        try:
            tempo_res = self.post("/rest/tempo-timesheets/3/worklogs", json=tempo_payload)
            if tempo_res.status_code in (200, 201):
                return tempo_res.json()
        except Exception:
            pass

        # Fallback to standard Jira issue worklog endpoint
        payload = {
            "timeSpent": time_spent,
            "comment": comment
        }
        if started:
            payload["started"] = started
        res = self.post(f"/rest/api/latest/issue/{key}/worklog", json=payload)
        if res.status_code in (200, 201):
            return res.json()
        raise RuntimeError(f"Add worklog to {key} failed ({res.status_code}): {res.text}")

    def get_worklogs(self, key):
        res = self.get(f"/rest/api/latest/issue/{key}/worklog")
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

        res = self.post("/rest/api/latest/issue", json={"fields": fields})
        if res.status_code in (200, 201):
            return res.json()
        raise RuntimeError(f"Create issue failed ({res.status_code}): {res.text}")

    def update_issue(self, key, fields):
        res = self.put(f"/rest/api/latest/issue/{key}", json={"fields": fields})
        if res.status_code in (200, 204):
            return True
        raise RuntimeError(f"Update issue {key} failed ({res.status_code}): {res.text}")
