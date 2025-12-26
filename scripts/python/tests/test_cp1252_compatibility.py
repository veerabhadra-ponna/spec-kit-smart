"""Test that all template and prompt files are cp1252 compatible."""

import os
from pathlib import Path

import pytest


def get_assets_dir() -> Path:
    """Get the assets directory path."""
    return Path(__file__).parent.parent / "speckit" / "assets"


def get_console_output_markdown_files() -> list[Path]:
    """Get markdown files that are rendered to console output.

    Only checks templates and prompts directories, not guidelines
    which are developer documentation that may use Unicode.
    """
    assets_dir = get_assets_dir()
    files = []

    # Templates rendered to console
    templates_dir = assets_dir / "templates"
    if templates_dir.exists():
        files.extend(templates_dir.rglob("*.md"))

    # Prompts rendered to console
    prompts_dir = assets_dir / "prompts"
    if prompts_dir.exists():
        files.extend(prompts_dir.rglob("*.md"))

    return files


class TestCp1252Compatibility:
    """Test cp1252 encoding compatibility for Windows console output."""

    def test_assets_directory_exists(self):
        """Verify assets directory exists."""
        assert get_assets_dir().exists(), "Assets directory not found"

    def test_markdown_files_exist(self):
        """Verify markdown files are found."""
        files = get_console_output_markdown_files()
        assert len(files) > 0, "No markdown files found in templates/prompts"

    @pytest.mark.parametrize(
        "md_file",
        get_console_output_markdown_files(),
        ids=lambda p: str(p.relative_to(get_assets_dir())),
    )
    def test_file_is_cp1252_compatible(self, md_file: Path):
        """Test that each markdown file can be encoded as cp1252.

        This ensures templates render correctly on Windows console which
        defaults to cp1252 encoding.
        """
        content = md_file.read_text(encoding="utf-8")

        try:
            content.encode("cp1252")
        except UnicodeEncodeError as e:
            # Find the problematic character and its location
            char = e.object[e.start]
            line_num = content[: e.start].count("\n") + 1
            col_num = e.start - content.rfind("\n", 0, e.start)

            pytest.fail(
                f"File contains non-cp1252 character at line {line_num}, col {col_num}: "
                f"'{char}' (U+{ord(char):04X})\n"
                f"Replace with ASCII equivalent for Windows compatibility."
            )
