# Plan Organization

This file owns the `vit-plan/v1` artifact schema and project-local file rules.
The physical files under `../templates/` own canonical document bodies.

## Location and naming

- Store plans beneath the current repository's `plans/` directory.
- Name a new plan directory `<YYMMDD-HHMM>-<descriptive-kebab-slug>`. This is
  the canonical project-local v1 convention enforced by the helper and linter.
- Name phases `phase-NN-<descriptive-kebab-slug>.md`, starting at `01` and
  increasing without gaps.
- Keep stored paths and links repository-relative. Return an absolute plan path
  only in the conversational handoff when useful.
- Use UTF-8 text and preserve the repository's newline convention.
- Refuse collisions. Never overwrite or silently merge an existing plan,
  phase, or directory.

## Plan schema

`plan.md` frontmatter accepts exactly these fields:

| Field | Rule |
|---|---|
| `schemaVersion` | Required literal `"vit-plan/v1"`. |
| `title` | Required quoted, non-empty string. |
| `description` | Required quoted, non-empty one-line string. |
| `status` | Required: `pending`, `in-progress`, `completed`, or `blocked`. |
| `priority` | Required project priority such as `P1`, `P2`, or `P3`. |
| `effort` | Required quoted estimate or empty string when unknown. |
| `tags` | Required inline list of plain tags; may be empty. |
| `blockedBy` | Required inline list of repo-relative plan-directory paths. |
| `blocks` | Required inline list of repo-relative plan-directory paths. |
| `created` | Required quoted `YYYY-MM-DD` date. |

Unknown fields are invalid in v1. `blockedBy` lists plans whose outputs this
plan requires. `blocks` is the inverse relationship. When a relationship is
confirmed, update both plans. A missing referenced plan is a lint error because
v1 has one project-local scope.

## Phase schema

Each phase frontmatter accepts exactly these fields:

| Field | Rule |
|---|---|
| `schemaVersion` | Required literal `"vit-plan/v1"`. |
| `id` | Required quoted `"phase-NN"`, matching its filename number. |
| `title` | Required quoted, non-empty string. |
| `status` | Required: `pending`, `in-progress`, `completed`, or `blocked`. |
| `dependencies` | Required inline list of quoted phase IDs; may be empty. |

Unknown fields are invalid in v1. `dependencies` means phases required by the
current phase. Every referenced phase must exist, must precede or otherwise
legitimately gate the current phase, and the dependency graph must be acyclic.

## Required content

The plan must contain Delivery Contract with outcome, constraints, non-goals,
and acceptance criteria; Phases; Dependencies; Risks and Mitigations; Success
Criteria; and Open Questions. Each phase must contain Context, Related Files,
Implementation Steps, Todo, Validation, Risks and Mitigations, and Rollback.

Use human-readable phase link text. The plan's phases table must link every
phase exactly once, and every linked file must exist.

## Creation

Prefer the optional helper when Python is available. Discover its exact
arguments with `../scripts/plan-tool.py --help`; the helper may only scaffold,
add a phase, or lint the controlled filesystem artifacts. Read generated files
before replacing instructional body text.

## Native fallback

When the helper cannot run:

1. Read `../templates/plan.md` and `../templates/phase.md`.
2. Choose a collision-free plan directory and phase filename.
3. Replace plan tokens `{{TITLE}}`, `{{DESCRIPTION}}`, `{{SLUG}}`, `{{DATE}}`,
   `{{FIRST_PHASE_TITLE}}`, and `{{FIRST_PHASE_FILE}}`.
4. Replace phase tokens `{{PHASE_ID}}`, `{{PHASE_TITLE}}`, and
   `{{DEPENDENCIES}}`. Render dependencies as `[]` or a YAML inline list of
   quoted phase IDs.
5. Create the directory and files without overwrite behavior.
6. Confirm frontmatter uses only the controlled fields and allowed statuses.
7. Confirm numbering, phase links, dependency references, and the absence of
   cycles.
8. Confirm every required section exists, no template token remains, and all
   stored paths are repository-relative.
9. Read every created file back. Report any failure instead of claiming a
   partial plan succeeded.
