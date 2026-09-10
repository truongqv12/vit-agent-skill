import sys
import argparse
from datetime import datetime, timedelta
from jira_api import JiraClient

def get_week_range(target_date=None):
    if target_date is None:
        target_date = datetime.now()
    start_of_week = target_date - timedelta(days=target_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return start_of_week, end_of_week

def resolve_user_key(client, username):
    cfg_key = client.config.get("user_key") or client.config.get("JIRA_USER_KEY")
    if cfg_key:
        return cfg_key
    try:
        today = datetime.now()
        past = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        now_str = today.strftime("%Y-%m-%d")
        w_res = client.session.get(
            f"{client.base_url}/rest/tempo-timesheets/3/worklogs?username={username}&dateFrom={past}&dateTo={now_str}"
        )
        if w_res.ok:
            items = w_res.json()
            if items and "author" in items[0] and "key" in items[0]["author"]:
                return items[0]["author"]["key"]
    except Exception:
        pass
    if username == "tttruong":
        return "JIRAUSER15790"
    return username

def main():
    parser = argparse.ArgumentParser(description="Submit Tempo timesheet for manager approval")
    parser.add_argument("reviewer", nargs="?", default="nghialt.tgg", help="Reviewer username (default: nghialt.tgg)")
    parser.add_argument("comment", nargs="?", default="Gửi anh duyệt chấm công tuần", help="Submission comment")
    parser.add_argument("--date", "-d", help="Date in target week YYYY-MM-DD (default: current week)")
    parser.add_argument("--last-week", "-l", action="store_true", help="Submit for last week")
    parser.add_argument("--weeks-ago", "-w", type=int, default=0, help="Weeks ago (1=last week, 2=2 weeks ago)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without submitting")
    parser.add_argument("--yes", "-y", action="store_true", help="Confirm immediately")
    args = parser.parse_args()

    client = JiraClient()
    username = client.username
    if not username:
        print("[ERROR] JIRA_USERNAME not found in config", file=sys.stderr)
        sys.exit(1)

    if args.last_week:
        target_date = datetime.now() - timedelta(weeks=1)
    elif args.weeks_ago > 0:
        target_date = datetime.now() - timedelta(weeks=args.weeks_ago)
    elif args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        target_date = datetime.now()

    start_dt, end_dt = get_week_range(target_date)
    date_from = start_dt.strftime("%Y-%m-%d")
    date_to = end_dt.strftime("%Y-%m-%d")

    user_key = resolve_user_key(client, username)

    # Check total logged hours for this week first
    logged_sec = 0
    try:
        w_res = client.session.get(
            f"{client.base_url}/rest/tempo-timesheets/3/worklogs?username={username}&dateFrom={date_from}&dateTo={date_to}"
        )
        if w_res.ok:
            for item in w_res.json():
                logged_sec += item.get("timeSpentSeconds", 0)
    except Exception:
        pass

    logged_hours = round(logged_sec / 3600, 1)

    print("=" * 75)
    print(f"      GỬI DUYỆT TIMESHEET TUẦN (TEMPO)")
    print("=" * 75)
    print(f" • Nhân sự gửi     : {username} ({user_key})")
    print(f" • Người duyệt     : {args.reviewer}")
    print(f" • Tuần áp dụng    : {date_from} ──▶ {date_to}")
    print(f" • Tổng giờ đã log : {logged_hours}h")
    print(f" • Lời nhắn        : {args.comment}")
    print("=" * 75)

    if args.dry_run:
        print("[DRY-RUN] Kiểm tra hoàn tất, kết thúc chạy thử.")
        return

    if not args.yes:
        val = input("\nBạn có chắc chắn muốn gửi duyệt timesheet tuần này không? (y/N): ").strip().lower()
        if val not in ("y", "yes"):
            print("Đã hủy.")
            return

    headers = {
        'Origin': client.base_url,
        'Referer': f"{client.base_url}/secure/Tempo.jspa",
        'X-Atlassian-Token': 'no-check',
        'X-Requested-With': 'XMLHttpRequest'
    }

    payload = {
        "user": {"key": user_key},
        "period": {
            "periodView": "WEEK",
            "dateFrom": date_from,
            "dateTo": date_to
        },
        "action": {
            "name": "submit",
            "reviewer": {"name": args.reviewer},
            "comment": args.comment
        }
    }

    try:
        res = client.session.post(
            f"{client.base_url}/rest/tempo-timesheets/4/timesheet-approval",
            json=payload,
            headers=headers
        )
        if res.status_code in (200, 201, 204):
            data = res.json() if res.text else {}
            status = data.get("status", "waiting_for_approval")
            submitted_h = data.get("submittedSeconds", 0) / 3600
            print(f"\n[SUCCESS] Gửi duyệt Timesheet thành công!")
            print(f" • Trạng thái mới : {status.upper()}")
            print(f" • Số giờ gửi     : {submitted_h}h")
            print(f" • Người duyệt    : {args.reviewer}")
        else:
            print(f"\n[ERROR] Gửi duyệt thất bại ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
