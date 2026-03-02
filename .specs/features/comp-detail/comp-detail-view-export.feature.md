---
feature: Comp detail view and export
domain: comp-detail
source: py/auto_sdd/lib/comp_detail.py, py/auto_sdd/scripts/comp_detail.py
tests:
  - py/tests/test_comp_detail.py
status: implemented
created: 2026-03-02
updated: 2026-03-02
---

# Comp Detail View and Export

**Source Files**:
- `py/auto_sdd/lib/comp_detail.py` — format_comp_detail, comp_to_dict, export_comps_to_csv, export_comps_to_json
- `py/auto_sdd/scripts/comp_detail.py` — CLI entrypoint (show / export subcommands)

## Feature: Single comp detail view

### Scenario: Format a comp as a detailed multi-line block
Given a `LeaseComp` instance with all fields populated
When `format_comp_detail(comp)` is called
Then a multi-line string is returned containing all fields with labels
And the output includes id, address, market, submarket, tenant, landlord, dates, term, size, rents, free rent, lease type, property type, floor, and source

### Scenario: format_comp_detail output is human-readable
Given a `LeaseComp` with size_sf=10000 and asking_rent_psf=75.50
When `format_comp_detail(comp)` is called
Then size_sf is shown formatted with thousands separator (e.g. "10,000 SF")
And asking_rent_psf is shown as currency (e.g. "$75.50/SF/yr")

## Feature: Comp serialization to dict

### Scenario: comp_to_dict returns all fields
Given a `LeaseComp` instance
When `comp_to_dict(comp)` is called
Then a dict is returned with all 18 LeaseComp fields
And date fields are serialized as ISO 8601 strings (YYYY-MM-DD)
And numeric fields remain as numbers (int or float)

### Scenario: comp_to_dict output is round-trip safe
Given a `LeaseComp` instance
When `comp_to_dict(comp)` is called and the result is passed to `LeaseComp.from_dict`
Then the resulting LeaseComp is equal to the original

## Feature: Export to CSV

### Scenario: Export a list of comps to CSV
Given a list of 3 `LeaseComp` instances
And a target path for the CSV file
When `export_comps_to_csv(comps, path)` is called
Then a CSV file is written at the target path
And the CSV has a header row with all field names
And the CSV has 3 data rows, one per comp

### Scenario: Export to CSV returns count of rows written
Given a list of 5 comps
When `export_comps_to_csv(comps, path)` is called
Then the function returns 5 (the number of comps written)

### Scenario: Export empty list to CSV writes header only
Given an empty list of comps
When `export_comps_to_csv(comps, path)` is called
Then a CSV file is written with only a header row
And the function returns 0

### Scenario: CSV dates are ISO 8601 strings
Given a comp with execution_date=2024-03-15
When `export_comps_to_csv([comp], path)` is called
Then the execution_date cell in the CSV is the string "2024-03-15"

### Scenario: CSV file uses comma delimiter
Given a list of comps
When `export_comps_to_csv(comps, path)` is called
Then the resulting file is parseable as a standard comma-delimited CSV

## Feature: Export to JSON

### Scenario: Export a list of comps to JSON
Given a list of 3 `LeaseComp` instances
And a target path for the JSON file
When `export_comps_to_json(comps, path)` is called
Then a JSON file is written at the target path
And the file contains a JSON array with 3 objects

### Scenario: Export to JSON returns count of records written
Given a list of 4 comps
When `export_comps_to_json(comps, path)` is called
Then the function returns 4

### Scenario: Export empty list to JSON writes empty array
Given an empty list of comps
When `export_comps_to_json(comps, path)` is called
Then the JSON file contains `[]`
And the function returns 0

### Scenario: JSON dates are ISO 8601 strings
Given a comp with execution_date=2024-03-15
When `export_comps_to_json([comp], path)` is called
Then the execution_date value in the JSON object is the string "2024-03-15"

### Scenario: JSON export output is round-trip safe
Given a list of comps
When `export_comps_to_json(comps, path)` is called
And the resulting file is loaded with `load_comps_from_json(path)`
Then the loaded comps equal the original comps

## Feature: CLI — show subcommand

### Scenario: CLI show prints detail for an existing comp ID
Given a JSON comps file containing a comp with id "comp-001"
When the CLI is invoked as `comp_detail show <file> comp-001`
Then the detailed view of that comp is printed to stdout
And the process exits with code 0

### Scenario: CLI show exits non-zero for unknown ID
Given a JSON comps file that does not contain id "nonexistent"
When the CLI is invoked as `comp_detail show <file> nonexistent`
Then an error message is printed to stderr
And the process exits with a non-zero code

### Scenario: CLI show exits non-zero for missing file
Given a path to a JSON file that does not exist
When the CLI is invoked as `comp_detail show <missing_file> comp-001`
Then an error message is printed to stderr
And the process exits with code 1

## Feature: CLI — export subcommand

### Scenario: CLI export writes CSV file
Given a JSON comps file with 5 comps
And the `--format csv` flag and an `--output` path
When the CLI is invoked as `comp_detail export <file> --format csv --output out.csv`
Then a CSV file is written at the output path
And the process exits with code 0

### Scenario: CLI export writes JSON file
Given a JSON comps file with 5 comps
And the `--format json` flag and an `--output` path
When the CLI is invoked as `comp_detail export <file> --format json --output out.json`
Then a JSON file is written at the output path
And the process exits with code 0

### Scenario: CLI export with filters exports only matching comps
Given a JSON comps file with comps in "NYC" and "Chicago"
When the CLI is invoked with `--market NYC --format csv --output out.csv`
Then the CSV contains only NYC comps

### Scenario: CLI export prints record count on success
Given a JSON comps file with 3 comps
When the CLI is invoked with export and valid arguments
Then a summary line "Exported 3 comp(s) to <path>" is printed to stdout

### Scenario: CLI export exits non-zero for unrecognized format
Given a JSON comps file
When the CLI is invoked with `--format xlsx`
Then the process exits with a non-zero code and an error message

### Scenario: CLI export exits non-zero for missing file
Given a path to a JSON file that does not exist
When the CLI is invoked with the export subcommand
Then the process exits with code 1 and an error message

## UI Mockup (CLI output)

### show subcommand
```
$ python -m auto_sdd.scripts.comp_detail show comps.json comp-001

Comp ID:          comp-001
Address:          350 Fifth Avenue, New York, NY
Market:           NYC
Submarket:        Midtown
Tenant:           Acme Corp
Landlord:         Rockefeller Group
Execution Date:   2024-01-15
Commencement:     2024-04-01
Expiration:       2034-03-31
Term:             120 months
Size:             12,500 SF
Asking Rent:      $75.00/SF/yr
Effective Rent:   $68.00/SF/yr
Free Rent:        6 months
Lease Type:       Direct
Property Type:    Office
Floor:            22
Source:           CoStar
```

### export subcommand
```
$ python -m auto_sdd.scripts.comp_detail export comps.json --format csv --output comps_export.csv

Exported 3 comp(s) to comps_export.csv
```

## Learnings

- `comp_to_dict` with ISO-format date strings enables round-trip serialization through both CSV and JSON without custom deserializers.
- Exporting returns the count of written records so callers can report progress without re-reading the file.
