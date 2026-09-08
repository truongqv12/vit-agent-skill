# Commit Workflow

Run inline, or through a delegation capability to isolate verbose output when
one is available. Commit only on explicit user intent — preview first, confirm,
then commit.

## Step 1: Stage + analyze
```bash
git add -A && \
echo "=== STAGED ===" && git diff --cached --stat && \
echo "=== SECURITY ===" && \
git diff --cached | grep -c -iE "(api[_-]?key|token|password|secret|credential)" | awk '{print "SECRETS:"$1}' && \
echo "=== GROUPS ===" && \
git diff --cached --name-only | awk -F'/' '{
  if ($0 ~ /\.(md|txt)$/) print "docs:"$0
  else if ($0 ~ /test|spec/) print "test:"$0
  else if ($0 ~ /\.claude/) print "config:"$0
  else if ($0 ~ /package\.json|lock/) print "deps:"$0
  else print "code:"$0
}'
```

**If SECRETS > 0:** STOP, show matches, block commit.

## Step 2: Split decision

Note:
- Search for related issues and add them to the body.
- Only use `feat`, `fix`, or `perf` prefixes for files in a `.claude` directory
  (do not use `docs`).

**From groups, decide:**

**A) Single commit:** Same type/scope, FILES ≤ 3, LINES ≤ 50

**B) Multi commit:** Mixed types/scopes, group by:
- Group 1: `config:` → `chore(config): ...`
- Group 2: `deps:` → `chore(deps): ...`
- Group 3: `test:` → `test: ...`
- Group 4: `code:` → `feat|fix: ...`
- Group 5: `docs:` → `docs: ...`

## Step 3: Commit

**Single:**
```bash
git commit -m "type(scope): description"
```

**Multi (sequential):**
```bash
git reset && git add file1 file2 && git commit -m "type(scope): desc"
```
Repeat for each group. Never add AI-attribution trailers to any message.

## Step 4: Push (if requested)
```bash
git push && echo "✓ pushed: yes" || echo "✓ pushed: no"
```

**Only push if the user explicitly requested it** ("push", "commit and push").
