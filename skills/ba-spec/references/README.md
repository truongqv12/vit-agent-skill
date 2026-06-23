# ba-spec References

These files contain case-specific operating rules. `SKILL.md` is intentionally short and acts as the router.

Read only the files relevant to the current task:

| Trigger | Read |
|---|---|
| Every task | `input-classification.md`, `output-packaging-rules.md`, `workspace-hygiene-rules.md`, `source-confidence-and-evidence.md`, `ba-documentation-principles.md`, `spec-generation-workflow.md`, `quality-gates.md` |
| Figma URL or screenshot exists | `figma-mcp-gate.md`, `figma-link-reference-rules.md` |
| Related files exist | `file-handling-rules.md` |
| Existing spec/change request exists | `feature-upgrade-rules.md` |
| HTML output requested | `html-rendering-rules.md` |
| Any user-facing output | `output-language-rules.md` |

Do not copy all reference content into the generated spec. Apply the rules and generate concise Vietnamese deliverables.

- `output-packaging-rules.md`: package folder naming, Epic/Story/feature slug convention, final deliverable layout.
- `workspace-hygiene-rules.md`: temporary scripts/files must live in tmp and be deleted before final response.
- `figma-link-reference-rules.md`: preserve clickable Figma links in specs and evidence logs.
