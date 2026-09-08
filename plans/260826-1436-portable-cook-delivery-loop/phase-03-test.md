---
schemaVersion: "vit-plan/v1"
id: "phase-03"
title: "Port test"
status: completed
dependencies: ["phase-01"]
---

# Phase 3: Port test

## Context

`cook`'s Step 4 MUST spawn `tester` and enforces 100% pass (unless `--no-test`).
The portable `test` skill runs suites, reports coverage, and returns a pass/fail
contract cook can gate on; native fallback runs the project's test command via
shell.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-test` — 4 md, ~12.5 KB
- Create: `skills/test/**`, `plans/reports/research-<ts>-test-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan; identify test-runner detection and coverage prose.
2. Preserve invariants: unit/integration/e2e execution, coverage report, build
   verification, forbid fake mocks / commented tests / weakened assertions.
3. Normalize handoffs; test-runner discovery must be project-driven, not
   AgentKit-driven.
4. Define a machine-readable pass/fail summary cook can consume.
5. Register and regenerate index.

## Todo

- [x] Pass/fail contract defined for cook's Step 4 gate.
- [x] Anti-cheat rules (no fake mocks/skips) preserved.
- [x] Passes validator and no-AK scenario.

## Validation

- Runs a real project test command and reports results offline.
- No `/ak:*` or named-subagent references remain.

## Risks and Mitigations

Runner auto-detection could hard-code a stack. Detect from project config with a
clear "unknown runner" failure message.

## Rollback

Remove `skills/test/**` and revert index/catalog hunks.
