# Source Confidence and Evidence Rules

## Tags

Use these tags exactly:

- `[PROVIDED]`: directly stated by the user.
- `[FIGMA]`: extracted from Figma screenshot/link/MCP.
- `[FILE]`: extracted from a related file.
- `[INFERRED]`: logically inferred from supplied evidence.
- `[ASSUMPTION]`: assumed only to make a draft usable; requires confirmation.
- `[OPEN_QUESTION]`: unresolved question affecting scope, behavior, testability, or implementation.

## Evidence discipline

1. Do not write unsupported details as facts.
2. Do not treat Figma UI labels as confirmed business rules.
3. Every business rule must have a source tag.
4. Every inferred behavior must be traceable to a provided fact, file, or Figma observation.
5. Every assumption must include impact if wrong.
6. Every open question must have a category and blocking flag.

## Required evidence log

When Figma links or related files exist, include an evidence section:

```markdown
## Nhật ký bằng chứng

| ID | Nguồn | Trạng thái xử lý | Bằng chứng trích xuất | Ảnh hưởng đến spec |
|---|---|---|---|---|
| EVD-001 | User text | Đã xử lý | ... | ... |
| EVD-002 | Figma link | MCP success / MCP unavailable / Failed / Skipped by user | ... | ... |
```

## Conflict handling

If sources conflict:

- Do not silently choose one.
- Add `CONFLICT-###` row in the evidence log.
- Add an `[OPEN_QUESTION]` asking which source is authoritative.
