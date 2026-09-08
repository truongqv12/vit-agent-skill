# vit-plan

`vit-plan` creates evidence-backed, phased implementation plans as portable
Markdown. It also supports decision validation and adversarial review. It never
implements the plan itself.

## Runtime contract

Required capabilities:

- read and write files inside the current project;
- inspect repository instructions, documentation, source, and tests;
- ask the user a concise question when a material decision remains.

Optional capabilities have complete fallbacks:

- **Python 3:** `scripts/plan-tool.py` provides deterministic `create`,
  `add-phase`, and `lint` operations using the standard library. Without it,
  copy `templates/plan.md` and `templates/phase.md`, replace their documented
  tokens, and apply the native checklist in `references/plan-organization.md`.
- **Delegation:** independent research or review lenses may run concurrently.
  Without delegation, run them sequentially with the same ownership and
  evidence requirements.
- **Structured questions:** use them when present. Otherwise ask the same
  material questions in plain conversation.
- **Runtime task tracking:** it may mirror plans with at least three meaningful
  phases. Without it, update Markdown statuses and checkboxes directly.
- **Web or current-documentation search:** use when current external facts are
  required. If unavailable, rely on local evidence and label the gap.

The skill has no required companion skill or service.

## Use

Read `SKILL.md`, then provide either:

- a task to plan, optionally with `--fast`, `--hard`, `--deep`, `--parallel`,
  `--two`, `--tdd`, or `--no-tasks`;
- `validate <plan-path>` for a material-decisions interview;
- `red-team <plan-path>` for adversarial review.

Run `python scripts/plan-tool.py --help` to discover the helper's installed
interface. Helper output never replaces the Markdown artifacts.

## Package map

- `SKILL.md` is the runtime router.
- `references/` owns modes, evidence, schema, design, validation, red-team, and
  optional task-projection rules.
- `templates/plan.md` and `templates/phase.md` are the canonical artifact
  bodies.
- `scripts/plan-tool.py` is an optional filesystem helper; its tests are the
  executable authority for helper behavior.

## Provenance

- License: MIT
- Author: `agentkit`
- Local version: `1.0.0`
- Source skill: `ak:plan` version `1.1.0`
- Source kit: `agentkit-engineer/2.4.0`
- Portability: standalone

The source repository URL and commit were not evidenced, so they are not
claimed here.

## Deliberate v1 changes

This port preserves the source's accepted-intent gate, unfinished-plan scan,
scope challenge, proportional modes, evidence-first design, durable plan
authority, validation interview, adversarial review, and whole-plan reread.

It deliberately removes the AgentKit command/runtime dependency, private
state store, dashboard, hooks, archive behavior, the redundant `--auto` flag,
global plan scope, HTML output, GitHub issue mutation, Wiki publishing, and
automatic image generation. Those features are not hidden dependencies or
silent side effects in v1.

