---
name: test
description: "Run unit, integration, e2e, and UI tests with coverage and build verification, and emit a machine-readable PASS/FAIL summary a caller can gate on. Use for test execution, coverage analysis, visual regression, and structured QA reports."
user-invocable: true
when_to_use: "Invoke for running or designing validation suites, or to gate delivery on a clear pass/fail result."
category: dev-tools
keywords: [test, unit, integration, e2e, coverage, qa]
license: MIT
argument-hint: "[context] OR ui [url]"
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:test"
  source-version: "1.0.0"
  portability: standalone
---

# Test

Comprehensive testing and quality assurance: code-level testing (unit,
integration, e2e), UI/visual testing via a browser-automation capability,
coverage analysis, build verification, and a structured QA report that ends in a
machine-readable PASS/FAIL verdict.

## Capability handoff convention

When a step below names a companion capability (interactive prompting, browser
automation, screenshot analysis, debugging, output organization, task
tracking):

- Use that capability **only** when the runtime exposes it and the user's
  request permits it.
- Otherwise perform the step inline with native tools (file read, content
  search, shell) or project-native commands.
- If neither path is possible, stop and report the missing capability honestly.

Never emit a hard vendor slash-command or a named source subagent as the only
path. Native shell execution of the project's own test runner is the
always-available core.

## Default (no arguments)

If invoked with context (a test scope), proceed with testing. If invoked WITHOUT
arguments, ask the user which operation to run — use an interactive question
capability when the runtime exposes one, otherwise ask in plain text:

| Operation | Description |
|-----------|-------------|
| `(default)` | Run unit / integration / e2e tests |
| `ui` | Run UI tests on a website |

## Core principle

**NEVER IGNORE OR HIDE A FAILING TEST.** Fix root causes, not symptoms.

### Anti-cheat (forbidden)

The following are forbidden ways to make a suite appear green and must never be
used:

- Adding fake mocks or stubbed return values that bypass the behavior under test.
- Commenting out, deleting, or `skip`/`xfail`-ing tests to avoid a failure.
- Changing or weakening assertions so a failing test passes.
- Silently skipping tests, or excluding files/paths, to make a suite pass.

A suite is PASS only when the real tests run and genuinely pass. If tests fail,
report the failures honestly — do not manipulate the suite to hide them.

## When to use

- **After implementation:** validate new features or bug fixes.
- **Coverage checks:** ensure coverage meets project thresholds.
- **UI verification:** visual regression, responsive layout, accessibility.
- **Build validation:** verify build process, dependencies, CI compatibility.
- **Pre-commit / pre-push:** final quality gate.

## Test-runner detection

Detection is **project-driven**. Determine the runner from project
configuration and manifests, not from a guess:

- JS/TS: `package.json` scripts and dev dependencies (Jest, Vitest, Mocha),
  lockfile for the package manager (`npm`, `yarn`, `pnpm`, `bun`).
- Python: `pyproject.toml`, `pytest.ini`, `tox.ini`, `setup.cfg` (pytest,
  unittest).
- Go: `go.mod` with `_test.go` files (`go test`).
- Rust: `Cargo.toml` (`cargo test`).
- Flutter/Dart: `pubspec.yaml` (`flutter test`).

If the project's test runner cannot be determined from its configuration, this
is an **honest failure**: report that the runner is unknown and ask for the test
command. Do not guess a runner or fabricate a pass.

## Workflows

Load the matching reference for the case at hand:

### 1. Code testing (`references/test-execution-workflow.md`)

Execute test suites, analyze results, generate coverage, verify the build.
Supports JS/TS, Python, Go, Rust, Flutter with project-driven commands.

**Load when:** running unit/integration/e2e tests, checking coverage, validating
builds.

### 2. UI testing (`references/ui-testing-workflow.md`)

Browser-based visual testing through a browser-automation capability or
project-native Playwright/Vitest/k6 commands. Covers screenshots, responsive
checks, accessibility audits, form automation, and console-error collection.

**Load when:** visual regression, UI bugs, responsive layout, accessibility.

### 3. Report format (`references/report-format.md`)

Structured QA report template ending in a machine-readable overall verdict.

**Load when:** producing a test summary report.

## Working process

1. Identify testing scope from recent changes or requirements.
2. Detect the project's test runner (see above); fail honestly if unknown.
3. Run typecheck / analyze commands first to catch syntax errors early.
4. Execute the appropriate test suites.
5. Analyze results — focus on failures; never hide them.
6. Generate coverage reports if applicable.
7. For frontend work, run UI tests via a browser-automation capability or
   project-native browser tests.
8. Produce a structured summary report ending in a machine-readable PASS/FAIL
   verdict a caller can gate on.

## Companion capabilities (all optional, native fallback)

- **Browser automation** for UI tests — a live browser-driving capability, the
  user's real-profile browser capability when real login/cookie state is
  required, or project-native Playwright/Vitest/k6 runs. Absent → run
  project-native browser tests or report the gap.
- **Screenshot / vision analysis** to inspect captured screenshots. Absent →
  report screenshot paths without automated analysis.
- **Debugging capability** when tests reveal bugs needing investigation. Absent
  → report the failure and root-cause notes.
- **Structured-reasoning capability** for complex failure analysis. Absent →
  reason inline.
- **Output organization capability** to place the report. Absent → place it by
  the project's existing convention.

## Quality standards

- All critical paths must have test coverage.
- Validate the happy path AND error scenarios.
- Ensure test isolation — no interdependencies.
- Tests must be deterministic and reproducible.
- Clean up test data after execution.
- Never ignore failing tests to pass the build (see Anti-cheat).

## Report output

Produce the report per `references/report-format.md`. It MUST end with a single
machine-readable overall verdict line (`Overall: PASS` or `Overall: FAIL`) so a
calling workflow can gate on it. A caller that enforces 100% pass treats any
failed test, or an unknown-runner failure, as `Overall: FAIL`.

Organize the report into the project's expected location; use an output/file
organization capability if one is available, otherwise place it by the project's
existing convention.

## Team mode

When operating as a teammate:

1. Discover the live task-management and team-coordination surfaces, if present.
2. Claim the assigned or next unblocked item when supported; otherwise read and
   update the active plan.
3. Read the full work description before starting and wait for prerequisites.
4. Respect file ownership — only create/edit the test files assigned.
5. When done, record completion and report results through the live team
   surface.

Plan files are the durable source of truth when runtime task tracking is absent
or session-scoped.

## References

- `references/test-execution-workflow.md` — code test execution, coverage, build.
- `references/ui-testing-workflow.md` — browser-based UI/visual testing.
- `references/report-format.md` — QA report template with machine-readable verdict.

## Workflow position

**Typically follows:** an implementation capability (test after implementation)
or a fix capability (test after a bug fix).

**Typically precedes:** a code-review capability (review after tests pass).

**Related:** debugging and structured-reasoning capabilities when tests reveal
issues that need investigation.
