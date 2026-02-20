#!/bin/bash
# Stage 2: Build - Write files from plan
# Input: plan.json
# Output: Source files on disk

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
source "$SCRIPT_DIR/../lib/models.sh"

PLAN_FILE="${1:-plan.json}"
SPEC_FILE="${2:-.specs/UNIFIED.md}"

log "Stage 2: Build"
log "Plan: $PLAN_FILE"
echo ""

# Validate inputs
if ! validate_json "$PLAN_FILE"; then
    exit 1
fi

if [ ! -f "$SPEC_FILE" ]; then
    error "Spec file not found: $SPEC_FILE"
    exit 1
fi

# Check for no-pending status
if jq -e '.status == "NO_PENDING_FEATURES"' "$PLAN_FILE" > /dev/null 2>&1; then
    log "No pending features. Nothing to build."
    exit 0
fi

# Extract plan data
FEATURE=$(jq -r '.feature' "$PLAN_FILE")
DOMAIN=$(jq -r '.domain' "$PLAN_FILE")
FILE_COUNT=$(jq '.files | length' "$PLAN_FILE")
SCENARIOS=$(jq -r '.scenarios | join("\n")' "$PLAN_FILE")
DESIGN_TOKENS=$(jq -r '.design_tokens | join(", ")' "$PLAN_FILE")

log "Building: $FEATURE"
log "Files to create: $FILE_COUNT"
echo ""

# Build each file
for i in $(seq 0 $(($FILE_COUNT - 1))); do
    FILE_PATH=$(jq -r ".files[$i].path" "$PLAN_FILE")
    FILE_PURPOSE=$(jq -r ".files[$i].purpose" "$PLAN_FILE")

    log "[$((i+1))/$FILE_COUNT] Creating: $FILE_PATH"

    # Build prompt for this file
    BUILD_PROMPT=$(cat <<PROMPT
You are implementing "$FEATURE" ($DOMAIN).

FILE TO CREATE: $FILE_PATH
PURPOSE: $FILE_PURPOSE

SCENARIOS TO IMPLEMENT:
$SCENARIOS

DESIGN TOKENS TO USE:
$DESIGN_TOKENS

INSTRUCTIONS:
1. Write complete, working code for this file
2. Follow the scenarios exactly
3. Use the design tokens appropriately
4. Include proper error handling
5. Write clean, production-ready code

OUTPUT FORMAT:
===FILE: $FILE_PATH===
[your code here]
===END===

Write only the file content. No explanation.
PROMPT
)

    # Call model
    RESPONSE=$(call_model "$BUILDER_URL" "$BUILD_PROMPT" 4096 0.2)
    CONTENT=$(extract_content "$RESPONSE")

    # Parse and write file
    parse_files_from_output "$CONTENT"

    # Verify file was created
    if [ -f "$FILE_PATH" ]; then
        success "Created: $FILE_PATH"
    else
        error "Failed to create: $FILE_PATH"
        exit 1
    fi
done

echo ""
success "Build complete: $FEATURE"
echo "  Files created: $FILE_COUNT"
