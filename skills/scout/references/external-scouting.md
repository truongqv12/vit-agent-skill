# External Scouting with a Permitted External Probe

Use an external agentic tool only when the user permits that execution path and
the runtime-native search is insufficient.

## Routing

```text
Native/local search sufficient  -> use content/name search, file reads, rg, wc, sed
External probe permitted        -> use an external CLI for bounded read-only scopes
Heavier autonomous tool wanted  -> only on explicit user request, through a
                                   dedicated orchestration capability
```

Ordinary scouting must not invoke a heavier autonomous browsing/agent tool
directly. If the user explicitly wants one, route through a dedicated
orchestration capability that owns its version, authentication, and safety
gates. Absent such a capability, decline and continue with native scouting.

## External CLI example (OpenCode)

```bash
opencode run "Find all payment-related files in lib/ and api/" --model opencode/grok-code
```

## Installation check

Verify the external tool before using it:

```bash
command -v opencode
```

If it is not installed, continue with native content/name search, file reads,
and scoped shell searches. Use parallel-agent delegation only when the user
explicitly requested or permitted subagents.

## Parallel external commands

Prefer parallel runtime tool calls when available. If only shell is available,
run independent one-shot searches with non-overlapping scopes:

```bash
opencode run "Read-only: search db/ and migrations/ for migration files" --model opencode/grok-code
opencode run "Read-only: search lib/ and src/ for database schema files" --model opencode/grok-code
opencode run "Read-only: search config/ for database configuration" --model opencode/grok-code
```

Do not dispatch multiple searches against the same directories. External tools
must stay read-only for scouting.

## Prompt guidelines

- Name exact directories to search.
- Request file paths with one-line relevance notes.
- State that the task is read-only.
- Set scope boundaries and exclusions.
- Ask for relationships only when they affect the task.

## Reading file content

Use local chunking for large files. Do not send whole private files to an
external CLI to bypass a context limit.

```bash
wc -l path/to/file1.ts path/to/file2.ts
sed -n '1,500p' large-file.ts
sed -n '501,1000p' large-file.ts
```

- Files under 500 lines: read directly.
- Files 500-1500 lines: 2-3 chunks.
- Files over 1500 lines: roughly 500-line chunks.

## Error handling

- Treat a non-zero exit code as failure.
- Do not retry a failed external probe automatically.
- After two external failures, continue with native/local scouting.
- Note incomplete directory coverage in the report.
