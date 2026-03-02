#!/usr/bin/env bash
# lib/general-estimates.sh — Token estimation and actual usage tracking
#
# Source this file, then call the provided functions.
# No code runs at source time.
#
# Functions provided:
#   get_session_actual_tokens [session_jsonl_path]
#   append_general_estimate <json_string>
#
# TOKEN REPORTING: Agent prompts should use get_session_actual_tokens()
# instead of the proxy formula (lines × 4 + 5000).
# See L-00145 for why the proxy was retired.
#
# Template for agent prompt Token Usage Report sections:
#
#   source lib/general-estimates.sh
#   echo "=== TOKEN USAGE REPORT ==="
#   echo "activity_type: [name]"
#   echo "estimated_tokens_pre: [N]"
#   ACTUAL_TOKENS=$(get_session_actual_tokens)
#   echo "actual_tokens_data: $ACTUAL_TOKENS"
#   ACTIVE=$(echo "$ACTUAL_TOKENS" | jq '.active_tokens // 0')
#   CUMULATIVE=$(echo "$ACTUAL_TOKENS" | jq '.cumulative_tokens // 0')
#   echo "active_tokens (input+output): $ACTIVE"
#   echo "cumulative_tokens (incl cache): $CUMULATIVE"
#   echo "estimation_error_pct: $(echo "scale=1; (([EST] - $ACTIVE) / $ACTIVE) * 100" | bc)"
#   echo "source: $(echo "$ACTUAL_TOKENS" | jq -r '.source')"
#   echo "=== END REPORT ==="
#
# CALIBRATION NOTE: Compare estimates against active_tokens, not cumulative_tokens.
# Cache reads are re-sent context (CLAUDE.md, tool defs, history) — they scale with
# conversation length and API call count, not with the work unit being estimated.
# active_tokens = input + output = new computation per session.

# Guard against double-sourcing
if [ "${_GENERAL_ESTIMATES_SH_LOADED:-}" = "true" ]; then
    return 0 2>/dev/null || true
fi
_GENERAL_ESTIMATES_SH_LOADED=true

# Default estimates file location (relative to repo root)
GENERAL_ESTIMATES_FILE="${GENERAL_ESTIMATES_FILE:-general-estimates.jsonl}"

# ── get_session_actual_tokens ────────────────────────────────────────────────
# Reads Claude Code's local JSONL session data and returns actual token counts.
#
# The JSONL files live at ~/.claude/projects/<encoded-cwd>/<session-id>.jsonl
# Each assistant entry has message.usage with:
#   input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens
#
# Usage: get_session_actual_tokens [path_to_jsonl]
#   If no path given, finds the most recent JSONL in ~/.claude/projects/
#
# Output: JSON object to stdout with fields:
#   input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens,
#   total_tokens, api_calls, source
#
# Returns 0 on success, 1 on failure (with error JSON on stdout).
# See L-00145 for why this replaces the proxy formula.
get_session_actual_tokens() {
    local jsonl_path="${1:-}"

    # If no explicit path, find the most recent session JSONL
    if [ -z "$jsonl_path" ]; then
        local claude_projects_dir="$HOME/.claude/projects"
        if [ ! -d "$claude_projects_dir" ]; then
            echo '{"error": "Claude projects directory not found", "source": "none"}'
            return 1
        fi

        jsonl_path=$(find "$claude_projects_dir" -name "*.jsonl" -type f -printf '%T+ %p\n' 2>/dev/null \
            | sort -r | head -1 | awk '{print $2}')

        if [ -z "$jsonl_path" ]; then
            echo '{"error": "No JSONL session files found", "source": "none"}'
            return 1
        fi
    fi

    if [ ! -f "$jsonl_path" ]; then
        echo "{\"error\": \"JSONL file not found: $jsonl_path\", \"source\": \"none\"}"
        return 1
    fi

    # Parse the JSONL: filter assistant entries, extract message.usage, sum fields
    python3 -c "
import json, sys

input_total = 0
output_total = 0
cache_creation_total = 0
cache_read_total = 0
api_calls = 0

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if data.get('type') != 'assistant':
            continue
        usage = data.get('message', {}).get('usage', {})
        if not usage:
            continue
        api_calls += 1
        input_total += usage.get('input_tokens', 0)
        output_total += usage.get('output_tokens', 0)
        cache_creation_total += usage.get('cache_creation_input_tokens', 0)
        cache_read_total += usage.get('cache_read_input_tokens', 0)

result = {
    'input_tokens': input_total,
    'output_tokens': output_total,
    'cache_creation_tokens': cache_creation_total,
    'cache_read_tokens': cache_read_total,
    'active_tokens': input_total + output_total,
    'cumulative_tokens': input_total + output_total + cache_creation_total + cache_read_total,
    'total_tokens': input_total + output_total + cache_creation_total + cache_read_total,
    'api_calls': api_calls,
    'source': 'jsonl_direct'
}
print(json.dumps(result))
" "$jsonl_path" 2>/dev/null

    if [ $? -ne 0 ]; then
        echo '{"error": "Failed to parse JSONL", "source": "none"}'
        return 1
    fi

    return 0
}

