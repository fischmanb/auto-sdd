# Retry Strategy

> Two-stage retry: fix-in-place before informed fresh retry.
> Implemented in `8533639` (2026-03-09). Decision log: `docs/knowledge/decisions.md`.

---

## Overview

When a build agent claims `FEATURE_BUILT` but post-build gates fail (tests, build check, drift), the build loop retries. The retry strategy is staged:

| Attempt | Git state | Prompt function | Strategy |
|---------|-----------|----------------|----------|
| 0 | Clean branch | `build_feature_prompt` | Full build from spec |
| 1 | Code stays on disk | `build_fix_prompt` | Diagnose and fix. Don't rewrite. |
| 2+ | `git reset --hard` | `build_retry_prompt` | Fresh start with failure history. |

Default `MAX_RETRIES=2` means up to 3 total attempts (initial + fix + informed retry).

---

## Stage 1: Fix-in-place (attempt 1)

**Trigger**: Post-build gates fail on committed code.

**Git state**: No reset. The agent's committed code is still on disk.

**What the agent receives**:
- Which gate failed (`test`, `build`, `drift`)
- Build check output (last 3000 chars)
- Test failure output (last 6000 chars)
- Instructions to run `git log --oneline -3` and `git diff HEAD~1`
- Explicit directive: "change as few lines as possible"

**Escape hatch**: If the agent determines the approach is fundamentally broken, it outputs `BUILD_FAILED: {explanation}` — which feeds into Stage 2.

**Why this works**: Most M-complexity feature failures are small: a type mismatch, missing import, off-by-one in a query. The 90%-correct implementation is preserved.

---

## Stage 2: Informed fresh retry (attempt 2+)

**Trigger**: Fix attempt also failed, or agent declared `BUILD_FAILED`.

**Git state**: `git reset --hard` to branch start commit + `git clean -fd`.

**What the agent receives**:
- Standard retry prompt (read spec, implement, verify)
- Build/test failure output from the most recent attempt
- **"APPROACHES THAT FAILED"** section: structured list of all prior attempts with:
  - Attempt number
  - Failure mode (which gate, or BUILD_FAILED)
  - Summary of what went wrong (first 500 chars of failure output)

**Why this works**: Agent builds from scratch but knows what didn't work. Avoids repeating the same structural mistakes.

---

## Gate failure tracking

`BuildLoop` tracks which gate failed and captures output:

```python
self._last_gate_name: str        # "test", "build", "drift"
self._last_gate_build_output: str  # last 3000 chars of build check
self._last_gate_test_output: str   # last 6000 chars of test output
```

These are reset at the start of each `_run_post_build_gates()` call and populated when a gate returns `False`.

---

## Prior attempt summaries

Structured failure context accumulates across attempts:

```python
prior_attempt_summaries: list[dict[str, str]] = [
    {"attempt": "1", "failure_mode": "test", "summary": "...first 500 chars..."},
    {"attempt": "2", "failure_mode": "BUILD_FAILED", "summary": "...reason..."},
]
```

Populated from:
- Gate failures in the `FEATURE_BUILT` path
- `BUILD_FAILED` signals from any attempt

---

## Key files

| File | What |
|------|------|
| `py/auto_sdd/lib/prompt_builder.py` | `build_fix_prompt()`, enhanced `build_retry_prompt()` |
| `py/auto_sdd/scripts/build_loop.py` | Retry loop (lines ~1091–1170), gate tracking vars |
| `py/tests/test_build_loop.py` | Retry path tests |
| `py/tests/test_prompt_builder.py` | Prompt construction tests |

---

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `MAX_RETRIES` | `2` | Total retry attempts (fix + informed retries) |
| `MIN_RETRY_DELAY` | `30` | Seconds between attempts |
| `RETRY_MODEL` | (same as BUILD_MODEL) | Model for fix/retry attempts |
