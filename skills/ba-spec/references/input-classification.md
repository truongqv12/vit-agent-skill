# Input Classification Rules

At the start of every task, classify input into these categories:

| Category | Meaning |
|---|---|
| `business_text` | Natural-language business requirement, workflow, policy, or stakeholder note. |
| `figma_screenshot` | Screenshot/exported image from Figma. |
| `figma_link` | Any URL containing `figma.com`. |
| `related_files` | Uploaded/referenced Markdown, PDF, spreadsheet, HTML, text, ticket, PRD, meeting note, API note. |
| `existing_spec` | Old feature spec or current behavior documentation. |
| `change_request` | Request to modify an existing behavior. |
| `unclear_input` | Input too small, conflicting, or missing critical details. |

## Required generated section

Every generated spec must include a Vietnamese `Tóm tắt đầu vào` section:

```markdown
## Tóm tắt đầu vào

| Loại đầu vào | Có? | Ghi chú |
|---|---:|---|
| Business text | Có/Không | ... |
| Figma screenshot | Có/Không | ... |
| Figma link | Có/Không | ... |
| Related files | Có/Không | ... |
| Existing spec | Có/Không | ... |
| Change request | Có/Không | ... |
| Unclear input | Có/Không | ... |
```

## Classification behavior

- If at least one Figma URL exists, set `figma_link = Có` and trigger the Figma MCP evidence gate.
- If the user provides a business workflow with numbered steps, treat it as `business_text` and extract flow steps.
- If the user provides both an old spec and requested changes, treat as `feature_upgrade` unless they say it is a new feature.
- If input is very small but user asks to proceed, create a draft with assumptions and open questions.
