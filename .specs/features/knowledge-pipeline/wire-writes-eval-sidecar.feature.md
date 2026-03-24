# Feature Spec: wire-writes-eval-sidecar

## Problem

`eval_sidecar.py` writes eval JSON files but does not insert findings into the knowledge store.
Eval data is write-only to disk with no queryable path.

## Solution

Modify `py/auto_sdd/scripts/eval_sidecar.py`:

1. **At sidecar init**: open a store connection via `init_store(db_path)` where
   `db_path = project_dir / ".sdd-state" / "knowledge.db"`
2. **After each eval JSON is written**: call `insert_entry()` with the eval data.
   - ID: `EVAL-{feature_name}-{timestamp}` (same scheme as migrate_evals)
   - entry_type: `"eval_finding"`
   - title: `"Eval: {feature} — {compliance}/{scope}"`
   - tags: comma-join of eval signal values
   - body: JSON summary of eval fields
   - confidence: `"high"`
   - source: relative path to eval JSON
3. **At sidecar shutdown**: `close_store(conn)`
4. **Graceful degradation**: if store init fails (e.g. locked), log warning and continue
   without store writes. Eval JSON files are still written — store is additive.

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/scripts/eval_sidecar.py` | Add store init/write/close around eval lifecycle |

## Testing

- Sidecar writes eval JSON AND store entry (verify both exist)
- Store entry has correct ID format and fields
- Store failure does not crash sidecar (graceful degradation)
- Sidecar without existing DB creates it

## Constraints

- Store writes must not slow down sidecar eval cycle
- Existing eval JSON file writes are preserved unchanged
- Import `knowledge_store` only — no other new deps
