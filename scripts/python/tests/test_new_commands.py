"""Tests for new CLI commands (project, chain, guidelines, workflow)."""

import json
import os
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from speckit.cli import app
from speckit.commands.project import (
    enumerate_project,
    get_file_category,
    detect_tech_stack,
    verify_analysis_report,
)
from speckit.commands.chain import (
    generate_chain_id,
    create_initial_state,
    validate_state,
)
from speckit.commands.guidelines import check_artifactory
from speckit.commands.workflow import (
    get_feature_paths,
    extract_plan_field,
    format_technology_stack,
)

runner = CliRunner()


class TestEnumerateProjectCommand:
    """Tests for enumerate-project command."""

    def test_help(self):
        """Test enumerate-project --help."""
        result = runner.invoke(app, ["enumerate-project", "--help"])
        assert result.exit_code == 0
        assert "Enumerate all files" in result.stdout

    def test_enumerate_project_function(self, tmp_path):
        """Test enumerate_project function."""
        # Create test files
        (tmp_path / "test.py").write_text("print('hello')")
        (tmp_path / "test.md").write_text("# Hello")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "nested.js").write_text("console.log('hi')")

        manifest = enumerate_project(tmp_path, show_progress=False)

        assert manifest["statistics"]["total_files"] == 3
        assert manifest["scan_info"]["project_path"] == str(tmp_path)


class TestChainStateCommand:
    """Tests for chain-state command."""

    def test_help(self):
        """Test chain-state --help."""
        result = runner.invoke(app, ["chain-state", "--help"])
        assert result.exit_code == 0
        assert "Manage chain state" in result.stdout

    def test_generate_id(self):
        """Test generate-id subcommand."""
        result = runner.invoke(app, ["chain-state", "generate-id"])
        assert result.exit_code == 0
        # Output should be 8 hex characters
        chain_id = result.stdout.strip()
        assert len(chain_id) == 8
        int(chain_id, 16)  # Should not raise


class TestVerifyReportCommand:
    """Tests for verify-report command."""

    def test_help(self):
        """Test verify-report --help."""
        result = runner.invoke(app, ["verify-report", "--help"])
        assert result.exit_code == 0
        assert "Verify analysis report" in result.stdout

    def test_nonexistent_file(self, tmp_path):
        """Test verify-report with nonexistent file."""
        result = runner.invoke(app, ["verify-report", str(tmp_path / "nonexistent.md")])
        assert result.exit_code == 1


class TestSetupPlanCommand:
    """Tests for setup-plan command."""

    def test_help(self):
        """Test setup-plan --help."""
        result = runner.invoke(app, ["setup-plan", "--help"])
        assert result.exit_code == 0
        assert "Set up plan file" in result.stdout


class TestUpdateAgentContextCommand:
    """Tests for update-agent-context command."""

    def test_help(self):
        """Test update-agent-context --help."""
        result = runner.invoke(app, ["update-agent-context", "--help"])
        assert result.exit_code == 0
        assert "Update agent context" in result.stdout


class TestGenerateGuidelinesCommand:
    """Tests for generate-guidelines command."""

    def test_help(self):
        """Test generate-guidelines --help."""
        result = runner.invoke(app, ["generate-guidelines", "--help"])
        assert result.exit_code == 0
        assert "Generate coding guidelines" in result.stdout


class TestCheckArtifactoryCommand:
    """Tests for check-artifactory command."""

    def test_help(self):
        """Test check-artifactory --help."""
        result = runner.invoke(app, ["check-artifactory", "--help"])
        assert result.exit_code == 0
        assert "Check if a library is available" in result.stdout


# Unit tests for helper functions


class TestGetFileCategory:
    """Tests for get_file_category function."""

    def test_code_files(self):
        """Test code file categorization."""
        assert get_file_category(".py") == "code"
        assert get_file_category(".js") == "code"
        assert get_file_category(".ts") == "code"
        assert get_file_category(".java") == "code"
        assert get_file_category(".cs") == "code"
        assert get_file_category(".go") == "code"
        assert get_file_category(".rs") == "code"

    def test_config_files(self):
        """Test config file categorization."""
        assert get_file_category(".json") == "config"
        assert get_file_category(".yaml") == "config"
        assert get_file_category(".yml") == "config"
        assert get_file_category(".toml") == "config"

    def test_doc_files(self):
        """Test documentation file categorization."""
        assert get_file_category(".md") == "documentation"
        assert get_file_category(".txt") == "documentation"

    def test_binary_files(self):
        """Test binary file categorization."""
        assert get_file_category(".dll") == "binary"
        assert get_file_category(".exe") == "binary"
        assert get_file_category(".pyc") == "binary"

    def test_no_extension(self):
        """Test files with no extension."""
        assert get_file_category("") == "no_extension"


