# F-021: Income Projection

**Category**: Portfolio & Underwriting
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Projects future rental income for a portfolio by modeling lease expirations, assumed renewal rates, and market rent escalations. Outputs a year-by-year income forecast that underwriters use for DCF analysis and lending decisions. Combines in-place lease data with market rent assumptions.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Projection horizon input: 1–10 years (default 5)
- [ ] User-configurable assumptions: renewal probability (%), rent escalation rate (%), downtime between leases (months)
- [ ] Bar chart: X-axis = year, Y-axis = projected gross rental income
- [ ] Stacked bars show: in-place income (from current leases) vs. projected renewal/new lease income
- [ ] Table below chart showing year-by-year: in-place SQFT, expiring SQFT, projected rent, total income

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

// 5+ records using exact CSV column names — with expiration dates for projection
const MOCK_RECORDS = [
  {
    "Tenant Name": "Morgan Stanley",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Street Address": "1585 Broadway",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 180000,
    "Starting Rent": 88.00,
    "Current Rent": 92.00,
    "Commencement Date": "2020-01-01",
    "Expiration Date": "2030-12-31",
    "Lease Type": "Full Service"
  },
  {
    "Tenant Name": "Sullivan & Cromwell",
    "Market": "New York City",
    "Submarket": "Downtown Manhattan",
    "Street Address": "125 Broad St",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 120000,
    "Starting Rent": 65.00,
    "Current Rent": 72.00,
    "Commencement Date": "2018-06-01",
    "Expiration Date": "2028-05-31",
    "Lease Type": "Full Service"
  },
  {
    "Tenant Name": "Spotify USA",
    "Market": "New York City",
    "Submarket": "Hudson Yards",
    "Street Address": "4 World Trade Center",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 85000,
    "Starting Rent": 78.00,
    "Current Rent": 82.00,
    "Commencement Date": "2021-03-15",
    "Expiration Date": "2031-03-14",
    "Lease Type": "Full Service"
  },
  {
    "Tenant Name": "Cushman & Wakefield",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Street Address": "1290 Avenue of the Americas",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 55000,
    "Starting Rent": 72.00,
    "Current Rent": 75.00,
    "Commencement Date": "2022-09-01",
    "Expiration Date": "2029-08-31",
    "Lease Type": "Full Service"
  },
  {
    "Tenant Name": "Conde Nast",
    "Market": "New York City",
    "Submarket": "Hudson Yards",
    "Street Address": "1 World Trade Center",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 140000,
    "Starting Rent": 80.00,
    "Current Rent": 85.00,
    "Commencement Date": "2019-07-01",
    "Expiration Date": "2034-06-30",
    "Lease Type": "Full Service"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Income projection uses Current Rent × Transaction SQFT for in-place income; Starting Rent for market rate assumptions
- Renewal probability and escalation rate are client-side inputs — not from CSV data
