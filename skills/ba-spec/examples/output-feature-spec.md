# Đặc tả tính năng: Duyệt yêu cầu hoàn tiền cho user VIP

> Markdown là source of truth. HTML chỉ là bản trình bày để review/gửi team.

---

## 1. Metadata tài liệu

| Trường | Giá trị |
|---|---|
| Document ID | SPEC-VIP-REFUND-APPROVAL |
| Tên tính năng | Duyệt yêu cầu hoàn tiền cho user VIP |
| Loại tính năng | new_feature |
| Phiên bản | 0.1 |
| Trạng thái | Draft |
| BA / Owner | Chưa xác định |
| PO / Stakeholder | Chưa xác định |
| Ngày tạo | YYYY-MM-DD |
| Source of truth | `feature-spec.md` |

## 2. Tóm tắt đầu vào

| Loại input | Có/Không | Ghi chú |
|---|---:|---|
| Business text | Có | Người dùng cung cấp rule duyệt/từ chối refund VIP. |
| Figma screenshot | Không | Không có UI input. |
| Figma link | Không | Không có Figma link. |
| Related files | Không | Không có file liên quan. |
| Existing spec | Không | Không có spec cũ. |
| Change request | Không | Đây là tính năng mới. |
| Unclear input | Có | Thiếu trạng thái ban đầu, rejected status, notification, visibility. |

## 3. Quy ước nguồn và độ chắc chắn

| Tag | Ý nghĩa |
|---|---|
| `[PROVIDED]` | Người dùng cung cấp trực tiếp |
| `[INFERRED]` | Suy luận hợp lý từ thông tin có sẵn |
| `[ASSUMPTION]` | Giả định cần xác nhận |
| `[OPEN_QUESTION]` | Câu hỏi còn mở |

## 4. Tổng quan tính năng

Tính năng cho phép Admin duyệt hoặc từ chối yêu cầu hoàn tiền của user VIP. Khi Admin duyệt, hệ thống ghi nhận trạng thái `approved`. Khi Admin từ chối, hệ thống bắt buộc Admin nhập lý do từ chối.

## 5. Mục tiêu nghiệp vụ

| ID | Mục tiêu | Ưu tiên | Nguồn |
|---|---|---|---|
| BG-001 | Cho phép yêu cầu hoàn tiền của user VIP được Admin xử lý bằng quyết định duyệt hoặc từ chối. | Must | [PROVIDED] |

## 7. Stakeholder và vai trò

| ID | Role / Actor | Mô tả | Tóm tắt quyền | Nguồn |
|---|---|---|---|---|
| ROLE-001 | Admin | Người xử lý yêu cầu hoàn tiền VIP. | Có thể duyệt hoặc từ chối. | [PROVIDED] |
| ROLE-002 | User VIP | Người có yêu cầu hoàn tiền cần được xử lý. | Là đối tượng của yêu cầu hoàn tiền. | [PROVIDED] |

## 9. Luồng nghiệp vụ

| Step ID | Actor | Trigger / Action | Phản hồi của hệ thống | Trạng thái kết quả | Nguồn |
|---|---|---|---|---|---|
| FLOW-001 | Admin | Mở yêu cầu hoàn tiền VIP cần xử lý. | Hệ thống hiển thị thông tin yêu cầu và action duyệt/từ chối. | pending_review | [INFERRED] |
| FLOW-002 | Admin | Chọn duyệt yêu cầu. | Hệ thống ghi nhận trạng thái `approved`. | approved | [PROVIDED] |
| FLOW-003 | Admin | Chọn từ chối và nhập lý do. | Hệ thống ghi nhận từ chối kèm lý do. | rejected | [ASSUMPTION] |

## 10. Functional requirements

