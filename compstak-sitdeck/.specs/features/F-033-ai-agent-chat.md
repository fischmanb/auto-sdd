# F-033: AI Agent (Chat)

**Category**: AI & Analytics
**Phase**: 2
**Data Source**: All + AI
**Status**: Planned

## Description

Conversational AI assistant that answers natural-language CRE questions by querying lease, sale, and property data via DuckDB. Users type questions like "What's the average rent for Class A office in Midtown Manhattan?" and receive data-backed answers with supporting transaction evidence. The most versatile AI widget in the deck.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Chat input text field with send button and Enter key submission
- [ ] Market filter dropdown populated from MOCK_MARKETS constant as default context
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while AI processes query and runs DuckDB
- [ ] Empty state: welcome message with example questions
- [ ] AI input prompt format: user's natural language question + current deck filters (market, property type, date range) as JSON context
- [ ] AI output format: narrative answer + optional data table + SQL query used (collapsible)
- [ ] Conversation history maintained within widget session (scrollable message list)
- [ ] "Clear conversation" button to reset chat history
- [ ] AI can reference data from leases, sales, and properties CSVs
- [ ] Error handling: if AI cannot answer, display "I couldn't find data to answer that question" with suggestions

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

// 5+ records representing example Q&A pairs — not CSV records
const MOCK_RECORDS = [
  {
    "user_question": "What's the average Class A office rent in Midtown Manhattan?",
    "ai_answer": "The average Starting Rent for Class A office space in Midtown Manhattan over the trailing 12 months is $84.50/SF across 142 transactions totaling 4.2M SF.",
    "sql_query": "SELECT AVG(\"Starting Rent\") FROM leases WHERE \"Market\" = 'New York City' AND \"Submarket\" = 'Midtown Manhattan' AND \"Building Class\" = 'A' AND \"Space Type\" = 'Office' AND \"Execution Date\" >= '2025-03-07'",
    "data_table": [{"metric": "Avg Starting Rent", "value": "$84.50"}, {"metric": "Transaction Count", "value": "142"}, {"metric": "Total SQFT", "value": "4,200,000"}]
  },
  {
    "user_question": "Show me the largest office sales in Miami this year",
    "ai_answer": "Here are the 5 largest office sales in Miami - Ft. Lauderdale in 2025, sorted by Total Sale Price.",
    "sql_query": "SELECT \"Street Address\", \"Submarket\", \"Total Sale Price\", \"Sale Price (PSF)\", \"Cap Rate\" FROM sales WHERE \"Market\" = 'Miami - Ft. Lauderdale' AND \"Property Type\" = 'Office' AND \"Sale Date\" >= '2025-01-01' ORDER BY \"Total Sale Price\" DESC LIMIT 5",
    "data_table": [{"Street Address": "1395 Brickell Ave", "Total Sale Price": "$245M", "Cap Rate": "4.8%"}]
  },
  {
    "user_question": "Which tenants are expanding in Austin?",
    "ai_answer": "In the trailing 24 months, 8 tenants have executed Expansion transactions in Austin, led by TechCorp Inc (85,000 SF) and DataStream Analytics (95,000 SF).",
    "sql_query": "SELECT \"Tenant Name\", SUM(\"Transaction SQFT\") as total_sqft FROM leases WHERE \"Market\" = 'Austin' AND \"Transaction Type\" = 'Expansion' GROUP BY \"Tenant Name\" ORDER BY total_sqft DESC",
    "data_table": [{"Tenant Name": "DataStream Analytics", "Total SQFT": "95,000"}, {"Tenant Name": "TechCorp Inc", "Total SQFT": "85,000"}]
  },
  {
    "user_question": "Compare cap rates between office and industrial in Dallas",
    "ai_answer": "In Dallas - Ft. Worth over the trailing 12 months, office cap rates average 5.9% while industrial cap rates average 6.8%, a spread of 90 basis points.",
    "sql_query": "SELECT \"Property Type\", AVG(\"Cap Rate\") FROM sales WHERE \"Market\" = 'Dallas - Ft. Worth' AND \"Property Type\" IN ('Office', 'Industrial') GROUP BY \"Property Type\"",
    "data_table": [{"Property Type": "Office", "Avg Cap Rate": "5.9%"}, {"Property Type": "Industrial", "Avg Cap Rate": "6.8%"}]
  },
  {
    "user_question": "How many properties does Blackstone own in Chicago?",
    "ai_answer": "Based on the properties dataset, Blackstone Group is listed as landlord for 12 properties in the Chicago Metro market totaling 8.4M SF.",
    "sql_query": "SELECT COUNT(*), SUM(\"PROPERTY_SIZE\") FROM properties WHERE \"MARKET\" = 'Chicago Metro' AND \"LANDLORD\" ILIKE '%Blackstone%'",
    "data_table": [{"metric": "Property Count", "value": "12"}, {"metric": "Total SQFT", "value": "8,400,000"}]
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- AI endpoint: POST to tRPC route calling OpenAI gpt-4.1-nano with text-to-SQL capabilities
- AI generates DuckDB SQL from natural language — SQL validated and executed server-side before returning results
- Security: AI-generated SQL must be sandboxed — read-only queries only, no DDL/DML
- All three CSV tables (leases, sales, properties) available for AI querying
