---
name: research
description: "Research technical solutions, evaluate architectures, and gather requirements into a concise, evidence-cited report. Use for technology evaluation, best-practice research, and solution design before implementation."
user-invocable: true
when_to_use: "Invoke for deep, evidence-first technical research before a decision or implementation."
category: dev-tools
keywords: [research, evaluation, analysis, synthesis, requirements]
license: MIT
argument-hint: "[topic]"
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:research"
  source-version: "1.0.0"
  portability: standalone
---

# Research

Turn a topic into strategic technical intelligence: define scope, gather
evidence from multiple sources, synthesize, and return a concise cited report.
Local evidence (repo, docs, shell) is the always-available core; web and
docs-lookup capabilities are optional accelerators.

**Be honest, be concise, straight to the point.** Honor YAGNI, KISS, and DRY.

## Capability handoff convention

When a step below names a companion capability (web search, docs lookup, output
organization):

- Use that capability **only** when the runtime exposes it and the user's
  request permits it.
- Otherwise perform the step inline with native tools (file read, content
  search, shell).
- If neither path is possible, stop and report the missing capability honestly.

Never treat an optional capability as required, and never emit a fixed vendor
command or a named source-subagent call as the only path.

## When to use

- Evaluating a technology, library, or architecture before committing.
- Gathering best practices, security posture, or performance characteristics.
- Comparing multiple solutions or approaches for a decision.
- Establishing requirements or design constraints ahead of implementation.

## Runtime tooling

Use portable capabilities, native-first:

- File content/name search and scoped reads for local evidence (existing code,
  docs, ADRs, configs, changelogs, lockfiles).
- Shell for local inspection (`rg`, dependency/version checks).
- **Optional:** a web search capability for current external sources.
- **Optional:** a documentation-lookup capability for library/API/GitHub docs.

**Offline core:** when no web or docs-lookup capability is available, the
research still completes using local evidence alone and produces a cited report
against local sources. Do not block on the network.

## Methodology

### Phase 1 — Scope

- Identify key terms, concepts, and the concrete question to answer.
- Set recency requirements and source-quality criteria.
- Bound the depth so the effort matches the decision at stake.

### Phase 2 — Gather (multi-source, evidence-first)

- Start with local evidence: search and read the repo, docs, and configs that
  bear on the question. Every claim must trace to a source you can cite.
- Use the web search capability for current external research when available and
  permitted. Run independent queries in parallel if the runtime supports it, and
  keep discovery bounded (about 5 external lookups; respect any lower user
  limit). Prioritize official docs, primary repositories, and recognized
  authorities.
- Use the documentation-lookup capability to read a specific library, API, or
  GitHub source when one is available; otherwise read the source directly with
  native fetch/search or fall back to local evidence.
- Cross-reference across independent sources; note consensus versus contested
  points and check publication dates for currency.
- **Mark gaps explicitly.** When a source is unavailable, a claim is unverified,
  or the network is absent, say so in the report rather than guessing.

### Phase 3 — Synthesis

- Identify patterns and best practices across sources.
- Weigh pros and cons, maturity, security, and performance.
- Derive concrete, actionable recommendations for the question asked.

### Phase 4 — Report

Produce a single markdown report, **capped at about 150 lines**, every
substantive claim carrying a citation. Prefer concision over completeness; drop
sections that do not apply.

```markdown
# Research Report: [Topic]

_Conducted: [YYYY-MM-DD]_

## Executive Summary
[2-3 tight paragraphs: findings + recommendation.]

## Key Findings
- [Finding] — [source/citation]
- ...

## Comparative Analysis
[Only when comparing options: brief table or bullets, each row cited.]

## Recommendations
- [Actionable next step, tied to a finding.]

## Sources
- [Title / repo / doc] — [URL or local path]

## Gaps & Unresolved Questions
- [Anything unavailable, unverified, or out of scope.]
```

Rules:

- Cite every substantive claim (URL for external, path for local).
- Sacrifice grammar for concision; use fenced code blocks and, where a diagram
  genuinely helps, mermaid or ASCII.
- End with unresolved questions and any marked gaps.

## Output location

Save the report to the path the caller specifies (for example a `Report:` path
in a provided naming or plan section). If no path is given, ask the main agent
where it belongs. Organize outputs into the project's expected location using an
output/file organization capability when one is available; otherwise place the
file by the project's existing convention. Use a descriptive filename.

## Quality standards

- **Accuracy:** claims verified across sources; unverified items marked.
- **Currency:** prefer material from the last ~12 months unless history matters;
  for security topics check recent advisories/CVEs.
- **Attribution:** every finding cites its source.
- **Actionability:** recommendations are concrete and implementable.

## Workflow position

**Typically precedes:** an ideation/brainstorm capability, a planning
capability, or an implementation capability once the approach is chosen.

**Related:** a scouting capability to locate local code before research, or a
review capability to validate a chosen solution afterward.
