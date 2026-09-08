# project-management

Project progress tracking, plan status sync-back, and cross-session continuity
over durable `vit-plan/v1` plan files. [`SKILL.md`](./SKILL.md) is the authority
for behavior; this README carries provenance and dependency notes.

## Provenance

- Source skill: `ak:project-management` v1.0.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `project-management`.

## Dependencies

- **standalone.** Sync-back, progress tracking, and reporting all work with
  native file reads, content search, and direct edits to the plan and phase
  Markdown files. There is no external plan store — the files are the store.

Optional accelerators (each with a native fallback):

- A live task-management surface for mirroring work in-session. Absent → update
  the active plan directly.
- A documentation capability for coordinated `docs/` updates. Absent → edit the
  smallest owning doc inline.
- A plan-linter helper to verify consistency after sync-back (in this repo,
  `python skills/vit-plan/scripts/plan-tool.py lint <plan-dir>`). Absent →
  re-read the edited files and confirm the table and frontmatter agree.
- A review or test capability when verifying task completeness. Absent → inspect
  acceptance criteria and evidence directly.

Plan files remain the durable source of truth; runtime task state is never
completion evidence on its own.

## Portability notes

Dropped during normalization (source coupling with no portable meaning here):

- The AgentKit CLI plan store and its plan-status subcommands — replaced by
  direct edits to `plan.md` and `phase-XX-*.md`, with the optional vit-plan
  linter for verification.
- The AgentKit plans dashboard — replaced by an optional plan-dashboard
  capability handoff.
- Named source subagents (documentation, review, test) — replaced by capability
  handoffs with native fallbacks.

The source plan frontmatter was reconciled to the repo's `vit-plan/v1` schema;
the templates under `skills/vit-plan/templates/` are the field authority.

## References

- [`references/task-operations.md`](./references/task-operations.md) — optional
  runtime work tracking.
- [`references/hydration-workflow.md`](./references/hydration-workflow.md) —
  hydrate / work / sync-back / resume bridge.
- [`references/progress-tracking.md`](./references/progress-tracking.md) — plan
  scanning, status derivation, and verification.
- [`references/reporting-patterns.md`](./references/reporting-patterns.md) —
  report templates and naming.
- [`references/documentation-triggers.md`](./references/documentation-triggers.md)
  — when and how to coordinate doc updates.
