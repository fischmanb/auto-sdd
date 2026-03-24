# Feature Spec: migrate-markdown-learnings

## Problem

300+ learnings entries (L-00001–L-00226, M-00001–M-00095) live in markdown files under
`learnings/`. Each entry follows a graph-schema format with `## ID — Title`, metadata
fields (Type, Confidence, Status, Tags, Related), and a prose body. These must be parsed
and inserted into the knowledge store.

## Solution

Create `py/auto_sdd/lib/migrations/migrate_learnings.py`:

1. **`parse_learning_entry(text_block: str) -> dict`** — parse one `## L-NNNNN` or `## M-NNNNN` block:
   - Extract ID from header (`## L-00042 — Title here`)
   - Extract title from header (after ` — `)
   - Extract metadata: `Type:`, `Confidence:`, `Status:`, `Tags:`, `Related:`
   - Body = everything after metadata, before next `## ` header
   - Return dict with keys: id, title, entry_type, confidence, status, tags, related, body

2. **`parse_learnings_file(file_path: Path) -> list[dict]`** — split file by `## [LM]-` headers, parse each

3. **`migrate_learnings(conn, learnings_dir: Path) -> int`** — walk all `.md` files in dir,
   parse entries, insert into store. Return count of entries migrated. Skip entries already
   in store (idempotent). Also insert `relationships` rows from `Related:` fields.

## Files to Create

| File | Purpose |
|------|---------|
| `py/auto_sdd/lib/migrations/__init__.py` | Package init |
| `py/auto_sdd/lib/migrations/migrate_learnings.py` | Markdown learnings parser + migrator |

## Testing

- Parse a single well-formed entry → correct fields extracted
- Parse entry with missing optional fields (no Related:) → no crash
- Parse a file with 3 entries → returns 3 dicts
- `migrate_learnings` against real `learnings/` dir → count > 0
- Idempotent: running twice doesn't duplicate entries
- Relationships are inserted for entries with `Related:` fields
- `entry_type` is set to `"learning"` for all entries

## Constraints

- Parser must handle both `L-NNNNN` and `M-NNNNN` ID formats
- Tags field is stored as comma-separated string (matches FTS5 expectations)
- Source field = relative path of the markdown file
