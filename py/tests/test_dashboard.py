"""Tests for auto_sdd.scripts.dashboard — CLI status dashboard."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_sdd.scripts.dashboard import (
    _api_key_status,
    _build_loop_status,
    _count_roadmap_statuses,
    _read_last_cost_entry,
    render_dashboard,
    main,
)


# ── _count_roadmap_statuses ───────────────────────────────────────────────────


def test_count_roadmap_statuses_returns_zeros_when_file_absent(tmp_path: Path) -> None:
    counts = _count_roadmap_statuses(tmp_path / "roadmap.md")
    assert counts == {"completed": 0, "in_progress": 0, "pending": 0, "blocked": 0}


def test_count_roadmap_statuses_counts_completed_rows(tmp_path: Path) -> None:
    roadmap = tmp_path / "roadmap.md"
    roadmap.write_text("| 1 | Feature A | - | - | M | - | ✅ |\n")
    counts = _count_roadmap_statuses(roadmap)
    assert counts["completed"] == 1


def test_count_roadmap_statuses_counts_in_progress_rows(tmp_path: Path) -> None:
    roadmap = tmp_path / "roadmap.md"
    roadmap.write_text("| 1 | Feature B | - | - | M | - | 🔄 |\n")
    counts = _count_roadmap_statuses(roadmap)
    assert counts["in_progress"] == 1


def test_count_roadmap_statuses_counts_pending_rows(tmp_path: Path) -> None:
    roadmap = tmp_path / "roadmap.md"
    roadmap.write_text("| 2 | Feature C | - | - | S | - | ⬜ |\n")
    counts = _count_roadmap_statuses(roadmap)
    assert counts["pending"] == 1


def test_count_roadmap_statuses_counts_blocked_rows(tmp_path: Path) -> None:
    roadmap = tmp_path / "roadmap.md"
    roadmap.write_text("| 3 | Feature D | - | - | L | - | ⏸️ |\n")
    counts = _count_roadmap_statuses(roadmap)
    assert counts["blocked"] == 1


def test_count_roadmap_statuses_ignores_template_comment_rows(tmp_path: Path) -> None:
    roadmap = tmp_path / "roadmap.md"
    roadmap.write_text(
        "| <!-- 1 --> | <!-- Feature --> | <!-- clone-app --> | <!-- - --> | <!-- M --> | <!-- - --> | <!-- ⬜ --> |\n"
    )
    counts = _count_roadmap_statuses(roadmap)
    assert counts == {"completed": 0, "in_progress": 0, "pending": 0, "blocked": 0}


def test_count_roadmap_statuses_ignores_non_table_lines(tmp_path: Path) -> None:
    roadmap = tmp_path / "roadmap.md"
    roadmap.write_text(
        "# Heading\n"
        "\n"
        "> Some note about ✅ things\n"
        "| 1 | Real Feature | - | - | M | - | ✅ |\n"
    )
    counts = _count_roadmap_statuses(roadmap)
    assert counts["completed"] == 1


def test_count_roadmap_statuses_multiple_features(tmp_path: Path) -> None:
    roadmap = tmp_path / "roadmap.md"
    roadmap.write_text(
        "| 1 | A | - | - | M | - | ✅ |\n"
        "| 2 | B | - | - | M | - | ✅ |\n"
        "| 3 | C | - | - | S | - | 🔄 |\n"
        "| 4 | D | - | - | L | - | ⬜ |\n"
    )
    counts = _count_roadmap_statuses(roadmap)
    assert counts["completed"] == 2
    assert counts["in_progress"] == 1
    assert counts["pending"] == 1
    assert counts["blocked"] == 0


# ── _read_last_cost_entry ─────────────────────────────────────────────────────


def test_read_last_cost_entry_returns_none_when_file_absent(tmp_path: Path) -> None:
    result = _read_last_cost_entry(tmp_path / "general-estimates.jsonl")
    assert result is None


def test_read_last_cost_entry_returns_last_record(tmp_path: Path) -> None:
    log = tmp_path / "general-estimates.jsonl"
    records = [
        {"timestamp": "2026-01-01T00:00:00Z", "activity_type": "first"},
        {"timestamp": "2026-02-01T00:00:00Z", "activity_type": "second"},
    ]
    log.write_text("\n".join(json.dumps(r) for r in records) + "\n")
    result = _read_last_cost_entry(log)
    assert result is not None
    assert result["activity_type"] == "second"


def test_read_last_cost_entry_skips_records_without_timestamp(tmp_path: Path) -> None:
    log = tmp_path / "general-estimates.jsonl"
    log.write_text(
        json.dumps({"timestamp": "2026-01-01T00:00:00Z", "activity_type": "valid"})
        + "\n"
        + json.dumps({"no_timestamp": True})
        + "\n"
    )
    result = _read_last_cost_entry(log)
    assert result is not None
    assert result["activity_type"] == "valid"


def test_read_last_cost_entry_skips_blank_lines(tmp_path: Path) -> None:
    log = tmp_path / "general-estimates.jsonl"
    log.write_text(
        "\n"
        + json.dumps({"timestamp": "2026-01-01T00:00:00Z", "activity_type": "only"})
        + "\n\n"
    )
    result = _read_last_cost_entry(log)
    assert result is not None
    assert result["activity_type"] == "only"


def test_read_last_cost_entry_skips_malformed_json_lines(tmp_path: Path) -> None:
    log = tmp_path / "general-estimates.jsonl"
    log.write_text(
        json.dumps({"timestamp": "2026-01-01T00:00:00Z", "activity_type": "good"})
        + "\n"
        "NOT VALID JSON\n"
    )
    result = _read_last_cost_entry(log)
    assert result is not None
    assert result["activity_type"] == "good"


def test_read_last_cost_entry_returns_none_for_empty_file(tmp_path: Path) -> None:
    log = tmp_path / "general-estimates.jsonl"
    log.write_text("")
    result = _read_last_cost_entry(log)
    assert result is None


# ── _build_loop_status ────────────────────────────────────────────────────────


def test_build_loop_status_idle_when_no_lock_file(tmp_path: Path) -> None:
    status = _build_loop_status(tmp_path)
    assert "idle" in status


def test_build_loop_status_running_when_lock_file_present(tmp_path: Path) -> None:
    (tmp_path / "build.lock").write_text("12345\n")
    status = _build_loop_status(tmp_path)
    assert "running" in status


# ── _api_key_status ───────────────────────────────────────────────────────────


def test_api_key_status_shows_set_when_key_present(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-key-1234")
    status = _api_key_status()
    assert "✓" in status or "set" in status


def test_api_key_status_shows_not_set_when_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    status = _api_key_status()
    assert "NOT SET" in status


def test_api_key_status_shows_key_length_not_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    key = "sk-secret-key-9876543210"
    monkeypatch.setenv("ANTHROPIC_API_KEY", key)
    status = _api_key_status()
    assert key not in status
    assert str(len(key)) in status


# ── render_dashboard ──────────────────────────────────────────────────────────


def test_render_dashboard_contains_project_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    output = render_dashboard(tmp_path)
    assert str(tmp_path.resolve()) in output


def test_render_dashboard_contains_roadmap_section(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    output = render_dashboard(tmp_path)
    assert "Roadmap" in output


def test_render_dashboard_contains_auth_section(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    output = render_dashboard(tmp_path)
    assert "Auth" in output
    assert "ANTHROPIC_API_KEY" in output


def test_render_dashboard_contains_build_loop_section(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    output = render_dashboard(tmp_path)
    assert "Build Loop" in output


def test_render_dashboard_shows_no_cost_data_when_log_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    output = render_dashboard(tmp_path)
    assert "No cost data" in output


def test_render_dashboard_shows_last_cost_entry_when_log_present(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    log = tmp_path / "general-estimates.jsonl"
    log.write_text(
        json.dumps(
            {"timestamp": "2026-03-01T12:00:00Z", "activity_type": "test-activity"}
        )
        + "\n"
    )
    output = render_dashboard(tmp_path)
    assert "2026-03-01T12:00:00Z" in output
    assert "test-activity" in output


def test_render_dashboard_real_roadmap_counts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    roadmap = tmp_path / ".specs" / "roadmap.md"
    roadmap.parent.mkdir(parents=True, exist_ok=True)
    roadmap.write_text(
        "| 1 | Auth | - | - | M | - | ✅ |\n"
        "| 2 | Dashboard | - | - | M | - | 🔄 |\n"
        "| 3 | Future | - | - | S | - | ⬜ |\n"
    )
    output = render_dashboard(tmp_path)
    assert "1" in output  # at least one completed
    assert "Roadmap" in output


# ── main entrypoint ───────────────────────────────────────────────────────────


def test_main_returns_zero_exit_code(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    exit_code = main([str(tmp_path)])
    assert exit_code == 0


def test_main_prints_dashboard_to_stdout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    main([str(tmp_path)])
    captured = capsys.readouterr()
    assert "auto-sdd Dashboard" in captured.out
