# Merge Workflow

Run inline, or through a delegation capability to isolate verbose output when
one is available. Merge and push only on explicit user intent.

## Variables
- TO_BRANCH: target (defaults to `main`)
- FROM_BRANCH: source (defaults to current branch)

## Step 1: Sync with remote

**IMPORTANT: Always merge `main` (or any default branch) to the current branch first.**

```bash
git fetch origin
git checkout {TO_BRANCH}
git pull origin {TO_BRANCH}
```

## Step 2: Merge from REMOTE
```bash
git merge origin/{FROM_BRANCH} --no-ff -m "merge: {FROM_BRANCH} into {TO_BRANCH}"
```

**Why `origin/{FROM_BRANCH}`:** Ensures merging only committed+pushed changes, not local WIP.

## Step 3: Resolve conflicts
If conflicts:
1. Resolve manually
2. `git add . && git commit`
3. If clarifications are needed, report back before proceeding

## Step 4: Push
```bash
git push origin {TO_BRANCH}
```

## Pre-merge checklist
- Fetch latest: `git fetch origin`
- Ensure FROM_BRANCH is pushed to remote
- Check for conflicts: `git merge --no-commit --no-ff origin/{FROM_BRANCH}` then abort

## Error handling

| Error | Action |
|-------|--------|
| Merge conflicts | Resolve manually, then commit |
| Branch not found | Verify branch name, ensure pushed |
| Push rejected | `git pull --rebase`, retry |
