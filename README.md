# Portable Agent Skills

Repo này tập hợp và chuẩn hóa Agent Skills để dùng với nhiều agentic coding
runtime như Claude Code, Codex, Cursor, Gemini CLI và Antigravity.

Mục tiêu không phải mirror một CLI hoặc skill collection cụ thể. Skill mới hoặc
skill đã normalize phải được agent đọc trực tiếp, pickup theo intent và thực thi
bằng capability native có sẵn. Skill legacy được audit và migrate tăng dần.

```text
collect -> normalize -> index -> pickup
```

## Nguyên tắc

- Canonical skill name mô tả capability, không mô tả vendor hoặc CLI nguồn.
- Giữ provenance và license nhưng loại runtime coupling với source collection.
- Handoff theo capability; dùng native fallback hoặc báo dependency thiếu rõ
  ràng.
- Chỉ mang theo references, scripts và templates thực sự cần thiết.
- Skills CLI là kênh discovery/install tùy chọn, không phải runtime dependency.

Contract đầy đủ: [Portable Skill Contract](docs/portable-skill-contract.md).

## Bắt đầu

- Xem [Skill index](docs/skills/README.md) để chọn capability đang thực sự có
  trong `skills/`.
- Đọc [Portable Skill Contract](docs/portable-skill-contract.md) khi thêm hoặc
  normalize skill.
- `skills.sh.json` giữ grouping machine-readable; `SKILL.md` trong từng package
  là runtime contract.

## Cách AI pickup skill

1. Đọc [Skill index](docs/skills/README.md) để tìm nhóm capability.
2. So khớp request với `description` trong frontmatter của candidate skill.
3. Chọn một primary skill cho mỗi intent; chỉ thêm secondary skill khi scope
   thực sự giao nhau.
4. Đọc toàn bộ `SKILL.md` đã chọn.
5. Chỉ tải reference hoặc script được router yêu cầu cho case hiện tại.
6. Resolve handoff bằng live capabilities; không giả định CLI hoặc namespace
   của nguồn còn tồn tại.

Agent có thể dùng repo bằng cách đọc trực tiếp, không cần cài đặt:

```text
Đọc docs/skills/README.md, chọn skill phù hợp với yêu cầu, sau đó đọc đầy đủ
SKILL.md của skill đó trước khi thực hiện. Chỉ tải resource được skill route tới.
```

## Repository structure

```text
skills/
  <skill-name>/
    SKILL.md
    README.md
    references/       # optional
    scripts/          # optional
    templates/        # optional
    examples/         # optional
docs/
  skills/
    README.md          # generated skill index
  portable-skill-contract.md
scripts/
  generate-skill-index.py
  validate-skills.sh
skills.sh.json
README.md
```

## Optional Skills CLI compatibility

### Liệt kê skill

```bash
npx skills add truongqv12/vit-agent-skill --list
```

### Cài một skill đã chọn từ index

```bash
npx skills add truongqv12/vit-agent-skill --skill <skill-name>
```

### Cài cho agent cụ thể hoặc cài tất cả

```bash
npx skills add truongqv12/vit-agent-skill --skill <skill-name> -a codex
npx skills add truongqv12/vit-agent-skill --skill '*' -g
```

## Thêm hoặc migrate skill

1. Inventory file, behavior invariant, dependency, license và provenance nguồn.
2. Normalize theo [Portable Skill Contract](docs/portable-skill-contract.md).
3. Tạo `skills/<portable-name>/SKILL.md` và `README.md`.
4. Chỉ thêm references/scripts/templates khi contract cần.
5. Cập nhật grouping trong `skills.sh.json` khi phù hợp.
6. Sinh lại index từ skill thực tế, rồi chạy validation và discovery:

```bash
python scripts/generate-skill-index.py
bash scripts/validate-skills.sh .
npx skills add . --list
```

Validator yêu cầu folder/name cùng kebab-case, có `README.md`, có `name` và
`description`, từ chối runtime coupling nguồn trong skill standalone, đồng thời
kiểm tra `docs/skills/README.md` không lệch khỏi package thực tế.

## License

MIT. Mỗi skill imported vẫn phải giữ license và provenance riêng theo evidence
nguồn.
