#!/bin/bash
# Common utilities for SDD-256GB stages

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
success() { echo -e "${GREEN}[$(date '+%H:%M:%S')] ✓${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date '+%H:%M:%S')] ⚠${NC} $1"; }
error() { echo -e "${RED}[$(date '+%H:%M:%S')] ✗${NC} $1"; }

# Check if model server is healthy
check_model_health() {
    local url=$1
    local name=$2

    if ! curl -s "$url/health" > /dev/null 2>&1; then
        error "$name not responding at $url"
        return 1
    fi
    return 0
}

# Call model with retry
# Usage: call_model <url> <prompt> <max_tokens> [temperature]
call_model() {
    local url=$1
    local prompt=$2
    local max_tokens=$3
    local temperature=${4:-0.2}

    local json_payload=$(cat <<EOF
{
    "messages": [{"role": "user", "content": $(echo "$prompt" | jq -Rs .)}],
    "temperature": $temperature,
    "max_tokens": $max_tokens,
    "stream": false
}
EOF
)

    curl -s -X POST "$url/v1/chat/completions"         -H "Content-Type: application/json"         -d "$json_payload"
}

# Extract content from model response
extract_content() {
    local response=$1
    echo "$response" | jq -r '.choices[0].message.content // empty'
}

# Parse delimiter-based output into files
# Format: ===FILE: path/to/file===\ncontent\n===END===
parse_files_from_output() {
    local output=$1
    local writing=""

    while IFS= read -r line; do
        if [[ "$line" == "===FILE:"* ]]; then
            writing=$(echo "$line" | sed 's/===FILE: //; s/===//; s/^[[:space:]]*//')
            if [ -n "$writing" ]; then
                mkdir -p "$(dirname "$writing")"
                > "$writing"
                echo "Creating: $writing"
            fi
        elif [[ "$line" == "===END"* ]] || [[ "$line" == "===EOF"* ]]; then
            writing=""
        elif [[ -n "$writing" ]]; then
            echo "$line" >> "$writing"
        fi
    done <<< "$output"
}

# Validate JSON file
validate_json() {
    local file=$1
    if [ ! -f "$file" ]; then
        error "File not found: $file"
        return 1
    fi
    if ! jq empty "$file" 2>/dev/null; then
        error "Invalid JSON: $file"
        return 1
    fi
    return 0
}

# Check if spec has pending features
has_pending_features() {
    local spec_file=$1
    if [ ! -f "$spec_file" ]; then
        return 1
    fi
    grep -q "Status.*pending" "$spec_file" 2>/dev/null
    return $?
}

# Update spec status (simple sed replacement)
update_spec_status() {
    local spec_file=$1
    local feature=$2
    local new_status=$3

    # This is a simple implementation - may need refinement
    sed -i.bak "s/### Feature.*$feature.*\n.*Status.*: .*/### Feature: $feature\n**Status**: $new_status/" "$spec_file" 2>/dev/null || true
}
