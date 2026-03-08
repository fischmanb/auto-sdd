---
feature: Deal Pipeline
domain: deal-intelligence
source: components/widgets/DealPipelineWidget.tsx
tests:
  - tests/db/deal-pipeline.test.ts
components:
  - DealPipelineWidget
status: implemented
created: 2026-03-08
updated: 2026-03-08
---

# Feature: Deal Pipeline

**Source File**: components/widgets/DealPipelineWidget.tsx
**Design System**: .specs/design-system/tokens.md

A Kanban-style deal tracker that lets users manage CRE deals through pipeline stages. Each deal card shows property, counterparty, deal type, market, sqft, and estimated value. Users can add deals, move them between stages, and delete them. Data persists in SQLite (better-sqlite3).

## Feature: Deal Pipeline

### Scenario: View pipeline board (default)
Given the widget loads
When no filters are active
Then a Kanban board is displayed with 7 stage columns
And each column shows its deal cards and deal count
And columns are ordered: Prospect, Underwriting, LOI, Due Diligence, Closing, Closed Won, Dead

### Scenario: Filter by deal type
Given deals of type Lease and Sale exist
When the Type filter is set to "Lease" or "Sale"
Then only cards matching that deal type are shown across all columns

### Scenario: Filter by market
Given deals in multiple markets exist
When a market is selected from the Market filter
Then only deals matching that market are shown

### Scenario: Add a new deal
Given the user clicks "Add Deal"
When they fill in address, counterparty, deal type, market, and stage fields (required)
And optionally fill in sqft, value, priority, and notes
And submit the form
Then the new deal card appears in the correct stage column
And the column deal count increments

### Scenario: Move a deal to a different stage
Given a deal card is visible
When the user changes the stage dropdown on the card
Then the card moves to the new column
And the old and new column counts update accordingly

### Scenario: Delete a deal
Given a deal card is visible
When the user clicks "Delete" on the card and confirms
Then the card is removed from the board

### Scenario: Empty stage
Given a stage column has no deals
Then it shows a placeholder "No deals in this stage"
And the column header shows "(0)"

### Scenario: Empty state (no deals match filters)
Given an active filter produces no results
Then all columns show the empty placeholder

## Data Model

Each `PipelineDeal` record includes:
- `id` — unique deal identifier
- `address` — property street address
- `counterparty` — tenant name (lease) or buyer/seller name (sale)
- `deal_type` — "Lease" or "Sale"
- `market` — CRE market (e.g., "New York City")
- `sqft` — transaction square footage (nullable)
- `deal_value` — estimated deal value in USD (nullable)
- `stage` — pipeline stage (one of 7 stages)
- `priority` — "Low", "Medium", or "High"
- `notes` — free-form notes
- `created_at` — ISO 8601 creation timestamp
- `updated_at` — ISO 8601 last-updated timestamp

Pipeline stages (ordered):
1. Prospect
2. Underwriting
3. LOI
4. Due Diligence
5. Closing
6. Closed Won
7. Dead

## UI Mockup

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Deal Pipeline                                                                 │
│                                                                                │
│  Type [All ▼]   Market [All ▼]                          [+ Add Deal]          │
│                                                                                │
│ ┌─Prospect(2)─┐ ┌─Underwriting(1)┐ ┌─LOI(1)──────┐ ┌─Due Diligence(1)─┐    │
│ │ 30 Hudson Yds│ │ 350 N Michigan │ │ Brickell Ctr│ │ Fulton Mkt Tower │    │
│ │ WarnerMedia  │ │ JP Morgan Chase│ │ Blackstone  │ │ Hines            │    │
│ │ Lease · NYC  │ │ Sale · Chicago │ │ Sale · Miami│ │ Lease · Chicago  │    │
│ │ 45,000 SF    │ │ $320M          │ │ $85M        │ │ 22,000 SF        │    │
│ │ [Stage ▼][✕] │ │ [Stage ▼][✕]  │ │[Stage ▼][✕] │ │ [Stage ▼][✕]    │    │
│ └─────────────┘ └────────────────┘ └─────────────┘ └──────────────────┘    │
│                                                                                │
│ ┌─Closing(1)──┐ ┌─Closed Won(2)─┐ ┌─Dead(1)─────┐                           │
│ │ 425 Park Ave │ │ One Vanderbilt │ │ 600 Lex Ave │                           │
│ │ Citadel      │ │ KKR            │ │ WeWork      │                           │
│ │ Lease · NYC  │ │ Sale · NYC     │ │ Lease · NYC │                           │
│ │ 68,000 SF    │ │ $2.1B          │ │ 15,000 SF   │                           │
│ │ [Stage ▼][✕] │ │ [Stage ▼][✕]  │ │[Stage ▼][✕] │                           │
│ └─────────────┘ └───────────────┘ └─────────────┘                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Implementation Notes

- `updatePipelineDeal(id, patch)` exists in `lib/db/deal-pipeline.ts` and is fully tested but is **not yet exposed** via the tRPC router or UI. It supports partial updates to any deal field.
- The tRPC router exposes a `stages` endpoint (`dealPipeline.stages`) but the widget hardcodes `PIPELINE_STAGES` locally instead of fetching from the server.
- Priority badges (High/Medium/Low) are displayed on each deal card with color coding, complementing the priority field in the data model.

## Component References

- Design tokens: .specs/design-system/tokens.md
