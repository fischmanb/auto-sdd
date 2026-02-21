# Handoff Prompts for Successor Agents

> **Last updated**: 2026-02-20
> **Last agent**: Round 3 (claude/setup-auto-sdd-framework-INusW)
> **Repo**: fischmanb/auto-sdd

---

## How to Use This File

Each section below is a self-contained prompt. Copy one prompt at a time into a new Claude Code session. They are ordered by priority and can be done independently (no ordering dependency unless noted).

**Before each prompt**: Fork from the current integration branch:

    git fetch origin
    git checkout -b claude/<new-task-branch> \
      origin/claude/review-auto-sdd-framework-z0smI

Do NOT fork from `main` or from an older agent branch. The integration
branch contains all cumulative work from prior agents.

**After each prompt**: Verify with the checklist at the bottom of this file.

---

## Context for All Prompts

Copy this paragraph into every session to give the agent baseline context:

> You're working on `auto-sdd`, a spec-driven development automation system. It has two orchestration scripts (`scripts/build-loop-local.sh` and `scripts/overnight-autonomous.sh`) that build features from a roadmap by invoking AI agents via the `agent` CLI. Shared reliability functions live in `lib/reliability.sh`. Read `Agents.md` first — it has the full work log, known gaps, and verification checklist. All tests should pass before you commit: `./tests/test-reliability.sh` and `DRY_RUN_SKIP_AGENT=true ./tests/dry-run.sh`. Always fork your working branch from the integration branch (`claude/review-auto-sdd-framework-z0smI`), not from `main`. After completing work, request that your branch be merged into the integration branch so future agents inherit your changes.

---

## Prompt 1: Wire `run_parallel_drift_checks` into the Independent Build Pass

**Estimated scope**: ~50 lines changed in `scripts/build-loop-local.sh`
**Risk**: Medium (touches the build loop hot path)

```
Context: You're working on `auto-sdd`. Read `Agents.md` first for full context.

Task: Wire the existing `run_parallel_drift_checks()` function (defined in
`lib/reliability.sh`) into `scripts/build-loop-local.sh`.

Current state:
- `run_parallel_drift_checks` is defined and tested but NEVER CALLED
- The independent build pass (and the "both" strategy's independent pass)
  currently runs drift checks serially inside the per-feature loop
- The function expects an array of "spec_file:source_files" pairs

What to do:
1. Read `scripts/build-loop-local.sh` fully. Find the independent build pass.
2. During the independent build loop, accumulate drift targets into an array:
   DRIFT_PAIRS+=("$spec_file:$source_files")
   (The spec_file and source_files are already extracted via parse_signal)
3. After the independent build loop completes, if PARALLEL_VALIDATION=true,
   call `run_parallel_drift_checks "${DRIFT_PAIRS[@]}"` instead of having
   already done serial drift checks inside the loop.
4. If PARALLEL_VALIDATION=false (default), keep the existing serial behavior.
5. Update the test in `tests/test-reliability.sh` — the "Functions called
   from scripts" section has an INFO line about this being unwired. Change
   it to a PASS check.
6. Update `Agents.md` — remove `run_parallel_drift_checks` from the
   "Known Gaps" section and update the "Called from" column in the
   lib/reliability.sh table.

Verification:
- bash -n scripts/build-loop-local.sh
- ./tests/test-reliability.sh (all pass, including the new check)
- DRY_RUN_SKIP_AGENT=true ./tests/dry-run.sh
- grep "run_parallel_drift_checks" scripts/build-loop-local.sh | grep -v '#'
  (should show at least one non-comment call site)

Do NOT:
- Change the serial drift check behavior when PARALLEL_VALIDATION=false
- Modify overnight-autonomous.sh (it doesn't have independent strategy)
- Add new functions to lib/reliability.sh (it already has everything needed)
```

---

## Prompt 2: Make Resume Skip Already-Built Features

**Estimated scope**: ~15 lines changed in `scripts/build-loop-local.sh`
**Risk**: Low

