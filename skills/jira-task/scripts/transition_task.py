import os
import sys
import time
import json
import argparse
from jira_api import JiraClient

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transitions_cache.json")

# Default known transitions for VNPT Jira (CCDT workflow)
DEFAULT_TRANSITIONS = {
    "CCDT": {
        ("Open", "Resolved"): {"id": "131", "resolution": "Done"},
        ("Mở", "Đã giải quyết"): {"id": "131", "resolution": "Done"},
        ("Mở", "Resolved"): {"id": "131", "resolution": "Done"},
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

def transition_single_issue(client, issue_key, target_input, res_val, comment, force_refresh, cache, prefetched_issue=None):
    project_key = issue_key.split("-")[0]
    proj_cache = cache.setdefault(project_key, {})

    current_issue = prefetched_issue
    if not current_issue:
        try:
            current_issue = client.get_issue(issue_key, fields="status,resolution,summary")
        except Exception as e:
            print(f"[ERROR] Could not fetch issue {issue_key}: {e}", file=sys.stderr)
            return False

    cur_status = current_issue.get("fields", {}).get("status", {}).get("name", "Unknown")
    cur_res = current_issue.get("fields", {}).get("resolution", {})
    cur_res_name = cur_res.get("name", "Unresolved") if cur_res else "Unresolved"
    summary = current_issue.get("fields", {}).get("summary", "")

    print("\n" + "=" * 80)
    print(f" 📌 ISSUE: [{issue_key}] {summary}")
    print(f" Current Status     : {cur_status}")
    print(f" Current Resolution : {cur_res_name}")
    print("-" * 80)

    target_norm = normalize_status(target_input)
    actual_res_val = res_val or ("Done" if target_norm in ("resolve", "resolved", "done") else None)

    transition_id = None
    target_status_name = target_input

    # Check shortcuts
    if target_norm in ("resolve", "resolved", "done"):
        target_status_name = "Resolved"
        if not force_refresh:
            if cur_status in ("Open", "Mở"):
                transition_id = "131"
            elif proj_cache.get(f"{cur_status}->Resolved"):
                transition_id = proj_cache[f"{cur_status}->Resolved"]

    elif target_norm in ("close", "closed"):
        target_status_name = "Closed"
        if not force_refresh and proj_cache.get(f"{cur_status}->Closed"):
            transition_id = proj_cache[f"{cur_status}->Closed"]

    elif target_norm in ("start", "progress", "in progress"):
        target_status_name = "In Progress"
        if not force_refresh and proj_cache.get(f"{cur_status}->In Progress"):
            transition_id = proj_cache[f"{cur_status}->In Progress"]

    elif target_norm in ("reopen", "reopened", "open"):
        target_status_name = "Open"
        if not force_refresh and proj_cache.get(f"{cur_status}->Open"):
            transition_id = proj_cache[f"{cur_status}->Open"]

    # If already in target status and resolution matches
    if normalize_status(cur_status) == normalize_status(target_status_name):
        if not actual_res_val or (cur_res and normalize_status(cur_res.get("name")) == normalize_status(actual_res_val)):
            print(f" [INFO] Issue {issue_key} is ALREADY in status '{cur_status}' with resolution '{cur_res_name}'. Skipping.")
            return True

    # Try executing with cached ID first if available
    executed = False
    if transition_id:
        print(f"[+] Using cached transition ID {transition_id} for '{cur_status}' -> '{target_status_name}'...")
        fields = {"resolution": {"name": actual_res_val}} if actual_res_val else None
        try:
            client.transition_issue(issue_key, transition_id, fields=fields, comment=comment)
            executed = True
        except Exception as e:
            print(f"[!] Cached transition ID {transition_id} failed ({e}). Falling back to discovery...", file=sys.stderr)
            transition_id = None

    # Fallback to dynamic discovery
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
            print(f"Available transitions: {', '.join(avail)}", file=sys.stderr)
            return False

        transition_id = matched["id"]
        target_status_name = matched.get("to", {}).get("name", target_status_name)
        print(f"[+] Found matching transition: '{matched['name']}' (ID: {transition_id}) -> '{target_status_name}'")

        fields = {"resolution": {"name": actual_res_val}} if actual_res_val else None
        try:
            client.transition_issue(issue_key, transition_id, fields=fields, comment=comment)
            proj_cache[f"{cur_status}->{target_status_name}"] = str(transition_id)
            save_cache(cache)
            print(f"[+] Cached transition ID {transition_id} for future use.")
        except Exception as e:
            print(f"[ERROR] Transition failed: {e}", file=sys.stderr)
            return False

    # Verify after transition
    updated_issue = client.get_issue(issue_key, fields="status,resolution")
    new_status = updated_issue.get("fields", {}).get("status", {}).get("name", "Unknown")
    new_res = updated_issue.get("fields", {}).get("resolution", {})
    new_res_name = new_res.get("name", "None") if new_res else "None"

    print(f" [SUCCESS] Issue {issue_key} transitioned successfully!")
    print(f" Status     : {cur_status} ──▶ {new_status}")
    print(f" Resolution : {cur_res_name} ──▶ {new_res_name}")
    print("=" * 80)
    return True

def main():
    parser = argparse.ArgumentParser(description="Transition issue status with fast transition ID caching")
    parser.add_argument("keys", nargs="+", help="One or more issue keys (e.g. CCDT-99 or CCDT-33 CCDT-43 CCDT-103)")
    parser.add_argument("--to", "-t", help="Target status or shortcut (resolve, close, start, reopen, or exact status name)")
    parser.add_argument("--resolution", "-r", help="Resolution name (default 'Done' when resolving)")
    parser.add_argument("--comment", "-c", help="Optional comment to add during transition")
    parser.add_argument("--list", "-l", action="store_true", help="List available transitions from current status (first key)")
    parser.add_argument("--force-refresh", action="store_true", help="Bypass cache and fetch transitions from Jira")
    parser.add_argument("--delay", "-d", type=float, default=6.0, help="Seconds to wait between issues in batch mode (default: 6.0s)")
    args = parser.parse_args()

    client = JiraClient()
    raw_keys = []
    for k in args.keys:
        for sub_k in k.replace(",", " ").split():
            clean = sub_k.strip().upper()
            if clean and clean not in raw_keys:
                raw_keys.append(clean)

    if not raw_keys:
        return

    # If --list is requested
    if args.list or not args.to:
        first_key = raw_keys[0]
        issue = client.get_issue(first_key, fields="status,summary")
        cur_status = issue.get("fields", {}).get("status", {}).get("name", "Unknown")
        print("=" * 80)
        print(f" Available transitions for [{first_key}] from status '{cur_status}':")
        print("=" * 80)
        transitions = client.get_transitions(first_key)
        if not transitions:
            print(f" [!] No transitions available from '{cur_status}'.")
            return
        print(f"{'ID':<8} | {'TRANSITION NAME':<25} | {'TARGET STATUS'}")
        print("-" * 60)
        for t in transitions:
            print(f"{t.get('id'):<8} | {t.get('name'):<25} | {t.get('to', {}).get('name')}")
        print("-" * 60)
        return

    cache = load_cache()
    success_count = 0
    total = len(raw_keys)

    # Optimization: Prefetch all issue statuses in 1 JQL call to eliminate redundant requests
    prefetched = {}
    if total > 1:
        try:
            jql = f"key in ({', '.join(raw_keys)})"
            res = client.search_issues(jql, fields="status,resolution,summary", max_results=total + 10)
            for iss in res.get("issues", []):
                prefetched[iss.get("key", "").upper()] = iss
        except Exception:
            pass

    print(f"\n[+] Processing {total} issue(s) to transition to '{args.to}' (Delay: {args.delay}s/task)...")
    for idx, k in enumerate(raw_keys, start=1):
        ok = transition_single_issue(
            client=client,
            issue_key=k,
            target_input=args.to,
            res_val=args.resolution,
            comment=args.comment,
            force_refresh=args.force_refresh,
            cache=cache,
            prefetched_issue=prefetched.get(k)
        )
        if ok:
            success_count += 1

        if idx < total:
            time.sleep(args.delay)

    print(f"\n[SUMMARY] Successfully processed {success_count}/{total} issues.")

if __name__ == "__main__":
    main()