| ID | Requirement | Ưu tiên | Role liên quan | Flow liên quan | Nguồn |
|---|---|---|---|---|---|
| FR-001 | Hệ thống phải cho phép Admin duyệt yêu cầu hoàn tiền của user VIP. | Must | ROLE-001 | FLOW-002 | [PROVIDED] |
| FR-002 | Hệ thống phải cho phép Admin từ chối yêu cầu hoàn tiền của user VIP. | Must | ROLE-001 | FLOW-003 | [PROVIDED] |
| FR-003 | Hệ thống phải ghi nhận trạng thái `approved` khi Admin duyệt yêu cầu. | Must | ROLE-001 | FLOW-002 | [PROVIDED] |
| FR-004 | Hệ thống phải yêu cầu nhập lý do khi Admin từ chối yêu cầu. | Must | ROLE-001 | FLOW-003 | [PROVIDED] |

## 11. Business rules

| ID | Rule | Áp dụng cho | Ưu tiên | Nguồn |
|---|---|---|---|---|
| BR-001 | Admin có thể duyệt hoặc từ chối yêu cầu hoàn tiền VIP. | Permission / Action | Must | [PROVIDED] |
| BR-002 | Khi từ chối, lý do từ chối là bắt buộc. | Reject action | Must | [PROVIDED] |

## 15. State transition

| ID | From state | Trigger / Action | Điều kiện | To state | Actor | Nguồn |
|---|---|---|---|---|---|---|
| TR-001 | pending_review | Approve | Admin xác nhận duyệt. | approved | Admin | [ASSUMPTION] |
| TR-002 | pending_review | Reject | Admin nhập lý do từ chối. | rejected | Admin | [ASSUMPTION] |

## 17. Acceptance criteria

| ID | Acceptance criterion | Requirement liên quan | Ưu tiên |
|---|---|---|---|
| AC-001 | Admin có thể duyệt yêu cầu hoàn tiền VIP và trạng thái được ghi nhận là `approved`. | FR-001, FR-003 | Must |
| AC-002 | Admin không thể từ chối yêu cầu hoàn tiền VIP nếu chưa nhập lý do. | FR-002, FR-004, BR-002 | Must |
| AC-003 | Admin có thể từ chối yêu cầu hoàn tiền VIP khi đã nhập lý do. | FR-002, FR-004 | Must |

```gherkin
Feature: Duyệt yêu cầu hoàn tiền cho user VIP

Scenario: Admin duyệt yêu cầu hoàn tiền VIP
  Given một yêu cầu hoàn tiền VIP đang chờ xử lý
  When Admin duyệt yêu cầu
  Then hệ thống ghi nhận trạng thái yêu cầu là "approved"

Scenario: Admin từ chối nhưng chưa nhập lý do
  Given một yêu cầu hoàn tiền VIP đang chờ xử lý
  When Admin chọn từ chối mà chưa nhập lý do
  Then hệ thống không cho phép hoàn tất thao tác từ chối
  And hệ thống yêu cầu Admin nhập lý do từ chối
```

## 23. Assumptions

| ID | Assumption | Lý do | Impact nếu sai | Cần xác nhận bởi |
|---|---|---|---|---|
| ASM-001 | Trạng thái ban đầu là `pending_review`. | Input chưa nêu trạng thái ban đầu. | Sai state transition. | PO / BA |
| ASM-002 | Trạng thái khi từ chối là `rejected`. | Input chỉ nêu trạng thái khi duyệt. | Dev có thể implement sai status. | PO / BA |

## 24. Open questions

| ID | Câu hỏi | Nhóm | Blocking? | Cần ai trả lời |
|---|---|---|---:|---|
| Q-001 | Trạng thái ban đầu trước khi Admin xử lý là gì? | State | Có | PO / BA |
| Q-002 | Trạng thái chính xác khi từ chối là gì? | State | Có | PO / BA |
| Q-003 | User VIP có nhận thông báo sau khi được duyệt/từ chối không? | Flow | Không | PO |
| Q-004 | Ngoài Admin, role nào được xem yêu cầu hoàn tiền VIP? | Permission | Không | PO / BA |
