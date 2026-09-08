# fix

Repair a concrete bug, error, test failure, or CI/CD failure with intelligent
routing across bug types. [`SKILL.md`](./SKILL.md) is the authority for
behavior; this README carries provenance and dependency notes.

## Provenance

- Source skill: `ak:fix` v2.1.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `fix`.

## Behavior invariants preserved

- **Frame first:** capture the expected repaired behavior and safety boundary
  (outcome, constraints, non-goals, acceptance criteria) before touching code.
- **Prove root cause before selecting a fix:** scout then diagnose; symptom
  fixes and guessing are failure. Cite `file:line` evidence and a full
  root-cause checklist before any repair.
- **Cause-aligned, side-effect-free:** apply the smallest repair that addresses
  the root cause, then verify no regression across the blast radius with fresh
  evidence and public-contract checks.
- **Intelligent routing across bug types:** type errors, lint, log errors, UI
  bugs, test failures, and CI/CD failures each have a dedicated route, with a
  native fallback whenever a specialized sub-capability is absent.
- **3-attempt architecture gate:** after 3 failed fix attempts, stop and
  question the architecture with the user.
- **Distinct from feature work:** `fix` repairs broken behavior; building new
  behavior is handed off to an implementation capability.

## Dependencies

- **standalone.** The full fix loop works with native tools: content/name
  search, scoped file reads, and shell for reproduction, tests, typecheck,
  lint, build, and git.

Optional accelerators (each with a native fallback):

- A **scouting** capability to map affected files. Absent -> native search + reads.
- A **debugging / root-cause** capability for structured diagnosis. Absent ->
  inline structured reasoning over read/search/shell evidence.
- A **testing** capability for regression tests and verification. Absent -> run
  the project's own test command via shell.
- A **code-review** capability for the post-fix review. Absent -> inline review
  of the changed diff.
- **Ideation**, **research**, and **planning** capabilities for complex fixes.
  Absent -> compare options and write the plan inline.
- A **task-tracking** capability for multi-phase progress. Absent -> the active
  plan (the durable source of truth).
- **Documentation**, **version-control**, and **journaling** capabilities at
  finalize. Absent -> edit docs directly, commit via git, skip journaling.
- An **interactive-prompt** capability for mode choice and regression
  escalation. Absent -> ask in conversation.
- **Browser-automation** and **visual/multimodal** capabilities for UI bug
  verification. Absent -> the project's browser tests, or skip and note it.

No capability is required; each names a native fallback. Delegated, external, or
parallel-agent execution requires explicit user permission.

## References

- [`references/mode-selection.md`](./references/mode-selection.md) — mode-choice prompt and recommendations.
- [`references/complexity-assessment.md`](./references/complexity-assessment.md) — Simple/Moderate/Complex/Parallel classification.
- [`references/workflow-quick.md`](./references/workflow-quick.md) — fast scout -> diagnose -> fix -> verify cycle.
- [`references/workflow-standard.md`](./references/workflow-standard.md) — full moderate-complexity pipeline.
- [`references/workflow-deep.md`](./references/workflow-deep.md) — research + ideation + plan for complex issues.
- [`references/review-cycle.md`](./references/review-cycle.md) — autonomous vs human-in-the-loop review handling.
- [`references/capability-activation-matrix.md`](./references/capability-activation-matrix.md) — which capability to use at each step.
- [`references/parallel-exploration.md`](./references/parallel-exploration.md) — parallel exploration/verification coordination.
- [`references/workflow-ci.md`](./references/workflow-ci.md) — CI/CD pipeline failures.
- [`references/workflow-logs.md`](./references/workflow-logs.md) — application log analysis.
- [`references/workflow-test.md`](./references/workflow-test.md) — test-suite failures.
- [`references/workflow-types.md`](./references/workflow-types.md) — type errors.
- [`references/workflow-ui.md`](./references/workflow-ui.md) — visual/UI issues (capability-gated).
