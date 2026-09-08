---
name: docs
description: "Analyze a codebase and create, refresh, summarize, or audit project documentation without imposing a fixed docs layout. Invoke to create, refresh, summarize, or audit project documentation."
user-invocable: true
when_to_use: "Invoke to create, refresh, summarize, or audit project documentation."
category: utilities
keywords: [documentation, init, update, summarize, audit]
argument-hint: "init|update|summarize"
license: MIT
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:docs"
  source-version: "1.3.0"
  portability: standalone
---

# Documentation Management

Maintain the smallest documentation set that lets people and AI collaborators
understand the project's intent, current contract, evidence, and operating
workflow.

## Philosophy

Code owns WHAT and HOW; docs own WHY and WHERE. Docs are a thin navigation
layer plus knowledge code cannot express: decisions, rejected alternatives,
business rules, domain terminology, and constraints. Point to executable owners
instead of paraphrasing behavior. Load `references/doc-content-rules.md` for any
doc-writing operation and include its relevant rules in any delegated context.

## Capability handoff convention

When a step below names a companion capability (documentation authoring,
scouting, diagramming, planning, or a downstream implementation/fix workflow):

- Use the `<capability>` capability when the runtime exposes it and the user's
  request permits it; otherwise perform `<capability>` inline with native tools
  (read, search, shell). If neither path is possible, stop and report the
  missing capability honestly. Never emit a hard command or a named
  source-subagent call as the only path.

External or delegated execution requires explicit user permission. Companion
skills are named only as examples of a capability, never as required
invocations.

## Opening Gate

Docs mutation is explicit-intent. Start with a bounded brainstorm. Establish:

- who consumes the docs: people, AI, or both;
- the outcome and decisions the docs must make possible;
- which sources prove current behavior;
- what is evergreen guidance versus stateful evidence;
- the acceptance criteria for this docs operation.

Reuse an accepted plan or prior brainstorm when it already answers these
questions. Do not reopen settled intent without new evidence.

## Routing

Parse the first word of the arguments:

| Input | Load | Purpose |
|---|---|---|
| `init` | `references/init-workflow.md` | Establish a minimal project-specific docs route |
| `update` | `references/update-workflow.md` | Reconcile impacted docs with current evidence |
| `summarize` | `references/summarize-workflow.md` | Summarize current evidence without forcing a new file |
| empty or unclear | ask the user | Choose the operation; never assume `init` |

Other workflows deciding whether docs are affected should load
`references/documentation-management.md`.

## Discovery Contract

Do not assume filenames, a file count, or a universal documentation tree.
Discover the project's contract in this order:

1. repository instructions such as `AGENTS.md` or `CLAUDE.md`;
2. the root `README.md`;
3. the project's docs index or navigation file, when present;
4. existing files under `docs/` and links from the earlier routes;
5. source, tests, scripts, generated artifacts, and live state that prove claims.

Use `docs/` for project documentation when that is the repository convention.
Treat source and tests as evidence, not prose that must be copied into every
document.

## Maintenance Rules

- Update only documents whose contract or evidence changed. Scope every edit to
  the changed authority surface; never trigger a blanket whole-corpus refresh.
- Update the smallest owning surface.
- Delete stale or duplicate guidance instead of preserving it for history.
- Link to the owning script, manifest, schema, or generated source instead of
  copying command lists, inventories, or exact test names into multiple files.
- Keep evergreen guidance free of dates, issue IDs, phase labels, and section
  coordinates unless those values are the subject of the contract.
- Keep stateful research, plans, audit results, and release evidence clearly
  labeled and outside the evergreen authority path.
- Do not create an ADR, governance layer, generator, or docs-only CI gate unless
  the user explicitly requests that additional operating surface.
- Verify every path, command, configuration key, and behavioral claim against
  current evidence.

For diagrams, use a diagramming capability only when a visual materially
improves understanding, then visually review the output; if no such capability
is available, describe the structure in prose instead.

**Do not implement product code during a documentation operation.**

## References

- `references/doc-content-rules.md` — ownership, drift-resistance, and authority
  rules for any doc-writing operation.
- `references/init-workflow.md` — establish a minimal project-specific route.
- `references/update-workflow.md` — reconcile impacted docs with evidence.
- `references/summarize-workflow.md` — evidence-backed summary without a new file.
- `references/documentation-management.md` — impact routing for other workflows.
