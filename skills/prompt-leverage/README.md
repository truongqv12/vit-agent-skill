# prompt-leverage

Strengthen raw or underspecified user prompts into execution-ready instruction sets
for AI coding agents (Claude Code, Antigravity, Cursor, Amp, etc.) without altering
the underlying user intent.

[`SKILL.md`](./SKILL.md) is the authority for router behavior, workflow steps,
transformation rules, and quality bars. This README carries provenance, framework,
and usage notes.

## Provenance & Portability

- **Standalone.** Pure instructional and script-assisted prompt optimization.
- No dependency on vendor runtime CLI or proprietary services.
- Works across all major agentic execution environments.

## Framework Overview

Synthesizes flywheel execution controls with systematic prompting principles:

```text
Goal -> Context -> Work Style -> Tool Rules -> Output Contract -> Verification -> Done
```

1. **Objective**: Define success in observable terms.
2. **Context**: Specify relevant files, URLs, constraints, and boundaries.
3. **Work Style**: Set intensity (Light / Standard / Deep) and reasoning depth.
4. **Tool Rules**: Define file inspection, tests, or external tool expectations.
5. **Output Contract**: Structure, format, and schema expectations.
6. **Verification**: Explicit correctness checks and edge case verification.
7. **Done Criteria**: Explicit stopping conditions.

## Scripts & Automation

- `scripts/augment_prompt.py`: Deterministic first-pass prompt rewrite utility.

## References

- [`references/framework.md`](./references/framework.md)
- [`agents/openai.yaml`](./agents/openai.yaml)
