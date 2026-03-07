# F-023: Broker Rankings

**Category**: Broker & Network
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Individual broker leaderboard ranking named brokers (not firms) by transaction volume. While League Tables (F-022) rank firms, this widget ranks individual Landlord Brokers and Tenant Brokers, helping clients identify top-producing agents and enabling brokers to track their own competitive standing.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Toggle between Landlord Brokers and Tenant Brokers rankings
- [ ] Table columns: Rank, Broker Name, Firm, deal count, total Transaction SQFT, average Starting Rent
- [ ] Date range filter with presets: trailing 12M, trailing 24M, YTD, custom
- [ ] Broker name search input for finding specific individuals
- [ ] Top 50 brokers shown by default with "Show more" pagination

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

// 5+ records using exact CSV column names — with individual broker names
const MOCK_RECORDS = [
  {
    "Market": "Washington DC",
    "Submarket": "East End",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 55000,
    "Starting Rent": 58.50,
    "Execution Date": "2025-10-15",
    "Landlord Brokerage Firms": "JLL",
    "Landlord Brokers": "Robert Anderson",
    "Tenant Brokerage Firms": "CBRE",
    "Tenant Brokers": "Jessica Martinez"
  },
  {
    "Market": "Washington DC",
    "Submarket": "West End",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 38000,
    "Starting Rent": 62.00,
    "Execution Date": "2025-09-20",
    "Landlord Brokerage Firms": "Cushman & Wakefield",
    "Landlord Brokers": "Michael Thompson",
    "Tenant Brokerage Firms": "Newmark",
    "Tenant Brokers": "Karen White"
  },
  {
    "Market": "Washington DC",
    "Submarket": "NoMa/H Street",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 72000,
    "Starting Rent": 52.00,
    "Execution Date": "2025-08-05",
    "Landlord Brokerage Firms": "CBRE",
    "Landlord Brokers": "Robert Anderson",
    "Tenant Brokerage Firms": "JLL",
    "Tenant Brokers": "Daniel Kim"
  },
  {
    "Market": "Washington DC",
    "Submarket": "Capitol Hill",
    "Building Class": "B",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 15000,
    "Starting Rent": 48.00,
    "Execution Date": "2025-07-18",
    "Landlord Brokerage Firms": "Savills",
    "Landlord Brokers": "Patricia Clark",
    "Tenant Brokerage Firms": "Cushman & Wakefield",
    "Tenant Brokers": "Jessica Martinez"
  },
  {
    "Market": "Washington DC",
    "Submarket": "Tysons Corner",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Transaction SQFT": 48000,
    "Starting Rent": 45.00,
    "Execution Date": "2025-06-22",
    "Landlord Brokerage Firms": "JLL",
    "Landlord Brokers": "Robert Anderson",
    "Tenant Brokerage Firms": "CBRE",
    "Tenant Brokers": "Steve Garcia"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Broker columns may contain multiple names comma-separated — split and attribute each deal to each named broker
- Firm association derived by matching broker name position to brokerage firm name position in the comma-separated lists
