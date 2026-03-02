---
feature: Auth and dashboard shell
domain: auth-dashboard
source: py/auto_sdd/lib/config.py, py/auto_sdd/scripts/dashboard.py
tests:
  - py/tests/test_config.py
  - py/tests/test_dashboard.py
status: implemented
created: 2026-03-02
updated: 2026-03-02
---

# Auth and Dashboard Shell

**Source Files**:
- `py/auto_sdd/lib/config.py` — configuration and auth management
- `py/auto_sdd/scripts/dashboard.py` — CLI status dashboard

## Feature: Configuration and Auth Management

### Scenario: Load config from environment
Given a project directory with a `.env.local` file containing ANTHROPIC_API_KEY
When `resolve_config(project_dir)` is called
Then a `Config` dataclass is returned with the API key populated

### Scenario: Env file merged with process environment
Given a project directory with a `.env.local` containing FOO=bar
And FOO is not set in the process environment
When `resolve_config(project_dir)` is called
Then the config reflects FOO=bar from the env file

### Scenario: Process environment takes precedence over env file
Given ANTHROPIC_API_KEY is set in the process environment to "env-key"
And `.env.local` contains ANTHROPIC_API_KEY=file-key
When `resolve_config(project_dir)` is called
Then `config.anthropic_api_key` is "env-key" (process env wins)

### Scenario: Missing required key raises ConfigError
Given a project directory with no `.env.local`
And ANTHROPIC_API_KEY is not set in the process environment
When `resolve_config(project_dir)` is called
Then `ConfigError` is raised with a message identifying the missing variable

### Scenario: Missing env file is tolerated
Given a project directory with no `.env.local`
And ANTHROPIC_API_KEY is set in the process environment
When `resolve_config(project_dir)` is called
Then config loads successfully from the process environment

### Scenario: Malformed env file line is skipped
Given a `.env.local` containing a line with no `=` character
When `load_env_file(path)` is called
Then the malformed line is silently skipped and valid lines are returned

### Scenario: Comments and blank lines are ignored
Given a `.env.local` with `# comment` lines and blank lines
When `load_env_file(path)` is called
Then the returned dict contains no keys starting with `#` and no empty keys

## Feature: CLI Status Dashboard

### Scenario: Dashboard renders roadmap summary
Given a project directory with a `.specs/roadmap.md` containing real feature rows
When `render_dashboard(project_dir)` is called
Then the output contains counts for completed, in-progress, and pending features

### Scenario: Dashboard renders cost summary from JSONL log
Given a `general-estimates.jsonl` file with cost records that have `active_tokens` fields
When `render_dashboard(project_dir)` is called
Then the output shows the most recent cost entry's timestamp

### Scenario: Dashboard shows no costs when JSONL is absent
Given a project directory with no `general-estimates.jsonl` file
When `render_dashboard(project_dir)` is called
Then the output contains a "no cost data" message instead of raising

### Scenario: Dashboard shows lock status as idle when no lock file
Given no `build.lock` file in the project directory
When `render_dashboard(project_dir)` is called
Then the output contains "idle" for the build loop status

### Scenario: Dashboard CLI entrypoint exits 0
Given the dashboard script is invoked as `python -m auto_sdd.scripts.dashboard`
When the project directory is valid
Then the process exits with code 0

## UI Mockup (CLI output)

```
=== auto-sdd Dashboard ===
Project: /Users/brianfischman/auto-sdd

  Auth
  ANTHROPIC_API_KEY  ✓ set (48 chars)

  Roadmap
  ✅ Completed    1
  🔄 In Progress  0
  ⬜ Pending      0

  Build Loop
  Status: idle (no lock file)

  Recent Activity
  Last entry: 2026-03-02T05:00:58Z  bash-to-python-phase5-overnight
```

## Learnings

- Config resolution follows the same pattern as bash's `.env.local` sourcing: file values are loaded first, then process environment takes precedence.
- Dashboard reads files directly — no subprocess calls required.
