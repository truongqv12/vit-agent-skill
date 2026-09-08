---
name: code-review
description: "Review code for correctness, regressions, and production risk with evidence-based findings across pending changes, a PR, a commit, or a full codebase. Use to review diffs, PRs, commits, or codebases before merge."
user-invocable: true
when_to_use: "Invoke to review a diff, a PR, a commit, or a full codebase before merge or completion."
category: dev-tools
keywords: [review, quality, verification, reliability, regressions]
license: MIT
argument-hint: "[#PR | COMMIT | --pending | codebase [parallel]]"
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:code-review"
  source-version: "2.0.0"
  portability: standalone
---

# Code Review

Production-readiness code review with technical rigor, evidence-based claims,
and verification over performative responses. Reviews focus on production risks,
regression paths, and whether the implementation matches the requested change.

## Capability handoff convention

Several steps below name a companion capability (scouting, code-review
delegation, testing, fix/implementation, ship/release, research, planning,
task tracking, or an interactive prompt). Wherever that happens:

> Use the named capability when the runtime exposes it and the user's request
> permits it; otherwise perform that work inline with native tools (read,
> search, shell, git). If neither path is possible, stop and report the missing
> capability honestly. Never emit a hard vendor slash-command or a named
> source-subagent call as the only path.

Delegated or external execution requires explicit user permission. Reviewing is
read-only until the user accepts a fix.

## Input Modes

Auto-detect from arguments. If ambiguous or no arguments, ask the user directly
(use an interactive prompt capability when available; otherwise ask in
conversation).

| Input | Mode | What Gets Reviewed |
|-------|------|--------------------|
| `#123` or PR URL | **PR** | Full PR diff (see PR mode below) |
| `abc1234` (7+ hex chars) | **Commit** | Single commit diff via `git show` |
| `--pending` | **Pending** | Staged + unstaged changes via `git diff` |
| *(no args, recent changes)* | **Default** | Recent changes in context |
| `codebase` | **Codebase** | Full codebase scan |
| `codebase parallel` | **Codebase+** | Parallel multi-reviewer audit |

**Resolution details:** `references/input-mode-resolution.md`

### PR mode is explicit-intent and optional

PR mode uses a GitHub CLI (`gh`) capability. Use it only when the user asked to
review a PR **and** `gh` is available and authenticated. If `gh` is not present,
fall back to native git: fetch the PR branch if needed and review the branch
diff with `git diff <base>...<head>` (or the locally checked-out changes). Never
make `gh` the only path to a review.

### No Arguments

If invoked WITHOUT arguments and no recent changes in context, ask the user what
to review, offering: Pending changes, Enter PR number, Enter commit hash, Full
codebase scan, or Parallel codebase audit.

## Core Principle

**YAGNI**, **KISS**, **DRY** always. Technical correctness over social comfort.
**Be honest, be brutal, straight to the point, and be concise.**

Default assumption: reviewed code may be AI-assisted. Do not trust polished
shape, confident comments, or happy-path tests. Verify behavior, project-rule
compliance, and scope discipline from evidence.

No rubber-stamp reviews. The reviewer is not trying to please the author or
preserve momentum; the reviewer enforces the rulebook and blocks defects,
regressions, hidden scope drift, and AI-slop patterns.

Verify before implementing. Ask before assuming. Evidence before claims.

## Mandatory completion checks (a-e)

Every review MUST confirm all five checks before it reports a change as
complete. These are the contract a downstream implementation/orchestration
capability relies on; state each one explicitly with evidence:

- **(a) Acceptance criteria:** every stated acceptance criterion is met.
- **(b) No regression:** no regression to business logic in the touchpoints or
  the blast radius of the change.
- **(c) No breaking changes:** no breaking changes to public contracts —
  function signatures, exported types, API responses, database schemas,
  environment variables, config keys — unless the change explicitly called them
  out and the user accepted that scope.
- **(d) Follows existing patterns:** the change follows the patterns and
  conventions already present in the codebase.
- **(e) No new errors:** no new lint, type, or build errors anywhere, verified
  with fresh command output (see Verification Gates).

A failing check blocks completion until fixed and re-verified.

## Findings format

Findings are evidence-based and honest — no false positives, no rubber-stamping.

- **Evidence:** every finding cites `file:line` and states the concrete problem
  and a concrete fix. No `file:line` and reproduction path → not a blocking
  finding.
- **Severity tiers:**
  - **Critical** — bugs, security defects, regressions, breaking contract
    changes. Block completion/merge until fixed and re-verified.
  - **Warning** — real problems that should be fixed but do not block on their
    own (maintainability, reliability gaps, missing tests).
  - **Suggestion** — optional improvements; never gate on these.
- **Score:** end with a score out of 10 reflecting production readiness (10 =
  ship-ready, no critical or warning findings).
- **No false positives:** apply the suppression discipline in
  `references/checklists/base.md`; read the full diff before flagging anything;
  skip anything that is already fine.

## Practices

| Practice | When | Reference |
|----------|------|-----------|
| **Spec compliance** | After implementing from plan/spec, BEFORE quality review | `references/spec-compliance-review.md` |
| Receiving feedback | Unclear feedback, external reviewers, needs prioritization | `references/code-review-reception.md` |
| Requesting review | After tasks, before merge, stuck on problem | `references/requesting-code-review.md` |
| Verification gates | Before any completion claim, commit, PR | `references/verification-before-completion.md` |
| Edge case scouting | After implementation, before review | `references/edge-case-scouting.md` |
| **Checklist review** | Pre-landing, ship/release pipeline, security audit | `references/checklist-workflow.md` |
| **Tracked reviews** | Multi-file features (3+ files), parallel reviewers, fix cycles | `references/task-management-reviews.md` |

