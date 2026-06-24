# figma-to-code

Skill for converting one selected Figma node into production UI code with deterministic extraction.

This version fixes a common Figma/MCP issue: normal UI boxes may be exported as `VECTOR`.
The extractor now preserves vector fills/strokes as implementation CSS and marks them with:

- `renderHint: "css-box"`
- `renderHint: "css-divider"`
- `renderHint: "svg-or-icon"`

## Install

Copy this folder into your agent skill path, for example:

```txt
.agent-skills/
  figma-to-code/
    SKILL.md
    scripts/
      extract_figma_ir.py
```

Or keep it in a repo structure:

```txt
vit-agent-skill/
  skills/
    figma-to-code/
      SKILL.md
      scripts/
        extract_figma_ir.py
```

## Run extractor

```bat
python -X utf8 .agent-skills\figma-to-code\scripts\extract_figma_ir.py --input .design-snapshots\feature\raw-output.json --out .design-snapshots\feature\figma-ir.json
```

With target node:

```bat
python -X utf8 .agent-skills\figma-to-code\scripts\extract_figma_ir.py --input .design-snapshots\feature\raw-output.json --out .design-snapshots\feature\figma-ir.json --target-node-id 5675:288345
```

## Important IR fields

- `shapePrimitives`: vector/shape nodes with CSS.
- `compositeControls`: inferred button/input/select/badge pairings.
- `semanticNodes`: all kept nodes.
- `tokens`: colors, fonts, sizes, radii, strokes.
- `layout`: inferred columns/rows/sections.

The coding agent should not ignore `VECTOR` nodes with `renderHint: "css-box"`.
