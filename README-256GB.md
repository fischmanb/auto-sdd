# SDD-256GB: Optimized Spec-Driven Development

Single-context AI development for 256GB unified memory systems.

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

| Model | Purpose | Port | Memory |
|-------|---------|------|--------|
| Qwen2.5-Coder-32B | Primary Builder | 8080 | ~64GB |
| DeepSeek-Coder-V2-16B | Code Reviewer | 8081 | ~32GB |
| Qwen2.5-14B | Drift Checker | 8082 | ~28GB |
| **Total** | | | **~124GB** |

## Why This Works

- **Single context**: Entire codebase + specs fit in memory
- **No fragmentation**: One AI session completes full TDD cycle
- **Real-time**: 10-30 minutes per feature vs. hours

## Commands

```bash
./start.sh          # Start all model servers
./stop.sh           # Stop all servers
./status.sh         # Check server health
./demo.sh           # Run test feature build
```

## For Your Boss (Monday)

> "I optimized the SDD framework for my hardware. Instead of overnight batching with fragmented contexts, I run three specialized models concurrently with unified memory. Result: real-time feature development, 10-50x speedup."
