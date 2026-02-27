#!/usr/bin/env bash
# claude-wrapper.sh — wraps claude CLI to capture cost/usage data
# Runs claude with --output-format json, extracts .result as raw text to stdout,
# appends cost metadata to $COST_LOG_FILE as JSONL.

# NOTE: -e is intentionally omitted. With set -e, a non-zero exit from the
# claude invocation kills the script before claude_exit=$? can execute,
# and combined with stderr suppression all diagnostic output is lost.
# Errors are handled manually so claude failures produce diagnostic output.
set -uo pipefail

# Prevent nested-session detection if CLAUDECODE is inherited from a parent
# Claude Code session. claude -p detects this and exits immediately.
unset CLAUDECODE

COST_LOG="${COST_LOG_FILE:-./cost-log.jsonl}"

tmp=$(mktemp)
tmp_stderr=$(mktemp)
trap 'rm -f "$tmp" "$tmp_stderr"' EXIT

claude "$@" --output-format json > "$tmp" 2>"$tmp_stderr"
claude_exit=$?

# On failure, surface diagnostics to the caller and exit immediately.
if [ "$claude_exit" -ne 0 ]; then
    echo "WRAPPER_ERROR: claude exited with code $claude_exit" >&2
    if [ -s "$tmp_stderr" ]; then
        echo "=== claude stderr ===" >&2
        cat "$tmp_stderr" >&2
    fi
    if [ -s "$tmp" ]; then
        echo "=== claude stdout ===" >&2
        cat "$tmp" >&2
    fi
    exit "$claude_exit"
fi

# Success path: extract .result and log cost data.
if jq -e '.result' "$tmp" > /dev/null 2>&1; then
    jq -r '.result // empty' "$tmp"

    jq -c '{
        timestamp: (now | todate),
        cost_usd: .total_cost_usd,
        input_tokens: .usage.input_tokens,
        output_tokens: .usage.output_tokens,
        cache_creation_tokens: .usage.cache_creation_input_tokens,
        cache_read_tokens: .usage.cache_read_input_tokens,
        duration_ms: .duration_ms,
        duration_api_ms: .duration_api_ms,
        num_turns: .num_turns,
        model: (.modelUsage | keys[0] // "unknown"),
        session_id: .session_id,
        stop_reason: .stop_reason
    }' "$tmp" >> "$COST_LOG" 2>/dev/null
else
    cat "$tmp" >&2
    echo "WRAPPER_ERROR: claude did not return valid JSON. Raw output sent to stderr." >&1
fi

exit $claude_exit
