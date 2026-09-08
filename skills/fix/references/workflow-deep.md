# Deep Workflow

Full pipeline with research, ideation, and planning for complex issues. Use a
live **task-tracking** capability for dependency tracking when the runtime
exposes one; otherwise update the active plan. Plan files are the durable source
of truth.

The parent skill's opening intent frame is already satisfied. The ideation in
this route is a later solution decision grounded in diagnosis; it does not
replace or repeat the opening contract.

## Plan setup (before starting)

Record phase dependencies upfront. Scout + diagnose + research may run in
parallel when the runtime permits the needed delegation.

- Scout codebase.
- Diagnose root cause.
- Research solutions.
- Compare approaches, blocked by scout + diagnose + research.
- Create implementation plan, blocked by the approach decision.
- Implement fix, blocked by the plan.
- Verify + prevent, blocked by implementation.
- Code review, blocked by verification.
- Finalize & docs, blocked by review.

## Step 1: Scout codebase (parallel with Steps 2+3)

Mark scout active. Use the **scouting** capability, or launch 2-3 parallel
exploration agents when delegation is permitted; otherwise scan natively. Map
all affected files, module boundaries, call chains, and test-coverage gaps. See
`references/parallel-exploration.md`. Mark complete after evidence is captured.

**Output:** `Step 1: Scouted - [N] files, system impact: [scope]`

## Step 2: Diagnose root cause (parallel with Steps 1+3)

Mark diagnose active.

1. **Capture pre-fix state:** ALL error messages, failing tests, stack traces,
   logs.
2. Use the **debugging** capability (systematic investigation + call-stack
   tracing); otherwise reason through the evidence inline.
3. Form hypotheses through structured reasoning.
4. Test hypotheses with parallel exploration agents only when delegation is
   permitted.
5. If 2+ hypotheses fail, switch to a structured problem-solving reframe.
6. Trace backward through the call chain to the root-cause origin.

Use the root-cause checklist in the parent skill. Mark complete after the root
cause is proven.

**Output:** `Step 2: Diagnosed - Root cause: [summary], Evidence: [chain]`

## Step 3: Research (parallel with Steps 1+2)

Mark research active. Use a **research** capability only when delegation is
explicitly requested/permitted; otherwise read the project's docs and sources
and search inline.

- Search current docs and best practices.
- Find similar issues/solutions.
- Gather security advisories if relevant.

Mark complete after relevant evidence is retained.

**Output:** `Step 3: Research complete - [key findings]`

## Step 4: Compare approaches

Mark this active after scout, diagnosis, and research are complete. Use an
**ideation** capability to evaluate approaches; otherwise weigh them inline.

- Use scout + diagnosis + research findings.
- Consider trade-offs.
- Compare each option with the opening constraints, non-goals, and acceptance
  criteria.
- Resolve the preferred direction; explicit `--auto` mode may adopt the
  documented recommendation without a routine pause.

Mark complete after the direction is resolved.

**Output:** `Step 4: Approach selected - [chosen approach]`

## Step 5: Plan

Mark planning active. Use a **planning** capability only when delegation is
explicitly requested/permitted; otherwise write the plan locally.

- Break down into phases.
- Identify dependencies.
- Define success criteria.
- Include prevention measures.

Mark complete after the durable plan is written.

**Output:** `Step 5: Plan created - [N] phases`

## Step 6: Implement

Mark implementation active. Implement per plan; apply a structured
problem-solving reframe when stuck, and a **context-engineering** capability when
fixing AI/LLM/agent code.

- Fix the ROOT CAUSE per diagnosis — not symptoms.
- Follow plan phases. Minimal changes per phase.

Mark complete.

**Output:** `Step 6: Implemented - [N] files, [M] phases`

## Step 7: Verify + prevent

Mark verification active.

1. **Iron-law verify:** re-run EXACT commands from the pre-fix capture. Compare
   before/after.
2. **Regression test:** add comprehensive tests via the **testing** capability
   or the project's test command. Tests MUST fail without the fix and pass with
   it.
3. **Side-effect sweep (HARD-GATE-NO-SIDE-EFFECTS):** walk each dependent caller
   from the Step 1 blast radius. Run tests in modules that share
   files/contracts. Confirm public contracts unchanged.
4. **Defense-in-depth:** apply all relevant prevention layers.
5. **Verification commands:** run typecheck + lint + build + test through the
   shell; delegate only when explicitly requested/permitted.
6. **Edge cases:** test boundary conditions, security implications, performance
   impact.

**On regression / side effect:** use the **interactive-prompt** capability with
2-4 concrete options (revert / narrow scope / update dependents / accept). Never
silently patch.

**If verification fails:** loop back to Step 2. Max 3 attempts, then question
the architecture.

Mark complete only after fresh evidence passes.

**Output:** `Step 7: Verified + Prevented - [before/after], [N] tests, [M] guards`

## Step 8: Code review

Mark review active. Use the **code-review** capability only when delegation is
explicitly requested/permitted; otherwise review locally. See
`references/review-cycle.md`. Mark complete after accepted findings are
resolved.

**Output:** `Step 8: Review [score]/10 - [status]`

## Step 9: Finalize

Mark finalization active.

- Report summary: root cause, evidence chain, changes, prevention measures,
  confidence.
- Sync plan status and progress through the **task-tracking** capability when
  available; otherwise update the active plan.
- Evaluate docs impact; use the **documentation** capability only for affected
  authority surfaces, and the **version-control** capability only when
  explicitly requested/permitted.
- Optionally record a journal entry through a **journaling** capability.

Mark complete in the live surface when available and in the active plan.

**Output:** `Step 9: Complete - [actions taken]`

## Notes

- Don't skip steps. Validate before proceeding. One phase at a time.
- **Frontend:** verify through a **browser-automation** capability or the
  project's own browser tests.
- **Visual assets:** use a **visual/multimodal** capability for asset
  generation, analysis, and verification.
