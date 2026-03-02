"""
Comp detail view and export library.

Provides detailed formatting of a single LeaseComp and bulk export
of lease comp lists to CSV and JSON formats.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from auto_sdd.lib.lease_comp_search import LeaseComp


def format_comp_detail(comp: LeaseComp) -> str:
    """Format a single LeaseComp as a detailed multi-line block.

    All fields are shown with human-readable labels. Numeric values
    are formatted for readability (thousands separators, currency notation).

    Args:
        comp: The lease comp to format.

    Returns:
        A multi-line string ready for terminal output.
    """
    lines = [
        f"Comp ID:          {comp.id}",
        f"Address:          {comp.property_address}",
        f"Market:           {comp.market}",
        f"Submarket:        {comp.submarket}",
        f"Tenant:           {comp.tenant}",
        f"Landlord:         {comp.landlord}",
        f"Execution Date:   {comp.execution_date.isoformat()}",
        f"Commencement:     {comp.commencement_date.isoformat()}",
        f"Expiration:       {comp.expiration_date.isoformat()}",
        f"Term:             {comp.term_months} months",
        f"Size:             {comp.size_sf:,} SF",
        f"Asking Rent:      ${comp.asking_rent_psf:.2f}/SF/yr",
        f"Effective Rent:   ${comp.effective_rent_psf:.2f}/SF/yr",
        f"Free Rent:        {comp.free_rent_months} months",
        f"Lease Type:       {comp.lease_type}",
        f"Property Type:    {comp.property_type}",
        f"Floor:            {comp.floor}",
        f"Source:           {comp.source}",
    ]
    return "\n".join(lines)


def comp_to_dict(comp: LeaseComp) -> dict:
    """Serialize a LeaseComp to a plain dict.

    Date fields are converted to ISO 8601 strings (YYYY-MM-DD).
    All other fields retain their native Python types (int, float, str).

    Args:
        comp: The lease comp to serialize.

    Returns:
        A dict with all 18 LeaseComp fields.
    """
    return {
        "id": comp.id,
        "property_address": comp.property_address,
        "market": comp.market,
        "submarket": comp.submarket,
        "tenant": comp.tenant,
        "landlord": comp.landlord,
        "execution_date": comp.execution_date.isoformat(),
        "commencement_date": comp.commencement_date.isoformat(),
        "expiration_date": comp.expiration_date.isoformat(),
        "term_months": comp.term_months,
        "size_sf": comp.size_sf,
        "asking_rent_psf": comp.asking_rent_psf,
        "effective_rent_psf": comp.effective_rent_psf,
        "free_rent_months": comp.free_rent_months,
        "lease_type": comp.lease_type,
        "property_type": comp.property_type,
        "floor": comp.floor,
        "source": comp.source,
    }


def export_comps_to_csv(comps: list[LeaseComp], path: Path) -> int:
    """Export a list of lease comps to a CSV file.

    The CSV has a header row with all field names followed by one data
    row per comp. Date fields are written as ISO 8601 strings.

    Args:
        comps: List of LeaseComp instances to export. May be empty.
        path: Destination file path. Parent directories must exist.

    Returns:
        Number of data rows written (equal to len(comps)).
    """
    path = Path(path)
    fieldnames = [
        "id", "property_address", "market", "submarket",
        "tenant", "landlord", "execution_date", "commencement_date",
        "expiration_date", "term_months", "size_sf", "asking_rent_psf",
        "effective_rent_psf", "free_rent_months", "lease_type",
        "property_type", "floor", "source",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for comp in comps:
            writer.writerow(comp_to_dict(comp))
    return len(comps)


def export_comps_to_json(comps: list[LeaseComp], path: Path) -> int:
    """Export a list of lease comps to a JSON file.

    The file contains a JSON array with one object per comp.
    Date fields are written as ISO 8601 strings so the output is
    directly loadable by `load_comps_from_json`.

    Args:
        comps: List of LeaseComp instances to export. May be empty.
        path: Destination file path. Parent directories must exist.

    Returns:
        Number of records written (equal to len(comps)).
    """
    path = Path(path)
    records = [comp_to_dict(comp) for comp in comps]
    path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return len(comps)
