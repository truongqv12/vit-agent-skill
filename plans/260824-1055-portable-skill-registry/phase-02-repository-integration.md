---
title: "Phase 2: Repository Integration"
status: completed
---

# Phase 2: Repository Integration

## Overview

Register and explain `brainstorm`; make portable import invariants generic validator behavior.

## Requirements

- Root docs show all current skills and portable install/use examples without listing deleted `AGENTS.md`.
- Registry groups `brainstorm` under a general workflow category.
- Validator applies reusable checks to every skill: required `README.md`, portable kebab-case identity matching its directory, and absence of hard-coded `/ak:*` or `ak <command>` runtime instructions in `SKILL.md`.
- Research report explicitly supersedes its former `ak:brainstorm` recommendation with the accepted `brainstorm` decision; it remains ignored because `.gitignore` is out of scope.

## Related Code Files

- Modify: `README.md`
- Modify: `skills.sh.json`
- Modify: `scripts/validate-skills.sh`
- Modify: `plans/reports/research-260824-1020-migrate-ak-brainstorm.md` (ignored local artifact)

## Implementation Steps

1. Add the skill summary and `npx skills` list/install/invocation examples; reconcile the displayed repository tree with current files.
2. Add `brainstorm` to an `Agent Workflows` grouping without disturbing existing grouping behavior.
3. Extract frontmatter name in Bash, normalize optional quotes, compare to directory basename, enforce portable syntax, require README, and reject runtime command coupling with actionable errors. Keep the existing `ba-spec` checks.
4. Add a dated supersession note to the research report; update outcome, options, file paths, checks, and open questions consistently.

## Todo

- [x] Docs and registry updated.
- [x] Validator rules are generic, not a `brainstorm` special case.
- [x] Ignored report no longer recommends the old namespace.

## Success Criteria

- JSON parses; existing `ba-spec` and `figma-to-code` remain valid.
- Validator fails clearly for a mismatched/non-portable name or hard-coded AgentKit runtime command, without new dependencies.

## Risk Assessment

Naive grep can flag provenance prose. Match only slash commands and CLI-shaped `ak <subcommand>` text; keep `ak:brainstorm` provenance allowed.

## Rollback

Revert only these four scoped edits. Do not restore `AGENTS.md` or `CHANGELOG.md`.
