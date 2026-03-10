# Feature Spec: periodic-retune-trigger

## Problem

Column weights for FTS5 retrieval are set once during the initial tune (feature #15) and
never revisited. As new learnings accumulate and the knowledge distribution shifts, retrieval
quality can degrade without anyone noticing. The retrieval log enriched with scores
(feature #17) contains the data needed to detect degradation — but nothing reads it.

## Solution

Modify `py/auto_sdd/scripts/build_loop.py`:

1. **Add `check_retrieval_health(project_dir, window=20, threshold=0.5) -> bool`**:
   - Reads `{project_dir}/.sdd-state/retrieval-log.jsonl`
   - Filters to entries that have `precision` and `recall` fields (scored entries)
   - Takes the last `window` scored entries
   - Computes rolling mean precision and rolling mean recall
   - If either drops below `threshold`: returns False (degraded)
   - Otherwise returns True (healthy)
   - Returns True if fewer than `window` scored entries exist (not enough data)

2. **Add `maybe_retune(project_dir, eval_dir, specs_dir, learnings_dir, threshold) -> None`**:
   - Calls `check_retrieval_health(project_dir, threshold=threshold)`
   - If healthy: log "Retrieval health OK" and return
   - If degraded: call `retune_weights()` from `knowledge_backtest.py` (feature #15)
   - Log whether retune improved F1 above threshold

3. **In `BuildLoop.run()`**: at the **post-campaign** phase (after all features are
   built, before auto-QA), call `maybe_retune()`. This is a natural checkpoint where
   retrieval data from the just-completed campaign is available.
   - Guarded by `SKIP_RETUNE` env var (default: run)
   - Also guarded by store existence check

4. **Environment config**:
   - `RETUNE_THRESHOLD` (default: `0.5`) — minimum acceptable mean precision/recall
   - `RETUNE_WINDOW` (default: `20`) — number of recent scored entries to evaluate
   - `SKIP_RETUNE` (default: unset) — skip retune step entirely

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/scripts/build_loop.py` | Add check_retrieval_health, maybe_retune, wire into post-campaign |

## Testing

- `check_retrieval_health()` returns True when all scores are above threshold
- `check_retrieval_health()` returns False when scores drop below threshold
- `check_retrieval_health()` returns True when fewer than `window` entries exist
- `check_retrieval_health()` handles missing retrieval log gracefully (returns True)
- `maybe_retune()` calls `retune_weights()` only when health check fails
- `maybe_retune()` does not call `retune_weights()` when health check passes
- `SKIP_RETUNE=1` skips the entire retune step

## Constraints

- Retune is non-blocking — failure to retune does not fail the build loop
- Rolling window computation uses only stdlib (no numpy/pandas)
- `check_retrieval_health` must complete in < 1 second
- `maybe_retune` may take up to 30 seconds (grid search)
- Logged via standard `logging` module
