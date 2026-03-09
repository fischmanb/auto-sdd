# System Documentation

> **Single entry point for all auto-sdd documentation.** Everything navigable from here.
>
> For fresh onboarding, read `ONBOARDING.md` at repo root first — it bootstraps the session protocol.
> This directory is the organized reference layer for everything else.

---

## How to use this directory

**Building or debugging?** → `operations/`
**Understanding the architecture?** → `system/`
**Writing prompts or starting a session?** → `guides/`
**Looking up a past decision or learning?** → `knowledge/`
**Checking what's planned?** → `plans/`
**Reviewing agent round history?** → `history/`

---

## Directory map

```
docs/
├── README.md                          ← YOU ARE HERE
├── system/                            # How the system works
│   ├── architecture-summary.md        # Compact reference (~80 lines) — pipeline, modules, gates, retry, signals
│   ├── architecture.md                # System 1 (orchestration) + System 2 (archived local LLM)
│   ├── design-principles.md           # Grepability, graph-readiness, relationship schema, enums
│   ├── signal-protocol.md             # Agent signal format (FEATURE_BUILT, BUILD_FAILED, etc.)
│   └── configuration.md               # .sdd-config/project.yaml schema + .env.local reference
├── operations/                        # How to run things
│   ├── running-builds.md              # Build loop commands, env vars, campaign workflows
│   ├── retry-strategy.md              # Two-stage retry: fix-in-place → informed fresh retry
│   └── commands-reference.md          # Index of all .claude/commands/ slash commands
├── guides/                            # How to work with the system
│   ├── prompt-engineering.md          # Methodology for writing hardened agent prompts
│   ├── new-chat-prompt.md             # Fresh session bootstrap prompt
│   └── campaign-data-recovery.md      # Recovering campaign data from logs
├── knowledge/                         # What we've learned
│   ├── decisions.md                   # Append-only decision log with rationale
│   ├── methodology.md                 # HOW-I-WORK-WITH-GENERATIVE-AI observations
│   └── learnings/                     # Typed learning catalog (graph-schema format)
│       ├── core.md                    # 17 curated constitutional learnings (read every fresh onboard)
│       ├── failure-patterns.md        # failure_pattern entries
│       ├── process-rules.md           # process_rule entries
│       ├── empirical-findings.md      # empirical_finding entries
│       ├── architectural-rationale.md # architectural_rationale entries
│       └── domain-knowledge.md        # domain_knowledge entries
├── plans/                             # Work-in-progress specs and designs
│   ├── post-campaign-validation.md    # Seven-phase runtime validation pipeline (v0.3)
│   ├── campaign-intelligence-system.md# CIS Rounds 5-6 design
│   ├── knowledge-graph-build-intelligence.md
│   ├── auto-qa-cre-validation.md      # Auto-QA against SitDeck
│   ├── project-isolation-contract.md  # Three-layer isolation enforcement
│   ├── seed-data-distribution.md      # Seed data strategy
│   └── bash-to-python-conversion.md   # Phase 6 remaining (nightly, mapping, estimates)
└── history/
    └── agents.md                      # Full agent work log (Rounds 1–37+)
```

---

## Files that stay at repo root (protocol-critical)

| File | Why it stays |
|------|-------------|
| `ONBOARDING.md` | `.onboarding-state` protocol reads from root path |
| `ACTIVE-CONSIDERATIONS.md` | Checkpoint protocol reads/writes from root |
| `CLAUDE.md` | Claude Code agents read from repo root automatically |
| `README.md` | GitHub convention |
| `DECISIONS.md` | Checkpoint protocol appends here |
| `HOW-I-WORK-WITH-GENERATIVE-AI.md` | Checkpoint step 5 writes here |
| `.onboarding-state` | Protocol state file |
| `VERSION` | Semantic version |

The `docs/knowledge/` copies of `decisions.md` and `methodology.md` are the navigable versions.
Canonical writes still happen at root; docs/ copies are refreshed at checkpoint time.

---

## Quick lookups

**"What env vars does the build loop accept?"** → `system/configuration.md`
**"How does the system work?"** → `system/architecture-summary.md`
**"How does retry work?"** → `operations/retry-strategy.md`
**"What signals do agents emit?"** → `system/signal-protocol.md`
**"What failed before and why?"** → `knowledge/learnings/failure-patterns.md`
**"What was decided about X?"** → `knowledge/decisions.md`
**"How do I write a good agent prompt?"** → `guides/prompt-engineering.md`
**"What slash commands exist?"** → `operations/commands-reference.md`
**"What happened in Round N?"** → `history/agents.md`
