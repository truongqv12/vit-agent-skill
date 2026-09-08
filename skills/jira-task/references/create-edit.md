# Create and Edit Issues

Use `create_task.py` and `edit_task.py`.

## 1. Create an Issue (`create_task.py`)

Reads defaults from `assets/project-profiles.json` (default profile: `CCDT`).

```bash
# Create a standard task / bug:
python scripts/create_task.py "Tiêu đề công việc" -p CCDT -t Bug -d "Mô tả chi tiết" -a tttruong --priority High --due 2026-09-30

# Create a Sub-task under a parent issue:
python scripts/create_task.py "Làm giao diện chức năng ký số" --parent CCDT-45 -a tttruong

# Specify components and labels:
python scripts/create_task.py "Sửa lỗi font chữ" -p CCDT -c Frontend -l web bug
```

The script prints the newly created key and browse URL.

## 2. Edit an Existing Issue (`edit_task.py`)

```bash
# Change assignee:
python scripts/edit_task.py CCDT-99 -a tttruong

# Update due date and priority:
python scripts/edit_task.py CCDT-99 --due 2026-09-30 -p High

# Update summary or description:
python scripts/edit_task.py CCDT-99 -s "Tiêu đề mới" -d "Mô tả mới"

# Update labels:
python scripts/edit_task.py CCDT-99 -l web hotfix
```

After updating, `edit_task.py` automatically re-fetches the issue from Jira and verifies the changes.
