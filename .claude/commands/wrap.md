---
description: End-of-session wrap-up. Runs !learn, full checkpoint, and handoff file creation in sequence. Single command for retiring a chat.
---

# !wrap — End-of-Session Protocol

Single command to close out a session cleanly. Covers learnings extraction, full context checkpoint, and handoff file for the next session.

**Use when:** Brian says "wrap up", "new chat", "retiring this chat", 2+ compactions have occurred, or the session has accomplished its goals.

**Do not split across responses unless Brian asks.** Run the full sequence.

---

## Sequence

### Phase 1 — Learnings (`!learn`)

Execute the full `!learn` protocol from `.claude/commands/extract-learnings.md`.

This covers:
- Read current state (highest L- and M-numbers)
- Check HOW-I-WORK accumulation section
- Scan session: corrections, new rules, empirical findings, failures, methodology signals — both L-entries and M-entries
- Process `logs/learning-candidates.txt` if it exists (build agent candidates)
- Propose all candidates to Brian with full graph-schema entries
- **Wait for Brian's approval before writing anything**
- On approval: write to learnings files, increment counts, commit with message `learnings: L-NNNNN–L-NNNNN, M-NNNNN–M-NNNNN from !wrap`
- Run token usage report, append to general-estimates.jsonl with activity_type "wrap-learn"

### Phase 2 — Checkpoint (steps 4+5 already done in Phase 1)

Execute checkpoint steps in order, skipping 4 and 5 (covered by !learn):

**Step 1 — State file**
Read `.onboarding-state`. If `pending_captures` non-empty → proceed to step 2. Else skip to step 3.

**Step 2 — Flush captures**
Read `ACTIVE-CONSIDERATIONS.md`. Staleness scan: flag any items marked ✅/complete/merged/done to Brian, do not auto-remove. Update priority stack if priorities changed this session. Append `pending_captures` to appropriate section. Clear `pending_captures`.

**Step 3 — Decisions**
Review session for settled questions. Append to `DECISIONS.md` (date, what, why, rejected alternatives). Skip if none.

~~**Step 4 — Learnings**~~ ← Completed in Phase 1.

~~**Step 5 — Methodology signals**~~ ← Completed in Phase 1 (M-entries).

**Step 6 — ONBOARDING.md drift check**
`md5 -q ~/auto-sdd/ONBOARDING.md`. Compare to `last_check_hash` in `.onboarding-state`. Note changes if hash differs. Update hash.

**Step 7 — Commit and push (checkpoint files)**
`git add .onboarding-state ACTIVE-CONSIDERATIONS.md DECISIONS.md` (plus any other modified context files). `git commit -m "checkpoint: <brief summary>"`. Push — checkpoint commits always push, no approval needed.

**Step 8 — Update state**
Write `.onboarding-state`: `last_check_ts` = now, `last_check_hash` = current hash, `prompt_count` = 0, `pending_captures` = [].

**Step 9 — Context-loss self-test**
"If the context window were wiped after this response, could the next session pick up from file state alone?"
- `.onboarding-state` reflects current HEAD?
- `ACTIVE-CONSIDERATIONS.md` lists what's in-flight and what's next?
- All work committed (or described in a file if mid-stream)?
- Multi-response plans externalized, not only in context?

If any answer is no — fix it before proceeding to Phase 3.

### Phase 3 — Handoff File

**Write `.handoff.md`** at repo root (`~/auto-sdd/.handoff.md`). Keep it under 50 lines. The next session reads this on its first prompt and then archives it to `archive/handoffs/handoff-{DATE}.md`.

```markdown
# Session Handoff — [DATE]

## Session Summary
[1-3 sentences: what this session accomplished]

## Commits This Session
[commit hashes and one-line descriptions]

## Incomplete Work
[items started but not finished, with current state]

## Pending Decisions
[decisions that need Brian's input, with context]

## Active Priorities for Next Session
[ordered list — what the next session should do first]

## Context the Next Session Needs
[anything non-obvious that took this session time to discover]

## Files Modified This Session
[key files touched]
```

**Update `ACTIVE-CONSIDERATIONS.md`** — ensure all open items are current. This is the persistent cross-session state.

**Clear `.prompt-stash.json`** — content has been mined.

**Final push** — push any remaining commits. Non-checkpoint commits require Brian's explicit approval before pushing.

---

## What This Is Not

- The handoff file is not a replacement for learnings. Anything reusable goes in `/learnings`. The handoff covers ephemeral session-specific state only.
- Phase 2 steps 4+5 are intentionally omitted — `!learn` in Phase 1 is the complete execution of those steps. Do not re-scan the session.

---

## Quick Reference

```
!wrap = !learn (wait for approval) → checkpoint steps 1-3, 6-9 → .handoff.md + ACTIVE-CONSIDERATIONS update
```
