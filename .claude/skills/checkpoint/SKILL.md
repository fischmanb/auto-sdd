---
name: checkpoint
description: Update all context management files for auto-sdd. Run before ending a session, before a risky operation, or on demand. Use when Brian says "checkpoint", "save state", or "end session".
---

# Checkpoint Protocol

Single command to ensure all context management files are current. Prevents context loss across sessions.

## Checklist (execute in order)

### 1. State File
- Read `~/auto-sdd/.onboarding-state` via Desktop Commander
- If `pending_captures` non-empty → flush to ACTIVE-CONSIDERATIONS.md
- Increment prompt_count

### 2. Decisions
- If any questions settled this session with explicit decisions: append to DECISIONS.md
- If none → skip

### 3. Learnings (active scan)
- **Default: something to capture.** A scan finding zero candidates after agent completions or corrections is evidence of scan failure (L-00116).
- Check each category:
  - Agent completions: what worked, failed, surprised?
  - Corrections: each Brian correction is a candidate
  - New rules or patterns discovered
  - Empirical findings: measurements, data points
  - Failures or near-misses
- For each candidate: output in graph schema, ask Brian to confirm
- **Behavioral compliance check**: review core.md, flag violations

### 4. Methodology Signals
- Scan for operator-level insights about Brian's working style
- If found: append to HOW-I-WORK-WITH-GENERATIVE-AI.md accumulation section
- Format: graph schema with M-NNNNN IDs
- Voice: third person ("Brian prefers..."), empirical not prescriptive

### 5. Commit and Push
- `git add -A && git commit -m "checkpoint: <summary>"` via Desktop Commander
- Push to origin/main

### 6. Update State
Write .onboarding-state with current timestamp, HEAD hash, reset prompt_count to 0.

### 7. Context-Loss Self-Test (L-00130)
"If context were wiped, could next session pick up from file state alone?"
- .onboarding-state reflects HEAD?
- ACTIVE-CONSIDERATIONS.md current?
- All work committed?
- Multi-response plans externalized?
