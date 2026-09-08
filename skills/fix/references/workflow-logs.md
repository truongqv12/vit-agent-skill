# Log Analysis Fix Workflow

For fixing issues found in application logs.

## Prerequisites

- A log file at `./logs.txt` or a project-specific equivalent.

## Setup when logs are missing

Add persistent log piping to the project configuration:

- **Bash/Unix:** `command 2>&1 | tee logs.txt`
- **PowerShell:** `command *>&1 | Tee-Object logs.txt`

## Progress tracking

The stages are `analyze logs -> scout code -> plan fix -> implement -> test ->
review`. Use a live **task-tracking** capability to mirror this dependency chain
when available; otherwise update the active plan as stages start and finish.
Plan files are the durable source of truth.

## Workflow

### Step 1: Read and analyze logs

- Read the logs with native search; start with a small result limit.
- Use the **debugging** capability for root-cause analysis, or reason inline.
- Inspect recent lines first.
- Capture stack traces, error codes, timestamps, and repeated patterns.

### Step 2: Scout the codebase

Use the **scouting** capability, or parallel exploration agents when permitted,
to find the affected code. See `references/parallel-exploration.md`.

### Step 3: Plan the fix

Use a **planning** capability, or write the plan inline. Do not plan until the
log evidence and code paths agree on the root cause.

### Step 4: Implement

Implement the smallest cause-aligned fix.

### Step 5: Test

Use the **testing** capability, or run the project's test command. If the
original symptom remains, return to Step 2 before changing more code.

### Step 6: Review

Use the **code-review** capability, or review the diff inline, and retain fresh
verification evidence.

## Tips

- Focus on the most recent errors first.
- Correlate stack traces, error codes, and timestamps.
- Group repeated errors before forming hypotheses.
