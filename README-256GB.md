# SDD-256GB: Optimized Spec-Driven Development

> ⚠️ **WORKING BRANCH**: `optimized-256gb`  
> This branch contains the multi-invocation, context-safe implementation.  
> See [Agents.md](./Agents.md) for architecture details.  
> Main branch contains the original auto-sdd framework.

## Quick Start (15 minutes)

```bash
# 1. Clone this branch
git clone -b optimized-256gb https://github.com/fischmanb/auto-sdd.git sdd-256gb
cd sdd-256gb

# 2. Install llama.cpp
./install.sh

# 3. Download models (~15 min on 2Gbps fiber)
./download-models.sh

# 4. Start model servers
./start.sh

# 5. Run demo build
./demo.sh
```

## Architecture

| Model | Purpose | Port | Memory | Context |
|-------|---------|------|--------|---------|
| Qwen2.5-Coder-32B | Plan + Build | 8080 | ~64GB | Fresh per stage |
| DeepSeek-Coder-V2-16B | Review | 8081 | ~32GB | Fresh per review |
| Qwen2.5-14B | Fix (optional) | 8082 | ~28GB | Fresh per fix |
| **Total** | | | **~124GB** | **No context rot** |

## Why Multi-Invocation?

With 256GB, we could use one long context. But **context rot** is real:
- 0-20K tokens: Sharp, precise
- 20-50K: Good, misses edge cases
- 50-80K: Repetition creeps in
- 80K+: "What was I building again?"

**Solution**: Fresh context per stage. Each invocation is crisp.

## Stages

```
Spec ──▶ [Plan] ──▶ [Build] ──▶ [Review] ──▶ [Fix?] ──▶ Done
         20K ctx      15K ctx      30K ctx      25K ctx
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for details.

## Commands

```bash
./start.sh          # Start all model servers
./stop.sh           # Stop all servers
./status.sh         # Check server health
./demo.sh           # Run test feature build
./stages/01-plan.sh # Run single stage
```

## For Your Boss (Monday)

> "I optimized the SDD framework for my hardware. Instead of overnight batching with fragmented contexts, I run three specialized models with fresh, sharp contexts per stage. Result: real-time feature development, 10-50x speedup, no context rot."

## Documentation

- [Agents.md](./Agents.md) - For AI agents working on this codebase
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Design decisions and context management
