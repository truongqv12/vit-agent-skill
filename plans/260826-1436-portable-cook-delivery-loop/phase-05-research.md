---
schemaVersion: "vit-plan/v1"
id: "phase-05"
title: "Port research"
status: completed
dependencies: ["phase-01"]
---

# Phase 5: Port research

## Context

`cook`'s Step 1 spawns parallel `researcher` agents (skipped in fast/code mode).
Small source (~7 KB). Web/docs search is optional; local-evidence core first.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-research` — 1 md, ~7.0 KB
- Create: `skills/research/**`, `plans/reports/research-<ts>-research-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan; identify web/docs source handoffs.
2. Preserve invariants: multi-source synthesis, ≤150-line cited reports,
   evidence-first, mark gaps when a source is unavailable.
3. Normalize; make WebSearch/WebFetch optional with a local-evidence fallback.
4. Report format must be consumable by the plan step and gate 1.
5. Register and regenerate index.

## Todo

- [x] ≤150-line cited report contract preserved.
- [x] Web capability optional with documented fallback.
- [x] Passes validator and no-AK scenario.

## Validation

- Produces a cited report from local evidence with no network.
- No `/ak:*` or named-subagent references remain.

## Risks and Mitigations

Network dependence could block offline runs. Keep local-evidence path primary.

## Rollback

Remove `skills/research/**` and revert index/catalog hunks.
