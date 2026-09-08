---
schemaVersion: "vit-plan/v1"
id: "phase-08"
title: "Port journal"
status: completed
dependencies: ["phase-01"]
---

# Phase 8: Port journal

## Context

`cook`'s Step 6 runs `/ak:journal` to write a concise technical journal entry on
completion. Tiny source (~1.4 KB); mostly a writing contract and a path
convention (`plans/journals/`).

## Related Files

- Source skill (installed, read-only, not in repo): `ak-journal` — 1 md, ~1.4 KB
- Create: `skills/journal/**`, `plans/reports/research-<ts>-journal-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan (expected minimal).
2. Preserve invariants: chronological technical reflection, decisions/lessons,
   convert relative dates to absolute; journals do not replace docs/ADRs.
3. Normalize output path to this repo's `plans/journals/` convention.
4. Make invocation explicit-intent (writes a file).
5. Register and regenerate index.

## Todo

- [x] Journal writing contract preserved.
- [x] Output path uses repo convention.
- [x] Passes validator and no-AK scenario.

## Validation

- Writes a well-formed journal entry to `plans/journals/` offline.
- No `/ak:*` references remain.

## Risks and Mitigations

Low risk. Ensure it does not auto-fire without cook/user intent.

## Rollback

Remove `skills/journal/**` and revert index/catalog hunks.
