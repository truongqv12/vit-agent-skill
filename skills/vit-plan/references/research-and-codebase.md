# Research and Codebase Evidence

Research exists to resolve design uncertainty and prove current-state claims.
Skip work already covered by current, cited reports; verify report claims that
may have drifted.

## Evidence order

1. Read repository instructions and the root README.
2. Follow existing documentation navigation to requirements, architecture,
   security, design, and development standards relevant to the task.
3. Read unfinished related plans and supporting reports.
4. Inspect the owning source, tests, manifests, configuration, and build or
   deployment definitions.
5. Use current authoritative external documentation only when a dependency,
   standard, or public contract cannot be established locally.

Do not read secrets or broad private data. Inspect environment examples and
configuration schemas instead of credential-bearing files.

## Codebase analysis

- Locate actual entry points and trace calls, events, guards, and error paths.
- Identify conventions and existing reusable seams before proposing new ones.
- Enumerate consumers when a public or shared contract changes.
- Check tests for current guarantees and missing regression coverage.
- Map data lifetime, ownership, migrations, and compatibility boundaries.
- Record conflicting documentation as a finding; current executable evidence
  proves behavior, while accepted product intent proves the desired outcome.

Current-code claims cite `repo/relative/path:line`. When exact lines are
unstable, cite the closest owning symbol plus file and mark the limitation.

## Research execution

Partition broad work by independent question or approach. Optional delegates
may investigate those partitions concurrently, but each assignment needs a
bounded question, exact scope, evidence standard, and no overlapping writes.
If delegation is unavailable, perform the partitions sequentially.

For current external facts, prefer primary documentation. If search or network
access is unavailable, record the gap as `[UNVERIFIED]` and avoid a design that
depends on the unproved claim when a safer local alternative exists.

## Synthesis

Produce a compact evidence set for design:

- confirmed constraints and current patterns;
- affected files, contracts, and consumers;
- viable approaches and rejected alternatives;
- test, security, performance, and rollout implications;
- unresolved facts that could change the plan.

Research notes are supporting artifacts. Put durable decisions and citations
in the owning plan or phase section rather than requiring future implementers
to reconstruct the research trail.

