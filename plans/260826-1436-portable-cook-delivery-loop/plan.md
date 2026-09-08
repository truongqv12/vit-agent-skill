---
schemaVersion: "vit-plan/v1"
title: "Portable cook delivery-loop program"
description: "Port cook and every delivery-loop skill it orchestrates into portable, AgentKit-free skills, with cook as the capstone."
status: completed
priority: P1
effort: "60-80h"
tags: [program, skills, portability, cook, orchestration]
blockedBy: []
blocks: []
created: "2026-08-26"
---

# Portable cook delivery-loop program

## Overview

`cook` is the implementation workflow owner: it orchestrates the whole delivery
loop (scout → research → plan → implement → simplify → test → review →
finalize) by delegating to ~11 named subagents/skills and a live
task-management surface. Porting `cook` alone leaves it referencing skills that
do not exist in this kit. This program ports every delivery-loop skill `cook`
depends on, then ports `cook` last so its handoffs resolve to real portable
skills while retaining native fallbacks.

Each phase delivers **one portable skill** end-to-end per
`docs/portable-skill-contract.md` (collect → research → normalize → index →
verify). Heavier skills (`debug`, `fix`, `cook`) may spawn their own detailed
sub-plan and research report at execution time; this program owns ordering,
dependencies, and program-level acceptance.

Already ported (Wave 0, out of scope here): `brainstorm`, `vit-plan`.

## Delivery Contract

### Outcome

`cook` and the delivery-loop skills it orchestrates are directly discoverable
and runnable from this repo without AgentKit CLI, its private subagents, hidden
state (`.ck.json`, `CK_*`), store, or dashboard. `cook` degrades to native
tools when an optional companion skill is absent, and improves automatically as
companions are ported.

### Constraints

- Follow `docs/portable-skill-contract.md` for every skill.
- Preserve verified provenance (source-skill, source-version, MIT/agentkit).
- Handoffs are capability-neutral with a documented native fallback and honest
  missing-dependency behavior — never a hard `/ak:*` or named-subagent call.
- External effects (git commit/push, docs mutation, journal, GitHub/Wiki)
  require explicit user intent.
- Do not clone the AgentKit CLI, SQLite store, dashboard, hooks, or the
  `.ck.json` / `CK_SIMPLIFY_DISABLED` hidden state.
- Preserve each source skill's behavioral invariants; verify after normalize.
- Overlap-safe edits to shared root files (`README.md`, `skills.sh.json`,
  `scripts/validate-skills.sh`); do not erase prior portable-registry work.

### Non-goals

- Port skills outside the delivery loop (frontend/ui, media, deploy, security,
  MCP, etc.) unless `cook` provably requires one. `ui-ux-designer` and
  `fullstack-developer` are agent roles handled by native fallback, not ports.
- Recreate `code-simplifier` as a skill — keep the git-diff simplify gate as an
  optional native step.
- Any automatic external mutation.

### Acceptance Criteria

- Every ported skill passes the generic validator and a no-AgentKit-on-`PATH`
  discovery/pickup scenario.
- Each skill's source invariants map to target sections with verification
  evidence (research report per skill or per wave).
- `cook` orchestrates a real end-to-end task using the ported companions, and a
  second run with companions absent still completes via native fallback.
- No runtime instruction contains `/ak:*`, named source subagents, `.ck.json`,
  `CK_*`, `ak <command>` prose, or absolute source paths.
- Root catalog, grouping, and generated skill index stay current.

## Phases

| # | Phase | Status |
|---|---|---|
| 1 | [Port scout + define shared capability-handoff phrasing](./phase-01-scout.md) | Completed |
| 2 | [Port code-review](./phase-02-code-review.md) | Completed |
| 3 | [Port test](./phase-03-test.md) | Completed |
| 4 | [Port debug](./phase-04-debug.md) | Completed |
| 5 | [Port research](./phase-05-research.md) | Completed |
| 6 | [Port git](./phase-06-git.md) | Completed |
| 7 | [Port project-management](./phase-07-project-management.md) | Completed |
| 8 | [Port journal](./phase-08-journal.md) | Completed |
| 9 | [Port docs](./phase-09-docs.md) | Completed |
| 10 | [Port fix](./phase-10-fix.md) | Completed |
| 11 | [Port cook orchestrator (capstone)](./phase-11-cook.md) | Completed |
| 12 | [Program integration and end-to-end verification](./phase-12-integration-e2e.md) | Completed |

