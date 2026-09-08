---
schemaVersion: "vit-plan/v1"
id: "phase-10"
title: "Port fix"
status: completed
dependencies: ["phase-04"]
---

# Phase 10: Port fix

## Context

`cook` explicitly routes concrete bugs to `/ak:fix` ("it frames intent first,
then proves the root cause before selecting a solution"). Largest source
(~55 KB): budget a dedicated sub-plan/research report. Reuses ported `debug`
and `test`.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-fix` — 14 md, ~55.4 KB
- Create: `skills/fix/**`, `plans/reports/research-<ts>-fix-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan across 14 references; map intelligent routing
   (type/lint/log/UI/CI) and any `/ak:*` sibling handoffs.
2. Preserve invariants: frame expected repaired behavior + safety boundary,
   prove root cause before fixing, cause-aligned solution, verify no regression.
3. Normalize; reuse ported `debug` (root cause) and `test` (verification) as
   optional-with-fallback capabilities.
4. Keep `fix` distinct from `cook`: bugs vs known-scope feature work.
5. Register and regenerate index.

## Todo

- [x] Prove-cause-before-fix invariant preserved with evidence mapping.
- [x] Routing works with native fallback when a sub-capability is absent.
- [x] Passes validator and no-AK scenario.

## Validation

- Fixes a seeded bug offline: frames intent, proves cause, verifies no regression.
- No `/ak:*` or named-subagent references remain.

## Risks and Mitigations

Breadth and routing complexity hide coupling. Disposition all 14 files; consider
a separate detailed plan for this phase.

## Rollback

Remove `skills/fix/**` and revert index/catalog hunks.
