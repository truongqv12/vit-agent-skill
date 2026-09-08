---
schemaVersion: "vit-plan/v1"
id: "phase-04"
title: "Repository integration"
status: completed
dependencies: ["phase-02", "phase-03"]
---

# Phase 4: Repository integration

## Context

Expose `vit-plan` through the existing catalog and make the generic validator
enforce portable runtime documentation recursively.

## Related Files

- Modify: `README.md`
- Modify: `skills.sh.json`
- Modify: `scripts/validate-skills.sh`

## Implementation Steps

1. Add `vit-plan` to the Vietnamese catalog and install examples.
2. Add it to the existing Agent Workflows grouping without replacing
   `brainstorm` or other user changes.
3. Extend the validator to scan runtime Markdown under each skill while
   allowing provenance only in appropriate metadata/README contexts.
4. Add targeted `vit-plan` package checks for required templates, helper, and
   references while keeping legacy skills honestly classified.

## Todo

- [x] Catalog and grouping expose `vit-plan`.
- [x] Recursive portability validation covers runtime instructions.
- [x] Existing portable-registry changes remain intact.

## Validation

- `bash -n scripts/validate-skills.sh`
- `bash scripts/validate-skills.sh .`
- `Get-Content -Raw skills.sh.json | ConvertFrom-Json | Out-Null`

## Risks and Mitigations

Broad scanning could fail known legacy packages. Scope new recursive enforcement
to normalized packages through explicit portability metadata.

## Rollback

Revert only the three overlap-safe integration hunks.
