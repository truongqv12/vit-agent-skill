# Output Packaging Rules

Use these rules for every `ba-spec` run that creates deliverables.

## Core rule

Do not create final deliverables as loose files in the repository/project root. Always create one output package directory and put all final files inside it.

## Default output root

Use this root unless the user provides another path:

```text
ba-spec-output/
```

## Package folder naming convention

Use this pattern:

```text
{{YYYY-MM-DD}}__epic-{{epic-slug}}__story-{{story-slug}}__{{feature-slug}}
```

Example:

```text
ba-spec-output/2026-06-23__epic-cong-chung-dien-tu__story-quy-trinh-cong-chung-dien-tu-truc-tiep__cong-chung-dien-tu-truc-tiep/
```

## Slug rules

- Lowercase.
- Remove Vietnamese accents.
- Replace spaces and punctuation with `-`.
- Collapse repeated hyphens.
- Trim leading/trailing hyphens.
- Keep only `a-z`, `0-9`, and `-`.
- Maximum recommended length per slug: 60 characters.

If the user provides an Epic or Story name, use it. If not, infer conservatively from the business input:

- `epic-slug`: high-level domain or process group, e.g. `cong-chung-dien-tu`.
- `story-slug`: primary user-facing workflow, e.g. `quy-trinh-cong-chung-dien-tu-truc-tiep`.
- `feature-slug`: feature name, e.g. `xac-thuc-cccd-va-ky-so`.

If unsure, use the feature name for both story and feature, and mark the Epic/Story mapping as `[ASSUMPTION]` in `README.md`.

## Required package structure

```text
{{package-folder}}/
  README.md
  feature-spec.md
  feature-spec.html
  figma-links.md                # required if Figma links/screenshots exist
  evidence/
    figma-evidence-log.md       # required if Figma links/screenshots exist
  handoff/
    dev-handoff-checklist.md    # recommended
  questions/
    clarification-questions.md  # recommended when open questions exist
```

Optional:

```text
  assets/
  exports/
  change-impact-summary.md
```

## Package README requirements

The package `README.md` must include:

- Feature name.
- Epic name and Story name.
- Created date.
- Source of truth path.
- HTML path.
- Figma link index path when applicable.
- Evidence log path when applicable.
- Blocking open question count.
- Quality gate status.
- Cleanup status.

## Final response

Final response must link to the package folder or files inside it, not to loose root files.
