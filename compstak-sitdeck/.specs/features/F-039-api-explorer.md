# F-039: API Explorer

**Category**: Data Integration
**Phase**: 2
**Data Source**: API
**Status**: Planned

## Description

Interactive API documentation and testing widget that lets power users explore and execute CompStak data queries directly. Provides a Swagger-like interface for the SitDeck's internal tRPC routes, enabling custom data extraction, integration testing, and advanced querying beyond what pre-built widgets offer.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] No market filters — API explorer operates across all data
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while API request executes
- [ ] Empty state: list of available API endpoints with descriptions
- [ ] Endpoint selector dropdown listing all tRPC routes (leases, sales, properties, enums, health)
- [ ] Request builder: parameter inputs auto-generated from endpoint schema
- [ ] "Execute" button sends request and displays response in formatted JSON panel
- [ ] Response panel shows: HTTP status, response time (ms), payload size, formatted JSON body
- [ ] Request history: last 20 requests with replay capability
- [ ] "Copy as cURL" button for sharing API calls
- [ ] Rate limiting display: remaining requests and reset time

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

// 5+ records representing API endpoints and example requests/responses
const MOCK_RECORDS = [
  {
    "endpoint": "leases.query",
    "method": "POST",
    "description": "Query lease transactions with filters",
    "example_params": {"market": "New York City", "building_class": "A", "limit": 10},
    "example_response_status": 200,
    "example_response_time_ms": 145,
    "example_response_count": 10
  },
  {
    "endpoint": "sales.query",
    "method": "POST",
    "description": "Query sales transactions with filters",
    "example_params": {"market": "Miami - Ft. Lauderdale", "property_type": "Office", "min_sale_price": 50000000},
    "example_response_status": 200,
    "example_response_time_ms": 98,
    "example_response_count": 5
  },
  {
    "endpoint": "properties.lookup",
    "method": "GET",
    "description": "Look up property details by address or ID",
    "example_params": {"address": "One Vanderbilt Ave", "market": "New York City"},
    "example_response_status": 200,
    "example_response_time_ms": 52,
    "example_response_count": 1
  },
  {
    "endpoint": "enums.list",
    "method": "GET",
    "description": "List available filter enumerations",
    "example_params": {"type": "markets"},
    "example_response_status": 200,
    "example_response_time_ms": 12,
    "example_response_count": 40
  },
  {
    "endpoint": "health.feeds",
    "method": "GET",
    "description": "Check data feed health and freshness",
    "example_params": {},
    "example_response_status": 200,
    "example_response_time_ms": 8,
    "example_response_count": 3
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- API explorer reads tRPC route definitions for auto-generated parameter forms
- At integration: tRPC introspection or OpenAPI schema export for endpoint discovery
- Rate limiting enforced at tRPC middleware layer — explorer displays remaining quota
- Request history stored in browser localStorage — not persisted server-side
- Security: API explorer should respect same authentication and authorization as widget queries
