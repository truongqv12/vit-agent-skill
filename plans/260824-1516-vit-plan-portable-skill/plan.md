---
schemaVersion: "vit-plan/v1"
title: "Portable vit-plan skill"
description: "Migrate the planning workflow into a filesystem-first portable skill without AgentKit runtime coupling."
status: completed
priority: P1
effort: "10h"
tags: [feature, skills, planning]
blockedBy: []
blocks: []
created: "2026-08-24"
---

# Portable vit-plan skill

## Overview

Create `vit-plan` as an evidence-backed, plan-only workflow. Markdown plan and
phase files are durable authority; optional runtime tracking is only a derived
view. A small Python standard-library helper may scaffold and lint artifacts,
while physical templates and a native file fallback keep the skill usable when
Python is unavailable.

## Delivery Contract

### Outcome

`vit-plan` is directly discoverable from this repo and creates, validates,
challenges, and red-teams implementation plans without requiring the source
CLI, its private store, dashboard, hooks, or companion skills.

### Constraints

- Preserve verified MIT/agentkit/source version provenance.
- Use `vit-plan/v1` and keep stored paths repo-relative.
- Never overwrite generated files on collision.
- Require explicit intent for external effects.
- Preserve existing uncommitted work in shared files.

### Non-goals

- Recreate the source CLI, private store, dashboard, or hooks.
- Implement archive, HTML, GitHub, Wiki, images, global plan scope, or unrelated
  legacy cleanup.

### Acceptance Criteria

- Package identity and routing pass.
- Core behavioral invariants map to instructions and verification evidence.
- Canonical templates produce valid plans.
- Helper `create`, `add-phase`, and `lint` handle safety and error cases.
- Recursive portability checks and direct discovery pass without the source
  runtime on `PATH`.

## Phases

| # | Phase | Status |
|---|---|---|
| 1 | [Schema and canonical templates](./phase-01-schema-and-templates.md) | Completed |
| 2 | [Filesystem helper and tests](./phase-02-filesystem-helper.md) | Completed |
| 3 | [Portable planning workflow](./phase-03-portable-workflow.md) | Completed |
| 4 | [Repository integration](./phase-04-repository-integration.md) | Completed |
| 5 | [End-to-end verification](./phase-05-end-to-end-verification.md) | Completed |

## Implementation Allowlist

- Create `skills/vit-plan/**`.
- Modify `README.md`, `skills.sh.json`, and `scripts/validate-skills.sh` with
  overlap-safe patches that retain the existing portable-registry edits.
- Update only this plan directory and its completion journal/report during
  finalization.
- Do not restore or edit the user-owned deletions `AGENTS.md` and `CHANGELOG.md`.

## Dependencies

- Design authority: `plans/reports/research-260824-1243-vit-plan-migration.md`.
- Repository authority: `docs/portable-skill-contract.md`.
- Phase 2 requires phase 1; phase 3 requires phase 1; phase 4 requires phases 2
  and 3; phase 5 requires every implementation phase.

## Risks and Mitigations

- **Risk:** helper semantics drift from the documented artifact contract.
  **Mitigation:** run generated artifacts and this implementation plan through
  the same linter, then require independent test and review evidence.
- **Risk:** overlap-safe root edits erase earlier uncommitted work.
  **Mitigation:** patch only the catalog, grouping, and validator hunks and
  inspect the final diff/status before handoff.

## Success Criteria

- [x] All phase tasks and validation commands pass.
- [x] Runtime instructions contain no source CLI, slash-command, private path,
      dashboard, or hidden-store dependency.
- [x] Python absence has a documented native template/file fallback.
- [x] Existing worktree changes outside the allowlist remain untouched.
- [x] No unresolved blocking question remains.

## Open Questions

- None.

<!-- slug: vit-plan-portable-skill -->
