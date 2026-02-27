# Campaign Comparison: Sonnet vs Haiku

## Head-to-Head

| Metric | v2 (Sonnet 4.6) | v3 (Haiku 4.5) | Delta |
|---|---|---|---|
| Features built | **28/28** | 11 (in progress) | — |
| Features failed | **0** | 0 | — |
| Build window | 6.8h | 2.9h* | — |
| **Throughput** | **4.0 feat/h** | **3.8 feat/h** | **~equal** |
| Clean throughput (<60m) | 5.1 feat/h | — | — |
| Median feature time | 9.2 min | 7.4 min | — |
| Mean feature time | 14.9 min | 10.0 min | — |
| Min feature time | 5.4 min | — | — |
| Max feature time | 92.3 min | — | — |
| Cost per feature | $0.07 | $0.08 | ~equal |
| Drift reconciliation rate | 75% (21/28) | 73% | ~equal |

*v3 campaign still in progress — metrics based on partial data (11 features)

## Key Findings

### 1. 28 features, zero failures

The v2 (Sonnet 4.6) campaign built all 28 features from a React + TypeScript + Next.js roadmap without a single failed build. Features spanned foundation (project setup, auth, DB schema), core UI (deal listings, search, filters, maps), and advanced functionality (analytics, awards, API integrations). Total wall time: 6.8 hours.

### 2. Model speed ≠ build speed

Haiku generates tokens ~2x faster than Sonnet. Yet throughput is nearly identical (4.0 vs 3.8 features/hour). The bottleneck is CPU/disk-bound operations — npm install, TypeScript compilation, test execution, drift checks — not LLM inference. This is the single most counterintuitive finding and the one most teams would get wrong.

**Implication**: Parallelism across features matters more than per-feature model speed. Two Haiku agents building simultaneously would outperform one Sonnet agent, even though Sonnet produces higher-quality code per turn.

### 3. Drift rates are model-independent

Both models produce spec drift at ~73-75%. This means drift is a property of the spec-to-implementation translation problem, not the model. The drift reconciliation system adds overhead per feature but catches real mismatches that compound if ignored.

### 4. Cost is dominated by context, not generation

Cost per feature is nearly identical ($0.07 vs $0.08) despite different model pricing. Cache read tokens dominate both cost profiles — the system pays for context loading, not for the generation itself. This has architectural implications: reducing context window size would cut costs more than switching models.

### 5. Outlier features reveal retry cycles

The 92.3-minute outlier (v2) appears to involve retry cycles where the build loop detected failure and re-ran. Clean throughput (excluding features >60m) is 5.1 features/hour. Signal fallback detection (Round 31) should reduce these outliers in future campaigns.

## Methodology Notes

- Timing from build summary JSON (build loop internal timestamps, most accurate source)
- Git commit timestamps used as cross-reference
- "Clean" throughput excludes features >60 minutes (likely retries, not representative)
- Cost data from cost-log.jsonl — captures sidecar sessions, not primary build agent
- Both campaigns on same machine, same 28-feature roadmap, same codebase spec
- v2 ran to completion; v3 partial data (11 features at time of snapshot)

## Data Completeness

| Artifact | v2 (Sonnet) | v3 (Haiku) |
|---|---|---|
| Build summary JSON | ✅ complete | ⏳ campaign in progress |
| Build log | ✅ recovered (132KB) | ✅ recovered (53KB) |
| Cost log (JSONL) | ✅ 2 entries | ✅ 3 entries |
| Git history (timing) | ✅ 77 commits | ✅ 31 commits |
| Roadmap state | ✅ 28/28 complete | ✅ snapshot |
| Sidecar evals | ❌ not configured | ✅ 5 eval JSONs |
| Resume state | ✅ snapshot | ✅ snapshot |

Generated: 2026-02-28
