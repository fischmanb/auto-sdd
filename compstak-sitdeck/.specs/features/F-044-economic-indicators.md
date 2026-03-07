# F-044: Economic Indicators

**Category**: Financial & Economic
**Phase**: 3
**Data Source**: External
**Status**: Planned

## Description

Dashboard of macroeconomic indicators that influence CRE markets: GDP growth, unemployment rate, CPI inflation, consumer confidence, and job growth. Provides the economic backdrop that helps CRE professionals understand demand drivers and anticipate market turning points.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] No market/submarket filters — economic indicators are national
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while external economic data loads
- [ ] Empty state shown when economic data feed is unavailable
- [ ] AC describes data contract: expects JSON with fields: indicator_name, current_value, prior_value, change, unit, release_date, next_release_date, historical_series
- [ ] AC describes output format: indicator cards with current value, change from prior period, and trend arrow
- [ ] Line chart showing historical trends for selected indicator over 1Y, 3Y, 5Y periods
- [ ] Indicators tracked: GDP Growth (QoQ annualized), Unemployment Rate, CPI YoY, Consumer Confidence Index, Nonfarm Payrolls (monthly change)
- [ ] Next release date displayed for each indicator with countdown
- [ ] Monthly auto-refresh aligned with BLS/BEA release schedule

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

// TODO: Replace with live FRED / BLS / BEA API data at integration
// 5+ records representing economic indicator data points
const MOCK_RECORDS = [
  {
    "indicator_name": "GDP Growth (QoQ Annualized)",
    "current_value": 2.8,
    "prior_value": 3.1,
    "change": -0.3,
    "unit": "%",
    "release_date": "2026-02-27",
    "next_release_date": "2026-05-29",
    "source": "Bureau of Economic Analysis"
  },
  {
    "indicator_name": "Unemployment Rate",
    "current_value": 3.9,
    "prior_value": 4.0,
    "change": -0.1,
    "unit": "%",
    "release_date": "2026-03-07",
    "next_release_date": "2026-04-04",
    "source": "Bureau of Labor Statistics"
  },
  {
    "indicator_name": "CPI Year-over-Year",
    "current_value": 2.6,
    "prior_value": 2.8,
    "change": -0.2,
    "unit": "%",
    "release_date": "2026-03-12",
    "next_release_date": "2026-04-10",
    "source": "Bureau of Labor Statistics"
  },
  {
    "indicator_name": "Consumer Confidence Index",
    "current_value": 108.5,
    "prior_value": 106.2,
    "change": 2.3,
    "unit": "index",
    "release_date": "2026-02-25",
    "next_release_date": "2026-03-25",
    "source": "The Conference Board"
  },
  {
    "indicator_name": "Nonfarm Payrolls (Monthly Change)",
    "current_value": 215000,
    "prior_value": 188000,
    "change": 27000,
    "unit": "jobs",
    "release_date": "2026-03-07",
    "next_release_date": "2026-04-04",
    "source": "Bureau of Labor Statistics"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- TODO: External API integration required — FRED API (free, requires key) for all indicators
- Data contract: `GET /api/economic-indicators` returns JSON array matching MOCK_RECORDS shape
- Release schedule varies by indicator — GDP quarterly, unemployment/CPI/payrolls monthly
- FRED series IDs: GDP (A191RL1Q225SBEA), Unemployment (UNRATE), CPI (CPIAUCSL), Payrolls (PAYEMS)
- Cache with 1-day TTL — indicators update at most monthly
