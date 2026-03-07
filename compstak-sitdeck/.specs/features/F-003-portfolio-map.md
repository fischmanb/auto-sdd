# F-003: Portfolio Map

**Category**: Map
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Map view displaying a user-selected portfolio of properties with color-coded markers indicating performance metrics like occupancy or rent growth. Allows CRE professionals to see their entire portfolio's geographic distribution at a glance and identify underperforming assets by location.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] User can select/deselect properties to define a portfolio subset
- [ ] Markers color-coded by a selectable metric: Starting Rent, Transaction SQFT, or Cap Rate
- [ ] Summary bar shows portfolio totals: property count, total SQFT, average rent
- [ ] Clicking a marker shows property details with latest lease and sale data

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

// 5+ records using exact CSV column names — mixed lease and sale data
const MOCK_RECORDS = [
  {
    "Market": "Boston",
    "Submarket": "Back Bay",
    "Street Address": "200 Clarendon St",
    "City": "Boston",
    "State": "MA",
    "Geo Point": "42.3490,-71.0770",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 72.00,
    "Transaction SQFT": 38000,
    "Execution Date": "2025-09-01",
    "Lease Type": "Full Service"
  },
  {
    "Market": "Washington DC",
    "Submarket": "East End",
    "Street Address": "1201 New York Ave NW",
    "City": "Washington",
    "State": "DC",
    "Geo Point": "38.9010,-77.0280",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 58.50,
    "Transaction SQFT": 25000,
    "Execution Date": "2025-10-15",
    "Lease Type": "Full Service"
  },
  {
    "Market": "Atlanta",
    "Submarket": "Buckhead",
    "Street Address": "3344 Peachtree Rd NE",
    "City": "Atlanta",
    "State": "GA",
    "Geo Point": "33.8440,-84.3620",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 142000000,
    "Sale Price (PSF)": 380.00,
    "Cap Rate": 6.2,
    "Sale Date": "2025-08-10"
  },
  {
    "Market": "Seattle",
    "Submarket": "South Lake Union",
    "Street Address": "400 Fairview Ave N",
    "City": "Seattle",
    "State": "WA",
    "Geo Point": "47.6260,-122.3330",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 48.00,
    "Transaction SQFT": 55000,
    "Execution Date": "2025-11-20",
    "Lease Type": "NNN"
  },
  {
    "Market": "Denver",
    "Submarket": "LoDo",
    "Street Address": "1515 Wynkoop St",
    "City": "Denver",
    "State": "CO",
    "Geo Point": "39.7530,-105.0000",
    "Building Class": "B",
    "Property Type": "Office",
    "Total Sale Price": 67500000,
    "Sale Price (PSF)": 295.00,
    "Cap Rate": 6.8,
    "Sale Date": "2025-07-22"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Portfolio selection state persisted in widget config — not in CSV data
- Lease and sale records joined by Street Address + City + State for property-level view
