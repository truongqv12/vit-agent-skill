---
title: "Phase 3: Validation and Rollback"
status: completed
---

# Phase 3: Validation and Rollback

## Overview

Prove structure, portability, discovery, behavior preservation, and workspace safety.

## Requirements

- Run non-mutating checks first. Use an isolated install target if local install testing is needed; remove only a verified test artifact.
- Confirm pre-existing deletions remain deleted and no file outside the allowlist changed because of implementation.

## Related Code Files

- Modify: none; validation-only phase.

## Implementation Steps

1. Run `bash scripts/validate-skills.sh .`.
2. Run `npx skills add . --list` and confirm `ba-spec`, `figma-to-code`, and `brainstorm` appear.
3. Run `npx skills add . --skill brainstorm -y` only with a verified isolated target/agent location; otherwise record list/discovery evidence and skip the side-effecting install.
4. Run `rg -n '/ak:|(^|[^[:alnum:]_])ak[[:space:]]+' skills/brainstorm/SKILL.md` and expect no matches.
5. Compare source and port for the four contract fields, bug steps, at-most-three options, evidence boundary, and implementation boundary.
6. Run `git status --short -- AGENTS.md CHANGELOG.md`; expect both deletions unchanged. Review `git diff -- README.md skills.sh.json scripts/validate-skills.sh` and direct contents of new/ignored files.
7. Run `git check-ignore -v plans/reports/research-260824-1020-migrate-ak-brainstorm.md` and verify the report text directly because it will not appear in normal Git diffs.

## Todo

- [x] Static validation passes.
- [x] Discovery/install evidence captured.
- [x] Behavior checklist passes.
- [x] Scope and deletions verified.

## Validation evidence

- Bash syntax and generic validator: pass for 3/3 skills.
- JSON grouping: parses and lists `ba-spec`, `brainstorm`, `figma-to-code`.
- Skills CLI discovery: found exactly 3 skills.
- Direct pickup: `npx skills use . --skill brainstorm` returned the portable
  `SKILL.md` without installing it into the repo.
- Portability and source-invariant checks: pass.
- Independent tester: pass; final code review: 10/10, no findings.
- Side-effecting project install was skipped because no isolated agent target
  was needed after discovery/direct-pickup evidence succeeded.

## Success Criteria

- All checks pass; any skipped install check states why and does not masquerade as success.
- No AgentKit CLI is needed at skill runtime.
- The ignored report is locally updated, with its non-shippable status explicit.

## Risk Assessment

`npx skills add` may write outside the repo. Inspect its target first; prefer discovery-only evidence when isolation is unavailable. The ignored report cannot be delivered through a normal commit unless scope later permits an ignore-policy change.

## Rollback

Delete `skills/brainstorm/` and `docs/portable-skill-contract.md`; revert only the four scoped tracked/local edits. Never restore or alter `AGENTS.md` and `CHANGELOG.md`; never delete an unverified install target.
