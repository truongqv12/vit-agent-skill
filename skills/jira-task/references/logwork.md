# Log Work and Timesheet Management

Use `log_work.py`, `check_worklog.py`, and `submit_timesheet.py`.

## 1. Log Single Worklog (`log_work.py`)

```bash
# Log 8h for today:
python scripts/log_work.py CCDT-45 "8h" "Nội dung công việc"

# Log for a specific date and time:
python scripts/log_work.py CCDT-45 "4h" "Fix bug ký số" --date 2026-09-08 --time 08:30:00
```

## 2. Auto Full Week Logwork (`log_work.py --week`)

Automatically scans Monday to Friday of the target week, checks how many hours have already been logged on each day, and logs remaining hours up to 8h/day. Automatically skips weekends.

```bash
# Preview the weekly plan without writing (Dry run):
python scripts/log_work.py --week --key CCDT-45 --comment "Phát triển dự án công chứng số" --dry-run

# Execute full week auto-log:
python scripts/log_work.py --week --key CCDT-45 --comment "Phát triển dự án công chứng số" --yes

# Log for previous week:
python scripts/log_work.py --week --key CCDT-45 --weeks-ago 1 --yes

# Exclude specific holiday dates:
python scripts/log_work.py --week --key CCDT-45 --exclude 2026-09-02 --yes
```

## 3. Check Weekly Worklogs & Timesheet Status (`check_worklog.py`)

```bash
# Check current week:
python scripts/check_worklog.py

# Check previous week:
python scripts/check_worklog.py --weeks-ago 1
```

## 4. Submit Timesheet to Manager (`submit_timesheet.py`)

Submits Tempo timesheet to manager for approval (default reviewer: `nghialt.tgg`):

```bash
# Preview submission:
python scripts/submit_timesheet.py --dry-run

# Submit timesheet:
python scripts/submit_timesheet.py nghialt.tgg "Gửi anh duyệt chấm công tuần" --yes
```
