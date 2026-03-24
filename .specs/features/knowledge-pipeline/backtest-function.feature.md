# Feature Spec: backtest-function

## Problem

The knowledge pipeline has no way to measure whether `query_relevant()` returns useful results.
Without a backtest, FTS5 weights and query construction are tuned by intuition, not data. The
eval JSONs from the SitDeck campaign contain ground truth — each eval documents what signals
were found for a specific feature. If `query_relevant()` for that feature returns learnings
that match those signals, retrieval is working. If not, it's returning noise.

## Solution

Create `py/auto_sdd/lib/knowledge_backtest.py`:

1. **`BacktestResult` dataclass**:
   - feature_name: str
   - query_text: str
   - returned_ids: list[str]
   - relevant_ids: list[str] (ground truth from eval)
   - precision: float
   - recall: float

2. **`load_eval_ground_truth(eval_dir: Path) -> dict[str, list[str]]`**:
   - Reads all `eval-*.json` files in eval_dir
   - For each eval, extracts feature name and the non-passing signal IDs/types
   - Returns `{feature_name: [relevant_learning_ids]}` mapping
   - Matching logic: eval signals → learning tags overlap (exact match on tag tokens)

3. **`backtest_feature(conn, feature_name, spec_text, ground_truth_ids, top_k=10) -> BacktestResult`**:
   - Calls `query_relevant(conn, feature_name + " " + spec_text, top_k=top_k)`
   - Computes precision = |returned ∩ relevant| / |returned|
   - Computes recall = |returned ∩ relevant| / |relevant|
   - Returns `BacktestResult`

4. **`run_backtest(project_dir, learnings_dir, eval_dir, specs_dir) -> list[BacktestResult]`**:
   - Loads ground truth from eval_dir
   - For each feature with ground truth, reads its spec file from specs_dir
   - Calls `backtest_feature()` for each
   - Returns list of all results

5. **`summarize_backtest(results: list[BacktestResult]) -> str`**:
   - Computes mean precision, mean recall, F1
   - Per-feature breakdown
   - Returns formatted string for commit message or logging

## Files to Create

| File | Purpose |
|------|---------|
| `py/auto_sdd/lib/knowledge_backtest.py` | Backtest functions for retrieval quality measurement |

## Testing

- `load_eval_ground_truth()` with real eval JSONs returns non-empty dict
- `backtest_feature()` returns valid precision/recall (0.0-1.0 range)
- `backtest_feature()` with perfect overlap returns precision=1.0, recall=1.0
- `backtest_feature()` with zero overlap returns precision=0.0, recall=0.0
- `run_backtest()` returns one result per feature with ground truth
- `summarize_backtest()` produces readable output with mean metrics

## Constraints

- Operates against REAL data — no mocks of the store or eval files
- Must work with the actual `knowledge.db` populated by the migration (feature #7)
- Precision and recall formulas must handle zero denominators (return 0.0, not ZeroDivisionError)
- No external deps — stdlib + knowledge_store only
