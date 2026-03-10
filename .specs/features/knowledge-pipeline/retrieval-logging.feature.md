# Feature Spec: retrieval-logging

## Problem

After feature #12 wires `query_relevant()` into the prompt builder, there is no record of what
knowledge was retrieved for each feature build. Without a retrieval log, there is no way to
measure whether retrieval quality changes over time, correlate retrieval with build outcomes,
or detect degradation.

## Solution

Modify `py/auto_sdd/lib/prompt_builder.py`:

1. **Add `log_retrieval(log_path, feature_name, query_text, results, timestamp) -> None`**:
   - Appends one JSONL line to `log_path` with:
     ```json
     {
       "ts": "ISO timestamp",
       "feature": "feature_name",
       "query": "query_text (first 200 chars)",
       "returned_ids": ["L-00042", "EVAL-auth-...", ...],
       "bm25_ranks": [0.83, 1.21, ...],
       "count": 5
     }
     ```
   - Log path: `{project_dir}/.sdd-state/retrieval-log.jsonl`
   - Append mode — never truncate

2. **In `query_knowledge_for_feature()`**: after calling `query_relevant()` and before
   `format_knowledge_section()`, call `log_retrieval()` with the raw results.

3. **Graceful degradation**: if log write fails (permissions, disk full), log warning and
   continue. Retrieval logging is advisory — never blocks a build.

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/lib/prompt_builder.py` | Add `log_retrieval()`, call it from `query_knowledge_for_feature()` |

## Testing

- `log_retrieval()` creates JSONL file if it doesn't exist
- `log_retrieval()` appends (not overwrites) on subsequent calls
- Each JSONL line is valid JSON with all required fields
- `query_knowledge_for_feature()` writes a log entry when store has entries
- `query_knowledge_for_feature()` does NOT write a log entry when store is missing (no empty entries)
- Log write failure does not crash prompt building

## Constraints

- JSONL format — one JSON object per line, no pretty-printing
- Log file size is unbounded by design (periodic cleanup is a separate concern)
- `query` field truncated to 200 chars to prevent log bloat
- No external deps — stdlib `json` only
