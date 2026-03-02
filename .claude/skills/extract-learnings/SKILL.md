---
name: extract-learnings
description: Scan current session for uncaptured learnings and output in graph schema format. Use when Brian says "extract learnings", "get learnings", or "what did we learn".
---

# Extract Learnings from Current Session

Scan this session for uncaptured learnings and output them in graph schema format.

## Process

1. Read current highest L-number and M-number:
   ```bash
   grep "^## [LM]-" learnings/*.md HOW-I-WORK-WITH-GENERATIVE-AI.md | sed 's/.*\([LM]-[0-9]*\).*/\1/' | sort -t'-' -k2 -n | tail -5
   ```

2. Review everything discussed this session. Classify candidates:

   **L-entries** (system/process/engineering learnings):
   - process-rule, empirical-finding, architecture-decision

   **M-entries** (methodology signals about Brian's working style):
   - observation, preference, principle, workflow_fact

3. Deduplicate against existing entries. Skip if already captured, cite the existing entry.

4. Output each in graph schema:
   ```
   ## L-NNNNN
   - **Type:** [type]
   - **Tags:** [tags]
   - **Confidence:** [high/medium/low] — [justification]
   - **Status:** active
   - **Date:** [today]
   - **Related:** [references]

   [Specific body text with concrete details — commands, numbers, failure modes.]
   ```

5. Ask Brian to confirm before writing to files.

## What counts

**YES:** Something broke unexpectedly, heuristic proven wrong, process step missing, Brian corrected Claude, tool behaved differently, decision with explicit tradeoffs.

**NO:** Restating existing learnings, obvious from codebase, no future relevance, vague "be more careful" (L-00117).
