# F-020: Cap Rate Trends

**Category**: Portfolio & Underwriting
**Phase**: 1
**Data Source**: Sales
**Status**: Planned

## Description

Time-series chart tracking capitalization rate trends by market, property type, and building class over time. Essential for underwriters and investors to understand yield compression or expansion, informing acquisition pricing and disposition timing decisions.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Line chart: X-axis = Sale Quarter, Y-axis = average Cap Rate
- [ ] Multiple series support: overlay different property types or building classes on same chart
- [ ] Date range selector with presets: 1Y, 3Y, 5Y, and custom
- [ ] Hover tooltip: quarter, average Cap Rate, transaction count, average Sale Price (PSF)
- [ ] Trend indicator showing current quarter vs. trailing average

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

// 5+ records using exact CSV column names — sales spread across quarters
const MOCK_RECORDS = [
  {
    "Market": "Miami - Ft. Lauderdale",
    "Submarket": "Brickell",
    "Street Address": "1395 Brickell Ave",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 245000000,
    "Sale Price (PSF)": 520.00,
    "Cap Rate": 4.8,
    "NOI": 11760000,
    "Sale Date": "2024-03-15",
    "Sale Quarter": "Q1 2024",
    "Transaction SQFT": 471000
  },
  {
    "Market": "Miami - Ft. Lauderdale",
    "Submarket": "Brickell",
    "Street Address": "701 Brickell Ave",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 185000000,
    "Sale Price (PSF)": 475.00,
    "Cap Rate": 5.1,
    "NOI": 9435000,
    "Sale Date": "2024-07-20",
    "Sale Quarter": "Q3 2024",
    "Transaction SQFT": 389000
  },
  {
    "Market": "Miami - Ft. Lauderdale",
    "Submarket": "Coconut Grove",
    "Street Address": "2600 S Douglas Rd",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 92000000,
    "Sale Price (PSF)": 380.00,
    "Cap Rate": 5.5,
    "NOI": 5060000,
    "Sale Date": "2024-11-05",
    "Sale Quarter": "Q4 2024",
    "Transaction SQFT": 242000
  },
  {
    "Market": "Miami - Ft. Lauderdale",
    "Submarket": "Coral Gables",
    "Street Address": "396 Alhambra Cir",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 135000000,
    "Sale Price (PSF)": 440.00,
    "Cap Rate": 5.0,
    "NOI": 6750000,
    "Sale Date": "2025-02-10",
    "Sale Quarter": "Q1 2025",
    "Transaction SQFT": 307000
  },
  {
    "Market": "Miami - Ft. Lauderdale",
    "Submarket": "Fort Lauderdale CBD",
    "Street Address": "450 E Las Olas Blvd",
    "Building Class": "A",
    "Property Type": "Office",
    "Total Sale Price": 78000000,
    "Sale Price (PSF)": 350.00,
    "Cap Rate": 5.8,
    "NOI": 4524000,
    "Sale Date": "2025-06-18",
    "Sale Quarter": "Q2 2025",
    "Transaction SQFT": 223000
  },
  {
    "Market": "Miami - Ft. Lauderdale",
    "Submarket": "Doral",
    "Street Address": "8333 NW 53rd St",
    "Building Class": "B",
    "Property Type": "Industrial",
    "Total Sale Price": 55000000,
    "Sale Price (PSF)": 195.00,
    "Cap Rate": 6.2,
    "NOI": 3410000,
    "Sale Date": "2025-09-25",
    "Sale Quarter": "Q3 2025",
    "Transaction SQFT": 282000
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Cap Rate can be null in sales CSV — exclude nulls from trend calculations
- Sale Quarter column provides pre-formatted quarter string; alternatively derive from Sale Date using DATE_TRUNC
