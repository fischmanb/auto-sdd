# Agent Prompt: Schema Standardization + ID Format Expansion

## Precondition
```
Must be on main branch, up to date with origin.
Verify: git branch --show-current && git fetch origin && git diff main origin/main --stat
If not on main or not up to date: STOP. Report and wait.
```

## Context
The auto-sdd project has two systems that need structural alignment:
1. **Learnings** (`learnings/*.md`): 74 entries in graph-ready schema with IDs like `L-0141`
2. **HOW-I-WORK-WITH-GENERATIVE-AI.md**: 63+ methodology observations as bullet points

Two problems:
- HOW-I-WORK entries are raw bullets, not graph-schema. They need the same structured format as learnings.
- L-number IDs are 4-digit zero-padded (L-0001). Brian expects 10,000+ entries. The format must expand.

## Action Items (investigate → decide → implement)

### 1. ID Format Expansion
**Investigate:**
- Current format: `L-NNNN` (4 digits, max L-9999)
- 411 references across 23 .md files (see list below)
- What digit width supports 10,000+ with room to grow? 5? 6? Variable?
- What's the migration path for existing references?

**Decide** (document in DECISIONS.md):
- New format (e.g., L-00001 for 5-digit)
- Whether HOW-I-WORK entries get their own ID prefix (e.g., M-00001) or share L-space

**Implement:**
- Rename all existing L-NNNN → new format across ALL 23 files listed below
- Update any grep patterns, regex, or format references in commands/*.md
- Verify: count of entries before = count after. Zero broken references.

**Files containing L-number references:**
```
.checkpoint-stash.md, .claude/commands/checkpoint.md, .claude/commands/compound.md,
.claude/commands/review-signals.md, .claude/commands/verify-learnings-counts.md,
.claude/commands/verify-propagation.md, .specs/learnings/agent-operations.md,
.specs/learnings/core.md, ACTIVE-CONSIDERATIONS.md, Agents.md, DECISIONS.md,
DESIGN-PRINCIPLES.md, HOW-I-WORK-WITH-GENERATIVE-AI.md, ONBOARDING.md,
WIP/bash-to-python-conversion.md, WIP/post-campaign-validation.md,
learnings/architectural-rationale.md, learnings/core.md, learnings/domain-knowledge.md,
learnings/empirical-findings.md, learnings/failure-patterns.md, learnings/process-rules.md,
py/auto_sdd/conventions.md
```

### 2. HOW-I-WORK Graph Schema Conversion
**Investigate:**
- Read `learnings/process-rules.md` for the graph schema format (Type, Tags, Confidence, Status, Date, Related, body)
- Read `HOW-I-WORK-WITH-GENERATIVE-AI.md` — 63+ entries as `- (YYYY-MM-DD) text`
- What metadata fields make sense for methodology observations vs operational learnings?
- Do HOW-I-WORK entries need Confidence/Status? Or are those only meaningful for prescriptive rules?

**Decide** (document reasoning in commit message):
- Schema for HOW-I-WORK entries (which fields, what ID prefix)
- Whether to keep the Accumulation section as raw capture zone or convert everything
- Preserve the preamble and voice guidelines

**Implement:**
- Convert all existing entries to graph-schema format
- Each entry gets: ID, Type (observation/preference/principle/workflow_fact/etc.), Tags, Date, body
- Preserve Brian's direct quotes verbatim in body text (L-0141: quotes carry higher signal than gloss)
- Add one new entry: how Brian defined "close read" — structural audit, not summary. Cluster identification + gap analysis + maturity assessment. See L-0140 for the learning; this is the methodology observation.

### 3. Verification
After all changes:
```bash
# Entry counts
for f in learnings/*.md; do echo "$f: $(grep -c '^## [LM]-' "$f")"; done
grep -c '^## [LM]-' HOW-I-WORK-WITH-GENERATIVE-AI.md

# Reference integrity — no orphaned old-format IDs
grep -rn 'L-0[0-9]\{3\}[^0-9]' --include="*.md" | grep -v 'L-0[0-9]\{4\}' | head -20

# Total reference count should be >= 411 (may increase from HOW-I-WORK cross-refs)
grep -rn '[LM]-[0-9]' --include="*.md" | wc -l
```

## Hard Constraints
- Do NOT push to remote. Commit locally only. Brian reviews and pushes.
- Do NOT modify the preamble/voice guidelines in HOW-I-WORK (lines 1-14).
- Do NOT change learnings body text — only ID format in headers and references.
- Do NOT delete any content. Format conversion only.
- If ANY verification check fails: STOP. Report what failed and wait.
- If the ID format decision has non-obvious tradeoffs: STOP after investigation, report options, wait for decision before implementing.

## Reference Files
- `learnings/process-rules.md` — graph schema examples (look at any L-01XX entry)
- `HOW-I-WORK-WITH-GENERATIVE-AI.md` — entries to convert
- `.claude/commands/verify-learnings-counts.md` — existing count verification (will need regex update)
- `CLAUDE.md` — conventions file, check for format assumptions
