# F-005: Underlying Comps

**Category**: Rent & Pricing
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Displays the individual lease comparables that fed into the Rent Optimizer (F-004) calculation. Presented as a sortable table so users can audit which transactions drove the rent recommendation, inspect outliers, and manually exclude records that should not influence pricing.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Transaction Type filter populated from MOCK_TRANSACTION_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Table columns: Street Address, Submarket, Building Class, Transaction SQFT, Starting Rent, Net Effective Rent, Lease Term, Execution Date, Transaction Type
- [ ] All columns sortable ascending/descending
- [ ] User can check/uncheck rows to exclude comps from Rent Optimizer calculation
- [ ] Excluded comps visually dimmed but remain in the table

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
    "Street Address": "390 Madison Ave",
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 42000,
    "Starting Rent": 88.00,
    "Net Effective Rent": 80.25,
    "Lease Term": 132,
    "Execution Date": "2025-06-10",
    "Transaction Type": "Expansion",
    "Lease Type": "Full Service"
  },
  {
    "Street Address": "1271 Avenue of the Americas",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 45000,
    "Starting Rent": 82.50,
    "Net Effective Rent": 74.10,
    "Lease Term": 120,
    "Execution Date": "2025-09-15",
    "Transaction Type": "New Lease",
    "Lease Type": "Full Service"
  },
  {
    "Street Address": "114 W 47th St",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 38000,
    "Starting Rent": 78.00,
    "Net Effective Rent": 70.50,
    "Lease Term": 84,
    "Execution Date": "2025-07-22",
    "Transaction Type": "Renewal",
    "Lease Type": "Full Service"
  },
  {
    "Street Address": "85 Broad St",
    "Market": "New York City",
    "Submarket": "Downtown Manhattan",
    "Building Class": "A",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 52000,
    "Starting Rent": 64.00,
    "Net Effective Rent": 57.80,
    "Lease Term": 96,
    "Execution Date": "2025-10-01",
    "Transaction Type": "New Lease",
    "Lease Type": "Full Service"
  },
  {
    "Street Address": "620 Eighth Ave",
    "Market": "New York City",
    "Submarket": "Penn Plaza/Garment",
    "Building Class": "B",
    "Space Type": "Office",
    "Property Type": "Office",
    "Transaction SQFT": 22000,
    "Starting Rent": 55.00,
    "Net Effective Rent": 49.00,
    "Lease Term": 72,
    "Execution Date": "2025-08-05",
    "Transaction Type": "Relet",
    "Lease Type": "Gross"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Comp exclusion state stored in widget memory — not persisted to CSV; syncs with F-004 via shared widget context