# ── append_general_estimate ──────────────────────────────────────────────────
# Appends a JSON record to the general-estimates JSONL file.
#
# Usage: append_general_estimate <json_string>
#   json_string: a valid JSON object to append as one line
#
# The file path is controlled by GENERAL_ESTIMATES_FILE (default: general-estimates.jsonl).
append_general_estimate() {
    local json_string="${1:-}"

    if [ -z "$json_string" ]; then
        echo "append_general_estimate: json_string is required" >&2
        return 1
    fi

    # Validate JSON before appending
    if ! echo "$json_string" | jq -e '.' >/dev/null 2>&1; then
        echo "append_general_estimate: invalid JSON: $json_string" >&2
        return 1
    fi

    # Compact and append
    echo "$json_string" | jq -c '.' >> "$GENERAL_ESTIMATES_FILE"
}

# ── query_estimate_actuals ───────────────────────────────────────────────────
# Returns per-activity-type stats from general-estimates.jsonl.
#
# Usage: query_estimate_actuals [activity_type]
#   If activity_type given: returns stats for that type only.
#   If omitted: returns summary of all types.
#
# Output: JSON with sample_count, avg_active_tokens, avg_estimation_error_pct,
#   min_active, max_active, calibration_ready (true at 5+ samples).
#
# Uses active_tokens field if available, falls back to approx_actual_tokens.
query_estimate_actuals() {
    local activity_type="${1:-}"
    local estimates_file="${GENERAL_ESTIMATES_FILE}"

    if [ ! -f "$estimates_file" ]; then
        echo '{"error": "No estimates file found", "sample_count": 0, "calibration_ready": false}'
        return 1
    fi

    python3 -c "
import json, sys

activity_filter = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None
entries = []
with open(sys.argv[2]) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if activity_filter and entry.get('activity_type') != activity_filter:
            continue
        # Prefer active_tokens, fall back to approx_actual_tokens
        tokens = entry.get('active_tokens', entry.get('approx_actual_tokens', 0))
        if tokens > 0:
            entries.append({
                'tokens': tokens,
                'estimated': entry.get('estimated_tokens_pre', 0),
                'activity_type': entry.get('activity_type', 'unknown')
            })

if not entries:
    print(json.dumps({'sample_count': 0, 'calibration_ready': False, 'activity_type': activity_filter or 'all'}))
    sys.exit(0)

tokens_list = [e['tokens'] for e in entries]
errors = []
for e in entries:
    if e['estimated'] > 0 and e['tokens'] > 0:
        errors.append(((e['estimated'] - e['tokens']) / e['tokens']) * 100)

result = {
    'activity_type': activity_filter or 'all',
    'sample_count': len(entries),
    'avg_active_tokens': int(sum(tokens_list) / len(tokens_list)),
    'min_active': min(tokens_list),
    'max_active': max(tokens_list),
    'avg_estimation_error_pct': round(sum(errors) / len(errors), 1) if errors else None,
    'calibration_ready': len(entries) >= 5
}
print(json.dumps(result))
" "$activity_type" "$estimates_file"
}

# ── estimate_general_tokens ──────────────────────────────────────────────────
# Returns calibrated token estimate for an activity type.
#
# Usage: estimate_general_tokens <activity_type> <fallback_estimate>
#   activity_type: string matching activity_type in general-estimates.jsonl
#   fallback_estimate: heuristic estimate to use when no data exists
#
# Graduated blend (prevents single outlier from overriding heuristic):
#   1 sample:  20% actuals, 80% heuristic
#   2 samples: 40% actuals, 60% heuristic
#   3 samples: 60% actuals, 40% heuristic
#   4 samples: 80% actuals, 20% heuristic
#   5+ samples: 100% actuals
#
# Returns: integer token estimate to stdout.
estimate_general_tokens() {
    local activity_type="${1:-}"
    local fallback="${2:-0}"

    if [ -z "$activity_type" ] || [ "$fallback" = "0" ]; then
        echo "estimate_general_tokens: requires <activity_type> <fallback_estimate>" >&2
        return 1
    fi

    local stats
    stats=$(query_estimate_actuals "$activity_type")
    local sample_count
    sample_count=$(echo "$stats" | python3 -c "import sys,json; print(json.load(sys.stdin).get('sample_count',0))")

    if [ "$sample_count" = "0" ]; then
        echo "$fallback"
        return 0
    fi

    python3 -c "
import json, sys

stats = json.loads(sys.argv[1])
fallback = int(sys.argv[2])
n = stats['sample_count']
avg = stats['avg_active_tokens']

# Graduated blend: weight shifts 20% per sample toward actuals
actuals_weight = min(n * 0.2, 1.0)
blended = int(avg * actuals_weight + fallback * (1.0 - actuals_weight))
print(blended)
" "$stats" "$fallback"
}
