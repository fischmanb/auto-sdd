# F-040: Demographics

**Category**: Market Intelligence
**Phase**: 3
**Data Source**: External
**Status**: Planned

## Description

Displays demographic data for a selected market or submarket area: population, median household income, employment statistics, education levels, and population growth trends. Provides the socioeconomic context that CRE professionals need for retail site selection, multifamily underwriting, and market attractiveness assessments.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while external demographic data loads
- [ ] Empty state shown when no demographic data available for selected area
- [ ] AC describes data contract: expects JSON response with fields: population, median_income, employment_rate, education_bachelors_pct, population_growth_yoy_pct, median_age, total_households
- [ ] AC describes output format: KPI cards for each metric with 5-year trend sparklines
- [ ] Comparison mode: side-by-side demographics for two markets
- [ ] Data source attribution displayed (e.g., "Source: U.S. Census Bureau ACS")
- [ ] Last-updated timestamp for demographic data vintage

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

// TODO: Replace with live Census Bureau / BLS API data at integration
// 5+ records representing demographic data per market
const MOCK_RECORDS = [
  {
    "market": "Austin",
    "population": 2352000,
    "median_income": 82500,
    "employment_rate": 96.2,
    "education_bachelors_pct": 48.3,
    "population_growth_yoy_pct": 2.8,
    "median_age": 34.5,
    "total_households": 892000,
    "data_vintage": "2025 ACS 1-Year Estimate"
  },
  {
    "market": "Miami - Ft. Lauderdale",
    "population": 6185000,
    "median_income": 62400,
    "employment_rate": 95.1,
    "education_bachelors_pct": 35.2,
    "population_growth_yoy_pct": 1.9,
    "median_age": 40.2,
    "total_households": 2345000,
    "data_vintage": "2025 ACS 1-Year Estimate"
  },
  {
    "market": "Nashville",
    "population": 1985000,
    "median_income": 68200,
    "employment_rate": 96.5,
    "education_bachelors_pct": 42.1,
    "population_growth_yoy_pct": 2.1,
    "median_age": 36.8,
    "total_households": 762000,
    "data_vintage": "2025 ACS 1-Year Estimate"
  },
  {
    "market": "Bay Area",
    "population": 4720000,
    "median_income": 128500,
    "employment_rate": 95.8,
    "education_bachelors_pct": 52.7,
    "population_growth_yoy_pct": 0.4,
    "median_age": 37.9,
    "total_households": 1780000,
    "data_vintage": "2025 ACS 1-Year Estimate"
  },
  {
    "market": "Dallas - Ft. Worth",
    "population": 8100000,
    "median_income": 72800,
    "employment_rate": 96.0,
    "education_bachelors_pct": 38.5,
    "population_growth_yoy_pct": 2.3,
    "median_age": 35.2,
    "total_households": 2950000,
    "data_vintage": "2025 ACS 1-Year Estimate"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- Submarket filter wired to parent Market selection — no change at integration
- TODO: External API integration required — Census Bureau ACS API or third-party demographic provider
- Market name to FIPS/CBSA code mapping needed for Census API queries
- Demographic data updated annually — cache aggressively with 30-day TTL
- Data contract: `GET /api/demographics?market={market}` returns JSON matching MOCK_RECORDS shape
