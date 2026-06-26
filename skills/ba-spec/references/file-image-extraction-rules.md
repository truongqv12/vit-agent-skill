# File Image Extraction Rules

Apply when an input file (`.docx`, `.pptx`, `.pdf`) may contain embedded screenshots or diagrams that document UI/flow. Images in a spec source are evidence, not decoration — extract them and treat them as `[FILE]`.

## When to extract

Extract embedded images whenever:

- The file describes a UI, screen flow, or step-by-step process.
- Paragraphs reference figures (e.g. "Hình: ...", "Figure:", "Giao diện ...").
- The user asks to "use the images", "lấy ảnh", or embed screenshots.

If the file is text-only, skip this step.

## How to extract (deterministic, no extra dependency)

`.docx`/`.pptx` are ZIP archives. Extract with the language runtime's zip support — do not install new packages.

1. Unzip the file to a temp dir under the OS temp (prefix `ba-spec-`), not the project root.
2. Read media from `word/media/` (docx) or `ppt/media/` (pptx). Each is `imageN.ext`.
3. Parse the body XML (`word/document.xml`) **in document order**, walking paragraphs and `a:blip r:embed` IDs, resolving them via `word/_rels/document.xml.rels` to the media filename.
4. Pair each image with the **caption paragraph** that follows/precedes it (e.g. the "Hình: ..." line) so every image keeps its meaning.
5. For `.pdf`, extract embedded images with an available runtime tool; if none is available, record an `[OPEN_QUESTION]` instead of guessing.

## Where images go

Copy extracted images into the package `assets/` folder (see `output-packaging-rules.md`). Reference them with **relative paths** (`assets/imageNN.png`) from both `feature-spec.md` and `feature-spec.html`.

`assets/` is an allowed companion folder **only when the source contains images**; otherwise keep the default two-file package.

## Evidence discipline

- Tag every extracted screen `[FILE]`.
- Do not invent UI elements not visible in the image. If text and image conflict, raise `[OPEN_QUESTION]` (see `quality-gates.md`).
- When many images exist, you may delegate per-image field/button/state extraction to a vision-capable sub-agent, returning structured Vietnamese descriptions — but the controller still owns the spec.
- Map each screenshot to its business step so the spec stays step-by-step (see `html-rendering-rules.md` step-by-step variant).