```
Context: You're working on `auto-sdd`. Read `Agents.md` first for full context.

Task: Make the resume capability actually skip features that were already built.

Current state:
- `read_state()` sets RESUME_INDEX to skip the loop counter forward
- But if the roadmap wasn't updated to "completed" before the crash, the
  feature at RESUME_INDEX gets rebuilt unnecessarily
- The state file's `completed_features` array has the names of built features

What to do:
1. Read `scripts/build-loop-local.sh`. Find where `read_state` is called
   and where the build loop iterates over features.
2. After `read_state`, parse the `completed_features` JSON array from the
   state file into the BUILT_FEATURE_NAMES bash array. Use awk or grep
   (no jq dependency).
3. Inside the build loop, before calling the agent, check if the current
   feature name is already in BUILT_FEATURE_NAMES. If so, log a skip
   message and continue to the next feature.
4. Add a test case to `tests/test-reliability.sh` that writes state with
   completed features, reads it back, and verifies the array is populated.

Verification:
- bash -n scripts/build-loop-local.sh
- ./tests/test-reliability.sh
- DRY_RUN_SKIP_AGENT=true ./tests/dry-run.sh

Do NOT:
- Change the state file format
- Add a jq dependency
- Modify overnight-autonomous.sh
```

---

## Prompt 3: Harden `write_state` JSON Generation

**Estimated scope**: ~20 lines changed in `lib/reliability.sh`, ~10 in tests
**Risk**: Low

```
Context: You're working on `auto-sdd`. Read `Agents.md` first for full context.

Task: Make `write_state()` in `lib/reliability.sh` produce valid JSON even
when branch names or strategy names contain special characters.

Current state:
- `write_state()` uses raw string interpolation for branch_strategy and
  current_branch: "$strategy" and "$current_branch" go directly into the
  JSON heredoc without escaping
- `completed_features_json()` already properly escapes " and \ — but
  write_state's other fields don't
- Typical values (like "chained" or "auto/feature-1") work fine, but a
  branch name containing a quote would produce invalid JSON

What to do:
1. Read `lib/reliability.sh`, find `write_state()` (around line 87)
2. Escape `strategy` and `current_branch` the same way
   `completed_features_json` escapes feature names:
   printf '%s' "$var" | sed 's/\\/\\\\/g; s/"/\\"/g'
3. If `jq` is available, optionally use it to validate the output
   (but don't make jq a required dependency)
4. Add test cases to `tests/test-reliability.sh`:
   - write_state with a branch name containing a double quote
   - write_state with a branch name containing a backslash
   - Verify the state file is valid JSON (with jq if available)

Verification:
- bash -n lib/reliability.sh
- ./tests/test-reliability.sh (all pass including new cases)
- DRY_RUN_SKIP_AGENT=true ./tests/dry-run.sh
```

---

## Prompt 4: Clean Up Orphaned Library Files

**Estimated scope**: Investigation + possible deletion or integration
**Risk**: Low (orphaned code)

```
Context: You're working on `auto-sdd`. Read `Agents.md` first for full context.

Task: Investigate and resolve the orphaned `lib/common.sh` and `lib/models.sh`
files.

Current state:
- `lib/common.sh` (110 lines) defines: check_model_health, call_model,
  extract_content, parse_files_from_output, validate_json,
  has_pending_features, update_spec_status
- `lib/models.sh` (50 lines) defines: check_all_models
- Neither file is sourced by build-loop-local.sh or overnight-autonomous.sh
- They appear to serve the stages/ infrastructure (01-plan.sh through
  04-fix.sh) and framework/ai-dev

What to do:
1. Check if stages/*.sh or framework/ai-dev actually source these files
2. If they do: leave them alone but add a comment at the top of each file
   clarifying they serve the stages/ system, not the scripts/ system
3. If they don't: these files are fully orphaned. Either:
   a. Delete them (if stages/ is deprecated), or
   b. Wire them into stages/ if stages/ is still used but missing the source
4. Update Agents.md to reflect whatever you decide

Verification:
- grep -r "common.sh\|models.sh" stages/ framework/ scripts/
- bash -n on any modified files
- ./tests/test-reliability.sh
```

---

## Prompt 5: Add Live Integration Test

**Estimated scope**: ~50 lines in `tests/dry-run.sh`
**Risk**: Low (additive only)
**Prerequisite**: Requires a running agent endpoint (cannot run in CI without one)

