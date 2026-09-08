---
name: scout
description: "Fast, token-efficient codebase scouting to locate files and gather task context. Use for file discovery, codebase orientation, and scoped searches, with native search plus optional parallel agents and user-permitted external probes."
user-invocable: true
when_to_use: "Invoke for fast file discovery and codebase orientation before deeper work."
category: dev-tools
keywords: [codebase, scouting, file-discovery, search, orientation]
license: MIT
argument-hint: "[search-target] [ext]"
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:scout"
  source-version: "1.0.0"
  portability: standalone
---

# Scout

Fast, token-efficient codebase scouting. Find the files a task needs, size the
codebase, and return a concise report. Native search is the always-available
core; parallel agents and external probes are optional accelerators.

## Capability handoff convention

When a step below names a companion capability (parallel agents, external
probe, task tracking, output organization):

- Use that capability **only** when the runtime exposes it and the user's
  request permits it.
- Otherwise perform the step inline with native tools (file read, content
  search, shell).
- If neither path is possible, stop and report the missing capability honestly.

Never treat an optional capability as required, and never mutate anything —
scouting is read-only.

## Arguments

- Default: scout with native search; use parallel agents only when delegation is
  permitted (`./references/internal-scouting.md`).
- `ext`: use user-permitted external probes when native search is insufficient
  (`./references/external-scouting.md`).

## When to use

- Starting work on a feature spanning multiple directories.
- The user needs to "find", "locate", or "search for" files.
- Beginning an investigation that needs file-relationship understanding.
- Understanding project structure or where functionality lives.
- Before changes that might affect multiple parts of the codebase.

## Runtime tooling

Use portable capabilities, native-first:

- File content/name search for local discovery.
- Scoped file reads.
- Shell for local commands such as `rg`, `wc`, or `sed`.
- Optional: a delegation capability for parallel scout agents.
- Optional: a live task-management surface for progress tracking.

Do not spawn agents merely because this skill mentions them. Some runtimes
require the user's request to explicitly ask for subagents, delegation, or
parallel work. If that explicit request is absent, scout in the main agent with
native search and reads.

Delegation discovery: on runtimes where a parallel-agent role is a deferred
tool, discover it through the runtime's tool-search before spawning; do not set
a model override for the scout role. On Claude Code, use the native delegate
call with the `Explore` agent type.

## Workflow

### 1. Analyze the task

- Parse the request for search targets.
- Identify key directories, patterns, file types, and rough scale.
- Decide how many parallel scopes are worthwhile (SCALE).

### 2. Divide and conquer

- Split the codebase into logical, non-overlapping segments.
- Assign each scope specific directories or patterns.
- Maximize coverage, avoid overlap.

### 3. Register scout work (optional)

- Skip when SCALE ≤ 2 (overhead exceeds benefit).
- If a live task-management surface exists, register one scoped item per scope;
  otherwise update the active plan.
- Keep it concise: scope, assigned directories, status, timeout.
- The active plan is the durable source of truth.

### 4. Execute the scopes

Load the matching reference:

- **Internal (default):** `references/internal-scouting.md` — parallel agents
  when delegation is permitted, native search otherwise.
- **External:** `references/external-scouting.md` — user-permitted external
  probes.

Notes:

- Record each scope as in progress before starting it.
- Give each scope exact directories/files and a read-only instruction.
- Keep each agent's context bounded (chunk large files).
- If runtime policy blocks delegation because the user did not request it,
  continue with main-agent scouting instead of forcing a spawn.

### 5. Collect results

- Aggregate findings into a single report; deduplicate paths.
- Organize outputs into the project's expected location; use an output/file
  organization capability if one is available, otherwise place files by the
  project's existing convention.
- Timeout: 3 minutes per agent; skip non-responders and log them.
- List unresolved questions at the end.

## Report format

```markdown
# Scout Report

## Relevant Files
- `path/to/file.ts` - Brief description
- ...

## Unresolved Questions
- Any gaps in findings
```

## References

- `references/internal-scouting.md` — parallel scout agents (delegation-gated).
- `references/external-scouting.md` — user-permitted external probes.

## Workflow position

**Typically precedes:** a diagnosis/debug capability, a fix or implementation
capability, or a review capability (scout edge cases before review).

**Related:** an investigation capability after scouting, or an ideation
capability to explore options once relevant code is located.
