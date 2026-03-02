# Agent Prompt Checklist

Every agent prompt must include these sections. Missing any is a dispatch blocker.

## 1. Preconditions
- Branch state (main, up to date, clean)
- Dependencies from prior dispatches (merged? files exist?)
- Required tools/commands available

## 2. Scope Estimate (L-00143 — show your work)

Required format — bare numbers without calculation are not acceptable:

```
Files to read:
  [filename]: ~[N] lines × 4              = [X] tok
  This prompt: ~[N] lines × 4             = [X] tok
Reasoning overhead:                          5000 tok
Expected output:
  [description]: ~[N] lines × 4           = [X] tok
Total: [sum] tokens
Ceiling: (max_context - current_context_used) × quality_factor
Utilization: [total / ceiling] = [N]%
```

Before writing estimate, check for calibrated actuals:
```bash
source lib/general-estimates.sh
query_estimate_actuals "[activity_type]"
```
If calibration_ready: true → use avg_actual_tokens instead of heuristic.

## 3. Hard Constraints
- What the agent must NOT do
- Push restrictions (L-00005)
- Scope boundaries

## 4. Verification
- All checks must be mechanical (grep, diff, test runs)
- List expected output for each check
- All must pass before reporting completion

## 5. STOP Conditions
- When to halt and report instead of working around (L-00011)

## 6. Core Learnings Injection
Every agent prompt must include a Context section referencing CLAUDE.md's
Core Learnings block. Agent must read CLAUDE.md before starting work.
If hard constraints contradict a core learning, the core learning wins
unless Brian explicitly overrides for that specific dispatch.

## 7. Token Usage Report (mandatory)

Every agent prompt MUST end with a token report section. Without actuals,
L-00143 calibration has no data.

Agent runs at completion:
```bash
source lib/general-estimates.sh
ACTUAL=$(get_session_actual_tokens)
ACTIVE=$(echo "$ACTUAL" | python3 -c "import sys,json; print(json.load(sys.stdin).get('active_tokens',0))")
CUMULATIVE=$(echo "$ACTUAL" | python3 -c "import sys,json; print(json.load(sys.stdin).get('cumulative_tokens',0))")
echo "=== TOKEN USAGE REPORT ==="
echo "activity_type: [name]"
echo "estimated_tokens_pre: [N]"
echo "active_tokens (input+output): $ACTIVE"
echo "cumulative_tokens (incl cache): $CUMULATIVE"
echo "source: $(echo "$ACTUAL" | python3 -c "import sys,json; print(json.load(sys.stdin).get('source','unknown'))")"
echo "=== END REPORT ==="

append_general_estimate "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"activity_type\":\"[name]\",\"estimated_tokens_pre\":[N],\"active_tokens\":$ACTIVE,\"cumulative_tokens\":$CUMULATIVE,\"tool_calls\":[COUNT],\"notes\":\"actual via get_session_actual_tokens\"}"
```

Agent MUST include report in completion summary AND append to general-estimates.jsonl.
