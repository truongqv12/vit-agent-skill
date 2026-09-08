# debug

Systematic debugging and system investigation that proves the root cause before
any fix. [`SKILL.md`](./SKILL.md) is the authority for behavior; this README
carries provenance and dependency notes.

## Provenance

- Source skill: `ak:debug` v4.0.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `debug`.

## Behavior invariants preserved

- **Prove root cause before any fix** — diagnosis-first is the core invariant.
- Multi-layer (defense-in-depth) validation guidance, call-stack tracing, log
  and CI/CD failure analysis, database diagnostics, and performance-bottleneck
  analysis.
- A structured diagnostic report (symptom → evidence → root cause →
  recommended fix).
- **Read/diagnose-first:** debug does not mutate behavior. Behavior changes are
  recommended to the caller (a fix or implementation capability).
- Log, CI/CD, and database access are capabilities with a native fallback:
  read logs, files, and run shell directly when no specialized capability
  exists.

## Dependencies

- **standalone.** Core debugging works with native content/name search, scoped
  file reads, and shell. Database (`psql`) and CI/CD (`gh`) tooling is used only
  when a database or GitHub Actions pipeline is actually in scope.

Optional accelerators (each with a native fallback):

- A file-discovery/scouting capability to locate relevant files. Absent →
  native content and name search.
- A documentation-lookup capability for package/plugin docs. Absent → read the
  project's own docs and sources.
- A repository-packing capability for a broad snapshot. Absent → scoped reads.
- A browser-automation capability for frontend visual verification. Absent →
  the project's browser tests, or skip and note it.
- A live task-management surface for multi-step investigation tracking.
  Absent → the active plan (the durable source of truth).

Diagnosis never depends on a particular client's tooling. External or delegated
execution requires explicit user permission.

## References

- [`references/systematic-debugging.md`](./references/systematic-debugging.md) —
  four-phase root-cause-first framework.
- [`references/root-cause-tracing.md`](./references/root-cause-tracing.md) —
  trace bugs backward through the call stack.
- [`references/defense-in-depth.md`](./references/defense-in-depth.md) —
  multi-layer validation guidance for the recommended fix.
- [`references/verification.md`](./references/verification.md) —
  evidence-before-claims completion gate.
- [`references/investigation-methodology.md`](./references/investigation-methodology.md) —
  five-step system-level investigation.
- [`references/log-and-ci-analysis.md`](./references/log-and-ci-analysis.md) —
  log and CI/CD (GitHub Actions) failure analysis.
- [`references/performance-diagnostics.md`](./references/performance-diagnostics.md) —
  bottleneck and query-performance diagnostics.
- [`references/reporting-standards.md`](./references/reporting-standards.md) —
  structured diagnostic report format.
- [`references/task-management-debugging.md`](./references/task-management-debugging.md) —
  investigation progress coordination.
- [`references/frontend-verification.md`](./references/frontend-verification.md) —
  browser-based visual verification (capability-gated).

## Scripts

- [`scripts/find-polluter.sh`](./scripts/find-polluter.sh) — optional bash
  bisection helper for finding which test creates unwanted file/state
  pollution. Portable (accepts a custom per-file test command). If it cannot
  run in the current runtime, the same bisection can be reproduced inline with
  native shell.
