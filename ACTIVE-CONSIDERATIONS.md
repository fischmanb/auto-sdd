# Active Considerations

> What's next and what's in-flight. Priority stack is the execution plan; everything below it is context a fresh chat should pick up.
>
> Split from ONBOARDING.md (2026-03-01) to keep onboarding focused on orientation.

---

### Priority stack (updated 2026-03-05, afternoon)

Ordered by efficiency gain per complexity added:

1. **Auto-QA validation against CRE lease tracker — first full run complete, fixes applied, ready for re-run.**
   - Plan: `WIP/auto-qa-cre-validation.md` (4 rounds, updated with run results + post-run fixes)
   - **First full run (val-20260305-223636)**: 31 min, $5.61. 14/25 pass, 3 fail, 8 blocked. All 4 fix agents failed (root-only build gate). Details in WIP.
   - **Post-run fixes applied**: Phase 5 monorepo build gates, infra failure skip in Phase 5, credential persistence (`--teardown` explicit), configurable `AGENT_TIMEOUT` (600s), Phase 0 monorepo fallback for root package.json without build script, CRE .gitignore for agent artifacts.
   - **QA credentials restored** in CRE (`qa-test@test.local`).
   - **Next action**: Re-run full pipeline to validate fixes. Expect: fix agents succeed for RC-002/003/004, RC-001 (infra) skipped.
   - **Open**: Phase 1 may have browsed API health URL instead of client URL. 8 BLOCKED from parse error may recur.
2. **Campaign intelligence system — design complete, implementation blocked on #1.**
   - Full plan: `WIP/campaign-intelligence-system.md` (pressure-tested, revised)
   - CIS value depends on auto-QA producing validated runtime signals. Build-only CIS is just a fancier eval sidecar.
   - 3 Phase 1 rounds: (1) vector store + wire writers, (2) analysis framework + intra-campaign injection, (3) convention eval signals
   - Phase 2 (after real campaign): auto-QA feature attribution, cross-campaign ML model
   - Phase 3 (after 3+ campaigns): meta-learner
3. **Investigate Playwright validation granularity — COMPLETED, findings inform Round 4 if needed.**
   - Investigation complete (agent prompt #2). Rating: DEGRADED — 60-70% of failure modes covered.
   - Cheap fixes already landed: networkidle waits, multi-step interaction patterns, retry parity.
   - Heavier improvements (visual regression, console monitoring, screenshot-on-every-assertion) deferred to Round 4 of `WIP/auto-qa-cre-validation.md`, triggered only if CRE full-pipeline run exposes gaps.
4. **Seed data & distribution strategy — V1 plan: ship curated seed packs.**
   - Full plan: `WIP/seed-data-distribution.md`
   - New users cold-start with zero campaign data; seed packs provide immediate value from Brian's campaigns
   - V1: `seed-data/` directory with curated vectors, patterns, model weights. V2: tiered community packs. V3: global sync (if adoption warrants).
   - **Blocked on**: stable vector schema from CIS Round 1. Schema is the interface contract for all distribution strategies.
5. **Integration test of Python build pipeline against real project** — may combine with #1 (run campaign then auto-QA in sequence).
6. **Extract `errors.py`/`signals.py`/`state.py` from `reliability.py` monolith** — Conventions specify these modules but Phase 1 inlined them. Low urgency.
7. **Local model integration** — Replace cloud API with local LM Studio on Mac Studio. Reference: `archive/local-llm-pipeline/`. *Not started.*
8. **Adaptive routing / parallelism** — Only if data from campaigns justifies complexity. *Deprioritized.*

### Other active items

- **HOW-I-WORK corpus curation**: 84+ entries (M-00001–M-00084+). 4+ coherent clusters ready for formalization. Action: curate entries into named sections, promote mature patterns to learnings.
- **Core learnings demotion review**: core.md at 17 entries (threshold 15). L-00012 (client→server import chain) is stakd/Next.js-specific — candidate for demotion. Review after next campaign.
- **Learnings graph-schema conversion**: Schema standardization complete. Some old-format entries may remain in `.specs/learnings/` files. Two agent prompts ready (Prompts 4 & 5) for converting those.
- **Memory slot optimization**: 15/30 slots, ~1,500 words always-injected. Not urgent but monitor. (L-00095)

### Completed (archive — remove when no longer useful for context)

- **stakd 28-feature campaign**: v2 COMPLETE (28/28 Sonnet 4.6, post-build import error known), v3 STALLED at 11/28 Haiku 4.5. Key finding: token speed ≠ build speed (infra bottlenecks dominate). Data in `campaign-results/`.
- **Bash→Python conversion**: ALL PHASES COMPLETE (0-6). Post-conversion audit complete (30 findings, 16 resolved, 7 INFO-only). 740 tests, 15.86s.
- **auto-QA pipeline**: ALL PHASES COMPLETE (0-5). 96 tests. Next: live validation run against real project.
- **Learnings system**: IMPLEMENTED. 191+ entries (L-00001–L-00191, M-00001–M-00087+), 17 curated in core.md.
- **Test suite reliability (2026-03-04)**: Orphan cleanup, hang fixes (generate_codebase_summary mock), build_loop 162s→0.1s. 740 tests, 15.86s, zero hangs.
- **L-00178 enforcement (2026-03-04)**: 300-line prompt rule across 5 surfaces (tests, runtime, CLAUDE.md, core.md, process-rules).
- **Next.js detection fix (2026-03-04)**: `detect_build_check()` priority ordering + package.json validation.
- **Hard constraints fixes (2026-03-03)**: run_claude() cwd, retry model chain, AGENT_TIMEOUT configurable.
- **Project-agnostic audit (2026-03-03)**: 3 remediation rounds (47-49). Agent-based summary, multilang eval, infra portability.
- **Campaign intelligence system design (2026-03-04)**: Full plan pressure-tested and committed. Sectioned vector store, pluggable analysis rules (feature-flagged), mechanical detection, project-configurable quality dimensions, auto-QA integration path. `WIP/campaign-intelligence-system.md`.
