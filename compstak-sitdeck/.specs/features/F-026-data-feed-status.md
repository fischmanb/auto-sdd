# F-026: Data Feed Status

**Category**: AI & Analytics
**Phase**: 1
**Data Source**: Internal
**Status**: Planned

## Description

Operational dashboard showing the health and freshness of all data feeds powering the SitDeck: CSV file sizes, row counts, last-modified timestamps, and DuckDB query performance metrics. Ensures users know whether they're looking at current data and helps administrators diagnose data pipeline issues.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] No market/submarket filters — this is a system-wide status widget
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while status checks execute
- [ ] Empty state shown if no data feeds are configured
- [ ] Status card per data source: Leases CSV, Sales CSV, Properties CSV
- [ ] Each card shows: file name, file size, row count, last-modified date, load status (OK / Error / Stale)
- [ ] Stale threshold: flag files not updated in > 30 days as "Stale" with warning indicator
- [ ] DuckDB performance panel: total tables loaded, memory usage, average query time for last 10 queries
- [ ] Manual refresh button to re-scan file system and reload DuckDB tables
- [ ] Timestamp of last dashboard refresh displayed prominently

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

// 5+ records representing data feed status — not CSV transaction records
const MOCK_RECORDS = [
  {
    "feed_name": "snowflake-full-leases-2026-03-04.csv",
    "data_source": "Leases",
    "file_size_mb": 485,
    "row_count": 892000,
    "last_modified": "2026-03-04T08:30:00Z",
    "load_status": "OK",
    "duckdb_table": "leases"
  },
  {
    "feed_name": "snowflake-full-sales-2026-03-04.csv",
    "data_source": "Sales",
    "file_size_mb": 210,
    "row_count": 345000,
    "last_modified": "2026-03-04T08:30:00Z",
    "load_status": "OK",
    "duckdb_table": "sales"
  },
  {
    "feed_name": "snowflake-full-properties-2025-03-17.csv",
    "data_source": "Properties",
    "file_size_mb": 1200,
    "row_count": 3400000,
    "last_modified": "2025-03-17T12:00:00Z",
    "load_status": "Stale",
    "duckdb_table": "properties"
  },
  {
    "feed_name": "duckdb_performance",
    "data_source": "Internal",
    "tables_loaded": 3,
    "memory_usage_mb": 2048,
    "avg_query_time_ms": 145,
    "last_10_queries_ms": [120, 135, 180, 110, 155, 140, 165, 130, 125, 190]
  },
  {
    "feed_name": "dashboard_meta",
    "data_source": "Internal",
    "last_refresh": "2026-03-07T14:22:00Z",
    "refresh_duration_ms": 3200,
    "widget_count": 44,
    "active_widgets": 12
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- This widget reads file system metadata and DuckDB internals — no CSV column mapping needed
- Stale threshold (30 days) should be configurable via widget settings
- DuckDB performance metrics from `PRAGMA database_size` and query timing instrumentation
- At integration: add health check endpoint `GET /api/health/feeds` returning same shape as MOCK_RECORDS
