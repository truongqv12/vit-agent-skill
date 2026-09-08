# Test Execution Workflow

All commands below are examples of common runners. Use the command the
**project** actually defines (from its config/manifests). If the runner cannot
be determined from project configuration, report an honest failure and ask for
the command — do not guess.

## Step 1: Identify scope

Determine what to test based on recent changes:

- New feature → full test suite + new test cases.
- Bug fix → regression tests + targeted fix validation.
- Refactor → existing test suite (no new tests unless gaps found).
- Coverage check → full suite with coverage flags.

## Step 2: Pre-flight checks

Run syntax/type checks before tests to catch compile errors early:

```bash
# JavaScript/TypeScript
npx tsc --noEmit          # TypeScript check
npx eslint .              # Lint check

# Python
python -m py_compile file.py
flake8 .

# Flutter
flutter analyze

# Go
go vet ./...

# Rust
cargo check
```

## Step 3: Execute tests

### JavaScript/TypeScript
```bash
npm test                    # or yarn test / pnpm test / bun test
npm run test:coverage       # with coverage
npx vitest run              # Vitest
npx jest --coverage         # Jest with coverage
```

### Python
```bash
pytest                      # basic
pytest --cov=src --cov-report=term-missing  # with coverage
python -m unittest discover # unittest
```

### Go / Rust / Flutter
```bash
go test ./... -cover        # Go with coverage
cargo test                  # Rust
flutter test --coverage     # Flutter
```

## Step 4: Analyze results

Focus on:

1. **Failing tests** — read error messages and stack traces carefully.
2. **Flaky tests** — pass/fail intermittently; indicates race conditions or
   state leaks.
3. **Slow tests** — identify bottlenecks (>5s per test is suspicious).
4. **Skipped tests** — ensure skips are pre-existing and intentional, not hiding
   failures. Never add a skip to make a suite pass (see Anti-cheat in SKILL.md).

## Step 5: Coverage analysis

Thresholds (use the project's own thresholds when defined):

- **80%+** line coverage — common minimum.
- **70%+** branch coverage — acceptable for most projects.
- Focus on critical paths: auth, payment, data mutations.

Identify gaps:

- Uncovered error handlers.
- Missing edge-case branches.
- Untested utility functions.

## Step 6: Build verification

```bash
npm run build               # JS/TS production build
python setup.py build       # Python
go build ./...              # Go
cargo build --release       # Rust
flutter build               # Flutter
```

Check for:

- Build warnings or deprecation notices.
- Unresolved dependencies.
- Production config correctness.

## Quality checklist

- [ ] All tests pass (zero failures).
- [ ] Coverage meets the project threshold.
- [ ] No flaky tests detected.
- [ ] Build completes without errors.
- [ ] Error scenarios tested.
- [ ] Test isolation verified (no shared state).
- [ ] Test data cleaned up after execution.
- [ ] Mocks/stubs are legitimate, not cheats to bypass behavior under test.
- [ ] Environment variables correctly set.