```
Context: You're working on `auto-sdd`. Read `Agents.md` first for full context.

Task: Enhance `tests/dry-run.sh` to do a real end-to-end test when an agent
is available.

Current state:
- `tests/dry-run.sh` has a `structural_test()` (no agent needed) and a
  `full_test()` (requires `agent` CLI)
- The full_test runs build-loop-local.sh with MAX_FEATURES=1 but doesn't
  validate the output thoroughly
- No test currently validates signal parsing, drift check flow, or state
  persistence after a real agent run

What to do:
1. Read `tests/dry-run.sh` fully
2. In `full_test()`, after the build loop runs:
   a. Check if FEATURE_BUILT signal was emitted in the output
   b. Check if the roadmap was updated (grep for status change)
   c. Check if state file was created and has expected structure
   d. If DRIFT_CHECK was enabled, check for NO_DRIFT or DRIFT_FIXED signal
3. Add a `--verbose` flag that shows full agent output for debugging
4. Make the test idempotent (clean up all artifacts including git branches)

Verification:
- DRY_RUN_SKIP_AGENT=true ./tests/dry-run.sh (structural still passes)
- If agent is available: ./tests/dry-run.sh (full test runs)
```

---

## Prompt 6: Feature Parity Audit — overnight-autonomous.sh

**Estimated scope**: Investigation + ~30 lines
**Risk**: Medium

```
Context: You're working on `auto-sdd`. Read `Agents.md` first for full context.

Task: Audit overnight-autonomous.sh for feature parity with
build-loop-local.sh and close any meaningful gaps.

Current state (features present in build-loop but not overnight):
- Resume state (write_state/read_state/clean_state) — overnight doesn't
  have crash recovery
- run_parallel_drift_checks — only relevant for independent strategy
- "both" and "sequential" branch strategies — overnight only supports
  chained and independent
- Code review step — overnight has it but may not use run_agent_with_backoff
  for the review agent call

What to do:
1. Read both scripts fully
2. For each feature in build-loop, check if overnight has it or needs it
3. Add resume state to overnight if it runs long enough to benefit from
   crash recovery (it does — overnight runs can be 8+ hours)
4. Verify ALL agent calls in overnight use run_agent_with_backoff (not
   raw agent invocations)
5. Document which gaps are intentional (e.g., overnight doesn't need
   "sequential" strategy) vs accidental

Verification:
- bash -n scripts/overnight-autonomous.sh
- ./tests/test-reliability.sh
- grep "run_agent_with_backoff" scripts/overnight-autonomous.sh
  (should match all agent invocations)
- grep "agent " scripts/overnight-autonomous.sh | grep -v "run_agent_with_backoff"
  (should show NO raw agent calls)
```

---

## Verification Checklist (run after every prompt)

```bash
# 1. Syntax — all scripts must pass
bash -n scripts/build-loop-local.sh
bash -n scripts/overnight-autonomous.sh
bash -n lib/reliability.sh

# 2. Unit tests — all 41+ assertions must pass
./tests/test-reliability.sh

# 3. Structural dry-run
DRY_RUN_SKIP_AGENT=true ./tests/dry-run.sh

# 4. No functions defined but never called
# (test-reliability.sh checks this automatically, but you can also manually):
for func in acquire_lock run_agent_with_backoff truncate_for_context \
            check_circular_deps write_state read_state clean_state \
            completed_features_json; do
    echo -n "$func: "
    grep -l "$func" scripts/*.sh | head -1 || echo "NOT CALLED"
done

# 5. Both scripts source the shared library
grep "source.*reliability.sh" scripts/*.sh
```

---

## What NOT to Do

These are patterns from rounds 1-3 that caused problems:

1. **Don't define a function without verifying it's called.** This is the #1 agent failure mode. After adding any function, grep for call sites.
2. **Don't trust self-assessment.** Run the tests. If you can't run them, say so explicitly.
3. **Don't duplicate code between scripts.** Put shared logic in `lib/reliability.sh`.
4. **Don't add a `jq` dependency.** The codebase intentionally avoids it for portability. Use awk/sed.
5. **Don't modify both scripts in the same prompt** if you can avoid it. Smaller scopes = fewer mistakes.
6. **Don't delete the Agent Work Log in Agents.md.** Append to it.
