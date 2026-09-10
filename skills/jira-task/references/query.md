# Query, List, and View Issues

> **CRITICAL: NEVER USE MCP (`mcp-atlassian`).** Always execute scripts directly via terminal.

## Script Location
- List/Filter: `scripts/list_tasks.py`
- View/Attachments: `scripts/view_task.py`
- Export Excel: `scripts/export_excel.py`

## 1. List and Filter Tasks (`list_tasks.py`)

```bash
# My open/unresolved tasks (default)
python scripts/list_tasks.py --mine

# Unresolved tasks in project CCDT
python scripts/list_tasks.py -p CCDT

# Tasks due within 3 days
python scripts/list_tasks.py -p CCDT --due 3d

# Filter by assignee
python scripts/list_tasks.py -p CCDT -a tttruong

# Direct custom JQL
python scripts/list_tasks.py --jql "project = CCDT AND status = 'Đang xử lý' ORDER BY duedate ASC"

# Output raw JSON (for piping or LLM structured consumption)
python scripts/list_tasks.py --mine --json
```

## 2. View Full Detail & Download Attachments (`view_task.py`)

Supports checking one or multiple tasks at once:

```bash
# Check status, description, and comments of batch tasks:
python scripts/view_task.py CCDT-33 CCDT-43 CCDT-103

# View and download attachments locally:
python scripts/view_task.py CCDT-99 -d

# Output raw JSON
python scripts/view_task.py CCDT-99 --json
```

- When `-d` is passed, files are saved locally to `attachments/<KEY>/<id>_<filename>`.
