#!/usr/bin/env bash
set -euo pipefail

# Smoke test for collect.sh — validates JSON structure and required fields.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT=$(bash "$SCRIPT_DIR/collect.sh" 2>&1)
FAILURES=0

check_field() {
  local field="$1"
  if echo "$OUTPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); assert $field" 2>/dev/null; then
    echo "  PASS: $field"
  else
    echo "  FAIL: $field"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "Running collect.sh smoke test..."
echo ""

# Valid JSON
if echo "$OUTPUT" | python3 -c "import json,sys; json.load(sys.stdin)" 2>/dev/null; then
  echo "  PASS: valid JSON"
else
  echo "  FAIL: output is not valid JSON"
  echo "$OUTPUT"
  exit 1
fi

# Required fields exist and have correct types
check_field "'collected_at' in d"
check_field "isinstance(d['skills']['count'], int)"
check_field "isinstance(d['agents']['count'], int)"
check_field "isinstance(d['rules']['count'], int)"
check_field "isinstance(d['hooks']['total_entries'], int)"
check_field "isinstance(d['hooks']['event_types_used'], int)"
check_field "isinstance(d['hooks']['has_project_level'], bool)"
check_field "isinstance(d['plugins']['count'], int)"
check_field "isinstance(d['headless']['has_cron'], bool)"
check_field "isinstance(d['headless']['has_ci'], bool)"
check_field "isinstance(d['meta_learning']['has_reflection'], bool)"
check_field "isinstance(d['activity']['commit_velocity_30d'], int)"

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo "All checks passed."
else
  echo "$FAILURES check(s) failed."
  exit 1
fi
