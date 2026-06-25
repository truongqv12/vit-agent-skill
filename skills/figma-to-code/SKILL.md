---
name: figma-to-code
description: Translates exactly one selected Figma frame, component, or instance into production-ready frontend code with deterministic extraction, design-token mapping, component reuse, and visual validation. Use when implementing UI code from Figma, when the user mentions "implement design", "generate code", "implement component", "build this Figma", "match Figma", provides a Figma URL, or asks for UI code that must match a Figma selection. Do not use for editing the Figma canvas itself.
---

# Figma implement fidelity

## Purpose

Implement frontend UI from Figma with repeatable 1:1 visual fidelity. The agent must not code directly from a raw MCP dump. It must first create a deterministic design snapshot and normalized IR, then generate code from that IR and validate the result against a Figma screenshot.

## When to use

Use this skill when:

- The deliverable is application code, not edits inside Figma.
- The user provides a Figma URL, node ID, screenshot plus MCP output, or has selected a node in Figma desktop.
- The user asks to implement, generate, convert, or match a Figma design/component/screen/modal.
- Visual fidelity, exact spacing, typography, colors, and layout consistency matter.

Do not use this skill when:

- The user wants to create or modify nodes in Figma itself.
- The input is only a vague UI description with no Figma source.
- The user asks only for design critique or copy changes.

## Hard rules

1. Work from exactly one target node: a selected `FRAME`, `COMPONENT`, `COMPONENT_SET`, or `INSTANCE`.
2. Never implement from full `get_document` output unless debugging. Full document dumps often include sibling frames, off-canvas variants, and hidden layers.
3. Always produce a snapshot directory before coding.
4. Always run `scripts/extract_figma_ir.py` before the agent reads the raw MCP output in detail.
5. Generate code from `figma-ir.json`, not directly from raw MCP JSON.
6. Treat Figma screenshot as the visual source of truth for validation, not as the only implementation source.
7. Ignore hidden nodes, opacity-zero nodes, off-canvas sibling frames, and nodes outside the selected target bounds unless explicitly needed as overlays/assets.
8. Reuse project components and design tokens before creating raw HTML/CSS primitives.
9. Use absolute positioning only for icons, decorative vectors, and intentional overlays. Use flex/grid for forms, lists, cards, headers, footers, and main layout.
10. Validate rendered UI with screenshot comparison before declaring completion.
11. On Windows, run Python commands with `python -X utf8`.
12. Do not inspect raw Figma JSON with `json.load(open(path))`. Use `scripts/extract_figma_ir.py`, or use `Path(path).read_text(encoding="utf-8-sig")` for any quick JSON inspection.
13. Take flat colors, text, fonts, sizes, radius, and coordinates from JSON (`styles.fills`/`styles.strokes`/`characters`/`fontFamily`...). Do NOT eyeball them from the screenshot when JSON has them.
14. Use the screenshot to RECOVER what JSON cannot express: gradients (JSON gives one flat fill), empty `styles:{}` on a visible node, and `fills:"mixed"` (multiple colors in one node, e.g. label + red `*`). See `references/color-and-icon-extraction.md`.
15. Icons: JSON gives stroke/fill HEX but no usable path `d`. Either export the icon node as SVG (`save_screenshots` `format:"SVG"`) for exact paths, or recreate a matching line-icon and color it from the JSON hex. Record which.
16. Capture screenshots with `save_screenshots` to disk (PNG for visual checks + SVG for icon paths). Avoid `get_screenshot` for full frames — its inline base64 often exceeds the tool-result token limit.

## Required workflow

### 1. Resolve the target

If a Figma URL is provided, extract the exact `node-id`. If only desktop Figma is available, call the selection tool first.

Reject ambiguous targets:

- Multiple top-level selected nodes.
- A page/canvas/document root instead of a frame/component.
- A parent frame that contains many unrelated screens.

If there is ambiguity, choose the most specific selected frame or component. Do not crawl unrelated siblings.

### 2. Fetch focused design context

Preferred MCP sequence for `figma-mcp-go` style tools:

1. `get_selection`
2. `get_design_context` for the selected node, compact first
3. `get_node` for the selected node only when deeper details are required
4. `get_styles`
5. `get_variable_defs`
6. `get_fonts`
7. `export_tokens`
8. `save_screenshots` for the same node — write PNG (visual) + SVG (icon paths) to the snapshot dir. Prefer this over `get_screenshot`, whose inline base64 often exceeds the tool-result token limit for a full frame.

