# docs

Analyze a codebase and create, refresh, summarize, or audit project
documentation without imposing a fixed docs layout. [`SKILL.md`](./SKILL.md) is
the authority for behavior; this README carries provenance and dependency notes.

## Provenance

- Source skill: `ak:docs` v1.3.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `docs`.
- Ported version: `1.0.0`.

## Dependencies

- **standalone.** Core documentation work uses native repository search, scoped
  file reads, and shell.

Optional accelerators (each with a native fallback):

- A documentation-authoring delegation capability for evidence-first authoring
  (`init`/`update`). Absent → author inline with native tools.
- A scouting capability for locating source and evidence (`init`/`summarize`).
  Absent → focused native search.
- A diagramming or visualization capability for publish-grade visuals. Absent →
  describe structure in prose.
- A planning capability that reads routed project context before delivery.
  Absent → the active plan or brainstorm is the durable source of truth.

External or delegated execution requires explicit user permission. Docs mutation
is explicit-intent; no whole-corpus refresh runs without a scoped reason.

## References

- [`references/doc-content-rules.md`](./references/doc-content-rules.md) —
  ownership, drift-resistance, and authority rules for any doc-writing operation.
- [`references/init-workflow.md`](./references/init-workflow.md) — establish a
  minimal project-specific docs route.
- [`references/update-workflow.md`](./references/update-workflow.md) — reconcile
  impacted docs with current evidence.
- [`references/summarize-workflow.md`](./references/summarize-workflow.md) —
  evidence-backed summary without forcing a new file.
- [`references/documentation-management.md`](./references/documentation-management.md)
  — impact routing for other workflows.

## Not ported

- The source `references/llms.md` (an `llms.txt` generator sub-command) is not
  wired into the source `SKILL.md` routing table and is outside the skill's
  documented `init|update|summarize` surface, so it is excluded per the
  contract's "references only when actually used" rule.
