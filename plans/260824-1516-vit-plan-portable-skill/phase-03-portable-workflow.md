---
schemaVersion: "vit-plan/v1"
id: "phase-03"
title: "Portable planning workflow"
status: completed
dependencies: ["phase-01"]
---

# Phase 3: Portable planning workflow

## Context

Port the planning behavior, not the source runtime. References must remain
capability-based and work sequentially when optional tools are absent.

## Related Files

- Create: `skills/vit-plan/SKILL.md`
- Create: `skills/vit-plan/README.md`
- Create: `skills/vit-plan/references/workflow-modes.md`
- Create: `skills/vit-plan/references/scope-challenge.md`
- Create: `skills/vit-plan/references/research-and-codebase.md`
- Create: `skills/vit-plan/references/solution-design.md`
- Create: `skills/vit-plan/references/task-management.md`
- Create: `skills/vit-plan/references/validation-workflow.md`
- Create: `skills/vit-plan/references/validation-question-framework.md`
- Create: `skills/vit-plan/references/red-team-workflow.md`
- Create: `skills/vit-plan/references/red-team-personas.md`
- Create: `skills/vit-plan/references/verification-roles.md`

## Implementation Steps

1. Write a router-like `SKILL.md` that preserves the plan-only boundary,
   accepted intent, unfinished-plan scan, scope challenge, evidence-first flow,
   durable file authority, verification, validation, and red-team gates.
2. Define canonical fast/hard/deep/parallel/two/TDD/no-tasks semantics; omit
   source `--auto` and archive behavior explicitly.
3. Require user adjudication before verification or red-team corrections and a
   whole-plan consistency reread before handoff.
4. Use capability discovery with plain conversation/sequential/native
   fallbacks; document Python as optional.
5. Record provenance and deliberate adaptations without inventing source URL or
   commit.

## Todo

- [x] Router and package README created.
- [x] Core workflow references created and linked.
- [x] Thirteen source behavior invariants remain observable.

## Validation

- Every routed relative path exists.
- Current-code claims use file/line evidence; greenfield and plan findings use
  precise plan-section evidence.
- No runtime source command, path, hook, store, or dashboard reference remains.

## Risks and Mitigations

Text replacement could preserve hidden coupling or lose decision gates. Use an
invariant checklist and recursive scan.

## Rollback

Remove only the `skills/vit-plan/` documentation and template files owned by
this phase.
