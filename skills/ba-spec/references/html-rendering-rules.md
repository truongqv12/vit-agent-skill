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
