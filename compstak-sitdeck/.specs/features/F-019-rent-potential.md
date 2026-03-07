# F-019: Rent Potential

**Category**: Portfolio & Underwriting
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Compares in-place rents (Current Rent) against current market rents (from Rent Optimizer F-004) to identify mark-to-market upside or downside across a portfolio. Shows which leases are below market (upside at renewal) and which are above market (risk of tenant departure), enabling strategic lease management.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Table columns: Tenant Name, Street Address, Submarket, Transaction SQFT, Current Rent, Market Rent (from comps), delta ($), delta (%), Expiration Date
- [ ] Color-coded delta: green = below market (upside), red = above market (risk)
- [ ] Summary bar: total portfolio SQFT, aggregate rent gap ($), weighted average delta (%)
- [ ] Sortable by delta % to prioritize largest mark-to-market opportunities

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
    "Tenant Name": "Accenture LLP",
    "Market": "Boston",
    "Submarket": "Back Bay",
    "Street Address": "800 Boylston St",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 42000,
    "Current Rent": 65.00,
    "Starting Rent": 58.00,
    "Expiration Date": "2028-03-31",
    "Transaction Type": "Renewal"
  },
  {
    "Tenant Name": "Putnam Investments",
    "Market": "Boston",
    "Submarket": "Financial District",
    "Street Address": "100 Federal St",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 85000,
    "Current Rent": 52.00,
    "Starting Rent": 48.00,
    "Expiration Date": "2027-06-30",
    "Transaction Type": "Renewal"
  },
  {
    "Tenant Name": "Liberty Mutual",
    "Market": "Boston",
    "Submarket": "Back Bay",
    "Street Address": "175 Berkeley St",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 200000,
    "Current Rent": 70.00,
    "Starting Rent": 62.00,
    "Expiration Date": "2030-12-31",
    "Transaction Type": "Expansion"
  },
  {
    "Tenant Name": "Wayfair Inc",
    "Market": "Boston",
    "Submarket": "Back Bay",
    "Street Address": "4 Copley Place",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 110000,
    "Current Rent": 55.00,
    "Starting Rent": 52.00,
    "Expiration Date": "2026-09-30",
    "Transaction Type": "New Lease"
  },
  {
    "Tenant Name": "Fidelity Investments",
    "Market": "Boston",
    "Submarket": "Financial District",
    "Street Address": "245 Summer St",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 150000,
    "Current Rent": 48.00,
    "Starting Rent": 44.00,
    "Expiration Date": "2029-05-31",
    "Transaction Type": "Renewal"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Current Rent column may be null — exclude records with null Current Rent from this analysis
- Market rent derived from F-004 Rent Optimizer comps for same submarket/class/type — cross-widget data dependency
