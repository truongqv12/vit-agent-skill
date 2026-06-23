# Feature Upgrade Rules

Apply when the input includes:

- Existing spec.
- Current behavior.
- Change request.
- User says “nâng cấp”, “sửa”, “bổ sung”, “thay đổi”, “upgrade”, “change request”.

## Required upgrade sections

Add these sections to the spec:

1. Hành vi hiện tại.
2. Thay đổi yêu cầu.
3. Phạm vi ảnh hưởng.
4. Role bị ảnh hưởng.
5. Data/state bị ảnh hưởng.
6. Business rules bị ảnh hưởng.
7. Backward compatibility.
8. Regression risks.
9. Migration or transition notes, if applicable.

## Comparison table

Use this format:

```markdown
| ID | Khu vực | Hiện tại | Sau thay đổi | Tác động / rủi ro |
|---|---|---|---|---|
| CHG-001 | ... | ... | ... | ... |
```

## Preservation rule

If old requirement IDs exist, preserve them. Add new IDs only for new/changed requirements.

## Do not assume

Do not infer old behavior from the new request unless it is explicitly described. If missing, add an open question.
