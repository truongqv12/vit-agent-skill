# Skill Architecture Research Notes

This document records why `ba-spec` uses a short `SKILL.md` plus `references/` rule files.

## Observed patterns

### Angular `angular-developer`

The Angular skill keeps high-level routing in `SKILL.md` and points the agent to topic-specific files under `references/`, such as components, inputs, outputs, routing, testing, CLI, and MCP. This keeps the entrypoint readable while letting the agent load deeper context only when the task requires it.

Pattern to copy for `ba-spec`:

- Use `SKILL.md` as router.
- Use references for task-specific rules.
- Tell the agent exactly which reference to read for each case.

### Vercel `agent-skills`

Vercel's collection describes a skill as containing:

- `SKILL.md` for agent instructions.
- Optional `scripts/` for automation.
- Optional `references/` for supporting documentation.

Some Vercel skills, such as React best practices and React Native skills, list categories in `SKILL.md` and place expanded rule files under `rules/` or compiled documents such as `AGENTS.md`. The `vercel-optimize` skill is stricter: it defines a deterministic pipeline and says not to inspect source files until required evidence artifacts exist.

Pattern to copy for `ba-spec`:

- Add hard gates for evidence-sensitive steps.
- Do not let the agent silently fall back when evidence is unavailable.
- Require generated evidence artifacts before the final deliverable.

## Design decision for ba-spec v1.1

`SKILL.md` should not contain every rule. It should contain:

1. Trigger description.
2. Mandatory output language rule.
3. Mandatory workflow.
4. Figma hard gate.
5. Reference routing table.
6. Final response contract.

Detailed rules should live in `references/`:

| Reference | Purpose |
|---|---|
| `input-classification.md` | Detect business text, Figma link, files, change request. |
| `figma-mcp-gate.md` | Force MCP probe/extraction/failure evidence before spec generation. |
| `source-confidence-and-evidence.md` | Evidence log and confidence tagging. |
| `ba-documentation-principles.md` | BA analysis rules. |
| `spec-generation-workflow.md` | Markdown generation process. |
| `html-rendering-rules.md` | Tailwind HTML rendering rules. |
| `feature-upgrade-rules.md` | Upgrade/change impact rules. |
| `file-handling-rules.md` | Related file extraction rules. |
| `quality-gates.md` | Final checks. |
| `output-language-rules.md` | Vietnamese output enforcement. |

## Why this solves the Figma issue

The previous version said Figma MCP should be used “if available,” but did not require proof that the agent attempted it. Some agents therefore skipped MCP and still claimed they used Figma.

The new version makes Figma a hard gate:

- Any Figma URL triggers `figma-mcp-gate.md`.
- The agent must record `MCP_SUCCESS`, `MCP_UNAVAILABLE`, `MCP_FAILED`, `USER_SKIPPED`, or `SCREENSHOT_ONLY`.
- The spec must include a `Nhật ký bằng chứng Figma` section.
- The final response must report Figma link counts by outcome.

This does not guarantee every host agent will have Figma MCP tools, but it prevents silent false claims.
