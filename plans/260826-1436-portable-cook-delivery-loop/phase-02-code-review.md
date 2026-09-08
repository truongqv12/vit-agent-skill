---
schemaVersion: "vit-plan/v1"
id: "phase-02"
title: "Port code-review"
status: completed
dependencies: ["phase-01"]
---

# Phase 2: Port code-review

## Context

`cook`'s Step 5 spawns `code-reviewer` as a MANDATORY gate with explicit (a-e)
checks and drives HARD-GATE-NO-SIDE-EFFECTS. This is the highest-value
delegation to port. The portable skill must run as a capability, and `cook`
must degrade to a native inline review when it is absent.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-code-review` — 14 md, ~36.6 KB
- Create: `skills/code-review/**`, `plans/reports/research-<ts>-code-review-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan; identify input modes (pending diff, PR#, commit,
   codebase scan) and any `gh` CLI coupling.
2. Preserve invariants: evidence-based findings, severity tiers, the (a-e)
   check contract cook depends on, no-false-positive discipline.
3. Normalize handoffs using Phase 1 phrasing; make `gh`/PR modes explicit-intent
   and optional.
4. Ensure the (a-e) acceptance/contract checks are expressible without cook so
   the skill stands alone.
5. Register and regenerate index.

## Todo

- [x] (a-e) mandatory-check contract preserved and self-contained.
- [x] PR/`gh` modes gated on explicit intent + availability.
- [x] Passes validator and no-AK scenario.

## Validation

- A diff review runs offline with only native tools and returns scored findings.
- No `/ak:*` or named-subagent references remain.

## Risks and Mitigations

Losing the (a-e) contract would break cook's side-effect gate. Map each check to
a target section with a scenario.

## Rollback

Remove `skills/code-review/**` and revert index/catalog hunks.
