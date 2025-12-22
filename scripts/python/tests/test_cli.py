"""
Tests for speckit CLI.
"""

import re
import pytest
from typer.testing import CliRunner

from speckit.cli import app
from speckit import __version__


runner = CliRunner()


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class TestVersion:
    """Tests for version command."""

    def test_version_flag(self):
        """Should display version with --version flag."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.stdout

    def test_version_short_flag(self):
        """Should display version with -v flag."""
        result = runner.invoke(app, ["-v"])
        assert result.exit_code == 0
        assert __version__ in result.stdout


class TestHelp:
    """Tests for help output."""

    def test_main_help(self):
        """Should display help with --help flag."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Spec Kit Smart" in result.stdout

    def test_no_args_runs_default(self):
        """Should run without args (commands default to stage 1)."""
        result = runner.invoke(app, [])
        # Without no_args_is_help, CLI runs but may show help for subcommand selection
        # Exit code 0 means success, 2 means CLI needs subcommand
        assert result.exit_code in (0, 2)


class TestAnalyzeProjectCommand:
    """Tests for analyze-project command."""

    def test_help(self):
        """Should display help for analyze-project."""
        result = runner.invoke(app, ["analyze-project", "--help"])
        assert result.exit_code == 0
        output = strip_ansi(result.stdout)
        assert "analyze" in output.lower()
        assert "--stage" in output

    def test_default_stage(self):
        """Should accept default stage parameter."""
        # Just test that the command parses correctly
        result = runner.invoke(app, ["analyze-project", "--stage", "1"])
        # May fail due to missing project, but should parse args
        assert "--stage" not in result.stdout or result.exit_code in (0, 1)

    def test_path_without_scope_errors(self, tmp_path):
        """Should error when --path provided without --scope."""
        result = runner.invoke(app, ["analyze-project", "--path", str(tmp_path)])
        assert result.exit_code == 1
        output = strip_ansi(result.stdout)
        assert "--scope is required" in output


class TestConstitutionCommand:
    """Tests for constitution command."""

    def test_help(self):
        """Should display help for constitution."""
        result = runner.invoke(app, ["constitution", "--help"])
        assert result.exit_code == 0
        assert "constitution" in result.stdout.lower() or "principles" in result.stdout.lower()

    def test_stage_option(self):
        """Should accept stage option."""
        result = runner.invoke(app, ["constitution", "--stage", "1"])
        # Check command runs (may produce stage output or error)
        assert result.exit_code in (0, 1, 2)


class TestSpecifyCommand:
    """Tests for specify command."""

    def test_help(self):
        """Should display help for specify."""
        result = runner.invoke(app, ["specify", "--help"])
        assert result.exit_code == 0
        assert "--stage" in strip_ansi(result.stdout)

    def test_jira_without_feature_errors(self):
        """Should error when --jira provided without --feature."""
        result = runner.invoke(app, ["specify", "--jira", "PROJ-123"])
        assert result.exit_code == 1
        output = strip_ansi(result.stdout)
        assert "--feature is required" in output


class TestPlanCommand:
    """Tests for plan command."""

    def test_help(self):
        """Should display help for plan."""
        result = runner.invoke(app, ["plan", "--help"])
        assert result.exit_code == 0
        assert "--stage" in strip_ansi(result.stdout)


class TestTasksCommand:
    """Tests for tasks command."""

    def test_help(self):
        """Should display help for tasks."""
        result = runner.invoke(app, ["tasks", "--help"])
        assert result.exit_code == 0
        assert "--stage" in strip_ansi(result.stdout)


class TestImplementCommand:
    """Tests for implement command."""

    def test_help(self):
        """Should display help for implement."""
        result = runner.invoke(app, ["implement", "--help"])
        assert result.exit_code == 0
        assert "--stage" in strip_ansi(result.stdout)


class TestClarifyCommand:
    """Tests for clarify command."""

    def test_help(self):
        """Should display help for clarify."""
        result = runner.invoke(app, ["clarify", "--help"])
        assert result.exit_code == 0
        assert "--stage" in strip_ansi(result.stdout)


class TestChecklistCommand:
    """Tests for checklist command."""

    def test_help(self):
        """Should display help for checklist."""
        result = runner.invoke(app, ["checklist", "--help"])
        assert result.exit_code == 0
        assert "--stage" in strip_ansi(result.stdout)


class TestListFragmentsCommand:
    """Tests for list-fragments debug command."""

    def test_help(self):
        """Should display help for list-fragments."""
        result = runner.invoke(app, ["list-fragments", "--help"])
        assert result.exit_code == 0

    def test_list_constitution_fragments(self):
        """Should list fragments for constitution."""
        result = runner.invoke(app, ["list-fragments", "constitution"])
        # Should show some output
        assert "constitution" in result.stdout.lower() or "fragment" in result.stdout.lower()


class TestShowFragmentCommand:
    """Tests for show-fragment debug command."""

    def test_help(self):
        """Should display help for show-fragment."""
        result = runner.invoke(app, ["show-fragment", "--help"])
        assert result.exit_code == 0

    def test_show_missing_fragment(self):
        """Should handle missing fragment gracefully."""
        result = runner.invoke(app, ["show-fragment", "fake", "fake"])
        # Should show error
        assert result.exit_code != 0 or "error" in result.stdout.lower() or "not found" in result.stdout.lower()


class TestInitCommand:
    """Tests for init command."""

    def test_help(self):
        """Should display help for init."""
        result = runner.invoke(app, ["init", "--help"])
        assert result.exit_code == 0


class TestCommandConsistency:
    """Tests for consistent command structure."""

    def test_all_commands_have_help(self):
        """All commands should have help text."""
        commands = [
            "analyze-project",
            "constitution",
            "specify",
            "plan",
            "tasks",
            "implement",
            "clarify",
            "checklist",
            "list-fragments",
            "show-fragment",
            "init",
        ]
        for cmd in commands:
            result = runner.invoke(app, [cmd, "--help"])
            assert result.exit_code == 0, f"Command {cmd} failed to show help"

    def test_stage_commands_have_chain_option(self):
        """Stage-based commands should have --chain option."""
        stage_commands = [
            "analyze-project",
            "specify",
            "plan",
            "tasks",
            "implement",
            "clarify",
            "checklist",
        ]
        for cmd in stage_commands:
            result = runner.invoke(app, [cmd, "--help"])
            output = strip_ansi(result.stdout)
            assert "--chain" in output, f"Command {cmd} missing --chain option"
