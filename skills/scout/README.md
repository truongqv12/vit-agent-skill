# scout

Fast, token-efficient codebase scouting. [`SKILL.md`](./SKILL.md) is the
authority for behavior; this README carries provenance and dependency notes.

## Provenance

- Source skill: `ak:scout` v1.0.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `scout`.

## Dependencies

- **standalone.** Core scouting works with native content/name search, scoped
  file reads, and shell.

Optional accelerators (each with a native fallback):

- A delegation capability for parallel scout agents (Claude Code `Explore`, or a
  runtime-discovered parallel-agent role). Absent → main-agent scouting.
- A user-permitted external probe CLI (e.g. OpenCode) for large scopes. Absent →
  native search.
- A live task-management surface for progress tracking. Absent → active plan.
- An output/file organization capability at result collection. Absent → place
  files by the project's existing convention.

External or delegated execution requires explicit user permission. Scouting is
always read-only.

## References

- [`references/internal-scouting.md`](./references/internal-scouting.md) —
  parallel scout agents (delegation-gated).
- [`references/external-scouting.md`](./references/external-scouting.md) —
  user-permitted external probes.
