# Related File Handling Rules

Apply when the user provides or references files.

## Extraction rules

1. Identify file type and likely purpose.
2. Extract relevant business facts only.
3. Mark facts as `[FILE]`.
4. Preserve source identity in evidence log.
5. Detect conflicts between files and user text.
6. Do not expand technical detail beyond what the file states.
7. If the file embeds screenshots/diagrams (`.docx`/`.pptx`/`.pdf`), extract them per `file-image-extraction-rules.md`, copy into the package `assets/`, pair each with its caption, and tag `[FILE]`. Never ignore embedded UI screenshots in a UI/flow spec.

## File evidence log

```markdown
| ID | File | Loại file | Nội dung đã dùng | Ghi chú |
|---|---|---|---|---|
| FILE-001 | ... | PDF | ... | ... |
```

## Conflict handling

If file says one thing and user text says another:

- Add a conflict row.
- Do not silently pick one.
- Ask which source is authoritative unless one source is clearly newer and user asked to use latest.
