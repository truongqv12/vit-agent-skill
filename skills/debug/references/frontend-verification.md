# Frontend Verification

Visual verification of a frontend diagnosis through whatever browser-automation
capability the runtime exposes, or the project's own browser tests. This is a
read-only verification step, not a fix.

## Capability handoff

Browser automation is an **optional** capability:

- Use a browser-automation capability when the runtime exposes it and the
  user's request permits it. Runtimes surface this differently — an
  agent-driven browser, a real user-profile browser bridge, a browser MCP
  server, or the project's own end-to-end test runner.
- When real user login/cookies/profile state is required, use the
  runtime's profile-aware browser capability so the session carries that state;
  otherwise a generic, profile-independent browser capability is fine.
- If no browser capability is available, fall back to the project's browser
  tests. If none exist, skip visual verification and note it in the report.

Never assume a specific browser tool is installed.

## Applicability Check

**Skip entirely if the task is NOT frontend-related.** Frontend indicators:

- Files modified: `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.html`, `*.css`, `*.scss`
- Changes to: components, layouts, pages, styles, DOM structure, UI behavior
- Keywords: render, display, layout, responsive, animation, visual, UI, UX

If none match, skip this technique.

## Step 1: Decide the Verification Path

1. Does this verification need real user Chrome/browser profile state (login,
   cookies)?
   - **No:** use a generic browser-automation capability or the project's
     browser tests.
   - **Yes:** use a profile-aware browser capability so the session carries the
     user's real state. Do not drive profile-scoped tabs with a
     profile-independent tool.
2. Ensure the dev server is running before navigating.

## Step 2: Navigate, Screenshot, Inspect

Using the chosen browser capability:

1. Open the implementation URL (e.g. the local dev server).
2. Capture a screenshot or page snapshot.
3. Read the screenshot with a file-read capability to visually inspect it.

### Visual Inspection Checklist

After capturing the screenshot, verify:

1. **Layout** — Elements positioned correctly, no overflow/overlap
2. **Content** — Text, images, data rendered as expected
3. **Responsiveness** — Resize the viewport if the capability supports it
4. **Interactions** — Drive clicks/typing to test interactive elements
5. **Console errors** — Read console error output through the capability

### Console Error Check

Evaluate console error state in the page, for example reading any collected
`console.error` output, or observe error output surfaced by the browser
capability's responses. Zero errors = pass; errors = investigate before
claiming done.

### Get Page Content

Extract the rendered DOM/text through the capability to verify output matches
expectations.

## Step 3: Fallback When No Browser Capability

- Prefer the project's own browser tests (Playwright/Vitest/Cypress or
  equivalent) for repeatable evidence.
- If no browser tool and no project browser tests are available, skip visual
  verification and note in the report:

  > "Visual verification skipped — no browser-automation capability or
  > project-native browser test available."

## Step 4: Analyze Results

After capture:

1. **Read screenshot** — Visually inspect the PNG
2. **Check console output** — Zero errors = pass; errors = investigate
3. **Compare with expected** — Match against design specs or user description
4. **Document findings** — Include screenshot path and any issues in the report

## Integration with Verification Protocol

This technique extends `verification.md`. After standard verification (tests
pass, build succeeds), add frontend verification as the final gate:

```
Standard verification → Tests pass → Build succeeds → Frontend visual verification → Claim complete
```

Report format:

```
## Frontend Verification
- Method: [browser-automation capability | project-native browser test | skipped]
- Screenshot: ./verification-screenshot.png
- Console errors: [none | list]
- Visual check: [pass | issues found]
- Responsive: [checked at X viewports | skipped]
```
