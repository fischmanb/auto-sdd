#!/bin/bash
# Run a demo feature build

set -e

echo "SDD-256GB Demo"
echo "=============="
echo ""

# Check servers
for port in 8080 8081 8082; do
    if ! curl -s "http://127.0.0.1:$port/health" > /dev/null 2>&1; then
        echo "Error: Model server on port $port not running"
        echo "Start with: ./start.sh"
        exit 1
    fi
done
echo "✓ All model servers online"
echo ""

# Create demo project if needed
if [ ! -d "demo-project" ]; then
    mkdir -p demo-project/{src,tests,.specs}
    
    # Create package.json
    cat > demo-project/package.json << 'PKG'
{
  "name": "demo-project",
  "version": "1.0.0",
  "scripts": {
    "test": "node --test tests/*.test.js"
  }
}
PKG

    # Create UNIFIED.md spec
    cat > demo-project/.specs/UNIFIED.md << 'SPEC'
# Demo Project: Todo App

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
- **Empty Input**: Given empty list, When add "", Then error shown

#### UI Mockup
```
┌─ Todo App ──────────────┐
│ [________] [Add]        │
│ • Buy milk         [x]  │
└─────────────────────────┘
```
SPEC
fi

cd demo-project

echo "Building Feature 1: Add Todo"
echo "-----------------------------"
echo ""

# Simple curl-based build (for demo purposes)
SPEC_CONTENT=$(cat .specs/UNIFIED.md)

BUILD_PROMPT=$(cat <<PROMPT
You are building a todo app feature. Create these files:

1. src/todo.js - Implementation with:
   - addTodo(text) function
   - getTodos() function
   - deleteTodo(index) function
   - Uses in-memory array (no database needed for demo)

2. tests/todo.test.js - Tests for:
   - Adding a todo works
   - Empty string returns error
   - Deleting a todo works

Return ONLY the file contents in this format:

===FILE: src/todo.js===
[content]

===FILE: tests/todo.test.js===
[content]

Specification:
$SPEC_CONTENT
PROMPT
)

echo "Sending to Builder (Qwen 32B)..."
echo ""

RESPONSE=$(curl -s -X POST http://127.0.0.1:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{
        \"messages\": [{\"role\": \"user\", \"content\": $(echo "$BUILD_PROMPT" | jq -Rs .)}],
        \"temperature\": 0.2,
        \"max_tokens\": 4096
    }")

# Extract and write files
echo "$RESPONSE" | jq -r '.choices[0].message.content' | while IFS= read -r line; do
    if [[ "$line" == "===FILE:"* ]]; then
        FILENAME=$(echo "$line" | sed 's/===FILE: //; s/===//')
        mkdir -p "$(dirname "$FILENAME")"
        > "$FILENAME"
        WRITING="$FILENAME"
    elif [[ -n "$WRITING" && "$line" != "==="* ]]; then
        echo "$line" >> "$WRITING"
    fi
done

echo "Files created:"
ls -la src/ tests/
echo ""

echo "Running tests..."
npm test 2>&1 || echo "Tests completed (check output above)"
echo ""

echo "✓ Demo complete!"
echo ""
echo "Next steps:"
echo "  - Review: cat src/todo.js"
echo "  - Test: npm test"
echo "  - Modify spec and rebuild"
