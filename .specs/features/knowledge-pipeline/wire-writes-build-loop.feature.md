# Feature Spec: wire-writes-build-loop

## Problem

`build_loop.py` produces feature outcomes (success/failure, gate results, retry counts,
timing data) that are logged but not persisted to the knowledge store.

## Solution

Modify `py/auto_sdd/scripts/build_loop.py`:

1. **At BuildLoop init**: open store connection
2. **After each feature completes (success or failure)**: insert an entry:
   - ID: `BUILD-{feature_name}-{timestamp}`
   - entry_type: `"build_outcome"`
   - title: `"Build: {feature} — {success|failed} (attempt {N})"`
   - tags: comma-join of gate names that passed/failed, model used
   - body: structured summary — gate results, retry count, timing, error excerpts
   - confidence: `"high"`
   - source: `"build_loop"`
3. **At BuildLoop shutdown**: close store
4. **Graceful degradation**: store failure logs warning, does not halt build

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/scripts/build_loop.py` | Add store lifecycle + per-feature inserts |

## Testing

- Build outcome is inserted after feature success
- Build outcome is inserted after feature failure (with error data)
- Store failure does not crash build loop
- Entry contains correct gate pass/fail data
- Existing build loop behavior is unchanged (no functional regression)

## Constraints

- Store write happens AFTER feature commit, not before
- Keep insert payload under 4KB (truncate error output)
- No changes to build loop control flow — writes are additive side effects
