# Companion Capability Patterns

Standard patterns for invoking companion capabilities in cook workflows. Each
follows the Capability Handoff Convention: use the delegation capability with the
named companion when the runtime exposes it and the user permits it; otherwise
perform the step inline with native tools; if neither is possible, stop and
report honestly.

## Delegation pattern (when available)

```
delegate to <capability> with: prompt="[task]", context="[scope]"
```

## Research

```
<research> : "Research [topic]. Report ≤150 lines with citations."
```
- Use multiple research passes in parallel only when delegation exists.

## Scout

```
<scout> : "Find files related to [feature] in the codebase."
```

## Planning

```
<vit-plan> : "Create an implementation plan from these reports: [reports]. Save to [path]."
```
- Input: research and scout reports. Output: `plan.md` + `phase-XX-*.md`.

## UI Implementation

```
<ui/design capability> : "Implement [feature] UI per the project's discovered design guidance."
```
- Frontend work only; follow design guidelines. Native fallback: implement per adjacent component conventions.

## Testing

```
<test> : "Run the test suite for plan phase [phase-name]."
```
- Must achieve 100% pass. Native fallback: run the project's test command via shell.

## Debugging

```
<debug> : "Analyze failures: [details]. Prove the root cause before any fix."
```
- Use when tests fail; provides root-cause analysis. Native fallback: read logs/stack traces directly.

## Code Review

```
<code-review> : "Review changes for [phase] against these MANDATORY checks: (a) every acceptance criterion met; (b) no regression to business logic in touchpoints/blast-radius from scout; (c) no breaking changes to public contracts (signatures, schemas, APIs, env vars) unless explicitly called out; (d) follows existing patterns from scout; (e) no new lint/type/build errors anywhere. CONTEXT — scout summary: <scout-summary>; acceptance criteria: <acceptance-criteria>. Return score (X/10), critical, warnings, suggestions, and explicitly flag any side effects to trigger HARD-GATE-NO-SIDE-EFFECTS."
```

## Conditional Simplify

```
<simplification capability> : "Simplify these files while preserving behavior exactly: [file-list]"
```
- Trigger when the live `git diff --numstat HEAD --ignore-all-space` breaches any threshold (defaults: 400 LOC / 8 files / 200 single-file LOC; a project may override in its kit configuration).
- Scope the prompt to `git diff --name-only HEAD`.
- Verify with `git diff --shortstat HEAD -- [file-list]` before/after; do not rely on prose.
- Skip when the project disables the gate or no simplification capability exists.

## Project Management (MANDATORY at Finalize)

```
<project-management> : "Run full sync-back in [plan-path]: reconcile completed tasks with all phase files, backfill stale completed checkboxes across all phases, update plan.md status/progress, and report unresolved mappings."
```
- Native fallback: edit plan/phase checkboxes and the plan Status column directly.

## Documentation

```
<docs> : "Update docs for [phase]. Changed files: [list]. Scope to changed authority surfaces only."
```

## Git Operations

```
<git> : "Stage and commit changes with a conventional commit message, after explicit user confirmation."
```

## Journal

```
<journal> : "Write a concise technical journal entry for this completed work."
```

## Parallel Execution

```
<implementation capability> : "Implement [phase-file] with file ownership: [files]"
```
- Launch multiple for parallel phases only when delegation exists; include file ownership boundaries. Native fallback: implement phases sequentially with the same ownership graph.
