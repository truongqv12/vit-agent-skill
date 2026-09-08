# Unified Workflow Steps

All modes share core steps with mode-specific variations.

**Runtime progress contract:** discover the live task-management surface and use
it when available. Otherwise, update the active plan directly. Plan files are the
durable source of truth, and every workflow step must work without runtime task
tracking.

Every companion capability below follows the Capability Handoff Convention: use
the capability when available and permitted; otherwise do the step inline with
native tools; if neither is possible, stop and report honestly.

## Step 0: Brainstorm Contract, Intent Detection & Setup

1. Capture outcome, constraints, non-goals, and acceptance criteria. Reuse them
   from an accepted plan or design when present.
2. Resolve only material gaps; routine approval is unnecessary in explicit auto
   mode when the contract is already concrete.
3. Parse input with `intent-detection.md` rules.
4. If mode=code: detect plan path, set active plan, retain its accepted
   brainstorm contract.
5. For three or more meaningful steps, mirror progress into the live
   task-management surface when available.

**Output:** concise brainstorm contract plus detected workflow mode and reason.

## Step 1: Research (skip if fast/code mode)

**Interactive/Auto:**
- Use the `research` capability (parallel researchers if delegation exists;
  sequential otherwise).
- Use the `scout` capability for codebase search.
- Keep reports ≤150 lines.
- Evaluate findings against the opening outcome and constraints.

**Parallel:** optional; at most 2 research passes if complex.

**Output:** `✓ Step 1: Research complete - [N] reports gathered`

### [Review Gate 1] Post-Research (skip if auto mode)
- Present the research summary.
- Ask (interactive prompt capability or plainly): "Proceed to planning?" / "Request more research" / "Abort".
- **Auto mode:** skip this gate.

## Step 2: Planning

**Interactive/Auto/No-test:** use the `vit-plan` capability with research
context; create `plan.md` + `phase-XX-*.md` files.

**Fast:** use `vit-plan` in a fast mode with scout results only; minimal
planning, focus on action.

**Parallel:** use `vit-plan` in a parallel mode for a dependency graph + file
ownership matrix.

**Code:** skip — plan already exists; parse it for phases.

**Output:** `✓ Step 2: Plan created - [N] phases`

### [Review Gate 2] Post-Plan (skip if auto mode)
- Present the plan overview with phases.
- Ask: "Validate the plan / Approve to start implementation / Abort / Request revisions".
  - "Validate": run the `vit-plan` validation workflow.
  - "Approve": continue to implementation.
  - "Abort": stop.
  - "Request revisions": revise per feedback.
- **Auto mode:** skip this gate.

## Step 3: Implementation

**IMPORTANT:**
1. Read the active plan before trusting session state.
2. Discover the live task-management surface and compare any existing view with the plan.
3. If the view is absent or stale, rebuild it from unchecked plan items when supported.
4. Preserve phase order, dependencies, ownership, and source-plan mapping; otherwise track them in the active plan.

### Conformance Checklist (before writing code)

Before implementing each phase, the developer MUST:

1. **Read repository instructions and the routed project docs** relevant to this change; do not assume a standard docs filename exists.
2. **Scout adjacent code patterns** in the files being modified and follow the same import, logging, and error-wrapping style.
3. **Check for existing helpers** before creating new utilities (DRY).
4. **Verify interface contracts** so new code extends the current surface instead of creating a parallel one.
5. **Cross-check the plan checklist** so every file in the phase inventory is addressed.

After each file is modified:
- **Compile check:** run the relevant project compile/type-check command.
- **Pattern verify:** confirm the new code matches adjacent conventions.
- **Import check:** confirm no circular dependency or dead import was added.

### `--tdd` Flag Behavior

When `--tdd` is active, Step 3 splits per phase:

```
Step 3.T: Write tests for CURRENT behavior (regression safety net)
Step 3.I: Implement changes (refactor, new code)
Step 3.V: Verify all tests from 3.T still pass + compile gates
```

If any 3.T test fails after 3.I, the refactor broke something and must be fixed
before proceeding.

**All modes:**
- Record the current item as active through the live task-management surface when available; otherwise update the active plan.
- Execute phase tasks sequentially (Step 3.1, 3.2, …).
- Use a UI/design capability for frontend work; a media/image capability for image assets.
- Run type checking after each file.

**Parallel mode:**
- Discover the live task-management surface before using it.
- Launch parallel implementation agents via the delegation capability when
  present; otherwise implement sequentially with the same ownership graph.
- Record ownership and active state through the live capability or active plan.
- Respect file ownership boundaries; wait for the parallel group before the next.

**Output:** `✓ Step 3: Implemented [N] files - [X/Y] tasks complete`

### Step 3.S: Conditional Simplify (live-diff gated)

Recompute signals from the live worktree (no hidden hook state):

```bash
totals=$(git diff --numstat HEAD --ignore-all-space)
loc=$(echo "$totals" | awk '{s+=$1+$2} END {print s+0}')
files=$(echo "$totals" | awk 'NF{c++} END {print c+0}')
maxFile=$(echo "$totals" | awk 'BEGIN{m=0} {if ($1>m) m=$1} END {print m+0}')
modified=$(git diff --name-only HEAD)
```

Compare against thresholds — defaults **400 LOC / 8 files / 200 single-file
LOC**. A project MAY override these through its own kit configuration; if no
override is present, use the defaults. If any threshold is breached, run the
simplification capability scoped to the modified files:

> Simplify these files while preserving behavior exactly: [file-list]

After it returns, log only — never re-run or block:
- `git diff --shortstat HEAD -- [file-list]` changed → "simplifier made scoped edits"
- unchanged → "simplifier ran clean"

