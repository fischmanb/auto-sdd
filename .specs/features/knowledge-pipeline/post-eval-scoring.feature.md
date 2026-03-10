# Feature Spec: post-eval-scoring

## Problem

After a feature is built and eval'd, there is no comparison between what knowledge was
retrieved (retrieval log from feature #16) and what the eval actually found. This means
there is no feedback signal for retrieval quality during a live campaign — only the
offline backtest (feature #14) can measure it. A post-eval scoring step closes the loop
by computing hit/miss per feature, building the dataset for continuous optimization.

## Solution

Modify `py/auto_sdd/scripts/eval_sidecar.py`:

1. **Add `score_retrieval(retrieval_log_path, eval_result, feature_name) -> dict | None`**:
   - Reads the retrieval log JSONL, finds the entry matching `feature_name`
   - Extracts the `returned_ids` from the log entry
   - Extracts the eval signal types/findings from `eval_result`
   - Computes:
     - `hits`: IDs in both returned and eval-relevant
     - `misses`: IDs in eval-relevant but not returned (should have been retrieved)
     - `noise`: IDs in returned but not eval-relevant (irrelevant results)
     - `precision`: hits / (hits + noise)
     - `recall`: hits / (hits + misses)
   - Returns `{"feature": name, "hits": [...], "misses": [...], "noise": [...], "precision": float, "recall": float}`
   - Returns None if no retrieval log entry found for this feature

2. **Add `append_score_to_log(retrieval_log_path, feature_name, score) -> None`**:
   - Reads the JSONL, finds the line for `feature_name`
   - Rewrites that line with the score fields appended
   - This enriches the retrieval log with ground-truth comparison

3. **In the eval sidecar's per-feature eval flow**: after writing the eval JSON and
   store entry (feature #8), call `score_retrieval()` then `append_score_to_log()`.

4. **Graceful degradation**: if retrieval log doesn't exist or feature not found,
   skip scoring silently.

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/scripts/eval_sidecar.py` | Add score_retrieval, append_score_to_log, wire into eval flow |

## Testing

- `score_retrieval()` returns correct precision/recall for known inputs
- `score_retrieval()` returns None when feature not in retrieval log
- `append_score_to_log()` enriches the correct JSONL line without corrupting others
- Sidecar writes score after eval when retrieval log exists
- Missing retrieval log does not crash sidecar

## Constraints

- JSONL rewrite must be atomic (write to temp file, rename)
- Matching logic between eval signals and learning IDs uses the same scheme as backtest (feature #14)
- No external deps
- Scoring must not slow down the eval cycle (< 100ms per feature)
