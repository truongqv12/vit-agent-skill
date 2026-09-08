# cook

Smart, gated feature implementation. [`SKILL.md`](./SKILL.md) is the authority
for behavior, modes, flags, gates, and workflow. This README carries provenance
and dependency notes only.

## Provenance

- Source skill: `ak:cook` v2.2.0 (author: agentkit, MIT).
- Normalized per `docs/portable-skill-contract.md`. Folder and frontmatter
  `name` are both `cook`.
- Coupling removed: source slash-commands, named source subagents,
  `delegate_agent` / `ask_user` capability names, `the engineer/installed <x>
  skill` handoffs, and the hidden simplify state (`.ck.json` config keys and the
  `CK_*` environment toggle). The simplify gate is preserved as a git-diff-driven
  step with documented default thresholds and an optional project override.

## Dependencies

- **standalone.** Cook completes with native tools (read, search, shell, edit)
  and the durable plan files. It degrades gracefully when a companion is absent
  and improves automatically as companions are available.

Companion capabilities (each optional, each with a native fallback), by portable
skill name in this kit:

- `scout` — codebase discovery (native search fallback).
- `research` — evidence gathering (skipped in fast/code; local-evidence fallback).
- `vit-plan` — planning and plan execution (native plan-file authoring fallback).
- `code-review` — MANDATORY review gate (native inline (a-e) review fallback).
- `test` — MANDATORY test gate (native test-command fallback).
- `debug` — root-cause analysis on test failure (native log/trace reading fallback).
- `git` — commit at finalize, explicit-intent (native git via shell).
- `project-management` — MANDATORY whole-plan sync-back (native checkbox edits).
- `docs` — conditional docs update (native scoped edits).
- `journal` — completion journal (native entry to `plans/journals/`).
- `fix` — cook routes concrete bugs here.
- Optional UI/design, simplification, and preview capabilities.

All external effects at finalize (git commit, docs mutation, journal) require
explicit user intent.

## References

- [`references/intent-detection.md`](./references/intent-detection.md)
- [`references/workflow-routing.md`](./references/workflow-routing.md)
- [`references/workflow-steps.md`](./references/workflow-steps.md)
- [`references/review-cycle.md`](./references/review-cycle.md)
- [`references/subagent-patterns.md`](./references/subagent-patterns.md)
