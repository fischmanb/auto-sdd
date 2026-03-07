# F-024: Broker Activity Feed

**Category**: Broker & Network
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Real-time-style feed showing recent transactions attributed to a specific broker or brokerage firm, presented as a chronological activity stream. Enables brokers to track competitor activity, monitor team production, and build pitchbook evidence of market expertise.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Broker or firm name search input with typeahead from lease/sale brokerage columns
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Feed items show: date, transaction type (lease/sale), address, tenant/buyer name, SQFT, rent/price, broker role (landlord rep or tenant rep)
- [ ] Chronological ordering with most recent first
- [ ] Toggle between Landlord Brokers and Tenant Brokers scope
- [ ] Summary stats: total deals, total SQFT, trailing 12-month activity for the searched broker

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

// 5+ records using exact CSV column names — all for one broker
const MOCK_RECORDS = [
  {
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Street Address": "233 S Wacker Dr",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Tenant Name": "Sidley Austin LLP",
    "Transaction SQFT": 65000,
    "Starting Rent": 48.00,
    "Execution Date": "2025-11-10",
    "Transaction Type": "Renewal",
    "Landlord Brokerage Firms": "CBRE",
    "Landlord Brokers": "James Mitchell",
    "Tenant Brokerage Firms": "JLL",
    "Tenant Brokers": "Sarah O'Brien"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "West Loop",
    "Street Address": "150 N Riverside Plaza",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Tenant Name": "Kraft Heinz Co",
    "Transaction SQFT": 42000,
    "Starting Rent": 44.00,
    "Execution Date": "2025-09-28",
    "Transaction Type": "New Lease",
    "Landlord Brokerage Firms": "Cushman & Wakefield",
    "Landlord Brokers": "Nancy Price",
    "Tenant Brokerage Firms": "CBRE",
    "Tenant Brokers": "James Mitchell"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "River North",
    "Street Address": "321 N Clark St",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Tenant Name": "Salesforce Inc",
    "Transaction SQFT": 88000,
    "Starting Rent": 46.00,
    "Execution Date": "2025-08-15",
    "Transaction Type": "Expansion",
    "Landlord Brokerage Firms": "CBRE",
    "Landlord Brokers": "James Mitchell",
    "Tenant Brokerage Firms": "Savills",
    "Tenant Brokers": "Kevin Walsh"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "Fulton Market",
    "Street Address": "811 W Fulton Market",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Tenant Name": "McDonald's Corp",
    "Transaction SQFT": 35000,
    "Starting Rent": 52.00,
    "Execution Date": "2025-07-02",
    "Transaction Type": "New Lease",
    "Landlord Brokerage Firms": "CBRE",
    "Landlord Brokers": "James Mitchell",
    "Tenant Brokerage Firms": "Newmark",
    "Tenant Brokers": "Rebecca Owens"
  },
  {
    "Market": "Chicago Metro",
    "Submarket": "Chicago CBD",
    "Street Address": "10 S Dearborn St",
    "Building Class": "B",
    "Property Type": "Office",
    "Buyer": "Sterling Bay",
    "Seller": "Columbia Property Trust",
    "Total Sale Price": 145000000,
    "Sale Price (PSF)": 280.00,
    "Cap Rate": 6.5,
    "Sale Date": "2025-06-20",
    "Transaction SQFT": 518000
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Broker search uses ILIKE against both Landlord Brokers and Tenant Brokers columns
- Sales records do not have broker name fields — only Buyer/Seller; include in feed if firm name matches
