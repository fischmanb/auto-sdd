# F-029: Deal Pipeline

**Category**: Deal Intelligence
**Phase**: 2
**Data Source**: SQLite
**Status**: Planned

## Description

Kanban-style deal tracker where users manage their active deals through stages (Prospecting, LOI, Negotiation, Signed, Closed). Unlike transaction data from CSVs which shows completed deals, this widget tracks in-progress opportunities with user-entered notes, probability estimates, and target dates.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while SQLite query executes
- [ ] Empty state shown when no deals exist in pipeline
- [ ] Kanban board with columns: Prospecting, LOI, Negotiation, Signed, Closed
- [ ] Deal cards show: property address, tenant/buyer name, estimated SQFT, estimated rent/price, probability %, target close date
- [ ] Drag-and-drop to move deals between stages
- [ ] Add new deal form: address, market, tenant name, SQFT, estimated value, notes
- [ ] Summary bar: total pipeline value, deal count per stage, weighted pipeline value (value × probability)

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

// 5+ records representing pipeline deals — user-created data, not CSV records
const MOCK_RECORDS = [
  {
    "deal_id": "DEAL-001",
    "property_address": "200 Park Ave",
    "Market": "New York City",
    "Property Type": "Office",
    "tenant_name": "Acme Corp",
    "estimated_sqft": 35000,
    "estimated_rent": 82.00,
    "stage": "Negotiation",
    "probability_pct": 65,
    "target_close_date": "2026-05-15",
    "notes": "Tenant prefers 10-year term, landlord countered at $85/SF"
  },
  {
    "deal_id": "DEAL-002",
    "property_address": "100 Federal St",
    "Market": "Boston",
    "Property Type": "Office",
    "tenant_name": "TechStartup Inc",
    "estimated_sqft": 15000,
    "estimated_rent": 68.00,
    "stage": "LOI",
    "probability_pct": 40,
    "target_close_date": "2026-06-30",
    "notes": "LOI sent, awaiting landlord response"
  },
  {
    "deal_id": "DEAL-003",
    "property_address": "333 W Wacker Dr",
    "Market": "Chicago Metro",
    "Property Type": "Office",
    "tenant_name": "Global Consulting",
    "estimated_sqft": 48000,
    "estimated_rent": 44.00,
    "stage": "Signed",
    "probability_pct": 95,
    "target_close_date": "2026-04-01",
    "notes": "Lease signed, commencement pending TI buildout"
  },
  {
    "deal_id": "DEAL-004",
    "property_address": "2100 Ross Ave",
    "Market": "Dallas - Ft. Worth",
    "Property Type": "Office",
    "tenant_name": "EnergyServices LLC",
    "estimated_sqft": 22000,
    "estimated_rent": 36.00,
    "stage": "Prospecting",
    "probability_pct": 15,
    "target_close_date": "2026-08-01",
    "notes": "Initial tour scheduled next week"
  },
  {
    "deal_id": "DEAL-005",
    "property_address": "1100 Peachtree St",
    "Market": "Atlanta",
    "Property Type": "Office",
    "tenant_name": "FinTech Solutions",
    "estimated_sqft": 30000,
    "estimated_rent": 38.00,
    "stage": "Negotiation",
    "probability_pct": 55,
    "target_close_date": "2026-05-01",
    "notes": "Negotiating TI allowance and free rent concession"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- Deal pipeline data stored in local SQLite — not in CSV files
- At integration: CRUD endpoints for deals via tRPC routes
- Pipeline stages are a fixed enum: ["Prospecting", "LOI", "Negotiation", "Signed", "Closed"]
- Weighted pipeline value = SUM(estimated_rent × estimated_sqft × probability_pct / 100)
