---
name: git
description: "Git operations with conventional commits, secret scanning, and auto-split commits. Use for staging, committing, pushing, pull requests, merges, and release git steps."
user-invocable: true
when_to_use: "Invoke for commits, PRs, branch hygiene, or release git steps."
category: dev-tools
keywords: [git, commits, staging, PR, merge, merge-pr, ci]
license: MIT
argument-hint: "cm|cp|pr|merge|merge-pr [args]"
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:git"
  source-version: "1.1.0"
  portability: standalone
---

# Git Operations

Stage, commit, push, open pull requests, and merge with conventional commits,
a mandatory secret scan, and automatic commit splitting by type and scope.
Native `git` and `gh` are the always-available core; every mutation is
gated on explicit user intent.

## Capability handoff convention

When a step below names a companion capability (interactive prompt, verbose-
output delegation, context-budget tracking, or a fix/debug capability):

- Use that capability **only** when the runtime exposes it and the user's
  request permits it.
- Otherwise perform the step inline with native tools (read, search, shell,
  `git`, `gh`).
- If neither path is possible, stop and report the missing capability honestly.

Never emit a hard vendor slash-command or a named source-subagent call as the
only path, and never treat an optional capability as required.

## Mutation gate (non-negotiable)

Every mutation — commit, push, PR creation, merge, merge-pr, force push,
destructive recovery — requires **explicit user intent**. Default to preview
and confirm: show what will change, then wait for the user to approve. Never
auto-commit or auto-push because a workflow reached that step. `gh` and PR
features are explicit-intent only and must be availability-checked (`gh auth
status`) before use.

## Default (no arguments)

If invoked without arguments, present the available git operations and ask
which to run. Use an interactive-prompt capability when the runtime exposes one
(header "Git Operation", question "What would you like to do?"); otherwise list
them as plain text and wait for the user's choice.

| Operation | Description |
|-----------|-------------|
| `cm` | Stage files & create commits |
| `cp` | Stage files, create commits and push |
| `pr` | Create Pull Request |
| `merge` | Merge branches |
| `merge-pr` | Merge a GitHub PR + watch CI to green |

To keep verbose git output out of the main context, run the workflow through a
delegation capability when one is available; otherwise run the commands inline.
Keep token usage efficient — sacrifice grammar for concision, and pass the same
rules to any delegated worker.

## Arguments

- `cm`: Stage files & create commits
- `cp`: Stage files, create commits and push
- `pr`: Create Pull Request [to-branch] [from-branch]
  - `to-branch`: Target branch (default: main)
  - `from-branch`: Source branch (default: current branch)
- `merge`: Merge [to-branch] [from-branch]
  - `to-branch`: Target branch (default: main)
  - `from-branch`: Source branch (default: current branch)
- `merge-pr`: Merge PR [pr-ref] via `gh`, then watch post-merge CI until green
  and verify
  - `pr-ref`: PR number or URL (required)
  - Readiness-gated: refuses on conflicts, red CI, or `CHANGES_REQUESTED`; uses
    `--auto` when checks are pending

## Quick reference

| Task | Reference |
|------|-----------|
| Commit | `references/workflow-commit.md` |
| Push | `references/workflow-push.md` |
| Pull Request | `references/workflow-pr.md` |
| Merge | `references/workflow-merge.md` |
| Merge PR | `references/workflow-merge-pr.md` |
| Standards | `references/commit-standards.md` |
| Safety | `references/safety-protocols.md` |
| Branches | `references/branch-management.md` |
| GitHub CLI | `references/gh-cli-guide.md` |

## Core workflow

### Step 1: Stage + analyze
```bash
git add -A && git diff --cached --stat && git diff --cached --name-only
```

### Step 2: Security check
Scan for secrets before every commit:
```bash
git diff --cached | grep -iE "(api[_-]?key|token|password|secret|credential)"
```
**If secrets found:** STOP, warn the user, and suggest `.gitignore` or
environment variables. Never commit past a secret hit.

### Step 3: Split decision

**Note:**
- Search for related issues and add them to the body.
- Only use `feat`, `fix`, or `perf` prefixes for files in a `.claude` directory
  (do not use `docs`).

**Split commits if:**
- Different types mixed (feat + fix, code + docs)
- Multiple scopes (auth + payments)
- Config/deps + code mixed
- FILES > 10 unrelated

**Single commit if:**
- Same type/scope, FILES ≤ 3, LINES ≤ 50

### Step 4: Commit
```bash
git commit -m "type(scope): description"
```

Commit messages carry **no AI attribution** — no "Generated with", no
"Co-Authored-By" trailer, no AI reference of any kind.

## Output format
```
✓ staged: N files (+X/-Y lines)
✓ security: passed
✓ commit: HASH type(scope): description
✓ pushed: yes/no
```

## Error handling

| Error | Action |
|-------|--------|
| Secrets detected | Block commit, show files |
| No changes | Exit cleanly |
| Push rejected | Suggest `git pull --rebase` |
| Merge conflicts | Suggest manual resolution |

## References

- `references/workflow-commit.md` - Commit workflow with split logic
- `references/workflow-push.md` - Push workflow with error handling
- `references/workflow-pr.md` - PR creation with remote diff analysis
- `references/workflow-merge.md` - Branch merge workflow
- `references/workflow-merge-pr.md` - PR merge with post-merge CI watch and verification
- `references/commit-standards.md` - Conventional commit format rules
- `references/safety-protocols.md` - Secret detection, branch protection
- `references/branch-management.md` - Naming, lifecycle, strategies
- `references/gh-cli-guide.md` - GitHub CLI commands reference

## Workflow position

**Typically the finalize step** after implementation and review: stage, scan,
commit, and (on explicit request) push or open a PR. Pairs with any review
capability upstream and a fix/debug capability when post-merge CI fails.
