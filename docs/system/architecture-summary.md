# System Architecture Summary

> Token-sensitive reference for every fresh onboard. Covers the live Python system.
> Read this to understand how the pieces connect before modifying anything.
> For deep dives: `docs/system/architecture.md`, `docs/operations/retry-strategy.md`.

---

## Pipeline flow

```
roadmap.md → topo_sort → [per feature] → agent_build → gates → commit → [next feature]
                                              ↓ fail
                                         fix_agent (attempt 1, code on disk)
                                              ↓ fail
                                         retry_agent (attempt 2+, git reset, informed)
```

**Entry point**: `py/auto_sdd/scripts/build_loop.py` → `BuildLoop.run()`

1. `emit_topo_order()` parses `.specs/roadmap.md`, returns pending (⬜) features in dependency order
2. `show_preflight_summary()` displays the plan, waits for confirmation (unless AUTO_APPROVE)
3. Per feature: setup branch → generate codebase summary → build prompt → invoke agent → post-build gates
4. On success: record result, commit, write resume state, advance to next feature
5. On failure: two-stage retry (fix-in-place → informed fresh retry), then skip after max retries

## Key modules

| Module | Lines | Role |
|--------|-------|------|
| `scripts/build_loop.py` | ~2200 | `BuildLoop` class. Main orchestration: feature iteration, agent invocation, retry loop, gate dispatch, resume state, eval sidecar lifecycle. |
| `scripts/overnight_autonomous.py` | ~1400 | `OvernightRunner`. Does NOT subclass BuildLoop — similar structure but different behavioral requirements. |
| `scripts/eval_sidecar.py` | ~740 | Runs alongside build loop, polls for new commits, evaluates features mechanically + via agent. |
| `lib/prompt_builder.py` | ~575 | `build_feature_prompt()`, `build_fix_prompt()`, `build_retry_prompt()`, `show_preflight_summary()`. Constructs all agent prompts. Injects filesystem boundary, sidecar feedback, constraint patterns. |
| `lib/reliability.py` | ~600 | `emit_topo_order()`, `Feature` dataclass, locking, backoff, state persistence (`read_state`/`write_state`/`clean_state`), cycle detection, truncation. |
| `lib/build_gates.py` | ~660 | `check_build()`, `check_tests()`, dead export scan, lint. All post-build mechanical validation. |
| `lib/claude_wrapper.py` | ~260 | `run_claude()` — wraps `claude` CLI, captures output, logs cost to JSONL. Error types: `AgentTimeoutError`, `CreditExhaustionError`. |
| `lib/codebase_summary.py` | ~240 | Agent-generated project summary, cached by git tree hash. Injected into build prompts for cross-feature context. |
| `lib/branch_manager.py` | ~200 | Branch creation/cleanup for chained, independent, sequential strategies. |
| `lib/drift.py` | ~530 | Post-build spec↔code drift detection via fresh agent invocation. |

## Post-build gates (in order)

Gate 0: HEAD advanced (agent committed something)
Gate 1: Working tree clean
Gate 2: Build check passes (`build_cmd` from project.yaml)
Gate 3: Tests pass (`test_cmd` from project.yaml)
Gate 4: Drift check (fresh agent compares spec to code)
Gate 5: Dead export scan (advisory, non-blocking)
Gate 6: Lint (advisory, non-blocking)

If any blocking gate fails → `_last_gate_name` + output captured → retry loop.

## Two-stage retry

| Attempt | Git state | Prompt | Purpose |
|---------|-----------|--------|---------|
| 0 | Clean branch | `build_feature_prompt` | Full build from spec |
| 1 | Code on disk | `build_fix_prompt` | Targeted fix — diagnose, patch, don't rewrite |
| 2+ | `git reset --hard` | `build_retry_prompt` + `prior_attempts` | Fresh start, informed by all prior failures |

## Signal protocol

Agents emit grep-parseable flat strings (L-00028 — no JSON):
- `FEATURE_BUILT: {name}` / `BUILD_FAILED: {reason}` — primary success/failure
- `SPEC_FILE: {path}` / `SOURCE_FILES: {paths}` — required with FEATURE_BUILT
- `NO_DRIFT` / `DRIFT_FIXED` / `DRIFT_UNRESOLVABLE` — drift agent

## Configuration priority

env var > `.sdd-config/project.yaml` > auto-detection > hardcoded default

Key vars: `PROJECT_DIR`, `BUILD_MODEL`, `MAX_RETRIES` (2), `AGENT_TIMEOUT` (1800s), `SUMMARY_TIMEOUT` (300s), `BRANCH_STRATEGY` (chained), `CONTAMINATION_MODE` (warn).

## Filesystem layout (runtime)

- **auto-sdd repo**: `~/auto-sdd` — orchestration code, learnings, docs, commands
- **Target projects**: `~/compstak-sitdeck/` etc. — separate repos, connected via `PROJECT_DIR`
- **Logs**: `LOGS_DIR` (defaults to project dir, override to keep in auto-sdd)
- **Resume state**: `{PROJECT_DIR}/.sdd-state/resume.json`
- **Codebase cache**: `{PROJECT_DIR}/.auto-sdd-cache/`
- **Project config**: `{PROJECT_DIR}/.sdd-config/project.yaml`

## Trust model

Never trust agent self-assessment (L-00001). Every claim is verified by mechanical gates (grep, test runner, build check, `git diff --stat`). Agents say "all verifications passed" while having made changes far beyond scope — only machine-checkable gates are reliable.
