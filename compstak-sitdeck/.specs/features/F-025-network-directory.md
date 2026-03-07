# F-025: Network Directory

**Category**: Broker & Network
**Phase**: 1
**Data Source**: Leases
**Status**: Planned

## Description

Searchable directory of all brokers and brokerage firms extracted from lease transaction data, with contact-level detail and transaction history summary. Helps CRE professionals find and vet potential co-brokers, identify who controls specific buildings or tenant relationships, and build referral networks.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Free-text search input for broker name or firm name
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Space Type filter populated from MOCK_SPACE_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Directory card shows: Broker Name, Firm, primary Market, deal count, total SQFT, most recent transaction date
- [ ] Expandable card detail: list of recent transactions for that broker
- [ ] Alphabetical and by-volume sort options
- [ ] Distinct broker count and firm count displayed in summary bar

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

// 5+ records using exact CSV column names — diverse brokers and firms
const MOCK_RECORDS = [
  {
    "Market": "Denver",
    "Submarket": "LoDo",
    "Street Address": "1515 Wynkoop St",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 28000,
    "Starting Rent": 38.00,
    "Execution Date": "2025-10-15",
    "Landlord Brokerage Firms": "CBRE",
    "Landlord Brokers": "Mark Stevens",
    "Tenant Brokerage Firms": "Newmark",
    "Tenant Brokers": "Amy Carter"
  },
  {
    "Market": "Denver",
    "Submarket": "Cherry Creek",
    "Street Address": "3003 E 3rd Ave",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 15000,
    "Starting Rent": 42.00,
    "Execution Date": "2025-09-08",
    "Landlord Brokerage Firms": "JLL",
    "Landlord Brokers": "Chris Reynolds",
    "Tenant Brokerage Firms": "Cushman & Wakefield",
    "Tenant Brokers": "Laura Diaz"
  },
  {
    "Market": "Denver",
    "Submarket": "DTC/Greenwood Village",
    "Street Address": "6300 S Syracuse Way",
    "Space Type": "Office",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 22000,
    "Starting Rent": 28.00,
    "Execution Date": "2025-08-20",
    "Landlord Brokerage Firms": "Cushman & Wakefield",
    "Landlord Brokers": "Mark Stevens",
    "Tenant Brokerage Firms": "CBRE",
    "Tenant Brokers": "Jason Park"
  },
  {
    "Market": "Denver",
    "Submarket": "RiNo",
    "Street Address": "3500 Blake St",
    "Space Type": "Flex/R&D",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 12000,
    "Starting Rent": 32.00,
    "Execution Date": "2025-07-05",
    "Landlord Brokerage Firms": "Newmark",
    "Landlord Brokers": "Amy Carter",
    "Tenant Brokerage Firms": "JLL",
    "Tenant Brokers": "Chris Reynolds"
  },
  {
    "Market": "Denver",
    "Submarket": "CBD",
    "Street Address": "1801 California St",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 35000,
    "Starting Rent": 36.00,
    "Execution Date": "2025-06-12",
    "Landlord Brokerage Firms": "CBRE",
    "Landlord Brokers": "Mark Stevens",
    "Tenant Brokerage Firms": "Savills",
    "Tenant Brokers": "Rachel Green"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Broker names extracted from both Landlord Brokers and Tenant Brokers columns — deduplicate by name
- Firm association maintained by pairing broker name position with firm name position in comma-separated lists
