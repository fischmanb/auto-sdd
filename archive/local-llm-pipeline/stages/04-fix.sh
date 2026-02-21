#!/bin/bash
# Stage 4: Fix - Apply high-confidence fixes from review
# Input: review.json + files
# Output: Fixed files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
source "$SCRIPT_DIR/../lib/models.sh"

REVIEW_FILE="${1:-review.json}"
PLAN_FILE="${2:-plan.json}"

log "Stage 4: Fix"
echo ""

# Validate review
if ! validate_json "$REVIEW_FILE"; then
    exit 1
fi

# Check if we should skip
CONFIDENCE=$(jq -r '.confidence // 0' "$REVIEW_FILE")
ISSUE_COUNT=$(jq '.issues | length' "$REVIEW_FILE")

if [ "$ISSUE_COUNT" -eq 0 ]; then
    log "No issues to fix"
    exit 0
fi

if (( $(echo "$CONFIDENCE < 0.7" | bc -l) )); then
    warn "Review confidence too low ($CONFIDENCE), skipping auto-fix"
    warn "Manual review recommended"
    exit 0
fi

log "Applying fixes for $ISSUE_COUNT issues (confidence: $CONFIDENCE)"
echo ""

# Get high-severity issues only
HIGH_ISSUES=$(jq '[.issues[] | select(.severity == "high")]' "$REVIEW_FILE")

if [ "$HIGH_ISSUES" = "[]" ] || [ -z "$HIGH_ISSUES" ]; then
    log "No high-severity issues, skipping fix"
    exit 0
fi

# Apply fixes file by file
FILES_TO_FIX=$(echo "$HIGH_ISSUES" | jq -r '.[].file' | sort -u)

for file in $FILES_TO_FIX; do
    if [ ! -f "$file" ]; then
        warn "File not found, skipping: $file"
        continue
    fi

    FILE_ISSUES=$(echo "$HIGH_ISSUES" | jq --arg f "$file" '[.[] | select(.file == $f)]')
    FILE_CONTENT=$(cat "$file")

    log "Fixing: $file"

    FIX_PROMPT=$(cat <<PROMPT
Fix these issues in the code file.

FILE: $file

CURRENT CODE:
$FILE_CONTENT

ISSUES TO FIX:
$FILE_ISSUES

Instructions:
1. Apply all fixes
2. Maintain code style
3. Keep the file working
4. Output ONLY the fixed file content

===FILE: $file===
[fixed code]
===END===
PROMPT
)

    RESPONSE=$(call_model "$BUILDER_URL" "$FIX_PROMPT" 4096 0.2)
    CONTENT=$(extract_content "$RESPONSE")
    parse_files_from_output "$CONTENT"

    if [ -f "$file" ]; then
        success "Fixed: $file"
    fi
done

echo ""
success "Fix stage complete"
