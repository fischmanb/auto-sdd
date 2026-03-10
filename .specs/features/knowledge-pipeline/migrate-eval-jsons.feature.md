# Feature Spec: migrate-eval-jsons

## Problem

113+ eval JSON files in project eval output dirs contain structured evaluation data
(framework compliance, scope assessment, integration quality, repeated mistakes, eval notes).
The eval sidecar currently reads only the latest 1 of these files. All historical evals
must be queryable.

## Solution

Create `py/auto_sdd/lib/migrations/migrate_evals.py`:

1. **`parse_eval_json(file_path: Path) -> dict`** — read one eval JSON file, extract:
   - Generate synthetic ID: `EVAL-{feature_name}-{timestamp}` from filename/content
   - `entry_type`: `"eval_finding"`
   - `title`: `"Eval: {feature_name} — {framework_compliance}/{scope_assessment}"`
   - `tags`: comma-joined from framework_compliance, scope_assessment, integration_quality,
     repeated_mistakes values
   - `body`: JSON-formatted summary of all eval fields
   - `confidence`: `"high"` (mechanical eval data)
   - `source`: relative path to eval JSON file

2. **`migrate_evals(conn, eval_dir: Path) -> int`** — walk all `eval-*.json` files
   (excluding `eval-campaign-*.json`), parse each, insert into store. Return count.
   Skip files already migrated (idempotent via synthetic ID).

## Files to Create

| File | Purpose |
|------|---------|
| `py/auto_sdd/lib/migrations/migrate_evals.py` | Eval JSON parser + migrator |

## Testing

- Parse a well-formed eval JSON → correct fields
- Parse eval with missing optional fields → no crash, sensible defaults
- `migrate_evals` with a temp dir containing 3 mock eval JSONs → returns 3
- Idempotent: running twice returns 0 on second run
- `eval-campaign-*.json` files are excluded

## Constraints

- Eval JSON schema varies slightly across versions — parser must be lenient
- Synthetic IDs must be deterministic (same file → same ID) for idempotency
- No external deps beyond stdlib `json`
