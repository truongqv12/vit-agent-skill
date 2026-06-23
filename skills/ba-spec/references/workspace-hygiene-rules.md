# Workspace Hygiene Rules

Use these rules whenever the agent creates helper scripts, temporary extraction files, generated intermediates, or HTML conversion helpers.

## Core rule

Temporary helper artifacts must not be left in the user's project root.

Bad examples:

```text
extract_texts.py
generate_html.py
output.txt
extracted_texts.txt
figma_raw.json
markdown_cache.json
```

## Where temporary files may be created

Use one of these locations only:

1. OS temp directory with a `ba-spec-` prefix.
2. Package-local temporary directory:

```text
{{package-folder}}/.tmp/
```

Do not create helper scripts in the current working directory unless that directory is the package `.tmp/` directory.

## Cleanup requirement

Before final response:

1. Move final deliverables into the package directory.
2. Delete package `.tmp/`.
3. Delete any accidental root helper files created during the run.
4. Do not delete user-provided input files.
5. Do not delete files that existed before the run unless the user explicitly asked.

## Package-local generated files

By default, only these may remain because they are final deliverables:

```text
feature-spec.md
feature-spec.html
```

Extra package-local files such as `README.md`, `figma-links.md`, `evidence/figma-evidence-log.md`, `handoff/dev-handoff-checklist.md`, or `questions/clarification-questions.md` may remain only if the user explicitly requested separated companion files.

If the user did not ask for companion files, embed that information into `feature-spec.md` and `feature-spec.html` instead of creating extra files.

## Dependency rule

Do not run package installs such as `pip install markdown`, `npm install`, or similar in the user's project without explicit need and without explaining it. Prefer:

- existing skill templates,
- built-in language/runtime libraries,
- temporary script in `.tmp/`,
- no dependency install.

If a dependency install is unavoidable, ask the user or clearly state why it is needed.

## Final cleanup statement

The final response must include a Vietnamese cleanup statement, for example:

```text
Đã dọn file tạm: không còn helper script như extract_texts.py/generate_html.py ở thư mục gốc.
```
