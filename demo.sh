#!/bin/bash
# Run a demo feature build (multi-invocation)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"
source "$SCRIPT_DIR/lib/models.sh"

echo "═══════════════════════════════════════════════════════════"
echo "  SDD-256GB Demo: Multi-Invocation Build"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check servers
log "Checking model servers..."
if ! check_all_models; then
    echo ""
    error "Start servers with: ./start.sh"
    exit 1
fi
echo ""

# Create demo project
DEMO_DIR="demo-project"
if [ ! -d "$DEMO_DIR" ]; then
    log "Creating demo project..."
    mkdir -p "$DEMO_DIR"/{src,tests,.specs}

    cat > "$DEMO_DIR/package.json" << 'PKG'
{
  "name": "demo-todo",
  "version": "1.0.0",
  "scripts": {
    "test": "node --test tests/*.test.js"
  }
}
PKG

    cat > "$DEMO_DIR/.specs/UNIFIED.md" << 'SPEC'
# Demo: Todo App

## Vision
A simple todo list for testing the SDD framework.

## Design System
- `color-primary`: #3B82F6
- `spacing-4`: 1rem
- `text-base`: 1rem

## Features

### Feature 1: Add Todo
**Status**: pending
**Domain**: todos
**Source**: src/todo.js
**Tests**: tests/todo.test.js

#### Scenarios
- **Happy Path**: Given empty list, When add "Buy milk", Then list contains "Buy milk"
- **Empty Input**: Given empty list, When add "", Then error is thrown

#### UI Mockup
```
┌─ Todo App ──────────────┐
│ [________] [Add]        │
│ • Buy milk         [x]  │
└─────────────────────────┘
```

## Learnings Index

### Testing
- None yet
SPEC

    success "Demo project created"
fi

cd "$DEMO_DIR"
echo ""

# Stage 1: Plan
echo "═══════════════════════════════════════════════════════════"
echo "  STAGE 1: PLAN"
echo "═══════════════════════════════════════════════════════════"
"$SCRIPT_DIR/stages/01-plan.sh" .specs/UNIFIED.md plan.json

if jq -e '.status == "NO_PENDING_FEATURES"' plan.json > /dev/null 2>&1; then
    echo ""
    success "Demo complete (no pending features)"
    exit 0
fi

echo ""
cat plan.json | jq .
echo ""

# Stage 2: Build
echo "═══════════════════════════════════════════════════════════"
echo "  STAGE 2: BUILD"
echo "═══════════════════════════════════════════════════════════"
"$SCRIPT_DIR/stages/02-build.sh" plan.json .specs/UNIFIED.md

echo ""
echo "Files created:"
ls -la src/ tests/ 2>/dev/null || ls -la

echo ""

# Stage 3: Review
echo "═══════════════════════════════════════════════════════════"
echo "  STAGE 3: REVIEW"
echo "═══════════════════════════════════════════════════════════"
"$SCRIPT_DIR/stages/03-review.sh" plan.json .specs/UNIFIED.md review.json

echo ""
cat review.json | jq .

echo ""

# Summary
echo "═══════════════════════════════════════════════════════════"
echo "  DEMO COMPLETE"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Created files:"
find src tests -type f 2>/dev/null | head -10
echo ""
echo "Next steps:"
echo "  cd $DEMO_DIR"
echo "  cat src/todo.js"
echo "  npm test"
echo ""
