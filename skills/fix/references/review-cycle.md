# Review Cycle

Mode-aware handling of code-review results. Run the review through the
**code-review** capability when available; otherwise review the diff inline. Use
the **interactive-prompt** capability for any escalation.

## Autonomous mode

```
cycle = 0
LOOP:
  1. Run the review -> score, critical_count, warnings, suggestions

  2. IF score >= 9.5 AND critical_count == 0:
     -> "Review [score]/10 - Auto-approved"
     -> PROCEED to next step

  3. ELSE IF critical_count > 0 AND cycle < 3:
     -> "Auto-fixing [N] critical issues (cycle [cycle+1]/3)"
     -> Fix critical issues -> re-run tests -> cycle++, GOTO LOOP

  4. ELSE IF cycle >= 3:
     -> ESCALATE via the interactive-prompt capability
     -> Display findings
     -> Options: "Fix manually" / "Approve anyway" / "Abort"

  5. ELSE (score < 9.5, no critical):
     -> "Review [score]/10 - Approved with [N] warnings"
     -> PROCEED (warnings logged, not blocking)
```

## Human-in-the-loop mode

```
ALWAYS:
  1. Run the review -> score, critical_count, warnings, suggestions

  2. Display findings:
     Review: [score]/10
       Critical ([N]): [list]
       Warnings ([N]): [list]
       Suggestions ([N]): [list]

  3. Prompt (interactive-prompt capability):
     IF critical_count > 0:
       - "Fix critical issues" / "Fix all issues" / "Approve anyway" / "Abort"
     ELSE:
       - "Approve" / "Fix warnings/suggestions" / "Abort"

  4. Handle response:
     - Fix    -> implement, re-test, re-review (max 3 cycles)
     - Approve -> proceed
     - Abort   -> stop workflow
```

## Quick mode review

Same logic as autonomous, but:

- Lower threshold: score >= 8.5 acceptable.
- Only 1 auto-fix cycle before escalation.
- Focus on correctness, security, no regressions.

## Critical issues (always block)

- Security vulnerabilities (XSS, SQL injection, OWASP).
- Performance bottlenecks (O(n^2) when O(n) is possible).
- Architectural violations.
- Data-loss risks.
- Breaking changes without migration.
