# Feature Spec: wire-writes-auto-qa

## Problem

`post_campaign_validation.py` runs multi-phase QA (discovery, acceptance criteria, Playwright validation,
failure catalog, RCA, fix agents) but none of the findings, RCA entries, or fix outcomes are written
to the knowledge store. Auto-QA findings are dead data — they exist only in phase output files that
nothing downstream reads.

## Solution

Modify `py/auto_sdd/scripts/post_campaign_validation.py`:

1. **At pipeline init**: open a store connection via `init_store(db_path)` where
   `db_path = project_dir / ".sdd-state" / "knowledge.db"`
2. **After Phase 4a (failure catalog)**: for each failure entry, call `insert_entry()`:
   - ID: `QA-FAIL-{feature_name}-{hash(failure_summary)[:8]}`
   - entry_type: `"qa_failure"`
   - title: `"QA failure: {feature} — {failure_type}"`
   - tags: comma-join of feature name, phase, failure type
   - body: failure details (symptom, expected, actual)
   - confidence: `"high"`
   - source: relative path to phase 4a output
3. **After Phase 4b (RCA)**: for each root cause entry, call `insert_entry()`:
   - ID: `QA-RCA-{feature_name}-{hash(root_cause)[:8]}`
   - entry_type: `"qa_rca"`
   - title: `"RCA: {feature} — {root_cause_summary}"`
   - tags: comma-join of feature name, root cause category, affected files
   - body: root cause analysis text
   - confidence: `"medium"` (agent-generated)
   - source: relative path to phase 4b output
4. **After Phase 5 (fix agents)**: for each fix outcome, call `insert_entry()`:
   - ID: `QA-FIX-{feature_name}-{hash(fix_summary)[:8]}`
   - entry_type: `"qa_fix"`
   - title: `"Fix: {feature} — {fix_summary}"`
   - tags: comma-join of feature name, fix type, pass/fail
   - body: what was changed and whether it passed re-validation
   - confidence: `"high"` (mechanically verified)
   - source: relative path to phase 5 output
5. **At pipeline shutdown**: `close_store(conn)`
6. **Graceful degradation**: if store init fails, log warning and continue.

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/scripts/post_campaign_validation.py` | Add store init/write/close around QA lifecycle |

## Testing

- Pipeline writes store entries for Phase 4a failures (verify entry exists with correct type)
- Pipeline writes store entries for Phase 4b RCA (verify entry exists)
- Pipeline writes store entries for Phase 5 fixes (verify entry exists)
- Store failure does not crash pipeline (graceful degradation)
- Entry IDs are deterministic (same failure → same ID → upsert, not duplicate)

## Constraints

- Store writes must not slow down phase execution
- Existing phase output files are preserved unchanged
- Import `knowledge_store` only — no other new deps
- Hash-based IDs ensure idempotency on re-runs
