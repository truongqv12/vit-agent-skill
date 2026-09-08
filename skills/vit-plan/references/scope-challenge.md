# Scope Challenge

Run this before expensive research or design. Its purpose is to catch rebuilds,
scope creep, and accidental complexity once, then honor the resulting choice.

## Skip conditions

Skip when the user explicitly selects `--fast`, the task is a trivial
single-file correction, or an accepted plan already records the scope decision.
Urgency alone does not justify skipping evidence needed for safety.

## Inspect first

Answer these from repository evidence:

1. **What already exists?** Find utilities, services, contracts, tests, and
   unfinished plans that already solve part of the problem.
2. **What is the minimum change set?** Separate delivery-blocking work from
   useful but deferrable improvements.
3. **Is the proposed complexity justified?** Challenge plans that touch more
   than eight files, introduce more than two new abstractions, or require more
   than three phases. These are prompts for evidence, not automatic rejection.

Summarize:

```text
Existing reuse: ...
Minimum changes: ...
Complexity drivers: ...
Evidence gaps: ...
```

## Resolve material scope choices

When inspection exposes a real choice, offer:

- **Expand:** explore adjacent value and alternatives; keep stretch work
  explicitly separate from required acceptance.
- **Hold:** preserve the requested scope and strengthen edge cases, tests, and
  failure handling.
- **Reduce:** deliver only essentials and list deferred work under non-goals.

Use a structured question capability when available. Otherwise ask the same
choice in plain conversation. Recommend the smallest option that meets the
accepted outcome, but do not choose for the user when business value changes.

## After selection

- Expansion usually suggests `hard` or `two` mode.
- Hold keeps normal mode detection.
- Reduction usually suggests `fast` mode.
- Record the chosen scope in the delivery contract.
- Do not silently expand, reduce, or repeatedly relitigate it later.

Audits may identify a new constraint, but reversing an explicit scope choice
requires presenting the new evidence, trade-off, and concrete options to the
user.

