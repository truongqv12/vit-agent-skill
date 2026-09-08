---
date: 2026-08-26
session: portable-cook-delivery-loop
type: work-history
---

# Nhật ký: 2026-08-26 — Portable `cook` delivery-loop program

## Bối cảnh

Port `cook` và toàn bộ delivery-loop skill mà nó điều phối sang kit portable,
chạy được không cần AgentKit CLI, private subagent hay hidden state
(`.ck.json`, `CK_*`). `cook` là capstone: điều phối scout → research → plan →
implement → simplify → test → review → finalize qua ~11 skill companion. Nhật ký
này ghi lịch sử công việc, không thay thế plan, contract hay report hiện hành.

## Diễn tiến

1. Phân tích `ak:cook` (v2.2.0): 4 HARD-GATE, anti-rationalization table, 6 mode
   + `--tdd`, review gate, mandatory delegation, whole-plan finalize sync-back;
   nhận diện coupling `/ak:*`, named subagent, `delegate_agent`/`ask_user`, live
   task surface và simplify hidden state.
2. Lập program plan 12 phase (`vit-plan/v1`), chia 5 wave A–E theo giá trị điều
   phối và dependency; wave 0 (`brainstorm`, `vit-plan`) đã có sẵn.
3. Định nghĩa "Capability Handoff Convention" ở Phase 1 (scout) và tái dùng cho
   mọi skill: ưu tiên capability khi runtime expose, nếu không thì làm inline
   bằng native tool, hết đường thì báo thiếu trung thực — không bao giờ emit
   `/ak:*` hay named subagent làm đường duy nhất.
4. Port 11 skill: `scout`, `code-review`, `test`, `debug` (wave A); `research`,
   `git`, `project-management`, `journal`, `docs` (wave B); `fix` (wave C);
   `cook` (wave D). 9 skill giao cho subagent song song với ranh giới file rõ
   ràng (mỗi agent chỉ sở hữu `skills/<name>/**`); controller giữ file dùng
   chung (catalog, index, scripts).
5. Rewrite `cook` handoff về tên portable, giữ git-diff simplify threshold
   (400 LOC / 8 file / 200 single-file) nhưng bỏ `.ck.json` và
   `CK_SIMPLIFY_DISABLED`; mọi external effect finalize (commit, docs, journal)
   thành explicit-intent.
6. Đăng ký group "Delivery Loop" và "Project Operations" trong catalog, regen
   skill index, đóng plan (12/12 phase completed) và lint pass.

## Quyết định và tác động

| Quyết định | Lý do | Tác động |
|---|---|---|
| Port companion trước, `cook` cuối | Tránh viết lại handoff hai lần | Mọi handoff của `cook` resolve về skill thật khi lên |
| Capability-first + native fallback | Không giả định companion tồn tại | `cook` vẫn chạy khi thiếu skill, tự cải thiện khi có |
| Giữ simplify gate, bỏ hidden state | Bảo toàn invariant, cắt coupling | Simplify chạy bằng git-diff thuần, portable |
| Không tái tạo `code-simplifier` thành skill | YAGNI, ngoài delivery loop | Simplify là bước native optional, không thêm skill |
| External effect = explicit-intent | Chuẩn an toàn side effect | Không commit/push/mutate tự động |

## Xác minh

- Repository validator: **16/16 skill pass** (`ba-spec, brainstorm, code-review,
  cook, debug, docs, figma-to-code, fix, git, jira-task, journal,
  project-management, research, scout, test, vit-plan`).
- Skill index: **current** (`generate-skill-index.py --check` pass).
- Integration tĩnh: 11 handoff target của `cook` đều resolve về skill dir tồn
  tại; mọi skill dir có `SKILL.md` + `README.md`.
- Coupling scan: không còn `/ak:*`, named subagent, `.ck.json`, `CK_*`,
  `ak <command>` hay absolute source path trong runtime instruction; hit duy
  nhất là dòng provenance lành tính ở `skills/cook/README.md`.
- Plan: `plan-tool.py lint` pass; 12/12 phase `completed`, plan status
  `completed`.

## Giới hạn và non-goals

- Không port skill ngoài delivery loop (frontend/ui, media, deploy, security,
  MCP...). `ui-ux-designer`/`fullstack-developer` là agent role, xử lý bằng
  native fallback.
- Không clone AgentKit CLI, SQLite store, dashboard, hook, hay hidden state.
- E2E "chạy `cook` thật đầu-cuối" được xác minh ở mức tĩnh (handoff resolve,
  native fallback hiện diện, validator xanh); một lần chạy live trên task thực
  vẫn là bước xác minh thủ công còn lại.
- Chưa commit: mọi thay đổi đang ở worktree, chờ user xác nhận trước khi commit.

## Rollback và bước tiếp theo

- Rollback từng skill: xóa `skills/<name>/**` và revert hunk catalog/index tương
  ứng; các phase khác không bị ảnh hưởng.
- Tiếp theo: (a) chạy `cook` live một task thực để đóng nốt E2E manual;
  (b) commit theo conventional format nếu user đồng ý; (c) cân nhắc dọn stub
  `python3` trong `validate-skills.sh` trong một scope riêng.

## Câu hỏi chưa giải quyết

- Không có blocker. E2E live và commit chờ quyết định của user.
