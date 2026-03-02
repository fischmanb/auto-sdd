# CONVERSION CHANGELOG
# - New module, no bash original.
# - Roadmap parsing uses line-by-line regex (no YAML library) to match status
#   symbols in Markdown table rows, matching the approach used by generate_mapping.py.
# - JSONL reading is done by loading each line as JSON and picking the last
#   entry with a timestamp field; no pandas or external deps required.
# - Auth display: shows key length only, never the key value itself.

"""CLI status dashboard for auto-sdd.

Displays a concise overview of:
- ANTHROPIC_API_KEY presence and length
- Roadmap progress (completed / in-progress / pending counts)
- Build loop lock status (running or idle)
- Most recent cost-log entry from general-estimates.jsonl

Usage:
    python -m auto_sdd.scripts.dashboard [project_dir]

If ``project_dir`` is omitted, the parent directory of this file's package
root is used (i.e., the repository root containing ``.specs/``).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Status symbols used in roadmap.md table rows
_STATUS_COMPLETED = "✅"
_STATUS_IN_PROGRESS = "🔄"
_STATUS_PENDING = "⬜"
_STATUS_BLOCKED = "⏸️"

# Lock file name written by build_loop.py / build-loop-local.sh
_LOCK_FILENAME = "build.lock"

# JSONL cost log filename
_COST_LOG_FILENAME = "general-estimates.jsonl"


# ── Roadmap parsing ───────────────────────────────────────────────────────────


def _count_roadmap_statuses(roadmap_path: Path) -> dict[str, int]:
    """Count feature rows in roadmap.md by status symbol.

    Only real table rows (not template HTML-comment rows) are counted.
    A real row is one where the status cell contains one of the four status
    symbols and is NOT wrapped in HTML comment markers (``<!-- ... -->``).

    Args:
        roadmap_path: Path to ``roadmap.md``.

    Returns:
        Dict with keys "completed", "in_progress", "pending", "blocked".
    """
    counts: dict[str, int] = {
        "completed": 0,
        "in_progress": 0,
        "pending": 0,
        "blocked": 0,
    }

    if not roadmap_path.exists():
        return counts

    text = roadmap_path.read_text()

    for line in text.splitlines():
        # Skip HTML comment lines (template placeholders)
        if "<!--" in line and "-->" in line:
            continue
        # Must be a Markdown table row (starts with |)
        if not line.strip().startswith("|"):
            continue

        if _STATUS_COMPLETED in line:
            counts["completed"] += 1
        elif _STATUS_IN_PROGRESS in line:
            counts["in_progress"] += 1
        elif _STATUS_PENDING in line:
            counts["pending"] += 1
        elif _STATUS_BLOCKED in line:
            counts["blocked"] += 1

    return counts


# ── Cost log parsing ──────────────────────────────────────────────────────────


def _read_last_cost_entry(cost_log_path: Path) -> dict[str, object] | None:
    """Return the last JSONL record that has a ``timestamp`` field.

    Args:
        cost_log_path: Path to ``general-estimates.jsonl``.

    Returns:
        The parsed dict of the last timestamped record, or None if the file
        is absent or contains no valid records.
    """
    if not cost_log_path.exists():
        return None

    last: dict[str, object] | None = None
    try:
        for raw_line in cost_log_path.read_text().splitlines():
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                record: dict[str, object] = json.loads(raw_line)
                if "timestamp" in record:
                    last = record
            except json.JSONDecodeError:
                logger.debug("Skipping malformed JSONL line: %r", raw_line)
    except OSError as exc:
        logger.warning("Could not read cost log %s: %s", cost_log_path, exc)
        return None

    return last


# ── Lock status ───────────────────────────────────────────────────────────────


def _build_loop_status(project_dir: Path) -> str:
    """Return a human-readable status string for the build loop.

    Checks for the presence of ``build.lock`` in ``project_dir``.  If the
    lock file exists, the loop is considered running.  Otherwise it is idle.

    Returns:
        ``"running (lock file present)"`` or ``"idle (no lock file)"``.
    """
    lock_path = project_dir / _LOCK_FILENAME
    if lock_path.exists():
        return "running (lock file present)"
    return "idle (no lock file)"


# ── Auth display ──────────────────────────────────────────────────────────────


def _api_key_status() -> str:
    """Return a display string for the Anthropic API key.

    Never reveals the key value — only whether it is set and its length.
    """
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return f"✓ set ({len(key)} chars)"
    return "✗ NOT SET — builds will fail"


# ── Dashboard rendering ───────────────────────────────────────────────────────


def render_dashboard(project_dir: Path) -> str:
    """Build the full dashboard output string.

    Args:
        project_dir: Root directory of the auto-sdd project.

    Returns:
        Multi-line string ready to print to stdout.
    """
    project_dir = project_dir.resolve()
    lines: list[str] = []

    lines.append("=== auto-sdd Dashboard ===")
    lines.append(f"Project: {project_dir}")
    lines.append("")

    # Auth section
    lines.append("  Auth")
    lines.append(f"  ANTHROPIC_API_KEY  {_api_key_status()}")
    lines.append("")

    # Roadmap section
    roadmap_path = project_dir / ".specs" / "roadmap.md"
    counts = _count_roadmap_statuses(roadmap_path)
    lines.append("  Roadmap")
    lines.append(f"  {_STATUS_COMPLETED} Completed    {counts['completed']}")
    lines.append(f"  {_STATUS_IN_PROGRESS} In Progress  {counts['in_progress']}")
    lines.append(f"  {_STATUS_PENDING} Pending      {counts['pending']}")
    if counts["blocked"]:
        lines.append(f"  {_STATUS_BLOCKED} Blocked      {counts['blocked']}")
    lines.append("")

    # Build loop section
    loop_status = _build_loop_status(project_dir)
    lines.append("  Build Loop")
    lines.append(f"  Status: {loop_status}")
    lines.append("")

    # Recent activity section
    cost_log_path = project_dir / _COST_LOG_FILENAME
    last_entry = _read_last_cost_entry(cost_log_path)
    lines.append("  Recent Activity")
    if last_entry is None:
        lines.append("  No cost data available.")
    else:
        ts = last_entry.get("timestamp", "unknown")
        activity = last_entry.get("activity_type", "unknown")
        lines.append(f"  Last entry: {ts}  {activity}")

    return "\n".join(lines)


# ── Entry point ───────────────────────────────────────────────────────────────


def _default_project_dir() -> Path:
    """Return the project root directory.

    Walks up from this file's location until it finds a directory containing
    ``.specs/``.  Falls back to the current working directory.
    """
    # This file is at: <project_root>/py/auto_sdd/scripts/dashboard.py
    # Walk up 3 levels to reach project root.
    candidate = Path(__file__).resolve().parent.parent.parent.parent
    if (candidate / ".specs").exists():
        return candidate
    # Fallback: search cwd upward
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".specs").exists():
            return parent
    return cwd


def main(argv: list[str] | None = None) -> int:
    """Dashboard CLI entry point.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 on success).
    """
    logging.basicConfig(
        level=logging.WARNING,
        format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser(
        description="Show auto-sdd project status dashboard."
    )
    parser.add_argument(
        "project_dir",
        nargs="?",
        type=Path,
        default=None,
        help="Path to the auto-sdd project root (default: auto-detected from .specs/)",
    )
    args = parser.parse_args(argv)

    project_dir: Path = args.project_dir if args.project_dir is not None else _default_project_dir()

    output = render_dashboard(project_dir)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
