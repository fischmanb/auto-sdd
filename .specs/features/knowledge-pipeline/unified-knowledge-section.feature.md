# Feature Spec: unified-knowledge-section

## Problem

After feature #12, the prompt builder calls `query_knowledge_for_feature()` but the prompt
template still has separate structural slots for "Eval Feedback", "Recent Learnings", and
"Cumulative Mistakes". The agent prompt needs a single, clean "Relevant Knowledge" section
that presents FTS5-ranked results without legacy section headers.

## Solution

Modify `py/auto_sdd/lib/prompt_builder.py`:

1. **Remove the three legacy section injections** from the prompt template in
   `build_feature_prompt()`:
   - Remove the `## Eval Feedback` section (was `eval_feedback` variable)
   - Remove the `## Recent Learnings` section (was injected via codebase summary)
   - Remove the `## Cumulative Mistakes` section (was `cumulative_mistakes` variable)
2. **Add a single `## Relevant Knowledge` section** after the codebase summary and
   before the hard constraints block:
   - Content comes from `query_knowledge_for_feature()` (feature #12)
   - If empty, the section header is omitted entirely (no "No relevant knowledge found")
3. **Apply the same change to `build_fix_prompt()` and `build_retry_prompt()`**
4. **Remove unused imports and variables**: `read_latest_eval_feedback`,
   `get_cumulative_mistakes`, `_read_recent_learnings` calls (functions stay, callers go)
5. **Update constraint injection placement**: the `_inject_constraint_patterns()` output
   must remain AFTER the knowledge section (constraints are higher priority than advisory knowledge)

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/lib/prompt_builder.py` | Replace 3 legacy sections with 1 unified section |
| `py/auto_sdd/lib/codebase_summary.py` | Remove `_read_recent_learnings()` call from `generate_codebase_summary()` output |

## Testing

- `build_feature_prompt()` output does NOT contain "Eval Feedback" header
- `build_feature_prompt()` output does NOT contain "Recent Learnings" header
- `build_feature_prompt()` output does NOT contain "Cumulative Mistakes" header
- `build_feature_prompt()` output contains "Relevant Knowledge" header when store has entries
- `build_feature_prompt()` output omits "Relevant Knowledge" header when store is empty
- Constraint patterns appear AFTER knowledge section
- `build_fix_prompt()` and `build_retry_prompt()` follow same structure
- Total prompt size does not regress (no duplication)

## Constraints

- Knowledge section must be max 80 lines (enforced by `format_knowledge_section` max_lines param)
- `MAX_TOTAL_PROMPT_LINES` (400) assertion still holds
- Constraint patterns are NOT part of the knowledge section — they remain separate
