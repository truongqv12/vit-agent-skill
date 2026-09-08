---
name: debug
description: "Debug systematically and prove root cause before any fix. Use for bugs, test failures, unexpected behavior, performance issues, call-stack tracing, multi-layer validation, log analysis, CI/CD failures, database diagnostics, and system investigation."
user-invocable: true
when_to_use: "Invoke when the root cause of a bug, failure, or incident must be proven with evidence before a fix is applied."
category: dev-tools
keywords: [debug, root-cause, bugs, test-failures, investigation, diagnostics]
license: MIT
argument-hint: "[error or issue description]"
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:debug"
  source-version: "4.0.0"
  portability: standalone
---

# Debug

Systematic debugging and system investigation. Prove the root cause with
evidence, then hand a structured diagnosis to whoever applies the fix. This
skill diagnoses; it does not mutate behavior.

## Core principle

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Random fixes waste time and create new bugs. Find the root cause, locate it at
the source, understand the failing layers, and verify every claim with fresh
evidence. Diagnosis is the deliverable; behavior changes belong to the caller
(an implementation or fix capability).

## Capability handoff convention

Some steps below name a companion capability (scouting, docs lookup, codebase
packing, browser verification, fix/implementation, ideation, task tracking):

- Use that capability **only** when the runtime exposes it and the user's
  request permits it.
- Otherwise perform the step inline with native tools (file read, content
  search, shell).
- If neither path is possible, stop and report the missing capability honestly.

Never treat an optional capability as required, and never emit a hard,
runtime-specific command or a named subagent as the only path. Debugging never
depends on a particular client's tooling.

## When to use

- **Code-level:** test failures, bugs, unexpected behavior, build failures,
  integration problems.
- **System-level:** server errors, CI/CD pipeline failures, performance
  degradation, database issues, log analysis.
- **Always:** before claiming any work complete, fixed, or passing.

## Techniques

Load only the reference the current case needs.

### 1. Systematic debugging (`references/systematic-debugging.md`)

Four-phase framework: Root Cause Investigation -> Pattern Analysis ->
Hypothesis Testing -> Implementation guidance. Complete each phase before the
next. No fix proposals without Phase 1.

**Load when:** any bug or issue requiring investigation.

### 2. Root cause tracing (`references/root-cause-tracing.md`)

Trace bugs backward through the call stack to the original trigger. Fix at the
source, not the symptom. Includes an optional `scripts/find-polluter.sh` for
bisecting test-state pollution.

**Load when:** the error is deep in the call stack, or it is unclear where
invalid data originated.

### 3. Defense-in-depth (`references/defense-in-depth.md`)

Describe validation at every layer data passes through so the recommended fix
makes the bug structurally impossible: entry validation, business logic,
environment guards, debug instrumentation.

**Load when:** the root cause is found and the recommended fix needs
comprehensive validation guidance.

### 4. Verification (`references/verification.md`)

**Iron law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. Run the
command, read the output, then state the result.

**Load when:** about to claim work complete, fixed, or passing.

### 5. Investigation methodology (`references/investigation-methodology.md`)

Five-step investigation for system-level issues: Initial Assessment -> Data
Collection -> Analysis -> Root Cause Identification -> Solution Development.

**Load when:** server incidents, system behavior analysis, or multi-component
failures.

### 6. Log & CI/CD analysis (`references/log-and-ci-analysis.md`)

Collect and analyze logs from servers, CI/CD pipelines (GitHub Actions via the
`gh` CLI), and application layers; correlate across sources.

**Load when:** CI/CD pipeline failures, server errors, deployment issues.

### 7. Performance diagnostics (`references/performance-diagnostics.md`)

Identify bottlenecks, analyze query performance, develop optimization
strategies across network, application, database, filesystem, and external
dependencies.

**Load when:** performance degradation, slow queries, high latency, resource
exhaustion.

### 8. Reporting standards (`references/reporting-standards.md`)

Structured diagnostic report: Executive Summary -> Technical Analysis ->
Recommendations -> Evidence -> Unresolved Questions.

**Load when:** producing an investigation report or diagnostic summary.

### 9. Investigation tracking (`references/task-management-debugging.md`)

For multi-step investigations, track dependencies, ownership, and parallel
evidence collection on a live task-management surface when one exists;
otherwise update the active plan. Plan files are the durable source of truth.

**Load when:** multi-component investigation (3+ steps), parallel log
collection, or coordinating parallel evidence gathering.

### 10. Frontend verification (`references/frontend-verification.md`)

Visual verification of frontend diagnoses through whatever browser-automation
capability the runtime exposes, or the project's own browser tests. Detect
whether the issue is frontend-related, capture a screenshot, check console
errors, and report. Skip entirely when the issue is not frontend.

**Load when:** the issue touches frontend files (tsx/jsx/vue/svelte/html/css),
UI bugs, or visual regressions.

## Quick reference

```
Code bug       → systematic-debugging.md (Phase 1-4)
  Deep in stack  → root-cause-tracing.md (trace backward)
  Found cause    → defense-in-depth.md (validation layers for the fix)
  Claiming done  → verification.md (verify first)

System issue   → investigation-methodology.md (5 steps)
  CI/CD failure  → log-and-ci-analysis.md
  Slow system    → performance-diagnostics.md
  Need report    → reporting-standards.md

Frontend issue → frontend-verification.md (browser-automation capability)
```

## Tooling

Use portable capabilities, native-first:

- **Codebase search/read:** native content and name search plus scoped file
  reads to locate relevant code and evidence.
- **Shell:** local commands for reproduction, log capture, and inspection.
- **Database:** `psql` for PostgreSQL queries and diagnostics when a database
  is in scope.
- **CI/CD:** the `gh` CLI for GitHub Actions logs and pipeline debugging.
- **Optional — file discovery:** a scouting capability to locate relevant files
  when context is missing; otherwise native search.
- **Optional — docs lookup:** a documentation-lookup capability for
  package/plugin docs; otherwise read the project's own docs and sources.
- **Optional — codebase packing:** a repository-packing capability for a broad
  snapshot only when it materially helps; otherwise scoped reads.
- **Optional — browser verification:** a browser-automation capability for
  frontend visual checks; otherwise the project's browser tests, or skip and
  note it.

## Red flags

Stop and return to the systematic process if thinking:

- "Quick fix for now, investigate later."
- "Just try changing X and see if it works."
- "It's probably X, let me fix that."
- "Should work now" / "Seems fixed."
- "Tests pass, we're done."

## Workflow position

**Typically follows:** a scouting/discovery capability that located the
relevant code.

**Typically precedes:** a fix or implementation capability that applies the
diagnosed fix, or an ideation capability to explore solutions for complex
problems. This skill produces the diagnosis; it does not apply the fix itself.
