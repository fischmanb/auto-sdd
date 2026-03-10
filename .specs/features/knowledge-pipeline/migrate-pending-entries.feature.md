# Feature Spec: migrate-pending-entries

## Problem

`pending.md` (or similar pending capture files) contains entries that were flagged for
future processing but never ingested into a queryable store. These are write-only today.

## Solution

Create `py/auto_sdd/lib/migrations/migrate_pending.py`:

1. **`parse_pending_file(file_path: Path) -> list[dict]`** — parse pending entries.
   Format varies: may be bullet lists, may be `## ` headed blocks. Parser handles both:
   - Bullet items (`- ` or `* `) → each becomes an entry with synthetic ID `PENDING-{hash}`
   - Headed blocks (`## `) → parsed like learnings entries
   - `entry_type`: `"pending"`
   - `confidence`: `"low"` (unverified captures)
   - `tags`: extract any inline tags or keywords

2. **`migrate_pending(conn, project_dir: Path) -> int`** — find pending files
   (`pending.md`, `ACTIVE-CONSIDERATIONS.md` pending_captures if applicable),
   parse, insert. Return count. Idempotent.

## Files to Create

| File | Purpose |
|------|---------|
| `py/auto_sdd/lib/migrations/migrate_pending.py` | Pending entries parser + migrator |

## Testing

- Parse bullet-list format → correct entries
- Parse headed-block format → correct entries
- `migrate_pending` with mock file → returns expected count
- Idempotent: no duplicates on re-run
- Missing file → returns 0 (no crash)

## Constraints

- Synthetic IDs use content hash for dedup
- Small feature — keep parser simple, handle the two known formats
