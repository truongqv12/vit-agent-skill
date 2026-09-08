import sys
import json
import argparse
from jira_api import JiraClient

def main():
    parser = argparse.ArgumentParser(description="Query and list Jira issues")
    parser.add_argument("--mine", action="store_true", help="List my open/unresolved tasks")
    parser.add_argument("--project", "-p", help="Filter by project key (e.g. CCDT)")
    parser.add_argument("--assignee", "-a", help="Filter by assignee username")
    parser.add_argument("--unresolved", action="store_true", default=True, help="Only unresolved issues")
    parser.add_argument("--all-status", action="store_true", help="Include resolved/closed issues")
    parser.add_argument("--due", help="Due date filter (e.g. '3d' or '2026-09-30')")
    parser.add_argument("--jql", help="Direct JQL query string")
    parser.add_argument("--limit", "-l", type=int, default=50, help="Maximum number of issues (default: 50)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format")
    args = parser.parse_args()

    client = JiraClient()
    if not client.username and not client.pat:
        print("[ERROR] Neither JIRA_USERNAME nor JIRA_PAT configured in .env", file=sys.stderr)
        sys.exit(1)

    # Build JQL
    if args.jql:
        jql = args.jql
    else:
        conditions = []
        if args.mine:
            conditions.append("assignee = currentUser()")
        elif args.assignee:
            conditions.append(f'assignee = "{args.assignee}"')

        if args.project:
            conditions.append(f'project = "{args.project.upper()}"')

        if not args.all_status:
            conditions.append("resolution = Unresolved")

        if args.due:
            if args.due.endswith("d") or args.due.endswith("w"):
                conditions.append(f"duedate <= {args.due}")
            else:
                conditions.append(f'duedate <= "{args.due}"')

        if not conditions:
            # Default fallback: mine
            conditions.append("assignee = currentUser() AND resolution = Unresolved")

        jql = " AND ".join(conditions) + " ORDER BY updated DESC"

    fields = ["summary", "status", "priority", "issuetype", "assignee", "duedate", "updated"]

    try:
        data = client.search_issues(jql, fields=fields, max_results=args.limit)
        total = data.get("total", 0)
        issues = data.get("issues", [])

        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return

        print("=" * 110)
        print(f" JIRA TASK LIST ({len(issues)}/{total} issues) | JQL: {jql}")
        print("=" * 110)
        print(f"{'STT':<4} | {'KEY':<11} | {'LOẠI':<10} | {'TRẠNG THÁI':<15} | {'HẠN (DUE)':<11} | {'SUMMARY'}")
        print("-" * 110)

        for idx, issue in enumerate(issues, start=1):
            key = issue.get("key", "")
            f = issue.get("fields", {})
            itype = f.get("issuetype", {}).get("name", "Task")[:9]
            status = f.get("status", {}).get("name", "N/A")[:14]
            due = f.get("duedate") or "N/A"
            summary = f.get("summary", "")
            if len(summary) > 52:
                summary = summary[:49] + "..."

            print(f"{idx:<4} | {key:<11} | {itype:<10} | {status:<15} | {due:<11} | {summary}")

        print("-" * 110)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
