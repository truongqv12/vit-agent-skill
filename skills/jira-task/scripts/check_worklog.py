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

def main():
    parser = argparse.ArgumentParser(description="Check weekly worklogs and Tempo timesheet approval status")
    parser.add_argument("username", nargs="?", help="Jira username (default from .env)")
    parser.add_argument("--weeks-ago", "-w", type=int, default=0, help="Weeks ago (0=this week, 1=last week)")
    parser.add_argument("--date", "-d", help="Date in target week (YYYY-MM-DD)")
    args = parser.parse_args()

    client = JiraClient()
    username = args.username or client.username
    if not username:
        print("[ERROR] No username specified and none found in .env", file=sys.stderr)
        sys.exit(1)

    if args.date:
        base_date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        base_date = datetime.now() - timedelta(weeks=args.weeks_ago)

    start_dt, end_dt = get_week_range(base_date)
    start_str = start_dt.strftime("%Y-%m-%d")
    end_str = end_dt.strftime("%Y-%m-%d")

    print("=" * 80)
    print(f"      KIỂM TRA LOG WORK & PHÊ DUYỆT CHẤM CÔNG TUẦN")
    print("=" * 80)
    print(f" • Nhân sự     : {username}")
    print(f" • Tuần        : {start_str} ──▶ {end_str}")
    print("=" * 80)

    # 1. Check Tempo timesheet approval status
    print("\n[1] TRẠNG THÁI NỘP DUYỆT TIMESHEET (TEMPO):")
    try:
        u_res = client.get(f"/rest/api/2/user?username={username}")
        user_key = u_res.json().get("key", username) if u_res.ok else username
        t_res = client.get(f"/rest/tempo-timesheets/4/timesheet-approval/current?userKey={user_key}")
        if t_res.ok:
            t_data = t_res.json()
            status = t_data.get("status", {}).get("key", "OPEN")
            reviewer = t_data.get("reviewer", {}).get("displayName", "N/A")
            print(f" • Trạng thái : {status.upper()}")
            print(f" • Người duyệt: {reviewer}")
        else:
            print(" • Không lấy được thông tin Tempo (hoặc chưa cài Tempo Timesheet).")
    except Exception as e:
        print(f" • Lỗi kiểm tra Tempo: {e}")

    # 2. Check worklogs across the week
    print("\n[2] CHI TIẾT GIỜ ĐÃ LOG TRONG TUẦN:")
    jql = f'worklogAuthor = "{username}" AND worklogDate >= "{start_str}" AND worklogDate <= "{end_str}"'
    day_totals = {}
    day_details = {}
    total_week_seconds = 0

    try:
        data = client.search_issues(jql, fields="summary,worklog", max_results=100)
        issues = data.get("issues", [])
        for issue in issues:
            key = issue.get("key")
            summary = issue.get("fields", {}).get("summary", "")
            try:
                wls = client.get_worklogs(key)
            except Exception:
                wls = []
            for w in wls:
                if w.get("author", {}).get("name") == username:
                    d_str = w.get("started", "")[:10]
                    if start_str <= d_str <= end_str:
                        sec = w.get("timeSpentSeconds", 0)
                        comment = w.get("comment", "")
                        day_totals[d_str] = day_totals.get(d_str, 0) + sec
                        day_details.setdefault(d_str, []).append({
                            "key": key,
                            "summary": summary,
                            "hours": round(sec / 3600, 1),
                            "comment": comment
                        })
                        total_week_seconds += sec

        # Render Monday -> Friday
        day_names = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"]
        print(f"{'NGÀY':<12} | {'THỨ':<8} | {'TỔNG GIỜ':<10} | {'ĐÁNH GIÁ'}")
        print("-" * 65)
        for i in range(5):
            d = (start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
            d_name = day_names[i]
            sec = day_totals.get(d, 0)
            hrs = round(sec / 3600, 1)
            eval_str = "✅ Đạt chuẩn (8h)" if hrs >= 8.0 else f"⚠️ Thiếu {round(8.0 - hrs, 1)}h"
            print(f"{d:<12} | {d_name:<8} | {hrs:<10} | {eval_str}")

        print("-" * 65)
        total_h = round(total_week_seconds / 3600, 1)
        print(f"==> TỔNG CỘNG TUẦN: {total_h}h / 40.0h")
        if total_h >= 40.0:
            print("🎉 BẠN ĐÃ LOG ĐỦ GIỜ TUẦN NÀY!")
        else:
            print(f"⚠️ BẠN CÒN THIẾU: {round(40.0 - total_h, 1)}h.")

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
