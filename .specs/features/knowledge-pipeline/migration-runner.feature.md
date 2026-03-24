# Feature Spec: migration-runner

## Problem

Three separate migration modules exist (learnings, evals, pending) but no unified
entry point chains them, reports results, or handles the full migration lifecycle.

## Solution

Create `py/auto_sdd/scripts/migrate_knowledge.py`:

1. **CLI entry point** — callable as `python -m auto_sdd.scripts.migrate_knowledge`
2. **Arguments:**
   - `--project-dir` (required) — target project directory
   - `--learnings-dir` (default: `learnings/` relative to repo root)
   - `--db-path` (default: `{project_dir}/.sdd-state/knowledge.db`)
   - `--dry-run` — parse and count but do not insert
3. **Execution flow:**
   - Init store at db_path
   - Run `migrate_learnings(conn, learnings_dir)` then log count
   - Run `migrate_evals(conn, eval_dir)` then log count
   - Run `migrate_pending(conn, project_dir)` then log count
   - Log total summary
   - Close store
4. **`run_migration(project_dir, learnings_dir, db_path, dry_run) -> dict`**
   Returns `{"learnings": N, "evals": M, "pending": P, "total": T}`

## Files to Create

| File | Purpose |
|------|---------|
| `py/auto_sdd/scripts/migrate_knowledge.py` | Unified migration CLI + function |

## Testing

- `run_migration` with real learnings dir returns count > 0
- `dry_run=True` leaves DB empty
- Idempotent: second run returns zeros
- CLI `--help` runs without error
- Total equals sum of individual counts

## Constraints

- Must work against real `learnings/` directory
- Logging via `logging` module
- Exit code 0 on success, 1 on failure
