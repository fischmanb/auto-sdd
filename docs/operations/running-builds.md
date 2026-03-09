# Running Builds

> How to launch, monitor, and manage build campaigns.
> Brian runs all builds in Terminal — chat sessions provide commands and context but never launch builds.

---

## Single-feature validation build

Use this to validate the pipeline or test a fix before a full campaign:

```bash
caffeinate -diw $$ & cd ~/auto-sdd/py && \
  AUTO_APPROVE=true \
  MAX_FEATURES=1 \
  PROJECT_DIR=~/compstak-sitdeck \
  LOGS_DIR=~/auto-sdd/logs/compstak-sitdeck \
  .venv/bin/python -m auto_sdd.scripts.build_loop
```

## Full campaign

Same command, remove `MAX_FEATURES` (defaults to all pending):

```bash
caffeinate -diw $$ & cd ~/auto-sdd/py && \
  AUTO_APPROVE=true \
  PROJECT_DIR=~/compstak-sitdeck \
  LOGS_DIR=~/auto-sdd/logs/compstak-sitdeck \
  .venv/bin/python -m auto_sdd.scripts.build_loop
```

## Resume after crash

The build loop persists resume state to `.sdd-state/resume.json` after each feature. To resume:

```bash
# Same command — resume is automatic if resume.json exists
caffeinate -diw $$ & cd ~/auto-sdd/py && \
  AUTO_APPROVE=true \
  PROJECT_DIR=~/compstak-sitdeck \
  LOGS_DIR=~/auto-sdd/logs/compstak-sitdeck \
  .venv/bin/python -m auto_sdd.scripts.build_loop
```

To force a fresh start, delete `.sdd-state/resume.json` in the project dir.

---

## Key environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `PROJECT_DIR` | (required) | Absolute path to target project |
| `LOGS_DIR` | `{PROJECT_DIR}/logs` | Where build logs, cost logs, eval output go |
| `MAX_FEATURES` | all pending | Cap on features to build this run |
| `AUTO_APPROVE` | `false` | Skip pre-flight confirmation prompt |
| `BUILD_MODEL` | `claude-sonnet-4-6` | Model for initial build attempts |
| `RETRY_MODEL` | (same as BUILD_MODEL) | Model for retry/fix attempts |
| `AGENT_TIMEOUT` | `1800` | Seconds before killing an agent |
| `SUMMARY_TIMEOUT` | `300` | Seconds for codebase summary agent |
| `MAX_RETRIES` | `2` | Max retry attempts per feature (0 = no retries) |
| `MIN_RETRY_DELAY` | `30` | Seconds between retry attempts |
| `BRANCH_STRATEGY` | `chained` | `chained`, `independent`, `both`, or `sequential` |
| `CONTAMINATION_MODE` | `warn` | `warn` or `fail` — post-agent repo contamination check |
| `POST_BUILD_STEPS` | `test,dead-code,lint` | Comma-separated post-build gate steps |
| `SKIP_PREFLIGHT` | `false` | Skip the pre-flight summary |

Full reference: `.env.local.example` (167 lines) or `docs/system/configuration.md`.

---

## Project configuration (project.yaml)

Projects declare build settings in `.sdd-config/project.yaml`. These are defaults — env vars override them.

```yaml
build_cmd: NODE_ENV=production npx next build
test_cmd: npx vitest run --passWithNoTests
lint_cmd: npm run lint
build_model: claude-sonnet-4-6
max_retries: 2
agent_timeout: 1800
branch_strategy: chained
min_retry_delay: 30
drift_check: true
post_build_steps: test,dead-code,lint
```

---

## Monitoring a running build

```bash
# Check if build loop is running
ps aux | grep build_loop | grep -v grep

# Watch the latest log
tail -f ~/auto-sdd/logs/compstak-sitdeck/build-*.log

# Check cost accumulation
tail -5 ~/auto-sdd/logs/compstak-sitdeck/cost-log.jsonl
```

---

## Branch strategies

| Strategy | Behavior | Use case |
|----------|----------|----------|
| `chained` | Each feature branches from the previous | Default for local campaigns |
| `independent` | All features branch from base | Parallel comparison |
| `both` | Runs chained then independent | Head-to-head evaluation |
| `sequential` | No branching, commits to current branch | Simple linear builds |

---

## Post-run cleanup

```bash
# Check for orphan remote branches
git branch -r | grep "auto/" | wc -l

# Clean up orphan remote branches
git branch -r | grep auto/ | while read b; do git push origin --delete "${b#origin/}"; done

# Merge feature branch to main (manual step)
cd ~/compstak-sitdeck && git checkout main && git merge auto/chained-YYYYMMDD-HHMMSS
```

---

## Running tests (auto-sdd itself)

```bash
cd ~/auto-sdd/py

# Full Python test suite (~1026 tests, ~23s)
.venv/bin/pytest tests/ -q

# Specific module
.venv/bin/pytest tests/test_build_loop.py -v

# Type checking
.venv/bin/mypy --strict auto_sdd/
```
