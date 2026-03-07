# F-004: Rent Optimizer

**Category**: Rent & Pricing
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Calculates an optimized rent recommendation for a given space based on comparable lease transactions. Users specify property attributes (market, building class, space type, size) and the widget returns a recommended rent range with confidence intervals. This is the core pricing engine that F-005, F-006, and F-007 build upon.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Lease Type filter populated from MOCK_LEASE_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] User inputs target SQFT and the widget queries comparable leases within ±25% of that size
- [ ] Output displays recommended Starting Rent as a range (low / mid / high) with comp count
- [ ] Date range filter limits Execution Date of included comps (default: trailing 24 months)
- [ ] Results panel shows median, 25th percentile, and 75th percentile of Starting Rent

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
    "Net Effective Rent": 74.10,
    "Transaction SQFT": 45000,
    "Lease Term": 120,
    "Free Rent": 12,
    "TI Value / Work Value": 85.00,
    "Execution Date": "2025-09-15",
    "Lease Type": "Full Service",
    "Transaction Type": "New Lease"
  },
  {
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 78.00,
    "Net Effective Rent": 70.50,
    "Transaction SQFT": 38000,
    "Lease Term": 84,
    "Free Rent": 8,
    "TI Value / Work Value": 70.00,
    "Execution Date": "2025-07-22",
    "Lease Type": "Full Service",
    "Transaction Type": "Renewal"
  },
  {
    "Market": "New York City",
    "Submarket": "Midtown South",
    "Space Type": "Office",
    "Building Class": "B",
    "Property Type": "Office",
    "Starting Rent": 58.25,
    "Net Effective Rent": 52.00,
    "Transaction SQFT": 18000,
    "Lease Term": 60,
    "Free Rent": 6,
    "TI Value / Work Value": 45.00,
    "Execution Date": "2025-08-20",
    "Lease Type": "Full Service",
    "Transaction Type": "New Lease"
  },
  {
    "Market": "New York City",
    "Submarket": "Downtown Manhattan",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 64.00,
    "Net Effective Rent": 57.80,
    "Transaction SQFT": 52000,
    "Lease Term": 96,
    "Free Rent": 10,
    "TI Value / Work Value": 75.00,
    "Execution Date": "2025-10-01",
    "Lease Type": "Full Service",
    "Transaction Type": "New Lease"
  },
  {
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 88.00,
    "Net Effective Rent": 80.25,
    "Transaction SQFT": 42000,
    "Lease Term": 132,
    "Free Rent": 14,
    "TI Value / Work Value": 95.00,
    "Execution Date": "2025-06-10",
    "Lease Type": "Full Service",
    "Transaction Type": "Expansion"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Percentile calculations done in DuckDB using PERCENTILE_CONT aggregate function
- TI Value / Work Value and Free Rent columns used for Net Effective Rent derivation when NER is null
