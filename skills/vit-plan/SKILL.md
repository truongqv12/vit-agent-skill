---
name: vit-plan
description: "Create and challenge evidence-backed implementation plans and phased technical roadmaps as portable Markdown. Use for feature planning, architecture, implementation strategy, validation interviews, or red-team plan review."
license: MIT
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:plan"
  source-version: "1.1.0"
  source-kit: "agentkit-engineer/2.4.0"
  portability: standalone
---

# Vit Plan

Create implementation plans without implementing production changes. The
Markdown plan and phase files are the durable authority; research reports,
runtime work items, and helper output are supporting or derived evidence.

## Route the request

- A task description starts the planning workflow below.
- `validate` plus a plan path loads
  [validation-workflow.md](references/validation-workflow.md).
- `red-team` plus a plan path loads
  [red-team-workflow.md](references/red-team-workflow.md).
- If the operation or target is unclear, ask one concise question. Use the
  runtime's structured question capability when available; otherwise ask in
  plain conversation.

## Planning workflow

1. Reuse an accepted outcome, constraints, non-goals, and acceptance criteria.
   Capture only material gaps; do not reopen settled intent without evidence.
2. Resolve the project root and scan `plans/*/plan.md` for relevant unfinished
   plans. Read overlapping plans before creating a competing plan. Confirm
   ambiguous `blockedBy` or `blocks` relationships with the user.
3. Unless the request is explicitly fast or trivial, run the
   [scope challenge](references/scope-challenge.md).
4. Select a proportional mode using
   [workflow modes](references/workflow-modes.md). Delegation is optional;
   preserve the same work and evidence sequentially when it is unavailable.
5. Inspect repository instructions, documentation, source, tests, and current
   plans using [research and codebase guidance](references/research-and-codebase.md).
6. Choose the smallest evidence-supported solution using
   [solution design](references/solution-design.md).
7. Create project-local artifacts using
   [plan organization](references/plan-organization.md), the physical
   templates, and [output standards](references/output-standards.md). Never
   overwrite an existing plan or phase.
8. Apply the mode's verification, red-team, and validation gates. Any proposed
   correction requires user adjudication before plan files change.
9. After review edits, re-read `plan.md` and every phase file using the
   [whole-plan consistency sweep](references/verification-roles.md#whole-plan-consistency-sweep).
10. Optionally mirror work through
    [task management](references/task-management.md). `--no-tasks` skips this;
    lack of a runtime task surface never blocks planning.

## Artifact creation

The optional standard-library helper under `scripts/plan-tool.py` can create,
add, and structurally lint artifacts. Discover its exact interface with its
native help output. If Python or the helper is unavailable:

1. Copy [plan.md](templates/plan.md) and [phase.md](templates/phase.md) with
   native file operations.
2. Replace only the documented tokens.
3. Follow the naming, collision, schema, link, dependency, and section checks in
   [plan organization](references/plan-organization.md#native-fallback).
4. Read every generated file back before reporting success.

## Boundaries

- Plan only. Do not edit product code, tests, configuration, or deployment
  state.
- Default to project-local `plans/`; do not invent another plan root.
- Never claim current behavior from intent alone. Mark unresolved evidence
  gaps explicitly.
- Do not perform external or irreversible effects as part of this workflow.
- Preserve explicit user decisions. A later audit may reverse one only with new
  evidence and renewed user approval.
- End with the plan path, selected mode, completed gates, and unresolved
  questions. Offer an available implementation capability only after the plan
  is consistent and the user chooses to proceed.
