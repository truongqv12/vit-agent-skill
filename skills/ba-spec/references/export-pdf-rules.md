# PDF Export Rules (optional)

Apply only when the user explicitly asks for a PDF copy of the spec. PDF is a render of `feature-spec.html`, never a new source of truth. Default deliverables remain `feature-spec.md` + `feature-spec.html`.

## Render method

Render the existing `feature-spec.html` to PDF with a headless Chromium engine (Chrome or Edge). Do not add a PDF library dependency to the project.

Example (Chrome headless):

```bash
chrome --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=45000 --run-all-compositor-stages-before-draw \
  --user-data-dir="<os-temp>/ba-spec-chrome" \
  --print-to-pdf="<os-temp>/feature-spec.pdf" "<package>/feature-spec.html"
```

## Hard-won rules

1. **Write to OS temp, then copy.** Chrome is often denied write access directly inside the project directory. Print to an OS-temp path, then copy `feature-spec.pdf` into the package.
2. **No lazy images in the print pass.** `loading="lazy"` makes off-screen screenshots fail to render in the PDF (result: a tiny image-less PDF). For the print pass, render an HTML variant with `loading="lazy"` stripped, or omit lazy loading on images that must appear in PDF.
3. **Wait for client-side render.** Use a generous `--virtual-time-budget` (≈45s) so Mermaid diagrams and all images decode before printing.
4. **Sanity check size.** A spec with many screenshots should produce a multi-MB PDF. A few-KB PDF means images did not embed — fix lazy loading / virtual-time and re-render.
5. **Clean up.** Delete the temp Chrome profile and temp PDF after copying; keep only `feature-spec.pdf` in the package.

## Final response

When a PDF was produced, list it alongside the two default deliverables and state it was rendered from the HTML.
