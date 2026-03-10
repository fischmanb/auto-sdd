# Build Roadmap — Knowledge Pipeline

> Ordered list of features implementing the knowledge pipeline (SQLite + FTS5 store,
> migration, wire writes/reads, backtest, continuous optimization).
> Each feature is scoped for a single agent context window.

## Implementation Rules

**Every feature must include real tests, real data operations, and real integration.**

- **No stub functions** — every function must contain real logic.
- **No placeholder returns** — functions operate on actual SQLite, actual files, actual data.
- **Real tests** — pytest tests that exercise the actual code path. No mocks of the thing being tested.
- **Imports must resolve** — every import must point to an existing module. Check before committing.
- **Type annotations required** — all functions must have type hints. `mypy --strict` must pass.

---

## Progress

| Status | Count |
|--------|-------|
| ✅ Completed | 0 |
| 🔄 In Progress | 0 |
| ⬜ Pending | 18 |
| ⏸️ Blocked | 0 |

**Last updated**: 2026-03-10

---

## Phase 1: Store Foundation

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| 1 | knowledge-store-schema | knowledge-pipeline | - | M | - | ⬜ |
| 2 | knowledge-store-query | knowledge-pipeline | - | M | 1 | ⬜ |
| 3 | knowledge-store-tests | knowledge-pipeline | - | M | 2 | ⬜ |

---

## Phase 2: Migration

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| 4 | migrate-markdown-learnings | knowledge-pipeline | - | M | 1 | ⬜ |
| 5 | migrate-eval-jsons | knowledge-pipeline | - | M | 1 | ⬜ |
| 6 | migrate-pending-entries | knowledge-pipeline | - | S | 1 | ⬜ |
| 7 | migration-runner | knowledge-pipeline | - | M | 4,5,6 | ⬜ |

---

## Phase 3: Wire Writes

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| 8 | wire-writes-eval-sidecar | knowledge-pipeline | - | M | 1 | ⬜ |
| 9 | wire-writes-build-loop | knowledge-pipeline | - | M | 1 | ⬜ |
| 10 | wire-writes-mistake-tracker | knowledge-pipeline | - | M | 1 | ⬜ |
| 11 | wire-writes-auto-qa | knowledge-pipeline | - | M | 1 | ⬜ |

---

## Phase 4: Wire Reads

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| 12 | replace-broken-readers | knowledge-pipeline | - | M | 2,7 | ⬜ |
| 13 | unified-knowledge-section | knowledge-pipeline | - | M | 12 | ⬜ |

---

## Phase 5: Backtest + Tune

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| 14 | backtest-function | knowledge-pipeline | - | L | 7,12 | ⬜ |
| 15 | fts5-weight-tuner | knowledge-pipeline | - | M | 14 | ⬜ |

---

## Phase 6: Continuous Optimization

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| 16 | retrieval-logging | knowledge-pipeline | - | S | 12 | ⬜ |
| 17 | post-eval-scoring | knowledge-pipeline | - | M | 16 | ⬜ |
| 18 | periodic-retune-trigger | knowledge-pipeline | - | M | 15,17 | ⬜ |

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | Pending - not started |
| 🔄 | In Progress - currently being built |
| ✅ | Completed - PR merged |
| ⏸️ | Blocked - waiting on dependency or decision |

## Complexity Legend

| Symbol | Meaning | Typical Scope |
|--------|---------|---------------|
| S | Small | Single module, few functions |
| M | Medium | Multiple functions, moderate logic |
| L | Large | Cross-module, complex logic |
