# F-032: Tenant Credit Indicators

**Category**: Tenant & Property
**Phase**: 2
**Data Source**: Leases + AI
**Status**: Planned

## Description

AI-enhanced tenant credit risk assessment that combines lease transaction patterns with publicly available financial signals. Analyzes a tenant's leasing behavior (expansion vs. contraction, lease term trends, market presence changes) to produce a credit risk indicator that helps landlords evaluate tenant quality.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Tenant Name search input with typeahead from lease data
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while AI analysis executes
- [ ] Empty state shown when no tenant is selected
- [ ] AI input prompt format: JSON with tenant_name, transaction_history (array of {date, type, sqft, market}), lease_trend_summary (expanding/stable/contracting), total_sqft_leased, market_count
- [ ] AI output format: risk_score (1–10), risk_label (Low/Medium/High), reasoning (3–5 bullet points), confidence_level
- [ ] Risk score displayed as gauge or traffic light indicator
- [ ] Transaction history timeline showing expansion/contraction pattern
- [ ] Comparison panel: side-by-side credit indicators for multiple tenants

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

// 5+ records using exact CSV column names — tenant transaction history
const MOCK_RECORDS = [
  {
    "Tenant Name": "WeWork",
    "Tenant Industry": "Real Estate",
    "Market": "New York City",
    "Submarket": "Midtown South",
    "Transaction SQFT": 45000,
    "Starting Rent": 52.00,
    "Transaction Type": "New Lease",
    "Execution Date": "2023-03-15",
    "Lease Term": 60
  },
  {
    "Tenant Name": "WeWork",
    "Tenant Industry": "Real Estate",
    "Market": "New York City",
    "Submarket": "Downtown Manhattan",
    "Transaction SQFT": -30000,
    "Starting Rent": 48.00,
    "Transaction Type": "Renewal/Contraction",
    "Execution Date": "2024-01-20",
    "Lease Term": 36
  },
  {
    "Tenant Name": "WeWork",
    "Tenant Industry": "Real Estate",
    "Market": "Los Angeles - Orange - Inland",
    "Submarket": "Santa Monica",
    "Transaction SQFT": 22000,
    "Starting Rent": 58.00,
    "Transaction Type": "New Lease",
    "Execution Date": "2024-06-10",
    "Lease Term": 48
  },
  {
    "Tenant Name": "WeWork",
    "Tenant Industry": "Real Estate",
    "Market": "Bay Area",
    "Submarket": "South of Market",
    "Transaction SQFT": 35000,
    "Starting Rent": 62.00,
    "Transaction Type": "Assignment",
    "Execution Date": "2024-09-05",
    "Lease Term": 0
  },
  {
    "Tenant Name": "WeWork",
    "Tenant Industry": "Real Estate",
    "Market": "Chicago Metro",
    "Submarket": "Fulton Market",
    "Transaction SQFT": 18000,
    "Starting Rent": 44.00,
    "Transaction Type": "Renewal",
    "Execution Date": "2025-02-28",
    "Lease Term": 36
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- AI endpoint: POST to tRPC route calling OpenAI gpt-4.1-nano with tenant transaction history
- Credit risk is an AI-generated indicator, not a financial credit score — disclaimer must be displayed
- Transaction trend analysis (expanding/contracting) derived from DuckDB aggregation before AI call
