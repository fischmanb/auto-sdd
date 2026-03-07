# F-018: Lease Expiration Calendar

**Category**: Portfolio & Underwriting
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Visual calendar or timeline showing lease expirations by month/quarter for a portfolio, with bar height representing expiring SQFT. Lets asset managers see rollover risk concentration — months where multiple large leases expire simultaneously — and plan retention or re-leasing campaigns accordingly.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Stacked bar chart with X-axis = month or quarter, Y-axis = expiring Transaction SQFT
- [ ] Bars color-segmented by Tenant Name or Property Type (user toggle)
- [ ] Time horizon selector: 1Y, 3Y, 5Y forward from today
- [ ] Clicking a bar shows list of expiring leases in that period with Tenant Name, SQFT, and Starting Rent
- [ ] Summary: total expiring SQFT in selected horizon, percentage of portfolio

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

// 5+ records using exact CSV column names — spread across future expiration dates
const MOCK_RECORDS = [
  {
    "Tenant Name": "Amazon.com Services",
    "Market": "Seattle",
    "Submarket": "South Lake Union",
    "Street Address": "410 Terry Ave N",
    "Property Type": "Office",
    "Building Class": "A",
    "Transaction SQFT": 180000,
    "Starting Rent": 52.00,
    "Commencement Date": "2019-06-01",
    "Expiration Date": "2026-05-31"
  },
  {
    "Tenant Name": "T-Mobile US",
    "Market": "Seattle",
    "Submarket": "Bellevue CBD",
    "Street Address": "12920 SE 38th St",
    "Property Type": "Office",
    "Building Class": "A",
    "Transaction SQFT": 95000,
    "Starting Rent": 48.00,
    "Commencement Date": "2020-03-01",
    "Expiration Date": "2027-02-28"
  },
  {
    "Tenant Name": "Expedia Group",
    "Market": "Seattle",
    "Submarket": "Interbay",
    "Street Address": "1111 Expedia Group Way W",
    "Property Type": "Office",
    "Building Class": "A",
    "Transaction SQFT": 220000,
    "Starting Rent": 45.00,
    "Commencement Date": "2021-01-15",
    "Expiration Date": "2028-01-14"
  },
  {
    "Tenant Name": "Nordstrom Inc",
    "Market": "Seattle",
    "Submarket": "Downtown Seattle",
    "Street Address": "1501 5th Ave",
    "Property Type": "Retail",
    "Building Class": "A",
    "Transaction SQFT": 68000,
    "Starting Rent": 62.00,
    "Commencement Date": "2018-09-01",
    "Expiration Date": "2026-08-31"
  },
  {
    "Tenant Name": "Zillow Group",
    "Market": "Seattle",
    "Submarket": "South Lake Union",
    "Street Address": "1301 2nd Ave",
    "Property Type": "Office",
    "Building Class": "A",
    "Transaction SQFT": 110000,
    "Starting Rent": 50.00,
    "Commencement Date": "2020-07-01",
    "Expiration Date": "2027-06-30"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Expiration Date is the grouping key — DATE_TRUNC to month or quarter depending on view granularity
- Leases with null Expiration Date excluded from calendar view
