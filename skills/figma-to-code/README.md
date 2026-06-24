# vit-agent-skill: Figma implement fidelity

This package contains an agent skill for converting a single Figma selection into production frontend code with deterministic extraction and visual validation.

Suggested location in a repo:

```text
.agent-skills/figma-to-code/SKILL.md
.agent-skills/figma-to-code/scripts/extract_figma_ir.py
```

For Claude Code compatibility, you can also place it at:

```text
.claude/skills/figma-to-code/SKILL.md
```

The key design choice is to run the extractor before the agent reads the raw MCP dump. This reduces token usage and prevents sibling frames, hidden layers, and off-canvas variants from contaminating implementation.
