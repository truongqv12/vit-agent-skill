# Task Management

Plan files are the durable source of truth. A runtime task view is an optional,
session-scoped projection for visibility and coordination.

## Capability contract

1. Discover whether the current runtime exposes task tracking.
2. If available, mirror plan items, dependencies, ownership, and status.
3. If unavailable, manage progress directly in phase checkboxes and
   frontmatter.
4. Never infer availability from a client name or cached tool list.
5. When runtime and Markdown states disagree, verify evidence and make the plan
   files authoritative.

## When to hydrate

Hydrate only after `plan.md` and all phase files exist. By default, use runtime
tracking for plans with at least three meaningful phases. Skip for smaller
plans or when `--no-tasks` is requested.

## Projection rules

- Map every runtime item to one phase file and checklist item.
- Preserve dependency order and exclusive ownership.
- Mirror critical or high-risk steps when phase-level items are too coarse.
- Do not create runtime-only scope, acceptance criteria, or decisions.
- Runtime item counts and progress are advisory.

If tracking is unavailable, the same work proceeds sequentially from unchecked
phase items. This fallback is complete, not degraded planning.

## Sync back

1. Read every phase file, not only the active phase.
2. Confirm completion evidence for each runtime-complete item.
3. Update the mapped checkbox and phase status.
4. Derive plan status from actual phase state.
5. Report unmapped or contradictory items before claiming completion.

Runtime task mutation is an internal projection only. It does not authorize
implementation, external publication, or any other side effect.

## Quality checks

- No dependency cycle exists in either representation.
- Parallel items do not claim overlapping file ownership.
- Every completed item has observable evidence.
- Every runtime item maps back to durable plan work.
- A stale or unavailable task surface is reported plainly and never blocks the
  file-based workflow.
