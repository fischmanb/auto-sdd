# Brian's 15-Minute Setup

> For Mac Studio M3 Ultra with 256GB Unified Memory
> 2.1 Gbps fiber connection

## Prerequisites

- macOS (latest)
- Homebrew installed
- Git configured

## The 15 Minutes

### Minute 0-2: Clone
```bash
git clone -b optimized-256gb https://github.com/fischmanb/auto-sdd.git sdd-256gb
cd sdd-256gb
```

### Minute 2-4: Install llama.cpp
```bash
./install.sh
```
- Clones llama.cpp
- Builds with Metal support for M3 Ultra
- ~2 minutes on M3 Ultra

### Minute 4-15: Download Models
```bash
./download-models.sh
```
Downloads:
- Qwen2.5-Coder-32B (~20GB) - Primary builder
- DeepSeek-Coder-V2-16B (~10GB) - Reviewer  
- Qwen2.5-14B (~9GB) - Drift checker

**Total: ~39GB**  
**Time: ~10-11 minutes on 2Gbps fiber**

### Minute 15-16: Start Servers
```bash
./start.sh
```
- Loads all 3 models into memory
- ~30 seconds to initialize
- Check: `./status.sh`

### Minute 16-20: Demo
```bash
./demo.sh
```
Runs full pipeline:
1. Stage 1: Plan (spec → plan.json)
2. Stage 2: Build (plan → files)
3. Stage 3: Review (files → review.json)

## Verify It Works

```bash
# Check all models online
./status.sh

# Should show:
# ✓ Builder (Qwen 32B) at http://127.0.0.1:8080
# ✓ Reviewer (DeepSeek 16B) at http://127.0.0.1:8081
# ✓ Drift (Qwen 14B) at http://127.0.0.1:8082

# Run a feature build
./framework/ai-dev full
```

## For Monday's Demo

```bash
# 1. Show servers running
./status.sh

# 2. Run live build
./demo.sh

# 3. Show created files
ls -la demo-project/src/
cat demo-project/src/todo.js

# 4. Run tests
cd demo-project && npm test
```

## Talking Points

> "You sent me the SDD framework — great foundation. I optimized it for my hardware.
> Instead of overnight batching with fragmented contexts, I run three specialized
> models with fresh, sharp contexts per stage. Result: real-time feature development,
> 10-50x speedup, no context rot."

## Architecture

| Stage | Model | Context | Fresh? |
|-------|-------|---------|--------|
| Plan | Qwen 32B | 20K | Yes |
| Build | Qwen 32B | 15K/file | Yes |
| Review | DeepSeek 16B | 30K | Yes |
| Fix | Qwen 32B | 25K | Yes (if needed) |

See `../Agents.md` and `../ARCHITECTURE.md` for full details.

## Troubleshooting

**Models won't start:**
```bash
# Check logs
tail -f logs/builder.log

# Restart
./stop.sh && ./start.sh
```

**Download stuck:**
```bash
# Resume with huggingface-cli
huggingface-cli download ... --resume-download
```

**Out of memory:**
- You have 256GB. If this fails, something is very wrong.
- Check: `vm_stat` or Activity Monitor
