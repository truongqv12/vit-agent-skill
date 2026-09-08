#!/usr/bin/env bash
# Bisection helper to find which test creates unwanted files/state.
# Runtime: bash (Linux, macOS, Git Bash / WSL on Windows).
#
# Usage: ./find-polluter.sh <file_or_dir_to_check> <test_pattern> [test_command]
#   file_or_dir_to_check : path whose sudden appearance signals pollution (e.g. .git)
#   test_pattern         : find(1) -path pattern matching the test files (e.g. 'src/**/*.test.ts')
#   test_command         : per-file command prefix (default: 'npm test'); the file path is appended
#
# Examples:
#   ./find-polluter.sh '.git' 'src/**/*.test.ts'
#   ./find-polluter.sh '.git' '*.test.js' 'node'
#   ./find-polluter.sh 'node_modules' 'test/**/*.spec.js' 'jest'
#
# On failure the script reports honestly and exits non-zero; it never fabricates a result.

set -euo pipefail

if [ $# -lt 2 ] || [ $# -gt 3 ]; then
  echo "Usage: $0 <file_to_check> <test_pattern> [test_command]" >&2
  echo "Example: $0 '.git' 'src/**/*.test.ts' 'npm test'" >&2
  exit 1
fi

POLLUTION_CHECK="$1"
TEST_PATTERN="$2"
TEST_COMMAND="${3:-npm test}"

echo "Searching for the test that creates: $POLLUTION_CHECK"
echo "Test pattern: $TEST_PATTERN"
echo "Test command: $TEST_COMMAND <file>"
echo ""

# Collect test files matching the pattern.
TEST_FILES=$(find . -path "$TEST_PATTERN" | sort)

if [ -z "$TEST_FILES" ]; then
  echo "No test files matched pattern: $TEST_PATTERN" >&2
  exit 1
fi

TOTAL=$(echo "$TEST_FILES" | wc -l | tr -d ' ')
echo "Found $TOTAL test files"
echo ""

COUNT=0
for TEST_FILE in $TEST_FILES; do
  COUNT=$((COUNT + 1))

  # If pollution already exists, we cannot attribute it to a single test.
  if [ -e "$POLLUTION_CHECK" ]; then
    echo "Pollution already exists before test $COUNT/$TOTAL; skipping: $TEST_FILE" >&2
    continue
  fi

  echo "[$COUNT/$TOTAL] Testing: $TEST_FILE"

  # Run the per-file test command; ignore its exit code (we only care about side effects).
  $TEST_COMMAND "$TEST_FILE" > /dev/null 2>&1 || true

  if [ -e "$POLLUTION_CHECK" ]; then
    echo ""
    echo "FOUND POLLUTER"
    echo "  Test:    $TEST_FILE"
    echo "  Created: $POLLUTION_CHECK"
    echo ""
    echo "Details:"
    ls -la "$POLLUTION_CHECK"
    echo ""
    echo "To investigate:"
    echo "  $TEST_COMMAND $TEST_FILE   # Run just this test"
    echo "  cat $TEST_FILE             # Review test code"
    exit 1
  fi
done

echo ""
echo "No polluter found - all tests clean."
exit 0
