"""Shared test fixtures for auto-sdd Python test suite."""

import pytest
from pathlib import Path


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """A temporary project directory with minimal structure."""
    (tmp_path / "src").mkdir()
    (tmp_path / ".specs").mkdir()
    (tmp_path / ".specs" / "roadmap.md").touch()
    return tmp_path


@pytest.fixture
def sample_spec(tmp_path: Path) -> Path:
    """A valid feature spec file with frontmatter."""
    spec = tmp_path / "feature.md"
    spec.write_text(
        "---\n"
        "feature: test-feature\n"
        "domain: core\n"
        "status: pending\n"
        "---\n"
        "# Test Feature\n"
    )
    return spec


@pytest.fixture
def mock_claude_output(tmp_path: Path) -> Path:
    """A file containing mock claude JSON output."""
    output = tmp_path / "claude-output.json"
    output.write_text(
        '{"result": "mock output", "total_cost_usd": 0.01, '
        '"usage": {"input_tokens": 100, "output_tokens": 50}}'
    )
    return output
