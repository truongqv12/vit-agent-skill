# brainstorm

`brainstorm` giúp agent biến một yêu cầu chưa hoàn chỉnh thành delivery contract
có giới hạn trước khi lập kế hoạch hoặc triển khai.

## Khi nên dùng

- Mở đầu công việc product, code, documentation hoặc maintainer có nhiều bước.
- Yêu cầu còn thiếu một quyết định có thể thay đổi kết quả hoặc public contract.
- Một lỗi đã được chẩn đoán nhưng còn nhiều phương án sửa hợp lệ.
- Cần so sánh tối đa ba hướng tiếp cận bằng evidence và trade-off.

Không cần dùng cho câu trả lời trực tiếp hoặc thao tác read-only đơn giản.

## Contract đầu ra

Skill luôn làm rõ bốn trường:

1. Outcome.
2. Constraints.
3. Non-goals.
4. Acceptance criteria.

Skill chỉ định hình intent và lựa chọn. Nó không tự triển khai giải pháp.

## Tính portable

- Không yêu cầu AgentKit CLI.
- Không gọi command hoặc skill thuộc một bộ công cụ cố định.
- Handoff theo capability mà runtime hiện tại có thể cung cấp.
- Có native fallback khi runtime không cài planning, implementation hoặc repair
  skill chuyên biệt.

## Nguồn và adaptation

- Nguồn: `ak:brainstorm`.
- Source skill baseline: `ak:brainstorm` v2.3.0.
- License: MIT.
- Author nguồn: `agentkit`.
- Local skill version: 1.0.0.

Adaptation trong repo này:

- Đổi canonical name từ `ak:brainstorm` thành `brainstorm`.
- Loại bỏ handoff phụ thuộc command AgentKit.
- Giữ nguyên bốn trường contract, proportional behavior, bug-routing sequence,
  giới hạn tối đa ba phương án và implementation boundary.

Chưa xác định upstream URL/commit từ thư mục nguồn cục bộ; không suy đoán thông
tin này.

## Cách dùng

```text
Use brainstorm.
Giúp tôi làm rõ outcome, constraints, non-goals và acceptance criteria cho
tính năng duyệt hoàn tiền trước khi lập kế hoạch.
```

Agent cũng có thể đọc trực tiếp `SKILL.md`; cài đặt qua Skills CLI chỉ là một
kênh phân phối tùy chọn.
