"""
Tests for speckit.core.emit module.
"""

import io
import sys
from contextlib import redirect_stdout

import pytest

from speckit.core.emit import (
    emit_stage,
    emit_chunk,
    emit_complete,
    emit_error,
    emit_template,
    _wrap_content,
    _format_box_line,
    BOX_TOP,
    BOX_BOTTOM,
)


class TestWrapContent:
    """Tests for _wrap_content helper."""

    def test_short_line(self):
        """Should not wrap short lines."""
        result = _wrap_content("short line", width=64)
        assert result == ["short line"]

    def test_long_line(self):
        """Should wrap long lines."""
        long_text = "This is a very long line that should be wrapped to fit within the specified width limit"
        result = _wrap_content(long_text, width=30)
        assert len(result) > 1
        for line in result:
            assert len(line) <= 30

    def test_multiline(self):
        """Should handle multiline input."""
        result = _wrap_content("line1\nline2\nline3", width=64)
        assert "line1" in result
        assert "line2" in result
        assert "line3" in result

    def test_empty_string(self):
        """Should handle empty string."""
        result = _wrap_content("", width=64)
        assert result == [""]


class TestFormatBoxLine:
    """Tests for _format_box_line helper."""

    def test_basic_formatting(self):
        """Should format line with box characters."""
        result = _format_box_line("test", width=64)
        assert result.startswith("│ ")
        assert result.endswith(" │")
        assert "test" in result

    def test_padding(self):
        """Should pad to correct width."""
        result = _format_box_line("hi", width=10)
        # │ + space + text + padding + space + │ = width + 4
        assert len(result) == 14  # 10 + 4 for box chars


class TestEmitStage:
    """Tests for emit_stage function."""

    def test_basic_output(self):
        """Should output stage with box format."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_stage(
                stage_num=1,
                total_stages=3,
                title="Test Stage",
                content="Do something",
                next_cmd="speckit test --stage=2",
            )

        result = output.getvalue()
        assert BOX_TOP in result
        assert BOX_BOTTOM in result
        assert "STAGE: 1/3" in result
        assert "Test Stage" in result
        assert "Do something" in result
        assert "NEXT: speckit test --stage=2" in result

    def test_with_context(self):
        """Should include context if provided."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_stage(
                stage_num=1,
                total_stages=3,
                title="Test",
                content="Content",
                next_cmd="next",
                context={"key": "value"},
            )

        result = output.getvalue()
        assert "Context:" in result
        assert "key: value" in result

    def test_with_alt_cmd(self):
        """Should include alternative command if provided."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_stage(
                stage_num=1,
                total_stages=3,
                title="Test",
                content="Content",
                next_cmd="next",
                alt_cmd="alternative",
            )

        result = output.getvalue()
        assert "OR: alternative" in result


class TestEmitChunk:
    """Tests for emit_chunk function."""

    def test_basic_output(self):
        """Should output chunk with correct format."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_chunk(
                chunk_num=2,
                total_chunks=9,
                title="Technology Stack",
                content="Document the tech stack",
                file_path="analysis-report.md",
                mode="APPEND",
                line_range=(30, 50),
                next_cmd="speckit analyze --chunk=3",
            )

        result = output.getvalue()
        assert "REPORT CHUNK: 2/9" in result
        assert "Technology Stack" in result
        assert "30-50 lines" in result
        assert "Write to: analysis-report.md" in result
        assert "Mode: APPEND" in result

    def test_create_mode(self):
        """Should handle CREATE mode."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_chunk(
                chunk_num=1,
                total_chunks=5,
                title="Summary",
                content="Write summary",
                file_path="report.md",
                mode="CREATE",
                line_range=(10, 20),
                next_cmd="next",
            )

        result = output.getvalue()
        assert "Mode: CREATE" in result


class TestEmitComplete:
    """Tests for emit_complete function."""

    def test_basic_output(self):
        """Should output completion message."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_complete(message="Workflow finished successfully")

        result = output.getvalue()
        assert "WORKFLOW_COMPLETE" in result
        assert "Workflow finished successfully" in result

    def test_with_artifacts(self):
        """Should list generated artifacts."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_complete(
                message="Done",
                artifacts=["report.md", "spec.md"],
            )

        result = output.getvalue()
        assert "Generated artifacts:" in result
        assert "report.md" in result
        assert "spec.md" in result

    def test_with_next_steps(self):
        """Should list next steps."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_complete(
                message="Done",
                next_steps=["Review report", "Run tests"],
            )

        result = output.getvalue()
        assert "Next steps:" in result
        assert "Review report" in result
        assert "Run tests" in result


class TestEmitError:
    """Tests for emit_error function."""

    def test_basic_output(self):
        """Should output error message."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_error(
                error_type="VALIDATION_ERROR",
                message="Something went wrong",
            )

        result = output.getvalue()
        assert "ERROR: VALIDATION_ERROR" in result
        assert "Something went wrong" in result

    def test_with_recovery(self):
        """Should include recovery command."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_error(
                error_type="STATE_ERROR",
                message="State corrupted",
                recovery_cmd="speckit analyze --stage=1",
            )

        result = output.getvalue()
        assert "RECOVERY: speckit analyze --stage=1" in result

    def test_with_details(self):
        """Should include error details."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_error(
                error_type="FILE_ERROR",
                message="File not found",
                details="The file /path/to/file.txt does not exist",
            )

        result = output.getvalue()
        assert "Details:" in result
        assert "file.txt" in result


class TestEmitTemplate:
    """Tests for emit_template function."""

    def test_basic_output(self):
        """Should output template with stage info."""
        output = io.StringIO()
        with redirect_stdout(output):
            emit_template(
                stage_info={
                    "num": 2,
                    "total": 4,
                    "title": "Generate Spec",
                    "next_cmd": "speckit spec --stage=3",
                },
                template_content="# Template\n\n{placeholder}",
                context={"project": "my-app"},
                output_file="spec.md",
            )

        result = output.getvalue()
        assert "STAGE: 2/4" in result
        assert "Generate Spec" in result
        assert "Create file: spec.md" in result
        assert "Template" in result
        assert "project: my-app" in result
