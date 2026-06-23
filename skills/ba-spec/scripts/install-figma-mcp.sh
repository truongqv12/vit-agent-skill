#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-$(pwd)}"
MCP_JSON="$PROJECT_DIR/.mcp.json"
VSCODE_DIR="$PROJECT_DIR/.vscode"
VSCODE_MCP_JSON="$VSCODE_DIR/mcp.json"
PLUGIN_DIR="$PROJECT_DIR/.figma-mcp-go"
PLUGIN_ZIP="$PLUGIN_DIR/plugin.zip"
PLUGIN_URL="https://github.com/vkhanhqui/figma-mcp-go/releases/latest/download/plugin.zip"

echo "== ba-spec: figma-mcp-go setup =="
echo "Project directory: $PROJECT_DIR"

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1"
    return 1
  fi
}

echo ""
echo "Checking Node/npm/npx..."
need_cmd node || { echo "Install Node.js 18+ before continuing."; exit 1; }
need_cmd npm || { echo "Install npm before continuing."; exit 1; }
need_cmd npx || { echo "Install npx before continuing."; exit 1; }

echo "Node: $(node -v)"
echo "npm: $(npm -v)"
echo "npx: $(npx -v)"

echo ""
echo "Testing @vkhanhqui/figma-mcp-go package availability..."
npx -y @vkhanhqui/figma-mcp-go@latest --help >/dev/null 2>&1 || true
echo "Package check attempted. Some MCP servers do not expose --help; continuing."

echo ""
echo "Writing generic MCP config: $MCP_JSON"
cat > "$MCP_JSON" <<'JSON'
{
  "mcpServers": {
    "figma-mcp-go": {
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go@latest"]
    }
  }
}
JSON

echo ""
echo "Writing VS Code/Cursor style MCP config: $VSCODE_MCP_JSON"
mkdir -p "$VSCODE_DIR"
cat > "$VSCODE_MCP_JSON" <<'JSON'
{
  "servers": {
    "figma-mcp-go": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go@latest"]
    }
  }
}
JSON

echo ""
if command -v claude >/dev/null 2>&1; then
  echo "Claude Code detected. Adding MCP server to project scope..."
  claude mcp add -s project figma-mcp-go -- npx -y @vkhanhqui/figma-mcp-go@latest || {
    echo "Claude MCP add failed. You can still use .mcp.json."
  }
else
  echo "Claude Code CLI not detected. Skipping Claude-specific setup."
fi

echo ""
if command -v codex >/dev/null 2>&1; then
  echo "Codex CLI detected. Adding MCP server..."
  codex mcp add figma-mcp-go -- npx -y @vkhanhqui/figma-mcp-go@latest || {
    echo "Codex MCP add failed. You can still use .mcp.json if supported by your setup."
  }
else
  echo "Codex CLI not detected. Skipping Codex-specific setup."
fi

echo ""
echo "Attempting to download Figma plugin.zip..."
mkdir -p "$PLUGIN_DIR"

if command -v curl >/dev/null 2>&1; then
  if curl -L --fail "$PLUGIN_URL" -o "$PLUGIN_ZIP"; then
    echo "Downloaded plugin zip to: $PLUGIN_ZIP"
  else
    echo "Could not download plugin.zip automatically."
    echo "Manual download: open the figma-mcp-go GitHub releases page and download plugin.zip."
  fi
else
  echo "curl not found. Manual download required."
fi

echo ""
echo "Manual step required in Figma Desktop:"
echo "1. Extract plugin.zip if downloaded."
echo "2. Open Figma Desktop."
echo "3. Go to Plugins -> Development -> Import plugin from manifest."
echo "4. Select manifest.json from the extracted plugin folder."
echo "5. Run the plugin inside the Figma file you want the agent to inspect."
echo ""
echo "Setup complete for the automatable parts."
