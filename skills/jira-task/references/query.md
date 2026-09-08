# Query, List, and View Issues

Use `list_tasks.py` and `view_task.py` directly. No MCP needed.

## 1. List and Filter Tasks (`list_tasks.py`)

Run `python scripts/list_tasks.py` with flexible flags:

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

```bash
# View 1 issue with description and all comments
python scripts/view_task.py CCDT-99

# View multiple issues and automatically download all image/file attachments:
python scripts/view_task.py CCDT-99 CCDT-97 CCDT-96 -d

# Output raw JSON
python scripts/view_task.py CCDT-99 --json
```

- When `-d` is passed, files are saved locally to `attachments/<KEY>/<id>_<filename>`.
- Use vision analysis on downloaded images to inspect UI/UX requirements.

## 3. Export Project to Styled Excel (`export_excel.py`)

```bash
# Export all tasks of CCDT with status colors, hyperlinks, and auto-width:
python scripts/export_excel.py CCDT

# Only unresolved tasks:
python scripts/export_excel.py CCDT --unresolved
```
