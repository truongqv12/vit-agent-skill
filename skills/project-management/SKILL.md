---
name: project-management
description: "Track progress, update plan statuses, coordinate runtime work, generate reports, and preserve cross-session continuity. Invoke for progress tracking, plan status updates, whole-plan sync-back, or cross-session handoffs."
user-invocable: true
when_to_use: "Invoke for progress tracking, plan status, or handoffs."
category: utilities
keywords: [project, progress, status, reports, plan, sync-back]
argument-hint: "[task: status, hydrate, sync, report]"
license: MIT
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:project-management"
  source-version: "1.0.0"
  portability: standalone
---

# Project Management

Project oversight and coordination with durable plan files as the sole authority
and optional runtime task tracking. Plan files (`plan.md` plus every
`phase-XX-*.md`) are the durable source of truth; every other surface is a
disposable working view.

**Principles:** Token efficiency | Concise reports | Data-driven insights

## Capability handoff convention

When a step below names a companion capability (a live task-management surface,
a documentation capability, a plan-linter helper, a review or test capability):

- Use that capability when the runtime exposes it and the user's request permits
  it.
- Otherwise perform the step inline with native tools (file read, content
  search, shell, direct edits to the plan and phase files).
- If neither path is possible, stop and report the missing capability honestly.

Never emit a source-specific command or a named source subagent as the only
path, and never treat an optional capability as required.

## When to Use

- Checking project status or progress across plans
- Updating plan statuses after feature completion
- Mirroring plan work into a live task-management surface
- Generating status reports or summaries
- Coordinating documentation updates after milestones
- Verifying task completeness against acceptance criteria
- Cross-session resume of multi-phase work

## Runtime Capability Contract

Discover the live task-management surface at runtime. Use it when available to
mirror work, dependencies, ownership, and status. Otherwise, update the active
plan directly. Never infer availability from a client name or a cached tool
list. Plan files are the durable source of truth, and sync-back MUST work
without any runtime task tracking.

Plans in this repo follow the `vit-plan/v1` Markdown schema. Treat the plan and
phase templates under `skills/vit-plan/templates/` as the field authority; do
not invent frontmatter fields to serve a particular runtime task system.

## Core Capabilities

### 1. Runtime Work Tracking
Load: `references/task-operations.md`

When a live task-management surface exists:
- Mirror plan items with enough context to map them back to their source
- Track pending, active, blocked, and completed state
- Preserve dependency relationships
- Coordinate parallel agents with scoped ownership

### 2. Session Bridging (Hydration Pattern)
Load: `references/hydration-workflow.md`

Runtime tracking may be ephemeral. Plan files are durable. The hydration pattern
bridges them:
- **Hydrate:** Read unchecked plan items and mirror them when a live surface exists
- **Work:** Track live progress when possible; otherwise update the active plan
- **Sync-back:** Reconcile completed work across ALL phase files, update `[ ]` → `[x]`, derive phase and plan status from checkbox state
- **Resume:** Next session re-hydrates from remaining `[ ]` items

### 3. Progress Tracking
Load: `references/progress-tracking.md`

- Scan `plans/*/plan.md` for active plans
- Parse YAML frontmatter for status, priority, effort
- Count `[x]` vs `[ ]` in each phase `## Todo` section for completion %
- Cross-reference completed work against planned tasks
- Verify acceptance criteria met before marking complete

### 4. Documentation Coordination
Load: `references/documentation-triggers.md`

Trigger `docs/` updates when:
- Phase status changes, major features complete
- API contracts change, architecture decisions made
- Security patches applied, breaking changes occur

Route the actual update through a documentation capability when the runtime
exposes one; otherwise update the smallest owning doc inline with native edits.

### 5. Status Reporting
Load: `references/reporting-patterns.md`

Generate reports: session summaries, plan completion, multi-plan overviews.
- Use naming: `{reports-path}/pm-{date}-{time}-{slug}.md` (default reports path
  `plans/reports/`)
- Sacrifice grammar for brevity; use tables over prose
- List unresolved questions at end

## Workflow

```
[Scan Plans] → [Hydrate Tasks] → [Track Progress] → [Update Status] → [Generate Report] → [Trigger Doc Updates]
```

1. Read the durable plan and discover the live task-management surface
2. If the live view is empty, hydrate it from unchecked plan items
3. During work, update the live view when available; otherwise update the active plan
4. On completion: run full-plan sync-back (all phase files, including backfill for earlier phases), then derive frontmatter status from checkbox state
5. Generate a status report to the reports directory
6. Coordinate doc updates if changes warrant

## Mandatory Sync-Back Guard

When updating plan status, NEVER mark only the currently active phase.

1. Sweep ALL `phase-XX-*.md` files under the target plan directory.
2. Reconcile every completed runtime item to its source phase and checklist item.
3. Backfill stale completed checkboxes in earlier phases before marking later phases done.
4. Derive each phase's frontmatter `status` from its `## Todo` checkbox state
   (none checked → `pending`, some → `in-progress`, all → `completed`).
5. Derive `plan.md` frontmatter `status` from the phase statuses, and update each
   Phases-table Status cell to match its phase frontmatter (change only the cell;
   preserve the table structure exactly).
6. If any completed task cannot be mapped to a phase file, report unresolved
   mappings and do not claim full completion.

### Native-first, plan files are authority

Sync-back edits the Markdown plan and phase files directly — this is the always
available path and requires no runtime task surface. There is no external plan
store: the files are the store.

Optional verification: when a plan-linter helper is exposed, run it to confirm
the plan and phase files stay internally consistent after sync-back — for this
repo, `python skills/vit-plan/scripts/plan-tool.py lint <plan-dir>` checks that
each Phases-table Status cell matches its phase frontmatter and that the schema
holds. Absent that helper, re-read the edited files and confirm the table and
frontmatter agree by eye.

## Plan Schema

All plans follow the `vit-plan/v1` schema. `plan.md` frontmatter carries
`schemaVersion`, `title`, `description`, `status`, `priority`, `effort`, `tags`,
`blockedBy`, `blocks`, and `created`; each `phase-XX-*.md` carries
`schemaVersion`, `id`, `title`, `status`, and `dependencies`. Plan and phase
`status` is one of `pending`, `in-progress`, `blocked`, or `completed`.

Update `status` only when the underlying checkbox state justifies the
transition. The templates under `skills/vit-plan/templates/` are the field
authority — do not copy or fork that list here.

## Quality Standards

- All analysis data-driven, referencing specific plans and reports
- Focus on business value delivery and actionable insights
- Highlight critical issues requiring immediate attention
- Maintain traceability between requirements and implementation

## Related Capabilities

- A planning capability that produces the `vit-plan/v1` plans this skill tracks
  (in this repo, the `vit-plan` skill).
- An implementation/execution capability that invokes this skill at its finalize
  step to run whole-plan sync-back.
- A visual plan-dashboard capability for browsing plans, when one is exposed.

Name these only as examples of a capability; resolve the actual handoff through
the runtime's live capabilities, never a fixed source command.
