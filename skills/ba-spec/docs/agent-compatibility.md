# Agent Compatibility Notes

Tài liệu này ghi rõ phần nào là chuẩn tương đối chung, phần nào phụ thuộc agent.

## 1. Chuẩn chung tương đối

Hầu hết agent hỗ trợ Agent Skills hiện nay đều dùng ý tưởng:

```text
skill-folder/
  SKILL.md
  scripts/
  references/ hoặc docs/
  templates/
  assets/
```

`SKILL.md` thường có YAML frontmatter:

```markdown
---
name: ba-spec
description: ...
---
```

Các agent thường dùng `description` để quyết định khi nào load skill. Vì vậy `description` của `ba-spec` đã front-load các trigger như `business requirements`, `feature specifications`, `Figma`, `change requests`, `dev/QA handoff`.

Nguồn tham khảo:

- OpenAI Codex Skills: https://developers.openai.com/codex/skills
- Claude Skills best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Google Antigravity Skills: https://antigravity.google/docs/skills
- Skills CLI: https://github.com/vercel-labs/skills

## 2. Codex

Codex mô tả skill là directory có `SKILL.md` và optional `scripts`, `references`, `assets`. `SKILL.md` cần có `name` và `description`.

Vị trí phổ biến:

```text
.agents/skills/ba-spec/
~/.codex/skills/ba-spec/
```

Invocation thường có thể explicit qua `/skills` hoặc `$ba-spec`, hoặc implicit khi prompt match description.

## 3. Claude Code

Claude Code/Claude Skills dùng progressive disclosure: chỉ load phần cần thiết khi skill được chọn. Vì vậy `SKILL.md` nên ngắn vừa đủ và trỏ sang `templates/` hoặc `docs/` khi cần.

Vị trí phổ biến:

```text
.claude/skills/ba-spec/
~/.claude/skills/ba-spec/
```

## 4. Antigravity / Antigravity CLI

Antigravity documentation mô tả skill là folder có `SKILL.md` chứa instructions. Project path thường dùng:

```text
.agents/skills/ba-spec/
```

Global path phụ thuộc bản cài và môi trường.

## 5. Gemini CLI

Gemini CLI có thể dùng MCP/extensions và có các workflow liên quan Figma. Với Agent Skills, cách cài phụ thuộc bản CLI và ecosystem skills đang dùng.

Khuyến nghị tool-agnostic:

```text
.agents/skills/ba-spec/
```

Nếu Gemini/Antigravity setup của anh có path riêng, copy nguyên folder `ba-spec` vào đúng path đó.

## 6. `npx skills add`

`npx skills add` là CLI của hệ sinh thái open agent skills. Nó có thể cài từ GitHub/package registry vào nhiều agent target, nhưng không phải là command bắt buộc của mọi agent.

Ví dụ:

```bash
npx skills add <owner>/ba-spec
```

Nếu CLI không nhận đúng agent/path, dùng manual install.

## 7. Quy tắc thiết kế tool-agnostic cho `ba-spec`

- Không phụ thuộc một agent cụ thể.
- Không giả định agent luôn có MCP.
- Không giả định agent luôn có Figma access.
- Không yêu cầu BA biết code.
- `SKILL.md` chỉ chứa workflow và policy cốt lõi.
- Template chi tiết đặt trong `templates/`.
- Research/compatibility đặt trong `docs/`.
- Script chỉ hỗ trợ setup, không bắt buộc skill chạy.
