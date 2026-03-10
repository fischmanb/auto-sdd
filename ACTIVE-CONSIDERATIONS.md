# Active Considerations

> What's next and what's in-flight. Priority stack is the execution plan; everything below it is context a fresh chat should pick up.
>
> Split from ONBOARDING.md (2026-03-01) to keep onboarding focused on orientation.

---

### Priority stack (updated 2026-03-10 — post session 3)

Ordered by efficiency gain per complexity added:

1. **Knowledge pipeline — 18 features spec'd, branch ready for build loop**
   - Branch: `knowledge-pipeline-specs` (2 commits ahead of main at `245eb59`).
   - 18 feature specs in `.specs/features/knowledge-pipeline/`, roadmap in `.specs/roadmap.md`.
   - `project.yaml` + CLAUDE.md Python section committed.
   - Run: `MAX_FEATURES=3 PROJECT_DIR=~/auto-sdd` on `knowledge-pipeline-specs` branch.
   - Phases: Store (1-3) → Migration (4-7) → Wire Writes (8-11) → Wire Reads (12-13) → Backtest (14-15) → Optimization (16-18).
2. **SitDeck build campaign — 37+/49 features built, auto-QA running.**
   - Auto-QA scale test in progress (PID 27468). Phase 3 Playwright validation: 25 features completed, 4 timeouts, 3 parse failures. Still running.
   - Pipeline: build_loop → post-campaign verify → auto-QA now fully wired (Round 39, 7f97dff).
   - **Resume command**: `caffeinate -diw $$ & cd ~/auto-sdd/py && AUTO_APPROVE=true PROJECT_DIR=~/compstak-sitdeck LOGS_DIR=~/auto-sdd/logs/compstak-sitdeck .venv/bin/python -m auto_sdd.scripts.build_loop`
3. **CIS Rounds 5-6 — need campaign data from #2.**
   - Campaign data exists (feature-vectors.jsonl in ~/compstak-sitdeck/.sdd-state/). May be unblocked.
   - Full plan: `WIP/campaign-intelligence-system.md`
4. **Seed data & distribution** — Blocked on stable vector schema.
5. **Extract errors.py/signals.py/state.py from reliability.py** — Low urgency.
6. **Local model integration — GPT-OSS target** — Best coding performance per GB active RAM. Move off cloud API entirely. Active priority on roadmap.
7. **Adaptive routing** — Deprioritized.

### Knowledge graph build intelligence — DESIGNED, NOT STARTED

- **WIP:** `WIP/knowledge-graph-build-intelligence.md` (207 lines)

### Other active items

- **Build launches are Brian-only**: Brian runs all builds in Terminal himself. Chat sessions provide run commands and pre-flight context but never launch build_loop.

- **auto-sdd vs superloop naming asymmetry**: Local dir is `~/auto-sdd`, GitHub repo is `fischmanb/superloop`. No functional impact, doc-layer confusion only. Deferred.
- **ONBOARDING.md reconciliation needed**: File is stale — describes pre-campaign, pre-isolation state. Needs full refresh to match current reality (project segregated, isolation enforcement, 1026 tests, L-00226/M-00095).
- **HOW-I-WORK corpus curation**: 84+ entries. 4+ clusters ready for formalization.
- **Memory slot optimization**: 15/30 slots. Not urgent. (L-00095)


- **docs/ directory restructure (2026-03-09)**: Single organized entry point at docs/README.md — system/, operations/, guides/, knowledge/, plans/, history/. 5 new files, 29 total. de0d5d7.
- **Superloop HTML deck on GitHub Pages**: Self-contained presentation at https://fischmanb.github.io/superloop/interactive/superloop-deck.html. Slide 3 is interactive 12-step closed loop stepper. Replaces PPTX. Source at docs/interactive/superloop-deck.html.
- **Test count trend gate (future)**: `--passWithNoTests` in vitest is correct for early features, but a gate that tracks test count trends and flags features that add code with zero corresponding tests would be a stronger signal than binary pass/fail. Low priority.
- **Round 38 merged (26a7b2f)**: Environment isolation (NODE_ENV=development forced in agent + gate subprocesses), dependency health gate (check_deps, Gate 1.75), post-campaign clean-room verification. 1045 tests all passing.
- **Auto-QA scale test running**: First run against compstak-sitdeck (37+ features). CRE lease tracker (3 features) validated the pipeline; this is the real scale proof. Run ID in logs/auto-qa-sitdeck-*.log.
- **Adaptive timeouts from token estimator (design)**: Hardcoded timeouts (600s build, 900s auto-QA) cause premature kills on large projects and waste time on small ones. The estimator already has agent token data in general-estimates.jsonl. Timeout should be `f(estimated_tokens, historical_tokens_per_second, buffer_multiplier)` — not arbitrary. Applies to build loop agents AND auto-QA agents. Phase 3 Playwright agents are especially variable (5 min for simple features, 15+ min for complex multi-widget features). The token estimation calibration system (estimated vs actual JSONL) provides the training data. Implementation: compute rolling median tokens/sec from last N runs, multiply by estimated tokens for the task, add 2x safety buffer, floor at 120s, cap at 3600s.

### Completed (archive — remove when no longer useful for context)

- **Two-stage retry system (2026-03-09)**: Fix-in-place (attempt 1) before informed fresh retry (attempt 2+). Live-validated on Feature #19. 8533639.
- **Codebase summary timeout fix (2026-03-09)**: Excluded SDD metadata from file tree, timeout bumped to 300s (SUMMARY_TIMEOUT env var). 63edac4.

- **Integration pipeline test (2026-03-09)**: 8 tests covering full build loop with isolation layers — single-feature build, prompt boundary, chmod protection/restore, root file protection, contamination check clean/dirty, config loading, log derivation. 1026 total tests.
- **Credit exhaustion test fix (2026-03-09)**: Two tests broken by prior refactor (31ef249) — mocks returned output text instead of raising CreditExhaustionError. Fixed.
- **Repo triage complete (2026-03-09)**: logs/ gitignored (23 tracked files untracked), 45 orphan branches deleted in auto-sdd, working tree clean.
- **Project isolation enforcement (2026-03-09)**: Three-layer protection. Contract: `WIP/project-isolation-contract.md`. 92 build_loop tests.
- **Project directory segregation (2026-03-09)**: compstak-sitdeck at `~/compstak-sitdeck/`. Nested dir issue found and flattened. project.yaml recovered and committed to project git.
- **SitDeck campaign (2026-03-08)**: 36/49 features built, merged to main, orphan branches deleted. $201 cost.
- **Learnings system**: L-00001–L-00226, M-00001–M-00095, 17 curated in core.md.
