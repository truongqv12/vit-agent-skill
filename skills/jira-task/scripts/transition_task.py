import os
import sys
import json
import argparse
from jira_api import JiraClient

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transitions_cache.json")

# Default known transitions for VNPT Jira (CCDT workflow)
DEFAULT_TRANSITIONS = {
    "CCDT": {
        # Open -> Resolved
        ("Open", "Resolved"): {"id": "131", "resolution": "Done"},
        ("Mở", "Đã giải quyết"): {"id": "131", "resolution": "Done"},
        ("Mở", "Resolved"): {"id": "131", "resolution": "Done"},
        # Shortcuts
        "resolve": {"to": "Resolved", "id": "131", "resolution": "Done"},
        "done": {"to": "Resolved", "id": "131", "resolution": "Done"},
        "close": {"to": "Closed", "id": None},
        "start": {"to": "In Progress", "id": None},
        "reopen": {"to": "Reopened", "id": None}
    }
}

def load_cache():
    if os.path.isfile(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def normalize_status(name):
    return (name or "").strip().lower()

def main():
    parser = argparse.ArgumentParser(description="Transition issue status with fast transition ID caching")
    parser.add_argument("key", help="Issue key (e.g. CCDT-99)")
    parser.add_argument("--to", "-t", help="Target status or shortcut (resolve, close, start, reopen, or exact status name)")
    parser.add_argument("--resolution", "-r", help="Resolution name (default 'Done' when resolving)")
    parser.add_argument("--comment", "-c", help="Optional comment to add during transition")
    parser.add_argument("--list", "-l", action="store_true", help="List available transitions from current status")
    parser.add_argument("--force-refresh", action="store_true", help="Bypass cache and fetch transitions from Jira")
    args = parser.parse_args()

    client = JiraClient()
    issue_key = args.key.upper()
    project_key = issue_key.split("-")[0]

    # 1. Fetch current status of issue
    try:
        current_issue = client.get_issue(issue_key, fields="status,resolution,summary")
    except Exception as e:
        print(f"[ERROR] Could not fetch issue {issue_key}: {e}", file=sys.stderr)
        sys.exit(1)

    cur_status = current_issue.get("fields", {}).get("status", {}).get("name", "Unknown")
    cur_res = current_issue.get("fields", {}).get("resolution", {})
    cur_res_name = cur_res.get("name", "Unresolved") if cur_res else "Unresolved"
    summary = current_issue.get("fields", {}).get("summary", "")

    print("=" * 80)
    print(f" ISSUE: [{issue_key}] {summary}")
    print(f" Current Status     : {cur_status}")
    print(f" Current Resolution : {cur_res_name}")
    print("=" * 80)

    # 2. If user just wants to list transitions
    if args.list or not args.to:
        print(f"\n[+] Fetching available transitions from status '{cur_status}'...")
        transitions = client.get_transitions(issue_key)
        if not transitions:
            print(f" [!] No transitions available from current status '{cur_status}'.")
            return

        print(f"\n{'ID':<8} | {'TRANSITION NAME':<25} | {'TARGET STATUS'}")
        print("-" * 60)
        for t in transitions:
            tid = t.get("id")
            tname = t.get("name")
            to_name = t.get("to", {}).get("name")
            print(f"{tid:<8} | {tname:<25} | {to_name}")
        print("-" * 60)
        return

    # 3. Resolve target status and transition ID
    target_input = args.to.strip()
    target_norm = normalize_status(target_input)

    # Determine resolution
    res_val = args.resolution or ("Done" if target_norm in ("resolve", "resolved", "done") else None)

    cache = load_cache()
    proj_cache = cache.setdefault(project_key, {})
    default_proj = DEFAULT_TRANSITIONS.get(project_key, {})

    transition_id = None
    target_status_name = target_input

    # Check shortcuts
    if target_norm in ("resolve", "resolved", "done"):
        target_status_name = "Resolved"
        if not args.force_refresh:
            # Check default known ID
            if cur_status in ("Open", "Mở"):
                transition_id = "131"
            elif proj_cache.get(f"{cur_status}->Resolved"):
                transition_id = proj_cache[f"{cur_status}->Resolved"]

    elif target_norm in ("close", "closed"):
        target_status_name = "Closed"
        if not args.force_refresh and proj_cache.get(f"{cur_status}->Closed"):
            transition_id = proj_cache[f"{cur_status}->Closed"]

    elif target_norm in ("start", "progress", "in progress"):
        target_status_name = "In Progress"
        if not args.force_refresh and proj_cache.get(f"{cur_status}->In Progress"):
            transition_id = proj_cache[f"{cur_status}->In Progress"]

    elif target_norm in ("reopen", "reopened", "open"):
        target_status_name = "Open"
        if not args.force_refresh and proj_cache.get(f"{cur_status}->Open"):
            transition_id = proj_cache[f"{cur_status}->Open"]

    # 4. Try executing with cached ID first if available
    executed = False
    if transition_id:
        print(f"[+] Using cached transition ID {transition_id} for '{cur_status}' -> '{target_status_name}'...")
        fields = {"resolution": {"name": res_val}} if res_val else None
        try:
            client.transition_issue(issue_key, transition_id, fields=fields, comment=args.comment)
            executed = True
        except Exception as e:
            print(f"[!] Cached transition ID failed ({e}). Falling back to discovery...", file=sys.stderr)
            transition_id = None

    # 5. If not executed yet, discover from Jira
    if not executed:
        print(f"[+] Discovering transitions from Jira API for '{cur_status}'...")
        transitions = client.get_transitions(issue_key)
        matched = None
        for t in transitions:
            to_name = t.get("to", {}).get("name", "")
            t_name = t.get("name", "")
            if (normalize_status(to_name) == normalize_status(target_status_name) or
                normalize_status(t_name) == normalize_status(target_status_name) or
                target_norm in normalize_status(to_name) or
                target_norm in normalize_status(t_name)):
                matched = t
                break

        if not matched:
            avail = [f"{t.get('name')} -> {t.get('to',{}).get('name')} (ID: {t.get('id')})" for t in transitions]
            print(f"[ERROR] Target status '{target_status_name}' not available from '{cur_status}'.", file=sys.stderr)
            print(f"Available: {', '.join(avail)}", file=sys.stderr)
            sys.exit(1)

        transition_id = matched["id"]
        target_status_name = matched.get("to", {}).get("name", target_status_name)
        print(f"[+] Found matching transition: '{matched['name']}' (ID: {transition_id}) -> '{target_status_name}'")

        # Execute
        fields = {"resolution": {"name": res_val}} if res_val else None
        try:
            client.transition_issue(issue_key, transition_id, fields=fields, comment=args.comment)
            # Update cache on success
            proj_cache[f"{cur_status}->{target_status_name}"] = str(transition_id)
            save_cache(cache)
            print(f"[+] Cached transition ID {transition_id} for future instant use.")
        except Exception as e:
            print(f"[ERROR] Transition failed: {e}", file=sys.stderr)
            sys.exit(1)

    # 6. Verify after transition (Verification rule)
    print(f"\n[+] Verifying status after transition...")
    updated_issue = client.get_issue(issue_key, fields="status,resolution")
    new_status = updated_issue.get("fields", {}).get("status", {}).get("name", "Unknown")
    new_res = updated_issue.get("fields", {}).get("resolution", {})
    new_res_name = new_res.get("name", "None") if new_res else "None"

    print("=" * 80)
    print(f" [SUCCESS] Issue {issue_key} transitioned successfully!")
    print(f" Status     : {cur_status} ──▶ {new_status}")
    print(f" Resolution : {cur_res_name} ──▶ {new_res_name}")
    print("=" * 80)

if __name__ == "__main__":
    main()
