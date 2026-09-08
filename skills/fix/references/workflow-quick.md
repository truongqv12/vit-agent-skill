# Quick Workflow

Fast scout -> diagnose -> fix -> verify cycle for simple issues.

The parent skill's opening intent frame is already satisfied before this route
loads. Quick mode does not skip or repeat it.

## Step 1: Scout (minimal)

Locate affected file(s) and their direct dependencies only.

- Read the error message -> identify the file path.
- Check direct imports/dependencies of the affected file.
- Skip full codebase mapping.

**Output:** `Step 1: Scouted - [file], [N] direct deps`

## Step 2: Diagnose (abbreviated)

Use the **debugging** capability for structured analysis; otherwise reason
through the evidence inline.

- Read the error message/logs.
- **Capture pre-fix state:** record exact error output — this is the
  verification baseline.
- Identify the root cause (usually obvious for simple issues).
- Skip parallel hypothesis testing for trivial cases.
- Confirm there is one direct, cause-aligned repair. If meaningful alternatives
  remain, escalate to Standard or Deep before implementing.

**Output:** `Step 2: Diagnosed - Root cause: [brief description]`

## Step 3: Fix & verify

Implement the fix directly.

- Make minimal changes.
- Follow existing patterns.
- Preserve the opening constraints and non-goals.

**Verification:** re-run the EXACT command from the pre-fix capture and compare
output. Run typecheck and lint through the shell; split across workers only when
delegation is permitted. See `references/parallel-exploration.md`.

**Output:** `Step 3: Fixed - [N] files, verified (types/lint passed)`

## Step 4: Review + prevent

Use the **code-review** capability for a quick review with an explicit
side-effect sweep; otherwise review the diff inline. Check: (a) acceptance
criteria met, (b) no regression to business logic in the blast radius from
Step 1, (c) no breaking changes to public contracts (signatures, schemas, APIs,
env vars), (d) follows existing patterns, (e) no new lint/type/build errors.
Score X/10 and explicitly flag any side effects.

See HARD-GATE-NO-SIDE-EFFECTS in `SKILL.md` — on a flagged regression, use the
**interactive-prompt** capability with 2-4 options (revert / narrow / update
dependents / accept).

**Prevention (abbreviated for Quick):**

- Type/lint errors: the type system is the test -> regression test optional.
- Bug fixes: add at least 1 test covering the fixed scenario.
- Still require a before/after comparison of verification output.

**Review handling:** see `references/review-cycle.md`.

**Output:** `Step 4: Review [score]/10 - [prevention measures]`

## Step 5: Report

Report the summary to the user (root cause, files changed, prevention).

**Output:** `Step 5: Reported`

## Step 6: Finalize (MANDATORY — every fix)

1. Sync plan status and progress through the **task-tracking** capability when a
   runtime surface exists; otherwise update the active plan. Not optional.
2. Evaluate docs impact; use the **documentation** capability only when a routed
   authority surface changed.
3. Commit through the **version-control** capability, or with git via the shell.
4. Optionally record a journal entry through a **journaling** capability when one
   exists.

**Output:** `Step 6: Finalized - sync-back complete, committed`

## Notes

- Escalate to Standard if review fails.
- No planning phase needed.
- Pre-fix state capture is STILL mandatory (even for quick fixes).
- Step 6 finalize is MANDATORY — progress sync is not optional, though the
  durable authority is always the plan file.
