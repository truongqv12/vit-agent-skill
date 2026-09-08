---
schemaVersion: "vit-plan/v1"
id: "phase-01"
title: "Port scout + define shared capability-handoff phrasing"
status: completed
dependencies: []
---

# Phase 1: Port scout

## Context

`cook`'s HARD-GATE-SCOUT-FIRST requires codebase orientation before planning.
`scout` is small and low-coupling, so it ports first and also establishes the
**shared capability-handoff vocabulary** every later phase reuses (how to phrase
"use the review capability, else native fallback").

## Related Files

- Source skill (installed, read-only, not in repo): `ak-scout` — 3 md, ~11.8 KB
- Create: `skills/scout/SKILL.md`, `skills/scout/README.md`, references as used
- Create: `plans/reports/research-<ts>-scout-migration.md`
- Modify: `skills.sh.json`, `docs/skills/README.md` (overlap-safe)

## Implementation Steps

1. Inventory source; classify coupling (`/ak:*`, named agents, OpenCode probes,
   Explore-agent handoff).
2. Define the reusable handoff phrasing block: capability-first, native
   Glob/Grep/`Explore` fallback, honest missing-dependency behavior.
3. Normalize identity to `scout`; strip source CLI/agent names.
4. Preserve invariants: fast file discovery, scoped searches, task-context
   gathering, read-only.
5. Register in catalog/grouping; regenerate skill index.

## Todo

- [x] Coupling scan recorded in research report.
- [x] Shared handoff phrasing documented for reuse by phases 2-11.
- [x] `scout` passes validator and no-AK discovery.

## Validation

- Zero `/ak:*`, named-subagent, or absolute source paths in runtime files.
- Scout scenario returns relevant files without AgentKit on `PATH`.

## Risks and Mitigations

Optional Explore/OpenCode acceleration could become a hard dependency. Keep
native search as the guaranteed path.

## Rollback

Remove `skills/scout/**` and revert the overlap-safe catalog/index hunks.
