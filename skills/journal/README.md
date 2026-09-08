# journal

Write a concise chronological technical journal of a work session.
[`SKILL.md`](./SKILL.md) is the authority for behavior; this README carries
provenance and dependency notes.

## Provenance

- Source skill: `ak:journal` v1.0.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `journal`.

## Dependencies

- **standalone.** Core journaling works with native scoped file reads, content
  search, and shell (`git log`, `git diff`, `git status`).

Optional accelerators (each with a native fallback):

- A change-history or memory-exploration capability (e.g. a journaling
  subagent) to gather session material. Absent → gather natively with git and
  file reads.
- An output/file organization capability at write time. Absent → follow the
  project's existing convention.
- A publishing or sharing capability (wiki / knowledge base) for the finished
  entry. Absent → publishing is skipped and reported.

Any external, delegated, or publishing action requires explicit user
permission. Invocation is explicit-intent because the skill writes a file.

## Output

- Entries are written to this repository's `plans/journals/` directory,
  following the existing `plans/journals/*.md` naming convention.
- Journals are work history only — not current product or decision authority.
  Durable decisions belong in the project's ADR or current documentation owner.
