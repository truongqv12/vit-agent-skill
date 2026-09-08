---
schemaVersion: "vit-plan/v1"
id: "phase-07"
title: "Port project-management"
status: completed
dependencies: ["phase-01"]
---

# Phase 7: Port project-management

## Context

`cook`'s Step 6 MUST activate project-management for full plan sync-back across
ALL `phase-XX-*.md` (not just the current phase), updating `plan.md`
status/progress. This is largely portable file logic and pairs naturally with
the existing `vit-plan` schema and its `plan-tool.py` helper.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-project-management` — 6 md, ~15.1 KB
- Create: `skills/project-management/**`, `plans/reports/research-<ts>-project-management-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan; separate durable plan-file logic from AgentKit
   store/dashboard/CLI status coupling.
2. Preserve invariants: whole-plan sync-back, backfill stale checkboxes across
   every phase, derive plan status from actual checkbox state, report unresolved
   task→phase mappings.
3. Reuse `vit-plan/v1` schema and `plan-tool.py status/lint`; native checkbox
   edit fallback.
4. Drop AgentKit SQLite store, `ak plan` status subcommands, and dashboard.
5. Register and regenerate index.

## Todo

- [x] Whole-plan (not current-phase-only) sync-back preserved.
- [x] Status derived from `vit-plan/v1` checkboxes; store dependency dropped.
- [x] Passes validator and no-AK scenario.

## Validation

- Sync-back on a multi-phase plan reconciles all phases and updates plan.md.
- No `/ak:*`, `ak <command>`, store, or dashboard references remain.

## Risks and Mitigations

Copying store semantics would reintroduce hidden state. Filesystem plan files
are the sole authority.

## Rollback

Remove `skills/project-management/**` and revert index/catalog hunks.
