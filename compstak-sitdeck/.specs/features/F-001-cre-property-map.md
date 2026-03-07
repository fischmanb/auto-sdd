# F-001: CRE Property Map

**Category**: Map
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Interactive map displaying commercial real estate properties with lease and sales transaction data plotted as markers. Users can click any property to see summary metrics (rent, cap rate, building class) and drill into transaction history. This is the foundational spatial widget that other map widgets extend.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Map renders property markers from both leases and sales CSVs using Geo Point coordinates (leases/sales) and LATITUDE/LONGITUDE (properties CSV)
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Clicking a marker opens a popover with property address, building class, property type, and latest transaction summary
- [ ] Map supports zoom and pan with cluster aggregation at low zoom levels
- [ ] Color-coded markers distinguish lease vs. sale transactions

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
    "Street Address": "390 Madison Ave",
    "City": "New York",
    "State": "NY",
    "Geo Point": "40.7580,-73.9755",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 82.50,
    "Transaction SQFT": 45000,
    "Execution Date": "2025-09-15"
  },
  {
    "Market": "Los Angeles - Orange - Inland",
    "Submarket": "West Los Angeles",
    "Street Address": "11601 Wilshire Blvd",
    "City": "Los Angeles",
    "State": "CA",
    "Geo Point": "34.0490,-118.4695",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 54.00,
    "Transaction SQFT": 22000,
    "Execution Date": "2025-11-01"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Street Address": "233 S Wacker Dr",
    "City": "Chicago",
    "State": "IL",
    "Geo Point": "41.8789,-87.6359",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 285000000,
    "Sale Price (PSF)": 425.00,
    "Cap Rate": 5.8,
    "Sale Date": "2025-10-20"
  },
  {
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Uptown/Turtle Creek",
    "Street Address": "2000 McKinney Ave",
    "City": "Dallas",
    "State": "TX",
    "Geo Point": "32.7950,-96.8010",
    "Building Class": "B",
    "Property Type": "Office",
    "Starting Rent": 38.75,
    "Transaction SQFT": 15000,
    "Execution Date": "2025-08-22"
  },
  {
    "Market": "Bay Area",
    "Submarket": "South of Market",
    "Street Address": "525 Market St",
    "City": "San Francisco",
    "State": "CA",
    "Geo Point": "37.7905,-122.3990",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 195000000,
    "Sale Price (PSF)": 612.00,
    "Cap Rate": 4.9,
    "Sale Date": "2025-12-05"
  },
  {
    "Market": "Miami - Ft. Lauderdale",
    "Submarket": "Brickell",
    "Street Address": "1395 Brickell Ave",
    "City": "Miami",
    "State": "FL",
    "Geo Point": "25.7590,-80.1910",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 62.00,
    "Transaction SQFT": 18500,
    "Execution Date": "2025-07-10"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Geo Point column contains "lat,lng" string — split on comma for map coordinates
- Properties CSV uses separate LATITUDE and LONGITUDE columns — normalize to common format at query layer
