# Build Roadmap

> Ordered list of features to implement. Each feature should be completable within a single agent context window.
> Updated by `/clone-app`, `/roadmap-triage`, and `/build-next`.

---

## Progress

<!-- Auto-updated summary -->

| Status | Count |
|--------|-------|
| ✅ Completed | 0 |
| 🔄 In Progress | 0 |
| ⬜ Pending | 0 |
| ⏸️ Blocked | 0 |

**Last updated**: <!-- timestamp -->

---

## Phase 1: Foundation

> Core infrastructure and authentication. Must be built first.

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| <!-- 1 --> | <!-- Auth: User signup --> | <!-- clone-app --> | <!-- PROJ-101 --> | <!-- M --> | <!-- - --> | <!-- ⬜ --> |

---

## Phase 2: Core Features

> Primary user-facing functionality.

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| <!-- 10 --> | <!-- Dashboard --> | <!-- clone-app --> | <!-- PROJ-110 --> | <!-- L --> | <!-- 1,2 --> | <!-- ⬜ --> |

---

## Phase 3: Enhancement

> Secondary features, polish, and optimizations.

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| <!-- 20 --> | <!-- Dark mode --> | <!-- slack:C123/ts --> | <!-- PROJ-120 --> | <!-- S --> | <!-- - --> | <!-- ⬜ --> |

---

## Ad-hoc Requests

> Features added from Slack/Jira that don't fit a phase. Processed after current phase.

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| <!-- 100 --> | <!-- Export to CSV --> | <!-- jira:PROJ-456 --> | <!-- PROJ-456 --> | <!-- S --> | <!-- 10 --> | <!-- ⬜ --> |

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | Pending - not started |
| 🔄 | In Progress - currently being built |
| ✅ | Completed - PR merged |
| ⏸️ | Blocked - waiting on dependency or decision |
| ❌ | Cancelled - no longer needed |

## Complexity Legend

| Symbol | Meaning | Typical Scope |
|--------|---------|---------------|
| S | Small | Single component, few files |
| M | Medium | Multiple components, moderate logic |
| L | Large | Full feature, many files, complex logic |

---

## Notes

<!-- Any important context for the roadmap -->

---

_This file is the single source of truth for `/build-next`. Features are picked in order, respecting dependencies._
