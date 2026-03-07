# F-043: CRE Capital Markets

**Category**: Financial & Economic
**Phase**: 3
**Data Source**: External
**Status**: Planned

## Description

Aggregated view of CRE capital markets activity: total investment sales volume, debt origination trends, CMBS issuance, and lending spreads by property type. Provides the macroeconomic capital flow context that helps investors understand whether money is flowing into or out of CRE sectors and how financing availability is shifting.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant to filter by sector
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while external capital markets data loads
- [ ] Empty state shown when capital markets feed is unavailable
- [ ] AC describes data contract: expects JSON with fields: metric_name, sector, current_value, prior_period_value, change_pct, period, source
- [ ] AC describes output format: KPI cards for total investment volume, CMBS issuance, average lending spread, and debt origination volume
- [ ] Bar chart showing quarterly investment sales volume by property type
- [ ] Lending spread trend line overlaid on volume chart
- [ ] Data sourced from industry reports (RCA, MSCI, Trepp) — display source attribution
- [ ] Quarterly data update cadence with last-updated timestamp

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

// TODO: Replace with live capital markets data feed at integration
// 5+ records representing capital markets metrics
const MOCK_RECORDS = [
  {
    "metric_name": "Total CRE Investment Sales Volume",
    "sector": "All",
    "current_value_billions": 142.5,
    "prior_period_value_billions": 128.3,
    "change_pct": 11.1,
    "period": "Q4 2025",
    "source": "MSCI Real Capital Analytics"
  },
  {
    "metric_name": "Office Investment Sales Volume",
    "sector": "Office",
    "current_value_billions": 22.8,
    "prior_period_value_billions": 18.5,
    "change_pct": 23.2,
    "period": "Q4 2025",
    "source": "MSCI Real Capital Analytics"
  },
  {
    "metric_name": "CMBS Issuance",
    "sector": "All",
    "current_value_billions": 28.4,
    "prior_period_value_billions": 24.1,
    "change_pct": 17.8,
    "period": "Q4 2025",
    "source": "Trepp"
  },
  {
    "metric_name": "Average Lending Spread (over SOFR)",
    "sector": "Office",
    "current_value_bps": 225,
    "prior_period_value_bps": 245,
    "change_bps": -20,
    "period": "Q4 2025",
    "source": "CBRE Lending Momentum Index"
  },
  {
    "metric_name": "Industrial Investment Sales Volume",
    "sector": "Industrial",
    "current_value_billions": 38.2,
    "prior_period_value_billions": 35.8,
    "change_pct": 6.7,
    "period": "Q4 2025",
    "source": "MSCI Real Capital Analytics"
  },
  {
    "metric_name": "CRE Debt Origination Volume",
    "sector": "All",
    "current_value_billions": 95.6,
    "prior_period_value_billions": 82.4,
    "change_pct": 16.0,
    "period": "Q4 2025",
    "source": "MBA Quarterly Survey"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- TODO: External data feed integration required — MSCI RCA, Trepp, MBA sources typically require paid subscriptions
- Data contract: `GET /api/capital-markets?sector={sector}&period={quarter}` returns JSON matching MOCK_RECORDS shape
- Quarterly data cadence — cache aggressively with 7-day TTL within quarter
- Lending spreads reported in basis points over SOFR — display as "SOFR + {spread}bps"
- Source attribution required per data point — different metrics may come from different providers
