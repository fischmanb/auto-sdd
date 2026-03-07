# F-009: Market Overview

**Category**: Market Intelligence
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Dashboard-style summary widget presenting key market metrics at a glance: average rent, vacancy proxy, transaction volume, average cap rate, and YoY changes. Serves as the primary market intelligence landing widget that other analytical widgets reference for context.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] KPI cards display: average Starting Rent, total Transaction SQFT, deal count, average Cap Rate (from sales), and average Sale Price (PSF)
- [ ] Each KPI shows trailing-12-month value and YoY % change with up/down indicator
- [ ] Date range selector defaults to trailing 12 months with custom range option
- [ ] Mini sparkline chart beneath each KPI showing quarterly trend

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
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Uptown/Turtle Creek",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Starting Rent": 38.75,
    "Transaction SQFT": 15000,
    "Execution Date": "2025-08-22",
    "Transaction Type": "New Lease",
    "Lease Type": "Full Service"
  },
  {
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Las Colinas",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Starting Rent": 32.00,
    "Transaction SQFT": 42000,
    "Execution Date": "2025-05-10",
    "Transaction Type": "Renewal",
    "Lease Type": "NNN"
  },
  {
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Richardson/Plano",
    "Building Class": "B",
    "Property Type": "Office",
    "Space Type": "Office",
    "Starting Rent": 26.50,
    "Transaction SQFT": 20000,
    "Execution Date": "2025-03-18",
    "Transaction Type": "New Lease",
    "Lease Type": "Modified Gross"
  },
  {
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Uptown/Turtle Creek",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 125000000,
    "Sale Price (PSF)": 345.00,
    "Cap Rate": 5.9,
    "NOI": 7375000,
    "Sale Date": "2025-06-15",
    "Transaction SQFT": 362000
  },
  {
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Las Colinas",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 88000000,
    "Sale Price (PSF)": 280.00,
    "Cap Rate": 6.5,
    "NOI": 5720000,
    "Sale Date": "2025-09-01",
    "Transaction SQFT": 314000
  },
  {
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Far North Dallas",
    "Building Class": "B",
    "Property Type": "Industrial",
    "Total Sale Price": 42000000,
    "Sale Price (PSF)": 155.00,
    "Cap Rate": 7.1,
    "NOI": 2982000,
    "Sale Date": "2025-07-20",
    "Transaction SQFT": 271000
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- YoY calculations require querying two 12-month windows: current and prior year same period
- Cap Rate and Sale Price (PSF) sourced from sales CSV; Starting Rent and Transaction SQFT from leases CSV
