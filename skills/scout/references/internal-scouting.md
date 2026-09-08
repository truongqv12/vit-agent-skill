# Internal Scouting with Parallel Agents

Use parallel scout agents when SCALE is high (roughly ≥ 6 scopes) or external
tools are unavailable, and only when the active runtime permits a delegation
capability.

## Delegation gate

Do not spawn agents only because this reference mentions them. Spawn only when
ALL of these hold:

- The user explicitly asked for subagents, delegation, or parallel agent work.
- The active runtime exposes a delegation capability.
- Each agent has a distinct scope and useful work to do.

If any condition is false, scout in the main agent with native content/name
search, scoped file reads, and shell.

## How it works

Spawn multiple scout agents through the runtime's delegation capability to
search codebase segments in parallel. On Claude Code this is the native delegate
call with the `Explore` agent type. On runtimes where the parallel-agent role is
a deferred tool, discover it through the runtime's tool-search first, then spawn
it. Do not set a model override; the scout role owns its runtime model. Close
completed agents after collecting results so they free concurrency slots.

## Prompt template

```
Quickly scout {DIRECTORY} for files related to: {USER_PROMPT}

Instructions:
- Search for relevant files matching the task (read-only)
- List files with brief descriptions
- Timeout: 3 minutes max, skip if reached

Report format:
## Found Files
- `path/file.ext` - description

## Patterns
- Key patterns observed
```

## Spawning strategy

### Directory division

Split the codebase logically, for example:

- `src/` — source code
- `lib/` — libraries
- `tests/` — test files
- `config/` — configuration
- `api/` — API routes

### Parallel execution

- Spawn all agents in a single turn when the runtime supports parallel tool
  calls.
- Each agent gets a distinct directory scope; no overlap.

## Example

User prompt: "Find authentication-related files"

```
Agent 1: Scout src/auth/, src/middleware/ for auth files
Agent 2: Scout src/api/, src/routes/ for auth endpoints
Agent 3: Scout tests/ for auth tests
Agent 4: Scout lib/, utils/ for auth utilities
Agent 5: Scout config/ for auth configuration
Agent 6: Scout types/, interfaces/ for auth types
```

## Timeout handling

- 3-minute timeout per agent.
- Skip non-responding agents; do not restart them.
- Aggregate whatever results are available and note gaps.

## Reading file content

Chunk large files to stay within context limits (keep well under the agent's
window).

### Step 1: Get line counts

```bash
wc -l path/to/file1.ts path/to/file2.ts path/to/file3.ts
```

### Step 2: Calculate chunks

- Target ~500 lines per chunk.
- Max per agent: 3-5 small files OR one large file chunked.

```
chunks = ceil(total_lines / 500)
lines_per_chunk = ceil(total_lines / chunks)
```

### Step 3: Read chunks

- Files < 500 lines: read directly.
- Files 500-1500 lines: 2-3 chunks.
- Files > 1500 lines: `ceil(lines / 500)` chunks, e.g. `sed -n '1,500p' file`.

Delegate chunk reading only when the user explicitly requested parallel
delegation and the runtime has an appropriate worker role.

## Result aggregation

1. Deduplicate file paths.
2. Merge descriptions.
3. Note gaps and timeouts.
4. List unresolved questions.
