# Feature Spec: Sidecar → Build Agent Feedback Loop

## Problem

The eval sidecar (`scripts/eval-sidecar.sh`) runs alongside the build loop, evaluating each feature commit for framework compliance, scope creep, integration quality, and repeated mistakes. It writes eval JSON files to `$EVAL_OUTPUT_DIR` (default: `$PROJECT_DIR/logs/evals/`). 

**The build loop never reads these files.** The build agent that caused a problem doesn't know about it. The next build agent doesn't know about patterns from prior features. The sidecar is an observer with no actuator.

## Evidence

From the v3 Haiku campaign (5 evals captured):
- **0/5 framework compliance passes** — every eval flagged issues
- **Repeated `isApproved` filter omission** — same security bug in multiple features
- **Server/client RSC violation** — runtime-breaking bug that passed TypeScript compilation and tests
- **Trivially-passing tests** — tests that satisfy `test_files_touched: true` without testing the contract

Full analysis: `campaign-results/reports/sidecar-findings.md`

## Solution

Inject sidecar findings into the build agent's prompt before each feature build. Three components:

### 1. Read latest eval after each feature completes

**Where**: `build-loop-local.sh`, in the success path after `FEATURE_BUILT` is confirmed and drift check passes, BEFORE moving to the next feature.

**What**: Read the most recent eval JSON from `$EVAL_OUTPUT_DIR`. The sidecar runs asynchronously — the eval for the feature that just built may not exist yet. Read whatever the most recent eval IS (it will be from a prior feature, which is still useful).

```bash
# New function: read_latest_eval_feedback
# Returns a formatted string suitable for injection into the next build prompt.
# Returns empty string if no evals exist or sidecar is disabled.
read_latest_eval_feedback() {
    local eval_dir="${EVAL_OUTPUT_DIR:-$PROJECT_DIR/logs/evals}"
    
    if [ ! -d "$eval_dir" ]; then
        echo ""
        return
    fi
    
    # Get the most recent eval file (by modification time)
    local latest_eval
    latest_eval=$(ls -t "$eval_dir"/eval-*.json 2>/dev/null | grep -v 'eval-campaign-' | head -1)
    
    if [ -z "$latest_eval" ]; then
        echo ""
        return
    fi
    
    # Extract key fields
    local fw_compliance scope_assessment integration_quality repeated_mistakes eval_notes
    fw_compliance=$(awk -F'"' '/"framework_compliance"/{print $4}' "$latest_eval" 2>/dev/null || echo "")
    scope_assessment=$(awk -F'"' '/"scope_assessment"/{print $4}' "$latest_eval" 2>/dev/null || echo "")
    integration_quality=$(awk -F'"' '/"integration_quality"/{print $4}' "$latest_eval" 2>/dev/null || echo "")
    repeated_mistakes=$(awk -F'"' '/"repeated_mistakes"/{print $4}' "$latest_eval" 2>/dev/null || echo "")
    eval_notes=$(awk -F'"' '/"eval_notes"/{print $4}' "$latest_eval" 2>/dev/null || echo "")
    
    # Build feedback block (only if there's something to report)
    local feedback=""
    
    if [ "$fw_compliance" = "warn" ] || [ "$fw_compliance" = "fail" ]; then
        feedback="${feedback}⚠ FRAMEWORK COMPLIANCE: ${fw_compliance}. Update roadmap to ✅ after completion. Add Agents.md round entry. Match spec frontmatter exactly.\n"
    fi
    
    if [ "$scope_assessment" = "moderate" ] || [ "$scope_assessment" = "sprawling" ]; then
        feedback="${feedback}⚠ SCOPE: Previous feature had scope creep (${scope_assessment}). Only modify files directly required by this feature's spec. Do not introduce pages, routes, or components not in the spec.\n"
    fi
    
    if [ -n "$repeated_mistakes" ] && [ "$repeated_mistakes" != "none" ]; then
        feedback="${feedback}🔴 REPEATED MISTAKE: ${repeated_mistakes} — This pattern has occurred in prior features. Check your implementation specifically for this issue before committing.\n"
    fi
    
    if [ "$integration_quality" = "major_issues" ]; then
        feedback="${feedback}🔴 INTEGRATION: Previous feature had major integration issues. Verify server/client component boundaries. No event handlers on server components. No missing authorization filters.\n"
    fi
    
    if [ -n "$eval_notes" ]; then
        feedback="${feedback}📋 EVAL NOTES: ${eval_notes}\n"
    fi
    
    echo -e "$feedback"
}
```

### 2. Maintain cumulative repeated_mistakes file

**Where**: New file `$STATE_DIR/repeated-mistakes.txt` (alongside `resume.json`).

**What**: After each eval is read, append any new `repeated_mistakes` values. This file grows across the campaign and gets injected into every subsequent build prompt.

