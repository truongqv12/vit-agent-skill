import sys
import argparse
from datetime import datetime, timedelta
from jira_api import JiraClient

def get_week_start(target_date=None):
    if target_date is None:
        target_date = datetime.now()
    start_of_week = target_date - timedelta(days=target_date.weekday())
    return start_of_week.strftime("%Y-%m-%d")

def main():
    parser = argparse.ArgumentParser(description="Submit Tempo timesheet for manager approval")
    parser.add_argument("reviewer", nargs="?", default="nghialt.tgg", help="Reviewer username (default: nghialt.tgg)")
    parser.add_argument("comment", nargs="?", default="Gửi duyệt chấm công tuần", help="Submission comment")
    parser.add_argument("--date", "-d", help="Start of week date YYYY-MM-DD (default: current week)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without submitting")
    parser.add_argument("--yes", "-y", action="store_true", help="Confirm immediately")
    args = parser.parse_args()

    client = JiraClient()
    username = client.username
    if not username:
        print("[ERROR] JIRA_USERNAME not found in config", file=sys.stderr)
        sys.exit(1)

    target_week_start = args.date or get_week_start()

    print("=" * 70)
    print(f"      GỬI DUYỆT TIMESHEET TUẦN (TEMPO)")
    print("=" * 70)
    print(f" • Nhân sự gửi   : {username}")
    print(f" • Người duyệt   : {args.reviewer}")
    print(f" • Tuần bắt đầu  : {target_week_start}")
    print(f" • Lời nhắn      : {args.comment}")
    print("=" * 70)

    try:
        # Get user keys
        u_res = client.get(f"/rest/api/2/user?username={username}")
        user_key = u_res.json().get("key", username) if u_res.ok else username

        r_res = client.get(f"/rest/api/2/user?username={args.reviewer}")
        reviewer_key = r_res.json().get("key", args.reviewer) if r_res.ok else args.reviewer
        reviewer_name = r_res.json().get("displayName", args.reviewer) if r_res.ok else args.reviewer

        print(f"[+] UserKey: {user_key} | Reviewer: {reviewer_name} ({reviewer_key})")

        if args.dry_run:
            print("[DRY-RUN] Kiểm tra hoàn tất, kết thúc chạy thử.")
            return

        if not args.yes:
            val = input("\nBạn có chắc chắn muốn gửi duyệt timesheet tuần này không? (y/N): ").strip().lower()
            if val not in ("y", "yes"):
                print("Đã hủy.")
                return

        payload = {
            "userKey": user_key,
            "reviewerKey": reviewer_key,
            "comment": args.comment,
            "dateFrom": target_week_start
        }
        res = client.post("/rest/tempo-timesheets/4/timesheet-approval/submit", json=payload)
        if res.status_code in (200, 204):
            print("\n[SUCCESS] Đã gửi duyệt Timesheet thành công!")
        else:
            print(f"\n[ERROR] Gửi duyệt thất bại ({res.status_code}): {res.text}")

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
