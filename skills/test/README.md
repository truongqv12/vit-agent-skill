# test

Run unit, integration, e2e, and UI tests, analyze coverage, verify the build,
and emit a machine-readable PASS/FAIL verdict. [`SKILL.md`](./SKILL.md) is the
authority for behavior; this README carries provenance and dependency notes.

## Provenance

- Source skill: `ak:test` v1.0.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `test`.

## Dependencies

- **standalone.** Core testing works by running the project's own test runner
  through native shell, plus native file read/search for scope detection and
  report writing.

Optional accelerators (each with a native fallback):

- A **browser-automation capability** for UI/visual tests (a live tool-managed
  browser, or the user's real-profile browser when real login/cookie state is
  needed). Absent → project-native Playwright/Vitest/k6, or report the gap.
- A **screenshot / vision-analysis capability** to inspect captured
  screenshots. Absent → reference saved screenshot paths.
- A **debugging capability** when tests reveal bugs. Absent → report failures
  with root-cause notes.
- A **structured-reasoning capability** for complex failure analysis. Absent →
  reason inline.
- An **output/file-organization capability** to place the report. Absent →
  place it by the project's existing convention.
- A **live task/team-coordination surface** for team mode. Absent → the active
  plan is the durable source of truth.

External or delegated execution requires explicit user permission.

## Behavior invariants preserved

- Execution of unit, integration, e2e, and UI tests; coverage analysis; build
  verification.
- Anti-cheat: no fake mocks, no commented-out/skipped tests, no weakened
  assertions, no silent skipping to make a suite pass.
- A machine-readable overall `PASS`/`FAIL` verdict a caller can gate on (a
  100%-pass gate treats any failure or unknown runner as `FAIL`).
- Project-driven test-runner detection; an undeterminable runner is an honest
  failure, never a guess.

## References

- [`references/test-execution-workflow.md`](./references/test-execution-workflow.md)
  — code test execution, coverage, and build verification.
- [`references/ui-testing-workflow.md`](./references/ui-testing-workflow.md) —
  browser-based UI/visual testing.
- [`references/report-format.md`](./references/report-format.md) — QA report
  template ending in a machine-readable verdict.
