import sys
import argparse
from jira_api import JiraClient

def main():
    parser = argparse.ArgumentParser(description="Edit fields on an existing Jira issue")
    parser.add_argument("key", help="Issue key (e.g. CCDT-99)")
    parser.add_argument("--summary", "-s", help="New summary / title")
    parser.add_argument("--desc", "-d", help="New description")
    parser.add_argument("--assignee", "-a", help="New assignee username")
    parser.add_argument("--priority", "-p", help="New priority (High, Medium, Low...)")
    parser.add_argument("--due", help="New due date (YYYY-MM-DD)")
    parser.add_argument("--labels", "-l", nargs="*", help="New labels list")
    args = parser.parse_args()

    client = JiraClient()
    issue_key = args.key.upper()

    fields_to_update = {}
    if args.summary:
        fields_to_update["summary"] = args.summary
    if args.desc is not None:
        fields_to_update["description"] = args.desc
    if args.assignee:
        fields_to_update["assignee"] = {"name": args.assignee}
    if args.priority:
        fields_to_update["priority"] = {"name": args.priority}
    if args.due:
        fields_to_update["duedate"] = args.due
    if args.labels is not None:
        fields_to_update["labels"] = args.labels

    if not fields_to_update:
        print("[ERROR] No fields specified to update!", file=sys.stderr)
        sys.exit(1)

    print("=" * 70)
    print(f" UPDATING ISSUE: {issue_key}")
    for k, v in fields_to_update.items():
        print(f" • {k:<12}: {v}")
    print("=" * 70)

    try:
        client.update_issue(issue_key, fields_to_update)
        print(f"\n[SUCCESS] Issue {issue_key} updated successfully!")

        # Verify
        req_fields = ",".join(fields_to_update.keys())
        updated = client.get_issue(issue_key, fields=req_fields)
        print("[+] Verified values on Jira:")
        for k in fields_to_update.keys():
            val = updated.get("fields", {}).get(k)
            print(f"   - {k}: {val}")

    except Exception as e:
        print(f"[ERROR] Failed to update {issue_key}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
