---
description: Mechanical propagation check after writing learnings or protocol changes
---

Verify propagation: $ARGUMENTS

## Purpose
After writing a learning or changing a protocol file, mechanically verify
all consumption points are updated. Prevents drift where the rule says one
thing but the onboarding path teaches another (L-0114).

## Process

### 1. Identify What Changed
Parse $ARGUMENTS or scan `git diff --name-only HEAD` for:
- `learnings/*.md` — new or modified learnings
- `.claude/commands/checkpoint.md` — protocol changes
- `ONBOARDING.md` — onboarding path changes

### 2. For Each New Learning (L-XXXX)

**a) Core check**: Read `learnings/core.md`. Apply L-0118 criterion:
"If a fresh session doesn't know this, will it make a mistake that matters?"
- If yes and NOT in core.md → flag: "L-XXXX should be in core.md"
- If no → skip

**b) Count check**: Run `/verify-learnings-counts` to catch drift.

### 3. For Each Protocol Change

Check these files for stale references:
- `ONBOARDING.md` — step summary must match protocol definition
- `ACTIVE-CONSIDERATIONS.md` — any mentions of the changed protocol
- `learnings/core.md` — if protocol is referenced in a core learning

### 4. Convention File Audit (L-0125)

Check for stale references in files agents read:
- `CLAUDE.md` — conventions file for Claude Code agents
- `.claude/commands/*.md` — slash commands that reference changed items

### 5. Report

```
## Propagation Check

Changes detected:
  - L-0127 added to process-rules.md
  - checkpoint.md step 4 modified

Propagation status:
  core.md: L-0127 — does not meet core threshold (operational, not constitutional) ✅ SKIP
  ONBOARDING.md counts: 62 claimed, 62 actual ✅ MATCH
  ACTIVE-CONSIDERATIONS.md: counts match ✅
  CLAUDE.md: no stale references ✅

Result: ALL CLEAR
```

### 6. Fix
Apply fixes for any flagged items. Count corrections are mechanical —
no Brian approval needed. Core.md additions need Brian's approval.

## When to Run
- Automatically during checkpoint step 4 propagation check
- After any commit that touches learnings/ or protocol files
- When `--quick` flag: skip convention file audit, just do counts + core check
