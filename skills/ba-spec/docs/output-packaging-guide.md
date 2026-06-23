# Output Packaging Guide

`ba-spec` creates one output package per run so dev/QA receive a clean handoff folder instead of loose files.

## Default folder name

```text
ba-spec-output/YYYY-MM-DD__epic-{epic-slug}__story-{story-slug}__{feature-slug}/
```

Example:

```text
ba-spec-output/2026-06-23__epic-cong-chung-dien-tu__story-quy-trinh-cong-chung-dien-tu-truc-tiep__cong-chung-dien-tu-truc-tiep/
```

## Required files

```text
README.md
feature-spec.md
feature-spec.html
```

When Figma input exists:

```text
figma-links.md
evidence/figma-evidence-log.md
```

## Temporary files

Temporary helper scripts must be created in `.tmp/` or OS temp and deleted before final response.
