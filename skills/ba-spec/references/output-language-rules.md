# Output Language Rules

## Default language

All user-facing deliverables must be written in Vietnamese unless the user explicitly requests another language.

Use Vietnamese for:

- Section names.
- Business descriptions.
- User stories.
- Functional requirements.
- Business rules.
- Acceptance criteria.
- Assumptions.
- Open questions.
- Clarification questions.
- Dev/QA notes.
- HTML visible text.

Keep these items in English for machine readability:

- Requirement IDs: `FR-001`, `BR-001`, `AC-001`, etc.
- Confidence tags: `[PROVIDED]`, `[FIGMA]`, `[FILE]`, `[INFERRED]`, `[ASSUMPTION]`, `[OPEN_QUESTION]`.
- File names unless the user requests localization.
- Gherkin keywords may remain `Given`, `When`, `Then`, `And`.

## Vietnamese writing style

Prefer concise BA language:

- “Hệ thống phải…” for mandatory system behavior.
- “Người dùng có thể…” for user capability.
- “Không được…” for prohibition.
- “Khi… thì…” for conditional rules.
- “Cần xác nhận…” for unresolved items.

Avoid vague phrasing:

- “xử lý phù hợp”
- “vân vân”
- “tùy trường hợp” without listing cases
- “nếu cần” without owner/condition

## Do not translate tags

Correct:

```text
Hệ thống phải ghi nhận trạng thái giao dịch là `approved`. [PROVIDED]
```

Incorrect:

```text
Hệ thống phải ghi nhận trạng thái giao dịch là `approved`. [ĐÃ_CUNG_CẤP]
```
