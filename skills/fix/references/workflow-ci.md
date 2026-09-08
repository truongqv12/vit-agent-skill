# CI/CD Fix Workflow

For GitHub Actions failures and CI/CD pipeline issues.

## Prerequisites

- The `gh` CLI installed and authenticated, plus the failing run ID or URL. If
  `gh` is unavailable, read the pipeline logs the CI provider exposes and
  reproduce the failing step locally instead.

## Workflow

1. **Fetch logs.** Use the **debugging** capability, or read the logs directly:

   ```bash
   gh run view <run-id> --log-failed
   gh run view <run-id> --log
   ```

2. **Analyze** the root cause from the logs (HARD-GATE-EXACT-ROOT-CAUSE).

3. **Implement** the smallest cause-aligned fix.

4. **Test locally** through the **testing** capability, or run the project's
   test command directly, before pushing.

5. **Iterate.** If tests fail, return to step 3.

## Notes

- If `gh` is unavailable, instruct the user to install and run `gh auth login`,
  or supply the logs another way.
- Check both the failed step and the preceding steps for context.
- Common causes: env vars, dependencies, permissions, timeouts.
