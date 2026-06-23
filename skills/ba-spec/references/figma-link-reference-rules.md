# Figma Link Reference Rules

Use these rules whenever the input contains Figma URLs.

## Core rule

Every original Figma URL provided by the user must be preserved as a clickable reference in the final deliverables. Do not replace original URLs with only node IDs.

## Default output location

Do not create `figma-links.md` or `evidence/figma-evidence-log.md` by default.

Instead, include Figma reference tables inside both default deliverables:

```text
feature-spec.md
feature-spec.html
```

Create separate `figma-links.md` or `evidence/figma-evidence-log.md` only when the user explicitly asks for separated companion files or debug/evidence artifacts.

## Required sections inside feature-spec.md

If Figma input exists, `feature-spec.md` must include:

1. `Danh sách link Figma gốc`
2. `Nhật ký bằng chứng Figma`

## Required sections inside feature-spec.html

If Figma input exists, `feature-spec.html` must mirror the same information with clickable links.

## Required fields

Each Figma link row must include:

- Stable ID, e.g. `FIG-LINK-001`.
- User-provided label, e.g. `app1`, `Màn thêm mới`, `Ký USB Token`.
- Business step, e.g. `Bước 1`.
- Original full URL as a clickable Markdown/HTML link.
- File key if extractable from URL.
- Node ID if extractable from URL.
- MCP result: `MCP_SUCCESS`, `MCP_UNAVAILABLE`, `MCP_FAILED`, `USER_SKIPPED`, or `SCREENSHOT_ONLY`.
- Extracted UI evidence or fallback note.

## Markdown link format

Use this format in Markdown:

```markdown
[app1](https://www.figma.com/design/...)
```

## HTML link format

Use this format in HTML:

```html
<a href="https://www.figma.com/design/..." target="_blank" rel="noopener noreferrer">app1</a>
```

## Evidence integrity

- If MCP succeeds: write `[FIGMA]` facts only for extracted UI evidence.
- If MCP fails/unavailable: keep the link, mark the row as failed/unavailable, and do not create `[FIGMA]` facts from that link.
- If the same URL appears more than once, preserve one canonical row and mention duplicate references.

## Dev handoff expectation

Dev and QA must be able to open the original design links directly from the Markdown and HTML spec.
