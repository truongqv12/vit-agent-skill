# AGENTS.md

Guidance for AI coding agents working in this repository.

## Repository Overview

This repository is a multi-skill Agent Skills collection. Each skill is a standalone folder under `skills/<skill-name>/` and follows the Agent Skills format.

## Skill Directory Convention

```text
skills/
  {skill-name}/
    SKILL.md              # Required
    README.md             # Recommended
    references/           # Optional detailed rules loaded on demand
    scripts/              # Optional automation scripts
    templates/            # Optional output templates
    examples/             # Optional examples
    docs/                 # Optional setup/research docs
```

## SKILL.md Rules

- File name must be exactly `SKILL.md`.
- Use YAML frontmatter.
- Required fields: `name`, `description`.
- Keep `SKILL.md` focused and router-like.
- Put long rules in `references/`.
- Put reusable output skeletons in `templates/`.
- Put executable automation in `scripts/`.

## Adding a New Skill

1. Create `skills/<new-skill-name>/`.
2. Add `SKILL.md`.
3. Add `README.md`.
4. Add `references/`, `templates/`, or `scripts/` only when needed.
5. Update root `README.md`.
6. Update `skills.sh.json` grouping when appropriate.
7. Test discovery with:

```bash
npx skills add . --list
```

8. Test install locally with:

```bash
npx skills add . --skill <new-skill-name> -y
```

## ba-spec Notes

`ba-spec` must produce Vietnamese user-facing deliverables. Its `SKILL.md` is English for agent execution, but Markdown specs, HTML specs, questions, evidence logs, assumptions, and handoff checklists should be Vietnamese unless the user explicitly asks otherwise.

If input contains Figma URLs, `ba-spec` must run the Figma MCP evidence gate before writing or editing the spec. If MCP fails or is unavailable, the output must say so and must not claim Figma was analyzed.

HTML outputs from `ba-spec` must render Mermaid diagrams with Mermaid.js CDN and keep source fallback in collapsible blocks.
