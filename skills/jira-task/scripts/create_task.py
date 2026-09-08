import os
import sys
import json
import argparse
from jira_api import JiraClient

PROFILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "project-profiles.json")

def load_profiles():
    if os.path.isfile(PROFILES_PATH):
        try:
            with open(PROFILES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"defaultProfile": "CCDT", "profiles": {}}

def main():
    parser = argparse.ArgumentParser(description="Create a new Jira issue")
    parser.add_argument("summary", help="Issue summary / title")
    parser.add_argument("--project", "-p", help="Project key (default from project-profiles.json, e.g. CCDT)")
    parser.add_argument("--type", "-t", help="Issue type (Bug, Task, Sub-task, Story)")
    parser.add_argument("--desc", "-d", default="", help="Issue description (markdown)")
    parser.add_argument("--assignee", "-a", help="Assignee username")
    parser.add_argument("--priority", help="Priority (e.g. High, Medium, Low)")
    parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--parent", help="Parent issue key if creating a Sub-task (e.g. CCDT-45)")
    parser.add_argument("--components", "-c", nargs="*", help="Component names")
    parser.add_argument("--labels", "-l", nargs="*", help="Labels")
    args = parser.parse_args()

    profiles_data = load_profiles()
    default_proj = profiles_data.get("defaultProfile", "CCDT")
    proj_key = (args.project or default_proj).upper()
    proj_cfg = profiles_data.get("profiles", {}).get(proj_key, {})

    issue_type = args.type or proj_cfg.get("default_issue_type", "Task")
    if args.parent and not args.type:
        issue_type = "Sub-task"

    components = args.components if args.components is not None else proj_cfg.get("components", [])

    additional_fields = {}
    if args.labels:
        additional_fields["labels"] = args.labels
    elif "default_additional_fields" in proj_cfg and "labels" in proj_cfg["default_additional_fields"]:
        additional_fields["labels"] = proj_cfg["default_additional_fields"]["labels"]

    if args.parent:
        additional_fields["parent"] = {"key": args.parent.upper()}

    client = JiraClient()
    print("=" * 80)
    print(f" CREATING ISSUE IN PROJECT: {proj_key}")
    print(f" Summary    : {args.summary}")
    print(f" Type       : {issue_type}")
    print(f" Assignee   : {args.assignee or client.username or 'Unassigned'}")
    print(f" Priority   : {args.priority or 'Default'}")
    if args.parent:
        print(f" Parent     : {args.parent.upper()}")
    print("=" * 80)

    try:
        res = client.create_issue(
            project_key=proj_key,
            summary=args.summary,
            issue_type=issue_type,
            description=args.desc,
            assignee=args.assignee or client.username,
            priority=args.priority,
            components=components,
            duedate=args.due,
            additional_fields=additional_fields if additional_fields else None
        )
        key = res.get("key")
        print(f"\n[SUCCESS] Created issue: {key}")
        print(f"URL: {client.base_url}/browse/{key}")
    except Exception as e:
        print(f"[ERROR] Failed to create issue: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
