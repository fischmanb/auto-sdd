# F-012: Deal Activity Heatmap

**Category**: Deal Intelligence
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Geographic heatmap overlaying transaction density on a map, with intensity representing deal volume or total SQFT transacted. Unlike the Market Map (F-002) which shows submarket-level choropleth shading, this widget uses point-based heat rendering at the individual transaction level for granular spatial patterns.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Heatmap intensity driven by selectable metric: transaction count, Transaction SQFT, or Starting Rent
- [ ] Date range filter limits transactions included in heatmap (Execution Date for leases, Sale Date for sales)
- [ ] Toggle between lease-only, sale-only, or combined heatmap layers
- [ ] Heat radius and opacity configurable via widget settings
- [ ] Legend shows intensity scale mapping color to metric range

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

// 5+ records using exact CSV column names — with Geo Point for heatmap plotting
const MOCK_RECORDS = [
  {
    "Market": "Los Angeles - Orange - Inland",
    "Submarket": "West Los Angeles",
    "Geo Point": "34.0490,-118.4695",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 22000,
    "Starting Rent": 54.00,
    "Execution Date": "2025-11-01"
  },
  {
    "Market": "Los Angeles - Orange - Inland",
    "Submarket": "Santa Monica",
    "Geo Point": "34.0195,-118.4912",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 18000,
    "Starting Rent": 66.00,
    "Execution Date": "2025-10-15"
  },
  {
    "Market": "Los Angeles - Orange - Inland",
    "Submarket": "Downtown Los Angeles",
    "Geo Point": "34.0522,-118.2437",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 220000000,
    "Sale Price (PSF)": 410.00,
    "Cap Rate": 5.3,
    "Sale Date": "2025-09-05",
    "Transaction SQFT": 536000
  },
  {
    "Market": "Los Angeles - Orange - Inland",
    "Submarket": "El Segundo/Beach Cities",
    "Geo Point": "33.9192,-118.4165",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 35000,
    "Starting Rent": 42.00,
    "Execution Date": "2025-08-20"
  },
  {
    "Market": "Los Angeles - Orange - Inland",
    "Submarket": "Burbank/Glendale/Pasadena",
    "Geo Point": "34.1808,-118.3090",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 28000,
    "Starting Rent": 38.50,
    "Execution Date": "2025-07-12"
  },
  {
    "Market": "Los Angeles - Orange - Inland",
    "Submarket": "Irvine",
    "Geo Point": "33.6846,-117.8265",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 95000000,
    "Sale Price (PSF)": 320.00,
    "Cap Rate": 5.8,
    "Sale Date": "2025-06-25",
    "Transaction SQFT": 297000
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Geo Point column contains "lat,lng" string — split on comma for heatmap coordinates
- Properties CSV uses separate LATITUDE and LONGITUDE columns — normalize at query layer if joined
