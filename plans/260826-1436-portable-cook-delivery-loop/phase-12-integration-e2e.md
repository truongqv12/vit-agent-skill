---
schemaVersion: "vit-plan/v1"
id: "phase-12"
title: "Program integration and end-to-end verification"
status: completed
dependencies: ["phase-11"]
---

# Phase 12: Program integration and E2E

## Context

Final wave: verify the ported delivery loop works as a system and the catalog,
grouping, and generated index are current across all new skills.

## Related Files

- Modify: `README.md`, `skills.sh.json`, `docs/skills/README.md`,
  `scripts/validate-skills.sh`, `scripts/generate-skill-index.py` (overlap-safe)
- Create: this plan's completion journal and report at finalize.

## Implementation Steps

1. Confirm cross-skill routing: cook → scout/research/vit-plan/code-review/test/
   debug/git/project-management/docs/journal, and cook ↔ fix boundary.
2. Ensure shared handoff phrasing (Phase 1) is consistent across all skills.
3. Run the generic validator repo-wide and regenerate the skill index.
4. Run two end-to-end scenarios: (a) full loop with all companions present;
   (b) companions absent → native fallback still completes.
5. Recursive static scan for residual coupling across every new skill.

## Todo

- [x] Full-loop E2E passes with companions present.
- [x] Fallback E2E passes with companions absent.
- [x] Repo-wide validator and index regeneration pass.
- [x] Zero AgentKit coupling in any runtime instruction.

## Validation

- Both E2E scenarios complete; validator green; index current.
- No `/ak:*`, named-subagent, hidden-state, or absolute-source-path references
  anywhere under `skills/`.

## Risks and Mitigations

Inconsistent handoff vocabulary across skills breaks routing. Reconcile against
the Phase 1 shared phrasing before closing.

## Rollback

Revert only the overlap-safe root/catalog/index hunks from this phase; skill
directories are owned by their own phases.
