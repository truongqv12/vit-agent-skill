---
name: jira-task
description: Work with Jira (VNPT Server 8.22, self-hosted) directly via high-performance standalone Python scripts. Query and list issues, view details with attachments, create and edit issues from project profiles, fast transition and close issues with transition ID caching, and log work across a week. Portable toolkit that works anywhere with a .env file.
user-invocable: true
when_to_use: "Invoke whenever the user asks to find, list, filter, read, create, edit, transition, close, export Excel, or log work on Jira issues, or wants an analysis/report of a Jira module."
category: productivity
keywords: [jira, script, python, worklog, logwork, transition, resolve, requirements, task, subtask, vnpt, ccdt]
metadata:
  author: opencode
  version: "3.0.0"
  portability: standalone
---

# Jira Task Toolkit (Standalone Python Suite)

Drive Jira **directly through the bundled Python scripts in `scripts/`** (or the project workspace).
This eliminates heavy MCP round-trips, saves LLM context/requests, and prevents server-side rate limits with built-in backoff.

- Target: **Jira Server / Data Center 8.22** (self-hosted, `cntt.vnpt.vn`).
- Scripts resolve configuration from `.env` in the workspace or skill directory.
- Supports **Personal Access Token (`JIRA_PAT`)**, **Session Cookie (`JIRA_COOKIE`)**, or **Basic Auth**.

## Global rules (always apply)

1. **Confirm before any WRITE.** Writes = `transition_task.py`, `create_task.py`, `edit_task.py`, `log_work.py`, `submit_timesheet.py`.
   Before writing: show exactly what will change (issue key, field, old→new / hours / target status), then ask for a yes. Read tools never need confirmation.
2. **Auto-verification after write.** Every write script automatically re-fetches the issue and verifies the state (e.g. status/resolution or worklog ID). Report the verified result to the user.
3. **Optimized Transitions & Caching:** `transition_task.py` caches transition IDs (e.g. Open -> Resolved = `131` with `resolution=Done`) in `transitions_cache.json`. Transitions execute in a single HTTP request without repeated discovery round-trips.
4. **Reliability & Rate-limit Handling:** Built into `jira_api.py`. Rapid requests to `cntt.vnpt.vn` return 401/OTP if called too fast; the client automatically backs off (15s) and retries.
5. **Prefer portable CLI execution:** Run scripts via terminal (`python scripts/<script>.py ...`). Do not invoke MCP tools.

## Workflow router & Script reference

| User intent | Script command | Reference doc |
|-------------|----------------|---------------|
| **List my open tasks** | `python scripts/list_tasks.py --mine` | `references/query.md` |
| **Filter tasks by project / JQL** | `python scripts/list_tasks.py -p CCDT --due 3d` | `references/query.md` |
| **View details, comments, download attachments** | `python scripts/view_task.py CCDT-99 -d` | `references/query.md` |
| **Fast Transition / Resolve / Close** | `python scripts/transition_task.py CCDT-99 --to resolve` | `references/transition-close.md` |
| **Create new issue / Sub-task** | `python scripts/create_task.py "Tiêu đề" -p CCDT -t Bug` | `references/create-edit.md` |
| **Edit fields (Assignee, Due, Priority...)** | `python scripts/edit_task.py CCDT-99 -a tttruong --due 2026-09-30` | `references/create-edit.md` |
| **Log work (Single / Full week 40h)** | `python scripts/log_work.py --week --key CCDT-45` | `references/logwork.md` |
| **Check timesheet & week logwork** | `python scripts/check_worklog.py` | `references/logwork.md` |
| **Export project to styled Excel** | `python scripts/export_excel.py CCDT` | `references/query.md` |

## Configuration & Portability

- `.env.example` — Copy to `.env` in any folder to carry this tool suite anywhere.
- `assets/project-profiles.json` — Per-project defaults for issue creation.