## Quick Decision Tree

```
SITUATION?
│
├─ Input mode? → Resolve diff (references/input-mode-resolution.md)
│   ├─ #PR / URL → fetch PR diff (gh capability, explicit + optional; git fallback)
│   ├─ commit hash → git show
│   ├─ --pending → git diff (staged + unstaged)
│   ├─ codebase → full scan (references/codebase-scan-workflow.md)
│   ├─ codebase parallel → parallel audit (references/parallel-review-workflow.md)
│   └─ default → recent changes in context
│
├─ Received feedback → STOP if unclear, verify if external, implement if human partner
├─ Completed work from plan/spec:
│   ├─ Stage 1: Spec compliance review (references/spec-compliance-review.md)
│   │   └─ PASS? → Stage 2 │ FAIL? → Fix → Re-review Stage 1
│   ├─ Stage 2: Code quality review (code-review delegation or inline)
│   │   └─ Scout edge cases → Review standards, performance
│   └─ Verification gate → Run required tests/builds before claims
├─ Completed work (no plan) → Scout → Code quality → Verification
├─ Pre-landing / ship → Load checklists → Two-pass review → Verification
├─ Multi-file feature (3+ files) → Track review pipeline (scout→review→fix→verify)
└─ About to claim status → RUN verification command FIRST
```

### Review Protocol

**Stage 1 — Spec Compliance** (load `references/spec-compliance-review.md`)
- Does code match what was requested?
- Any missing requirements? Any unjustified extras?
- MUST pass before Stage 2

**Stage 2 — Code Quality** (code-review delegation capability, else inline)
- Only runs AFTER spec compliance passes
- Standards, security, performance, edge cases

**Final Verification**
- Runs AFTER Stage 2 passes
- Re-run the relevant tests, build, lint, or manual reproduction
- Verify accepted findings are fixed and no new regression is introduced
- Critical findings block merge until fixed and re-verified

## Receiving Feedback

**Pattern:** READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT
No performative agreement. Verify before implementing. Push back if wrong.

**Full protocol:** `references/code-review-reception.md`

## Requesting Review

**When:** After each task, major features, before merge

**Process:**
1. **Scout edge cases first** (see below)
2. Get SHAs: `BASE_SHA=$(git rev-parse HEAD~1)` and `HEAD_SHA=$(git rev-parse HEAD)`
3. Run a code-quality review over the diff with: WHAT, PLAN, BASE_SHA, HEAD_SHA,
   DESCRIPTION — via a code-review delegation capability when available,
   otherwise perform the review inline against the diff.
4. Fix Critical immediately, Warning before proceeding

**Full protocol:** `references/requesting-code-review.md`

## Edge Case Scouting

**When:** After implementation, before requesting a code-quality review

**Process:**
1. Run an edge-case-focused scouting pass — use a scouting capability when
   available, otherwise search and read affected files with native tools.
2. Analyze: affected files, data flows, error paths, boundary conditions
3. Review findings for potential issues
4. Address critical gaps before code review

**Full protocol:** `references/edge-case-scouting.md`

## Tracked Review Pipeline

**When:** Multi-file features (3+ changed files), parallel review scopes, review
cycles with Critical fix iterations.

Discover the live task-management surface at runtime. If available, represent
the `scout → review → fix → verify` dependency chain there. Otherwise, record
the same states in the active plan and run the chain sequentially. Plan files
are the durable source of truth; runtime tracking is only a working view.

**Parallel reviews:** Split independent file groups (e.g., backend + frontend)
into scoped reviews. The fix step blocks on all reviews completing.

**Re-review cycles:** If fixes introduce new issues, add another review cycle.
Limit 3 cycles, then escalate to the user.

**Full protocol:** `references/task-management-reviews.md`

## Verification Gates

**Iron Law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

**Gate:** IDENTIFY command → RUN full → READ output → VERIFY confirms → THEN claim

**Requirements:**
- Tests pass: Output shows 0 failures
- Build succeeds: Exit 0
- Bug fixed: Original symptom passes
- Requirements met: Checklist verified

**Red Flags:** "should"/"probably"/"seems to", satisfaction before verification, trusting agent reports

**Full protocol:** `references/verification-before-completion.md`

## Integration with Workflows

- **Delegated review:** Scout → Review → Verify before next task
- **Pull Requests:** Scout → Code quality → Verify → Merge
- **Tracked Pipeline:** Record dependencies → advance only when prerequisites complete
- **Implementation handoff:** an implementation capability completes a phase →
  this review pipeline completes → implementation proceeds
- **PR Review:** pass a PR number → resolve the PR diff → full review pipeline on PR changes
- **Commit Review:** pass a commit hash → review that commit with the full pipeline

## Codebase Analysis Subcommands

| Subcommand | Reference | Purpose |
|------------|-----------|---------|
| `codebase` | `references/codebase-scan-workflow.md` | Scan & analyze the codebase |
| `codebase parallel` | `references/parallel-review-workflow.md` | Think through edge cases, then parallel verify |

## Bottom Line

1. Resolve input mode first — know WHAT you're reviewing
2. Technical rigor over social performance
3. Scout edge cases before review
4. Evidence before claims
5. Confirm the (a-e) mandatory checks before reporting complete

Verify. Scout. Question. Then implement. Evidence. Then claim.

## Workflow position

**Typically follows:** an implementation capability (review after building), a
fix capability (review after a bug fix).

**Typically precedes:** a ship/release capability (ship after review passes).

**Related:** a scouting capability (scout before reviewing) and a testing
capability (test before reviewing).
