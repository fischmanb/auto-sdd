# F-036: Situation Reports

**Category**: AI & Analytics
**Phase**: 2
**Data Source**: All + AI
**Status**: Planned

## Description

AI-generated situation report for a specific property or portfolio, combining all available data sources (leases, sales, properties, news) into a comprehensive assessment. Answers the question "What's the full picture on this asset?" — covering tenant roster, lease rollover, market positioning, comparable sales, and recent news in a single document.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Property search input with typeahead by address or property name
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while AI aggregates data and generates report
- [ ] Empty state shown when no property is selected
- [ ] AI input prompt format: JSON with property details (from Properties CSV), lease history (from Leases CSV), recent sales comps (from Sales CSV), and market context
- [ ] AI output format: structured report with sections: Property Profile, Tenant Roster, Lease Rollover Risk, Market Comps, Valuation Indicators, Key Risks & Opportunities
- [ ] Report displays inline data tables for tenant list, comparable transactions, and valuation metrics
- [ ] "Export to PDF" button for downloadable report
- [ ] "Regenerate" button to produce alternative report version
- [ ] Report generation timestamp displayed prominently

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

// 5+ records representing situation report data — multi-source property data
const MOCK_RECORDS = [
  {
    "section": "property_profile",
    "PROPERTY_NAME": "One Vanderbilt",
    "ADDRESS": "One Vanderbilt Ave",
    "MARKET": "New York City",
    "SUBMARKET": "Grand Central",
    "PROPERTY_SIZE": 1657000,
    "BUILDING_CLASS": "A",
    "PROPERTY_TYPE": "Office",
    "YEAR_BUILT": 2020,
    "FLOORS": 77,
    "LANDLORD": "SL Green Realty",
    "LATITUDE": 40.7527,
    "LONGITUDE": -73.9787
  },
  {
    "section": "tenant_roster",
    "Tenant Name": "TD Securities",
    "Transaction SQFT": 200000,
    "Starting Rent": 130.00,
    "Commencement Date": "2021-01-01",
    "Expiration Date": "2036-12-31",
    "Transaction Type": "New Lease"
  },
  {
    "section": "tenant_roster",
    "Tenant Name": "Carlyle Group",
    "Transaction SQFT": 85000,
    "Starting Rent": 145.00,
    "Commencement Date": "2021-06-01",
    "Expiration Date": "2036-05-31",
    "Transaction Type": "New Lease"
  },
  {
    "section": "sales_comp",
    "Street Address": "390 Madison Ave",
    "Submarket": "Grand Central",
    "Total Sale Price": 825000000,
    "Sale Price (PSF)": 1050.00,
    "Cap Rate": 4.2,
    "Sale Date": "2025-03-15"
  },
  {
    "section": "sales_comp",
    "Street Address": "425 Park Ave",
    "Submarket": "Grand Central",
    "Total Sale Price": 650000000,
    "Sale Price (PSF)": 1100.00,
    "Cap Rate": 4.0,
    "Sale Date": "2024-11-20"
  },
  {
    "section": "market_context",
    "Market": "New York City",
    "Submarket": "Grand Central",
    "avg_class_a_rent": 92.00,
    "avg_cap_rate": 4.5,
    "vacancy_proxy_pct": 12.3
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- AI endpoint: POST to tRPC route calling OpenAI gpt-4.1-nano with multi-source property data
- Property lookup joins Properties CSV (by ADDRESS + MARKET) with Leases CSV (by Street Address + Market)
- Sales comps filtered to same submarket and property type within trailing 24 months
- PDF export requires server-side rendering — same infrastructure as F-035 Market Briefing
