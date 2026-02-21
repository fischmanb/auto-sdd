# Code Review: Auto-SDD Framework

**Date**: 2026-02-21
**Branch reviewed**: `claude/setup-auto-sdd-framework-INusW` (merged into `claude/review-auto-sdd-framework-z2Ngc`)
**Reviewer**: Claude (Opus 4.6)
**Scope**: Full codebase review — all 30 files across 3 rounds of agent work

---

## Executive Summary

The framework is solid, well-documented, and honestly self-aware about its gaps. `Agents.md` is the best agent work log I've seen — it documents failures as candidly as successes. The reliability library extracts are clean, the test suite is thorough (41 assertions, all passing), and the architecture of "two systems, one repo" is clearly delineated.

**Critical bugs found: 3** (one causes a crash, two cause silent misbehavior)
**Design issues: 5** (functional but suboptimal)
**Documentation gaps: 2** (minor)
**Total files reviewed: 30**

---

## Critical Bugs

### BUG-1: Typo in `framework/ai-dev` causes crash when issues > 0

**File**: `framework/ai-dev:101`
**Severity**: CRASH

```bash
# Line 101:
ISSUE_COUNT=$(jq '.issues | length' review.json 2>/dev/null || echo 0)
if [ "$ISSUE_COUNT" -gt 0 ]; then
    log "Found $ISSUEUE issues, attempting fix..."   # <-- $ISSUEUE instead of $ISSUE_COUNT
```

`$ISSUEUE` is an undefined variable. This line will print "Found issues, attempting fix..." (blank count) instead of the actual number. Not a crash per se (bash treats unset vars as empty), but with `set -e` active at the top of the script, this combined with the `-gt` comparison will cause the script to silently swallow the count.

**Fix**: Change `$ISSUEUE` to `$ISSUE_COUNT`.

---

### BUG-2: `overnight-autonomous.sh` uses `local` inside non-function context

**File**: `scripts/overnight-autonomous.sh` (Step 3 build loop, around line 400+)
**Severity**: SYNTAX ERROR on some bash versions

```bash
local AGENT_EXIT=0
local BUILD_PROMPT_OVERNIGHT="..."
```

These `local` declarations appear inside the `for i in $(seq 1 "$MAX_FEATURES")` loop body but **outside any function**. In bash, `local` is only valid inside a function. Most bash versions warn but don't error. Some strict modes will reject this.

By contrast, `build-loop-local.sh` wraps its build loop inside `run_build_loop()`, correctly using `local` within a function scope.

**Fix**: Remove the `local` keywords from these variable declarations in the top-level loop. They should just be regular variable assignments.

---

### BUG-3: `overnight-autonomous.sh` sources `reliability.sh` before `SCRIPT_DIR` is set

**File**: `scripts/overnight-autonomous.sh:51`
**Severity**: ERROR — script will fail to source the library

```bash
# Line 51 (early in the file, after color/logging definitions):
source "$SCRIPT_DIR/../lib/reliability.sh"
```

But `SCRIPT_DIR` is not set until line ~100:
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

The `source` command at line 51 will fail because `$SCRIPT_DIR` is empty at that point, causing the script to try to source `/../lib/reliability.sh` which doesn't exist.

**Why tests didn't catch this**: `bash -n` only checks syntax, not runtime variable ordering. The unit tests source `reliability.sh` directly, not through `overnight-autonomous.sh`.

**Fix**: Move the `source "$SCRIPT_DIR/../lib/reliability.sh"` line to after `SCRIPT_DIR` is assigned.

---

## Design Issues

### DESIGN-1: `run_cmd_safe()` doesn't add safety — identical code paths

**Files**: `scripts/build-loop-local.sh:356-367`, `scripts/overnight-autonomous.sh`

```bash
run_cmd_safe() {
    local cmd="$1"
    local is_custom="${2:-false}"
    if [ "$is_custom" = "true" ]; then
        warn "Executing custom command from .env.local: $cmd"
        bash -c "$cmd"
    else
        bash -c "$cmd"
    fi
}
```

