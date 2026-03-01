# DECISIONS.md

> Append-only decision log. Prevents re-litigating settled questions across sessions.
> Format: date, what, why, alternatives rejected.

---

## 2026-02-28 — Learnings system: separate file per type (not monolithic catalog)

**Decision:** One file per learning type in `learnings/` at repo root.
**Why:** Grep works per-type without filtering. Files stay manageable size. New types = new file, not restructuring.
**Rejected:** Single monolithic catalog (scaling concern), directory-per-entry (overkill for markdown entries).

---

## 2026-02-28 — Learnings schema: flat K:V metadata (not YAML or compressed header)

**Decision:** Each entry uses `Key: value` on separate lines. One `Related:` line per relationship.
**Why:** Only format satisfying DESIGN-PRINCIPLES.md §1 (grepability without parsing). `grep "Type: failure_pattern"` just works.
**Rejected:** Alt A (pipe-delimited header) — saves 3 lines but breaks grep reliability. Alt B (YAML block) — requires jq/yq, violates "no nested structures requiring parsing."

---

## 2026-02-28 — Global sequential L-XXXX IDs (not per-type prefixes)

**Decision:** Single ID sequence shared across all learnings files.
**Why:** Type already in metadata — encoding in ID violates single-source-of-truth. Collision risk near zero with serial writes.
**Rejected:** Per-type prefixes (FP-0001, PR-0001) — redundant with Type field.

---

## 2026-02-28 — ISO 8601 datetime with timezone (not date-only)

**Decision:** `Date: 2026-02-28T20:31:00-05:00` format.
**Why:** Preserves intra-day ordering. Supports ET and future contributors. Grepability unaffected (prefix match works).
**Rejected:** Date-only (YYYY-MM-DD) — loses ordering within a day.

---

## 2026-03-01 — core.md is curated index (not filtered view)

**Decision:** Human judgment selects core entries. Chat proposes, Brian approves. No algorithmic criteria.
**Why:** "What must every fresh session know" is a judgment call, not a query.
**Rejected:** Automated filtering by confidence/status/tag — too mechanical, misses the point.

---

## 2026-03-01 — Deprecate .specs/learnings/agent-operations.md

**Decision:** Add deprecation pointer, preserve file, all new work goes to `learnings/`.
**Why:** 38 entries fully migrated. Single source of truth is now `learnings/`.
**Rejected:** Deletion — old prompts may still reference the path.
