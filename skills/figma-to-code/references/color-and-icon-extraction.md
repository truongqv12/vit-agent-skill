# Color & icon extraction reasoning

Load this when generating code from a Figma node and color/icon fidelity matters.
Covers what the JSON metadata reliably provides, where it silently fails, and how
to recover the truth from the rendered screenshot.

## Source-of-truth hierarchy

For every visual property, prefer the most reliable source available:

1. **Per-node JSON (`get_node` / IR `semanticNodes[].styles`)** — exact values.
   - `styles.fills` → background color (hex). Map to `background`.
   - `styles.strokes` → border color (hex). Map to `border-color`.
   - `characters` → text content (copy verbatim, keep Vietnamese diacritics).
   - `fontFamily` / `fontSize` / `fontStyle` / `fontWeight` / `textAlignHorizontal` → typography.
   - `bounds` `{x,y,width,height}` → geometry.
   - `cornerRadius` / `strokeWeight` / `effects` → radius, border width, shadow.
2. **Rendered screenshot (PNG)** — use ONLY to resolve the gaps below.
3. **Exported SVG** — for exact icon/vector path geometry.

Rule: take flat colors, text, fonts, sizes, and coordinates from JSON — never
"eyeball" them from the image when JSON has them. The image is for the cases JSON
cannot express.

## Where JSON silently fails → read the screenshot

The figma-mcp-go serializer flattens paint data. These cases REQUIRE the image:

| Symptom in JSON | Reality | Recovery |
|---|---|---|
| `styles.fills:["#825ef5"]` (one flat hex) | Node is a **gradient** | Read PNG, build `linear-gradient(...)`; JSON hex ≈ one stop |
| `styles:{}` empty, node clearly visible | Paint exists but was dropped | Read the visible color at that node's `bounds` from PNG |
| `fills:"mixed"` (string, not array) | **Multiple fills** in one node | Split visually; e.g. label text gray + required `*` red |
| Text fill `"mixed"` on a `*` label | Label color ≠ asterisk color | Render label in muted color, `*` in danger red |
| Subtle shadow not in `effects` | Soft drop shadow | Approximate `box-shadow` from PNG |

Concrete examples from a real frame (node 6101:38389):

```jsonc
// Flat fill in JSON, gradient in render → use gradient
{"id":"6101:38546","styles":{"fills":["#825ef5"]}}        // "Thêm" button
// Empty styles, visibly purple in PNG → read color from image
{"id":"6101:38540","styles":{}}                            // "Tiếp tục" button
// mixed = label + red asterisk
{"id":"6101:38848","characters":"Họ và tên *","styles":{"fills":"mixed"}}
```

## Icons: JSON has color, NOT shape

`get_node` decomposes an icon into many child `VECTOR` nodes that carry `bounds`
and `styles` (stroke/fill hex) but **no usable path `d`**. You cannot reconstruct
the glyph from JSON. Two valid strategies — pick per fidelity need:

- **Exact (export SVG):** export the icon node with
  `save_screenshots`/`get_screenshot` `format:"SVG"`; inline the returned path.
  Use when the icon is brand/custom or pixel-exact tracing is required.
- **Practical (recreate line-icon):** redraw a matching Lucide/Feather-style icon,
  and take the **color from the JSON `strokes`/`fills` hex**. Use for generic line
  icons (chevron, search, calendar, plus, pencil, contactless/NFC, etc.).

Read the icon's sub-vector `bounds` to guess the glyph: e.g. a small circle `6x6`
plus an arc `12x4` is a contactless/NFC wave; three nested arcs = wifi/NFC.

Record which strategy you used so a reviewer can re-trace if needed.

## Screenshot capture without blowing the token budget

`get_screenshot` returns base64 image data inline; for a full frame this often
**exceeds the tool-result token limit** and fails. Prefer writing to disk:

```jsonc
// Write PNG (for visual checks) AND SVG (for exact icon/vector paths)
save_screenshots({ items: [
  { nodeId: "<id>", outputPath: "<snapshot>/screenshot.png", format: "PNG", scale: 2 },
  { nodeId: "<id>", outputPath: "<snapshot>/reference.svg", format: "SVG" }
]})
```

Then `Read` the PNG (vision) to resolve gradients/empty-fill/mixed cases, and open
the SVG only when you need an exact icon path.

## Validation loop (render → look → fix)

After generating code, render it and compare to the PNG:
1. Render the page headless (e.g. Chrome `--headless --screenshot=out.png "file:///..."`,
   or the repo's visual test tool). On a file path, pass a `file://` URL — a bare
   `index.html` is treated as a hostname and fails to load.
2. Read the render and the Figma PNG side by side.
3. Fix the largest mismatch first: layout → typography → color → radius/shadow → missing nodes.
4. Repeat until major mismatches are gone; document any deliberate deviation
   (e.g. fonts loaded via CDN, icons recreated rather than traced).
