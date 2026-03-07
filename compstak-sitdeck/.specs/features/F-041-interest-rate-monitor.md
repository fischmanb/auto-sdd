# F-041: Interest Rate Monitor

**Category**: Financial & Economic
**Phase**: 3
**Data Source**: External
**Status**: Planned

## Description

Tracks key interest rates that directly impact CRE financing: Federal Funds Rate, 10-Year Treasury, SOFR, and commercial mortgage spreads. Provides historical trend charts and current values so investors and underwriters can assess financing conditions and model debt costs in real time.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] No market/submarket filters — interest rates are national
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while external rate data loads
- [ ] Empty state shown when rate feed is unavailable
- [ ] AC describes data contract: expects JSON with fields: rate_name, current_value, previous_value, change_bps, date, historical_series (array of {date, value})
- [ ] AC describes output format: rate cards showing current value + daily change in basis points with up/down arrow
- [ ] Line chart showing historical trends for all tracked rates over selectable period (1M, 3M, 6M, 1Y, 5Y)
- [ ] Rates tracked: Fed Funds Rate, 10-Year Treasury, SOFR, 30-Day Avg SOFR, Prime Rate
- [ ] Auto-refresh on configurable interval (15min default)
- [ ] Last-updated timestamp prominently displayed

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

// TODO: Replace with live FRED API / Treasury.gov data at integration
// 5+ records representing interest rate data points
const MOCK_RECORDS = [
  {
    "rate_name": "Federal Funds Rate",
    "current_value": 4.50,
    "previous_value": 4.50,
    "change_bps": 0,
    "date": "2026-03-07",
    "historical_series": [
      {"date": "2025-09-01", "value": 5.00},
      {"date": "2025-12-01", "value": 4.75},
      {"date": "2026-03-01", "value": 4.50}
    ]
  },
  {
    "rate_name": "10-Year Treasury",
    "current_value": 4.22,
    "previous_value": 4.18,
    "change_bps": 4,
    "date": "2026-03-07",
    "historical_series": [
      {"date": "2025-09-01", "value": 4.35},
      {"date": "2025-12-01", "value": 4.28},
      {"date": "2026-03-01", "value": 4.20}
    ]
  },
  {
    "rate_name": "SOFR",
    "current_value": 4.30,
    "previous_value": 4.31,
    "change_bps": -1,
    "date": "2026-03-07",
    "historical_series": [
      {"date": "2025-09-01", "value": 4.82},
      {"date": "2025-12-01", "value": 4.58},
      {"date": "2026-03-01", "value": 4.32}
    ]
  },
  {
    "rate_name": "30-Day Avg SOFR",
    "current_value": 4.32,
    "previous_value": 4.33,
    "change_bps": -1,
    "date": "2026-03-07",
    "historical_series": [
      {"date": "2025-09-01", "value": 4.85},
      {"date": "2025-12-01", "value": 4.60},
      {"date": "2026-03-01", "value": 4.34}
    ]
  },
  {
    "rate_name": "Prime Rate",
    "current_value": 7.50,
    "previous_value": 7.50,
    "change_bps": 0,
    "date": "2026-03-07",
    "historical_series": [
      {"date": "2025-09-01", "value": 8.00},
      {"date": "2025-12-01", "value": 7.75},
      {"date": "2026-03-01", "value": 7.50}
    ]
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- TODO: External API integration required — FRED (Federal Reserve Economic Data) API for Treasury and Fed Funds, NY Fed for SOFR
- Data contract: `GET /api/rates` returns JSON array matching MOCK_RECORDS shape
- Historical series requires daily data points — FRED provides this via series endpoint
- Cache with 15-minute TTL matching auto-refresh interval
- Rate change in basis points: (current - previous) × 100
