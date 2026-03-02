"""Tests for comp detail view and export (Feature #3).

Covers: format_comp_detail, comp_to_dict, export_comps_to_csv,
        export_comps_to_json, and the CLI show / export subcommands.

Test ID prefix: CD
"""

import csv
import json
import sys
from datetime import date
from pathlib import Path

import pytest

from auto_sdd.lib.comp_detail import (
    comp_to_dict,
    export_comps_to_csv,
    export_comps_to_json,
    format_comp_detail,
)
from auto_sdd.lib.lease_comp_search import LeaseComp, load_comps_from_json
from auto_sdd.scripts.comp_detail import main as cli_main


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_comp(**overrides) -> LeaseComp:
    """Return a valid LeaseComp, optionally overriding specific fields."""
    defaults = {
        "id": "comp-001",
        "property_address": "350 Fifth Avenue, New York, NY",
        "market": "NYC",
        "submarket": "Midtown",
        "tenant": "Acme Corp",
        "landlord": "Rockefeller Group",
        "execution_date": date(2024, 1, 15),
        "commencement_date": date(2024, 4, 1),
        "expiration_date": date(2034, 3, 31),
        "term_months": 120,
        "size_sf": 12500,
        "asking_rent_psf": 75.0,
        "effective_rent_psf": 68.0,
        "free_rent_months": 6,
        "lease_type": "Direct",
        "property_type": "Office",
        "floor": "22",
        "source": "CoStar",
    }
    defaults.update(overrides)
    return LeaseComp(**defaults)


def _make_comp_dict(**overrides) -> dict:
    """Return a valid comp dict (as loaded from JSON), optionally overriding fields."""
    defaults = {
        "id": "comp-001",
        "property_address": "350 Fifth Avenue, New York, NY",
        "market": "NYC",
        "submarket": "Midtown",
        "tenant": "Acme Corp",
        "landlord": "Rockefeller Group",
        "execution_date": "2024-01-15",
        "commencement_date": "2024-04-01",
        "expiration_date": "2034-03-31",
        "term_months": 120,
        "size_sf": 12500,
        "asking_rent_psf": 75.0,
        "effective_rent_psf": 68.0,
        "free_rent_months": 6,
        "lease_type": "Direct",
        "property_type": "Office",
        "floor": "22",
        "source": "CoStar",
    }
    defaults.update(overrides)
    return defaults


def _write_comps_json(path: Path, comps: list[LeaseComp]) -> None:
    """Write a list of LeaseComp instances to a JSON file."""
    records = [comp_to_dict(c) for c in comps]
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# CD-001 – CD-010: format_comp_detail
# ---------------------------------------------------------------------------

class TestFormatCompDetail:

    def test_CD001_returns_string(self):
        comp = _make_comp()
        result = format_comp_detail(comp)
        assert isinstance(result, str)

    def test_CD002_contains_comp_id(self):
        comp = _make_comp(id="cd-test-99")
        result = format_comp_detail(comp)
        assert "cd-test-99" in result

    def test_CD003_contains_address(self):
        comp = _make_comp(property_address="1 World Trade Center")
        result = format_comp_detail(comp)
        assert "1 World Trade Center" in result

    def test_CD004_contains_all_expected_labels(self):
        comp = _make_comp()
        result = format_comp_detail(comp)
        expected_labels = [
            "Comp ID",
            "Address",
            "Market",
            "Submarket",
            "Tenant",
            "Landlord",
            "Execution Date",
            "Commencement",
            "Expiration",
            "Term",
            "Size",
            "Asking Rent",
            "Effective Rent",
            "Free Rent",
            "Lease Type",
            "Property Type",
            "Floor",
            "Source",
        ]
        for label in expected_labels:
            assert label in result, f"Missing label: {label!r}"

    def test_CD005_size_formatted_with_thousands_separator(self):
        comp = _make_comp(size_sf=10000)
        result = format_comp_detail(comp)
        assert "10,000" in result

    def test_CD006_asking_rent_formatted_as_currency(self):
        comp = _make_comp(asking_rent_psf=75.50)
        result = format_comp_detail(comp)
        assert "$75.50" in result

    def test_CD007_effective_rent_formatted_as_currency(self):
        comp = _make_comp(effective_rent_psf=68.00)
        result = format_comp_detail(comp)
        assert "$68.00" in result

    def test_CD008_execution_date_iso_format(self):
        comp = _make_comp(execution_date=date(2024, 3, 15))
        result = format_comp_detail(comp)
        assert "2024-03-15" in result

    def test_CD009_is_multiline(self):
        comp = _make_comp()
        result = format_comp_detail(comp)
        assert "\n" in result
        assert len(result.splitlines()) >= 18

    def test_CD010_contains_market_and_submarket(self):
        comp = _make_comp(market="Chicago", submarket="Loop")
        result = format_comp_detail(comp)
        assert "Chicago" in result
        assert "Loop" in result