```bash
# New function: update_repeated_mistakes
# Appends new mistake pattern to cumulative list (deduped).
update_repeated_mistakes() {
    local mistake="$1"
    local mistakes_file="$STATE_DIR/repeated-mistakes.txt"
    
    if [ -z "$mistake" ] || [ "$mistake" = "none" ]; then
        return
    fi
    
    mkdir -p "$STATE_DIR"
    touch "$mistakes_file"
    
    # Deduplicate
    if ! grep -qF "$mistake" "$mistakes_file" 2>/dev/null; then
        echo "$mistake" >> "$mistakes_file"
    fi
}

# New function: get_cumulative_mistakes
# Returns formatted list of all known repeated mistakes for prompt injection.
get_cumulative_mistakes() {
    local mistakes_file="$STATE_DIR/repeated-mistakes.txt"
    
    if [ ! -f "$mistakes_file" ] || [ ! -s "$mistakes_file" ]; then
        echo ""
        return
    fi
    
    local mistakes=""
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        mistakes="${mistakes}\n- ${line}"
    done < "$mistakes_file"
    
    if [ -n "$mistakes" ]; then
        echo -e "KNOWN REPEATED MISTAKES (from prior features in this campaign — do NOT repeat these):${mistakes}"
    fi
}
```

### 3. Inject into build_feature_prompt

**Where**: `build_feature_prompt()` function in `build-loop-local.sh`.

**What**: Add a new section between the codebase summary block and the signal output instructions.

```bash
# In build_feature_prompt(), after the codebase summary block:

local eval_feedback
eval_feedback=$(read_latest_eval_feedback)
local cumulative_mistakes
cumulative_mistakes=$(get_cumulative_mistakes)

# Then in the prompt heredoc, after the codebase summary and before
# "After completion, output EXACTLY these signals":

${eval_feedback:+## Quality Gate Feedback (from automated eval of prior features)
${eval_feedback}
}${cumulative_mistakes:+## ${cumulative_mistakes}
}
```

### 4. Severity gating (optional, phase 2)

**Not in this implementation.** Advisory-only for now. If the feedback loop proves effective at reducing repeated mistakes, add blocking for `integration_quality: "major_issues"` in a future round.

Rationale: Blocking kills throughput. The v2 campaign built 28 features at 4.0/hour with zero failures. Adding a blocking gate risks introducing false-positive halts. Start advisory, measure whether mistake rates drop, then decide on blocking.

## Files to Modify

| File | Change |
|---|---|
| `scripts/build-loop-local.sh` | Add `read_latest_eval_feedback()`, `update_repeated_mistakes()`, `get_cumulative_mistakes()`. Modify `build_feature_prompt()` to inject feedback. Add eval read + mistake update in success path after each feature. |
| `lib/reliability.sh` | No changes (state helpers already exist). |
| `scripts/eval-sidecar.sh` | No changes (already writes correct JSON format). |

## Integration Point

In `build-loop-local.sh`, the success path where `feature_done=true` is set (~line 1280), after the feature is confirmed built and before the next iteration:

```bash
# After: BUILT_FEATURE_NAMES+=("$feature_name")
# Before: write_state (resume checkpoint)
# Add:

# Read latest sidecar eval and update cumulative mistakes
local _latest_eval_dir="${EVAL_OUTPUT_DIR:-$PROJECT_DIR/logs/evals}"
local _latest_eval_file
_latest_eval_file=$(ls -t "$_latest_eval_dir"/eval-*.json 2>/dev/null | grep -v 'eval-campaign-' | head -1)
if [ -n "$_latest_eval_file" ]; then
    local _rm
    _rm=$(awk -F'"' '/"repeated_mistakes"/{print $4}' "$_latest_eval_file" 2>/dev/null || echo "")
    update_repeated_mistakes "$_rm"
    log "Eval feedback queued for next build agent"
fi
```

The `build_feature_prompt()` function already runs fresh for each feature (called inside the while loop), so the feedback will be current for each invocation.

## Testing

1. **Unit test**: Create a mock eval JSON in `logs/evals/`, run `read_latest_eval_feedback()`, verify output format contains expected warnings.
2. **Integration test**: Run a 2-feature build with sidecar enabled. After feature 1, verify feature 2's build log contains eval feedback section.
3. **Regression test**: Run with sidecar disabled (`EVAL_SIDECAR=false`). Verify `read_latest_eval_feedback()` returns empty and build_feature_prompt is unchanged.
4. **Cumulative test**: Pre-populate `repeated-mistakes.txt` with 3 entries. Verify `get_cumulative_mistakes()` returns all 3. Add a duplicate via `update_repeated_mistakes()`. Verify dedup works (still 3 entries).

## Config

No new env vars. The feature activates automatically when sidecar evals exist in `$EVAL_OUTPUT_DIR`. When no evals exist, the feedback functions return empty strings and the build prompt is unchanged from current behavior.

Optional future: `EVAL_FEEDBACK_BLOCKING=true` for phase 2 severity gating.

## Success Criteria

Run a campaign with feedback enabled and compare to v3 baseline:
- `repeated_mistakes` occurrences should decrease across the campaign
- `framework_compliance: "pass"` rate should increase from 0% baseline
- Build throughput should not degrade (advisory-only, no blocking gates)

## Context Budget

Feedback injection adds ~200-500 tokens per build prompt depending on findings. Cumulative mistakes list bounded by campaign length (typically <10 unique patterns). Total: <1% of build agent context window. Negligible cost/speed impact.
