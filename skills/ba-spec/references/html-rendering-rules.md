# HTML Rendering Rules

HTML is a presentation copy of `feature-spec.md`, not the source of truth.

## Required styling

Use Tailwind CDN in `templates/feature-spec.html`:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

## HTML requirements

The HTML must include:

- Vietnamese visible text.
- Clean typography.
- Table of contents.
- Metadata card.
- Evidence log.
- Distinct visual tags for source confidence.
- Tables for requirements, business rules, permissions, states, acceptance criteria, traceability.
- Highlighted assumptions and open questions.
- Print-friendly behavior.

## Consistency rule

Do not add content to HTML that is absent from Markdown. HTML mirrors the Markdown.

## Security/practicality rule

Do not embed sensitive tokens, private Figma credentials, or raw API secrets in HTML.


## Mermaid diagram rendering

If the Markdown spec contains Mermaid diagrams, the HTML output must render them visually. Do not leave Mermaid diagrams only as code blocks.

Use Mermaid.js CDN in `templates/feature-spec.html`:

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function () {
    if (window.mermaid) {
      window.mermaid.initialize({
        startOnLoad: true,
        theme: 'neutral',
        securityLevel: 'strict'
      });
    }
  });
</script>
```

For each diagram, output both:

1. A rendered block:

```html
<div class="mermaid">
flowchart TD
  A[Start] --> B[Next step]
</div>
```

2. A collapsible source fallback using `<details>` and `<pre><code>`.

This is required because some users open HTML files locally or in restricted environments where CDN scripts may be blocked.

Do not put Markdown fences such as ```mermaid inside the `<div class="mermaid">` block. Only put raw Mermaid DSL there.

## Step-by-step document variant (when screenshots exist)

When the source provides per-step screenshots (see `file-image-extraction-rules.md`), render the HTML as a **reading document**, not a screenshot gallery dumped at the end. For each business step:

- A numbered step header (actor + App/Web tag).
- A two-column block on desktop, stacked on mobile: left = narrative (actor → action → fields → selects → buttons); right = that step's screenshots as thumbnails.
- Each screenshot is a clickable thumbnail that zooms via a **pure-CSS lightbox** (no JS library), so it stays print-friendly.

Reading-document principles: body ≥16px, `line-height` ~1.6, limit measure (`max-width: 70ch`), clear heading/weight hierarchy, intentional whitespace to separate steps.

### Pure-CSS lightbox (no dependency)

```html
<style>
  .lb { position:fixed; inset:0; z-index:1000; display:flex; align-items:center; justify-content:center; padding:1.5rem; background:rgba(15,23,42,.88); opacity:0; pointer-events:none; transition:opacity .2s; }
  .lb:target { opacity:1; pointer-events:auto; }
  .lb img { max-width:96vw; max-height:92vh; border-radius:.5rem; }
  .lb-close { position:absolute; top:1rem; right:1.5rem; color:#fff; font-size:2rem; text-decoration:none; }
  .shot { cursor:zoom-in; }
  @media print { .lb { display:none !important; } }
</style>
<!-- thumbnail -->
<a href="#lb-image19"><img src="assets/image19.png" class="shot" alt="..."></a>
<!-- overlay (place near end of body) -->
<div id="lb-image19" class="lb"><a href="#steps-doc" class="lb-close">&times;</a><img src="assets/image19.png" alt="..."></div>
```

For PDF export, omit `loading="lazy"` on images that must appear (see `export-pdf-rules.md`).
