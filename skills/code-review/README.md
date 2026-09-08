# code-review

Evidence-based, production-readiness code review across pending changes, a PR, a
commit, or a full codebase. [`SKILL.md`](./SKILL.md) is the authority for
behavior; this README carries provenance and dependency notes.

## Provenance

- Source skill: `ak:code-review` v2.0.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `code-review`.

## Dependencies

- **standalone.** The full review pipeline runs with native tools: content/name
  search, scoped file reads, shell, and `git` (`git diff`, `git show`,
  `git rev-parse`).

Optional accelerators (each with a native fallback):

- A **scouting** capability for edge-case discovery. Absent → search and read
  affected files with native tools.
- A **code-review delegation** capability (e.g. a reviewer subagent) for
  Stage 2 quality review and parallel scopes. Absent → review inline against the
  diff.
- A **GitHub CLI (`gh`)** capability for PR mode. Explicit-intent and optional;
  absent → fetch the branch and review with native `git diff <base>...<head>`.
- A **testing** capability for verification. Absent → run the project's test,
  build, and lint commands directly.
- A **live task-management surface** for the scout → review → fix → verify chain.
  Absent → track states in the active plan (the durable source of truth).
- **research** and **planning** capabilities used by the codebase-scan workflow.
  Absent → search sources and draft the plan inline.
- An **interactive prompt** capability for resolving an ambiguous target. Absent
  → ask the user in conversation.

Delegated or external execution requires explicit user permission. Reviewing is
read-only until the user accepts a fix.

## Behavioral invariants preserved

- The **(a-e) mandatory completion checks** (acceptance criteria, no regression,
  no breaking public-contract changes, follows existing patterns, no new
  lint/type/build errors) — expressed standalone in `SKILL.md`.
- Four input modes: pending changes, PR number, commit hash, and full codebase
  scan (plus a parallel codebase audit).
- Evidence-based findings (`file:line`), severity tiers
  (critical / warning / suggestion), a score out of 10, and no-false-positive
  discipline.
- Staged pipeline: spec compliance → code quality → verification, with edge-case
  scouting first and verification gates before any completion claim.

## References

- [`references/input-mode-resolution.md`](./references/input-mode-resolution.md) — resolve arguments into a reviewable diff.
- [`references/spec-compliance-review.md`](./references/spec-compliance-review.md) — Stage 1 spec/plan match.
- [`references/code-review-reception.md`](./references/code-review-reception.md) — receiving feedback with rigor.
- [`references/requesting-code-review.md`](./references/requesting-code-review.md) — request a quality review over a diff.
- [`references/verification-before-completion.md`](./references/verification-before-completion.md) — evidence gates before claims.
- [`references/edge-case-scouting.md`](./references/edge-case-scouting.md) — scout edge cases before review.
- [`references/checklist-workflow.md`](./references/checklist-workflow.md) — checklist-based pre-landing review.
  - [`references/checklists/base.md`](./references/checklists/base.md), [`api.md`](./references/checklists/api.md), [`web-app.md`](./references/checklists/web-app.md) — checklist bodies.
- [`references/task-management-reviews.md`](./references/task-management-reviews.md) — track the review pipeline.
- [`references/codebase-scan-workflow.md`](./references/codebase-scan-workflow.md) — full codebase scan.
- [`references/parallel-review-workflow.md`](./references/parallel-review-workflow.md) — parallel edge-case verification.
