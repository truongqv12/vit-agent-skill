---
schemaVersion: "vit-plan/v1"
id: "phase-01"
title: "Schema and canonical templates"
status: completed
dependencies: []
---

# Phase 1: Schema and canonical templates

## Context

The source embeds drifting plan and phase examples. This phase gives each
artifact one canonical owner and defines the controlled v1 contract.

## Related Files

- Create: `skills/vit-plan/templates/plan.md`
- Create: `skills/vit-plan/templates/phase.md`
- Create: `skills/vit-plan/references/plan-organization.md`
- Create: `skills/vit-plan/references/output-standards.md`

## Implementation Steps

1. Define allowed plan/phase fields, statuses, stable quoted phase IDs,
   dependency semantics, optional fields, and unknown-field rejection.
2. Require outcome, constraints, non-goals, acceptance, phases, dependencies,
   risk, rollback, and unresolved-question sections at the correct level.
3. Use repo-relative stored links, UTF-8, deterministic slug/number rules, and
   collision-safe no-overwrite behavior.
4. Document a native render/lint checklist for runtimes without Python.

## Todo

- [x] Canonical plan template created.
- [x] Canonical phase template created.
- [x] Schema and fallback rules documented without duplication.

## Validation

- Templates contain `schemaVersion: "vit-plan/v1"` and no unresolved invalid
  placeholder fields.
- Every schema rule has one owning reference or template.

## Risks and Mitigations

Ambiguous YAML or dependency meaning could make helpers unsafe. Reject syntax
outside the controlled grammar.

## Rollback

Remove only the four new files owned by this phase.
