# F-031: Template Outreach

**Category**: Deal Intelligence
**Phase**: 2
**Data Source**: AI
**Status**: Planned

## Description

AI-powered email template generator that creates personalized outreach messages for brokers based on tenant records and market data. Given a target tenant and property, it drafts cold outreach, renewal proposals, or relocation pitches using transaction history as context for the messaging.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while AI generates template
- [ ] Empty state shown when no tenant is selected
- [ ] AI input prompt format: JSON with template_type (cold_outreach | renewal_proposal | relocation_pitch), tenant_name, tenant_industry, current_lease_details (SQFT, rent, expiration), target_property_details (address, rent, class)
- [ ] AI output format: email subject line + email body with greeting, value proposition, call-to-action, and sign-off
- [ ] Template type selector: Cold Outreach, Renewal Proposal, Relocation Pitch
- [ ] Tenant name search input with autocomplete from lease data (Tenant Name column)
- [ ] "Copy to clipboard" button for generated email text
- [ ] "Regenerate" button to produce alternative version

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

// 5+ records representing template generation context — lease data for the tenant
const MOCK_RECORDS = [
  {
    "Tenant Name": "Salesforce Inc",
    "Tenant Industry": "Technology",
    "Market": "Bay Area",
    "Submarket": "Financial District",
    "Street Address": "415 Mission St",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 350000,
    "Starting Rent": 78.00,
    "Current Rent": 82.00,
    "Expiration Date": "2028-12-31",
    "Transaction Type": "Renewal"
  },
  {
    "Tenant Name": "Salesforce Inc",
    "Tenant Industry": "Technology",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Street Address": "3 Bryant Park",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 85000,
    "Starting Rent": 88.00,
    "Current Rent": 92.00,
    "Expiration Date": "2027-06-30",
    "Transaction Type": "New Lease"
  },
  {
    "Tenant Name": "Salesforce Inc",
    "Tenant Industry": "Technology",
    "Market": "Chicago Metro",
    "Submarket": "River North",
    "Street Address": "111 W Illinois St",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 45000,
    "Starting Rent": 42.00,
    "Current Rent": 45.00,
    "Expiration Date": "2026-09-30",
    "Transaction Type": "Expansion"
  },
  {
    "Tenant Name": "Salesforce Inc",
    "Tenant Industry": "Technology",
    "Market": "Atlanta",
    "Submarket": "Midtown",
    "Street Address": "950 E Paces Ferry Rd",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 30000,
    "Starting Rent": 36.00,
    "Current Rent": 38.00,
    "Expiration Date": "2027-03-31",
    "Transaction Type": "New Lease"
  },
  {
    "Tenant Name": "Salesforce Inc",
    "Tenant Industry": "Technology",
    "Market": "Dallas - Ft. Worth",
    "Submarket": "Uptown/Turtle Creek",
    "Street Address": "2200 Ross Ave",
    "Space Type": "Office",
    "Building Class": "A",
    "Property Type": "Office",
    "Transaction SQFT": 25000,
    "Starting Rent": 38.00,
    "Current Rent": 40.00,
    "Expiration Date": "2026-12-31",
    "Transaction Type": "Renewal"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- AI endpoint: POST to tRPC route calling OpenAI gpt-4.1-nano with tenant context and template type
- Tenant data pulled from lease CSV via DuckDB — same query pattern as F-013 Tenant Records
- Generated emails must not include CompStak proprietary rent data in the template — use relative language ("competitive rates") instead
