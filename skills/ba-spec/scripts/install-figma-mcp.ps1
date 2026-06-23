param(
  [string]$ProjectDir = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$McpJson = Join-Path $ProjectDir ".mcp.json"
$VsCodeDir = Join-Path $ProjectDir ".vscode"
$VsCodeMcpJson = Join-Path $VsCodeDir "mcp.json"
$PluginDir = Join-Path $ProjectDir ".figma-mcp-go"
$PluginZip = Join-Path $PluginDir "plugin.zip"
$PluginUrl = "https://github.com/vkhanhqui/figma-mcp-go/releases/latest/download/plugin.zip"

Write-Host "== ba-spec: figma-mcp-go setup =="
Write-Host "Project directory: $ProjectDir"

function Test-Command {
  param([string]$Name)
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  return $null -ne $cmd
}

Write-Host ""
Write-Host "Checking Node/npm/npx..."

if (-not (Test-Command "node")) { Write-Error "Missing node. Install Node.js 18+ before continuing." }
if (-not (Test-Command "npm")) { Write-Error "Missing npm. Install npm before continuing." }
if (-not (Test-Command "npx")) { Write-Error "Missing npx. Install npx before continuing." }

Write-Host "Node: $(node -v)"
Write-Host "npm: $(npm -v)"
Write-Host "npx: $(npx -v)"

Write-Host ""
Write-Host "Testing @vkhanhqui/figma-mcp-go package availability..."
try {
  npx -y @vkhanhqui/figma-mcp-go@latest --help | Out-Null
} catch {
  Write-Host "Package check attempted. Some MCP servers do not expose --help; continuing."
}

Write-Host ""
Write-Host "Writing generic MCP config: $McpJson"
@'
{
  "mcpServers": {
    "figma-mcp-go": {
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go@latest"]
    }
  }
}
'@ | Set-Content -Encoding UTF8 $McpJson

Write-Host ""
Write-Host "Writing VS Code/Cursor style MCP config: $VsCodeMcpJson"
New-Item -ItemType Directory -Force -Path $VsCodeDir | Out-Null
@'
{
  "servers": {
    "figma-mcp-go": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go@latest"]
    }
  }
}
'@ | Set-Content -Encoding UTF8 $VsCodeMcpJson

Write-Host ""
if (Test-Command "claude") {
  Write-Host "Claude Code detected. Adding MCP server to project scope..."
  try { claude mcp add -s project figma-mcp-go -- npx -y @vkhanhqui/figma-mcp-go@latest }
  catch { Write-Host "Claude MCP add failed. You can still use .mcp.json." }
} else {
  Write-Host "Claude Code CLI not detected. Skipping Claude-specific setup."
}

Write-Host ""
if (Test-Command "codex") {
  Write-Host "Codex CLI detected. Adding MCP server..."
  try { codex mcp add figma-mcp-go -- npx -y @vkhanhqui/figma-mcp-go@latest }
  catch { Write-Host "Codex MCP add failed. You can still use .mcp.json if supported by your setup." }
} else {
  Write-Host "Codex CLI not detected. Skipping Codex-specific setup."
}

Write-Host ""
Write-Host "Attempting to download Figma plugin.zip..."
New-Item -ItemType Directory -Force -Path $PluginDir | Out-Null
try {
  Invoke-WebRequest -Uri $PluginUrl -OutFile $PluginZip
  Write-Host "Downloaded plugin zip to: $PluginZip"
} catch {
  Write-Host "Could not download plugin.zip automatically."
  Write-Host "Manual download: open the figma-mcp-go GitHub releases page and download plugin.zip."
}

Write-Host ""
Write-Host "Manual step required in Figma Desktop:"
Write-Host "1. Extract plugin.zip if downloaded."
Write-Host "2. Open Figma Desktop."
Write-Host "3. Go to Plugins -> Development -> Import plugin from manifest."
Write-Host "4. Select manifest.json from the extracted plugin folder."
Write-Host "5. Run the plugin inside the Figma file you want the agent to inspect."
Write-Host ""
Write-Host "Setup complete for the automatable parts."