# ---------------------------------------------------------------------------
# CD-011 – CD-020: comp_to_dict
# ---------------------------------------------------------------------------

class TestCompToDict:

    def test_CD011_returns_dict(self):
        comp = _make_comp()
        result = comp_to_dict(comp)
        assert isinstance(result, dict)

    def test_CD012_has_all_18_fields(self):
        comp = _make_comp()
        result = comp_to_dict(comp)
        assert len(result) == 18

    def test_CD013_date_fields_are_strings(self):
        comp = _make_comp()
        result = comp_to_dict(comp)
        assert isinstance(result["execution_date"], str)
        assert isinstance(result["commencement_date"], str)
        assert isinstance(result["expiration_date"], str)

    def test_CD014_date_strings_are_iso_format(self):
        comp = _make_comp(execution_date=date(2024, 3, 15))
        result = comp_to_dict(comp)
        assert result["execution_date"] == "2024-03-15"

    def test_CD015_numeric_fields_retain_type(self):
        comp = _make_comp(size_sf=5000, asking_rent_psf=42.5)
        result = comp_to_dict(comp)
        assert isinstance(result["size_sf"], int)
        assert isinstance(result["asking_rent_psf"], float)

    def test_CD016_round_trip_via_from_dict(self):
        comp = _make_comp()
        d = comp_to_dict(comp)
        restored = LeaseComp.from_dict(d)
        assert restored.id == comp.id
        assert restored.execution_date == comp.execution_date
        assert restored.size_sf == comp.size_sf
        assert restored.asking_rent_psf == comp.asking_rent_psf

    def test_CD017_all_fields_present_by_name(self):
        comp = _make_comp()
        result = comp_to_dict(comp)
        for key in [
            "id", "property_address", "market", "submarket",
            "tenant", "landlord", "execution_date", "commencement_date",
            "expiration_date", "term_months", "size_sf", "asking_rent_psf",
            "effective_rent_psf", "free_rent_months", "lease_type",
            "property_type", "floor", "source",
        ]:
            assert key in result, f"Missing key: {key!r}"

    def test_CD018_string_fields_are_strings(self):
        comp = _make_comp()
        result = comp_to_dict(comp)
        for key in ["id", "market", "tenant", "landlord", "lease_type",
                    "property_type", "floor", "source"]:
            assert isinstance(result[key], str), f"{key} should be str"

    def test_CD019_free_rent_months_is_int(self):
        comp = _make_comp(free_rent_months=3)
        result = comp_to_dict(comp)
        assert result["free_rent_months"] == 3
        assert isinstance(result["free_rent_months"], int)

    def test_CD020_term_months_is_int(self):
        comp = _make_comp(term_months=60)
        result = comp_to_dict(comp)
        assert result["term_months"] == 60
        assert isinstance(result["term_months"], int)


# ---------------------------------------------------------------------------
# CD-021 – CD-030: export_comps_to_csv
# ---------------------------------------------------------------------------

