# Agents.md

> **For AI agents working on this codebase**  
> Last updated: 2024-02-20  
> Architecture: Multi-invocation, context-safe

## What This Is

A spec-driven development system optimized for 256GB unified memory. Uses multiple local LLMs with **fresh contexts per stage** to avoid context rot.

## Core Principle: Context Management

**DO NOT** use one long context. **DO** use fresh contexts per stage.

| Stage | Max Tokens | Why |
|-------|------------|-----|
| Plan | 20K | Spec only, crisp planning |
| Build | 15K | Plan + one file, focused |
| Review | 30K | All files + spec, comprehensive |
| Fix | 25K | Review + files, targeted |

## File Structure

```
optimized-256gb/
├── stages/           # One script per stage
│   ├── 01-plan.sh   # Spec → plan.json
│   ├── 02-build.sh  # plan.json → files
│   ├── 03-review.sh # files → review.json
│   └── 04-fix.sh    # review.json → fixed files
├── lib/             # Shared libraries
│   ├── common.sh    # curl, parsing, validation
│   └── models.sh    # Model endpoint management
└── framework/       # User-facing tools
    └── ai-dev       # Main CLI entry
```

## How to Modify

### Adding a Stage

1. Create `stages/05-newstage.sh`
2. Follow the pattern:
   - Read input from previous stage's JSON
   - Call model with fresh context
   - Write output to JSON
   - Return 0 on success, 1 on failure
3. Update `framework/ai-dev` to call new stage

### Modifying a Stage

1. Keep context budget under the limit (see table above)
2. Maintain JSON I/O format for chaining
3. Test in isolation: `./stages/02-build.sh < test-input.json`

### Changing Models

Edit `lib/models.sh`:
```bash
BUILDER_URL="http://127.0.0.1:8080"
REVIEWER_URL="http://127.0.0.1:8081"
DRIFT_URL="http://127.0.0.1:8082"
```

## Common Pitfalls

**DON'T**: Increase context sizes to "fit more"  
**DO**: Split into more stages if needed

**DON'T**: Merge stages to reduce HTTP calls  
**DO**: Keep stages separate for crispness

**DON'T**: Parse model output with regex alone  
**DO**: Use delimiters + JSON fallback (see `lib/common.sh`)

**DON'T**: Assume model output is valid  
**DO**: Validate JSON, check file existence, handle errors

## State Management

State passes between stages via JSON files:

```
01-plan.sh    → plan.json
02-build.sh   ← plan.json → writes files
03-review.sh  ← files + spec → review.json
04-fix.sh     ← review.json → fixes files
```

Each stage is idempotent. Can restart from any point.

## Testing Changes

Run a single stage in isolation:

```bash
# Test plan stage
cat test-spec.md | ./stages/01-plan.sh
cat plan.json

# Test build stage (requires plan.json)
./stages/02-build.sh
ls -la src/

# Test review stage (requires built files)
./stages/03-review.sh
cat review.json
```

## Model Endpoints

| Endpoint | Purpose | Health Check |
|----------|---------|--------------|
| `:8080/v1/chat/completions` | Builder | `curl :8080/health` |
| `:8081/v1/chat/completions` | Reviewer | `curl :8081/health` |
| `:8082/v1/chat/completions` | Drift/Fix | `curl :8082/health` |

## Architecture Decision Log

| Decision | Rationale |
|----------|-----------|
| Fresh context per stage | Avoid context rot, maintain precision |
| JSON state files | Machine-parseable, resumable, debuggable |
| Delimiter + JSON output | Robust parsing, handles malformed output |
| Atomic file writes | No partial files on crash |
| Separate models per stage | Each model stays sharp in its role |

## Questions?

See [ARCHITECTURE.md](./ARCHITECTURE.md) for deeper design rationale.
