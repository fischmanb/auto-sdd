# Feature Spec: knowledge-store-query

## Problem

The store from feature #1 can insert and get by ID, but the knowledge pipeline needs
relevance-ranked retrieval: given a feature name + spec text, return the most relevant
learnings, eval findings, and mistake patterns.

## Solution

Add to `py/auto_sdd/lib/knowledge_store.py`:

1. **`QueryResult` dataclass** — id, entry_type, title, body, tags, rank (BM25 score)
2. **`query_relevant(conn, query_text, *, top_k=10, entry_types=None) -> list[QueryResult]`**
   - Runs FTS5 MATCH against `entries_fts` using `query_text`
   - Orders by `bm25(entries_fts)` (lower = more relevant in SQLite FTS5)
   - Filters by `entry_types` if provided (e.g. `["learning", "eval_finding"]`)
   - Returns top K results as `QueryResult` objects
3. **`format_knowledge_section(results: list[QueryResult], max_lines: int = 80) -> str`**
   - Formats results into a prompt-injectable section
   - Each entry: `### {id} — {title}\n{body (truncated)}\nTags: {tags}`
   - Respects `max_lines` budget — stops adding entries when exceeded

## Files to Modify

| File | Change |
|------|--------|
| `py/auto_sdd/lib/knowledge_store.py` | Add QueryResult, query_relevant, format_knowledge_section |

## Testing

- Insert 5 entries with distinct tags/titles, query for a term in one → that entry ranks first
- `top_k=2` returns exactly 2 results
- `entry_types` filter excludes non-matching types
- Empty query returns empty list (no crash)
- `format_knowledge_section` respects `max_lines` cap
- `format_knowledge_section` with empty list returns empty string

## Constraints

- FTS5 `bm25()` function — do NOT use `rank` column (it's an alias; explicit bm25() is portable)
- Query text is sanitized: strip FTS5 operators (`AND`, `OR`, `NOT`, `*`, `"`) from user input
- No external deps
