# UI Fix Workflow

For fixing visual and interaction issues. This route leans on capabilities that
may be absent; each has a native fallback and none is required.

## Capabilities used

- A **frontend design / UX** capability for design-system and implementation
  guidance. Absent -> follow the project's existing component patterns and any
  routed design guidance.
- A **visual/multimodal** capability to analyze screenshots/videos and verify
  the rendered result. Absent -> compare against the accepted design manually.
- A **browser-automation** capability, or the project's own browser tests, to
  inspect runtime behavior. Absent -> skip and note it.

## Pre-fix research

If a design/pattern research capability is available, query it for the relevant
product type, style, and accessibility guidance before implementing. Otherwise,
read the project's own design guidance and nearby components.

## Progress tracking

The stages are `analyze -> implement -> verify visually -> inspect runtime ->
test -> document`. Use a live **task-tracking** capability to mirror this chain
when available; otherwise update the active plan. Plan files are the durable
source of truth.

## Workflow

### Step 1: Analyze

Analyze screenshots or videos with the **visual/multimodal** capability. Read
the project's routed design guidance when present and identify the exact
discrepancy.

### Step 2: Implement

Follow existing component patterns and the frontend design/UX guidance.

### Step 3: Verify visually

Capture the affected container, compare it with the accepted design, and use the
**visual/multimodal** capability when useful. If incorrect, return to Step 2.

### Step 4: Inspect runtime behavior

Use a **browser-automation** capability or the project's own browser tests.
Check interaction, console, and network behavior.

### Step 5: Test

Use the **testing** capability for compilation and the affected UI test surface,
or run the project's test command directly.

### Step 6: Document

Update routed design guidance only when the accepted design contract changed.

## Tips

- Use a **visual/multimodal** capability for generating visual assets.
- Use a deterministic image-processing tool (for example ImageMagick) for image
  transformations.
