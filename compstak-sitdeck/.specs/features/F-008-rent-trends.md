# F-008: Rent Trends

**Category**: Rent & Pricing
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Time-series chart showing how Starting Rent and Net Effective Rent have trended over a configurable period for a selected market, submarket, and space type. Enables CRE professionals to identify rent growth or compression patterns and time lease negotiations accordingly.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Line chart with dual Y-axis or overlay: median Starting Rent and median Net Effective Rent per quarter
- [ ] Date range selector with presets: 1Y, 3Y, 5Y, and custom range
- [ ] Hover tooltip shows quarter, median rent, transaction count, and YoY % change
- [ ] Option to toggle between median and average aggregation

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

// 5+ records using exact CSV column names — spread across quarters
const MOCK_RECORDS = [
  {
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 42.00,
    "Net Effective Rent": 37.80,
    "Transaction SQFT": 30000,
    "Execution Date": "2024-01-18",
    "Transaction Type": "New Lease"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 43.50,
    "Net Effective Rent": 39.10,
    "Transaction SQFT": 25000,
    "Execution Date": "2024-05-10",
    "Transaction Type": "Renewal"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 44.25,
    "Net Effective Rent": 40.00,
    "Transaction SQFT": 35000,
    "Execution Date": "2024-09-22",
    "Transaction Type": "New Lease"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 45.00,
    "Net Effective Rent": 40.50,
    "Transaction SQFT": 28000,
    "Execution Date": "2025-02-14",
    "Transaction Type": "Expansion"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 46.00,
    "Net Effective Rent": 41.40,
    "Transaction SQFT": 32000,
    "Execution Date": "2025-07-05",
    "Transaction Type": "New Lease"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "River North",
    "Space Type": "Office",
    "Building Class": "B",
    "Property Type": "Office",
    "Starting Rent": 34.00,
    "Net Effective Rent": 30.50,
    "Transaction SQFT": 15000,
    "Execution Date": "2025-04-20",
    "Transaction Type": "Relet"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Quarterly aggregation uses DuckDB DATE_TRUNC('quarter', "Execution Date") for grouping
- YoY calculation compares same quarter across years — handle partial quarters at series edges
