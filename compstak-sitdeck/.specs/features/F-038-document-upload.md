# F-038: Document Upload

**Category**: Data Integration
**Phase**: 2
**Data Source**: Client
**Status**: Planned

## Description

Document management widget for uploading, storing, and referencing CRE documents (LOIs, lease abstracts, appraisals, offering memoranda) alongside dashboard data. Enables users to attach supporting documents to specific properties or deals, creating a centralized workspace for transaction due diligence.

## Acceptance Criteria

- [ ] Widget renders in a deck grid cell at minimum 2×2 grid units
- [ ] No market/submarket filters — documents are organized by user's own taxonomy
- [ ] Widget-level filters override deck-level filters when set
- [ ] Loading state shown while documents load
- [ ] Empty state shown when no documents have been uploaded
- [ ] Drag-and-drop file upload supporting PDF, DOCX, XLSX, and image formats (max 25MB per file)
- [ ] Document list with columns: filename, type, upload date, associated property/deal, file size
- [ ] Tag system for organizing documents: LOI, Lease Abstract, Appraisal, OM, Financial Model, Other
- [ ] Search by filename or tag
- [ ] Click to preview PDF and image files inline; download for DOCX/XLSX
- [ ] Associate documents with a property address or deal pipeline entry (F-029)
- [ ] Delete confirmation dialog before removing uploaded documents

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

// 5+ records representing uploaded documents — not CSV transaction records
const MOCK_RECORDS = [
  {
    "doc_id": "DOC-001",
    "filename": "200-Park-Ave-LOI-Draft.pdf",
    "file_type": "PDF",
    "file_size_kb": 245,
    "upload_date": "2026-03-05T10:30:00Z",
    "tag": "LOI",
    "associated_property": "200 Park Ave, New York, NY",
    "associated_deal_id": "DEAL-001"
  },
  {
    "doc_id": "DOC-002",
    "filename": "Q4-2025-Appraisal-Willis-Tower.pdf",
    "file_type": "PDF",
    "file_size_kb": 1800,
    "upload_date": "2026-02-28T14:15:00Z",
    "tag": "Appraisal",
    "associated_property": "Willis Tower, Chicago, IL",
    "associated_deal_id": null
  },
  {
    "doc_id": "DOC-003",
    "filename": "Tenant-Financial-Model-2026.xlsx",
    "file_type": "XLSX",
    "file_size_kb": 520,
    "upload_date": "2026-03-01T09:00:00Z",
    "tag": "Financial Model",
    "associated_property": null,
    "associated_deal_id": "DEAL-003"
  },
  {
    "doc_id": "DOC-004",
    "filename": "1395-Brickell-OM.pdf",
    "file_type": "PDF",
    "file_size_kb": 3200,
    "upload_date": "2026-02-20T16:45:00Z",
    "tag": "OM",
    "associated_property": "1395 Brickell Ave, Miami, FL",
    "associated_deal_id": null
  },
  {
    "doc_id": "DOC-005",
    "filename": "Lease-Abstract-Acme-Corp.docx",
    "file_type": "DOCX",
    "file_size_kb": 85,
    "upload_date": "2026-03-04T11:20:00Z",
    "tag": "Lease Abstract",
    "associated_property": "200 Park Ave, New York, NY",
    "associated_deal_id": "DEAL-001"
  }
];
```

## API Readiness Notes

- MOCK_* constants replace with `GET /api/enums/{type}` when live
- Documents stored in local file system — not in CSV data or DuckDB
- At integration: consider cloud storage (S3) with pre-signed URLs for document access
- Document metadata stored in SQLite alongside deal pipeline data (F-029)
- PDF preview uses browser-native PDF viewer; image preview via img tag
- File validation: reject executables, enforce max file size, scan for malware at integration
