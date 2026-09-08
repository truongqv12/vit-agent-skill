# Workflow Routing

Use this file when choosing the sequence for multi-step work. It is a routing
map only; load the owning `SKILL.md` before executing details. Names below are
portable skill names in this kit; resolve each as a capability (with native
fallback) per the Capability Handoff Convention.

## Core Sequences

| User intent | Sequence |
|---|---|
| Implement a feature | `brainstorm` → `vit-plan` → `cook` → `test` → `code-review` |
| Execute an accepted plan | reuse its brainstorm contract → `cook <plan-path>` |
| Quick implementation | bounded brainstorm gate → `cook --fast` |
| Bug, error, failed test, or CI failure | opening intent frame → `fix` |
| Investigate before deciding | `scout` → `debug` → `brainstorm` → `vit-plan` |
| Update project docs | `docs` |

## Implementation Owner

- Start delivery with outcome, constraints, non-goals, and acceptance criteria.
  Reuse them from an accepted plan instead of asking again.
- Use `cook` for known feature scope after requirements are clear.
- Use `fix` for concrete bugs, errors, test failures, and CI failures.
- Use `vit-plan` when work needs architecture, phases, file ownership, or TDD
  structure.
- Use `test` for verification-only work.
- Read-only scout, debug, review, and explanation work may stop without an
  interactive design loop. Satisfy the brainstorm gate if it crosses into
  delivery or workspace mutation.

## Handoff Rules

- Establish the brainstorm contract, then use the domain capability for evidence
  and design, followed by the workflow owner. Example: for a React feature,
  route to a frontend-development capability, then execute through `vit-plan`
  and `cook`.
- For documentation changes, invoke the `docs` capability and follow its
  documentation-management routing.
- If a skill-discovery capability is available and the choice is ambiguous, use
  it for domain routing. Otherwise use the installed skill names and
  descriptions.

## Post-Implementation

- Review high-risk, cross-module, or public-contract changes before shipping.
- Update docs only when behavior, setup, commands, architecture, security
  posture, public contracts, or future maintainer decisions changed.
- Journal when a workflow creates durable decisions or debugging lessons.
