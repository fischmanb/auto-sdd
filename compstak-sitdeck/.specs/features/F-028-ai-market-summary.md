# F-028: AI Market Summary

**Category**: Market Intelligence
**Phase**: 2
**Data Source**: Leases + AI
**Status**: Planned

## Description

AI-generated narrative summary of market conditions based on lease transaction data, producing human-readable market commentary. Synthesizes rent trends, transaction volume, tenant activity, and notable deals into a concise briefing that reads like a research analyst's quarterly report.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while AI generation executes
- [ ] Empty state shown when no data matches filters
- [ ] AI input prompt format: structured JSON with market name, trailing-12M stats (avg rent, total SQFT, deal count, YoY changes), top 5 transactions by SQFT
- [ ] AI output format: 3–5 paragraph narrative with sections: Market Overview, Rent Trends, Notable Transactions, Outlook
- [ ] "Regenerate" button to request a fresh summary with same inputs
- [ ] Generated text displays with formatted headings and bullet points
- [ ] Timestamp showing when summary was last generated

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

// 5+ records representing AI input context — lease summary data
const MOCK_RECORDS = [
  {
    "Market": "Bay Area",
    "Submarket": "South of Market",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 68.00,
    "Transaction SQFT": 55000,
    "Execution Date": "2025-11-10",
    "Transaction Type": "New Lease",
    "Tenant Name": "Stripe Inc"
  },
  {
    "Market": "Bay Area",
    "Submarket": "Financial District",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 72.00,
    "Transaction SQFT": 42000,
    "Execution Date": "2025-10-05",
    "Transaction Type": "Renewal",
    "Tenant Name": "Wells Fargo"
  },
  {
    "Market": "Bay Area",
    "Submarket": "Mission Bay",
    "Space Type": "Flex/R&D",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 85.00,
    "Transaction SQFT": 78000,
    "Execution Date": "2025-09-15",
    "Transaction Type": "New Lease",
    "Tenant Name": "Genentech"
  },
  {
    "Market": "Bay Area",
    "Submarket": "Palo Alto",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 95.00,
    "Transaction SQFT": 25000,
    "Execution Date": "2025-08-20",
    "Transaction Type": "Expansion",
    "Tenant Name": "Anthropic"
  },
  {
    "Market": "Bay Area",
    "Submarket": "Mountain View",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Starting Rent": 78.00,
    "Transaction SQFT": 120000,
    "Execution Date": "2025-07-01",
    "Transaction Type": "Renewal",
    "Tenant Name": "Google LLC"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- AI endpoint: POST to tRPC route calling OpenAI gpt-4.1-nano with structured market data as context
- AI prompt template and output format defined in AC — do not allow freeform prompt injection from user input