Both branches do `bash -c "$cmd"`. The only difference is the warning message. The function name suggests it adds safety, but it doesn't — no input validation, no quoting protection, no timeout. The `bash -c` invocation is intentional (documented in Agents.md as allowing pipes), but the function name is misleading.

**Recommendation**: Either add actual safety (timeout, restricted env) or rename to `run_cmd_logged()` to accurately reflect what it does.

---

### DESIGN-2: `parse_signal` is duplicated between scripts

**Files**: `scripts/build-loop-local.sh:180-190`, `scripts/overnight-autonomous.sh:57-67`

The `parse_signal()` and `validate_required_signals()` functions are defined identically in both scripts. They were not extracted to `lib/reliability.sh` during Round 3.

Similarly `format_duration()`, `extract_drift_targets()`, `detect_build_check()`, `detect_test_check()`, `agent_cmd()`, `check_build()`, `check_tests()`, `should_run_step()` are all duplicated or near-duplicated.

**Recommendation**: Extract `parse_signal`, `validate_required_signals`, and `format_duration` into `lib/reliability.sh` (they have no script-specific dependencies). The detection functions are borderline — they could go either way.

---

### DESIGN-3: `lib/common.sh` uses `jq` but the rest of the project avoids it

**File**: `lib/common.sh:37,52,84`

`lib/common.sh` (used by stages/) relies on `jq` for JSON parsing (`jq -Rs`, `jq -r`, `jq empty`). This is fine for the stages system, but it creates a hidden dependency that contradicts the guidance in `HANDOFF-PROMPT.md` ("Don't add a jq dependency").

The project has two dependency profiles:
- System 1 (scripts/): no `jq`, uses `awk`/`sed` for portability
- System 2 (stages/): requires `jq` (and also `curl`, `bc`)

**Recommendation**: Document this split explicitly. Add a comment at the top of `lib/common.sh`: "# NOTE: This file requires jq. It serves stages/ only, not scripts/."

---

### DESIGN-4: `models.sh` has leading whitespace on function definition

**File**: `lib/models.sh:20`

```bash
 check_all_models() {    # Note: leading space before 'check_all_models'
```

This leading space is harmless but suggests copy-paste artifact. Could confuse pattern matching if someone greps for `^check_all_models`.

**Recommendation**: Remove the leading space.

---

### DESIGN-5: Overnight script's Slack/Jira triage uses raw agent call

**File**: `scripts/overnight-autonomous.sh` (Step 2, ~line 310)

The triage agent call and the code-review agent call use raw `$(agent_cmd ...)` instead of `run_agent_with_backoff`. This means rate-limit retries don't apply to these calls. The build agent call (Step 3) correctly uses `run_agent_with_backoff`.

`HANDOFF-PROMPT.md` Prompt 6 already identifies this gap.

**Recommendation**: Wrap all agent calls in `run_agent_with_backoff` for consistency.

---

## Code Quality Observations (Not Bugs)

### The `.env.local` loader in `build-loop-local.sh` is well-engineered

Lines 95-108: The custom `.env.local` parser correctly:
- Skips comments and blank lines
- Uses `[[ -n "${!key+x}" ]]` to check if a variable is already set (command-line override wins)
- Strips both single and double quotes from values
- Uses regex capture groups for clean parsing

This is significantly better than the typical `source .env.local` approach, which would overwrite command-line env vars. Good design choice.

### The DFS cycle detection in `check_circular_deps()` is portable and correct

Using bash associative arrays for the DFS rather than awk user-defined functions (which require gawk) was the right call for mawk compatibility. The implementation correctly uses three-state marking (0=unvisited, 1=in-stack, 2=done) for standard Tarjan-style cycle detection.

### `truncate_for_context()` is clever

The awk filter that strips non-Gherkin content while preserving frontmatter and scenario lines is a good approach to context budget management. The 4-chars-per-token estimate is reasonable for English text.

### Test suite is well-structured

`test-reliability.sh` tests both happy paths and edge cases, includes a meta-test (grep check that functions are called), and correctly handles the "known gap" of `run_parallel_drift_checks` being unwired. The `dry-run.sh` structural test is a good smoke test.

