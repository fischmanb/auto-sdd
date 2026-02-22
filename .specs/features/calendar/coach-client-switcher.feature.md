---
feature: Coach Client Switcher
domain: calendar
source: src/components/coach/ClientSwitcher.tsx
tests:
  - src/components/coach/__tests__/ClientSwitcher.test.tsx
components:
  - ClientSwitcher
status: implemented
created: 2026-02-22
updated: 2026-02-22
---

# Coach Client Switcher

**Source File**: src/components/coach/ClientSwitcher.tsx
**Design System**: .specs/design-system/tokens.md

## Feature: Coach Client Switcher

A horizontal pill/tab row that allows a coach to toggle between clients. Selecting a client updates the WeekView to display that client's blocks.

### Scenario: Display all clients in the switcher

```gherkin
Given a coach has 3 clients in their roster
When the ClientSwitcher renders
Then all 3 client names are displayed as selectable options
And the first client is selected by default (highlighted)
```

### Scenario: Switch to a different client

```gherkin
Given the ClientSwitcher is showing Client A as the active selection
When the coach taps Client B's option
Then Client B becomes the active/highlighted selection
And the onSelect callback is called with Client B's id
```

### Scenario: Selected client's blocks are shown in the WeekView

```gherkin
Given a coach has 2 clients with different blocks
And Client A's blocks are currently shown in the WeekView
When the coach selects Client B in the ClientSwitcher
Then the WeekView re-renders with Client B's blocks
And Client A's blocks are no longer visible
```

### Scenario: Single client (no roster)

```gherkin
Given a coach has only 1 client
When the ClientSwitcher renders with 1 client
Then that client's name is displayed as the only option
And it is shown as selected
```

## UI Mockup

```
┌─────────────────────────────────────────────────────┐
│  Client Switcher (bg: surface, px: spacing-4)       │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ [● Alex Chen] [ Jordan K. ] [ Sam Rivera ]   │   │
│  └──────────────────────────────────────────────┘   │
│   ▲ selected pill: bg-primary text-white             │
│     unselected: bg-surface border text-text          │
│                                                     │
│  Week View (below) shows Alex Chen's blocks...      │
└─────────────────────────────────────────────────────┘

Selected pill:
┌────────────────┐
│  ● Alex Chen   │  (bg-primary, text-white, radius-full, px-4 py-2)
└────────────────┘

Unselected pill:
┌────────────────┐
│    Jordan K.   │  (bg-surface, text-text, border, radius-full, px-4 py-2)
└────────────────┘
```

## Types

```typescript
interface Client {
  id: string
  name: string
  blocks: CalendarBlock[]
}

interface ClientSwitcherProps {
  clients: Client[]
  selectedClientId: string
  onSelect: (clientId: string) => void
}
```

## Mock Data

Co-located at `src/components/coach/__mocks__/clients.ts`.

Requirements:
- 3 clients with distinct names
- Each client has 3–5 blocks in the mock week (2026-02-16)
- Blocks differ per client so switching is visually obvious

## Component References

- ClientSwitcher: new component
