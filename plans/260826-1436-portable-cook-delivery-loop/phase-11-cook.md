---
schemaVersion: "vit-plan/v1"
id: "phase-11"
title: "Port cook orchestrator (capstone)"
status: completed
dependencies: ["phase-01","phase-02","phase-03","phase-04","phase-05","phase-06","phase-07","phase-08","phase-09","phase-10"]
---

# Phase 11: Port cook (capstone)

## Context

Port `cook` last so every handoff resolves to a real portable skill while
retaining native fallbacks. Source has 35 `/ak:*` refs, 48 named-subagent refs,
18 `delegate_agent`, 9 `ask_user`, 9 live-task-surface refs, and the `.ck.json`
/ `CK_SIMPLIFY_DISABLED` hidden simplify state.

## Related Files

- Source skill (installed, read-only, not in repo): `ak-cook` — 7 md, ~38.0 KB
- Create: `skills/cook/**`, `plans/reports/research-<ts>-cook-migration.md`
- Modify: catalog, grouping, generated index (overlap-safe)

## Implementation Steps

1. Write the full cook migration research report (executive summary → invariants
   → coupling → target design), reusing this session's analysis.
2. Preserve invariants verbatim in intent: 4 HARD-GATEs (brainstorm-first,
   plan-before-code, scout-first, no-side-effects), anti-rationalization table,
   6 modes + `--tdd`, review gates, mandatory-delegation contract, whole-plan
   finalize sync-back, plan-file-as-authority.
3. Map handoffs to ported skills: `scout`, `research`, `vit-plan` (plan),
   `code-review`, `test`, `debug`, `git`, `project-management`, `docs`,
   `journal`, `fix`; each capability-first with native sequential fallback.
4. Rewrite the simplify gate: keep git-diff-driven thresholds, drop `.ck.json`
   and `CK_SIMPLIFY_DISABLED`; read thresholds from kit config or defaults.
5. Replace `delegate_agent`/`ask_user` with capability + plain-text fallback;
   live task surface stays optional projection over plan files.
6. Make Finalize external effects (commit, docs, journal) explicit-intent.
7. Register and regenerate index.

## Todo

- [x] All 4 HARD-GATEs + anti-rationalization preserved.
- [x] Every handoff maps to a ported skill with native fallback.
- [x] `.ck.json` / `CK_*` hidden state removed; simplify gate portable.
- [x] Passes validator and no-AK scenario.

## Validation

- End-to-end run drives ported companions on a real task.
- Second run with companions absent still completes via native fallback.
- Zero `/ak:*`, named-subagent, `.ck.json`, `CK_*`, or `ak <command>` refs.

## Risks and Mitigations

Orchestration assumes companions always exist. Every step must state its native
fallback; the no-companion scenario is a required gate.

## Rollback

Remove `skills/cook/**` and revert index/catalog hunks.
