"""
CLI entrypoint for comp detail view and export.

Usage:
    python -m auto_sdd.scripts.comp_detail show <comps.json> <comp-id>
    python -m auto_sdd.scripts.comp_detail export <comps.json> --format csv --output <path>
    python -m auto_sdd.scripts.comp_detail export <comps.json> --format json --output <path>

The export subcommand supports the same filters as lease_comp_search.

Export filter options:
    --market TEXT           Filter by market (case-insensitive)
    --submarket TEXT        Filter by submarket (case-insensitive)
    --property-type TEXT    Filter by property type (e.g., Office, Retail)
    --lease-type TEXT       Filter by lease type (e.g., Direct, Sublease)
    --min-size INT          Minimum size in square feet
    --max-size INT          Maximum size in square feet
    --min-rent FLOAT        Minimum asking rent ($/SF/year)
    --max-rent FLOAT        Maximum asking rent ($/SF/year)
    --after DATE            Only comps executed on or after this date (YYYY-MM-DD)
    --before DATE           Only comps executed on or before this date (YYYY-MM-DD)
    --tenant TEXT           Filter by tenant name substring
    --landlord TEXT         Filter by landlord name substring
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from auto_sdd.lib.comp_detail import (
    export_comps_to_csv,
    export_comps_to_json,
    format_comp_detail,
)
from auto_sdd.lib.lease_comp_search import (
    LeaseCompFilter,
    load_comps_from_json,
    search_comps,
)

_SUPPORTED_FORMATS = ("csv", "json")


def _parse_date_arg(value: str | None, flag: str) -> "datetime.date | None":
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise SystemExit(
            f"error: invalid date for {flag}: {value!r} (expected YYYY-MM-DD)"
        )


def _add_filter_args(parser: argparse.ArgumentParser) -> None:
    """Attach the shared filtering arguments to a subcommand parser."""
    parser.add_argument("--market", default=None, help="Filter by market (e.g., NYC)")
    parser.add_argument("--submarket", default=None, help="Filter by submarket")
    parser.add_argument(
        "--property-type", dest="property_type", default=None,
        help="Filter by property type (e.g., Office, Retail, Industrial)",
    )
    parser.add_argument(
        "--lease-type", dest="lease_type", default=None,
        help="Filter by lease type (e.g., Direct, Sublease)",
    )
    parser.add_argument(
        "--min-size", dest="min_size", type=int, default=None,
        help="Minimum size in square feet (inclusive)",
    )
    parser.add_argument(
        "--max-size", dest="max_size", type=int, default=None,
        help="Maximum size in square feet (inclusive)",
    )
    parser.add_argument(
        "--min-rent", dest="min_rent", type=float, default=None,
        help="Minimum asking rent in $/SF/year (inclusive)",
    )
    parser.add_argument(
        "--max-rent", dest="max_rent", type=float, default=None,
        help="Maximum asking rent in $/SF/year (inclusive)",
    )
    parser.add_argument(
        "--after", default=None,
        help="Only comps executed on or after this date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--before", default=None,
        help="Only comps executed on or before this date (YYYY-MM-DD, inclusive)",
    )
    parser.add_argument(
        "--tenant", default=None,
        help="Filter by tenant name substring (case-insensitive)",
    )
    parser.add_argument(
        "--landlord", default=None,
        help="Filter by landlord name substring (case-insensitive)",
    )


def _build_filter(args: argparse.Namespace) -> LeaseCompFilter:
    after = _parse_date_arg(getattr(args, "after", None), "--after")
    before = _parse_date_arg(getattr(args, "before", None), "--before")
    return LeaseCompFilter(
        market=getattr(args, "market", None),
        submarket=getattr(args, "submarket", None),
        property_type=getattr(args, "property_type", None),
        lease_type=getattr(args, "lease_type", None),
        min_size_sf=getattr(args, "min_size", None),
        max_size_sf=getattr(args, "max_size", None),
        min_rent_psf=getattr(args, "min_rent", None),
        max_rent_psf=getattr(args, "max_rent", None),
        executed_after=after,
        executed_before=before,
        tenant_contains=getattr(args, "tenant", None),
        landlord_contains=getattr(args, "landlord", None),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="comp_detail",
        description="View details for a single comp or export comps to CSV/JSON.",
    )
    sub = parser.add_subparsers(dest="subcommand")

    # --- show subcommand ---
    show_p = sub.add_parser(
        "show",
        help="Display all fields for a single comp identified by its ID.",
    )
    show_p.add_argument(
        "file", type=Path,
        help="Path to JSON file containing lease comp records.",
    )
    show_p.add_argument(
        "comp_id",
        help="ID of the comp to display.",
    )

    # --- export subcommand ---
    export_p = sub.add_parser(
        "export",
        help="Export comps (with optional filters) to CSV or JSON.",
    )
    export_p.add_argument(
        "file", type=Path,
        help="Path to JSON file containing lease comp records.",
    )
    export_p.add_argument(
        "--format", dest="fmt", choices=_SUPPORTED_FORMATS, required=True,
        help="Output format: csv or json.",
    )
    export_p.add_argument(
        "--output", "-o", dest="output", type=Path, required=True,
        help="Destination file path for the export.",
    )
    _add_filter_args(export_p)

    return parser


def _cmd_show(args: argparse.Namespace) -> int:
    try:
        comps = load_comps_from_json(args.file)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    match = next((c for c in comps if c.id == args.comp_id), None)
    if match is None:
        print(
            f"error: comp ID {args.comp_id!r} not found in {args.file}",
            file=sys.stderr,
        )
        return 1

    print(format_comp_detail(match))
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    try:
        comps = load_comps_from_json(args.file)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    filters = _build_filter(args)
    results = search_comps(comps, filters)

    if args.fmt == "csv":
        count = export_comps_to_csv(results, args.output)
    else:
        count = export_comps_to_json(results, args.output)

    print(f"Exported {count} comp(s) to {args.output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the comp detail CLI.

    Returns:
        Exit code (0 = success, non-zero = error).
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "show":
        return _cmd_show(args)
    if args.subcommand == "export":
        return _cmd_export(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
