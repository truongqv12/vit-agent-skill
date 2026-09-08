---
name: journal
description: "Write a concise chronological technical journal of a work session — decisions, difficulties, and lessons learned — so work history is preserved. Invoke on explicit request for session reflection or a chronological work record."
user-invocable: true
when_to_use: "Invoke on explicit request for technical session reflection or a chronological work record."
category: utilities
keywords: [journal, reflection, changes, session, work-history]
license: MIT
argument-hint: "[topic or reflection]"
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:journal"
  source-version: "1.0.0"
  portability: standalone
---

# Journal

Write a concise, chronological technical journal of a work session: the key
events, changes, decisions, difficulties, and lessons learned. A journal
preserves work history — it is **not** current product or decision authority.

## Explicit intent only

This skill writes a file to the repository. Invoke it only on the user's
explicit request for a journal or session reflection. Do not auto-fire it after
shipping, implementing, or fixing.

## Capability handoff convention

When a step below names a companion capability (exploring memory/change history,
organizing outputs, or publishing/sharing the entry):

- Use that capability **only** when the runtime exposes it and the user's
  request permits it.
- Otherwise perform the step inline with native tools (file read, content
  search, shell — e.g. `git log`, `git diff`).
- If neither path is possible, stop and report the missing capability honestly.

Never emit a hard runtime command or a named source-subagent call as the only
path.

## Workflow

### 1. Gather the material

Explore recent code changes and session memory to find what matters. Use a
change-history or memory-exploration capability when one is available and the
user permits it; otherwise gather natively with scoped file reads and shell
(`git log`, `git diff`, `git status`). A dedicated journaling subagent is one
example of such a capability, not a requirement.

### 2. Select what to record

Keep entries concise and focused on the most important:

- Events and key changes, with their impact.
- Decisions made, and the difficulties encountered.
- Lessons learned.

Convert any relative dates (e.g. "yesterday", "last week") to absolute
calendar dates so the record stays accurate when read later.

### 3. Write the entry

- Write to this repository's journal location: `plans/journals/`.
- Follow the existing naming convention in that directory
  (`plans/journals/*.md`).
- Mark the entry as work history — not current product or decision authority.
  Record durable decisions in the project's ADR or current documentation owner
  instead.

### 4. Organize and (optionally) publish

- Place the output in the project's expected location. Use an output/file
  organization capability if one is available; otherwise follow the project's
  existing convention.
- If a publishing or sharing capability (wiki, knowledge base, or similar) is
  available and the user permits it, publish/share the entry through it.
  Otherwise report that publishing was skipped.

## Invariants

- Chronological technical record of decisions, difficulties, and lessons.
- Relative dates are converted to absolute dates.
- Journals preserve work history; they do **not** replace current docs or ADRs.
- Output lives in `plans/journals/` per this repo's convention.
- Invocation is explicit-intent because it writes a file.

## Workflow position

**Typically follows:** a shipping, implementation, or bug-fix capability —
journal the session after the work completes.

**Terminal:** no typical successor.
