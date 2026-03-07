# F-015: Property Details

**Category**: Tenant & Property
**Phase**: 1
**Data Source**: Properties CSV
**Status**: Planned

## Description

Detailed property profile card showing building-level attributes from the properties dataset: size, year built, building class, parking ratio, floor count, and landlord. Links to the CompStak exchange listing via the LINK column. The primary reference widget when a user needs to look up a specific building's physical characteristics.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] Property search input with typeahead by ADDRESS or PROPERTY_NAME from properties CSV
- [ ] Market filter dropdown populated from MOCK_MARKETS constant (maps to MARKET column)
- [ ] Submarket dropdown populates from data filtered by currently selected Market — never a static list (maps to SUBMARKET column)
- [ ] Building Class filter populated from MOCK_BUILDING_CLASSES constant (maps to BUILDING_CLASS column)
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while DuckDB query executes
- [ ] Empty state shown when no data matches filters
- [ ] Property card displays: PROPERTY_NAME, ADDRESS, CITY, STATE, ZIPCODE, MARKET, SUBMARKET, LANDLORD, PROPERTY_SIZE, YEAR_BUILT, YEAR_RENOVATED, FLOORS, CEILING_HEIGHT, PARKING_RATIO, BUILDING_CLASS, PROPERTY_TYPE, PROPERTY_SUBTYPE
- [ ] LINK column rendered as clickable "View on CompStak" button opening in new tab
- [ ] Estimated rent fields shown: PROPERTY_MARKET_EFFECTIVE_RENT_ESTIMATE and PROPERTY_MARKET_STARTING_RENT_ESTIMATE
- [ ] Map pin shown using LATITUDE and LONGITUDE columns (not Geo Point)

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

