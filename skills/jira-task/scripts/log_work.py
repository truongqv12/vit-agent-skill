import sys
import argparse
from datetime import datetime, timedelta
from jira_api import JiraClient

def get_week_days(target_date=None):
    if target_date is None:
        target_date = datetime.now()
    start_of_week = target_date - timedelta(days=target_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    day_names = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"]
    work_days = []
    for i in range(5):
        d = start_of_week + timedelta(days=i)
        work_days.append({
            "date": d.strftime("%Y-%m-%d"),
            "day_name": day_names[i],
            "datetime": d
        })
    return work_days, start_of_week, start_of_week + timedelta(days=6)

def run_weekly_log(client, key, comment, hours_per_day, weeks_ago, target_date, exclude_dates, dry_run, confirm):
    if target_date:
        base_date = datetime.strptime(target_date, "%Y-%m-%d")
    else:
        base_date = datetime.now() - timedelta(weeks=weeks_ago)

    work_days, start_dt, end_dt = get_week_days(base_date)
    start_str = start_dt.strftime("%Y-%m-%d")
    end_str = end_dt.strftime("%Y-%m-%d")

    print("=" * 80)
    print(f"      TỰ ĐỘNG LOG WORK FULL TUẦN (THỨ 2 -> THỨ 6)")
    print("=" * 80)
    print(f" • Task mục tiêu : {key.upper()}")
    print(f" • Tuần áp dụng  : Từ {start_str} đến {end_str}")
    print(f" • Định mức ngày : {hours_per_day}h / ngày")
    print(f" • Nội dung      : {comment}")
    if exclude_dates:
        print(f" • Ngày loại trừ : {', '.join(exclude_dates)}")
    print("-" * 80)

    # Check existing worklogs
    username = client.username
    jql = f'worklogAuthor = "{username}" AND worklogDate >= "{start_str}" AND worklogDate <= "{end_str}"'
    logged_days = {}
    try:
        data = client.search_issues(jql, fields="worklog", max_results=100)
        for issue in data.get("issues", []):
            ikey = issue.get("key")
            try:
                wls = client.get_worklogs(ikey)
            except Exception:
                wls = []
            for w in wls:
                if w.get("author", {}).get("name") == username:
                    d_str = w.get("started", "")[:10]
                    sec = w.get("timeSpentSeconds", 0)
                    logged_days[d_str] = logged_days.get(d_str, 0) + sec
    except Exception as e:
        print(f"[!] Warning checking existing logs: {e}")

    # Build plan
    plan = []
    for day in work_days:
        d_str = day["date"]
        d_name = day["day_name"]
        if d_str in exclude_dates:
            status_text = "BỎ QUA (Nghỉ lễ/theo yêu cầu)"
            needed_h = 0
        else:
            already_sec = logged_days.get(d_str, 0)
            already_h = round(already_sec / 3600, 1)
            needed_h = max(0.0, float(hours_per_day) - already_h)
            if needed_h <= 0:
                status_text = f"ĐỦ RỒI (Đã log {already_h}h)"
            else:
                status_text = f"CẦN LOG: {needed_h}h (Đã có: {already_h}h)"

        plan.append({
            "date": d_str,
            "day_name": d_name,
            "needed_h": needed_h,
            "status": status_text
        })

    # Print plan table
    print(f"{'NGÀY':<12} | {'THỨ':<8} | {'TRẠNG THÁI HIỆN TẠI VÀ KẾ HOẠCH'}")
    print("-" * 80)
    for p in plan:
        print(f"{p['date']:<12} | {p['day_name']:<8} | {p['status']}")
    print("-" * 80)

    total_need = sum(p["needed_h"] for p in plan)
    if total_need <= 0:
        print("\n[OK] Toàn bộ các ngày trong tuần đều đã được log đủ giờ!")
        return

    print(f"\n=> TỔNG SỐ GIỜ CẦN LOG BÙ: {total_need}h")
    if dry_run:
        print("[DRY-RUN] Chế độ chạy thử, kết thúc không gửi request.")
        return

    if not confirm:
        val = input("\nBạn có chắc chắn muốn log các ngày trên không? (y/N): ").strip().lower()
        if val not in ("y", "yes"):
            print("Đã hủy.")
            return

    # Execute
    print("\n[+] Bắt đầu gửi logwork...")
    for p in plan:
        if p["needed_h"] > 0:
            h_str = f"{int(p['needed_h'])}h" if p["needed_h"].is_integer() else f"{p['needed_h']}h"
            started_iso = f"{p['date']}T08:30:00.000+0700"
            try:
                client.add_worklog(key.upper(), h_str, comment, started_iso)
                print(f" [+] {p['date']} ({p['day_name']}): Log {h_str} thành công!")
            except Exception as e:
                print(f" [ERROR] {p['date']}: {e}")

    print("\n[HOÀN TẤT] Log work tuần xong.")

def main():
    parser = argparse.ArgumentParser(description="Log work to Jira (single issue or full week)")
    parser.add_argument("key", nargs="?", default="CCDT-45", help="Issue key (e.g. CCDT-45)")
    parser.add_argument("time_spent", nargs="?", default="8h", help="Time spent (e.g. 8h, 4h, 1d) - for single mode")
    parser.add_argument("comment", nargs="?", default="Phát triển dự án", help="Worklog comment")
    parser.add_argument("--week", action="store_true", help="Run full week auto-log mode (Mon-Fri)")
    parser.add_argument("--date", "-d", help="Date string YYYY-MM-DD (default: today)")
    parser.add_argument("--time", "-t", default="08:30:00", help="Start time HH:MM:SS (default: 08:30:00)")
    parser.add_argument("--hours", "-H", type=int, default=8, help="Hours per day in week mode (default: 8)")
    parser.add_argument("--weeks-ago", "-w", type=int, default=0, help="Weeks ago (0=this week, 1=last week)")
    parser.add_argument("--exclude", "-e", nargs="*", default=[], help="Exclude dates (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()

    client = JiraClient()

    if args.week:
        run_weekly_log(
            client=client,
            key=args.key,
            comment=args.comment,
            hours_per_day=args.hours,
            weeks_ago=args.weeks_ago,
            target_date=args.date,
            exclude_dates=args.exclude,
            dry_run=args.dry_run,
            confirm=args.yes
        )
    else:
        # Single log mode
        target_date = args.date or datetime.now().strftime("%Y-%m-%d")
        started_iso = f"{target_date}T{args.time}.000+0700"
        print("=" * 70)
        print(f" LOG WORK: {args.key.upper()} | {args.time_spent} on {target_date}")
        print(f" Comment: {args.comment}")
        print("=" * 70)

        if not args.yes and not args.dry_run:
            pass  # proceed

        if args.dry_run:
            print("[DRY-RUN] Preview only.")
            return

        try:
            res = client.add_worklog(args.key.upper(), args.time_spent, args.comment, started_iso)
            print(f"\n[SUCCESS] Worklog ID: {res.get('id')}")
            print(f"Author: {res.get('author', {}).get('displayName', client.username)}")
        except Exception as e:
            print(f"[ERROR] Failed to log work: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
