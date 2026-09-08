---
title: "Phase 1: Portable brainstorm contract"
status: completed
---

# Phase 1: Portable brainstorm contract

## Overview

Create the portable skill and the evergreen import rules it exemplifies.

## Requirements

- Functional: preserve Outcome, Constraints, Non-goals, Acceptance criteria; proportional behavior; evidence-first bug routing; option exploration; boundaries.
- Portability: `name: brainstorm`; no mandatory `ak` executable, `/ak:*` command, or absent companion skill. Handoffs discover an installed planning/implementation/debugging capability and otherwise use an equivalent native workflow.
- Provenance: retain MIT, author `agentkit`, upstream name `ak:brainstorm`, and baseline version `2.3.0`; do not invent an upstream URL or commit.

## Architecture

`SKILL.md` remains a self-contained router. Its README records source/adaptations. `docs/portable-skill-contract.md` defines reusable name, dependency, handoff, provenance, and validation conventions for later imports.

## Related Code Files

- Create: `skills/brainstorm/SKILL.md`
- Create: `skills/brainstorm/README.md`
- Create: `docs/portable-skill-contract.md`

## Implementation Steps

1. Copy only the source behavior needed by the skill; change identity to `brainstorm`.
2. Rewrite Mermaid labels, handoff, and workflow-position text so named AgentKit commands are neither required nor promised.
3. Document upstream baseline and a concise local-adaptation list in the skill README.
4. Define a reusable contract: folder/frontmatter identity, capability discovery with native fallback, no machine paths/runtime CLI coupling, provenance, and review checklist.

## Todo

- [x] Portable skill created.
- [x] Provenance and import contract documented.

## Success Criteria

- `skills/brainstorm/SKILL.md` is independently executable and keeps the source decision semantics.
- `rg -n '/ak:|(^|[^[:alnum:]_])ak[[:space:]]+' skills/brainstorm/SKILL.md` returns no runtime command dependency.

## Risk Assessment

Over-editing may cause semantic drift. Mitigate with a source-to-port checklist for the four fields, bug sequence, option limit, and boundaries.

## Rollback

Remove only the three files created in this phase.
