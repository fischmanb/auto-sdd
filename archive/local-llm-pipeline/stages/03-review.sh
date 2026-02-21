#!/bin/bash
# Stage 3: Review - Check implementation against spec
# Input: Built files + spec
# Output: review.json

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
source "$SCRIPT_DIR/../lib/models.sh"

PLAN_FILE="${1:-plan.json}"
SPEC_FILE="${2:-.specs/UNIFIED.md}"
OUTPUT_FILE="${3:-review.json}"

log "Stage 3: Review"
log "Output: $OUTPUT_FILE"
echo ""

# Check reviewer health
if ! check_model_health "$REVIEWER_URL" "Reviewer"; then
    warn "Reviewer unavailable, skipping review"
    echo '{"status": "SKIPPED", "issues": [], "confidence": 0}' > "$OUTPUT_FILE"
    exit 0
fi

# Validate inputs
if ! validate_json "$PLAN_FILE"; then
    exit 1
fi

if [ ! -f "$SPEC_FILE" ]; then
    error "Spec file not found: $SPEC_FILE"
    exit 1
fi

# Load spec and plan
SPEC_CONTENT=$(cat "$SPEC_FILE")
PLAN_CONTENT=$(cat "$PLAN_FILE")
FEATURE=$(jq -r '.feature' "$PLAN_FILE")

# Collect all source files
FILE_LIST=$(jq -r '.files[].path' "$PLAN_FILE")
ALL_CODE=""

for file in $FILE_LIST; do
    if [ -f "$file" ]; then
        ALL_CODE="${ALL_CODE}\n\n=== $file ===\n$(cat "$file")"
    fi
done

log "Reviewing: $FEATURE"
log "Files to review: $(echo "$FILE_LIST" | wc -w)"
echo ""

# Build review prompt
REVIEW_PROMPT=$(cat <<PROMPT
You are a senior code reviewer. Review this implementation against its specification.

FEATURE: $FEATURE

SPECIFICATION:
$SPEC_CONTENT

IMPLEMENTATION:
$ALL_CODE

Review instructions:
1. Check each scenario from the spec - is it implemented?
2. Look for bugs, missing error handling, edge cases
3. Check code quality and best practices
4. Output ONLY valid JSON:

{
  "status": "reviewed",
  "issues": [
    {
      "file": "src/file.js",
      "line": 15,
      "severity": "high|medium|low",
      "issue": "Description of the problem",
      "fix": "Suggested fix"
    }
  ],
  "confidence": 0.85,
  "summary": "2 high, 1 medium issues found"
}

If no issues: "issues": [], "confidence": 0.95
Output ONLY JSON, no markdown, no explanation.
PROMPT
)

log "Sending to Reviewer (DeepSeek 16B)..."
RESPONSE=$(call_model "$REVIEWER_URL" "$REVIEW_PROMPT" 2048 0.2)
CONTENT=$(extract_content "$RESPONSE")

# Extract JSON
JSON_CONTENT=$(echo "$CONTENT" | sed -n '/^```json/,/^```$/p' | sed '1d;$d')
if [ -z "$JSON_CONTENT" ]; then
    JSON_CONTENT="$CONTENT"
fi

# Validate and write
if echo "$JSON_CONTENT" | jq empty 2>/dev/null; then
    echo "$JSON_CONTENT" | jq . > "$OUTPUT_FILE"
    ISSUE_COUNT=$(jq '.issues | length' "$OUTPUT_FILE")
    CONFIDENCE=$(jq -r '.confidence' "$OUTPUT_FILE")
    success "Review complete: $ISSUE_COUNT issues (confidence: $CONFIDENCE)"
else
    error "Invalid review JSON"
    echo "$CONTENT" > "$OUTPUT_FILE.raw"
    echo '{"status": "error", "issues": [], "confidence": 0}' > "$OUTPUT_FILE"
    exit 1
fi