## Skill Inventory and Waves

| # | Skill | Wave | Source bytes |
|---|---|---|---|
| 1 | scout | A discovery | 11.8 KB |
| 2 | code-review | A verify-core | 36.6 KB |
| 3 | test | A verify-core | 12.5 KB |
| 4 | debug | A verify-core | 41.4 KB |
| 5 | research | B research | 7.0 KB |
| 6 | git | B finalize | 21.8 KB |
| 7 | project-management | B finalize | 15.1 KB |
| 8 | journal | B finalize | 1.4 KB |
| 9 | docs | B finalize | 15.5 KB |
| 10 | fix | C bug path | 55.4 KB |
| 11 | cook | D capstone | 38.0 KB |
| 12 | (integration) | E integration | n/a |

## Wave Rationale

- **Wave A (scout, code-review, test, debug):** `cook`'s mandatory delegations
  and scout gate. Highest orchestration value; port first.
- **Wave B (research, git, project-management, journal, docs):** `cook`'s Step 1
  research and Step 6 finalize toolchain. `project-management` sync-back is
  largely portable file logic already.
- **Wave C (fix):** sibling skill `cook` routes concrete bugs to. Largest source;
  reuses `debug` and `test`.
- **Wave D (cook):** capstone. Ported last so every handoff maps to a real
  portable skill; native fallbacks retained for missing runtimes.
- **Wave E:** cross-skill routing, catalog/index, and full end-to-end
  verification with and without companions present.

## Implementation Allowlist

- Create `skills/<name>/**` for each ported skill.
- Overlap-safe edits to `README.md`, `skills.sh.json`,
  `scripts/validate-skills.sh`, `scripts/generate-skill-index.py`, and
  `docs/skills/README.md`.
- Create per-skill research reports under `plans/reports/` and this plan
  directory's journal/report during finalization.
- Do not restore or edit user-owned deletions (`AGENTS.md`, `CHANGELOG.md`).

## Dependencies

- Design authority: `docs/portable-skill-contract.md`; the `cook` analysis in
  this session; per-skill research reports created at phase execution.
- Prior art: `plans/reports/research-260824-1243-vit-plan-migration.md` and the
  completed `vit-plan` / `brainstorm` ports.
- `brainstorm` and `vit-plan` must remain available (Wave 0).
- Phases 1–10 are independent of each other and may run in any order within
  their wave; each only requires Wave 0.
- Phase 11 (`cook`) should follow phases 1–10 to avoid double-rewriting
  handoffs, but can ship earlier as standalone-with-fallback if prioritized.
- Phase 12 requires every skill phase.

## Risks and Mitigations

- **Risk:** program scope is large; drift or half-ported skills accumulate.
  **Mitigation:** one skill fully done + verified per phase before the next;
  no phase closes without validator + no-AK scenario evidence.
- **Risk:** porting `cook` first would force rewriting handoffs twice.
  **Mitigation:** default order ports companions before `cook`.
- **Risk:** hidden coupling (`.ck.json`, `CK_*`, live task surface) leaks into a
  ported skill. **Mitigation:** recursive static scan gate in every phase's
  validation, reused from the `vit-plan` no-AK check.
- **Risk:** companion skills invent their own incompatible handoff vocabulary.
  **Mitigation:** shared capability-handoff phrasing defined in Phase 1 and
  reused by all later phases.

## Success Criteria

- [x] All 11 delivery-loop skills ported and individually verified.
- [x] `cook` runs a real end-to-end task through ported companions.
- [x] `cook` still completes with companions absent (native fallback).
- [x] Zero AgentKit CLI/subagent/hidden-state coupling in runtime instructions.
- [x] Catalog, grouping, and generated skill index current.
- [x] Existing worktree changes outside the allowlist untouched.

## Open Questions

1. Ship `cook` standalone-with-fallback early (before all companions) or strictly
   last? Recommendation: strictly last unless the user needs `cook` usable sooner.
2. Do we need `research`'s external web/docs capabilities in v1, or local-evidence
   only first? Recommendation: local-evidence core first, web optional.
3. Should `fix` reuse the ported `debug` as a hard dependency or keep a native
   fallback? Recommendation: optional-with-fallback, consistent with the contract.

<!-- slug: portable-cook-delivery-loop -->
