# Push Workflow

Run inline, or through a delegation capability to isolate verbose output when
one is available. Push only on explicit user intent.

## Pre-push checklist
1. All changes committed
2. Secrets scanned (see `safety-protocols.md`)
3. Branch pushed to remote

## Step 1: Verify state
```bash
git status && \
git log origin/$(git rev-parse --abbrev-ref HEAD)..HEAD --oneline 2>/dev/null || echo "NO_UPSTREAM"
```

**If uncommitted changes:** Warn the user, suggest commit first.
**If NO_UPSTREAM:** Use `git push -u origin HEAD`.

## Step 2: Push
```bash
git push origin HEAD
```

**On success:** Report commit hashes pushed.

## Error handling

| Error | Cause | Solution |
|-------|-------|----------|
| `rejected - non-fast-forward` | Remote has newer commits | `git pull --rebase`, resolve conflicts, push again |
| `no upstream branch` | Branch not tracked | `git push -u origin HEAD` |
| `Authentication failed` | Invalid credentials | Check `gh auth status` or SSH keys |
| `Repository not found` | Wrong remote URL | Verify `git remote -v` |
| `Permission denied` | No write access | Check repository permissions |

## Force push (DANGER)

**NEVER force push to main/master/production branches.**

If the user explicitly requests force push on a feature branch:
```bash
git push -f origin HEAD
```

**Warn the user:** "Force push rewrites history. Collaborators may lose work."

## Output format
```
✓ pushed: N commits to origin/{branch}
  - abc123 feat(auth): add login
  - def456 fix(api): resolve timeout
```