Avoid `get_document` for implementation. If a response is truncated, fetch smaller child nodes by ID rather than broadening scope.

### 3. Save a deterministic snapshot

Create:

```text
.design-snapshots/<feature-name>/
  raw-output.json
  screenshot.png
  tokens.json
  styles.json
  fonts.json
  component-registry.json
  figma-ir.json
```

### 4. Run the extractor before reading raw output

Run:

```bash
python -X utf8 .claude/skills/figma-to-code/scripts/extract_figma_ir.py \
  --input .design-snapshots/<feature-name>/raw-output.json \
  --out .design-snapshots/<feature-name>/figma-ir.json \
  --target-node-id <nodeId>
```

If the target node ID is unknown, run the extractor without `--target-node-id` to get a candidate summary, then re-run with the chosen target.


On Windows, never inspect JSON with the default encoding:

```bash
# Do not use this:
python -c "import json; data=json.load(open('.design-snapshots/<feature-name>/raw-output.json')); print(data.keys())"

# Use this instead:
python -X utf8 -c "import json, pathlib; p=pathlib.Path(r'.design-snapshots/<feature-name>/raw-output.json'); data=json.loads(p.read_text(encoding='utf-8-sig')); c=(data.get('context') or [data])[0]; print(c.get('id'), c.get('type'), c.get('name'))"
```

### 5. Inspect the IR summary

Before coding, read only:

- `summary`
- `layout.columns`
- `layout.sections`
- `tokens`
- `semanticNodes`
- `warnings`

Only open raw output when IR has warnings that require source verification.

### 6. Map to project conventions

Check the repository before creating new primitives:

- Existing `Button`, `Input`, `Select`, `Dialog`, `Modal`, `Card`, `Table`, `Typography`, `Icon`, `FormField` components.
- CSS variable names, Tailwind config, design token files, theme provider, and font imports.
- Routing, data fetching, validation, and state management conventions.

Use `examples/component-registry.example.json` as the registry format if the repo does not already have one.

### 7. Generate code

Implementation priorities:

1. Semantic structure: modal/header/body/footer, form sections, form rows, fields, actions.
2. Layout: columns, rows, gaps, padding, width/height from IR.
3. Typography: font family, size, weight, line height.
4. Colors, borders, radius, shadows, opacity — flat values from JSON; resolve gradients / empty `styles:{}` / `fills:"mixed"` from the screenshot per `references/color-and-icon-extraction.md`.
5. Assets/icons: export the icon node as SVG for exact paths, or recreate a line-icon colored from the JSON hex (JSON has icon color but no usable path `d`).
6. Responsive behavior from constraints/auto-layout patterns.

Do not copy hidden-node styles into global CSS.

### 8. Validate visually

Render the result and capture a screenshot (Playwright, the repo's visual test tool, or headless Chrome `--headless --screenshot`). When rendering a local file, pass a `file://` URL — a bare `index.html` is parsed as a hostname and fails to load. Compare with the Figma reference:

- Layout: x/y/width/height/gap differences.
- Typography: font family, size, weight, line-height.
- Color: fill/stroke/text/background.
- Radius/shadow/opacity.
- Missing/extra nodes.

Iterate until the major mismatches are fixed. If exact parity is impossible, document why.

## Common failure modes to prevent

- Raw MCP output includes unrelated sibling frames and the agent copies their styles.
- Parser generated by the agent changes every run.
- Hidden variants leak styles into visible elements.
- Vector rectangles are treated as semantic containers without grouping.
- The agent creates absolute-positioned layouts for forms that should be flex/grid.
- Figma MCP output is treated as final React/Tailwind instead of a design reference.
- Screenshot is used without metadata, causing guessed spacing and typography.
- A gradient or empty-`styles` node is shipped as the wrong flat color because the screenshot was never consulted.
- Icon shapes are invented from imagination instead of exported SVG or a matched line-icon colored from the JSON hex.

## Example prompt

```text
Implement the selected Figma node in this repo using the figma-to-code skill.

Requirements:
- Use the exact selected frame/component only.
- Run the extractor before reading raw MCP output in detail.
- Generate code from figma-ir.json, not raw output.
- Reuse existing Button/Input/Select/Modal/FormField components.
- Use project tokens where possible.
- Validate against the Figma screenshot with Playwright and fix visible mismatches.
```
