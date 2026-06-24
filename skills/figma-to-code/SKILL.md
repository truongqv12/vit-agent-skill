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
13. Do not ignore `VECTOR` or `RECTANGLE` nodes. In flattened Figma exports, these often represent real UI surfaces: backgrounds, cards, inputs, buttons, badges, overlays, and dividers.
14. If a node has `renderHint: "css-box"`, implement it as a DOM/CSS box or map it to a project component. Do not treat it as a decorative SVG.
15. If a node has `renderHint: "svg-or-icon"`, keep it as an icon/SVG asset or use an existing icon component. Do not use its fill/stroke as a parent element background.
16. Read `compositeControls` before writing form/button code. These pair background vectors with contained text/icon nodes.


### Vector-as-box interpretation

Many Figma/MCP dumps flatten normal UI elements as `VECTOR`. The extractor preserves those nodes in three places:

- `shapePrimitives`: every visible vector/shape with its `role`, `renderHint`, bounds, and CSS.
- `semanticNodes`: all filtered nodes, including shape nodes with `css`.
- `compositeControls`: inferred controls/buttons/badges created by pairing a CSS-box vector with text/icon nodes inside it.

Implementation rules:

```txt
renderHint = "css-box"     → DOM/CSS box, component surface, input border, button background, card, badge, overlay
renderHint = "css-divider" → border/divider
renderHint = "svg-or-icon" → icon/SVG asset, not a layout background
renderHint = "text"        → text node
```

Never discard a `VECTOR` only because its name is `Vector`. First check `role`, `renderHint`, and `css`.

When writing code, process IR in this order:

```txt
summary
tokens
layout
compositeControls
shapePrimitives
semanticNodes
```

If `shapePrimitives` contains CSS boxes with `backgroundColor` or `borderColor`, those styles must be represented in the generated UI. Typical mappings:

```txt
role = overlay       → fixed/absolute overlay background
role = modal-surface → modal/dialog container background
role = surface       → page/card/upload area/table surface
role = control-box   → input/select/date-picker shell
role = button-bg     → button component/background
role = badge         → chip/status badge
role = divider       → border line
```

If a vector UI box is missing radius/effects, do not invent large values. Use a conservative project default and add a note that the MCP serializer may need to export `cornerRadius`, `effects`, `strokeWeight`, and `opacity`.

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
8. `get_screenshot` for the same selected node

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
python -X utf8 .agent-skills/figma-to-code/scripts/extract_figma_ir.py \
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
4. Colors, borders, radius, shadows, opacity.
5. Assets/icons from snapshot or MCP asset endpoint.
6. Responsive behavior from constraints/auto-layout patterns.

Do not copy hidden-node styles into global CSS. Do not invent icon packages when Figma provides assets.

### 8. Validate visually

Run the app and capture screenshot with Playwright or the repo's visual test tool. Compare with the Figma reference:

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
