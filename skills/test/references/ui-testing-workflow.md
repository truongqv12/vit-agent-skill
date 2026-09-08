# UI Testing Workflow

Run UI tests through whatever browser path the runtime and the user's request
permit, native-first:

- A **browser-automation capability** for live browser interaction when a
  fresh / tool-managed browser is enough.
- The user's **real-profile browser capability** only when a test needs the
  user's real browser profile, cookies, or already-logged-in state, and the
  user permits it.
- **Project-native** Playwright / Vitest / k6 commands for repeatable test runs.

If no browser-automation capability is available and the project has no native
browser tests, report the missing capability honestly rather than skipping the
check silently.

## Purpose

Run comprehensive UI tests on a website and generate a detailed report.

## Arguments

- `$1: URL` — the URL of the website to test.
- `$2: OPTIONS` — optional test configuration (e.g. `--headless`, `--mobile`,
  `--auth`).

## Testing protected routes (authentication)

### Step 1: Establish auth state

Prefer project-native auth helpers (stored storage-state / fixtures) for
repeatable tests. For ad-hoc driving that needs the user's real login/cookies,
use the real-profile browser capability and its setup/verification steps, with
the user's permission.

If real user profile state is NOT required, use a fresh tool-managed browser and
capture its state after a manual login step when the capability supports it.

### Step 2: Run tests

After auth is available, run tests normally.

- Without real user state: open the target page with the browser-automation
  capability and capture screenshots/snapshots.
- With real user state: open through the real-profile browser capability, bind
  to the page it returns for that profile, and capture through that active
  bridge. Do not drive an arbitrary page/profile as the opening path when a
  specific profile is required.

## Workflow

- Use a planning/organization capability to organize the test plan and report;
  otherwise structure them inline by the project's convention.
- Save all screenshots in the same report directory.
- Browse the URL, discover pages, components, and endpoints.
- Create a test plan based on the discovered structure.
- When parallel delegation is available and the user permits it, split the work
  across scopes (pages, forms, navigation, user flows, accessibility, responsive
  layouts, performance, security, SEO); otherwise cover them sequentially.
- Analyze screenshots with a vision/screenshot-analysis capability when
  available; otherwise reference the saved paths.
- Generate a comprehensive Markdown report.

## Output requirements

- Clear, structured Markdown with headers, lists, and code blocks.
- Include a test-results summary, key findings, and screenshot references.
- Keep it token-efficient while maintaining high quality; sacrifice grammar for
  concision.

**Do not** start implementing fixes.
