# Feature Spec: fts5-weight-tuner

## Problem

The FTS5 virtual table weights title, body, and tags columns equally by default.
Learnings with precise tags (e.g. `prompt_builder.py, build_feature_prompt`) should rank
higher for queries containing those exact tokens than entries where the same tokens appear
buried in body text. Without column weight tuning, retrieval precision suffers.

## Solution

Add to `py/auto_sdd/lib/knowledge_store.py` and `py/auto_sdd/lib/knowledge_backtest.py`:

1. **`COLUMN_WEIGHTS` module-level dict** in `knowledge_store.py`:
   - Default: `{"title": 2.0, "body": 1.0, "tags": 3.0}`
   - These map to the FTS5 `bm25()` function column weight arguments
   - `query_relevant()` passes weights to `bm25(entries_fts, {title_w}, {body_w}, {tags_w})`

2. **`set_column_weights(title, body, tags) -> None`** in `knowledge_store.py`:
   - Updates `COLUMN_WEIGHTS` at module level
   - Takes effect on next `query_relevant()` call

3. **`tune_weights(project_dir, eval_dir, specs_dir, learnings_dir) -> dict`**
   in `knowledge_backtest.py`:
   - Tries a grid of weight combinations:
     - title: [1.0, 2.0, 3.0]
     - body: [0.5, 1.0, 2.0]
     - tags: [2.0, 3.0, 5.0]
   - For each combination, sets weights via `set_column_weights()`, runs `run_backtest()`,
     records mean F1
   - Returns `{"best_weights": {...}, "best_f1": float, "grid_results": [...]}`

4. **`retune_weights(project_dir, eval_dir, specs_dir, learnings_dir, threshold) -> bool`**
   in `knowledge_backtest.py`:
   - Runs `tune_weights()`, compares best F1 to `threshold`
   - If best F1 >= threshold: sets column weights to best, returns True
   - If best F1 < threshold: logs warning, keeps current weights, returns False

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/lib/knowledge_store.py` | Add COLUMN_WEIGHTS, set_column_weights, update query_relevant |
| `py/auto_sdd/lib/knowledge_backtest.py` | Add tune_weights, retune_weights |

## Testing

- `set_column_weights()` changes the weights used by `query_relevant()`
- Different weights produce different ranking orders for the same query
- `tune_weights()` returns a dict with best_weights and best_f1
- `tune_weights()` grid search produces at least len(title) * len(body) * len(tags) results
- `retune_weights()` returns True when best F1 exceeds threshold
- `retune_weights()` returns False when best F1 is below threshold

## Constraints

- Grid search must complete in < 30 seconds against a populated store (100-300 entries)
- FTS5 `bm25()` accepts column weights as positional args after the table name
- Module-level weights are acceptable — no need for per-connection configuration
- No external deps
