# F-027: Breaking CRE News

**Category**: Market Intelligence
**Phase**: 2
**Data Source**: External
**Status**: Planned

## Description

Aggregated feed of breaking commercial real estate news from industry sources, filtered by market and property type relevance. Keeps CRE professionals informed about major transactions, market shifts, regulatory changes, and economic developments without leaving the dashboard.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant to filter news by geographic relevance
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant to filter by sector
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while news feed loads
- [ ] Empty state shown when no news matches filters
- [ ] News items display: headline, source, publication date, market tag, brief excerpt
- [ ] Chronological ordering with most recent first
- [ ] Clicking a headline opens the full article in a new tab
- [ ] Auto-refresh interval configurable: 5min, 15min, 30min, or manual only
- [ ] Maximum 50 articles displayed with "Load more" pagination

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

// 5+ records representing news articles — not CSV transaction records
const MOCK_RECORDS = [
  {
    "headline": "Brookfield Closes $2.1B Office Portfolio Acquisition in Manhattan",
    "source": "Commercial Observer",
    "published_date": "2026-03-06T14:30:00Z",
    "market_tag": "New York City",
    "property_type_tag": "Office",
    "excerpt": "Brookfield Asset Management has finalized its acquisition of a five-building office portfolio in Midtown Manhattan, marking the largest office transaction of 2026.",
    "url": "https://example.com/news/brookfield-manhattan"
  },
  {
    "headline": "Miami Office Vacancy Drops Below 10% for First Time Since 2019",
    "source": "GlobeSt.com",
    "published_date": "2026-03-05T10:15:00Z",
    "market_tag": "Miami - Ft. Lauderdale",
    "property_type_tag": "Office",
    "excerpt": "South Florida's office market continues to tighten as firms relocate from the Northeast, pushing Brickell and Coral Gables vacancy to historic lows.",
    "url": "https://example.com/news/miami-vacancy"
  },
  {
    "headline": "Amazon Leases 1.2M SF Industrial Distribution Center in Dallas",
    "source": "Dallas Morning News",
    "published_date": "2026-03-04T08:00:00Z",
    "market_tag": "Dallas - Ft. Worth",
    "property_type_tag": "Industrial",
    "excerpt": "The e-commerce giant has signed a long-term lease for a new distribution facility in the Alliance submarket, the largest industrial lease in DFW this year.",
    "url": "https://example.com/news/amazon-dallas"
  },
  {
    "headline": "Fed Holds Rates Steady, CRE Capital Markets React",
    "source": "Bisnow",
    "published_date": "2026-03-03T16:45:00Z",
    "market_tag": "National",
    "property_type_tag": "Other",
    "excerpt": "The Federal Reserve's decision to maintain current interest rates has stabilized cap rate expectations across major markets.",
    "url": "https://example.com/news/fed-rates-cre"
  },
  {
    "headline": "Austin Office Construction Pipeline Hits 5-Year Low",
    "source": "Austin Business Journal",
    "published_date": "2026-03-02T11:20:00Z",
    "market_tag": "Austin",
    "property_type_tag": "Office",
    "excerpt": "New office starts in the Austin metro have declined 60% year-over-year, signaling a potential supply correction that could tighten the market by 2028.",
    "url": "https://example.com/news/austin-construction"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- News feed requires external RSS/API integration — not sourced from CSV data
- At integration: `GET /api/news?market={market}&property_type={type}` returns articles
- Market tag mapping needed to match news source geographic labels to MOCK_MARKETS values
- Rate limiting and caching required — news APIs typically have request quotas
