---
name: jira-task
description: Work with Jira (VNPT Server 8.22, self-hosted) directly via high-performance standalone Python scripts. Query and list issues, view details with attachments, create and edit issues from project profiles, fast transition and close issues with transition ID caching, and log work across a week. Portable toolkit that works anywhere with a .env file.
user-invocable: true
when_to_use: "Invoke whenever the user asks to find, list, filter, read, create, edit, transition, close, export Excel, or log work on Jira issues, or wants an analysis/report of a Jira module."
category: productivity
keywords: [jira, script, python, worklog, logwork, transition, resolve, requirements, task, subtask, vnpt, ccdt]
metadata:
  author: opencode
  version: "3.1.0"
  portability: standalone
---

# Jira Task Toolkit (Standalone Python Suite)

> [!CRITICAL]
> ### STRICT BAN ON MCP TOOLS (`mcp-atlassian`)
> **NEVER CALL ANY TOOL FROM THE `mcp-atlassian` MCP SERVER** (`jira_get_issue`, `jira_search`, `jira_transition_issue`, `jira_add_worklog`, etc.).
> Calling Jira VNPT through MCP triggers server-side rate limits (`HTTP 401: OTP_REQUIRED`), wastes LLM context, and fails.
> **All Jira actions MUST be executed by running the Python scripts below via terminal.**

---

## Script Paths & Universal Execution

The scripts are installed in the skill's `scripts/` folder.
Whenever you are working in **any workspace**, run the scripts via terminal using their path:

```bash
# Run using the skill's script path or relative path:
python scripts/<script_name>.py [args...]

# Or when working outside the skill folder, execute using the installed skill path:
python "<skill_dir>/scripts/<script_name>.py" [args...]
```

Credentials are automatically loaded from:
1. Workspace `.env` (if present)
2. Skill folder `.env`
3. Global environment variables (`JIRA_BASE_URL`, `JIRA_PAT`, `JIRA_COOKIE`, etc.)

---

## Global Rules

1. **Confirm before any WRITE.** Writes = `transition_task.py`, `create_task.py`, `edit_task.py`, `log_work.py`, `submit_timesheet.py`.
   Before writing: show exactly what will change (issue keys, old→new status/resolution/fields), then ask for user confirmation. Read scripts never need confirmation.
2. **Auto-verification after write.** Every write script automatically re-fetches the issue from Jira and verifies the result.
3. **Multi-key batch operations:** Both `view_task.py` and `transition_task.py` accept **multiple keys at once** (e.g. `CCDT-33 CCDT-43 CCDT-103`).
   - `view_task.py` automatically aggregates all keys into a single JQL query (`key in (...)`), turning N requests into **1 single HTTP request** to prevent triggering WAF burst limits.
   - `transition_task.py` prefetches statuses in 1 call to instantly skip already resolved tasks, and uses a default `--delay 6.0s` between task transitions.
4. **Transition Caching:** `transition_task.py` uses `transitions_cache.json` (e.g. `Open -> Resolved` = ID `131` with `resolution=Done`). Transitions execute in 1 single HTTP request.
5. **Rate-limit Protection:** Handled transparently by `jira_api.py` with baseline throttle, browser User-Agent, and automatic 20s exponential backoff retry on 401/429.
6. **Authentication for VNPT Jira (MFA):** Do not rely on PAT if blocked by MFA gateway. Use `JIRA_COOKIE` (`JSESSIONID`) from active browser session. `jira_api.py` automatically binds the cookie to the exact host domain.

---

## Workflow Router & CLI Commands

### 1. Check / View Tasks (Single or Batch)
```bash
# Check status, description, and comments of one or more tasks:
python scripts/view_task.py CCDT-33 CCDT-43 CCDT-103

# View and download attachments locally:
python scripts/view_task.py CCDT-99 -d
```

### 2. Transition / Resolve / Close Tasks (Single or Batch)
```bash
# Fast Resolve batch tasks (sets Status = Resolved, Resolution = Done):
python scripts/transition_task.py CCDT-33 CCDT-43 CCDT-103 --to resolve

# Fast Close batch tasks:
python scripts/transition_task.py CCDT-33 CCDT-43 CCDT-103 --to close

# Inspect available transitions from an issue's current status:
python scripts/transition_task.py CCDT-33 --list
```

### 3. List & Filter Tasks
```bash
# My open/unresolved tasks:
python scripts/list_tasks.py --mine

# Unresolved tasks in project CCDT:
python scripts/list_tasks.py -p CCDT --due 3d

# Custom JQL query:
python scripts/list_tasks.py --jql "key in (CCDT-33, CCDT-43) ORDER BY updated DESC"
```

### 4. Create & Edit Issues
```bash
# Create issue from profile:
python scripts/create_task.py "Tiêu đề" -p CCDT -t Bug -a tttruong

# Edit fields:
python scripts/edit_task.py CCDT-99 -a tttruong --due 2026-09-30
```

### 5. Log Work & Timesheets
```bash
# Auto full week 40h logwork:
python scripts/log_work.py --week --key CCDT-45 --yes

# Check weekly logged hours & Tempo approval (current week or last week):
python scripts/check_worklog.py
python scripts/check_worklog.py -w 1

# Submit timesheet to manager (default: nghialt.tgg):
python scripts/submit_timesheet.py nghialt.tgg "Gửi anh duyệt chấm công" --last-week --yes
```

### 6. Export Project to Styled Excel
```bash
python scripts/export_excel.py CCDT
```

