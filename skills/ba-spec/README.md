# ba-spec

`ba-spec` là Agent Skill dành cho BA/PO/stakeholder muốn chuyển mô tả nghiệp vụ thành tài liệu đặc tả tính năng cho dev và QA.

Skill file (`SKILL.md`) được viết bằng tiếng Anh để agent dễ đọc, nhưng đầu ra mặc định của skill là tiếng Việt.

## Đầu ra chính

Skill tạo một folder ngắn gọn theo ngày và tên tính năng, nhưng **mặc định chỉ tạo 2 file cho team xem**:

```text
ba-spec-output/{{YYYYMMDD}}/{{feature-slug}}/
  feature-spec.md
  feature-spec.html
```

Ví dụ:

```text
ba-spec-output/20260623/cong-chung-dien-tu-truc-tiep/
  feature-spec.md
  feature-spec.html
```

Markdown là source of truth. HTML là bản trình bày để dev/QA/PO/stakeholder đọc.

Epic, Story, Figma links, Figma evidence, open questions, assumptions, checklist và traceability không tách thành nhiều file mặc định. Tất cả được nhúng vào `feature-spec.md` và render lại trong `feature-spec.html`.

Chỉ tạo thêm file phụ như `README.md`, `figma-links.md`, `evidence/figma-evidence-log.md`, `handoff/dev-handoff-checklist.md` khi người dùng yêu cầu rõ.

HTML template dùng Tailwind CDN và Mermaid.js CDN, không cần build step. Sơ đồ Mermaid trong Markdown sẽ được render trực tiếp trong HTML, kèm source fallback để đọc khi CDN bị chặn.

## Skill này dùng khi nào

Dùng khi cần:

- Tạo spec cho tính năng mới.
- Tạo spec nâng cấp tính năng cũ.
- Chuyển mô tả nghiệp vụ rời rạc thành tài liệu có cấu trúc.
- Chuẩn hóa yêu cầu từ Figma screenshot/link, file cũ, ticket, meeting note, PDF, Excel, HTML, Markdown.
- Hỏi lại các điểm thiếu trước khi dev implement.
- Tách business rule, data rule, permission, state transition, edge case, acceptance criteria.

## Skill này không dùng để làm gì

Không dùng để:

- Tự viết code production.
- Tự bịa API/database/architecture khi người dùng chưa cung cấp căn cứ.
- Biến Figma UI thành business rule đã xác nhận.
- Thay PO/stakeholder quyết định nghiệp vụ.

## Cấu trúc thư mục

```text
skills/
  ba-spec/
    SKILL.md
    README.md
    templates/
      feature-spec.md
      feature-spec.html
      clarification-questions.md
      dev-handoff-checklist.md
    references/
      figma-mcp-gate.md
      html-rendering-rules.md
      quality-gates.md
      ...
    scripts/
      install-figma-mcp.sh
      install-figma-mcp.ps1
    examples/
      input-business-text.md
      output-feature-spec.md
      output-feature-spec.html
    docs/
      ba-practice-research.md
      figma-mcp-setup.md
      agent-compatibility.md
```

## Cài bằng Skills CLI

```bash
npx skills add <your-github-org-or-user>/<your-repo> --skill ba-spec
```

Ghi chú: `npx skills add` thuộc hệ sinh thái Skills CLI. Không phải mọi agent đều bắt buộc dùng đúng lệnh này. Một số agent có thể dùng `.agents/skills`, `.claude/skills`, `~/.codex/skills`, hoặc cơ chế extension/plugin riêng.

## Cài thủ công

Copy folder `skills/ba-spec` vào thư mục skill của agent.

Ví dụ project-scoped phổ biến:

```text
.agents/skills/ba-spec/
```

Claude Code thường hỗ trợ:

```text
.claude/skills/ba-spec/
```

Codex thường hỗ trợ:

```text
.agents/skills/ba-spec/
```

## Cách gọi skill

Ví dụ:

```text
Use ba-spec.
Tạo đặc tả tính năng duyệt hoàn tiền cho user VIP.
Admin có thể duyệt hoặc từ chối.
Nếu duyệt thì trạng thái là approved.
Nếu từ chối thì bắt buộc nhập lý do.
```

Hoặc:

```text
$ba-spec
Hãy tạo feature-spec.md và feature-spec.html bằng tiếng Việt từ mô tả sau...
```

## Ví dụ input bằng Figma screenshot

```text
Use ba-spec.
Tôi gửi screenshot Figma của màn hình Refund Approval.
Hãy tạo spec cho dev/QA.
Chỉ dùng những gì nhìn thấy trong ảnh và đánh dấu phần nào là suy luận.
```

