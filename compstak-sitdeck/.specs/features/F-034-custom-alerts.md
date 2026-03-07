# F-034: Custom Alerts

**Category**: AI & Analytics
**Phase**: 2
**Data Source**: All
**Status**: Planned

## Description

Data-driven alert system that monitors lease and sales transaction feeds for user-defined conditions and triggers notifications when matches occur. Unlike News Alerts (F-030) which monitor external news, Custom Alerts monitor the actual CompStak transaction data — e.g., "alert me when a new lease over 50K SF is recorded in Midtown Manhattan."

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Market filter dropdown populated from MOCK_MARKETS constant for alert conditions
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list
- [ ] Property Type filter populated from MOCK_PROPERTY_TYPES constant
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant
- [ ] Transaction Type filter populated from MOCK_TRANSACTION_TYPES constant
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while alerts and matches load
- [ ] Empty state shown when no alert rules are configured
- [ ] Alert rule builder: market, submarket, property type, building class, transaction type, min/max SQFT, min/max rent, tenant name pattern
- [ ] Alert feed shows matched transactions with timestamp and rule that triggered
- [ ] Unread alert count badge on widget header
- [ ] Maximum 25 active data alert rules per user

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

// 5+ records representing alert rules and matched transactions
const MOCK_RECORDS = [
  {
    "alert_id": "DATA-ALERT-001",
    "rule_name": "Large Midtown Leases",
    "Market": "New York City",
    "Submarket": "Midtown Manhattan",
    "Property Type": "Office",
    "Building Class": "A",
    "min_sqft": 50000,
    "matched_transaction": {
      "Tenant Name": "BlackRock Inc",
      "Street Address": "50 Hudson Yards",
      "Transaction SQFT": 72000,
      "Starting Rent": 95.00,
      "Execution Date": "2026-03-01",
      "Transaction Type": "Expansion"
    }
  },
  {
    "alert_id": "DATA-ALERT-002",
    "rule_name": "Industrial Sales > $50M",
    "Market": "Dallas - Ft. Worth",
    "Property Type": "Industrial",
    "min_sale_price": 50000000,
    "matched_transaction": {
      "Street Address": "4500 Diplomacy Rd",
      "Buyer": "Prologis Inc",
      "Total Sale Price": 88000000,
      "Sale Price (PSF)": 165.00,
      "Cap Rate": 6.2,
      "Sale Date": "2026-02-20"
    }
  },
  {
    "alert_id": "DATA-ALERT-003",
    "rule_name": "Tech Tenant New Leases",
    "Market": "Austin",
    "Transaction Type": "New Lease",
    "tenant_pattern": "tech|software|data|AI",
    "matched_transaction": {
      "Tenant Name": "DataStream Analytics",
      "Street Address": "401 Congress Ave",
      "Transaction SQFT": 45000,
      "Starting Rent": 58.00,
      "Execution Date": "2026-02-15",
      "Transaction Type": "New Lease"
    }
  },
  {
    "alert_id": "DATA-ALERT-004",
    "rule_name": "High-Rent Office Renewals",
    "min_rent": 100,
    "Transaction Type": "Renewal",
    "Building Class": "A",
    "matched_transaction": {
      "Tenant Name": "Sullivan & Cromwell",
      "Market": "New York City",
      "Street Address": "125 Broad St",
      "Transaction SQFT": 120000,
      "Starting Rent": 108.00,
      "Execution Date": "2026-01-28",
      "Transaction Type": "Renewal"
    }
  },
  {
    "alert_id": "DATA-ALERT-005",
    "rule_name": "Bay Area Pre-leases",
    "Market": "Bay Area",
    "Transaction Type": "Pre-lease",
    "matched_transaction": {
      "Tenant Name": "Anthropic",
      "Street Address": "250 Brannan St",
      "Transaction SQFT": 55000,
      "Starting Rent": 82.00,
      "Execution Date": "2026-03-03",
      "Transaction Type": "Pre-lease"
    }
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Alert rules stored in local SQLite; background job scans new CSV rows against rules
- Alert matching runs on CSV data load/refresh — not real-time streaming
