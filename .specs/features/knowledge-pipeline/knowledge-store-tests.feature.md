# Feature Spec: knowledge-store-tests

## Problem

Features #1 and #2 created the store module with basic tests alongside. This feature
adds comprehensive edge-case and integration tests to harden the store before wiring
it into the build pipeline.

## Solution

Create `py/tests/test_knowledge_store.py` with comprehensive pytest coverage:

1. **Schema tests** — verify table creation, FTS5 table exists, WAL mode, idempotent re-init
2. **CRUD tests** — insert, get, upsert (update-on-conflict), get nonexistent returns None
3. **Query tests:**
   - FTS5 matches on title, body, and tags independently
   - BM25 ranking: entry with term in title ranks higher than term in body only
   - Multiple matches ranked correctly
   - `top_k` truncation
   - `entry_types` filtering
   - Query with no matches returns empty list
   - Query with FTS5 special chars doesn't crash (sanitization)
4. **Relationship tests** — insert relationship, query by source/target
5. **Concurrency** — two connections to same DB don't corrupt (WAL)
6. **Format tests** — `format_knowledge_section` output structure, max_lines cap, empty input

## Files to Create

| File | Purpose |
|------|---------|
| `py/tests/test_knowledge_store.py` | Comprehensive test suite |

## Testing

This IS the test feature. Target: 25+ test functions. All must pass with:
```
cd py && .venv/bin/pytest tests/test_knowledge_store.py -v
```

## Constraints

- Use `tmp_path` fixture for temp DB files (no test pollution)
- No mocking of sqlite3 — test against real SQLite
- Each test function is independent (own DB instance)
