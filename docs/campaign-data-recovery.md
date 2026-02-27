 "Terminal" to return history of tab 1 of window id WINID' > recovered.txt
   ```
   Match tty to window: iterate windows with `get tty of tab 1 of window id X`
3. If tee is dead → data is gone. Git history has timing data as fallback.

### If cost logs are missing
1. Check `$LOGS_DIR/cost-log.jsonl` (new location)
2. Legacy: check `$PROJECT_DIR/cost-log.jsonl` (old default from claude-wrapper.sh cwd)
3. Fallback: API usage dashboard at console.anthropic.com

### If eval files are missing
1. Check `$LOGS_DIR/evals/` (new location)
2. Legacy: check `$PROJECT_DIR/logs/evals/`
3. Fallback: git log for `state: checkpoint` commits (evals trigger on checkpoint)

## Prevention Rules

1. **Never store campaign artifacts inside a git working tree.** Use `$LOGS_DIR`.
2. **Export `COST_LOG_FILE` explicitly.** Don't rely on cwd default.
3. **`git clean -fd -e logs`** is insufficient — the exclusion fails on edge cases. Move logs out entirely.
4. **Terminal.app `history` ≠ `contents`.** `contents` = visible area. `history` = full scrollback.
5. **Campaign-results go in main repo** (`~/auto-sdd/campaign-results/`), not project repos.
