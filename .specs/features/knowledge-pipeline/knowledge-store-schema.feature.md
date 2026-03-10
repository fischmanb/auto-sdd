# Feature Spec: knowledge-store-schema

## Problem

The knowledge pipeline has no persistent store. Learnings, eval results, and mistake patterns live in
scattered markdown files and JSON blobs. Five data flow connections are broken because there is no
queryable substrate.

## Solution

Create `py/auto_sdd/lib/knowledge_store.py` with:

1. **SQLite + FTS5 schema** — single `knowledge.db` file at `{project_dir}/.sdd-state/knowledge.db`
2. **Tables:**
   - `entries` — id TEXT PRIMARY KEY, entry_type TEXT, source TEXT, title TEXT, body TEXT,
     tags TEXT, confidence TEXT, status TEXT, created_at TEXT, updated_at TEXT
   - `entries_fts` — FTS5 virtual table on (title, body, tags) for full-text search
   - `relationships` — source_id TEXT, target_id TEXT, edge_type TEXT, PRIMARY KEY (source_id, target_id)
3. **Functions:**
   - `init_store(db_path: Path) -> sqlite3.Connection` — create tables if not exist, enable WAL mode
   - `close_store(conn: sqlite3.Connection) -> None`
   - `insert_entry(conn, id, entry_type, source, title, body, tags, confidence, status) -> None` — upsert
   - `get_entry(conn, id) -> dict | None`
   - `count_entries(conn) -> int`
   - `count_by_type(conn, entry_type) -> int`

## Files to Create

| File | Purpose |
|------|---------|
| `py/auto_sdd/lib/knowledge_store.py` | Store module with schema + CRUD |

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/lib/__init__.py` | Ensure importable (create if missing) |

## Testing

- `init_store` creates tables successfully on a temp db
- `insert_entry` + `get_entry` round-trips correctly
- `insert_entry` with same ID updates (upsert behavior)
- `count_entries` and `count_by_type` return correct numbers
- FTS5 virtual table is created (verify with `PRAGMA table_info`)
- WAL mode is enabled

## Constraints

- No external dependencies — stdlib `sqlite3` only
- All functions must have full type annotations
- `mypy --strict` must pass
- DB path is configurable, not hardcoded
