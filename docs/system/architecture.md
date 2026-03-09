# ARCHITECTURE.md

> Design decisions and context management for SDD-256GB

## Context Rot: The Problem

Even with 256GB memory, LLMs exhibit **context rot**:

| Token Range | Behavior |
|-------------|----------|
| 0-20K | Sharp, precise instruction following |
| 20-50K | Good, occasional misses |
| 50-80K | Repetition, forgotten constraints |
| 80K+ | Degraded quality, hallucination |

**Solution**: Fresh context per stage. Each invocation starts crisp.

## Stage Breakdown

### Stage 1: Plan (Builder, 32B)

**Purpose**: Parse UNIFIED.md, identify next pending feature, create implementation plan

**Input**: `.specs/UNIFIED.md` (~10K tokens)
**Output**: `plan.json`

```json
{
  "feature": "Add Todo",
  "domain": "todos",
  "files": [
    {"path": "src/todo.js", "purpose": "Core logic"},
    {"path": "tests/todo.test.js", "purpose": "Unit tests"}
  ],
  "dependencies": [],
  "scenarios": ["Happy path", "Empty input"]
}
```

**Context budget**: 20K tokens (spec + plan output)
**Fresh context**: Yes (cold start)

### Stage 2: Build (Builder, 32B)

**Purpose**: Write each file from the plan

**Input**: `plan.json` + file index
**Output**: Source files on disk

**Loop**: One HTTP request per file
```
Request 1: "Write src/todo.js"
Request 2: "Write tests/todo.test.js"
```

**Context budget**: 15K tokens (plan + one file)
**Fresh context**: Yes (new request per file)
**Atomic**: Each file write is independent

### Stage 3: Review (Reviewer, 16B)

**Purpose**: Check implementation against spec scenarios

**Input**: All files + spec scenarios (~25K tokens)
**Output**: `review.json`

```json
{
  "issues": [
    {
      "file": "src/todo.js",
      "line": 15,
      "severity": "high",
      "issue": "Missing null check",
      "fix": "Add if (!text) throw new Error(...)"
    }
  ],
  "confidence": 0.85,
  "summary": "2 issues found"
}
```

**Context budget**: 30K tokens (all code + spec)
**Fresh context**: Yes (different model)

### Stage 4: Fix (Builder, 32B) - Conditional

**Purpose**: Apply high-confidence fixes from review

**Input**: `review.json` + files
**Output**: Fixed files

**Condition**: Only runs if `confidence > 0.7` and issues exist

**Context budget**: 25K tokens
**Fresh context**: Yes

## State Management

### Between Stages

```
UNIFIED.md ──▶ 01-plan.sh ──▶ plan.json
                                 │
                                 ▼
                           02-build.sh ──▶ src/*, tests/*
                                 │
                                 ▼
                           03-review.sh ──▶ review.json
                                 │
                                 ▼ (if issues)
                           04-fix.sh ──▶ fixed src/*
```

### Resumability

Each stage checks for its input file:
- `01-plan.sh`: Checks for `UNIFIED.md`
- `02-build.sh`: Checks for `plan.json`
- `03-review.sh`: Checks for built files
- `04-fix.sh`: Checks for `review.json` with issues

Can restart from any point without re-running previous stages.

## Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Model server down | Health check fail | Clear error, suggest `./start.sh` |
| Plan parsing fails | Invalid JSON | Log raw output, exit with error |
| File write fails | File doesn't exist | Retry once, then exit |
| Review hallucinates | Confidence < 0.5 | Skip fix stage, warn user |
| Build crashes mid-file | Partial file | Atomic writes prevent corruption |

## Performance Characteristics

| Stage | Expected Latency | Bottleneck |
|-------|------------------|------------|
| Plan | 30-60s | Model inference |
| Build (per file) | 20-45s | Model inference |
| Review | 45-90s | Model inference |
| Fix | 30-60s | Model inference |

**Total for 3-file feature**: ~3-5 minutes

## Memory Usage

| Model | Loaded Size | Context Peak |
|-------|-------------|--------------|
| Qwen 32B | ~20GB | ~25GB |
| DeepSeek 16B | ~10GB | ~15GB |
| Qwen 14B | ~9GB | ~12GB |
| **Total** | **~39GB** | **~52GB** |

Well under 256GB. Room for 4x scaling.

## Design Principles

1. **Fresh > Long**: Better to have 4 crisp contexts than 1 rotting one
2. **Explicit state**: JSON files between stages, not hidden in context
3. **Atomic operations**: Each file write is all-or-nothing
4. **Fail fast**: Clear errors, no silent failures
5. **Debuggable**: Every intermediate state is inspectable
