# F-037: Client Data Overlay

**Category**: Data Integration
**Phase**: 2
**Data Source**: Client
**Status**: Planned

## Description

Allows users to upload their own proprietary data (rent rolls, portfolio lists, custom market data) and overlay it on CompStak's market data within the map and chart widgets. Enables side-by-side comparison of internal portfolio performance against market benchmarks without exposing proprietary data to the platform.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while client data processes
- [ ] Empty state shown when no client data has been uploaded
- [ ] CSV file upload with drag-and-drop support (max 50MB)
- [ ] Column mapping UI: user maps their CSV columns to standard fields (address, market, rent, sqft, etc.)
- [ ] Uploaded data displayed as distinct layer on CRE Property Map (F-001) with different marker color
- [ ] Comparison table: client rent vs. market average rent per property, with delta
- [ ] Client data stored locally in DuckDB — never sent to external servers
- [ ] "Clear client data" button to remove all uploaded data

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

// 5+ records representing client-uploaded rent roll data
const MOCK_RECORDS = [
  {
    "client_property_address": "200 Clarendon St",
    "client_market": "Boston",
    "client_submarket": "Back Bay",
    "client_tenant": "PwC LLP",
    "client_sqft": 65000,
    "client_rent": 72.00,
    "client_expiration": "2028-06-30",
    "market_avg_rent": 68.00,
    "delta_pct": 5.9
  },
  {
    "client_property_address": "1201 New York Ave NW",
    "client_market": "Washington DC",
    "client_submarket": "East End",
    "client_tenant": "Covington & Burling",
    "client_sqft": 45000,
    "client_rent": 62.00,
    "client_expiration": "2029-12-31",
    "market_avg_rent": 58.00,
    "delta_pct": 6.9
  },
  {
    "client_property_address": "233 S Wacker Dr",
    "client_market": "Chicago Metro",
    "client_submarket": "Chicago CBD",
    "client_tenant": "United Airlines",
    "client_sqft": 88000,
    "client_rent": 46.00,
    "client_expiration": "2030-03-31",
    "market_avg_rent": 44.00,
    "delta_pct": 4.5
  },
  {
    "client_property_address": "2000 McKinney Ave",
    "client_market": "Dallas - Ft. Worth",
    "client_submarket": "Uptown/Turtle Creek",
    "client_tenant": "Goldman Sachs",
    "client_sqft": 35000,
    "client_rent": 42.00,
    "client_expiration": "2027-09-30",
    "market_avg_rent": 38.00,
    "delta_pct": 10.5
  },
  {
    "client_property_address": "400 Fairview Ave N",
    "client_market": "Seattle",
    "client_submarket": "South Lake Union",
    "client_tenant": "Meta Platforms",
    "client_sqft": 110000,
    "client_rent": 52.00,
    "client_expiration": "2028-12-31",
    "market_avg_rent": 48.00,
    "delta_pct": 8.3
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- Client data loaded into a separate DuckDB table (client_data) — no mixing with CompStak CSV tables
- Submarket filter wired to parent Market selection — no change at integration
- Column mapping stored in widget config — user defines mapping once per uploaded file
- Market average rent derived from leases CSV queries matching same market/submarket/class — cross-widget dependency with F-004
- Privacy: client data must remain local — no transmission to external APIs including AI endpoints
