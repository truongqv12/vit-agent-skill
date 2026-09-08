# Portable Skill Contract

Tài liệu này là contract bắt buộc cho skill mới hoặc skill được normalize từ
nguồn khác vào repo. Mục tiêu là để bất kỳ agent nào có thể đọc repo, chọn đúng
skill và thực thi bằng capability native của runtime, không phụ thuộc CLI hoặc
layout của nguồn.

Các skill có trước contract này được migrate tăng dần và có thể chưa đạt toàn
bộ quy tắc. Catalog phải ghi đúng trạng thái; không được claim repository-wide
portability trước khi từng skill được audit.

## Lifecycle

```text
collect -> normalize -> index -> pickup
```

1. **Collect:** lấy skill và toàn bộ file thực sự cần thiết từ nguồn.
2. **Normalize:** đổi identity, path, handoff và script về contract portable.
3. **Index:** đăng ký grouping trong `skills.sh.json`, rồi sinh
   `docs/skills/README.md` từ frontmatter thực tế.
4. **Pickup:** agent đọc index, tải skill cần thiết và dùng tool hiện có.

Skills CLI là kênh discovery/install tùy chọn. Nó không phải runtime dependency.

## Package tối thiểu

```text
skills/<portable-name>/
  SKILL.md
  README.md
```

Chỉ thêm `references/`, `scripts/`, `templates/`, `examples/` hoặc `docs/` khi
skill thực sự sử dụng chúng.

## Canonical identity

- Folder và frontmatter `name` phải giống nhau.
- Dùng kebab-case, mô tả capability thay vì vendor hoặc CLI.
- Tên nguồn được giữ trong provenance, không dùng làm runtime identity.
- `description` phải nói rõ outcome và trigger để agent routing được chỉ bằng
  catalog metadata.

Ví dụ:

```yaml
---
name: brainstorm
description: "Turn unclear intent into an accepted outcome before delivery."
license: MIT
metadata:
  author: agentkit
  version: "1.0.0"
  source-skill: "ak:brainstorm"
  source-version: "2.3.0"
  portability: standalone
---
```

Không bịa source URL, commit, license hoặc version khi evidence nguồn không có.

## Portability rules

### Handoff theo capability

Mô tả capability cần dùng, ví dụ planning, browser testing hoặc code review.
Không bắt agent gọi một command hay skill name chỉ tồn tại trong bộ nguồn.

Khi capability chuyên biệt không tồn tại, skill phải:

1. Dùng tool native tương đương nếu an toàn.
2. Hoặc dừng và báo dependency còn thiếu nếu không có fallback đúng.

### Dependencies

Phân loại dependency trong README hoặc SKILL:

- `standalone`: không cần skill khác.
- `optional`: có thể tăng chất lượng nhưng có native fallback.
- `required`: không thể hoàn thành contract nếu thiếu; phải nêu cách phát hiện và
  failure behavior.

Không claim dependency đã được cài chỉ vì nó có trong source collection.

### References và scripts

- Dùng đường dẫn tương đối tính từ skill directory.
- Không hard-code home directory, username hoặc source installation path.
- Script phải khai báo runtime và hỗ trợ OS đúng với phạm vi đã công bố.
- Nếu script nguồn không portable, sửa hoặc loại khỏi package; không để dead
  file chỉ vì muốn copy đủ.
- Khi script thất bại, báo failure; không giả lập kết quả.

### Behavior preservation

Trước khi sửa, xác định các invariant của skill nguồn. Sau khi normalize, đối
chiếu từng invariant bằng scenario hoặc static check. Portability edit không
được âm thầm đổi outcome cốt lõi.

## Pickup protocol cho agent

1. Đọc generated index `docs/skills/README.md` để xác định nhóm capability.
2. So khớp request với `description` của các candidate `SKILL.md`.
3. Chọn một primary skill cho mỗi intent; chỉ thêm secondary skill khi scope
   thực sự giao nhau.
4. Đọc toàn bộ `SKILL.md` đã chọn.
5. Chỉ tải reference/script mà router yêu cầu cho case hiện tại.
6. Resolve handoff bằng live capabilities; không suy từ source namespace.
7. Thực thi và kiểm chứng theo contract của skill.

## Checklist migrate một skill

- [ ] Đã inventory toàn bộ file nguồn và dependency thực.
- [ ] Đã xác định invariant hành vi cần giữ.
- [ ] Folder/name dùng canonical portable identity.
- [ ] Description đủ để routing.
- [ ] Provenance và license có evidence.
- [ ] Không còn source CLI command hoặc absolute source path ở runtime contract.
- [ ] Handoff dùng capability và có fallback/failure behavior.
- [ ] References/scripts resolve bằng đường dẫn tương đối.
- [ ] `skills.sh.json` đã cập nhật và generated skill index đang current.
- [ ] Generic validator pass.
- [ ] Skills CLI discovery pass như một compatibility check tùy chọn.
- [ ] Scenario checks chứng minh invariant nguồn còn nguyên.

## Definition of done

Một skill được coi là portable khi agent chỉ cần repo này và capability native
được khai báo để hiểu lúc nào dùng, đọc đủ instruction, thực thi đúng behavior
và báo dependency thiếu trung thực. Không cần truy cập source collection hoặc
CLI của source trong runtime.
