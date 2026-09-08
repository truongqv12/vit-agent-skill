---
schemaVersion: "vit-plan/v1"
id: "phase-02"
title: "Filesystem helper and tests"
status: completed
dependencies: ["phase-01"]
---

# Phase 2: Filesystem helper and tests

## Context

The optional helper makes common filesystem operations deterministic without
becoming a replacement CLI or durable state owner.

## Related Files

- Create: `skills/vit-plan/scripts/plan-tool.py`
- Create: `skills/vit-plan/scripts/test-plan-tool.py`

## Implementation Steps

1. Implement standard-library commands `create`, `add-phase`, and `lint`.
2. Resolve package templates relative to the script and restrict all writes to
   the explicit target plan directory.
3. Make multi-file creation transactional, refuse collisions/path traversal,
   and never overwrite an existing plan or phase.
4. Lint frontmatter, statuses, plan links, phase IDs, dependencies, cycles, and
   required sections with stable exit codes and actionable errors.
5. Test happy paths, UTF-8, BOM/newlines, malformed frontmatter, collisions,
   reserved/path escape targets, broken/gapped/duplicate phases, and cycles.

## Todo

- [x] Minimal helper implemented.
- [x] Standard-library test suite implemented.
- [x] Generated artifacts round-trip through lint.

## Validation

- `python -X utf8 skills/vit-plan/scripts/test-plan-tool.py`
- `python -X utf8 skills/vit-plan/scripts/plan-tool.py --help`

## Risks and Mitigations

A permissive parser may corrupt files or scope-creep into a CLI clone. Keep the
grammar controlled and commands limited to three.

## Rollback

Remove both script files owned by this phase.
