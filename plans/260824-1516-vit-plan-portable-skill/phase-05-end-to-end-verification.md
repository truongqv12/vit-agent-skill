---
schemaVersion: "vit-plan/v1"
id: "phase-05"
title: "End-to-end verification"
status: completed
dependencies: ["phase-01", "phase-02", "phase-03", "phase-04"]
---

# Phase 5: End-to-end verification

## Context

Prove the package is portable, discoverable, safe, and regression-free before
syncing the durable plan state.

## Related Files

- Verify: `skills/vit-plan/**`
- Verify: `README.md`
- Verify: `skills.sh.json`
- Verify: `scripts/validate-skills.sh`
- Update after evidence: this plan directory

## Implementation Steps

1. Run helper unit/negative tests and generic repository validation.
2. Run recursive forbidden-coupling and relative-link checks.
3. Exercise create/add-phase/lint in an isolated temporary project with source
   CLI absent from `PATH`; verify native fallback instructions independently.
4. Run Skills CLI list/direct pickup compatibility checks when available.
5. Delegate testing and code review; fix critical failures, then sync every
   phase checkbox and plan status from evidence.

## Todo

- [x] All automated and scenario checks pass.
- [x] Reviewer confirms acceptance, blast radius, contracts, patterns, and
      lint/build cleanliness.
- [x] Full-plan sync and journal completed.

## Validation

- `git diff --check`
- `git status --short` confirms unrelated deletions remain untouched.
- No new environment variable, credential, network, or external-service setup
  is required.

## Risks and Mitigations

Optional discovery may fail from network/tool availability; report it
separately from core correctness.

## Rollback

If core validation fails, remove the new package and revert only the three
integration hunks.
