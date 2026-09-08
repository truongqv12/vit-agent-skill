# Capability Activation Matrix

Which capability to use at each step of a fixing workflow. Every capability
below has a native fallback (read, search, shell, git) per the parent skill's
Capability handoff convention; none is a hard dependency.

## Always (all workflows)

Before using any capability, capture or reuse the opening outcome, safety
boundary, non-goals, and acceptance criteria. This is a workflow gate, not a
separate step.

| Capability | Step | Reason | Native fallback |
|------------|------|--------|-----------------|
| **scouting** | Step 1 | Understand codebase context before diagnosing | Native search + scoped reads |
| **debugging / root-cause** | Step 2 | Systematic root-cause investigation | Structured reasoning over evidence |
| **task-tracking** | Step 6 | Sync-back and progress tracking (every fix) | Update the active plan |

## Progress orchestration (Moderate+ only)

| Capability | Use when |
|------------|----------|
| **task-tracking** | After complexity assessment, when runtime discovery confirms a live surface |
| **delegation** (parallel agents) | User explicitly requested subagents/parallel work AND runtime permits it |

Skip progress orchestration for Quick (< 3 steps).

## Auto-triggered

| Capability | Trigger |
|------------|---------|
| structured problem-solving | 2+ hypotheses refuted in Step 2 diagnosis |

## Conditional

| Capability | Use when |
|------------|----------|
| **ideation** | After diagnosis, when multiple valid approaches or an architecture decision remain |
| **context-engineering** | Fixing AI/LLM/agent code or context-window issues |
| **visual/multimodal** | UI issues, screenshots provided, visual bugs |

## By workflow

| Workflow | Capabilities |
|----------|--------------|
| Quick | intent frame, scouting (minimal), debugging, code-review, task-tracking, shell verification |
| Standard | Quick set + optional task-tracking, auto problem-solving, optional post-diagnosis ideation, optional delegated testing/exploration when permitted |
| Deep | Standard set + post-diagnosis ideation, context-engineering, research, planning |
| Parallel | per-issue trees + task-tracking + delegated implementation agents + live coordination when available |

## Step -> capability chain (mandatory order)

| Step | Chain |
|------|-------|
| Opening gate | outcome -> safety boundary -> non-goals -> acceptance criteria |
| Step 0: Mode | interactive-prompt only when mode is not explicit or safely inferable |
| Step 1: Scout | scouting OR parallel exploration when permitted -> map files, deps, tests |
| Step 2: Diagnose | capture pre-fix state -> debugging -> structured hypotheses -> optional delegated exploration -> (problem-solving if 2+ fail) |
| Step 3: Assess | classify complexity -> direct cause-aligned fix or post-diagnosis ideation -> record dependencies (Moderate+) |
| Step 4: Fix | implement per route -> follow root cause |
| Step 5: Verify+Prevent | iron-law verify -> regression test -> side-effect sweep -> defense-in-depth -> shell verify -> code-review |
| Step 6: Finalize | report -> task-tracking sync (mandatory) -> docs-impact decision -> conditional documentation -> version-control -> optional journaling |

## Detection triggers

| Keyword/pattern | Capability to consider |
|-----------------|------------------------|
| "AI", "LLM", "agent", "context" | context-engineering |
| "stuck", "tried everything" | structured problem-solving |
| "complex", "multi-step" | structured reasoning |
| "which approach", "options" | ideation |
| "current docs", "best practice" | research |
| Screenshot attached | visual/multimodal |
