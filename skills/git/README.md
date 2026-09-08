# git

Git operations with conventional commits, secret scanning, and auto-split
commits. [`SKILL.md`](./SKILL.md) is the authority for behavior; this README
carries provenance and dependency notes.

## Provenance

- Source skill: `ak:git` v1.1.0 (author: agentkit, MIT).
- Normalized into this repo per `docs/portable-skill-contract.md`.
- Canonical identity: folder and frontmatter `name` are both `git`.

## Dependencies

- **standalone.** Core operations work with native `git` (stage, commit, push,
  branch, merge) plus content search and shell.

Optional accelerators (each with a native fallback):

- The `gh` GitHub CLI for pull-request and PR-merge workflows. Absent or
  unauthenticated → skip PR/merge-pr steps and report; use `git` for local
  operations. Check with `gh auth status` before use.
- A delegation capability to isolate verbose git output from the main context.
  Absent → run the commands inline.
- An interactive-prompt capability for the no-argument operation menu. Absent →
  present the options as plain text and wait for the user's choice.
- A context-budget/token-tracking capability for long sessions. Absent → keep
  output concise natively.
- A fix/debug capability for post-merge CI failures (`merge-pr` Step 5). Absent
  → diagnose and fix inline with native tools.

All mutations (commit, push, PR, merge, merge-pr, force push, destructive
recovery) require **explicit user intent**; the default is preview and confirm.
`gh` and PR features are explicit-intent and availability-checked.

## Preserved invariants

- Conventional commit format; commits auto-split by type/scope.
- Mandatory secret scan before every commit; a hit blocks the commit.
- No AI-attribution footers or co-author trailers in commit messages.
- Remote-first diffs for PR and merge (`origin/...`), never local WIP.
- Never force push to `main`/`master`/`production`/`prod`/`release/*`.
- `merge-pr` readiness gate refuses on conflicts, red CI, or
  `CHANGES_REQUESTED`.
- Confirm with the user before any destructive operation.

## References

- [`references/workflow-commit.md`](./references/workflow-commit.md) — commit workflow with split logic.
- [`references/workflow-push.md`](./references/workflow-push.md) — push workflow with error handling.
- [`references/workflow-pr.md`](./references/workflow-pr.md) — PR creation with remote diff analysis.
- [`references/workflow-merge.md`](./references/workflow-merge.md) — branch merge workflow.
- [`references/workflow-merge-pr.md`](./references/workflow-merge-pr.md) — PR merge with post-merge CI watch and verification.
- [`references/commit-standards.md`](./references/commit-standards.md) — conventional commit format rules.
- [`references/safety-protocols.md`](./references/safety-protocols.md) — secret detection, branch protection.
- [`references/branch-management.md`](./references/branch-management.md) — naming, lifecycle, strategies.
- [`references/gh-cli-guide.md`](./references/gh-cli-guide.md) — GitHub CLI commands reference.
