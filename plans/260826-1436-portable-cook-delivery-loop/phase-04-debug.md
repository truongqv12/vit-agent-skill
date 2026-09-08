---
schemaVersion: "vit-plan/v1"
id: "phase-04"
title: "Port debug"
status: completed
dependencies: ["phase-01"]
---

# Phase 4: Port debug

## Context

`cook`'s Step 4 spawns `debugger` on test failure for root-cause analysis. `fix`
(Phase 10) also relies on it. Large source (~41 KB): budget a dedicated
sub-plan/research report if needed.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-debug` — 12 md, ~41.4 KB
- Create: `skills/debug/**`, `plans/reports/research-<ts>-debug-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan across 12 references; classify log/CI/DB probing
   handoffs.
2. Preserve invariants: prove root cause before fix, multi-layer validation,
   call-stack tracing, log/CI/DB diagnostics, structured diagnostic report.
3. Normalize handoffs (log access, CI, DB) to capability + native fallback; no
   AgentKit-specific tooling assumptions.
4. Keep `debug` read/diagnose-first; behavior changes belong to cook/fix.
5. Register and regenerate index.

## Todo

- [x] Root-cause-before-fix invariant preserved with evidence mapping.
- [x] Diagnostic report format is self-contained.
- [x] Passes validator and no-AK scenario.

## Validation

- Diagnoses a seeded failure offline and produces a root-cause report.
- No `/ak:*` or named-subagent references remain.

## Risks and Mitigations

Breadth may hide coupling. Use the recursive static scan and disposition every
one of the 12 source files explicitly.

## Rollback

Remove `skills/debug/**` and revert index/catalog hunks.
