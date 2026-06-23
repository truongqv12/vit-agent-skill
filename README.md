# AI Agent Skills

Bộ sưu tập Agent Skills cá nhân/team cho các agentic coding tools như Claude Code, Codex, Antigravity, Cursor, Gemini CLI và các tool hỗ trợ `npx skills`.

Repo này được tổ chức theo kiểu multi-skill giống `vercel-labs/agent-skills`: mỗi skill nằm trong `skills/<skill-name>/` và có `SKILL.md` riêng.

## Available Skills

### ba-spec

Tạo đặc tả tính năng nghiệp vụ cho dev/QA từ mô tả BA, Figma link/screenshot, tài liệu cũ, ticket, meeting note hoặc change request. Skill file viết bằng tiếng Anh để agent dễ thực thi, nhưng output mặc định là tiếng Việt.

Use when:

- Chuyển yêu cầu nghiệp vụ thành `feature-spec.md` và `feature-spec.html`.
- Tạo tài liệu handoff cho dev, QA, PO, stakeholder.
- Phân tích quy trình nghiệp vụ nhiều bước.
- Ghi nhận requirement, business rule, permission, validation, state transition, edge case, acceptance criteria.
- Có Figma URL và cần bắt agent chạy Figma MCP evidence gate trước khi viết spec.

Features:

- Router-style `SKILL.md` ngắn, rule chi tiết nằm trong `references/`.
- Output tiếng Việt.
- Markdown là source of truth.
- HTML dùng Tailwind CDN và Mermaid.js CDN.
- Output được đóng gói vào thư mục `ba-spec-output/YYYY-MM-DD__epic-...__story-...__feature.../`.
- Có Figma MCP hard gate: không được claim đã phân tích Figma nếu không có evidence log.
- Giữ nguyên link Figma gốc trong `figma-links.md`, `feature-spec.md`, và HTML.
- Helper scripts/temp files phải tạo trong tmp và xóa trước final response.
- Hỗ trợ new feature và feature upgrade.

## Repository Structure

```text
skills/
  ba-spec/
    SKILL.md
    README.md
    templates/
    references/
    scripts/
    examples/
    docs/
skills.sh.json
AGENTS.md
README.md
```

## Install

### List skills in this repo

```bash
npx skills add <your-github-user>/<your-repo> --list
```

### Install only `ba-spec`

```bash
npx skills add <your-github-user>/<your-repo> --skill ba-spec
```

### Install globally

```bash
npx skills add <your-github-user>/<your-repo> --skill ba-spec -g
```

### Install for a specific agent

```bash
npx skills add <your-github-user>/<your-repo> --skill ba-spec -a claude-code
npx skills add <your-github-user>/<your-repo> --skill ba-spec -a codex
npx skills add <your-github-user>/<your-repo> --skill ba-spec -a antigravity
```

### Install all skills from this repo later

```bash
npx skills add <your-github-user>/<your-repo> --skill '*'
```

## Use

```text
Use ba-spec.
Tạo feature-spec.md và feature-spec.html bằng tiếng Việt từ mô tả nghiệp vụ sau...
```

Nếu input có Figma URL, prompt nên ghi rõ:

```text
Trước khi tạo spec, bắt buộc chạy Figma MCP evidence gate. Nếu MCP không khả dụng, ghi rõ MCP_UNAVAILABLE/MCP_FAILED trong Nhật ký bằng chứng Figma, không được claim đã phân tích Figma.
```

## Add a New Skill Later

Tạo folder mới:

```text
skills/<new-skill-name>/
  SKILL.md
  README.md
  references/
  scripts/
  templates/
```

Yêu cầu tối thiểu:

```markdown
---
name: new-skill-name
description: Explain exactly when this skill should trigger.
---

# New Skill Name

Instructions for the agent.
```

Sau đó update `skills.sh.json` nếu muốn skill được group đẹp trên skills.sh.

## License

MIT
