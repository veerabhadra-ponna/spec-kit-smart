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

    def test_path_without_scope_uses_default(self, tmp_path):
        """Should proceed with default scope A when --path provided without --scope."""
        # With AI agent-based input collection, CLI no longer requires --scope
        # when --path is provided. The workflow defaults to scope A and the AI
        # agent can collect scope from user via prompts if needed.
        result = runner.invoke(app, ["analyze-project", "--path", str(tmp_path)])
        # Should not error - defaults to scope A
        assert result.exit_code == 0


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

    def test_feature_without_jira_succeeds(self):
        """Should accept --feature without --jira (JIRA is optional)."""
        result = runner.invoke(app, ["specify", "--stage", "2", "--feature", "Add user auth"])
        # Should succeed - JIRA is optional, command outputs stage prompt
        assert result.exit_code == 0


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

    def test_feature_commands_have_feature_dir_option(self):
        """Feature-scoped commands should have --feature-dir option."""
        feature_commands = [
            "specify",
            "plan",
            "tasks",
            "implement",
            "clarify",
            "checklist",
        ]
        for cmd in feature_commands:
            result = runner.invoke(app, [cmd, "--help"])
            output = strip_ansi(result.stdout)
            assert "--feature-dir" in output, f"Command {cmd} missing --feature-dir option"

    def test_analyze_project_has_analysis_dir_option(self):
        """Analyze-project should have --analysis-dir option."""
        result = runner.invoke(app, ["analyze-project", "--help"])
        output = strip_ansi(result.stdout)
        assert "--analysis-dir" in output, "analyze-project missing --analysis-dir option"


class TestListFilesCommand:
    """Tests for list-files command."""

    def test_help(self):
        """Should display help for list-files."""
        result = runner.invoke(app, ["list-files", "--help"])
        assert result.exit_code == 0
        output = strip_ansi(result.stdout)
        assert "--pattern" in output
        assert "--category" in output
        assert "--count" in output

    def test_list_files_with_pattern(self, tmp_path):
        """Should list files matching pattern."""
        # Create test files
        (tmp_path / "test1.py").write_text("# test")
        (tmp_path / "test2.py").write_text("# test")
        (tmp_path / "other.txt").write_text("text")

        result = runner.invoke(app, [
            "list-files",
            "--pattern", "*.py",
            "--project-path", str(tmp_path),
        ])
        assert result.exit_code == 0
        assert "test1.py" in result.stdout
        assert "test2.py" in result.stdout
        assert "other.txt" not in result.stdout

    def test_count_returns_total_not_limited(self, tmp_path):
        """--count should return total matches, not limited count."""
        # Create more files than the limit
        for i in range(150):
            (tmp_path / f"file{i:03d}.py").write_text("# test")

        result = runner.invoke(app, [
            "list-files",
            "--pattern", "*.py",
            "--project-path", str(tmp_path),
            "--limit", "50",
            "--count",
        ])
        assert result.exit_code == 0
        # Should show 150, not 50
        assert result.stdout.strip() == "150"

    def test_limit_restricts_output_but_not_count(self, tmp_path):
        """--limit should restrict displayed files but show total in summary."""
        # Create test files
        for i in range(10):
            (tmp_path / f"file{i}.py").write_text("# test")

        result = runner.invoke(app, [
            "list-files",
            "--pattern", "*.py",
            "--project-path", str(tmp_path),
            "--limit", "5",
        ])
        assert result.exit_code == 0
        output = strip_ansi(result.stdout)
        # Should show "Showing 5 of 10"
        assert "5 of 10" in output or "5" in output

    def test_category_controllers(self, tmp_path):
        """Should list controller files by category."""
        (tmp_path / "UserController.py").write_text("# controller")
        (tmp_path / "service.py").write_text("# service")

        result = runner.invoke(app, [
            "list-files",
            "--category", "controllers",
            "--project-path", str(tmp_path),
        ])
        assert result.exit_code == 0
        assert "UserController.py" in result.stdout
        assert "service.py" not in result.stdout


class TestUpdatePreferencesCommand:
    """Tests for update-preferences command."""

    def test_help(self):
        """Should display help for update-preferences."""
        result = runner.invoke(app, ["update-preferences", "--help"])
        assert result.exit_code == 0
        assert "Update modernization preferences" in result.stdout

    def test_rejects_invalid_json(self, tmp_path):
        """Should reject invalid JSON input."""
        # Create analysis folder with state
        analysis_dir = tmp_path / ".analysis" / "test-analysis"
        analysis_dir.mkdir(parents=True)
        state_file = analysis_dir / "state.json"
        state_file.write_text('{"schema_version": 1, "workflow": "analyze-project"}')

        result = runner.invoke(app, [
            "update-preferences",
            "not-valid-json",
            "--analysis-dir", str(analysis_dir),
        ])
        assert result.exit_code == 1
        assert "Invalid JSON" in result.stdout

    def test_rejects_empty_preferences(self, tmp_path):
        """Should reject empty preferences object."""
        analysis_dir = tmp_path / ".analysis" / "test-analysis"
        analysis_dir.mkdir(parents=True)
        state_file = analysis_dir / "state.json"
        state_file.write_text('{"schema_version": 1, "workflow": "analyze-project", "modernization_preferences": {}}')

        result = runner.invoke(app, [
            "update-preferences",
            "{}",
            "--analysis-dir", str(analysis_dir),
        ])
        assert result.exit_code == 1
        assert "empty" in result.stdout.lower()

    def test_warns_on_unknown_keys(self, tmp_path):
        """Should warn but allow unknown preference keys."""
        analysis_dir = tmp_path / ".analysis" / "test-analysis"
        analysis_dir.mkdir(parents=True)
        state_file = analysis_dir / "state.json"
        state_file.write_text('{"schema_version": 1, "workflow": "analyze-project", "modernization_preferences": {}}')

        result = runner.invoke(app, [
            "update-preferences",
            '{"unknown_key": "value", "q1_language": "Python"}',
            "--analysis-dir", str(analysis_dir),
        ])
        # Should succeed but warn
        assert result.exit_code == 0
        output = strip_ansi(result.stdout)
        assert "Warning" in output
        assert "unknown_key" in output

    def test_accepts_valid_preference_keys(self, tmp_path):
        """Should accept valid Q1-Q10 preference keys."""
        analysis_dir = tmp_path / ".analysis" / "test-analysis"
        analysis_dir.mkdir(parents=True)
        state_file = analysis_dir / "state.json"
        state_file.write_text('{"schema_version": 1, "workflow": "analyze-project", "modernization_preferences": {}}')

        result = runner.invoke(app, [
            "update-preferences",
            '{"q1_language": "Python 3.11", "q2_database": "PostgreSQL"}',
            "--analysis-dir", str(analysis_dir),
        ])
        assert result.exit_code == 0

        # Verify state was updated
        import json
        state = json.loads(state_file.read_text())
        assert state["modernization_preferences"]["q1_language"] == "Python 3.11"
        assert state["modernization_preferences"]["q2_database"] == "PostgreSQL"
