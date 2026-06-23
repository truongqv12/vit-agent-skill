# BA Practice Research cho `ba-spec`

Tài liệu này tóm tắt phần research về kỹ năng BA thực tế dùng để thiết kế template output của skill.

## 1. Năng lực BA nền tảng cần encode vào skill

Theo IIBA, business analysis không chỉ là ghi lại yêu cầu. BA phải lập kế hoạch approach, làm việc với stakeholder, elicitation, quản lý vòng đời requirement, strategy analysis, requirement analysis/design definition, solution evaluation và dùng các kỹ thuật như business rules analysis, process modelling, data dictionary, roles and permissions matrix, state modelling, use cases, user stories, reviews, prioritization.

Nguồn:

- IIBA Business Analysis Standard: https://www.iiba.org/knowledgehub/the-business-analysis-standard/
- BABOK Requirements Classification Schema: https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/2-business-analysis-key-concepts/2-3-requirements-classification-schema/

## 2. Requirement classification

Skill phải phân biệt các loại thông tin sau:

| Nhóm | Ý nghĩa trong spec | Cách thể hiện trong template |
|---|---|---|
| Business requirement | Mục tiêu/kết quả nghiệp vụ | `Mục tiêu nghiệp vụ`, `Problem / Opportunity`, `Desired outcome` |
| Stakeholder requirement | Nhu cầu của stakeholder hoặc nhóm người dùng | `Stakeholder`, `User roles`, `User stories` |
| Functional requirement | Hành vi hệ thống phải có | `Functional requirements` |
| Non-functional requirement | Ràng buộc chất lượng ở mức BA hiểu được | `NFR cấp BA` |
| Transition/change requirement | Yêu cầu chuyển đổi/nâng cấp | `Feature Upgrade Details`, `Change impact`, `Regression risks` |
| Business rule | Quy tắc nghiệp vụ, điều kiện, ràng buộc | `Business rules` |
| Data requirement | Dữ liệu nghiệp vụ cần hiển thị/tạo/cập nhật | `Data requirements`, `Validation rules` |

Lý do: nếu trộn tất cả thành một danh sách requirement, dev và QA khó xác định đâu là mục tiêu, đâu là rule, đâu là flow, đâu là điều kiện kiểm thử.

## 3. Elicitation và clarification

Input từ BA/PO thường thiếu, mơ hồ hoặc nằm rải rác trong text, Figma, file cũ, meeting note. Vì vậy skill cần cơ chế hỏi lại có thứ tự ưu tiên.

Nhóm câu hỏi cần có:

1. Business goal.
2. User roles.
3. Scope.
4. Main flow.
5. Business rules.
6. UI/Figma.
7. Data.
8. Permissions.
9. Edge cases.
10. Acceptance criteria.
11. Dependencies.

Nguyên tắc hỏi:

- Hỏi blocking question trước.
- Không hỏi quá 10 câu trong một lượt.
- Không hỏi lại thông tin đã có.
- Nếu người dùng muốn proceed, tạo draft và đưa các điểm thiếu vào `[OPEN_QUESTION]`.

## 4. Process flow / workflow

Một feature spec thực dụng cho dev không nên chỉ có user story. Cần có luồng nghiệp vụ:

- Trigger bắt đầu.
- Actor thực hiện.
- Action.
- System response.
- Resulting state.
- Alternative flow.
- Exception flow.

Template dùng bảng `Luồng chính` và `Luồng thay thế`, kèm Mermaid flowchart nếu agent/render hỗ trợ.

## 5. Business rules

Business rule phải được tách khỏi functional requirement.

Ví dụ:

- Functional requirement: “Hệ thống phải cho phép Admin từ chối yêu cầu hoàn tiền.”
- Business rule: “Khi từ chối, Admin bắt buộc nhập lý do.”

Nếu trộn hai phần này, QA dễ bỏ sót negative test và dev dễ hard-code sai rule.

## 6. Data requirements và validation