class TestExportCompsToCSV:

    def test_CD021_creates_file(self, tmp_path):
        comp = _make_comp()
        out = tmp_path / "out.csv"
        export_comps_to_csv([comp], out)
        assert out.exists()

    def test_CD022_returns_count_of_rows_written(self, tmp_path):
        comps = [_make_comp(id=f"c{i}") for i in range(5)]
        out = tmp_path / "out.csv"
        count = export_comps_to_csv(comps, out)
        assert count == 5

    def test_CD023_empty_list_writes_header_only(self, tmp_path):
        out = tmp_path / "out.csv"
        count = export_comps_to_csv([], out)
        assert count == 0
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert rows == []

    def test_CD024_empty_list_returns_zero(self, tmp_path):
        out = tmp_path / "out.csv"
        result = export_comps_to_csv([], out)
        assert result == 0

    def test_CD025_csv_has_header_row(self, tmp_path):
        comp = _make_comp()
        out = tmp_path / "out.csv"
        export_comps_to_csv([comp], out)
        with out.open(encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
        assert "id" in header
        assert "market" in header
        assert "execution_date" in header

    def test_CD026_csv_date_is_iso_string(self, tmp_path):
        comp = _make_comp(execution_date=date(2024, 3, 15))
        out = tmp_path / "out.csv"
        export_comps_to_csv([comp], out)
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert rows[0]["execution_date"] == "2024-03-15"

    def test_CD027_csv_three_comps_three_rows(self, tmp_path):
        comps = [_make_comp(id=f"x{i}") for i in range(3)]
        out = tmp_path / "out.csv"
        export_comps_to_csv(comps, out)
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert len(rows) == 3

    def test_CD028_csv_is_comma_delimited(self, tmp_path):
        comp = _make_comp()
        out = tmp_path / "out.csv"
        export_comps_to_csv([comp], out)
        raw = out.read_text(encoding="utf-8")
        first_line = raw.splitlines()[0]
        assert "," in first_line

    def test_CD029_csv_id_field_matches_comp(self, tmp_path):
        comp = _make_comp(id="unique-id-123")
        out = tmp_path / "out.csv"
        export_comps_to_csv([comp], out)
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert rows[0]["id"] == "unique-id-123"

    def test_CD030_csv_size_sf_is_integer_string(self, tmp_path):
        comp = _make_comp(size_sf=7500)
        out = tmp_path / "out.csv"
        export_comps_to_csv([comp], out)
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert rows[0]["size_sf"] == "7500"


# ---------------------------------------------------------------------------
# CD-031 – CD-040: export_comps_to_json
# ---------------------------------------------------------------------------

class TestExportCompsToJSON:

    def test_CD031_creates_file(self, tmp_path):
        comp = _make_comp()
        out = tmp_path / "out.json"
        export_comps_to_json([comp], out)
        assert out.exists()

    def test_CD032_returns_count_of_records_written(self, tmp_path):
        comps = [_make_comp(id=f"j{i}") for i in range(4)]
        out = tmp_path / "out.json"
        count = export_comps_to_json(comps, out)
        assert count == 4

    def test_CD033_empty_list_writes_empty_array(self, tmp_path):
        out = tmp_path / "out.json"
        export_comps_to_json([], out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data == []

    def test_CD034_empty_list_returns_zero(self, tmp_path):
        out = tmp_path / "out.json"
        result = export_comps_to_json([], out)
        assert result == 0

    def test_CD035_json_is_array(self, tmp_path):
        comp = _make_comp()
        out = tmp_path / "out.json"
        export_comps_to_json([comp], out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert isinstance(data, list)

    def test_CD036_json_three_comps_three_records(self, tmp_path):
        comps = [_make_comp(id=f"jx{i}") for i in range(3)]
        out = tmp_path / "out.json"
        export_comps_to_json(comps, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert len(data) == 3

    def test_CD037_json_date_is_iso_string(self, tmp_path):
        comp = _make_comp(execution_date=date(2024, 3, 15))
        out = tmp_path / "out.json"
        export_comps_to_json([comp], out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data[0]["execution_date"] == "2024-03-15"

    def test_CD038_json_round_trip_via_load_comps_from_json(self, tmp_path):
        comp = _make_comp()
        out = tmp_path / "round_trip.json"
        export_comps_to_json([comp], out)
        loaded = load_comps_from_json(out)
        assert len(loaded) == 1
        assert loaded[0].id == comp.id
        assert loaded[0].execution_date == comp.execution_date
        assert loaded[0].size_sf == comp.size_sf

    def test_CD039_json_file_is_valid_json(self, tmp_path):
        comp = _make_comp()
        out = tmp_path / "out.json"
        export_comps_to_json([comp], out)
        # Should not raise
        json.loads(out.read_text(encoding="utf-8"))

    def test_CD040_json_id_field_matches_comp(self, tmp_path):
        comp = _make_comp(id="json-id-456")
        out = tmp_path / "out.json"
        export_comps_to_json([comp], out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data[0]["id"] == "json-id-456"


# ---------------------------------------------------------------------------
# CD-041 – CD-050: CLI — show subcommand
# ---------------------------------------------------------------------------

class TestCLIShow:

    def test_CD041_show_exits_0_for_valid_comp(self, tmp_path):
        comp = _make_comp(id="show-test")
        jf = tmp_path / "comps.json"
        _write_comps_json(jf, [comp])
        rc = cli_main(["show", str(jf), "show-test"])
        assert rc == 0

    def test_CD042_show_prints_comp_detail(self, tmp_path, capsys):
        comp = _make_comp(id="show-print")
        jf = tmp_path / "comps.json"
        _write_comps_json(jf, [comp])
        cli_main(["show", str(jf), "show-print"])
        captured = capsys.readouterr()
        assert "show-print" in captured.out
        assert "Comp ID" in captured.out

    def test_CD043_show_exits_nonzero_for_unknown_id(self, tmp_path):
        comp = _make_comp(id="real-id")
        jf = tmp_path / "comps.json"
        _write_comps_json(jf, [comp])
        rc = cli_main(["show", str(jf), "nonexistent-id"])
        assert rc != 0

    def test_CD044_show_prints_error_to_stderr_for_unknown_id(self, tmp_path, capsys):
        comp = _make_comp(id="real-id")
        jf = tmp_path / "comps.json"
        _write_comps_json(jf, [comp])
        cli_main(["show", str(jf), "ghost"])
        captured = capsys.readouterr()
        assert "error" in captured.err.lower() or "ghost" in captured.err

    def test_CD045_show_exits_1_for_missing_file(self, tmp_path):
        rc = cli_main(["show", str(tmp_path / "missing.json"), "any-id"])
        assert rc == 1

    def test_CD046_show_prints_all_field_labels(self, tmp_path, capsys):
        comp = _make_comp(id="all-fields")
        jf = tmp_path / "comps.json"
        _write_comps_json(jf, [comp])
        cli_main(["show", str(jf), "all-fields"])
        out = capsys.readouterr().out
        for label in ["Tenant", "Market", "Size", "Asking Rent", "Lease Type"]:
            assert label in out, f"Missing label in output: {label!r}"

    def test_CD047_show_finds_correct_comp_among_multiple(self, tmp_path, capsys):
        comps = [
            _make_comp(id="alpha", tenant="AlphaCorp"),
            _make_comp(id="beta", tenant="BetaInc"),
        ]
        jf = tmp_path / "comps.json"
        _write_comps_json(jf, comps)
        cli_main(["show", str(jf), "beta"])
        out = capsys.readouterr().out
        assert "BetaInc" in out
        assert "AlphaCorp" not in out

    def test_CD048_show_exits_1_for_malformed_json(self, tmp_path):
        jf = tmp_path / "bad.json"
        jf.write_text("not valid json", encoding="utf-8")
        rc = cli_main(["show", str(jf), "any"])
        assert rc == 1


# ---------------------------------------------------------------------------
# CD-051 – CD-065: CLI — export subcommand
# ---------------------------------------------------------------------------

class TestCLIExport:

    def test_CD051_export_csv_exits_0(self, tmp_path):
        comp = _make_comp()
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.csv"
        _write_comps_json(jf, [comp])
        rc = cli_main(["export", str(jf), "--format", "csv", "--output", str(out)])
        assert rc == 0

    def test_CD052_export_csv_creates_file(self, tmp_path):
        comp = _make_comp()
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.csv"
        _write_comps_json(jf, [comp])
        cli_main(["export", str(jf), "--format", "csv", "--output", str(out)])
        assert out.exists()

    def test_CD053_export_json_exits_0(self, tmp_path):
        comp = _make_comp()
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.json"
        _write_comps_json(jf, [comp])
        rc = cli_main(["export", str(jf), "--format", "json", "--output", str(out)])
        assert rc == 0

    def test_CD054_export_json_creates_file(self, tmp_path):
        comp = _make_comp()
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.json"
        _write_comps_json(jf, [comp])
        cli_main(["export", str(jf), "--format", "json", "--output", str(out)])
        assert out.exists()

    def test_CD055_export_prints_record_count(self, tmp_path, capsys):
        comps = [_make_comp(id=f"e{i}") for i in range(3)]
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.csv"
        _write_comps_json(jf, comps)
        cli_main(["export", str(jf), "--format", "csv", "--output", str(out)])
        captured = capsys.readouterr()
        assert "3" in captured.out
        assert "Exported" in captured.out

    def test_CD056_export_with_market_filter_exports_only_matching(self, tmp_path):
        nyc = _make_comp(id="nyc", market="NYC")
        chi = _make_comp(id="chi", market="Chicago")
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.csv"
        _write_comps_json(jf, [nyc, chi])
        cli_main([
            "export", str(jf),
            "--format", "csv",
            "--output", str(out),
            "--market", "NYC",
        ])
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert len(rows) == 1
        assert rows[0]["id"] == "nyc"

    def test_CD057_export_json_round_trip(self, tmp_path):
        comp = _make_comp()
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.json"
        _write_comps_json(jf, [comp])
        cli_main(["export", str(jf), "--format", "json", "--output", str(out)])
        loaded = load_comps_from_json(out)
        assert len(loaded) == 1
        assert loaded[0].id == comp.id

    def test_CD058_export_exits_1_for_missing_file(self, tmp_path):
        out = tmp_path / "out.csv"
        rc = cli_main([
            "export", str(tmp_path / "missing.json"),
            "--format", "csv", "--output", str(out),
        ])
        assert rc == 1

    def test_CD059_export_filter_no_matches_exports_zero(self, tmp_path, capsys):
        comp = _make_comp(market="NYC")
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.csv"
        _write_comps_json(jf, [comp])
        cli_main([
            "export", str(jf),
            "--format", "csv",
            "--output", str(out),
            "--market", "Boston",
        ])
        captured = capsys.readouterr()
        assert "0" in captured.out
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert rows == []

    def test_CD060_export_all_comps_when_no_filter(self, tmp_path):
        comps = [_make_comp(id=f"all{i}") for i in range(5)]
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.csv"
        _write_comps_json(jf, comps)
        cli_main(["export", str(jf), "--format", "csv", "--output", str(out)])
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert len(rows) == 5

    def test_CD061_export_json_summary_includes_path(self, tmp_path, capsys):
        comp = _make_comp()
        jf = tmp_path / "comps.json"
        out = tmp_path / "export_out.json"
        _write_comps_json(jf, [comp])
        cli_main(["export", str(jf), "--format", "json", "--output", str(out)])
        captured = capsys.readouterr()
        assert "export_out.json" in captured.out

    def test_CD062_export_exits_1_for_malformed_json_source(self, tmp_path):
        jf = tmp_path / "bad.json"
        jf.write_text("not valid json", encoding="utf-8")
        out = tmp_path / "out.csv"
        rc = cli_main(["export", str(jf), "--format", "csv", "--output", str(out)])
        assert rc == 1

    def test_CD063_no_subcommand_exits_nonzero(self):
        rc = cli_main([])
        assert rc != 0

    def test_CD064_export_csv_tenant_filter(self, tmp_path):
        comp_a = _make_comp(id="t1", tenant="Google LLC")
        comp_b = _make_comp(id="t2", tenant="Amazon Inc")
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.csv"
        _write_comps_json(jf, [comp_a, comp_b])
        cli_main([
            "export", str(jf),
            "--format", "csv",
            "--output", str(out),
            "--tenant", "amazon",
        ])
        rows = list(csv.DictReader(out.open(encoding="utf-8")))
        assert len(rows) == 1
        assert rows[0]["tenant"] == "Amazon Inc"

    def test_CD065_export_json_size_filter(self, tmp_path):
        small = _make_comp(id="s", size_sf=2000)
        large = _make_comp(id="l", size_sf=15000)
        jf = tmp_path / "comps.json"
        out = tmp_path / "out.json"
        _write_comps_json(jf, [small, large])
        cli_main([
            "export", str(jf),
            "--format", "json",
            "--output", str(out),
            "--min-size", "10000",
        ])
        data = json.loads(out.read_text(encoding="utf-8"))
        assert len(data) == 1
        assert data[0]["id"] == "l"
