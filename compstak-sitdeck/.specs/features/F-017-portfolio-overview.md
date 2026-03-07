# F-017: Portfolio Overview

**Category**: Portfolio & Underwriting
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Aggregated dashboard showing portfolio-level KPIs across all properties in a user-defined portfolio: total SQFT, weighted average rent, occupancy proxy, total asset value from recent sales. Provides the executive summary that asset managers and portfolio strategists need for reporting and decision-making.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] KPI cards: total portfolio SQFT, weighted average Starting Rent (weighted by SQFT), total lease count, total estimated asset value (from Sale Price PSF × SQFT)
- [ ] Pie chart breakdown by Property Type showing SQFT distribution
- [ ] Bar chart showing top 10 properties by Transaction SQFT
- [ ] Date range filter for which lease/sale records are included

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

// 5+ records using exact CSV column names — mix of lease and sale
const MOCK_RECORDS = [
  {
    "Market": "Nashville",
    "Submarket": "CBD/SoBro",
    "Street Address": "501 Commerce St",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 48000,
    "Starting Rent": 42.00,
    "Execution Date": "2025-07-15",
    "Transaction Type": "New Lease",
    "Lease Type": "Full Service"
  },
  {
    "Market": "Nashville",
    "Submarket": "Gulch",
    "Street Address": "1222 Demonbreun St",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 32000,
    "Starting Rent": 46.00,
    "Execution Date": "2025-09-01",
    "Transaction Type": "Renewal",
    "Lease Type": "Full Service"
  },
  {
    "Market": "Nashville",
    "Submarket": "CBD/SoBro",
    "Street Address": "315 Deaderick St",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 180000000,
    "Sale Price (PSF)": 420.00,
    "Cap Rate": 5.4,
    "Sale Date": "2025-06-10",
    "Transaction SQFT": 428000
  },
  {
    "Market": "Charlotte",
    "Submarket": "Uptown",
    "Street Address": "201 S Tryon St",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 55000,
    "Starting Rent": 38.00,
    "Execution Date": "2025-08-20",
    "Transaction Type": "New Lease",
    "Lease Type": "Full Service"
  },
  {
    "Market": "Charlotte",
    "Submarket": "SouthPark",
    "Street Address": "6100 Fairview Rd",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 92000000,
    "Sale Price (PSF)": 310.00,
    "Cap Rate": 6.1,
    "Sale Date": "2025-10-05",
    "Transaction SQFT": 297000
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Weighted average rent: SUM("Starting Rent" × "Transaction SQFT") / SUM("Transaction SQFT")
- Asset value estimation uses most recent Sale Price (PSF) per property × total building SQFT