class TestChainFunctions:
    """Tests for chain state functions."""

    def test_generate_chain_id(self):
        """Test chain ID generation."""
        chain_id = generate_chain_id()
        assert len(chain_id) == 8
        int(chain_id, 16)  # Should be valid hex

    def test_generate_unique_ids(self):
        """Test that IDs are unique."""
        ids = [generate_chain_id() for _ in range(100)]
        assert len(set(ids)) == 100

    def test_create_initial_state(self):
        """Test initial state creation."""
        state = create_initial_state("abc12345")
        assert state["chain_id"] == "abc12345"
        assert "start_time" in state
        assert "timestamp" in state
        assert state["stage"] == "initialization"

    def test_validate_state_valid(self):
        """Test state validation with valid state."""
        state = {
            "chain_id": "abc12345",
            "timestamp": "2025-01-01T00:00:00Z",
        }
        assert validate_state(state) is True

    def test_validate_state_missing_chain_id(self):
        """Test state validation with missing chain_id."""
        state = {"timestamp": "2025-01-01T00:00:00Z"}
        assert validate_state(state) is False


class TestCheckArtifactoryFunction:
    """Tests for check_artifactory function."""

    def test_not_configured(self):
        """Test with unconfigured URL."""
        exit_code, message = check_artifactory("Not configured", "some-lib")
        assert exit_code == 4
        assert "not configured" in message.lower()

    def test_empty_url(self):
        """Test with empty URL."""
        exit_code, message = check_artifactory("", "some-lib")
        assert exit_code == 4


class TestWorkflowFunctions:
    """Tests for workflow helper functions."""

    def test_extract_plan_field(self):
        """Test plan field extraction."""
        content = """
# Plan

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLAlchemy
**Storage**: PostgreSQL
"""
        assert extract_plan_field(content, "Language/Version") == "Python 3.11"
        assert extract_plan_field(content, "Primary Dependencies") == "FastAPI, SQLAlchemy"
        assert extract_plan_field(content, "Storage") == "PostgreSQL"
        assert extract_plan_field(content, "Missing Field") == ""

    def test_format_technology_stack(self):
        """Test technology stack formatting."""
        assert format_technology_stack("Python", "FastAPI") == "Python + FastAPI"
        assert format_technology_stack("Python", "") == "Python"
        assert format_technology_stack("", "FastAPI") == "FastAPI"
        assert format_technology_stack("", "") == ""


class TestDetectTechStack:
    """Tests for tech stack detection."""

    def test_detect_python(self, tmp_path):
        """Test Python detection."""
        (tmp_path / "requirements.txt").write_text("fastapi\nuvicorn\n")

        manifest = {"files": [{"path": "requirements.txt"}]}
        tech = detect_tech_stack(manifest, tmp_path)

        assert "python" in tech["languages"]

    def test_detect_javascript(self, tmp_path):
        """Test JavaScript/Node detection."""
        pkg = {"name": "test", "dependencies": {"react": "^18.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))

        manifest = {"files": [{"path": "package.json"}]}
        tech = detect_tech_stack(manifest, tmp_path)

        assert "javascript" in tech["languages"]
        assert "react" in tech["frameworks"]["frontend"]

    def test_detect_java_maven(self, tmp_path):
        """Test Java/Maven detection."""
        pom = """<project><modelVersion>4.0.0</modelVersion></project>"""
        (tmp_path / "pom.xml").write_text(pom)

        manifest = {"files": [{"path": "pom.xml"}]}
        tech = detect_tech_stack(manifest, tmp_path)

        assert "java" in tech["languages"]
        assert "maven" in tech["build_tools"]


class TestVerifyAnalysisReport:
    """Tests for verify_analysis_report function."""

    def test_missing_file(self, tmp_path):
        """Test with missing report file."""
        result = verify_analysis_report(str(tmp_path / "missing.md"))
        assert result is False

    def test_incomplete_report(self, tmp_path):
        """Test with incomplete report."""
        report = tmp_path / "report.md"
        report.write_text("# Report\n\nPhase 1\nPhase 2\n")

        result = verify_analysis_report(str(report))
        assert result is False  # Missing phases

    def test_valid_report(self, tmp_path):
        """Test with valid report (all phases, 3000+ lines)."""
        content = "# Analysis Report\n\n"
        for i in range(1, 10):
            content += f"## Phase {i}\n\n"
            content += ("Analysis content with file:123 reference.\n" * 100)
            content += "\nSeverity: HIGH\nSeverity: MEDIUM\nSeverity: LOW\n\n"

        # Pad to 3000+ lines
        content += "\n".join(["Line " + str(i) for i in range(3000)])

        report = tmp_path / "report.md"
        report.write_text(content)

        result = verify_analysis_report(str(report))
        assert result is True
