# F-016: Terminated Lease Monitor

**Category**: Tenant & Property
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Monitors leases that have recently expired or are approaching expiration, flagging spaces that will become or have become vacant. Critical for landlord reps tracking upcoming vacancy exposure and tenant rep brokers identifying relocation opportunities for displaced tenants.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Configurable expiration window: "expired in last N months" and "expiring in next N months"
- [ ] Table columns: Tenant Name, Street Address, Submarket, Transaction SQFT, Starting Rent, Expiration Date, days until/since expiration
- [ ] Color-coded status: red (already expired), orange (expiring within 6 months), yellow (expiring 6–12 months)
- [ ] Summary bar: total expiring SQFT, count of leases, average rent of expiring leases

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

// 5+ records using exact CSV column names — mix of expired and soon-to-expire
const MOCK_RECORDS = [
  {
    "Tenant Name": "Regus Management Group",
    "Market": "Phoenix",
    "Submarket": "Camelback Corridor",
    "Street Address": "2415 E Camelback Rd",
    "City": "Phoenix",
    "State": "AZ",
    "Space Type": "Office",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 18000,
    "Starting Rent": 28.00,
    "Commencement Date": "2019-04-01",
    "Expiration Date": "2025-03-31",
    "Transaction Type": "New Lease"
  },
  {
    "Tenant Name": "Allstate Insurance",
    "Market": "Phoenix",
    "Submarket": "Tempe",
    "Street Address": "1 W Washington St",
    "City": "Tempe",
    "State": "AZ",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 42000,
    "Starting Rent": 32.00,
    "Commencement Date": "2018-07-01",
    "Expiration Date": "2026-06-30",
    "Transaction Type": "Renewal"
  },
  {
    "Tenant Name": "Banner Health",
    "Market": "Phoenix",
    "Submarket": "Scottsdale",
    "Street Address": "9201 E Mountain View Rd",
    "City": "Scottsdale",
    "State": "AZ",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 65000,
    "Starting Rent": 35.00,
    "Commencement Date": "2020-01-15",
    "Expiration Date": "2026-01-14",
    "Transaction Type": "Expansion"
  },
  {
    "Tenant Name": "Insight Direct",
    "Market": "Phoenix",
    "Submarket": "Chandler/Gilbert",
    "Street Address": "6820 S Harl Ave",
    "City": "Chandler",
    "State": "AZ",
    "Space Type": "Office",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 30000,
    "Starting Rent": 24.00,
    "Commencement Date": "2020-06-01",
    "Expiration Date": "2025-05-31",
    "Transaction Type": "New Lease"
  },
  {
    "Tenant Name": "Desert Financial Credit Union",
    "Market": "Phoenix",
    "Submarket": "CBD",
    "Street Address": "100 N 15th Ave",
    "City": "Phoenix",
    "State": "AZ",
    "Space Type": "Office",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 22000,
    "Starting Rent": 26.00,
    "Commencement Date": "2019-09-01",
    "Expiration Date": "2026-08-31",
    "Transaction Type": "Renewal"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Expiration Date can be null — exclude null records from this widget entirely
- Days calculation: DATEDIFF('day', CURRENT_DATE, "Expiration Date") — negative = already expired