// 5+ records using exact Properties CSV column names
const MOCK_RECORDS = [
  {
    "ID": 100234,
    "LINK": "https://exchange.compstak.com/property/100234",
    "ADDRESS": "One Vanderbilt Ave",
    "CITY": "New York",
    "STATE": "NY",
    "ZIPCODE": "10017",
    "COUNTY": "New York",
    "MARKET": "New York City",
    "SUBMARKET": "Grand Central",
    "LATITUDE": 40.7527,
    "LONGITUDE": -73.9787,
    "PROPERTY_NAME": "One Vanderbilt",
    "LANDLORD": "SL Green Realty",
    "PROPERTY_SIZE": 1657000,
    "PARKING_RATIO": 0.1,
    "YEAR_BUILT": 2020,
    "YEAR_RENOVATED": null,
    "FLOORS": 77,
    "CEILING_HEIGHT": 14,
    "BUILDING_CLASS": "A",
    "PROPERTY_TYPE": "Office",
    "PROPERTY_SUBTYPE": "Professional Building",
    "PROPERTY_MARKET_EFFECTIVE_RENT_ESTIMATE": 125.00,
    "PROPERTY_MARKET_STARTING_RENT_ESTIMATE": 140.00,
    "DATE_CREATED": "2021-01-15"
  },
  {
    "ID": 100456,
    "LINK": "https://exchange.compstak.com/property/100456",
    "ADDRESS": "Willis Tower",
    "CITY": "Chicago",
    "STATE": "IL",
    "ZIPCODE": "60606",
    "COUNTY": "Cook",
    "MARKET": "Chicago Metro",
    "SUBMARKET": "Chicago CBD",
    "LATITUDE": 41.8789,
    "LONGITUDE": -87.6359,
    "PROPERTY_NAME": "Willis Tower",
    "LANDLORD": "Blackstone Group",
    "PROPERTY_SIZE": 4477000,
    "PARKING_RATIO": 0.3,
    "YEAR_BUILT": 1973,
    "YEAR_RENOVATED": 2020,
    "FLOORS": 110,
    "CEILING_HEIGHT": 12,
    "BUILDING_CLASS": "A",
    "PROPERTY_TYPE": "Office",
    "PROPERTY_SUBTYPE": "Professional Building",
    "PROPERTY_MARKET_EFFECTIVE_RENT_ESTIMATE": 38.00,
    "PROPERTY_MARKET_STARTING_RENT_ESTIMATE": 44.00,
    "DATE_CREATED": "2019-05-20"
  },
  {
    "ID": 100789,
    "LINK": "https://exchange.compstak.com/property/100789",
    "ADDRESS": "555 California St",
    "CITY": "San Francisco",
    "STATE": "CA",
    "ZIPCODE": "94104",
    "COUNTY": "San Francisco",
    "MARKET": "San Francisco",
    "SUBMARKET": "Financial District",
    "LATITUDE": 37.7922,
    "LONGITUDE": -122.4035,
    "PROPERTY_NAME": "555 California Street",
    "LANDLORD": "Vornado Realty Trust",
    "PROPERTY_SIZE": 1800000,
    "PARKING_RATIO": 0.2,
    "YEAR_BUILT": 1969,
    "YEAR_RENOVATED": 2015,
    "FLOORS": 52,
    "CEILING_HEIGHT": 11,
    "BUILDING_CLASS": "A",
    "PROPERTY_TYPE": "Office",
    "PROPERTY_SUBTYPE": "Professional Building",
    "PROPERTY_MARKET_EFFECTIVE_RENT_ESTIMATE": 72.00,
    "PROPERTY_MARKET_STARTING_RENT_ESTIMATE": 82.00,
    "DATE_CREATED": "2018-11-10"
  },
  {
    "ID": 101012,
    "LINK": "https://exchange.compstak.com/property/101012",
    "ADDRESS": "2000 McKinney Ave",
    "CITY": "Dallas",
    "STATE": "TX",
    "ZIPCODE": "75201",
    "COUNTY": "Dallas",
    "MARKET": "Dallas - Ft. Worth",
    "SUBMARKET": "Uptown/Turtle Creek",
    "LATITUDE": 32.7950,
    "LONGITUDE": -96.8010,
    "PROPERTY_NAME": "McKinney & Olive",
    "LANDLORD": "Harvest Partners",
    "PROPERTY_SIZE": 530000,
    "PARKING_RATIO": 2.5,
    "YEAR_BUILT": 2016,
    "YEAR_RENOVATED": null,
    "FLOORS": 27,
    "CEILING_HEIGHT": 10,
    "BUILDING_CLASS": "A",
    "PROPERTY_TYPE": "Office",
    "PROPERTY_SUBTYPE": "Professional Building",
    "PROPERTY_MARKET_EFFECTIVE_RENT_ESTIMATE": 42.00,
    "PROPERTY_MARKET_STARTING_RENT_ESTIMATE": 48.00,
    "DATE_CREATED": "2017-03-22"
  },
  {
    "ID": 101345,
    "LINK": "https://exchange.compstak.com/property/101345",
    "ADDRESS": "1201 New York Ave NW",
    "CITY": "Washington",
    "STATE": "DC",
    "ZIPCODE": "20005",
    "COUNTY": "District of Columbia",
    "MARKET": "Washington DC",
    "SUBMARKET": "East End",
    "LATITUDE": 38.9010,
    "LONGITUDE": -77.0280,
    "PROPERTY_NAME": "CityCenter DC - Office",
    "LANDLORD": "Hines",
    "PROPERTY_SIZE": 390000,
    "PARKING_RATIO": 0.8,
    "YEAR_BUILT": 2015,
    "YEAR_RENOVATED": null,
    "FLOORS": 10,
    "CEILING_HEIGHT": 10,
    "BUILDING_CLASS": "A",
    "PROPERTY_TYPE": "Office",
    "PROPERTY_SUBTYPE": "Professional Building",
    "PROPERTY_MARKET_EFFECTIVE_RENT_ESTIMATE": 55.00,
    "PROPERTY_MARKET_STARTING_RENT_ESTIMATE": 62.00,
    "DATE_CREATED": "2016-08-05"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- DuckDB column names match CSV headers verbatim — no mapping needed at integration
- Submarket filter wired to parent Market selection — no change at integration
- Properties CSV uses LATITUDE and LONGITUDE as separate columns — NOT Geo Point
- LINK column contains CompStak exchange URL — open in new tab, do not iframe
- Many columns nullable (YEAR_RENOVATED, CEILING_HEIGHT, LOT_SIZE) — display "N/A" when null
