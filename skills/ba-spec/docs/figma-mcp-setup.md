# Figma MCP Setup cho `ba-spec`

`ba-spec` có thể dùng Figma theo 3 cách:

1. Screenshot/export frame.
2. Link Figma qua MCP.
3. Mô tả thủ công khi không dùng được MCP.

## 1. Lựa chọn MCP

### Option A — Official Figma MCP

Figma có MCP server chính thức tại remote endpoint:

```text
https://mcp.figma.com/mcp
```

Một số client như Claude Code, Codex, Gemini CLI, VS Code, Cursor có hướng dẫn riêng.

Nguồn:

- Figma Help Center: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server
- Figma MCP server guide: https://github.com/figma/mcp-server-guide

### Option B — Community `figma-mcp-go`

Repo tham khảo:

```text
https://github.com/vkhanhqui/figma-mcp-go
```

Theo mô tả repo, hướng này dùng plugin bridge với Figma Desktop, có thể chạy MCP server qua:

```bash
npx -y @vkhanhqui/figma-mcp-go@latest
```

Điểm cần lưu ý:

- Có phần server chạy bằng `npx`.
- Có phần plugin trong Figma Desktop.
- Không thể tự động hóa hoàn toàn bước import plugin vì phải thao tác trong UI Figma.
- Script trong repo này chỉ tự động hóa phần cấu hình MCP và tải plugin nếu URL release hoạt động.

## 2. Điều kiện cần

- Node.js 18+.
- npm/npx.
- Figma Desktop nếu dùng `figma-mcp-go`.
- Quyền truy cập Figma file.
- Agent/client có hỗ trợ MCP.

## 3. Cấu hình generic `.mcp.json` cho `figma-mcp-go`

```json
{
  "mcpServers": {
    "figma-mcp-go": {
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go@latest"]
    }
  }
}
```

## 4. Cấu hình official Figma MCP

Generic HTTP config:

```json
{
  "mcpServers": {
    "figma": {
      "url": "https://mcp.figma.com/mcp"
    }
  }
}
```

Claude Code manual setup:

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

Gemini CLI extension theo guide chính thức:

```bash
gemini extensions install https://github.com/figma/mcp-server-guide
```

Sau đó trong Gemini CLI:

```text
/mcp auth figma
```

## 5. Cách test

Mở Figma file, chọn frame cần phân tích, sau đó hỏi agent:

```text
Use ba-spec.
Đọc Figma frame hiện tại qua MCP nếu có thể.
Chỉ tóm tắt text, button, field, status, state và interaction nhìn thấy được.
Không suy diễn business rule nếu không có căn cứ.
```

Kỳ vọng:

- Agent nhận được context từ Figma.
- Agent phân loại dữ liệu là `[FIGMA]`.
- Agent hỏi lại business rule còn thiếu.

## 6. Troubleshooting

### MCP server không chạy

Kiểm tra:

```bash
node -v
npm -v
npx -v
```

Thử chạy:

```bash
npx -y @vkhanhqui/figma-mcp-go@latest
```

### Agent không đọc được Figma

Kiểm tra:

- Figma Desktop đang mở nếu dùng plugin bridge.
- Plugin đã import và đang chạy.
- Đúng file/frame đã được chọn.
- MCP config nằm đúng chỗ agent đọc.
- Agent/client đã restart sau khi sửa config.

### Không đọc được link Figma

Một số MCP flow cần node/frame selection hoặc node-id từ link. Nếu link không đọc được:

- Mở file thủ công trong Figma.
- Select đúng frame/layer.
- Copy link to selection.
- Chạy lại prompt.

## 7. Fallback nếu không dùng MCP

Cung cấp một trong các input sau:

- Screenshot frame.
- Export PNG/PDF.
- Copy text từ Figma.
- List screen/action/status.
- Mô tả flow nghiệp vụ bằng văn xuôi.

## 8. Nguyên tắc dùng Figma trong BA spec

Figma là nguồn cho UI/design evidence, không phải luôn là nguồn xác nhận business rule.

Ví dụ:

```text
[FIGMA] Có button "Từ chối" trên màn hình duyệt hoàn tiền.
[INFERRED] Có khả năng hệ thống hỗ trợ hành động từ chối.
[OPEN_QUESTION] Khi từ chối thì trạng thái chính xác chuyển thành gì?
```

---

## ba-spec v1.1: Mandatory Figma Evidence Gate

When using this skill, any input containing a `figma.com` URL must pass the Figma evidence gate before the agent writes or edits the feature spec.

The agent must record one outcome per link:

| Outcome | Meaning |
|---|---|
| `MCP_SUCCESS` | MCP was used and UI evidence was extracted. |
| `MCP_UNAVAILABLE` | The current agent environment exposes no usable Figma MCP tool/server. |
| `MCP_FAILED` | MCP was attempted but failed. |
| `USER_SKIPPED` | User explicitly asked to skip Figma/MCP. |
| `SCREENSHOT_ONLY` | No MCP extraction, but screenshots/exported frames were analyzed. |

Required spec section:

```markdown
## Nhật ký bằng chứng Figma

| Figma ID | Label | URL / Node | Kết quả MCP | Bằng chứng UI trích xuất | Ghi chú / fallback |
|---|---|---|---|---|---|
```

If this section is missing while Figma URLs were provided, the generated spec is incomplete.
