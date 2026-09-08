# Validation Question Framework

Ask only questions whose answers could materially change the implementation
plan. Do not use an interview to make the user reconfirm facts already proved
by source or tests.

## Topic categories

| Category | Look for |
|---|---|
| Architecture | Competing designs, boundaries, data models, API shapes. |
| Assumptions | `assume`, `expect`, defaults, missing evidence. |
| Trade-offs | Compatibility, cost, complexity, performance, maintainability. |
| Risks | Security, data loss, partial failure, dependency, rollback. |
| Scope | MVP boundary, deferrals, ownership, acceptance. |

Verification failures and `[UNVERIFIED]` tags take priority over speculative
questions.

## Question rules

- State the exact plan claim or missing decision.
- Explain why the answer changes implementation.
- Offer two to four mutually exclusive concrete options.
- Put the recommended option first and suffix its label with `(Recommended)`.
- Allow free-form input when the provided choices do not fit.
- Avoid compound questions; split independent decisions.
- Group only closely related questions.

When structured questions are unavailable, use the same wording and choices in
plain conversation.

## Recording format

```markdown
### Session N — YYYY-MM-DD
**Trigger:** Why validation ran

#### Verification Results
- Tier: Light | Standard | Full
- Claims checked: N
- Verified: N | Failed: N | Unverified: N

#### Questions and Answers
1. **[Category] Full question text**
   - Options: A | B | C
   - Answer: User choice
   - Custom input: Verbatim text, when provided
   - Rationale: Why the decision matters

#### Confirmed Decisions
- Decision: choice — rationale

#### Impact on Phases
- phase-NN: required update

#### Action Items
- [ ] Specific approved change
```

Increment the session number from the latest existing session. Preserve exact
custom input. Put unresolved questions at the end of the log and the plan.

## Propagation map

| Decision type | Likely owners |
|---|---|
| Outcome or scope | Delivery Contract, phase Context and Steps |
| Architecture or contract | Dependencies, Related Files, Steps, Validation |
| Risk or failure behavior | Risks and Mitigations, Rollback, Validation |
| Acceptance | Delivery Contract, phase Todo and Validation |

The map is a prompt, not a substitute for rereading the complete plan.