## Ví dụ input bằng Figma link

```text
Use ba-spec.
Figma link: <link>
Nếu MCP đọc được thì phân tích frame này.
Nếu không đọc được thì hỏi tôi fallback cần cung cấp gì.
```

Fallback gồm screenshot frame, export PNG/PDF, copy text từ Figma, mô tả màn hình, danh sách field/action/status.

## Ví dụ input bằng file liên quan

```text
Use ba-spec.
Tôi có file requirement cũ và meeting note mới.
Hãy tạo spec nâng cấp, chỉ rõ current behavior, requested change, impact và regression risk.
```

## Khi input thiếu

Với input quá ngắn như:

```text
Tạo chức năng duyệt refund.
```

Skill nên hỏi tối đa 10 câu ưu tiên. Nếu người dùng yêu cầu làm tiếp, skill vẫn tạo bản draft và đánh dấu các phần chưa rõ bằng `[OPEN_QUESTION]`.

## Cài Figma MCP

Xem:

```text
docs/figma-mcp-setup.md
```

Script macOS/Linux:

```bash
bash scripts/install-figma-mcp.sh
```

Script Windows:

```powershell
.\scripts\install-figma-mcp.ps1
```

Script chỉ tự động hóa phần có thể làm được. Riêng thao tác import plugin vào Figma Desktop vẫn cần làm thủ công.

## Quy tắc output tiếng Việt

Mặc định các file được agent tạo từ skill phải dùng tiếng Việt. Có thể giữ các mã sau bằng tiếng Anh để dễ parse:

- `FR-001`, `BR-001`, `AC-001`, `Q-001`.
- `[PROVIDED]`, `[FIGMA]`, `[FILE]`, `[INFERRED]`, `[ASSUMPTION]`, `[OPEN_QUESTION]`.
- Gherkin `Given / When / Then`.

---

## v1.1 Architecture Note: Short SKILL.md + references/

`ba-spec` now uses a router-style `SKILL.md` and case-specific rule files under `references/`.

Why:

- Agents often load `SKILL.md` first and may skip long instructions buried deep in a large file.
- Figma requires a hard evidence gate: if Figma links exist, the agent must either inspect them through MCP, record MCP failure/unavailability, or ask for fallback input.
- BA documentation rules are easier to maintain when separated from Figma, file handling, upgrade handling, HTML rendering, and quality gates.

Important files:

```text
references/
  input-classification.md
  figma-mcp-gate.md
  source-confidence-and-evidence.md
  ba-documentation-principles.md
  spec-generation-workflow.md
  html-rendering-rules.md
  feature-upgrade-rules.md
  file-handling-rules.md
  quality-gates.md
  output-language-rules.md
```

### Figma MCP hard gate

If the input contains a `figma.com` URL, the agent must not generate or edit `feature-spec.md` / `feature-spec.html` until it records one of these outcomes for each Figma link:

- `MCP_SUCCESS`
- `MCP_UNAVAILABLE`
- `MCP_FAILED`
- `USER_SKIPPED`
- `SCREENSHOT_ONLY`

The spec must include `Nhật ký bằng chứng Figma`.

If MCP is unavailable, the agent must say so directly and must not claim that Figma was analyzed.


## Mermaid trong HTML

`feature-spec.html` dùng Mermaid.js CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
```

Khi spec có `flowchart`, `stateDiagram-v2`, `sequenceDiagram` hoặc sơ đồ Mermaid khác, HTML phải render bằng `<div class="mermaid">...</div>` và giữ source trong `<details>` để fallback.


## Quy tắc package output

Skill không tạo loose files ở thư mục gốc. Đầu ra mặc định nằm trong package folder ngắn:

```text
ba-spec-output/20260623/cong-chung-dien-tu-truc-tiep/
```

Nếu cần group theo Epic, chỉ dùng khi người dùng yêu cầu rõ:

```text
ba-spec-output/cong-chung-dien-tu/20260623-cong-chung-dien-tu-truc-tiep/
```

Nếu agent cần tạo script tạm để extract Figma hoặc render HTML, script phải nằm trong `.tmp/` hoặc OS temp và bị xóa trước final response.

Nếu có Figma URL, `feature-spec.md` và `feature-spec.html` phải nhúng đầy đủ link gốc và nhật ký bằng chứng Figma để dev/QA mở lại thiết kế. Không tạo file Figma phụ nếu người dùng không yêu cầu.
