---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements - runs a code-quality review of the implementation against plan or requirements before proceeding
---

# Requesting Code Review

Run a code-quality review to catch issues before they cascade.

**Core principle:** Scout first, review often.

Use a **code-review delegation** capability (e.g. a reviewer subagent) when the
runtime exposes it and the user permits delegation; otherwise perform the review
inline against the diff with native read/search tools. Never make a named
subagent the only path.

## When to Request Review

**Mandatory:**
- After each task in delegated/subagent-driven development
- After completing a major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing a complex bug

## How to Request

**0. Scout edge cases first:**
```
Before the quality review, scout to find:
- Files affected by changes (not just modified files)
- Data flow paths that could break
- Edge cases and boundary conditions
- Potential side effects

Use a scouting capability when available; otherwise search and read the
affected files with native tools. See: references/edge-case-scouting.md
```

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Run the code-quality review:**

Provide the reviewer (delegated or inline) with this context:

- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{DESCRIPTION}` - Brief summary

The reviewer evaluates the `BASE_SHA..HEAD_SHA` diff against the plan and the
checklists, and returns findings with `file:line` evidence and severity
(critical / warning / suggestion).

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Warning issues before proceeding
- Note Suggestions for later
- Push back if the reviewer is wrong (with reasoning)

## Example

```
[Just completed task 2: Add verification function]

Let me run a code review before proceeding.

BASE_SHA=$(git log --oneline | grep "task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Review the BASE_SHA..HEAD_SHA diff]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Findings]:
  Strengths: Clean architecture, real tests
  Issues:
    Warning: Missing progress indicators
    Suggestion: Magic number (100) for reporting interval
  Assessment: Ready to proceed after Warning fix

[Fix progress indicators]
[Continue to task 3]
```

## Integration with Workflows

**Delegated / subagent-driven development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to the next task

**Executing plans:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**Ad-hoc development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Warning issues
- Argue with valid technical feedback

**If the reviewer is wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification
