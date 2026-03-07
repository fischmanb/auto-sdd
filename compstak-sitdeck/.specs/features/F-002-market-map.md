# F-002: Market Map

**Category**: Map
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Choropleth-style map visualizing lease activity intensity across submarkets within a selected market. Shading density reflects transaction volume or average rent, letting brokers instantly identify hot and cold zones. Extends the base map component from F-001.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Submarket regions shaded by selectable metric: transaction count, average Starting Rent, or total Transaction SQFT
- [ ] Color scale legend displayed with min/max values
- [ ] Hovering a submarket region shows tooltip with submarket name and metric value
- [ ] Date range filter constrains Execution Date for included transactions

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

// 5+ records using exact CSV column names
const MOCK_RECORDS = [
  {
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 82.50,
    "Transaction SQFT": 45000,
    "Execution Date": "2025-09-15",
    "Transaction Type": "New Lease"
  },
  {
    "Market": "New York City",
    "Submarket": "Downtown Manhattan",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 64.00,
    "Transaction SQFT": 32000,
    "Execution Date": "2025-10-01",
    "Transaction Type": "Renewal"
  },
  {
    "Market": "New York City",
    "Submarket": "Midtown South",
    "Space Type": "Office",
    "Building Class": "B",
    "Property Type": "Office",
    "Starting Rent": 58.25,
    "Transaction SQFT": 18000,
    "Execution Date": "2025-08-20",
    "Transaction Type": "New Lease"
  },
  {
    "Market": "New York City",
    "Submarket": "Penn Plaza/Garment",
    "Space Type": "Retail",
    "Building Class": "B",
    "Property Type": "Retail",
    "Starting Rent": 95.00,
    "Transaction SQFT": 5500,
    "Execution Date": "2025-11-12",
    "Transaction Type": "Relet"
  },
  {
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 78.00,
    "Transaction SQFT": 28000,
    "Execution Date": "2025-07-30",
    "Transaction Type": "Expansion"
  },
  {
    "Market": "New York City",
    "Submarket": "Hudson Yards",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 105.00,
    "Transaction SQFT": 62000,
    "Execution Date": "2025-06-18",
    "Transaction Type": "Pre-lease"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Submarket boundary polygons not in CSV data — will need GeoJSON source at integration time
