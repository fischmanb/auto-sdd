# F-011: Recent Transactions

**Category**: Deal Intelligence
**Phase**: 1
**Data Source**: Leases + Sales
**Status**: Planned

## Description

Paginated, sortable table of the most recent lease and sale transactions in a market. The go-to widget for brokers who need a quick pulse on what deals just closed, at what terms, and who was involved. Supports filtering by transaction type, space type, and date range.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Transaction Type filter populated from MOCK_TRANSACTION_TYPES constant (leases) and text search for Sale Type (sales)
- [ ] Sale Type filter is a text search input, not a dropdown — state this explicitly
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Lease rows show: Street Address, Submarket, Tenant Name, Transaction SQFT, Starting Rent, Execution Date, Transaction Type
- [ ] Sale rows show: Street Address, Submarket, Buyer, Total Sale Price, Sale Price (PSF), Cap Rate, Sale Date
- [ ] Toggle between "Leases", "Sales", or "All" view modes
- [ ] Default sort by most recent date (Execution Date or Sale Date)
- [ ] Pagination with 25 rows per page

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

// 5+ records using exact CSV column names — mix of lease and sale
const MOCK_RECORDS = [
  {
    "Market": "Houston",
    "Submarket": "The Woodlands",
    "Street Address": "9950 Woodloch Forest Dr",
    "City": "Houston",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Tenant Name": "EnergyTech Solutions",
    "Transaction SQFT": 35000,
    "Starting Rent": 34.00,
    "Execution Date": "2025-11-15",
    "Transaction Type": "New Lease",
    "Lease Type": "Full Service"
  },
  {
    "Market": "Houston",
    "Submarket": "Galleria/Uptown",
    "Street Address": "2929 Allen Pkwy",
    "City": "Houston",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Office",
    "Space Type": "Office",
    "Tenant Name": "Baker & McKenzie LLP",
    "Transaction SQFT": 22000,
    "Starting Rent": 42.00,
    "Execution Date": "2025-10-28",
    "Transaction Type": "Renewal",
    "Lease Type": "Full Service"
  },
  {
    "Market": "Houston",
    "Submarket": "CBD",
    "Street Address": "1000 Louisiana St",
    "City": "Houston",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Office",
    "Buyer": "Brookfield Asset Management",
    "Seller": "Hines REIT",
    "Total Sale Price": 310000000,
    "Sale Price (PSF)": 395.00,
    "Cap Rate": 5.5,
    "Sale Date": "2025-09-20",
    "Transaction SQFT": 784000
  },
  {
    "Market": "Houston",
    "Submarket": "Katy Freeway",
    "Street Address": "1500 Citywest Blvd",
    "City": "Houston",
    "State": "TX",
    "Building Class": "B",
    "Property Type": "Office",
    "Space Type": "Office",
    "Tenant Name": "Patriot Engineering",
    "Transaction SQFT": 12000,
    "Starting Rent": 28.00,
    "Execution Date": "2025-11-02",
    "Transaction Type": "Expansion",
    "Lease Type": "Modified Gross"
  },
  {
    "Market": "Houston",
    "Submarket": "Energy Corridor",
    "Street Address": "14520 Memorial Dr",
    "City": "Houston",
    "State": "TX",
    "Building Class": "A",
    "Property Type": "Office",
    "Buyer": "KKR Real Estate",
    "Seller": "ConocoPhillips",
    "Total Sale Price": 175000000,
    "Sale Price (PSF)": 285.00,
    "Cap Rate": 6.8,
    "Sale Date": "2025-10-05",
    "Transaction SQFT": 614000
  },
  {
    "Market": "Houston",
    "Submarket": "Westchase",
    "Street Address": "3040 Post Oak Blvd",
    "City": "Houston",
    "State": "TX",
    "Building Class": "B",
    "Property Type": "Industrial",
    "Space Type": "Industrial",
    "Tenant Name": "Gulf Coast Logistics",
    "Transaction SQFT": 85000,
    "Starting Rent": 12.50,
    "Execution Date": "2025-08-18",
    "Transaction Type": "New Lease",
    "Lease Type": "NNN"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Sale Type is free-text in the CSV — always render as text search input, never a dropdown
- Lease and sale records come from separate CSVs; UNION query needed for "All" view mode
