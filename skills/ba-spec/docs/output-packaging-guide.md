# Output Packaging Guide

`ba-spec` creates one output folder per run so dev/QA receive a clean handoff instead of loose files.

## Default principle

The default output must be simple:

```text
feature-spec.md
feature-spec.html
```

The Markdown file is the source of truth. The HTML file is the readable version for team review.

Do not create separate README, Figma index, evidence log, checklist, or question files by default. Those sections belong inside the two files above.

## Recommended default folder

Use a short date folder plus a short feature slug:

```text
ba-spec-output/YYYYMMDD/{feature-slug}/
```

Example:

```text
ba-spec-output/20260623/cong-chung-dien-tu-truc-tiep/
  feature-spec.md
  feature-spec.html
```

This is preferred over embedding Epic, Story, and Feature into one long directory name.

## Optional Epic grouping

Only when the user asks for Epic grouping:

```text
ba-spec-output/{epic-slug}/YYYYMMDD-{feature-slug}/
```

Example:

```text
ba-spec-output/cong-chung-dien-tu/20260623-cong-chung-dien-tu-truc-tiep/
  feature-spec.md
  feature-spec.html
```

## Where Epic / Story info goes

Keep BA hierarchy in document metadata, not in long folder names:

- `feature-spec.md`
- `feature-spec.html`
- traceability matrix

## Figma links and evidence

If Figma input exists, embed these sections inside both `feature-spec.md` and `feature-spec.html`:

- `Danh sách link Figma gốc`
- `Nhật ký bằng chứng Figma`

Only create `figma-links.md` or `evidence/figma-evidence-log.md` when the user explicitly asks for separated evidence files.

## Optional companion files

Create companion files only on explicit request:

```text
README.md
figma-links.md
evidence/figma-evidence-log.md
handoff/dev-handoff-checklist.md
questions/clarification-questions.md
```

## Temporary files

Temporary helper scripts must be created in `.tmp/` or OS temp and deleted before final response.
