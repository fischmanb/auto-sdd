#!/bin/bash
# Build next feature from UNIFIED.md (256GB optimized)

set -e

SPEC_FILE=".specs/UNIFIED.md"
BUILDER_URL="http://127.0.0.1:8080"

echo "Building next feature from $SPEC_FILE..."
echo ""

if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: $SPEC_FILE not found"
    exit 1
fi

SPEC_CONTENT=$(cat "$SPEC_FILE")

# Find and build next pending feature
BUILD_PROMPT=$(cat <<PROMPT
Read this specification and build the first pending feature.

SPECIFICATION:
$SPEC_CONTENT

Instructions:
1. Find the feature with status "pending"
2. Implement all files needed (source + tests)
3. Update the spec status to "completed"
4. Add any learnings discovered

Return files in format:
===FILE: path/to/file===
[content]
PROMPT
)

echo "Sending to Builder (Qwen 32B)..."
echo "This may take 2-5 minutes..."
echo ""

RESPONSE=$(curl -s -X POST "$BUILDER_URL/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d "{
        \"messages\": [{\"role\": \"user\", \"content\": $(echo "$BUILD_PROMPT" | jq -Rs .)}],
        \"temperature\": 0.2,
        \"max_tokens\": 8192
    }")

# Extract and write files
echo "$RESPONSE" | jq -r '.choices[0].message.content' | while IFS= read -r line; do
    if [[ "$line" == "===FILE:"* ]]; then
        FILENAME=$(echo "$line" | sed 's/===FILE: //; s/===//; s/^[[:space:]]*//')
        if [ -n "$FILENAME" ]; then
            mkdir -p "$(dirname "$FILENAME")"
            > "$FILENAME"
            WRITING="$FILENAME"
            echo "Creating: $FILENAME"
        fi
    elif [[ -n "$WRITING" && "$line" != "==="* ]]; then
        echo "$line" >> "$WRITING"
    fi
done

echo ""
echo "✓ Build complete"
echo "Run tests: npm test (or your test command)"
