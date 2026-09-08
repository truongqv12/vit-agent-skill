#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"

echo "Checking skills under: $ROOT/skills"

if [ ! -d "$ROOT/skills" ]; then
  echo "Missing skills/ directory" >&2
  exit 1
fi

found=0
for skill_dir in "$ROOT"/skills/*; do
  [ -d "$skill_dir" ] || continue
  found=$((found + 1))
  name="$(basename "$skill_dir")"
  skill_file="$skill_dir/SKILL.md"
  readme_file="$skill_dir/README.md"

  if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "FAIL: $name directory must use portable kebab-case" >&2
    exit 1
  fi
  if [ ! -f "$skill_file" ]; then
    echo "FAIL: $name missing SKILL.md" >&2
    exit 1
  fi
  if [ ! -f "$readme_file" ]; then
    echo "FAIL: $name missing README.md" >&2
    exit 1
  fi

  first_line="$(head -n 1 "$skill_file" | tr -d '\r')"
  if [ "$first_line" != "---" ]; then
    echo "FAIL: $name SKILL.md must start with YAML frontmatter" >&2
    exit 1
  fi
  closing_frontmatter_line="$(awk 'NR > 1 && /^---[[:space:]]*$/ { print NR; exit }' "$skill_file")"
  if [ -z "$closing_frontmatter_line" ]; then
    echo "FAIL: $name SKILL.md missing closing YAML frontmatter delimiter" >&2
    exit 1
  fi
  frontmatter="$(awk 'NR == 1 { next } /^---[[:space:]]*$/ { exit } { print }' "$skill_file")"
  if ! grep -q '^name:' <<< "$frontmatter"; then
    echo "FAIL: $name SKILL.md missing name frontmatter" >&2
    exit 1
  fi
  if ! grep -q '^description:' <<< "$frontmatter"; then
    echo "FAIL: $name SKILL.md missing description frontmatter" >&2
    exit 1
  fi

  declared_name="$(sed -n 's/^name:[[:space:]]*//p' <<< "$frontmatter" | head -n 1)"
  declared_name="$(sed -E 's/[[:space:]]+#.*$//' <<< "$declared_name")"
  declared_name="$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<< "$declared_name")"
  declared_name="${declared_name#\"}"
  declared_name="${declared_name%\"}"
  declared_name="${declared_name#\'}"
  declared_name="${declared_name%\'}"
  if [ "$declared_name" != "$name" ]; then
    echo "FAIL: $name SKILL.md name '$declared_name' must match its directory" >&2
    exit 1
  fi

  if grep -Eq '/ak:[[:alnum:]_-]+' "$skill_file"; then
    echo "FAIL: $name SKILL.md contains an AgentKit slash-command dependency" >&2
    exit 1
  fi
  if grep -Eq '(^|[[:space:]`])ak[[:space:]]+[[:alnum:]_-]+' "$skill_file"; then
    echo "FAIL: $name SKILL.md contains an AgentKit CLI dependency" >&2
    exit 1
  fi

  portability="$(sed -n 's/^[[:space:]]*portability:[[:space:]]*//p' <<< "$frontmatter" | head -n 1)"
  portability="${portability#\"}"
  portability="${portability%\"}"
  portability="${portability#\'}"
  portability="${portability%\'}"
  if [ "$portability" = "standalone" ]; then
    while IFS= read -r runtime_doc; do
      rel_doc="${runtime_doc#"$skill_dir/"}"
      if grep -Eq '/ak:[[:alnum:]_-]+' "$runtime_doc"; then
        echo "FAIL: $name $rel_doc contains an AgentKit slash-command dependency" >&2
        exit 1
      fi
      if grep -Eq '(^|[[:space:]`])ak[[:space:]]+[[:alnum:]_-]+' "$runtime_doc"; then
        echo "FAIL: $name $rel_doc contains an AgentKit CLI dependency" >&2
        exit 1
      fi
      if grep -Eq '\.agentkit/|localhost:3456|[A-Za-z]:\\Users\\[^\\]+\\' "$runtime_doc"; then
        echo "FAIL: $name $rel_doc contains a source-private runtime path or service" >&2
        exit 1
      fi
    done < <(
      find "$skill_dir" -type f \
        \( -path '*/SKILL.md' -o -path '*/README.md' -o -path '*/references/*.md' -o -path '*/templates/*.md' \) \
        -print
    )
  fi

  if [ "$name" = "ba-spec" ]; then
    required=(
      "references/output-packaging-rules.md"
      "references/workspace-hygiene-rules.md"
      "references/figma-link-reference-rules.md"
      "templates/feature-spec.md"
      "templates/feature-spec.html"
    )
    for rel in "${required[@]}"; do
      if [ ! -f "$skill_dir/$rel" ]; then
        echo "FAIL: $name missing $rel" >&2
        exit 1
      fi
    done
    if ! grep -q 'ba-spec-output' "$skill_file"; then
      echo "FAIL: ba-spec SKILL.md missing output package rule" >&2
      exit 1
    fi
  fi

  if [ "$name" = "vit-plan" ]; then
    required=(
      "templates/plan.md"
      "templates/phase.md"
      "references/plan-organization.md"
      "references/output-standards.md"
      "scripts/plan-tool.py"
      "scripts/test-plan-tool.py"
    )
    for rel in "${required[@]}"; do
      if [ ! -f "$skill_dir/$rel" ]; then
        echo "FAIL: $name missing $rel" >&2
        exit 1
      fi
    done
    if ! grep -q 'schemaVersion: "vit-plan/v1"' "$skill_dir/templates/plan.md"; then
      echo "FAIL: vit-plan plan template missing vit-plan/v1 schema" >&2
      exit 1
    fi
    if ! grep -q 'schemaVersion: "vit-plan/v1"' "$skill_dir/templates/phase.md"; then
      echo "FAIL: vit-plan phase template missing vit-plan/v1 schema" >&2
      exit 1
    fi
  fi

  echo "OK: $name"
done

if [ "$found" -eq 0 ]; then
  echo "No skills found" >&2
  exit 1
fi

python_cmd=""
if command -v python3 >/dev/null 2>&1; then
  python_cmd="python3"
elif command -v python >/dev/null 2>&1; then
  python_cmd="python"
else
  echo "Python 3 is required to verify the generated skill index" >&2
  exit 1
fi

"$python_cmd" "$ROOT/scripts/generate-skill-index.py" --root "$ROOT" --check

echo "All skill checks passed."
