# Solution Design

Design against the accepted delivery contract and current evidence. Apply
YAGNI, KISS, and DRY in that order.

## Choose the approach

1. State the requirements and constraints the design must satisfy.
2. Reuse existing components, patterns, and contracts where they fit.
3. Compare multiple approaches only when the trade-off is material.
4. Evaluate compatibility, complexity, effort, failure modes, testing, rollout,
   and rollback.
5. Recommend the smallest approach that satisfies acceptance criteria.
6. Record why rejected alternatives are unnecessary or riskier now.

Do not introduce an abstraction, service, migration, dependency, or governance
surface solely for hypothetical future use.

## Required design lenses

### Contracts and data

- Inputs, outputs, validation, errors, and compatibility.
- Data ownership, lifetime, consistency, and migration behavior.
- All known callers, consumers, exports, and configuration surfaces.

### Security

- The actual assets, trust boundaries, identities, and exposed inputs.
- Authentication, authorization, secret handling, privacy, injection, and
  dependency risks relevant to that threat model.
- Safe defaults and failure behavior; avoid generic security checklists with no
  connection to the system.

### Reliability and performance

- Partial failures, retries, idempotency, concurrency, and recovery.
- Resource or latency bottlenecks supported by expected load or current data.
- Observability needed to verify rollout and diagnose rollback.

### Delivery

- Dependency-ordered phases with clear file ownership.
- Narrow validation at each phase and broader contract validation at
  integration points.
- Backward-compatible rollout or an explicitly accepted breaking change.
- A rollback that preserves unrelated user data and work.

When evidence cannot resolve a material design decision, present concrete
options and wait for user adjudication. Record the decision once in its owning
plan section and propagate it to affected phases.

