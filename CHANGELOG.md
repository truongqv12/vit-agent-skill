# Changelog

## 1.3.0

- Added required output package convention under `ba-spec-output/YYYY-MM-DD__epic-...__story-...__feature.../`.
- Added workspace hygiene rules: helper scripts/temp files must be created in tmp and deleted before final response.
- Added `figma-links.md` template and mandatory preservation of clickable original Figma URLs for dev/QA handoff.
- Added package README template and package/output quality gates.
- Updated Markdown/HTML templates to include Figma link index and package metadata.

## 1.2.0

- Restructured repository as a multi-skill collection under `skills/`.
- Added root `README.md`, `AGENTS.md`, `skills.sh.json`, `.gitignore`, and `LICENSE`.
- Updated `ba-spec` HTML template to render Mermaid diagrams using Mermaid.js CDN.
- Added source fallback for diagrams when CDN is blocked.

## 1.1.0

- Converted `ba-spec` to router-style `SKILL.md` plus `references/`.
- Added mandatory Figma MCP evidence gate.
- Added BA practice research and skill architecture research docs.
