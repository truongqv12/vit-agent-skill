# Mode Selection

Choose a fix mode at the start of the workflow through the **interactive-prompt**
capability when the mode is not explicit or safely inferable; otherwise ask in
conversation.

## Prompt shape

Offer three options for "How should I handle the fix workflow?":

- **Autonomous (recommended)** — auto-approve when quality is high, ask only
  when stuck.
- **Human-in-the-loop** — pause for approval at each major step.
- **Quick fix** — fast diagnose-fix-review cycle for simple issues.

Single-select.

## Mode recommendations

| Issue type | Recommended mode |
|------------|------------------|
| Type errors, lint errors | Quick |
| Single-file bugs | Quick or Autonomous |
| Multi-file, unclear root cause | Autonomous |
| Production/critical code | Human-in-the-loop |
| System-wide / architecture | Human-in-the-loop |
| Security vulnerabilities | Human-in-the-loop |

## Skip mode selection when

- The issue is clearly trivial (type-error keyword detected) -> default Quick.
- The user explicitly specified a mode in the request.
- Previous context already established the mode.
