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
  if [ ! -f "$skill_file" ]; then
    echo "FAIL: $name missing SKILL.md" >&2
    exit 1
  fi
  if ! grep -q '^name:' "$skill_file"; then
    echo "FAIL: $name SKILL.md missing name frontmatter" >&2
    exit 1
  fi
  if ! grep -q '^description:' "$skill_file"; then
    echo "FAIL: $name SKILL.md missing description frontmatter" >&2
    exit 1
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

  echo "OK: $name"
done

if [ "$found" -eq 0 ]; then
  echo "No skills found" >&2
  exit 1
fi

echo "All skill checks passed."
