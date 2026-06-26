# BA Documentation Principles

Apply these Business Analyst practices when producing a feature spec.

## 1. Requirement classification

Separate the following:

| Type | Meaning | Example |
|---|---|---|
| Business goal | Why the feature exists | Rút ngắn thời gian xử lý hồ sơ công chứng. |
| Stakeholder requirement | What stakeholder needs | CCV cần kiểm tra chữ ký số trước khi ký. |
| Functional requirement | What the system shall do | Hệ thống phải cho phép NVNV khởi tạo giao dịch. |
| Business rule | Constraint or decision logic | Chỉ chuyển CCV ký khi tất cả người yêu cầu đã ký. |
| Data requirement | Business data needed | CCCD, họ tên, loại văn bản, file văn bản công chứng. |
| Validation rule | Input/action constraint | Lý do từ chối là bắt buộc khi từ chối. |
| Permission rule | Who can do what | CCV được phê duyệt trình ký. |
| NFR | Quality expectation at BA level | Thao tác ký cần có audit log. |
| Transition/change requirement | Needed for upgrade/migration | Dữ liệu giao dịch cũ phải giữ trạng thái hiện tại. |

## 2. Elicitation discipline

When input is incomplete:

- Ask only blocking questions first.
- Do not ask more than 10 questions in one turn.
- If the user asks for best-effort output, proceed and mark gaps.

## 3. Workflow modelling

For every workflow, capture:

- Trigger.
- Actor.
- User action.
- System response.
- Resulting state.
- Alternative flow.
- Exception/error flow.

## 4. Business rule modelling

A business rule must be:

- Atomic.
- Testable.
- Source-tagged.
- Not mixed with implementation.

Example:

```text
BR-001: Giao dịch chỉ được chuyển sang bước CCV ký khi tất cả người yêu cầu công chứng đã hoàn tất ký số. [INFERRED]
```

If this is not explicitly provided, add an open question.

## 5. State modelling

Define:

- State name.
- Meaning.
- Entry trigger.
- Exit trigger.
- Actor.
- Terminal or not.

Never invent state names as confirmed facts. If state names are inferred, tag them `[INFERRED]` or `[ASSUMPTION]`.

## 6. Acceptance criteria

Acceptance criteria must be testable.

Use checklist for simple requirements.
Use Gherkin for decision-heavy flows:

```gherkin
Scenario: CCV phê duyệt trình ký
  Given giao dịch công chứng đã được NVNV lưu thông tin và vị trí ký
  When CCV chọn phê duyệt trình ký
  Then hệ thống chuyển giao dịch sang bước người yêu cầu công chứng ký số
```

## 7. Traceability

Map each important source/goal to requirements, business rules, acceptance criteria, and QA focus.

Do not leave high-priority requirements untraced.

## 8. UI elements: catalog selects, never guess buttons

When documenting UI from screenshots or descriptions:

- **Select / dropdown:** record the visible option catalog (the list of values). If the full catalog is not visible, write down what is seen and raise a `UIQ-###` asking for the complete catalog. Do not fabricate options.
- **Buttons / icons / controls with unclear purpose:** do not infer behavior. List them as `UIQ-###` UI open questions and ask.
- Collect all `UIQ-###` items into a dedicated "UI Open Questions" section (separate from business `Q-###`), each with the screen, the element, what is seen, and what must be clarified.

Guessing a select catalog or a button's action is a defect. When unsure, ask via `UIQ-###`.
