# F-013: Tenant Records

**Category**: Tenant & Property
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Comprehensive lease history for a specific tenant across all markets, showing every recorded transaction. Lets landlord reps research a prospective tenant's leasing track record — size preferences, rent levels, lease terms, and geographic footprint — to prepare for negotiations.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Tenant Name search input with typeahead/autocomplete from lease data
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Transaction Type filter populated from MOCK_TRANSACTION_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Table columns: Street Address, Market, Submarket, Transaction SQFT, Starting Rent, Lease Term, Execution Date, Expiration Date, Transaction Type, Tenant Industry
- [ ] All columns sortable ascending/descending
- [ ] Summary row: total locations, total SQFT, average Starting Rent, average Lease Term
- [ ] Export to CSV button for the filtered result set

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

// 5+ records using exact CSV column names — same tenant across markets
const MOCK_RECORDS = [
  {
    "Tenant Name": "Deloitte LLP",
    "Tenant Industry": "Professional Services",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Street Address": "30 Rockefeller Plaza",
    "City": "New York",
    "State": "NY",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 120000,
    "Starting Rent": 88.00,
    "Lease Term": 180,
    "Execution Date": "2024-03-15",
    "Expiration Date": "2039-03-14",
    "Transaction Type": "Renewal",
    "Lease Type": "Full Service"
  },
  {
    "Tenant Name": "Deloitte LLP",
    "Tenant Industry": "Professional Services",
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Street Address": "111 S Wacker Dr",
    "City": "Chicago",
    "State": "IL",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 85000,
    "Starting Rent": 44.00,
    "Lease Term": 120,
    "Execution Date": "2023-08-20",
    "Expiration Date": "2033-08-19",
    "Transaction Type": "New Lease",
    "Lease Type": "Full Service"
  },
  {
    "Tenant Name": "Deloitte LLP",
    "Tenant Industry": "Professional Services",
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Uptown/Turtle Creek",
    "Street Address": "2200 Ross Ave",
    "City": "Dallas",
    "State": "TX",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 62000,
    "Starting Rent": 38.00,
    "Lease Term": 84,
    "Execution Date": "2024-11-01",
    "Expiration Date": "2031-10-31",
    "Transaction Type": "Expansion",
    "Lease Type": "NNN"
  },
  {
    "Tenant Name": "Deloitte LLP",
    "Tenant Industry": "Professional Services",
    "Market": "Bay Area",
    "Submarket": "Downtown San Jose",
    "Street Address": "225 W Santa Clara St",
    "City": "San Jose",
    "State": "CA",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 45000,
    "Starting Rent": 56.00,
    "Lease Term": 60,
    "Execution Date": "2025-02-10",
    "Expiration Date": "2030-02-09",
    "Transaction Type": "New Lease",
    "Lease Type": "Full Service"
  },
  {
    "Tenant Name": "Deloitte LLP",
    "Tenant Industry": "Professional Services",
    "Market": "Atlanta",
    "Submarket": "Midtown",
    "Street Address": "191 Peachtree St NE",
    "City": "Atlanta",
    "State": "GA",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 55000,
    "Starting Rent": 36.00,
    "Lease Term": 96,
    "Execution Date": "2024-06-15",
    "Expiration Date": "2032-06-14",
    "Transaction Type": "Renewal",
    "Lease Type": "Full Service"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Tenant Name search uses ILIKE pattern matching in DuckDB — autocomplete queries with debounce
- Tenant Industry column may be null — display "Unknown" when missing
