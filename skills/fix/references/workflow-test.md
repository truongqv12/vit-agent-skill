# Test Failure Fix Workflow

For fixing failing tests and test-suite regressions.

## Progress tracking

The stages are `collect failures -> diagnose -> plan -> implement -> retest ->
review`. Use a live **task-tracking** capability to mirror this dependency chain
when available; otherwise update the active plan. Plan files are the durable
source of truth.

## Workflow

### Step 1: Compile and collect failures

Use the **testing** capability, or run the suite directly. Fix syntax or
compilation errors before running behavior tests. Run the relevant suite,
collect every failure, and group failures by module or likely shared cause.

### Step 2: Diagnose

Use the **debugging** capability, or reason inline. Analyze each failure group
and prove shared root causes before modifying code.

### Step 3: Plan

Use a **planning** capability, or plan inline. Prioritize shared root causes
first and record dependencies between fixes.

### Step 4: Implement

Implement fixes in dependency order and keep changes cause-aligned.

### Step 5: Retest

Use the **testing** capability, or run the suite directly. Start with the narrow
failing test, then broaden across the blast radius. If tests still fail, return
to Step 2.

### Step 6: Review

Use the **code-review** capability, or review inline, and retain fresh test
evidence.

## Common commands

```bash
npm test
bun test
pytest
go test ./...
```

## Tips

- Run one failing test first for faster iteration.
- Compare assertions with intended behavior.
- Verify fixtures and mocks represent real contracts.
- Change a test only when evidence proves the test is wrong.
