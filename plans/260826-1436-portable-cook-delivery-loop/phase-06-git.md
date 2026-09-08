---
schemaVersion: "vit-plan/v1"
id: "phase-06"
title: "Port git"
status: completed
dependencies: ["phase-01"]
---

# Phase 6: Port git

## Context

`cook`'s Step 6 spawns `git-manager` to stage/commit after user approval. The
portable `git` skill does conventional commits, secret scanning, and commit
splitting. All mutation requires explicit user intent.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-git` — 10 md, ~21.8 KB
- Create: `skills/git/**`, `plans/reports/research-<ts>-git-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Inventory + coupling scan; classify PR/`gh` and commit-split logic.
2. Preserve invariants: conventional commits, auto-split by type/scope, secret
   scan before commit, no AI-reference footers per repo rules.
3. Normalize; commit/push/PR are explicit-intent, native `git`/`gh` fallback.
4. Enforce "confirm before committing" per repo development rules.
5. Register and regenerate index.

## Todo

- [x] Secret scan and conventional-commit invariants preserved.
- [x] All mutations gated on explicit intent.
- [x] Passes validator and no-AK scenario.

## Validation

- Produces a conventional commit on a sandbox change only after confirmation.
- No `/ak:*` or named-subagent references remain.

## Risks and Mitigations

Auto-commit could mutate without consent. Default to preview + confirm.

## Rollback

Remove `skills/git/**` and revert index/catalog hunks.
