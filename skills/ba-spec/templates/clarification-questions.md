# Câu hỏi làm rõ: {{FEATURE_NAME}}

Dùng template này khi input thiếu, mơ hồ hoặc có rủi ro nếu dev implement ngay.

Quy tắc:

- Hỏi câu blocking trước.
- Không hỏi quá 10 câu trong một lượt nếu người dùng chưa yêu cầu discovery đầy đủ.
- Đánh dấu `Blocking` hoặc `Non-blocking`.
- Nếu người dùng muốn tiếp tục, chuyển câu chưa trả lời thành `[OPEN_QUESTION]`.

---

## 1. Business goal

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-BG-001 | Tính năng này giải quyết vấn đề nghiệp vụ nào? | Có | Tránh build action/UI không gắn với outcome. |
| Q-BG-002 | Kết quả thành công được đo như thế nào? | Không | Hỗ trợ acceptance criteria và analytics. |
| Q-BG-003 | Tính năng này phục vụ release, campaign, compliance hay quy trình vận hành cụ thể nào không? | Không | Hỗ trợ scope/prioritization. |

## 2. User roles

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-ROLE-001 | Những role nào được dùng tính năng này? | Có | Cần cho permission và test case. |
| Q-ROLE-002 | Mỗi role được xem/tạo/sửa/duyệt/từ chối/xóa/export gì? | Có | Tránh mơ hồ authorization. |
| Q-ROLE-003 | Có actor hệ thống hoặc hệ thống ngoài nào tham gia không? | Không | Bắt trigger không do người dùng tạo. |

## 3. Scope

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-SCOPE-001 | Release này chính xác bao gồm những phần nào? | Có | Xác định ranh giới implement. |
| Q-SCOPE-002 | Những phần nào chắc chắn ngoài scope? | Có | Tránh scope creep. |
| Q-SCOPE-003 | Có enhancement tương lai cần ghi nhận nhưng chưa làm không? | Không | Tách current scope và future scope. |

## 4. Flow

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-FLOW-001 | Happy path từ lúc bắt đầu đến lúc hoàn tất là gì? | Có | Cốt lõi cho dev và QA. |
| Q-FLOW-002 | Điều gì trigger flow? | Có | Cần entry condition. |
| Q-FLOW-003 | Sau action chính thì hệ thống phản hồi và đổi trạng thái như thế nào? | Có | Cần output và state. |
| Q-FLOW-004 | Có alternative path như hủy, lưu nháp, retry, approve, reject, escalate, resubmit không? | Không | Bắt nhánh ngoài happy path. |

## 5. Business rules

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-BR-001 | Điều kiện nào phải đúng trước khi user được thực hiện action? | Có | Xác định eligibility. |
| Q-BR-002 | Điều kiện nào chặn action? | Có | Xác định negative cases. |
| Q-BR-003 | Có threshold, limit, deadline, quota hoặc special case không? | Không | Tránh thiếu nhánh rule. |
| Q-BR-004 | Rule này đến từ policy, operation, legal, finance hay product decision? | Không | Hỗ trợ traceability. |

## 6. UI / Figma

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-UI-001 | Những screen/frame Figma nào liên quan? | Không | Map UI với flow. |
| Q-UI-002 | Có field, button, label, status badge, banner, modal bắt buộc nào không? | Không | Xác định UI behavior. |
| Q-UI-003 | Có empty/loading/success/error/permission-denied state không? | Không | Hỗ trợ QA UI states. |
| Q-UI-004 | Nếu MCP không dùng được, anh có thể gửi screenshot/export/copy text từ Figma không? | Không | Fallback cho Figma link. |

## 7. Data

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-DATA-001 | Tính năng này tạo, cập nhật hoặc hiển thị dữ liệu nào? | Có | Cần cho dev/QA. |
| Q-DATA-002 | Field nào bắt buộc, optional hoặc conditional? | Có | Cần cho validation. |
| Q-DATA-003 | Allowed values/statuses là gì? | Có | Cần cho data consistency. |
| Q-DATA-004 | Có cần giữ lịch sử thay đổi không? | Không | Cần cho audit/trace. |

## 8. Permissions

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-PERM-001 | Ai được xem tính năng/dữ liệu này? | Có | Access control. |
| Q-PERM-002 | Ai được create/update/approve/reject/delete/export? | Có | Permission matrix. |
| Q-PERM-003 | User không có quyền sẽ thấy gì? | Không | UX và QA. |
| Q-PERM-004 | Permission có kế thừa từ module hiện có không? | Không | Tránh duplicate rule. |

## 9. Edge cases

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-EDGE-001 | Nếu thiếu dữ liệu bắt buộc thì hệ thống xử lý thế nào? | Có | Validation. |
| Q-EDGE-002 | Nếu nhiều user cập nhật cùng lúc thì xử lý thế nào? | Không | Concurrency. |
| Q-EDGE-003 | Nếu hệ thống ngoài/API fail thì user thấy gì? | Không | Error handling. |
| Q-EDGE-004 | Có ngoại lệ theo user/account/status/khoảng thời gian nghiệp vụ không? | Không | Business exception. |

## 10. Acceptance criteria

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-AC-001 | Điều gì phải đúng để PO/QA chấp nhận tính năng? | Có | Definition of done. |
| Q-AC-002 | QA bắt buộc phải test scenario nào? | Có | Testability. |
| Q-AC-003 | Team có muốn acceptance criteria dạng Gherkin không? | Không | BDD nếu cần. |
| Q-AC-004 | Có audit log/report/notification cần verify không? | Không | Operational acceptance. |

## 11. Dependencies

| ID | Câu hỏi | Blocking? | Vì sao cần hỏi |
|---|---|---:|---|
| Q-DEP-001 | Tính năng phụ thuộc team, API, policy, data source hoặc release nào không? | Không | Planning. |
| Q-DEP-002 | Có module/rule hiện có phải reuse không? | Không | Consistency. |
| Q-DEP-003 | Có constraint từ legal/security/finance/operations không? | Không | Non-functional/policy. |
