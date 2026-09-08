# Standard Workflow

Full pipeline for moderate-complexity issues. Use a live **task-tracking**
capability for phase tracking when the runtime exposes one; otherwise update the
active plan. Plan files are the durable source of truth.

The parent skill captures the opening intent frame before this route loads.

## Plan setup (before starting)

Record the phase dependency order upfront:

- Scout codebase.
- Diagnose root cause.
- Implement fix, blocked by scout + diagnose.
- Verify + prevent, blocked by implementation.
- Code review, blocked by verification.
- Finalize, blocked by review.

## Step 1: Scout codebase

Mark the scout phase active.

- Use the **scouting** capability, or launch 2-3 parallel exploration agents in
  one turn when delegation is explicitly requested/permitted; otherwise scan
  with native search + reads.
- Map: affected files, module boundaries, dependencies, related tests, recent
  git changes.

See `references/parallel-exploration.md`. Mark scout complete after evidence is
captured.

**Output:** `Step 1: Scouted [N] areas - [M] files, [K] tests found`

## Step 2: Diagnose root cause

Mark the diagnose phase active.

1. **Capture pre-fix state:** exact error messages, failing test output, stack
   traces.
2. Use the **debugging** capability (systematic root-cause investigation);
   otherwise reason through the evidence inline.
3. Form hypotheses through structured reasoning — no guessing.
4. Test hypotheses with parallel exploration agents only when delegation is
   explicitly requested/permitted.
5. If 2+ hypotheses fail, switch to a structured problem-solving reframe.
6. Trace backward to the root cause (not just the symptom location).

Use the root-cause checklist in the parent skill. Mark diagnose complete after
the root cause is proven.

**Output:** `Step 2: Diagnosed - Root cause: [summary], Evidence: [brief], Scope: [N files]`

Before implementing, compare only cause-aligned fixes. Record the direct choice
and its fit with the acceptance criteria. If multiple viable approaches or an
architecture decision remain, use an **ideation** capability and escalate to
Deep for a plan.

## Step 3: Implement fix

Mark implementation active once scout and diagnosis are complete.

Fix the ROOT CAUSE per diagnosis, not symptoms.

- Apply a structured problem-solving reframe if stuck.
- Minimal changes. Follow existing patterns.
- Preserve the opening constraints and non-goals.

Mark implementation complete.

**Output:** `Step 3: Implemented - [N] files changed`

## Step 4: Verify + prevent

Mark verify active.

1. **Iron-law verify:** re-run the EXACT commands from the pre-fix capture.
   Compare before/after.
2. **Regression test:** add/update test(s) covering the fix via the **testing**
   capability or the project's test command. The test MUST fail without the fix
   and pass with it.
3. **Side-effect sweep (HARD-GATE-NO-SIDE-EFFECTS):** walk each dependent caller
   of changed functions from the Step 1 blast radius. Run tests in modules that
   share files/contracts. Confirm public contracts (signatures, schemas, APIs,
   env vars) unchanged.
4. **Defense-in-depth:** apply the relevant prevention layers.
5. **Verification commands:** run typecheck, lint, build, and tests through the
   shell; delegate only when the user requested parallel delegation and the
   runtime permits it.

**On regression / side effect:** use the **interactive-prompt** capability with
2-4 concrete options (revert / narrow scope / update dependents / accept). Never
silently patch.

**If verification fails:** loop back to Step 2. Max 3 attempts.

Mark verify complete only after fresh evidence passes.

**Output:** `Step 4: Verified + Prevented - [before/after], [N] tests added, [M] guards`

## Step 5: Code review

Mark review active. Use the **code-review** capability when delegation is
permitted; otherwise review the changed files inline. See
`references/review-cycle.md`. Mark review complete after accepted findings are
resolved.

**Output:** `Step 5: Review [score]/10 - [status]`

## Step 6: Finalize

Mark finalize active.

- Report summary: root cause, changes, prevention measures, confidence.
- Sync plan status and progress through the **task-tracking** capability when
  available; otherwise update the active plan.
- Evaluate docs impact; use the **documentation** capability only for affected
  authority surfaces.
- Ask to commit through the **version-control** capability or git via the shell.
- Optionally record a journal entry through a **journaling** capability.

Mark finalize complete in the live surface when available and in the active plan.

**Output:** `Step 6: Complete - [action]`

## Notes

- Don't skip steps. Validate before proceeding. One phase at a time.
- **Frontend:** verify through a **browser-automation** capability or the
  project's own browser tests.
- **Visual assets:** use a **visual/multimodal** capability for asset
  generation, analysis, and verification.
