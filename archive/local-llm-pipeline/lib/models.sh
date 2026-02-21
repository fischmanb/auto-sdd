#!/bin/bash
# Model endpoint configuration for SDD-256GB

# Model endpoints
BUILDER_URL="${BUILDER_URL:-http://127.0.0.1:8080}"
REVIEWER_URL="${REVIEWER_URL:-http://127.0.0.1:8081}"
DRIFT_URL="${DRIFT_URL:-http://127.0.0.1:8082}"

# Context limits (tokens)
BUILDER_MAX_CONTEXT=128000
REVIEWER_MAX_CONTEXT=64000
DRIFT_MAX_CONTEXT=64000

# Default max tokens for responses
BUILDER_MAX_TOKENS=4096
REVIEWER_MAX_TOKENS=2048
DRIFT_MAX_TOKENS=2048

# Check all models
check_all_models() {
    local failed=0

    if ! curl -s "$BUILDER_URL/health" > /dev/null 2>&1; then
        echo "✗ Builder (Qwen 32B) not responding at $BUILDER_URL"
        failed=1
    else
        echo "✓ Builder (Qwen 32B) at $BUILDER_URL"
    fi

    if ! curl -s "$REVIEWER_URL/health" > /dev/null 2>&1; then
        echo "✗ Reviewer (DeepSeek 16B) not responding at $REVIEWER_URL"
        failed=1
    else
        echo "✓ Reviewer (DeepSeek 16B) at $REVIEWER_URL"
    fi

    if ! curl -s "$DRIFT_URL/health" > /dev/null 2>&1; then
        echo "✗ Drift (Qwen 14B) not responding at $DRIFT_URL"
        failed=1
    else
        echo "✓ Drift (Qwen 14B) at $DRIFT_URL"
    fi

    return $failed
}

# Export for use in other scripts
export BUILDER_URL REVIEWER_URL DRIFT_URL
export BUILDER_MAX_TOKENS REVIEWER_MAX_TOKENS DRIFT_MAX_TOKENS