BA không cần thiết kế database, nhưng phải mô tả dữ liệu nghiệp vụ:

- Field nào hiển thị.
- Field nào bắt buộc.
- Allowed values.
- Format.
- Khi action xảy ra thì data/status đổi thế nào.
- Error message hoặc behavior khi validation fail.

Do đó template có hai bảng riêng:

- `Data requirements`
- `Validation rules`

## 7. Permission matrix

Permission không nên viết lẫn trong paragraph. Nên dùng ma trận để dev và QA dễ test:

| Role | View | Create | Update | Delete | Approve | Reject | Export |
|---|---:|---:|---:|---:|---:|---:|---:|

Nguồn BABOK liệt kê `Roles and Permissions Matrix` là một kỹ thuật business analysis phổ biến.

## 8. State transition

Các feature có trạng thái như request, order, approval, ticket, payment, refund cần state transition rõ ràng:

- From state.
- Trigger/action.
- Condition.
- To state.
- Actor.
- Terminal state?

Nếu input chưa nói rõ state, skill phải đánh dấu `[ASSUMPTION]` hoặc `[OPEN_QUESTION]`.

## 9. User stories và acceptance criteria

User story nên dùng để diễn đạt nhu cầu theo vai trò, nhưng không đủ để dev implement. Skill phải bổ sung functional requirement, rule, flow, data, permission, state và acceptance criteria.

Agile Alliance mô tả INVEST là checklist chất lượng cho user story. Với acceptance criteria, Given/When/Then là template để viết acceptance test từ user story.

Nguồn:

- INVEST, Agile Alliance: https://agilealliance.org/glossary/invest/
- Given-When-Then, Agile Alliance: https://agilealliance.org/glossary/given-when-then/

## 10. Traceability

Traceability giúp biết requirement đến từ đâu, phục vụ scope/change/risk/test. Trong `ba-spec`, mỗi requirement có ID và traceability matrix map:

- Source / business goal.
- Functional requirement.
- Business rule.
- Acceptance criteria.
- Test focus.

Nguồn:

- IIBA Trace Requirements: https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/5-requirements-life-cycle-management/5-1-trace-requirements/

## 11. Feature upgrade / change request

Với nâng cấp tính năng, spec không chỉ mô tả behavior mới. Cần có:

- Current behavior.
- Requested change.
- Affected roles.
- Affected data/status.
- Impacted business rules.
- Backward compatibility.
- Regression risks.
- Items not changed.

Nếu không có current behavior, skill phải hỏi hoặc đánh dấu open question.

## 12. Non-functional requirements ở mức BA

Không phải mọi NFR cần kiến trúc sâu. BA nên ghi các NFR quan trọng nếu có căn cứ:

- Usability.
- Accessibility.
- Auditability.
- Security/privacy ở mức business.
- Performance expectation ở mức observable.
- Compliance/policy.
- Availability/operational constraint nếu stakeholder nêu.

Không tự bịa SLA hoặc kiến trúc.

## 13. Quyết định thiết kế template

Vì BA và dev không cùng workspace, template phải tự chứa đủ context nghiệp vụ:

- `Input Summary` để biết nguồn.
- `Source tags` để tránh lẫn fact/suy luận.
- `Requirement IDs` để trace.
- `Tables` để agent parse.
- `Open questions` để PO/BA xử lý.
- `Assumptions` để không biến giả định thành fact.
- `Handoff checklist` để kiểm tra trước khi gửi dev/QA.

## 14. Mức độ chắc chắn

Skill không được biến thông tin thiếu thành spec chắc chắn. Dùng tag:

- `[PROVIDED]` cho thông tin user nói trực tiếp.
- `[FIGMA]` cho thông tin nhìn thấy hoặc đọc từ Figma.
- `[FILE]` cho thông tin từ tài liệu.
- `[INFERRED]` cho suy luận hợp lý.
- `[ASSUMPTION]` cho giả định cần confirm.
- `[OPEN_QUESTION]` cho câu hỏi cần trả lời.
