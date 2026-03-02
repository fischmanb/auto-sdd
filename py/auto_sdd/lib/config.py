# CONVERSION CHANGELOG
# - No bash original. This is a new module for the Python port.
# - Process environment takes precedence over .env.local values, matching bash
#   convention where exported vars are not overwritten by sourced files.
# - load_env_file is pure (no side effects on os.environ). Callers decide what
#   to do with parsed values.
# - ConfigError is defined here (not in errors.py) to avoid a circular import;
#   errors.py does not exist yet.

"""Configuration and authentication management for auto-sdd.

Reads ``.env.local`` from the project directory and merges with the process
environment. Process environment always takes precedence so that CI-injected
secrets are not overridden by checked-in env files.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

# Required environment variables for the system to function
REQUIRED_ENV_VARS: frozenset[str] = frozenset({"ANTHROPIC_API_KEY"})

_DEFAULT_ENV_FILENAME = ".env.local"


# ── Exceptions ────────────────────────────────────────────────────────────────


class ConfigError(Exception):
    """Configuration is invalid or missing required values."""


# ── Data types ────────────────────────────────────────────────────────────────


@dataclass
class Config:
    """Resolved, validated configuration for an auto-sdd project.

    Attributes:
        anthropic_api_key: Claude/Anthropic API key.
        project_dir: Absolute path to the auto-sdd project root.
        specs_dir: Absolute path to ``.specs/`` inside project_dir.
        cost_log_path: Path to ``general-estimates.jsonl``, or None if the
            file does not exist.
    """

    anthropic_api_key: str
    project_dir: Path
    specs_dir: Path
    cost_log_path: Path | None


# ── Public API ────────────────────────────────────────────────────────────────


def load_env_file(env_path: Path) -> dict[str, str]:
    """Parse a ``.env``-style file into a mapping.

    Rules:
    - Lines starting with ``#`` (after optional leading whitespace) are comments
      and are skipped.
    - Blank lines are skipped.
    - Lines without an ``=`` are skipped with a warning.
    - The first ``=`` splits key from value; subsequent ``=`` signs are part of
      the value.
    - Surrounding whitespace is stripped from both key and value.
    - Inline ``#`` comments are **not** stripped (matches bash ``source`` behaviour).

    Args:
        env_path: Path to the ``.env`` file to parse.

    Returns:
        A ``dict[str, str]`` of variable names to values.  Does **not** mutate
        ``os.environ``.

    Raises:
        OSError: If the file cannot be read.
    """
    result: dict[str, str] = {}
    raw = env_path.read_text()
    for lineno, line in enumerate(raw.splitlines(), start=1):
        stripped = line.strip()
        # Skip blank lines and comments
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            logger.warning(
                "%s:%d — line has no '=' separator, skipping: %r",
                env_path,
                lineno,
                line,
            )
            continue
        key, _, value = stripped.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            logger.warning(
                "%s:%d — empty key after stripping, skipping: %r",
                env_path,
                lineno,
                line,
            )
            continue
        result[key] = value
    return result


def resolve_config(
    project_dir: Path,
    env_file: Path | None = None,
) -> Config:
    """Load and validate configuration for an auto-sdd project.

    Resolution order (later sources override earlier ones — except process env
    which always wins):

    1. Parse ``env_file`` (defaults to ``project_dir/.env.local``).
    2. For each key, use the process environment value if set, otherwise use the
       file value.  This ensures CI-injected secrets are honoured.

    Args:
        project_dir: Root directory of the auto-sdd project.
        env_file: Optional explicit path to a ``.env`` file.  If *None*, the
            path ``project_dir/.env.local`` is tried; a missing file is silently
            ignored.

    Returns:
        A populated :class:`Config` dataclass.

    Raises:
        ConfigError: If any variable in :data:`REQUIRED_ENV_VARS` is absent
            from both the env file and the process environment.
    """
    project_dir = project_dir.resolve()

    # Determine env file path
    env_path: Path | None = env_file
    if env_path is None:
        candidate = project_dir / _DEFAULT_ENV_FILENAME
        env_path = candidate if candidate.exists() else None

    # Load file values (if file exists)
    file_values: dict[str, str] = {}
    if env_path is not None:
        try:
            file_values = load_env_file(env_path)
            logger.debug("Loaded %d vars from %s", len(file_values), env_path)
        except OSError as exc:
            logger.warning("Could not read env file %s: %s", env_path, exc)

    # Build merged environment: process env takes precedence
    merged: dict[str, str] = {**file_values, **os.environ}

    # Validate required vars
    missing = sorted(v for v in REQUIRED_ENV_VARS if not merged.get(v))
    if missing:
        raise ConfigError(
            f"Required environment variable(s) not set: {', '.join(missing)}. "
            f"Set them in the process environment or in {project_dir / _DEFAULT_ENV_FILENAME}."
        )

    specs_dir = project_dir / ".specs"
    cost_log_candidate = project_dir / "general-estimates.jsonl"

    return Config(
        anthropic_api_key=merged["ANTHROPIC_API_KEY"],
        project_dir=project_dir,
        specs_dir=specs_dir,
        cost_log_path=cost_log_candidate if cost_log_candidate.exists() else None,
    )
