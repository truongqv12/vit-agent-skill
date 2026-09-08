# Documentation Impact Routing

Use this file when another workflow must decide whether docs are affected. For
full operations, run this skill's `init`, `update`, or `summarize` route.

## Update docs when a change affects

- user-visible behavior, setup, commands, or configuration;
- architecture, data flow, public contracts, security, or recovery;
- machine-readable contracts or generated reference output;
- an accepted maintainer decision that future work must not rediscover.

Do not add documentation churn for internal edits whose observable contract did
not change. Docs own WHY and WHERE; current WHAT and HOW must point to an
executable owner. If a review exposes an unwritten rejection criterion, record
it once in the repository's canonical review or standards surface.

## Discover the target

Read repository instructions, the root README, and the project's existing docs
navigation. Search current docs for the changed concept. Do not route by a
universal filename list.

Update the smallest authority surface. If a command, inventory, matrix, or
generated output already has a machine owner, update that owner and have prose
link to it rather than copying the details.

## Evidence and state

- Evergreen docs describe durable intent and operating contracts.
- Source, tests, manifests, generated output, artifacts, and live services prove
  current behavior.
- Plans, reports, audits, and release records are stateful evidence, not product
  authority.

Before updating a document, read it. After updating, verify links and claims
against the owning evidence. Remove stale or duplicate text rather than adding
another reconciliation layer.

## Cross-workflow handoffs

Resolve each handoff by capability: use the named capability when the runtime
exposes it and the user's request permits it; otherwise perform it inline with
native tools (read, search, shell), or stop and report the missing capability
honestly. Never emit a hard command or a named source-subagent call as the only
path.

- An implementation or fix workflow updates docs during finalize only when the
  impact criteria above apply.
- A planning capability reads routed project context before creating an
  execution plan.
- A preview or visualization capability keeps temporary visuals with the active
  plan; link them from evergreen docs only when they remain useful.
- A diagramming capability produces publish-grade diagrams when a visual
  materially improves the document.
- Any workflow editing `docs/` applies `references/doc-content-rules.md`.
