# Quality Gates

Run these checks before final response.

## Hard gates

| Gate | Pass condition |
|---|---|
| Output language | All user-facing output is Vietnamese unless user asked otherwise. |
| Figma gate | If Figma URLs exist, there is an evidence log showing MCP success/failure/unavailable/skipped. |
| Source confidence | Facts, assumptions, inferences, and open questions are separated. |
| No fake Figma analysis | No claim of Figma analysis without evidence rows. |
| No unsupported implementation | No invented API/database/infrastructure design. |
| Markdown source of truth | HTML mirrors Markdown. |

## BA completeness gates

| Gate | Pass condition |
|---|---|
| Business goal | At least one business goal or open question. |
| Roles | Roles/actors identified or open question. |
| Scope | In-scope/out-of-scope present or open question. |
| Flow | Main flow documented. |
| Business rules | Rules separated from requirements. |
| Data | Data fields/objects or open questions. |
| Permissions | Permission matrix or open questions. |
| State | States/transitions or open questions. |
| Acceptance criteria | Testable AC mapped to requirements. |
| Traceability | Important goals/sources map to FR/BR/AC/test focus. |
| Image evidence | If the source embeds screenshots, they are extracted to `assets/`, tagged `[FILE]`, and shown beside the relevant step (not ignored). |
| UI open questions | Every select with unknown catalog and every unclear button is captured as `UIQ-###` — none silently guessed. |
| Text vs image conflict | Any disagreement between narrative text and screenshots (e.g. step count) is raised as `[OPEN_QUESTION]`, not resolved arbitrarily. |

## Final response checklist

Final response must state in Vietnamese:

1. Files created/updated.
2. Whether Figma MCP was used.
3. Figma link counts: success, failed, unavailable, skipped.
4. Blocking open questions.
5. Quality gate status.


## Output package gates

Before final response, verify:

- Final deliverables are inside one short package folder under `ba-spec-output/` or a user-specified output path.
- Default package folder follows `ba-spec-output/{{YYYYMMDD}}/{{feature-slug}}/` unless the user requested another path.
- By default, the package contains only `feature-spec.md` and `feature-spec.html`.
- No final `feature-spec.md` or `feature-spec.html` is left as a loose root file.
- If Figma input exists, every original Figma URL is embedded as a clickable link in `feature-spec.md` and mirrored in `feature-spec.html`.
- If Figma input exists, the Figma evidence log is embedded in `feature-spec.md` and mirrored in `feature-spec.html`.
- Do not create `README.md`, `figma-links.md`, `evidence/`, `handoff/`, or `questions/` unless the user explicitly asked for separated companion files.
- Temporary helper scripts/files are deleted.
- No accidental root helper files remain: `extract_texts.py`, `generate_html.py`, `output.txt`, `extracted_texts.txt`, `figma_raw.json`, `markdown_cache.json`.
