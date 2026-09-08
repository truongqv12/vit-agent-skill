# Parallel Exploration

Patterns for launching multiple agents in parallel to scout the codebase, verify
implementation, and coordinate multi-phase fixes — always through whatever
delegation capability the runtime exposes, with a native fallback.

## Runtime rules

- Use the runtime's **delegation** capability for subagents; native names differ
  by runtime (e.g. Claude Code exposes an `Explore` agent role). If the
  delegation tool is deferred, discover it through the runtime's tool-discovery
  mechanism first.
- Do not spawn agents just because a step mentions them. Some runtimes require
  the actual user request to explicitly ask for subagents, delegation, or
  parallel work.
- If delegation is unavailable or not permitted, do the scout/verification in
  the main agent with native search, scoped reads, and shell.

## Parallel scouting

Launch multiple exploration agents simultaneously when locating:

- Related files across different areas.
- Similar implementations/patterns.
- Dependencies and usage.

**Pattern:** delegate one exploration agent per non-overlapping area (for
example: auth files in `src/`, API routes handling users, tests for the auth
module) in a single assistant turn when the runtime supports parallel calls.

## Parallel verification

Prefer direct shell verification in the main agent. Delegate verification only
when the user explicitly requested parallel delegation and the runtime has a
suitable worker role. Run typecheck, lint, build, and tests; split across
workers only when delegation is permitted.

## Task-coordinated parallel (Moderate+)

For multi-phase fixes, use a live **task-tracking** capability to coordinate
parallel agents when available; otherwise track scopes and status in the active
plan.

**Pattern — parallel issue trees:**

- Create separate plan items per independent issue.
- Mark each issue's diagnose item as blocking its fix item.
- Add a final integration-verify item blocked by all issue fixes.
- Spawn one agent per issue tree through the delegation capability when
  permitted.

Agents claim work through the live surface when supported. Otherwise the
orchestrator assigns non-overlapping scopes from the active plan and advances
blocked work only after prerequisites complete.

## When to use parallel

| Scenario | Strategy |
|----------|----------|
| Root cause unclear, multiple suspects | 2-3 exploration agents on different areas |
| Multi-module fix | Explore each module in parallel when delegation is permitted |
| After implementation | Shell verification (typecheck + lint + build); delegate only if permitted |
| Before commit | Shell verification (test + build + lint); delegate only if permitted |
| 2+ independent issues | Plan tree per issue + delegated implementation agents |

## Resource limits

- Max ~3 parallel agents recommended (system resources).
- Keep prompts concise to avoid context bloat.
- Check the live surface for unblocked work when supported; otherwise read the
  active plan.
