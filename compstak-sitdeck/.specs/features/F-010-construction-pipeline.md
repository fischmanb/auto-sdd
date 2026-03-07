# F-010: Construction Pipeline

**Category**: Market Intelligence
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Tracks new construction and pre-lease activity within a market by analyzing pre-lease transaction types and recent commencement dates for new buildings. Helps CRE professionals anticipate future supply that will impact rents and vacancy, essential for market timing decisions.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Filters to Transaction Type = "Pre-lease" to identify new developments with leasing activity
- [ ] Table shows Building Name, Street Address, Submarket, Transaction SQFT, Starting Rent, Commencement Date, and Tenant Name
- [ ] Summary bar: total pre-lease SQFT, number of buildings, and average Starting Rent for pre-leases
- [ ] Sortable by Commencement Date to show upcoming deliveries first

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

// 5+ records using exact CSV column names — all Pre-lease transactions
const MOCK_RECORDS = [
  {
    "Market": "Austin",
    "Submarket": "CBD",
    "Building Name": "Block 71 Tower",
    "Street Address": "601 W 6th St",
    "City": "Austin",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 85000,
    "Starting Rent": 62.00,
    "Commencement Date": "2027-01-15",
    "Tenant Name": "TechCorp Inc",
    "Transaction Type": "Pre-lease",
    "Execution Date": "2025-09-10"
  },
  {
    "Market": "Austin",
    "Submarket": "Domain",
    "Building Name": "Domain Tower III",
    "Street Address": "11800 Domain Blvd",
    "City": "Austin",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 120000,
    "Starting Rent": 55.00,
    "Commencement Date": "2026-09-01",
    "Tenant Name": "Global Consulting Group",
    "Transaction Type": "Pre-lease",
    "Execution Date": "2025-06-20"
  },
  {
    "Market": "Austin",
    "Submarket": "East Austin",
    "Building Name": "Eastside Innovation Center",
    "Street Address": "2100 E 5th St",
    "City": "Austin",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Flex/R&D",
    "Transaction SQFT": 45000,
    "Starting Rent": 48.00,
    "Commencement Date": "2026-06-01",
    "Tenant Name": "BioGen Labs",
    "Transaction Type": "Pre-lease",
    "Execution Date": "2025-08-05"
  },
  {
    "Market": "Austin",
    "Submarket": "South Congress",
    "Building Name": "SoCo Place",
    "Street Address": "1400 S Congress Ave",
    "City": "Austin",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Mixed-Use",
    "Space Type": "Office",
    "Transaction SQFT": 65000,
    "Starting Rent": 58.00,
    "Commencement Date": "2027-03-01",
    "Tenant Name": "FinServ Holdings",
    "Transaction Type": "Pre-lease",
    "Execution Date": "2025-10-15"
  },
  {
    "Market": "Austin",
    "Submarket": "CBD",
    "Building Name": "Congress Gateway",
    "Street Address": "401 Congress Ave",
    "City": "Austin",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 95000,
    "Starting Rent": 65.00,
    "Commencement Date": "2026-11-15",
    "Tenant Name": "DataStream Analytics",
    "Transaction Type": "Pre-lease",
    "Execution Date": "2025-07-28"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Commencement Date may be null for some pre-lease records — display "TBD" and sort nulls last
- Building Name column can be null — fall back to Street Address when displaying
