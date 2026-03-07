# F-007: Vacant Space Pricer

**Category**: Rent & Pricing
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Estimates market rent for a specific vacant space by matching its attributes against comparable lease transactions. Unlike the Rent Optimizer (F-004) which provides market-level recommendations, this widget targets a single address and floor, factoring in building-specific characteristics like class, size, and asking rent to produce a granular pricing estimate.

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
- [ ] User inputs target address, floor, and available SQFT for the vacant space
- [ ] Widget queries comps within same submarket matching building class and space type
- [ ] Output shows estimated Starting Rent range, comparable Asking Rent average, and suggested TI Value / Work Value range
- [ ] Comp radius selector: same submarket only, or expand to adjacent submarkets

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
    "Street Address": "200 Park Ave",
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 35000,
    "Starting Rent": 85.00,
    "Asking Rent": 92.00,
    "Net Effective Rent": 77.50,
    "TI Value / Work Value": 90.00,
    "Lease Term": 120,
    "Free Rent": 12,
    "Execution Date": "2025-08-15",
    "Lease Type": "Full Service",
    "Transaction Type": "New Lease"
  },
  {
    "Street Address": "299 Park Ave",
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 28000,
    "Starting Rent": 81.00,
    "Asking Rent": 88.00,
    "Net Effective Rent": 73.00,
    "TI Value / Work Value": 80.00,
    "Lease Term": 84,
    "Free Rent": 8,
    "Execution Date": "2025-09-22",
    "Lease Type": "Full Service",
    "Transaction Type": "Renewal"
  },
  {
    "Street Address": "345 Park Ave",
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 50000,
    "Starting Rent": 92.00,
    "Asking Rent": 100.00,
    "Net Effective Rent": 84.50,
    "TI Value / Work Value": 100.00,
    "Lease Term": 144,
    "Free Rent": 15,
    "Execution Date": "2025-06-30",
    "Lease Type": "Full Service",
    "Transaction Type": "New Lease"
  },
  {
    "Street Address": "277 Park Ave",
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 22000,
    "Starting Rent": 79.00,
    "Asking Rent": 85.00,
    "Net Effective Rent": 71.00,
    "TI Value / Work Value": 75.00,
    "Lease Term": 72,
    "Free Rent": 6,
    "Execution Date": "2025-10-10",
    "Lease Type": "Full Service",
    "Transaction Type": "Expansion"
  },
  {
    "Street Address": "399 Park Ave",
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 40000,
    "Starting Rent": 87.50,
    "Asking Rent": 95.00,
    "Net Effective Rent": 80.00,
    "TI Value / Work Value": 88.00,
    "Lease Term": 108,
    "Free Rent": 10,
    "Execution Date": "2025-07-18",
    "Lease Type": "Full Service",
    "Transaction Type": "New Lease"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Asking Rent column may have nulls in CSV — widget should display "N/A" and exclude from averages when null
- Adjacent submarket expansion requires a submarket adjacency lookup — stub with same-submarket only for Phase 1
