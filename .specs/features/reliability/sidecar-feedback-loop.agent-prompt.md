Implement the sidecar → build agent feedback loop per the spec at .specs/features/reliability/sidecar-feedback-loop.feature.md

Read that spec first. Then make these changes to scripts/build-loop-local.sh:

## 1. Add three new functions (place them near the other helper functions, after check_lint and before build_feature_prompt):

### read_latest_eval_feedback()
- Reads the most recent eval-*.json from $EVAL_OUTPUT_DIR (default: $PROJECT_DIR/logs/evals), excluding eval-campaign-* files
- Extracts: framework_compliance, scope_assessment, integration_quality, repeated_mistakes, eval_notes
- Returns a formatted multi-line string with warnings only for non-passing values
- Returns empty string if no evals dir or no eval files exist
- Use awk for JSON field extraction (same pattern already used in eval-sidecar.sh)

### update_repeated_mistakes()
- Takes a single mistake string argument
- Appends to $STATE_DIR/repeated-mistakes.txt if not already present (dedup via grep -qF)
- No-ops on empty string or "none"
- Creates $STATE_DIR and file if they don't exist

### get_cumulative_mistakes()
- Reads $STATE_DIR/repeated-mistakes.txt
- Returns formatted string: "KNOWN REPEATED MISTAKES (from prior features in this campaign — do NOT repeat these):" followed by "- {mistake}" per line
- Returns empty string if file missing or empty

## 2. Modify build_feature_prompt() to inject feedback

In the build_feature_prompt function, BEFORE the "After completion, output EXACTLY these signals" block, add:

```bash
local eval_feedback
eval_feedback=$(read_latest_eval_feedback)
local cumulative_mistakes
cumulative_mistakes=$(get_cumulative_mistakes)
```

Then in the heredoc/cat block, between the codebase summary section and the signal output instructions, add:

```
${eval_feedback:+## Quality Gate Feedback (from automated eval of prior features)
${eval_feedback}
}${cumulative_mistakes:+## ${cumulative_mistakes}
}
```

## 3. Add eval read + mistake tracking in the success path

Find the block where BUILT_FEATURE_NAMES+=("$feature_name") is called (the main success path, not the inferred-success paths). Right after that line, before the write_state call, add:

```bash
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

Also add the same block after the two inferred-success paths (inferred-drift and inferred-retry, around lines where BUILT_FEATURE_NAMES is set with "inferred" in the timing label).

## Constraints

- Do NOT modify eval-sidecar.sh or lib/eval.sh — the sidecar already writes the correct JSON format
- Do NOT add any new env vars — this activates automatically when eval files exist
- Do NOT add blocking gates — this is advisory only
- Keep the feedback functions self-contained. If $EVAL_OUTPUT_DIR doesn't exist or has no files, everything no-ops silently
- The repeated-mistakes.txt file should be in $STATE_DIR (same as resume.json)
- Do NOT modify the existing signal parsing, branch management, or retry logic

## Verification

After making changes:
1. Run `bash -n scripts/build-loop-local.sh` to verify no syntax errors
2. Create a test eval file: `mkdir -p logs/evals && echo '{"framework_compliance":"warn","scope_assessment":"moderate","repeated_mistakes":"isApproved_filter_missing","integration_quality":"minor_issues","eval_notes":"test note"}' > logs/evals/eval-test-feature-1.json`
3. Source the script functions and test: the read_latest_eval_feedback function should return warning lines about framework compliance and scope
4. Test get_cumulative_mistakes with an empty and populated repeated-mistakes.txt
5. Clean up test files

Commit with message: "feat: sidecar feedback loop — inject eval findings into build agent prompts"

FEATURE_BUILT: sidecar-feedback-loop
SPEC_FILE: .specs/features/reliability/sidecar-feedback-loop.feature.md
SOURCE_FILES: scripts/build-loop-local.sh