---

## Remaining Known Gaps (from Agents.md — confirmed accurate)

These gaps are documented in `Agents.md` and `HANDOFF-PROMPT.md`. I verified each:

| Gap | Status | Verification |
|-----|--------|-------------|
| `run_parallel_drift_checks` not wired | Confirmed | `grep -c "run_parallel_drift_checks" scripts/build-loop-local.sh` returns only comment hits |
| Resume doesn't skip already-built features | Confirmed | `read_state` sets `RESUME_INDEX` but doesn't populate `BUILT_FEATURE_NAMES` from state |
| `write_state` JSON escaping for branch names | Confirmed | Raw `"$strategy"` interpolation at line 98 of `lib/reliability.sh` |
| `lib/common.sh` and `lib/models.sh` "orphaned" | **Partially incorrect** | They ARE sourced by all 4 stages (`stages/*.sh`). They're only "orphaned" from the scripts/ perspective. Agents.md correctly notes this but the "orphaned" label is misleading. |

---

## File-by-File Summary

| File | Lines | Verdict | Notes |
|------|-------|---------|-------|
| `lib/reliability.sh` | 385 | Good | Clean extraction, proper guards, good defaults |
| `scripts/build-loop-local.sh` | 1311 | Good | Well-structured, comprehensive config options |
| `scripts/overnight-autonomous.sh` | ~790 | Has bugs | BUG-2 (local outside function), BUG-3 (source order), raw agent calls |
| `framework/ai-dev` | 136 | Has bug | BUG-1 ($ISSUEUE typo) |
| `tests/test-reliability.sh` | 457 | Good | Thorough, 41 assertions |
| `tests/dry-run.sh` | 213 | Good | Structural + full integration |
| `scripts/generate-mapping.sh` | 358 | Good | Robust with `awk` frontmatter extraction |
| `lib/common.sh` | 109 | OK | Serves stages/ correctly, needs jq note |
| `lib/models.sh` | 49 | Minor issue | Leading whitespace on function def |
| `stages/01-plan.sh` | 100 | OK | |
| `stages/02-build.sh` | 100 | OK | |
| `stages/03-review.sh` | 115 | OK | Graceful degradation if reviewer offline |
| `stages/04-fix.sh` | 96 | OK | Confidence threshold gating is smart |
| `Agents.md` | 321 | Excellent | Best agent work log I've seen |
| `ARCHITECTURE.md` | 164 | Good | Clear context-rot rationale |
| `HANDOFF-PROMPT.md` | 310 | Excellent | Actionable, scoped, with verification checklists |
| `.env.local.example` | 167 | Good | Comprehensive with inline documentation |
| `CLAUDE.md` | Long | Good | SDD workflow well-defined |
| `start.sh` | 77 | OK | Standard llama.cpp management |
| `stop.sh` | ~16 | OK | |
| `status.sh` | ~25 | OK | |
| `demo.sh` | ~134 | OK | |
| `install.sh` | ~30 | OK | |
| `download-models.sh` | ~48 | OK | |

---

## Recommendations (Priority Order)

1. **Fix BUG-1, BUG-2, BUG-3** (critical — these will cause runtime failures)
2. **Extract `parse_signal`, `validate_required_signals`, `format_duration`** into `lib/reliability.sh` to reduce duplication
3. **Document the jq dependency split** between System 1 and System 2
4. **Wrap all overnight agent calls** in `run_agent_with_backoff`
5. **Work through HANDOFF-PROMPT.md prompts 1-3** (parallel drift, resume, JSON escaping)
6. **Consider renaming `run_cmd_safe` to `run_cmd_logged`** to match actual behavior

---

## Test Results (at time of review)

```
$ bash -n scripts/build-loop-local.sh && bash -n scripts/overnight-autonomous.sh && bash -n lib/reliability.sh
# All pass

$ ./tests/test-reliability.sh
# 41 passed, 0 failed

$ DRY_RUN_SKIP_AGENT=true ./tests/dry-run.sh
# All dry-run tests passed
```
