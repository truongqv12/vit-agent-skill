---
date: 2026-08-24
session: vit-plan-portable-skill
type: work-history
---

# Nhật ký: 2026-08-24 — Portable `vit-plan` skill

## Bối cảnh

Chuyển workflow `ak:plan` thành package `vit-plan` portable, plan-only và
filesystem-first. Markdown trong `plans/` là durable authority; helper, runtime
task view và research chỉ là evidence hoặc projection. Nhật ký này ghi lịch sử
công việc, không thay thế plan, contract hay ADR hiện hành.

## Diễn tiến

1. Research inventory source skill, live CLI và coupling; chốt giữ 13 behavioral
   invariants nhưng không clone private store, dashboard, hook hay source CLI.
2. Định nghĩa schema `vit-plan/v1`, canonical `plan.md`/phase template, đường
   dẫn repo-relative, dependency không chu kỳ và nguyên tắc không overwrite.
3. Xây helper Python standard-library với đúng ba thao tác `create`, `add-phase`,
   `lint`; thêm native file/template fallback khi Python không có.
4. Port workflow planning theo capability: accepted intent, unfinished-plan
   scan, scope challenge, proportional modes, evidence-first design,
   verification, validation interview, red team và whole-plan reread.
5. Đăng ký `vit-plan` trong README/catalog; mở rộng validator để kiểm tra runtime
   Markdown đệ quy mà vẫn giữ nguyên các thay đổi đang có của portable registry.
6. Chạy kiểm thử, probes, lint, validator, discovery, no-source-runtime và review;
   không đụng hai deletion do user sở hữu là `AGENTS.md` và `CHANGELOG.md`.

## Quyết định và tác động

| Quyết định | Lý do | Tác động |
|---|---|---|
| Markdown là nguồn trạng thái duy nhất | Tránh lệ thuộc session/private runtime | Plan sống qua runtime; task/helper chỉ là derived view |
| Helper nhỏ, optional, standard-library | Cần scaffold/lint deterministic nhưng không dựng lại CLI | Có đường nhanh testable và native fallback đầy đủ |
| Chỉ ship Markdown core trong v1 | Giữ phạm vi, an toàn side effect | Không có HTML, GitHub, Wiki, image, archive hay global plan scope |
| Capability discovery + sequential fallback | Không giả định companion skill/tool | Package chạy độc lập và vẫn giữ chuẩn evidence/review |
| User adjudication trước review correction | Bảo toàn quyết định scope/contract | Validator và red team không tự ý đảo quyết định đã chấp thuận |

## Xác minh

- Helper tests: **15/15 pass**.
- Behavioral probes: **7/7 pass**.
- Active implementation plan: `lint` pass.
- Repository validator: **4/4 skills pass**; Bash syntax và JSON catalog pass.
- Targeted validator checks: **4/4 pass**; skill-package validator pass.
- Skills CLI discovery/direct pickup: pass; tìm thấy `vit-plan` đúng identity.
- No-source runtime: pass khi source runtime không có trên `PATH`; native
  fallback được xác nhận.
- Diff/status safety: shared integration giữ thay đổi có sẵn; unrelated user
  deletions không bị khôi phục.
- Independent review: **9.8/10**, không còn blocker.

## Giới hạn và non-goals

- Không implement product code; `vit-plan` chỉ tạo, challenge và validate plan.
- Không tái tạo source CLI, SQLite/private store, dashboard, hooks hay archive.
- Không cung cấp HTML/GitHub/Wiki/image generation hoặc global plan registry ở v1.
- Không khẳng định upstream URL/commit vì local evidence chưa chứng minh.
- AgentWiki đã bỏ qua vì chưa được ủy quyền xuất bản ra bên ngoài.

## Rollback và bước tiếp theo

- Rollback: xóa `skills/vit-plan/` và chỉ revert ba integration hunk liên quan
  trong `README.md`, `skills.sh.json`, `scripts/validate-skills.sh`; giữ nguyên
  mọi thay đổi không thuộc scope.
- Tiếp theo: đồng bộ phase 5 và plan status từ evidence, chạy final diff check,
  rồi handoff package; chỉ mở optional integrations trong một scope riêng có
  approval rõ ràng.

## Câu hỏi chưa giải quyết

- Không có câu hỏi blocking. Upstream repository URL/commit vẫn là evidence gap
  không ảnh hưởng runtime.
