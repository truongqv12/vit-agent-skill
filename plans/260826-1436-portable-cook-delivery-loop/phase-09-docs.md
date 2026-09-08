---
schemaVersion: "vit-plan/v1"
id: "phase-09"
title: "Port docs"
status: completed
dependencies: ["phase-01"]
---

# Phase 9: Port docs

## Context

`cook`'s Step 6 conditionally spawns `docs-manager` only when an authority
surface changed — never a whole-corpus refresh. The portable `docs` skill
creates/refreshes/audits docs without imposing a fixed layout, matching this
repo's documentation-management rule.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-docs` — 7 md, ~15.5 KB
- Create: `skills/docs/**`, `plans/reports/research-<ts>-docs-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan; identify docs-navigation discovery vs fixed
   filename assumptions.
2. Preserve invariants: no fixed docs tree, update smallest owning surface, link
   to machine-owned sources instead of copying, evidence-backed edits.
3. Normalize; docs mutation is explicit-intent and scoped to changed authority
   surfaces.
4. Align with `docs/portable-skill-contract.md` and the repo docs-impact rule.
5. Register and regenerate index.

## Todo

- [x] Scoped, docs-impact-gated behavior preserved (no blanket refresh).
- [x] Layout-agnostic discovery preserved.
- [x] Passes validator and no-AK scenario.

## Validation

- Updates only the changed authority surface on a scoped change, offline.
- No `/ak:*` or named-subagent references remain.

## Risks and Mitigations

A generic refresh could churn unrelated docs. Enforce scoped, evidence-based edits.

## Rollback

Remove `skills/docs/**` and revert index/catalog hunks.
