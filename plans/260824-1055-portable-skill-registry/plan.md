---
title: "Portable Skill Registry"
description: "Publish a portable brainstorm skill and reusable import contract without an AgentKit CLI runtime dependency."
status: completed
priority: P2
effort: "3h"
branch: main
tags: [feature, docs]
blockedBy: []
blocks: []
created: 2026-08-24
---

# Portable Skill Registry

## Overview

Convert local source `ak:brainstorm` v2.3.0 into repo skill `brainstorm`. Preserve its decision contract and bug routing while replacing named AgentKit handoffs with capability discovery plus native fallbacks. Document and validate the same portability rules for future imports.

## Delivery Contract

- **Outcome:** `brainstorm` is discoverable/installable from this repo, works without `ak` CLI or `/ak:*` skills, and establishes a reusable portable-skill contract.
- **Constraints:** YAGNI/KISS/DRY; retain MIT, `agentkit`, upstream name/version provenance; capability-based handoffs; modify only the implementation allowlist below; leave the existing deletions of `AGENTS.md` and `CHANGELOG.md` intact.
- **Non-goals:** migrate other AgentKit skills; recreate deleted files; change `.gitignore`; add a test framework, new scripts, templates, or references under `skills/brainstorm/`; determine an unverified upstream URL/commit.
- **Acceptance:** generic name/path align; four brainstorm fields and bug-routing semantics remain; no required `ak` CLI or `/ak:*` invocation; repo catalog/docs expose the skill; generic validator and discovery checks pass; ignored research report records the superseded naming decision.

## Phases

| # | Phase | Status |
|---|-------|--------|
| 1 | [Portable brainstorm contract](./phase-01-portable-brainstorm-contract.md) | Completed |
| 2 | [Repository integration](./phase-02-repository-integration.md) | Completed |
| 3 | [Validation and rollback](./phase-03-validation-and-rollback.md) | Completed |

## Implementation Allowlist

Create `skills/brainstorm/SKILL.md`, `skills/brainstorm/README.md`, and `docs/portable-skill-contract.md`. Modify `README.md`, `skills.sh.json`, `scripts/validate-skills.sh`, and ignored local report `plans/reports/research-260824-1020-migrate-ak-brainstorm.md`. No other implementation files.

## Dependencies

- Source baseline: `C:/Users/tttruong/.agents/skills/ak-brainstorm/SKILL.md` (read-only).
- No cross-plan dependencies. No runtime dependency on AgentKit CLI.

## Success Criteria

- [x] All phase criteria and validation commands pass.
- [x] `git status --short -- AGENTS.md CHANGELOG.md` still reports both user-owned deletions.
- [x] No unresolved blocking questions.

<!-- slug: portable-skill-registry -->
