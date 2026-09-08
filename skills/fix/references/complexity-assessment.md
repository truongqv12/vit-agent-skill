# Complexity Assessment

Classify issue complexity before routing to a workflow. Assessment happens AFTER
Step 1 (Scout) and Step 2 (Diagnose).

## Simple (-> workflow-quick.md) — no progress tracking

**Indicators:**

- Single file affected.
- Clear error message (type error, syntax, lint).
- Keywords: `type`, `typescript`, `tsc`, `lint`, `eslint`, `syntax`.
- Obvious fix location.
- Root cause confirmed by diagnosis (not assumed).

**Tracking:** skip. < 3 steps, overhead exceeds benefit.

**Examples:** "Fix type error in auth.ts", "ESLint errors after upgrade",
"Syntax error in config file".

## Moderate (-> workflow-standard.md) — track 6 phases

**Indicators:**

- 2-5 files affected.
- Root cause identified but fix spans multiple files.
- Needs investigation to confirm diagnosis.
- Keywords: `bug`, `broken`, `not working`, `fails sometimes`.
- Test failures with root cause traced.

**Tracking:** record the six phase dependencies in the active plan, and mirror
them into a live task-tracking capability when the runtime exposes one.

**Examples:** "Login sometimes fails", "API returns wrong data", "Component not
rendering correctly".

## Complex (-> workflow-deep.md) — track 9 phases with dependency chains

**Indicators:**

- System-wide impact (5+ files).
- Architecture decision needed.
- Research required for the solution.
- Keywords: `architecture`, `refactor`, `system-wide`, `design issue`.
- Performance/security vulnerabilities.
- Multiple interacting components.
- Root cause spans multiple layers/modules.

**Tracking:** record all nine phases and their dependencies. Scout + diagnose +
research may run in parallel; mirror the plan into a live task-tracking
capability when available.

**Examples:** "Memory leak in production", "Database deadlocks under load",
"Security vulnerability in auth flow".

## Parallel (-> parallel implementation agents) — track per-issue trees

**Triggers:**

- `--parallel` explicitly passed (activate parallel routing regardless of
  auto-classification).

**Indicators:**

- 2+ independent issues mentioned.
- Issues in different areas (frontend + backend, auth + payments).
- No dependencies between issues.
- Keywords: a list of issues, "and", "also", multiple error types.

**Tracking:** keep a separate dependency tree per independent issue
(scout + diagnose + fix + verify) and assign one non-overlapping scope per
agent. Parallel agents run only when the runtime permits delegation and the user
requested it; otherwise handle the issues sequentially in the main agent.

**Examples:** "Fix type errors AND update UI styling", "Auth bug + payment
integration issue", "3 different test failures in unrelated modules".
