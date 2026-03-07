# F-042: REIT Index Tracker

**Category**: Financial & Economic
**Phase**: 3
**Data Source**: External
**Status**: Planned

## Description

Tracks publicly traded REIT indices and individual REIT stock performance relevant to CRE sectors (office, industrial, retail, multifamily). Helps institutional investors benchmark private market performance against public market valuations and identify sector-level sentiment shifts.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant to filter REIT sector
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while external market data loads
- [ ] Empty state shown when market data feed is unavailable
- [ ] AC describes data contract: expects JSON with fields: index_name, sector, current_value, daily_change_pct, ytd_change_pct, market_cap_billions, dividend_yield_pct, historical_series
- [ ] AC describes output format: sector-grouped table with current value, daily change %, YTD %, dividend yield
- [ ] Line chart showing index performance over selectable period (1M, 3M, YTD, 1Y, 3Y)
- [ ] Indices tracked: FTSE Nareit All Equity REITs, FTSE Nareit Office, FTSE Nareit Industrial, FTSE Nareit Retail, FTSE Nareit Residential
- [ ] Daily auto-refresh after market close (4:30 PM ET)

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

// TODO: Replace with live financial data API at integration
// 5+ records representing REIT index data
const MOCK_RECORDS = [
  {
    "index_name": "FTSE Nareit All Equity REITs",
    "sector": "All",
    "current_value": 312.45,
    "daily_change_pct": 0.35,
    "ytd_change_pct": 4.8,
    "market_cap_billions": 1420,
    "dividend_yield_pct": 3.9,
    "date": "2026-03-06"
  },
  {
    "index_name": "FTSE Nareit Office",
    "sector": "Office",
    "current_value": 145.20,
    "daily_change_pct": -0.22,
    "ytd_change_pct": -1.5,
    "market_cap_billions": 85,
    "dividend_yield_pct": 5.2,
    "date": "2026-03-06"
  },
  {
    "index_name": "FTSE Nareit Industrial",
    "sector": "Industrial",
    "current_value": 428.90,
    "daily_change_pct": 0.58,
    "ytd_change_pct": 8.2,
    "market_cap_billions": 310,
    "dividend_yield_pct": 2.8,
    "date": "2026-03-06"
  },
  {
    "index_name": "FTSE Nareit Retail",
    "sector": "Retail",
    "current_value": 198.75,
    "daily_change_pct": 0.12,
    "ytd_change_pct": 2.1,
    "market_cap_billions": 165,
    "dividend_yield_pct": 4.5,
    "date": "2026-03-06"
  },
  {
    "index_name": "FTSE Nareit Residential",
    "sector": "Multi-Family",
    "current_value": 385.60,
    "daily_change_pct": 0.45,
    "ytd_change_pct": 6.3,
    "market_cap_billions": 245,
    "dividend_yield_pct": 3.2,
    "date": "2026-03-06"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- TODO: External financial data API required — consider Alpha Vantage, Yahoo Finance, or Nareit direct feed
- Data contract: `GET /api/reits?sector={sector}` returns JSON array matching MOCK_RECORDS shape
- REIT sector must map to MOCK_PROPERTY_TYPES for filtering consistency
- Historical data needed for chart — daily close values over selected time range
- Market data delayed 15+ minutes unless real-time feed purchased — display delay disclaimer
