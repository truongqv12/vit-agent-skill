# Verification Roles

Verify plan accuracy against the repository before asking the user to decide.
Verification reports evidence; it does not silently edit plans.

## Tiers

| Phases | Tier | Active roles | Claim budget |
|---|---|---|---|
| 1-2 | Light | Fact Checker | Up to 5 material claims per phase |
| 3-4 | Standard | Fact Checker, Contract Verifier | Up to 10 per phase |
| 5+ | Full | All four roles | At least 15 per phase when available |

Prioritize claims that affect architecture, compatibility, safety, dependency
order, or acceptance. Do not pad a budget with trivial facts.

## Fact Checker

Verify cited files, symbols, routes, fields, configuration keys, and tests.
Use native repository search and direct file reads. Record:

- `VERIFIED (path:line)`;
- `FAILED (not found; nearest evidence...)`;
- `UNVERIFIED (ambiguous or inaccessible)`.

## Flow Tracer

Verify behavioral claims by following the actual entry point through guards,
branches, calls, events, async boundaries, and early returns. Distinguish
causality from co-location. Output the traced `path:line` chain or the actual
flow that disproves the plan.

## Scope Auditor

Verify proposed state and ownership against all construction and lifetime
sites. Classify request, session, process, persistent, or shared lifetime. Look
for existing equivalent state, isolation leaks, and ownership overlap.

## Contract Verifier

Enumerate consumers of changed interfaces, schemas, exports, routes, commands,
or configuration. Include tests, re-exports, documentation, build automation,
and deployment configuration. List every consumer when practical; for a large
set, report the total, the highest-risk subset, and the discovery method.

## Evidence boundaries

- Existing-code claims require repository-relative `path:line` evidence.
- Greenfield contracts and missing plan elements cite exact plan file and
  heading; nonexistent code cannot provide code evidence.
- External claims cite authoritative current documentation.
- Mark unresolved ambiguity; never invent confirmation.

## Verification report

Append results to the active validation or red-team session:

```markdown
### Verification Results
- Tier: Light | Standard | Full
- Claims checked: N
- Verified: N | Failed: N | Unverified: N

#### Material Failures
1. [Role] Claim — evidence and actual state
```

Failed material claims require user adjudication before correction.

## Whole-plan consistency sweep

Run after any approved validation or red-team edit.

1. Re-read `plan.md` and every `phase-*.md` file after edits.
2. Build a decision-delta list: changed names, fields, APIs, paths, scopes,
   assumptions, dependencies, ownership, risks, and acceptance criteria.
3. Search all plan files for the old terms, superseded assumptions, and
   duplicate embedded contracts or pseudocode.
4. Reconcile the overview, delivery contract, phase table, dependencies,
   context, related files, steps, todo, validation, risks, rollback, and review
   logs.
5. Re-run structural lint or the native checklist.
6. Record the result:

```markdown
### Whole-Plan Consistency Sweep
- Files reread: ...
- Decision deltas checked: N
- Stale references reconciled: N
- Unresolved contradictions: N
```

When unresolved contradictions are greater than zero, list each affected file
and heading, ask the user when a decision is required, and do not present the
plan as ready for implementation.

