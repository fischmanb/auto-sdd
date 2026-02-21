#!/bin/bash
# Stage 1: Plan - Parse spec and create implementation plan
# Input: .specs/UNIFIED.md
# Output: plan.json

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/common.sh"
source "$SCRIPT_DIR/../lib/models.sh"

SPEC_FILE="${1:-.specs/UNIFIED.md}"
OUTPUT_FILE="${2:-plan.json}"

log "Stage 1: Plan"
log "Input: $SPEC_FILE"
log "Output: $OUTPUT_FILE"
echo ""

# Check model health
if ! check_model_health "$BUILDER_URL" "Builder"; then
    exit 1
fi

# Check spec exists
if [ ! -f "$SPEC_FILE" ]; then
    error "Spec file not found: $SPEC_FILE"
    exit 1
fi

SPEC_CONTENT=$(cat "$SPEC_FILE")

# Check for pending features
if ! echo "$SPEC_CONTENT" | grep -q "Status.*pending"; then
    warn "No pending features found in spec"
    echo '{"status": "NO_PENDING_FEATURES", "message": "All features completed"}' > "$OUTPUT_FILE"
    success "Plan complete (no work needed)"
    exit 0
fi

# Build prompt
PLAN_PROMPT=$(cat <<PROMPT
You are a software architect. Read this specification and create an implementation plan.

SPECIFICATION:
$SPEC_CONTENT

Instructions:
1. Find the FIRST feature with status "pending"
2. Create a detailed implementation plan
3. Output ONLY valid JSON in this exact format:

{
  "feature": "Feature Name",
  "domain": "domain-name",
  "status": "pending",
  "files": [
    {"path": "src/feature.js", "purpose": "What this file does"},
    {"path": "tests/feature.test.js", "purpose": "Test coverage"}
  ],
  "dependencies": [],
  "scenarios": ["Happy path description", "Edge case description"],
  "design_tokens": ["color-primary", "spacing-4"]
}

Rules:
- Files should be in dependency order (if B depends on A, A first)
- Keep file list minimal (3-5 files max per feature)
- Scenarios must match the Gherkin in the spec
- Output ONLY the JSON, no markdown, no explanation
PROMPT
)

log "Sending to Builder (Qwen 32B)..."
RESPONSE=$(call_model "$BUILDER_URL" "$PLAN_PROMPT" 2048 0.2)
CONTENT=$(extract_content "$RESPONSE")

# Try to extract JSON from markdown code blocks if present
JSON_CONTENT=$(echo "$CONTENT" | sed -n '/^```json/,/^```$/p' | sed '1d;$d')
if [ -z "$JSON_CONTENT" ]; then
    JSON_CONTENT="$CONTENT"
fi

# Validate JSON
if ! echo "$JSON_CONTENT" | jq empty 2>/dev/null; then
    error "Model returned invalid JSON"
    echo "Raw output saved to plan.json.raw"
    echo "$CONTENT" > "$OUTPUT_FILE.raw"
    exit 1
fi

# Write plan
echo "$JSON_CONTENT" | jq . > "$OUTPUT_FILE"
success "Plan created: $OUTPUT_FILE"

# Display summary
FEATURE=$(jq -r '.feature' "$OUTPUT_FILE")
FILE_COUNT=$(jq '.files | length' "$OUTPUT_FILE")
echo "  Feature: $FEATURE"
echo "  Files: $FILE_COUNT"
