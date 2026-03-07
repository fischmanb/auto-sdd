# F-030: News Alerts

**Category**: Deal Intelligence
**Phase**: 2
**Data Source**: External
**Status**: Planned

## Description

Configurable alert system that monitors CRE news feeds and notifies users when articles match their saved criteria — specific markets, property types, tenant names, or keywords. Extends Breaking CRE News (F-027) with persistent, personalized notification rules rather than passive browsing.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant for alert rule creation
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant for alert rule creation
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while alert rules and matches load
- [ ] Empty state shown when no alert rules are configured
- [ ] Alert rule builder: select market(s), property type(s), enter keyword(s), choose frequency (instant, daily digest, weekly digest)
- [ ] Alert list shows matched articles grouped by rule with match count badges
- [ ] Mark alerts as read/unread with visual distinction
- [ ] Maximum 20 active alert rules per user
- [ ] Unread alert count displayed as badge on widget header

## Mock Data Spec

```typescript
const MOCK_MARKETS = [
  "New York City", "Los Angeles - Orange - Inland", "Chicago Metro",
  "Dallas - Ft. Worth", "Boston", "Bay Area", "Washington DC", "Houston",
  "Atlanta", "Miami - Ft. Lauderdale", "Seattle", "Denver",
  "Philadelphia - Central PA - DE - So. NJ", "Phoenix", "Austin",
  "Nashville", "Charlotte", "Tampa Bay", "San Francisco", "San Diego",
  "New Jersey - North and Central", "Long Island", "Westchester and CT",
  "Baltimore", "Minneapolis - St. Paul", "Detroit - Ann Arbor - Lansing",
  "St. Louis Metro", "Kansas City Metro", "Portland Metro",
  "Sacramento - Central Valley", "Las Vegas", "Salt Lake City",
  "Indianapolis", "Columbus", "Pittsburgh", "Richmond",
  "Raleigh - Durham", "Orlando", "Jacksonville", "San Antonio"
];

const MOCK_BUILDING_CLASSES = ["A", "B", "C"];

const MOCK_PROPERTY_TYPES = [
  "Hotel", "Industrial", "Land", "Mixed-Use", "Multi-Family",
  "Office", "Other", "Retail"
];

const MOCK_SPACE_TYPES = [
  "Office", "Industrial", "Retail", "Flex/R&D", "Land", "Other"
];

const MOCK_TRANSACTION_TYPES = [
  "New Lease", "Renewal", "Expansion", "Extension", "Extension/Expansion",
  "Early Renewal", "Pre-lease", "Relet", "Assignment", "Restructure",
  "Renewal/Expansion", "Renewal/Contraction", "Long leasehold"
];

const MOCK_LEASE_TYPES = [
  "Full Service", "Gross", "Industrial Gross", "Modified Gross",
  "Net", "NN", "NNN", "Net of Electric"
];

// 5+ records representing alert rules and matches — not CSV transaction records
const MOCK_RECORDS = [
  {
    "alert_id": "ALERT-001",
    "rule_name": "NYC Office Deals > 50K SF",
    "markets": ["New York City"],
    "property_types": ["Office"],
    "keywords": ["lease", "signed"],
    "min_sqft": 50000,
    "frequency": "instant",
    "unread_count": 3,
    "last_match_date": "2026-03-06T14:30:00Z"
  },
  {
    "alert_id": "ALERT-002",
    "rule_name": "Miami Industrial Activity",
    "markets": ["Miami - Ft. Lauderdale"],
    "property_types": ["Industrial"],
    "keywords": ["warehouse", "distribution", "logistics"],
    "frequency": "daily",
    "unread_count": 7,
    "last_match_date": "2026-03-05T10:15:00Z"
  },
  {
    "alert_id": "ALERT-003",
    "rule_name": "Tech Tenant Relocations",
    "markets": ["Bay Area", "Austin", "Seattle"],
    "property_types": ["Office"],
    "keywords": ["relocation", "headquarters", "tech"],
    "frequency": "weekly",
    "unread_count": 12,
    "last_match_date": "2026-03-04T08:00:00Z"
  },
  {
    "alert_id": "ALERT-004",
    "rule_name": "Cap Rate Compression News",
    "markets": [],
    "property_types": [],
    "keywords": ["cap rate", "yield compression", "investment sales"],
    "frequency": "daily",
    "unread_count": 5,
    "last_match_date": "2026-03-03T16:45:00Z"
  },
  {
    "alert_id": "ALERT-005",
    "rule_name": "Dallas Retail Leasing",
    "markets": ["Dallas - Ft. Worth"],
    "property_types": ["Retail"],
    "keywords": ["retail", "shopping", "restaurant"],
    "frequency": "weekly",
    "unread_count": 0,
    "last_match_date": "2026-02-28T09:00:00Z"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- Alert rules stored in local SQLite — not in CSV files
- At integration: CRUD for alert rules, background job matching news to rules
- News source integration shared with F-027 Breaking CRE News
- Notification delivery (email, in-app) depends on user account system — Phase 2 scope is in-app only
