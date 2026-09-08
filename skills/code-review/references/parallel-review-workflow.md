# Parallel Review Workflow

Exhaustively list ALL potential edge cases for the given scope, then verify them
across parallel review scopes.

Each companion capability below (scouting, code-review delegation, fix, git) is
used when the runtime exposes it and the user permits it; otherwise perform that
step inline with native tools (read, search, shell, git). Ensure token
efficiency. Sacrifice grammar for concision.

## Workflow

### 1. List Edge Cases

Deeply analyze the scope to LIST all potential edge cases FIRST:
- Read repository instructions and follow the existing documentation navigation
  to find applicable requirements, architecture, and standards
- Use a scouting capability to find relevant files; otherwise search natively
- Confirm documentation claims against current source and tests in the review scope
- Think exhaustively about what could go wrong:
  - Null/undefined scenarios
  - Boundary conditions (off-by-one, empty, max values)
  - Error handling gaps
  - Race conditions, async edge cases
  - Input validation holes
  - Trust-boundary defects
  - Resource leaks
  - Untested code paths

**Output format:**
```markdown
## Edge Cases Identified

### Category: [scope-area]
1. [edge case description] → files: [file1, file2]
```

### 2. Categorize & Assign

Group edge cases by similar scope for parallel verification:
- Each category → one review scope
- Max 6 categories (merge small ones)
- Each scope gets specific edge cases to VERIFY, not discover

### 3. Parallel Verification

Verify the N categories in parallel — through a code-review delegation
capability when available, otherwise sequentially inline:
- Pass: category name, list of edge cases, relevant files
- Task: **VERIFY** whether each edge case is properly handled in code
- Report: which edge cases are handled vs unhandled, with `file:line` evidence

### 4. Aggregate Results

```markdown
## Edge Case Verification Report

### Summary
- Total edge cases: X
- Handled: Y
- Unhandled: Z
- Partial: W

### Unhandled Edge Cases (Need Fix)
| # | Edge Case | File | Status |
|---|-----------|------|--------|
```

### 5. Verification Review

After aggregation, verify accepted findings against the full scope:
- Re-check aggregated findings and unhandled edge cases
- Confirm each blocking issue has a concrete file/line and reproduction path
- Classify findings as Accept / Reject / Defer

### 6. Auto-Fix Pipeline

**IF** unhandled/partial edge cases found:
- Ask the user whether to fix them now — apply fixes through a fix/implementation
  capability when available, otherwise fix inline. Delegated fixes require the
  user's permission.

### 7. Final Report
- Summary of verification, with `file:line` evidence and a score out of 10
- Ask the user whether to commit — use a git capability when available,
  otherwise commit with native `git`.
