# jira-task

Standalone Python toolkit for interacting directly with Jira Server / Data Center
(specifically tuned for Jira Server 8.22, e.g. VNPT Jira `cntt.vnpt.vn`).

[`SKILL.md`](./SKILL.md) is the authority for router behavior, safety rules, and
script workflows. This README carries provenance, configuration, and portability notes.

## Provenance & Portability

- **Standalone.** Driven entirely by standalone Python 3 scripts in `scripts/`.
- Eliminates heavy MCP round-trips, prevents server-side 401/OTP rate limits via
  throttling and backoff, and caches transition IDs to resolve/close issues in a
  single HTTP request.
- Resolves configuration portably from `.env` in the workspace or the skill directory.
- No dependency on external tool-orchestration runtimes or private services.

## Features

- **Query & View**: List tasks (`list_tasks.py`), view issue details and download
  attachments (`view_task.py`), and export styled Excel reports (`export_excel.py`).
- **Issue Lifecycle**: Fast transition / resolve / close with transition ID caching
  (`transition_task.py`), create issues (`create_task.py`), and update fields (`edit_task.py`).
- **Worklog & Timesheet**: Log single worklog or auto-fill weekly 40h worklogs
  (`log_work.py`), check weekly timesheets (`check_worklog.py`), and submit timesheets
  to reviewers (`submit_timesheet.py`).

## Configuration

Copy `.env.example` to `.env` in your workspace or skill folder:

```bash
# Recommended: Personal Access Token (PAT)
JIRA_BASE_URL=https://cntt.vnpt.vn
JIRA_PAT=your_pat_token_here

# Or Username / Password
JIRA_USERNAME=your_username
JIRA_PASSWORD=your_password

# Or Session Cookie
JIRA_COOKIE=your_session_cookie

IGNORE_SSL_WARNINGS=true
```

Project profiles and defaults are defined in `assets/project-profiles.json`.

## References

- [`references/query.md`](./references/query.md)
- [`references/create-edit.md`](./references/create-edit.md)
- [`references/transition-close.md`](./references/transition-close.md)
- [`references/logwork.md`](./references/logwork.md)