Skip the step entirely when the project disables the simplify gate in its kit
configuration, or when no simplification capability is available.

**Output:** `✓ Step 3.S: Simplify [ran|skipped] - [scoped changes|clean|under threshold]`

### [Review Gate 3] Post-Implementation (skip if auto mode)
- Present the implementation summary (files changed, key changes).
- Ask: "Proceed to testing?" / "Request implementation changes" / "Abort".
- **Auto mode:** skip this gate.

## Step 4: Testing (skip if no-test mode)

**All modes (except no-test):**
- Write tests: happy path, edge cases, errors.
- **MUST** run the `test` capability to execute the suite.
- If failures: **MUST** use the `debug` capability → fix → repeat.
- **Forbidden:** fake mocks, commented tests, changed assertions, or skipping the test gate.

**Output:** `✓ Step 4: Tests [X/X passed] - test capability invoked`

### [Review Gate 4] Post-Testing (skip if auto mode)
- Present the test-results summary.
- Ask: "Proceed to code review?" / "Request test fixes" / "Abort".
- **Auto mode:** skip this gate.

## Step 5: Code Review

**All modes — MANDATORY:**
- **MUST** run the `code-review` capability with explicit (a-e) checks and scout/acceptance context:

  > Review changes against these MANDATORY checks: (a) every acceptance criterion met; (b) no regression to business logic in touchpoints/blast-radius from scout; (c) no breaking changes to public contracts (signatures, schemas, APIs, env vars) unless explicitly called out; (d) follows existing patterns from scout; (e) no new lint/type/build errors anywhere. CONTEXT — scout summary: <scout-summary>; acceptance criteria: <acceptance-criteria>. Return score (X/10), critical, warnings, suggestions, and explicitly flag any side effects to trigger HARD-GATE-NO-SIDE-EFFECTS.

- **DO NOT** skip review; if no review capability exists, perform the (a-e) review inline with native tools.

**Interactive/Parallel/Code/No-test:** interactive cycle (max 3), see `review-cycle.md`; requires user approval.
**Auto:** apply the auto-mode decision from `review-cycle.md`; auto-fix critical (max 3 cycles); escalate to user after 3 failed cycles.
**Fast:** simplified review, no fix loop; user approves or aborts.

**Output:** `✓ Step 5: Review [score]/10 - [Approved|Auto-approved] - code-review invoked`

## Step 6: Finalize

**All modes — finalize contract:**
1. **MUST** use the `project-management` capability — run full sync-back for [plan-path]: reconcile completed work with all phase files, backfill stale completed checkboxes across every phase, then update `plan.md` frontmatter/table progress. Do NOT only mark the current phase. Native fallback: edit plan/phase checkboxes directly.
2. Evaluate docs impact using the installed documentation-management routing. If an authority surface changed, use the `docs` capability with the changed contract, evidence, and exact routed docs in scope. Do not issue a generic whole-corpus refresh.
3. Project-management sync-back MUST include the Status Sync below.

### Status Sync (Finalize)

Prefer the `vit-plan` helper (`lint`/`status`) or the live task capability when
available; otherwise edit `plan.md` directly — change only the Status column
cell, preserve table structure.

   - Sweep all `phase-XX-*.md` files in the plan directory.
   - Mark every completed item `[ ] → [x]` based on completed tasks (including earlier phases finished before the current phase).
   - Update `plan.md` status/progress (`pending`/`in-progress`/`completed`) from actual checkbox state.
   - Return unresolved mappings if any completed task cannot be matched to a phase file.
4. After sync-back confirmation, reflect completion in the live task-management surface when available.
5. Onboarding check (API keys, env vars).
6. **MUST** ask the user, then commit via the `git` capability.
7. Use the `journal` capability to write a concise technical journal entry.

**CRITICAL:** Step 6 is incomplete without project-management sync-back, an
explicit docs-impact decision, and the configured git approval flow.

**Auto mode:** continue to the next phase automatically, starting from **Step 3**.
**Others:** ask the user before the next phase.

**Output:** `✓ Step 6: Finalized - sync-back completed - Committed`

## Mode-Specific Flow Summary

Legend: `[R]` = Review Gate (human approval required)

```
interactive: 0 → 1 → [R] → 2 → [R] → 3 → [R] → 4 → [R] → 5(user) → 6
auto:        0 → 1 → 2 → 3 → 4 → 5(auto) → 6 → next phase (NO stops)
fast:        0 → skip → 2(fast) → [R] → 3 → [R] → 4 → [R] → 5(simple) → 6
parallel:    0 → 1? → [R] → 2(parallel) → [R] → 3(multi-agent) → [R] → 4 → [R] → 5(user) → 6
no-test:     0 → 1 → [R] → 2 → [R] → 3 → [R] → skip → 5(user) → 6
code:        0 → skip → skip → 3 → [R] → 4 → [R] → 5(user) → 6
```

**Key difference:** `auto` mode is the ONLY mode that skips all review gates.

## Critical Rules

- Never skip steps without mode justification.
- **MANDATORY:** Steps 4, 5, 6 must run through their capability or native fallback. DO NOT skip.
  - Step 4: `test` (and `debug` if failures)
  - Step 5: `code-review`
  - Step 6: `project-management`, conditional `docs`, `git`
- Discover the live task-management surface before using runtime tracking.
- If available, mirror unchecked plan items and keep their status current.
- If unavailable, update the active plan directly; plan files remain authoritative.
- All step outputs follow the format: `✓ Step [N]: [status] - [metrics]`.
- **VALIDATION:** if the test, review, and finalize gates did not run, the workflow is INCOMPLETE.
