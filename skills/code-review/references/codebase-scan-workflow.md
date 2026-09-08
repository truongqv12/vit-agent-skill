# Codebase Scan Workflow

Scan and analyze the codebase for the given review scope, following the project's
development rules and existing documentation navigation. Sacrifice grammar for
concision. List unresolved questions at the end.

Each companion capability below (research, scouting, code-review delegation,
planning) is used when the runtime exposes it and the user permits it; otherwise
perform that step inline with native tools (read, search, shell). Never make a
named subagent the only path.

## Role Responsibilities

- Act as an elite software engineering reviewer focused on system architecture
  and technical decision-making.
- Operate by: **YAGNI**, **KISS**, and **DRY**.

## Workflow

### Research
* Use a research capability (e.g. parallel researcher agents, up to ~5 sources)
  when available; otherwise gather sources inline.
* Keep every research note concise (≤150 lines).
* Use a scouting capability to locate relevant files; otherwise search natively.

### Code Review
* Use a code-review delegation capability to review code in parallel scopes when
  available; otherwise review inline.
* If issues are found, improve and repeat until tests pass.
* When complete, run verification for accepted findings before reporting
  completion (see `verification-before-completion.md`).
* Report combined quality findings and verification evidence to the user, with
  `file:line` evidence, severity (critical / warning / suggestion), and a score
  out of 10.

### Plan
* Use a planning capability to analyze findings and create an improvement plan
  when available; otherwise draft the plan inline.
* Save the overview at `plan.md` and phase files as `phase-XX-phase-name.md`,
  following the project's plan location and naming convention.

### Final Report
* Summarize changes, guide the user on how to get started, and suggest next
  steps.
* Ask the user whether they want to commit and push.
