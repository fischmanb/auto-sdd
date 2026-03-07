# F-022: League Tables

**Category**: Broker & Network
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Ranked leaderboard of brokerage firms by total transaction volume (SQFT or dollar amount) within a market and time period. The industry-standard way to measure brokerage market share — used by firms for competitive positioning and by clients when selecting representation.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Toggle between Landlord Brokerage Firms and Tenant Brokerage Firms rankings
- [ ] Ranking metric selector: total Transaction SQFT, deal count, or total dollar volume (Starting Rent × SQFT for leases, Total Sale Price for sales)
- [ ] Table columns: Rank, Firm Name, deal count, total SQFT, total dollar volume, market share %
- [ ] Date range filter with presets: trailing 12M, trailing 24M, YTD, custom
- [ ] Horizontal bar chart visualization alongside the ranked table

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

// 5+ records using exact CSV column names — with brokerage firm fields
const MOCK_RECORDS = [
  {
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 45000,
    "Starting Rent": 82.50,
    "Execution Date": "2025-09-15",
    "Landlord Brokerage Firms": "CBRE",
    "Landlord Brokers": "Mary Johnson",
    "Tenant Brokerage Firms": "JLL",
    "Tenant Brokers": "John Smith"
  },
  {
    "Market": "New York City",
    "Submarket": "Downtown Manhattan",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 32000,
    "Starting Rent": 64.00,
    "Execution Date": "2025-10-01",
    "Landlord Brokerage Firms": "Cushman & Wakefield",
    "Landlord Brokers": "Sarah Davis",
    "Tenant Brokerage Firms": "CBRE",
    "Tenant Brokers": "Mike Chen"
  },
  {
    "Market": "New York City",
    "Submarket": "Midtown South",
    "Building Class": "B",
    "Property Type": "Office",
    "Transaction SQFT": 18000,
    "Starting Rent": 58.25,
    "Execution Date": "2025-08-20",
    "Landlord Brokerage Firms": "Newmark",
    "Landlord Brokers": "Tom Wilson",
    "Tenant Brokerage Firms": "Savills",
    "Tenant Brokers": "Lisa Park"
  },
  {
    "Market": "New York City",
    "Submarket": "Grand Central",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 62000,
    "Starting Rent": 78.00,
    "Execution Date": "2025-07-30",
    "Landlord Brokerage Firms": "JLL",
    "Landlord Brokers": "David Lee",
    "Tenant Brokerage Firms": "Cushman & Wakefield",
    "Tenant Brokers": "Emily Rodriguez"
  },
  {
    "Market": "New York City",
    "Submarket": "Hudson Yards",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 105000,
    "Starting Rent": 95.00,
    "Execution Date": "2025-06-18",
    "Landlord Brokerage Firms": "CBRE",
    "Landlord Brokers": "Robert Brown",
    "Tenant Brokerage Firms": "JLL",
    "Tenant Brokers": "Amanda Taylor"
  },
  {
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Building Class": "A",
    "Property Type": "Office",
    "Buyer": "Brookfield",
    "Seller": "RXR Realty",
    "Total Sale Price": 285000000,
    "Sale Price (PSF)": 425.00,
    "Cap Rate": 5.8,
    "Sale Date": "2025-10-20",
    "Transaction SQFT": 670000
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Brokerage firm columns can contain multiple firms comma-separated — split and count each firm independently
- Sales do not have Landlord/Tenant Brokerage fields — use Buyer/Seller for sales league tables
