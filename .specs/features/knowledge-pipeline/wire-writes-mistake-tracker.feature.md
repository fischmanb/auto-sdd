# Feature Spec: wire-writes-mistake-tracker

## Problem

`MistakeTracker` in `drift.py` accumulates repeated mistake patterns in memory but is
volatile — patterns are lost when the process exits. The tracker must persist to the
knowledge store so patterns survive across campaigns.

## Solution

Modify `py/auto_sdd/lib/drift.py` — specifically the `MistakeTracker` class:

1. **`MistakeTracker.__init__`**: accept optional `db_path: Path | None`. If provided,
   open store connection and load existing mistake entries from store.
2. **`MistakeTracker.track(pattern: str, feature: str)`**: after updating in-memory dict,
   also upsert to store:
   - ID: `MISTAKE-{hash(pattern)}`
   - entry_type: `"mistake_pattern"`
   - title: `"Repeated mistake: {pattern}"`
   - tags: features where pattern was seen (comma-joined)
   - body: occurrence count, first/last seen timestamps
   - confidence: increases with occurrence count (1=low, 2=medium, 3+=high)
3. **`MistakeTracker.load()`**: read all `mistake_pattern` entries from store into memory
4. **`MistakeTracker.save()`**: bulk upsert all in-memory patterns to store
5. **Graceful degradation**: if no db_path or store fails, tracker works as before (memory-only)

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/lib/drift.py` | Add persistence to MistakeTracker |

## Testing

- Track a pattern, create new tracker with same db_path, pattern is loaded
- Track same pattern 3 times, confidence is `"high"`
- Memory-only mode (no db_path) works exactly as before
- Store failure does not crash tracker
- `save()` then `load()` round-trips all patterns

## Constraints

- Backward compatible — callers that don't pass db_path get identical behavior
- Pattern hash must be deterministic
