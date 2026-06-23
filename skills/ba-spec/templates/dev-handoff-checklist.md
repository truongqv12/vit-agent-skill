# Dev / QA Handoff Checklist: {{FEATURE_NAME}}

Dùng checklist này trước khi gửi spec cho dev và QA.

Status:

- `Pass`
- `Partial`
- `Fail`
- `N/A`

---

## 1. Độ đầy đủ của requirement

| Check | Status | Notes |
|---|---:|---|
| Business goal đã rõ. | {{Pass/Partial/Fail}} | {{notes}} |
| User roles đã rõ. | {{Pass/Partial/Fail}} | {{notes}} |
| In scope và out of scope đã rõ. | {{Pass/Partial/Fail}} | {{notes}} |
| Main flow đã mô tả từng bước. | {{Pass/Partial/Fail}} | {{notes}} |
| Alternative flows đã có hoặc được mark open. | {{Pass/Partial/Fail}} | {{notes}} |
| Functional requirements có stable IDs. | {{Pass/Partial/Fail}} | {{notes}} |
| Business rules tách khỏi implementation detail. | {{Pass/Partial/Fail}} | {{notes}} |
| Data requirements đã có. | {{Pass/Partial/Fail}} | {{notes}} |
| Validation rules đã có. | {{Pass/Partial/Fail}} | {{notes}} |
| Permission matrix đã có. | {{Pass/Partial/Fail}} | {{notes}} |
| State transitions đã có. | {{Pass/Partial/Fail}} | {{notes}} |
| Edge cases và error handling đã có. | {{Pass/Partial/Fail}} | {{notes}} |
| Acceptance criteria testable. | {{Pass/Partial/Fail}} | {{notes}} |
| NFR cấp BA đã có nếu liên quan. | {{Pass/Partial/Fail/N/A}} | {{notes}} |

---

## 2. Traceability

| Check | Status | Notes |
|---|---:|---|
| Mỗi requirement map được về source hoặc business goal. | {{Pass/Partial/Fail}} | {{notes}} |
| Mỗi acceptance criterion map tới requirement. | {{Pass/Partial/Fail}} | {{notes}} |
| Assumptions được đánh dấu riêng. | {{Pass/Partial/Fail}} | {{notes}} |
| Open questions được đánh dấu riêng. | {{Pass/Partial/Fail}} | {{notes}} |
| Thông tin từ Figma được mark `[FIGMA]`. | {{Pass/Partial/Fail/N/A}} | {{notes}} |
| Thông tin từ file được mark `[FILE]`. | {{Pass/Partial/Fail/N/A}} | {{notes}} |
| Thông tin suy luận được mark `[INFERRED]`. | {{Pass/Partial/Fail}} | {{notes}} |

---

## 3. Checklist riêng cho feature upgrade

| Check | Status | Notes |
|---|---:|---|
| Current behavior đã mô tả. | {{Pass/Partial/Fail/N/A}} | {{notes}} |
| Requested change đã mô tả. | {{Pass/Partial/Fail/N/A}} | {{notes}} |
| Change impact đã mô tả. | {{Pass/Partial/Fail/N/A}} | {{notes}} |
| Affected roles đã mô tả. | {{Pass/Partial/Fail/N/A}} | {{notes}} |
| Affected data/status đã mô tả. | {{Pass/Partial/Fail/N/A}} | {{notes}} |
| Regression risks đã có. | {{Pass/Partial/Fail/N/A}} | {{notes}} |
| Backward compatibility đã xác định hoặc mark open. | {{Pass/Partial/Fail/N/A}} | {{notes}} |

---

## 4. Dev readiness

| Check | Status | Notes |
|---|---:|---|
| Dev biết cần build gì mà không cần hỏi lại scope cơ bản. | {{Pass/Partial/Fail}} | {{notes}} |
| Dev thấy rõ user action và system response. | {{Pass/Partial/Fail}} | {{notes}} |
| Dev thấy rõ state và transition. | {{Pass/Partial/Fail}} | {{notes}} |
| Dev thấy rõ permissions. | {{Pass/Partial/Fail}} | {{notes}} |
| Không có technical assumption vô căn cứ. | {{Pass/Partial/Fail}} | {{notes}} |
| Items chưa implement được liệt kê. | {{Pass/Partial/Fail}} | {{notes}} |

---

## 5. QA readiness

| Check | Status | Notes |
|---|---:|---|
| QA derive được happy-path test cases. | {{Pass/Partial/Fail}} | {{notes}} |
| QA derive được negative test cases. | {{Pass/Partial/Fail}} | {{notes}} |
| QA derive được permission test cases. | {{Pass/Partial/Fail}} | {{notes}} |
| QA derive được state-transition test cases. | {{Pass/Partial/Fail}} | {{notes}} |
| QA verify được error messages/behavior. | {{Pass/Partial/Fail}} | {{notes}} |
| Gherkin scenarios có nếu team cần. | {{Pass/Partial/Fail/N/A}} | {{notes}} |

---

## 6. Quyết định handoff

| Decision | Value |
|---|---|
| Ready for dev? | {{Yes/No/Conditional}} |
| Ready for QA test design? | {{Yes/No/Conditional}} |
| Blocking open questions | {{count_and_ids}} |
| Recommended next action | {{action}} |
