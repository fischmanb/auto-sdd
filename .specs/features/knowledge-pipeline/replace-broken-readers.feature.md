# Feature Spec: replace-broken-readers

## Problem

Three read paths in the build pipeline are broken or nearly useless:

1. **`read_latest_eval_feedback()`** in `drift.py` — reads only the single most recent eval JSON out of
   113+. All other eval findings are invisible to the build agent.
2. **`_read_recent_learnings()`** in `codebase_summary.py` — reads `.specs/learnings/` markdown (project-local
   learnings), capped at 40 lines, no relevance filtering. Returns a wall of text that may be entirely
   irrelevant to the feature being built.
3. **`get_cumulative_mistakes()`** in `drift.py` / `MistakeTracker` — in-memory list that resets every
   build loop invocation. Volatile — nothing persists across runs.

All three produce unranked, unfiltered text that the prompt builder injects blindly.

## Solution

Modify `py/auto_sdd/lib/prompt_builder.py` and `py/auto_sdd/lib/codebase_summary.py`:

1. **Add `query_knowledge_for_feature(project_dir, feature_name, spec_text, top_k=10) -> str`**
   to `prompt_builder.py`:
   - Opens store at `{project_dir}/.sdd-state/knowledge.db`
   - Constructs query from `feature_name + " " + spec_text`
   - Calls `query_relevant(conn, query_text, top_k=top_k)`
   - Calls `format_knowledge_section(results)` to get prompt-injectable text
   - Closes store, returns formatted text
   - On any failure (missing DB, import error): returns empty string + logs warning
2. **In `build_feature_prompt()`**: replace the three separate injection calls
   (`read_latest_eval_feedback`, `_read_recent_learnings`, `get_cumulative_mistakes`)
   with a single call to `query_knowledge_for_feature()`.
3. **In `build_fix_prompt()` and `build_retry_prompt()`**: also call
   `query_knowledge_for_feature()` so fix/retry agents get the same knowledge context.
4. **Do NOT delete** the old functions yet — leave them in place but unused. Removal is a
   separate cleanup task after the new path is validated.

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/lib/prompt_builder.py` | Add `query_knowledge_for_feature()`, replace 3 injection calls |

## Testing

- `query_knowledge_for_feature()` returns formatted text when store exists with entries
- `query_knowledge_for_feature()` returns empty string when store doesn't exist (graceful)
- `build_feature_prompt()` output contains "Relevant Knowledge" section (not "Eval Feedback" or "Recent Learnings")
- `build_fix_prompt()` output contains "Relevant Knowledge" section
- `build_retry_prompt()` output contains "Relevant Knowledge" section
- Old functions still importable (not deleted)

## Constraints

- Store access is read-only in this module — no writes
- Graceful degradation is mandatory — missing store = empty section, not crash
- Feature spec text is read from disk within the function (resolved via `_resolve_spec_file`)
- `query_relevant` import must be guarded with try/except ImportError
