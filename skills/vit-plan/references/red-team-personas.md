# Red-Team Personas

Use hostile lenses to expose real plan failures. The tone may be skeptical, but
findings must remain precise, evidenced, and useful. No praise or general code
quality review belongs in this workflow.

## Lenses

| Persona | Focus | Full-tier verification role |
|---|---|---|
| Security Adversary | Trust boundaries, authorization, injection, data exposure, supply chain. | Fact Checker |
| Failure Mode Analyst | Race conditions, partial failure, data loss, recovery, deployment and rollback holes. | Flow Tracer |
| Assumption Destroyer | Unproved dependencies, false current-state claims, missing error paths and scale assumptions. | Scope Auditor |
| Scope and Complexity Critic | Unnecessary abstractions, duplicated machinery, scope creep, missing minimal cuts. | Contract Verifier |

The verification tier in [verification-roles.md](verification-roles.md) takes
precedence over the persona mapping. At Light tier, use Fact Checker. At
Standard tier, combine Fact Checker and Contract Verifier. At Full tier, use
the mapped role.

## Reviewer brief

Give every reviewer or sequential lens:

- exact plan and phase paths;
- its persona and active verification role;
- the accepted delivery contract and explicit user decisions;
- instruction to review the plan, not implement, lint, build, or test code;
- instruction to inspect code only to verify factual claims;
- evidence and output rules below.

Use this prompt shape:

```text
Review this implementation plan through the {LENS} lens. Find only flaws that
could break the accepted outcome, safety boundary, compatibility, rollout, or
maintainability. Cite current-code claims as path:line. Cite greenfield or plan
contract flaws as exact file and heading. Do not praise, lint, implement, build,
or test. Return at most ten deduplicatable findings.
```

## Finding format

```markdown
### Finding N: Title
- Severity: Critical | High | Medium
- Location: file > heading
- Flaw: precise problem
- Failure scenario: concrete sequence and impact
- Evidence: path:line, plan heading, or authoritative source
- Suggested correction: smallest cause-aligned change
```

## Severity

- **Critical:** likely prevents the accepted outcome or creates unacceptable
  security/data loss.
- **High:** significant failure, compatibility, or rollback risk.
- **Medium:** notable weakness that should be resolved before implementation.

Reject style preferences, unsupported hypotheticals, duplicate findings, and
issues already disproved by verified evidence.

