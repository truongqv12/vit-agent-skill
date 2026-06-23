# Changelog

## 1.5.0

- Changed `ba-spec` default output to only two files inside the output folder: `feature-spec.md` and `feature-spec.html`.
- Embedded Figma original links, Figma evidence log, open questions, assumptions, Dev/QA notes, and quality checklist inside the two default deliverables.
- Marked `README.md`, `figma-links.md`, `evidence/`, `handoff/`, and `questions/` as optional companion files only when explicitly requested.
- Kept short output folder convention: `ba-spec-output/YYYYMMDD/feature-slug/`.

## 1.4.0

- Shortened `ba-spec` output folder convention to `ba-spec-output/YYYYMMDD/feature-slug/`.
- Added optional Epic grouping only when explicitly requested.
- Added output packaging guide.

## 1.3.0

- Added output packaging rules.
- Added workspace hygiene rules.
- Required original Figma links to be preserved for dev/QA.
- Added cleanup expectations for temporary helper scripts.

## 1.2.0

- Converted repository to multi-skill structure under `skills/`.
- Added Mermaid.js support in HTML template.
- Added root `README.md`, `AGENTS.md`, `skills.sh.json`, `.gitignore`, and `LICENSE`.

## 1.1.0

- Refactored `ba-spec` into router-style `SKILL.md` plus `references/` rule files.
- Added Figma MCP evidence gate.

## 1.0.0

- Initial `ba-spec` skill.
