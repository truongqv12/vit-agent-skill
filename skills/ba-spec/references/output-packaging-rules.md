# Output Packaging Rules

Use these rules for every `ba-spec` run that creates deliverables.

## Core rule

Do not create final deliverables as loose files in the repository/project root. Always create one short output folder and put the final deliverables inside it.

## Product decision

The default handoff must stay simple for team review:

```text
feature-spec.md
feature-spec.html
```

Do **not** create a pile of companion files by default. A BA handoff should be easy to send to dev/QA/PO: one Markdown source of truth and one HTML review file.

## Design decision

Keep the folder path short. Do not put full Epic, Story, and Feature names into the same folder name. Long paths are hard to read, easy to break on Windows, and inconvenient for dev/QA handoff.

Epic, Story, Feature name, package ID, Figma links, evidence logs, open questions, assumptions, checklist, and traceability must be stored inside:

- `feature-spec.md`
- `feature-spec.html`

The filesystem path is only for organization, not for carrying all BA meaning.

## Default output root

Use this root unless the user provides another path:

```text
ba-spec-output/
```

## Default package path

Use this short default pattern:

```text
ba-spec-output/{{YYYYMMDD}}/{{feature-slug}}/
```

Example:

```text
ba-spec-output/20260623/cong-chung-dien-tu-truc-tiep/
```

This is the preferred pattern for normal usage.

## Optional grouped-by-Epic path

Use this only when the user explicitly asks to group output by Epic or when the current workspace already uses Epic folders:

```text
ba-spec-output/{{epic-slug}}/{{YYYYMMDD}}-{{feature-slug}}/
```

Example:

```text
ba-spec-output/cong-chung-dien-tu/20260623-cong-chung-dien-tu-truc-tiep/
```

Do not create deeper nesting such as `epic/story/feature/date` unless the user requests it.

## Collision handling

If the target package already exists, do not overwrite silently. Use a numeric suffix:

```text
ba-spec-output/20260623/cong-chung-dien-tu-truc-tiep-02/
ba-spec-output/20260623/cong-chung-dien-tu-truc-tiep-03/
```

If the user asks to update an existing package, update that exact package and record the change in the metadata section of `feature-spec.md`.

## Slug rules

- Lowercase.
- Remove Vietnamese accents.
- Replace spaces and punctuation with `-`.
- Collapse repeated hyphens.
- Trim leading/trailing hyphens.
- Keep only `a-z`, `0-9`, and `-`.
- Maximum recommended feature slug length: 48 characters.
- Maximum recommended Epic slug length in grouped mode: 40 characters.
- If the feature name is longer than 48 characters, shorten it to a meaningful phrase and record the full feature name in `feature-spec.md`.

Recommended examples:

| Full Vietnamese name | Feature slug |
|---|---|
| Quy trình Công chứng điện tử trực tiếp | `cong-chung-dien-tu-truc-tiep` |
| Duyệt yêu cầu hoàn tiền cho user VIP | `duyet-hoan-tien-vip` |
| Xác thực CCCD qua NFC hoặc VNeID | `xac-thuc-cccd-nfc-vneid` |

## Epic / Story metadata rules

The package path should not try to encode the entire BA hierarchy. Instead, the spec metadata in `feature-spec.md` and `feature-spec.html` must include:

- Epic ID or Epic name, if known.
- Story ID or Story name, if known.
- Feature name.
- Package ID.
- Created date.
- Output path.

If the user does not provide Epic or Story, infer conservatively and mark it as `[ASSUMPTION]` in `feature-spec.md`.

## Default package structure

Use this by default:

```text
{{package-folder}}/
  feature-spec.md
  feature-spec.html
```

The two files must contain all review/handoff material needed by the team.

### Allowed `assets/` folder (images only)

When the input file embeds screenshots/diagrams (see `file-image-extraction-rules.md`), an `assets/` folder is allowed even by default, because the images are `[FILE]` evidence the spec must show:

```text
{{package-folder}}/
  feature-spec.md
  feature-spec.html
  assets/            # extracted screenshots, referenced via relative paths
```

If the user also asks for a PDF, `feature-spec.pdf` may remain in the package too (see `export-pdf-rules.md`). Do not add any other companion files unless the user explicitly asks.

## What must be embedded in the two default files

When Figma input exists, embed these sections in both files:

- `Danh sách link Figma gốc`
- `Nhật ký bằng chứng Figma`
- MCP status per link
- Original clickable Figma URL per link
- Node ID/file key when available
- Extracted UI evidence or fallback reason

When open questions exist, embed:

- `Câu hỏi mở`
- Blocking/non-blocking flag
- Needed owner/role

When dev/QA handoff is needed, embed:

- `Dev / QA handoff notes`
- `Quality checklist`

## Optional companion files

Only create extra files when the user explicitly asks for separated artifacts, examples:

- “tách riêng checklist”
- “xuất thêm figma-links.md”
- “tạo evidence log riêng”
- “tạo README package”
- “xuất bộ handoff đầy đủ nhiều file”

Optional separated structure:

```text
{{package-folder}}/
  feature-spec.md
  feature-spec.html
  README.md                         # optional only
  figma-links.md                    # optional only
  evidence/figma-evidence-log.md    # optional only
  handoff/dev-handoff-checklist.md  # optional only
  questions/clarification-questions.md # optional only
```

Temporary workspace, if needed during generation:

```text
{{package-folder}}/.tmp/            # must be deleted before final response
```

## Final response

Final response must link to the two final deliverables, not to loose root files.

Final response must include the short package path, for example:

```text
ba-spec-output/20260623/cong-chung-dien-tu-truc-tiep/
```

Final response must explicitly confirm:

- Only `feature-spec.md` and `feature-spec.html` were created by default, unless the user requested extras.
- Temporary helper files were cleaned up.
