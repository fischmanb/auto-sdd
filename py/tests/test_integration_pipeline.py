"""Integration tests for the full build pipeline with all isolation layers.

Exercises: prompt boundary injection, chmod protection + restore,
contamination audit, project config loading, log directory derivation,
and single-feature end-to-end build completion.

Each test is independent — no shared mutable state across tests.
"""
from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest

from auto_sdd.lib.claude_wrapper import ClaudeResult
from auto_sdd.lib.prompt_builder import BuildConfig, build_feature_prompt
from auto_sdd.scripts.build_loop import (
    BuildLoop,
    _check_repo_contamination,
    _EXPECTED_WRITE_PATTERNS,
    _protect_repo_tree,
    _PROTECT_DIRS,
    _PROTECT_ROOT_GLOBS,
    _REPO_ROOT,
    _restore_repo_tree,
)

# Patch target for codebase summary — called inside prompt_builder
_CODEBASE_SUMMARY_PATCH = (
    "auto_sdd.lib.prompt_builder.generate_codebase_summary"
)

# ── Roadmap fixture text ─────────────────────────────────────────────────────

ROADMAP_TEXT = """\
# Integration Test Roadmap

Minimal roadmap for integration pipeline testing.

| # | Feature | Source | Jira | Complexity | Deps | Status |
|---|---------|--------|------|------------|------|--------|
| 1 | Pipeline Feature | manual | - | S | - | ⬜ |
"""

VISION_TEXT = """\
# Integration Test Vision
A minimal project for integration pipeline testing.
"""


# ── Git helpers ──────────────────────────────────────────────────────────────


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=30,
    )


def _git_init(project: Path) -> None:
    """Initialize a git repo with initial commit."""
    _git(["init", "-b", "main"], project)
    _git(["config", "user.email", "test@integration.com"], project)
    _git(["config", "user.name", "IntegrationTest"], project)
    _git(["config", "commit.gpgsign", "false"], project)
    _git(["add", "-A"], project)
    _git(["commit", "-m", "initial: integration test project"], project)


# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def integration_project(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a minimal git-initialized project for integration tests."""
    project = tmp_path / "test-project"
    project.mkdir()

    # Spec files
    specs = project / ".specs"
    specs.mkdir()
    (specs / "roadmap.md").write_text(ROADMAP_TEXT)
    (specs / "vision.md").write_text(VISION_TEXT)

    # Minimal project files
    (project / "CLAUDE.md").write_text("# Test Project\n")
    (project / "package.json").write_text(
        '{"name": "integration-test", "version": "1.0.0"}\n'
    )

    _git_init(project)
    yield project


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove env vars that interfere with BuildLoop."""
    for var in [
        "PROJECT_DIR", "MAIN_BRANCH", "BASE_BRANCH",
        "BRANCH_STRATEGY", "MAX_FEATURES", "MAX_RETRIES",
        "MIN_RETRY_DELAY", "BUILD_MODE", "DRIFT_CHECK",
        "POST_BUILD_STEPS", "PARALLEL_VALIDATION",
        "ENABLE_RESUME", "AGENT_MODEL", "BUILD_MODEL",
        "RETRY_MODEL", "DRIFT_MODEL", "REVIEW_MODEL",
        "LOGS_DIR", "EVAL_OUTPUT_DIR", "COST_LOG_FILE",
        "BUILD_CHECK_CMD", "TEST_CHECK_CMD",
        "EVAL_SIDECAR", "CLAUDECODE", "AGENT_TIMEOUT",
    ]:
        monkeypatch.delenv(var, raising=False)


def _fake_agent(project: Path, feature_name: str) -> ClaudeResult:
    """Simulate what an agent does: create a file, commit, emit signals."""
    safe = feature_name.lower().replace(" ", "-")
    src_file = project / f"{safe}.ts"
    src_file.write_text(f'export const {safe} = "{feature_name}";\n')
    spec_file = project / ".specs" / f"{safe}.md"
    spec_file.write_text(f"---\nfeature: {feature_name}\n---\n")

    _git(["add", "-A"], project)
    _git(["commit", "-m", f"feat: {feature_name}"], project)

    return ClaudeResult(
        output=(
            f"FEATURE_BUILT: {feature_name}\n"
            f"SPEC_FILE: {spec_file}\n"
            f"SOURCE_FILES: {src_file}\n"
        ),
        exit_code=0,
        cost_usd=0.01,
        input_tokens=500,
        output_tokens=200,
    )


def _make_loop(project: Path) -> BuildLoop:
    """Create a BuildLoop pointed at a real git project."""
    defaults = {
        "PROJECT_DIR": str(project),
        "MAIN_BRANCH": "main",
        "BRANCH_STRATEGY": "sequential",
        "MAX_FEATURES": "1",
        "MAX_RETRIES": "0",
        "MIN_RETRY_DELAY": "0",
        "BUILD_CHECK_CMD": "skip",
        "TEST_CHECK_CMD": "skip",
        "POST_BUILD_STEPS": "",
        "DRIFT_CHECK": "false",
        "ENABLE_RESUME": "true",
        "EVAL_SIDECAR": "false",
        "LOGS_DIR": str(project / "logs"),
        "AGENT_TIMEOUT": "60",
    }
    for key, val in defaults.items():
        if key not in os.environ:
            os.environ[key] = val

    return BuildLoop()


# ═══════════════════════════════════════════════════════════════════════════
# INTEGRATION PIPELINE TESTS
# ═══════════════════════════════════════════════════════════════════════════


class TestFullPipelineIntegration:
    """Integration tests covering the full build pipeline with isolation."""

    def test_single_feature_build_completes(
        self, integration_project: Path
    ) -> None:
        """Build 1 feature end-to-end: agent mock commits, loop completes."""
        os.environ["MAX_FEATURES"] = "1"
        loop = _make_loop(integration_project)

        def mock_run_claude(
            args: list[str], **kwargs: object
        ) -> ClaudeResult:
            return _fake_agent(integration_project, "Pipeline Feature")

        with patch(
            "auto_sdd.scripts.build_loop.run_claude",
            side_effect=mock_run_claude,
        ), patch(
            _CODEBASE_SUMMARY_PATCH,
            return_value="(stubbed for integration test)",
        ):
            loop.run()

        assert loop.loop_built == 1
        assert loop.loop_failed == 0
        assert "Pipeline Feature" in loop.built_feature_names

        # Resume state is cleaned after 0-failure run
        state_file = integration_project / ".sdd-state" / "resume.json"
        assert not state_file.exists()

    def test_prompt_contains_filesystem_boundary(
        self, integration_project: Path
    ) -> None:
        """build_feature_prompt injects FILESYSTEM BOUNDARY with project path."""
        config = BuildConfig(
            project_dir=integration_project,
            main_branch="main",
            drift_check=False,
            build_cmd="skip",
            test_cmd="skip",
        )

        with patch(
            _CODEBASE_SUMMARY_PATCH,
            return_value="(stubbed)",
        ):
            prompt_text, _injections = build_feature_prompt(
                feature_id=1,
                feature_name="Pipeline Feature",
                project_dir=integration_project,
                config=config,
            )

        assert "FILESYSTEM BOUNDARY" in prompt_text
        assert str(integration_project) in prompt_text

    def test_protection_applies_and_restores(self) -> None:
        """_protect_repo_tree removes write permission; _restore restores it."""
        # Find a directory from _PROTECT_DIRS that exists in the real repo
        target_dir = None
        for d in _PROTECT_DIRS:
            candidate = _REPO_ROOT / d
            if candidate.is_dir():
                target_dir = candidate
                break
        assert target_dir is not None, (
            f"No _PROTECT_DIRS found under {_REPO_ROOT}"
        )

        # Pick a file inside it to check permissions
        test_file = None
        for f in target_dir.rglob("*"):
            if f.is_file():
                test_file = f
                break
        assert test_file is not None, f"No files found under {target_dir}"

        try:
            result = _protect_repo_tree(_REPO_ROOT)
            assert result is True

            # File should have lost write permission
            mode = test_file.stat().st_mode
            assert not (mode & stat.S_IWUSR), (
                f"{test_file} still has owner-write after protection"
            )
        finally:
            _restore_repo_tree(_REPO_ROOT)

        # After restore, write permission should be back
        mode = test_file.stat().st_mode
        assert (mode & stat.S_IWUSR), (
            f"{test_file} missing owner-write after restore"
        )

    def test_root_file_protection(self) -> None:
        """Root-level files matching _PROTECT_ROOT_GLOBS lose/regain write."""
        # Find a root file matching the globs
        test_file = None
        for pattern in _PROTECT_ROOT_GLOBS:
            matches = list(_REPO_ROOT.glob(pattern))
            for m in matches:
                if m.is_file():
                    test_file = m
                    break
            if test_file is not None:
                break
        assert test_file is not None, (
            f"No root files matching {_PROTECT_ROOT_GLOBS} under {_REPO_ROOT}"
        )

        try:
            _protect_repo_tree(_REPO_ROOT)
            mode = test_file.stat().st_mode
            assert not (mode & stat.S_IWUSR), (
                f"{test_file} still writable after protection"
            )
        finally:
            _restore_repo_tree(_REPO_ROOT)

        mode = test_file.stat().st_mode
        assert (mode & stat.S_IWUSR), (
            f"{test_file} not writable after restore"
        )

    def test_contamination_check_clean_repo(self) -> None:
        """Clean working tree returns no contaminated files."""
        contaminated = _check_repo_contamination(
            _REPO_ROOT, _EXPECTED_WRITE_PATTERNS
        )
        # Filter out learnings/pending.md which may be dirty from session work
        unexpected = [
            f for f in contaminated
            if not any(f.startswith(p) for p in _EXPECTED_WRITE_PATTERNS)
        ]
        assert unexpected == [], f"Unexpected contamination: {unexpected}"

    def test_contamination_check_detects_unexpected_write(self) -> None:
        """Staged unexpected file is detected as contamination."""
        contam_file = _REPO_ROOT / "CONTAMINATION_TEST_FILE.tmp"
        try:
            contam_file.write_text("contamination test\n")
            _git(["add", "CONTAMINATION_TEST_FILE.tmp"], _REPO_ROOT)

            contaminated = _check_repo_contamination(
                _REPO_ROOT, _EXPECTED_WRITE_PATTERNS
            )
            assert "CONTAMINATION_TEST_FILE.tmp" in contaminated
        finally:
            _git(
                ["reset", "HEAD", "--", "CONTAMINATION_TEST_FILE.tmp"],
                _REPO_ROOT,
            )
            if contam_file.exists():
                contam_file.unlink()

    def test_build_loop_initializes_with_project_dir(
        self, tmp_path: Path
    ) -> None:
        """BuildLoop loads project.yaml and sets project_dir correctly."""
        project = tmp_path / "config-test-project"
        project.mkdir()

        # Minimal project structure
        specs = project / ".specs"
        specs.mkdir()
        (specs / "roadmap.md").write_text(
            "# Roadmap\n\n"
            "| # | Feature | Source | Jira | Complexity | Deps | Status |\n"
            "|---|---------|--------|------|------------|------|--------|\n"
        )
        (specs / "vision.md").write_text("# Vision\n")
        (project / "CLAUDE.md").write_text("# Test\n")

        # Create .sdd-config/project.yaml
        config_dir = project / ".sdd-config"
        config_dir.mkdir()
        (config_dir / "project.yaml").write_text(
            "build_cmd: echo ok\ntest_cmd: echo ok\n"
        )

        _git_init(project)

        os.environ["PROJECT_DIR"] = str(project)
        os.environ["MAIN_BRANCH"] = "main"
        os.environ["BRANCH_STRATEGY"] = "sequential"
        os.environ["MAX_FEATURES"] = "1"
        os.environ["MAX_RETRIES"] = "0"
        os.environ["MIN_RETRY_DELAY"] = "0"
        os.environ["POST_BUILD_STEPS"] = ""
        os.environ["DRIFT_CHECK"] = "false"
        os.environ["ENABLE_RESUME"] = "true"
        os.environ["EVAL_SIDECAR"] = "false"
        os.environ["LOGS_DIR"] = str(project / "logs")
        os.environ["AGENT_TIMEOUT"] = "60"

        loop = BuildLoop()
        assert loop.project_dir == project.resolve()
        assert loop.build_cmd != ""

    def test_logs_dir_derivation_without_override(
        self, tmp_path: Path
    ) -> None:
        """Without LOGS_DIR, logs_dir derives from project_dir parent."""
        project = tmp_path / "log-test-project"
        project.mkdir()

        specs = project / ".specs"
        specs.mkdir()
        (specs / "roadmap.md").write_text(
            "# Roadmap\n\n"
            "| # | Feature | Source | Jira | Complexity | Deps | Status |\n"
            "|---|---------|--------|------|------------|------|--------|\n"
        )
        (specs / "vision.md").write_text("# Vision\n")
        (project / "CLAUDE.md").write_text("# Test\n")

        _git_init(project)

        os.environ["PROJECT_DIR"] = str(project)
        os.environ["MAIN_BRANCH"] = "main"
        os.environ["BRANCH_STRATEGY"] = "sequential"
        os.environ["MAX_FEATURES"] = "1"
        os.environ["MAX_RETRIES"] = "0"
        os.environ["MIN_RETRY_DELAY"] = "0"
        os.environ["POST_BUILD_STEPS"] = ""
        os.environ["DRIFT_CHECK"] = "false"
        os.environ["ENABLE_RESUME"] = "true"
        os.environ["EVAL_SIDECAR"] = "false"
        os.environ["AGENT_TIMEOUT"] = "60"
        # Explicitly do NOT set LOGS_DIR

        loop = BuildLoop()
        expected_logs = project.parent / "logs" / project.name
        assert loop.logs_dir == expected_logs
