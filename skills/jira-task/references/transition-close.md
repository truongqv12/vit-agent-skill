# Fast Transition and Close Issues

> **CRITICAL: NEVER USE MCP (`mcp-atlassian`).** Always execute `transition_task.py` directly via terminal.

## Script Location
`scripts/transition_task.py`

## The CCDT workflow: Two states in the Done category

Verified on Jira VNPT (`cntt.vnpt.vn`, project CCDT):
```
Open ──(131 "Resolved", resolution REQUIRED)──▶ Resolved ──("Closed")──▶ Closed
```

- **Resolution is set at the "Resolved" step** (`{"resolution": {"name": "Done"}}`).
- **"Closed" is a separate, subsequent status.**

## Commands (Supports Single or Batch Keys)

```bash
# 1. Inspect available transitions from an issue's current status:
python scripts/transition_task.py CCDT-99 --list

# 2. Fast resolve batch tasks (uses cached ID 131, automatically sets Resolution = Done):
python scripts/transition_task.py CCDT-33 CCDT-43 CCDT-103 --to resolve

# 3. Fast close batch tasks:
python scripts/transition_task.py CCDT-33 CCDT-43 CCDT-103 --to close

# 4. Start progress:
python scripts/transition_task.py CCDT-99 --to start

# 5. Reopen:
python scripts/transition_task.py CCDT-99 --to reopen

# 6. Custom target status with optional resolution and comment:
python scripts/transition_task.py CCDT-99 --to "Resolved" -r "Done" -c "Đã hoàn thành kiểm thử"
```

## Transition Caching (`transitions_cache.json`)

- `transition_task.py` maintains `transitions_cache.json`.
- When an ID is cached, transitioning takes **1 single HTTP POST request** (no extra discovery queries).
- If a cached ID fails or is not yet seen, it automatically fetches transitions from Jira, executes the right one, and saves the ID to the cache for all future calls.
- After every transition, the script re-fetches the issue and verifies both `status` and `resolution`.
