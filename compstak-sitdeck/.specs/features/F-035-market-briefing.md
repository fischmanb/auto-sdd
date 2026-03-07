# F-035: Market Briefing

**Category**: AI & Analytics
**Phase**: 2
**Data Source**: Leases + AI
**Status**: Planned

## Description

AI-generated one-page market briefing document combining quantitative data from the Market Overview (F-009) with narrative analysis from the AI Market Summary (F-028). Produces a client-ready PDF or printable summary suitable for investment committee presentations, pitch decks, or client reports.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while AI generates briefing
- [ ] Empty state shown when no data matches filters
- [ ] AI input prompt format: JSON with market stats (from F-009), rent trends (from F-008), top transactions, cap rate data
- [ ] AI output format: structured document with sections: Executive Summary, Market Statistics, Rent Analysis, Transaction Highlights, Capital Markets, Outlook
- [ ] Preview panel showing formatted briefing with charts and data tables
- [ ] "Export to PDF" button generating a downloadable document
- [ ] "Regenerate" button to produce alternative briefing version

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

// 5+ records representing briefing data context — aggregated market stats
const MOCK_RECORDS = [
  {
    "section": "market_stats",
    "Market": "Denver",
    "avg_starting_rent": 36.50,
    "total_transaction_sqft": 8200000,
    "deal_count": 485,
    "yoy_rent_change_pct": 3.2,
    "yoy_volume_change_pct": -5.8,
    "period": "trailing 12 months"
  },
  {
    "section": "cap_rate_summary",
    "Market": "Denver",
    "avg_cap_rate": 6.4,
    "cap_rate_range": "5.2–7.8",
    "total_sales_volume": 4200000000,
    "avg_sale_price_psf": 285.00,
    "period": "trailing 12 months"
  },
  {
    "section": "top_lease",
    "Market": "Denver",
    "Submarket": "LoDo",
    "Tenant Name": "Arrow Electronics",
    "Street Address": "9151 E Panorama Cir",
    "Transaction SQFT": 85000,
    "Starting Rent": 42.00,
    "Execution Date": "2025-11-15",
    "Transaction Type": "Renewal"
  },
  {
    "section": "top_sale",
    "Market": "Denver",
    "Submarket": "CBD",
    "Street Address": "1801 California St",
    "Total Sale Price": 185000000,
    "Sale Price (PSF)": 380.00,
    "Cap Rate": 5.5,
    "Sale Date": "2025-10-20",
    "Buyer": "Brookfield"
  },
  {
    "section": "construction",
    "Market": "Denver",
    "pre_lease_sqft": 425000,
    "pre_lease_count": 8,
    "avg_pre_lease_rent": 48.00,
    "earliest_delivery": "2026-Q3"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- AI endpoint: POST to tRPC route calling OpenAI gpt-4.1-nano with aggregated market data
- PDF generation requires server-side rendering library (e.g., Puppeteer, jsPDF) — not included in AI response
- Briefing combines data from F-008, F-009, F-020 widget queries — cross-widget data dependency
