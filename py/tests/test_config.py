"""Tests for auto_sdd.lib.config — configuration and auth management."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from auto_sdd.lib.config import (
    Config,
    ConfigError,
    load_env_file,
    resolve_config,
)


# ── load_env_file ─────────────────────────────────────────────────────────────


def test_load_env_file_parses_key_value_pair(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("FOO=bar\n")
    result = load_env_file(env)
    assert result == {"FOO": "bar"}


def test_load_env_file_skips_comment_lines(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("# this is a comment\nFOO=bar\n")
    result = load_env_file(env)
    assert "# this is a comment" not in result
    assert result == {"FOO": "bar"}


def test_load_env_file_skips_blank_lines(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("\n\nFOO=bar\n\n")
    result = load_env_file(env)
    assert result == {"FOO": "bar"}


def test_load_env_file_skips_line_without_equals(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("BADLINE\nFOO=bar\n")
    result = load_env_file(env)
    assert "BADLINE" not in result
    assert result["FOO"] == "bar"


def test_load_env_file_value_may_contain_equals(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("TOKEN=abc=def=ghi\n")
    result = load_env_file(env)
    assert result["TOKEN"] == "abc=def=ghi"


def test_load_env_file_strips_whitespace_around_key_and_value(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("  KEY  =  value  \n")
    result = load_env_file(env)
    assert result == {"KEY": "value"}


def test_load_env_file_multiple_vars(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("A=1\nB=2\nC=3\n")
    result = load_env_file(env)
    assert result == {"A": "1", "B": "2", "C": "3"}


def test_load_env_file_raises_oserror_on_missing_file(tmp_path: Path) -> None:
    with pytest.raises(OSError):
        load_env_file(tmp_path / "nonexistent.env")


def test_load_env_file_empty_file_returns_empty_dict(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("")
    result = load_env_file(env)
    assert result == {}


def test_load_env_file_inline_comment_not_stripped(tmp_path: Path) -> None:
    """Inline comments are NOT stripped (matches bash 'source' behaviour)."""
    env = tmp_path / ".env"
    env.write_text("KEY=value # with comment\n")
    result = load_env_file(env)
    # The value should include the inline comment text
    assert result["KEY"] == "value # with comment"


# ── resolve_config ────────────────────────────────────────────────────────────


def test_resolve_config_loads_key_from_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_file = tmp_path / ".env.local"
    env_file.write_text("ANTHROPIC_API_KEY=sk-test-from-file\n")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    config = resolve_config(tmp_path)
    assert config.anthropic_api_key == "sk-test-from-file"


def test_resolve_config_process_env_takes_precedence_over_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_file = tmp_path / ".env.local"
    env_file.write_text("ANTHROPIC_API_KEY=sk-file-key\n")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-env-key")
    config = resolve_config(tmp_path)
    assert config.anthropic_api_key == "sk-env-key"


def test_resolve_config_raises_config_error_when_key_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # No .env.local and no process env
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ConfigError, match="ANTHROPIC_API_KEY"):
        resolve_config(tmp_path)


def test_resolve_config_succeeds_without_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # No .env.local file at all — rely on process env
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-from-process-env")
    config = resolve_config(tmp_path)
    assert config.anthropic_api_key == "sk-from-process-env"


def test_resolve_config_sets_project_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    config = resolve_config(tmp_path)
    assert config.project_dir == tmp_path.resolve()


def test_resolve_config_sets_specs_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    config = resolve_config(tmp_path)
    assert config.specs_dir == tmp_path.resolve() / ".specs"


def test_resolve_config_cost_log_path_none_when_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    config = resolve_config(tmp_path)
    assert config.cost_log_path is None


def test_resolve_config_cost_log_path_set_when_file_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "general-estimates.jsonl").write_text("{}\n")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    config = resolve_config(tmp_path)
    assert config.cost_log_path == tmp_path.resolve() / "general-estimates.jsonl"


def test_resolve_config_accepts_explicit_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    custom_env = tmp_path / "custom.env"
    custom_env.write_text("ANTHROPIC_API_KEY=sk-custom\n")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    config = resolve_config(tmp_path, env_file=custom_env)
    assert config.anthropic_api_key == "sk-custom"


def test_resolve_config_config_error_message_names_missing_vars(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ConfigError) as exc_info:
        resolve_config(tmp_path)
    assert "ANTHROPIC_API_KEY" in str(exc_info.value)


def test_resolve_config_returns_config_dataclass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-dummy")
    config = resolve_config(tmp_path)
    assert isinstance(config, Config)
