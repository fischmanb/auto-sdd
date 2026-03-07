# F-014: Active Tenants

**Category**: Tenant & Property
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Lists all tenants with active (non-expired) leases in a selected market or building, showing current occupancy details. Landlords use this to understand the tenant mix at a property or across a submarket, identify anchor tenants, and spot upcoming lease expirations that create re-leasing risk or opportunity.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Filters to leases where Expiration Date > current date
- [ ] Table columns: Tenant Name, Tenant Industry, Street Address, Submarket, Transaction SQFT, Starting Rent, Commencement Date, Expiration Date
- [ ] Color-coded expiration urgency: red (< 12 months), yellow (12–24 months), green (> 24 months)
- [ ] Summary bar: total active tenants, total occupied SQFT, average remaining lease term

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

// 5+ records using exact CSV column names — all with future Expiration Dates
const MOCK_RECORDS = [
  {
    "Tenant Name": "JPMorgan Chase",
    "Tenant Industry": "Financial Services",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Street Address": "383 Madison Ave",
    "City": "New York",
    "State": "NY",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 250000,
    "Starting Rent": 92.00,
    "Commencement Date": "2020-01-01",
    "Expiration Date": "2035-12-31",
    "Transaction Type": "Renewal"
  },
  {
    "Tenant Name": "Kirkland & Ellis",
    "Tenant Industry": "Legal",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Street Address": "601 Lexington Ave",
    "City": "New York",
    "State": "NY",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 180000,
    "Starting Rent": 105.00,
    "Commencement Date": "2022-06-01",
    "Expiration Date": "2037-05-31",
    "Transaction Type": "New Lease"
  },
  {
    "Tenant Name": "WeWork",
    "Tenant Industry": "Real Estate",
    "Market": "New York City",
    "Submarket": "Midtown South",
    "Street Address": "115 Broadway",
    "City": "New York",
    "State": "NY",
    "Space Type": "Office",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 45000,
    "Starting Rent": 52.00,
    "Commencement Date": "2023-03-01",
    "Expiration Date": "2027-02-28",
    "Transaction Type": "New Lease"
  },
  {
    "Tenant Name": "Google LLC",
    "Tenant Industry": "Technology",
    "Market": "New York City",
    "Submarket": "Hudson Yards",
    "Street Address": "550 Washington St",
    "City": "New York",
    "State": "NY",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 320000,
    "Starting Rent": 78.00,
    "Commencement Date": "2021-09-01",
    "Expiration Date": "2036-08-31",
    "Transaction Type": "Expansion"
  },
  {
    "Tenant Name": "Citadel Securities",
    "Tenant Industry": "Financial Services",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Street Address": "425 Park Ave",
    "City": "New York",
    "State": "NY",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 95000,
    "Starting Rent": 115.00,
    "Commencement Date": "2024-01-15",
    "Expiration Date": "2039-01-14",
    "Transaction Type": "New Lease"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Active lease filter: WHERE "Expiration Date" > CURRENT_DATE — some records may have null Expiration Date, exclude those
- Remaining lease term calculated as DATEDIFF('month', CURRENT_DATE, "Expiration Date")
