# research

Deep, evidence-first technical research that returns a concise cited report.
[`SKILL.md`](./SKILL.md) is the authority for behavior; this README carries
provenance and dependency notes.

## Provenance

- Source skill: `ak:research` v1.0.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `research`.

## Dependencies

- **standalone.** The core research loop works offline with native content/name
  search, scoped file reads, and shell against local evidence, and still
  produces a cited report.

Optional accelerators (each with a native fallback):

- A web search capability for current external sources. Absent → local evidence
  only, with gaps marked.
- A documentation-lookup capability for library/API/GitHub docs. Absent → native
  fetch/search, or local evidence.
- An output/file organization capability at report save time. Absent → place the
  report by the project's existing convention.

External web access requires explicit user permission. Research is read-only
except for writing its own report.
