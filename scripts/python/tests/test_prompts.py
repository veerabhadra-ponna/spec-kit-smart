"""
Tests for speckit.core.prompts module.
"""

import pytest
from pathlib import Path

from speckit.core.prompts import (
    get_prompts_base,
    get_templates_base,
    get_prompt_fragment,
    load_template,
    render_prompt,
    list_fragments,
    get_stage_order,
    fragment_exists,
    get_next_stage,
    count_fragment_lines,
)


class TestGetPromptsBase:
    """Tests for get_prompts_base function."""

    def test_returns_path(self):
        """Should return a Path object."""
        result = get_prompts_base()
        assert isinstance(result, Path)

    def test_path_structure(self):
        """Should return path containing 'commands' or 'prompts'."""
        result = get_prompts_base()
        path_str = str(result)
        # Should point to commands directory
        assert "commands" in path_str or "prompts" in path_str


class TestGetPromptFragment:
    """Tests for get_prompt_fragment function."""

    def test_existing_fragment(self):
        """Should load existing fragment."""
        # Test with constitution command (known to exist)
        try:
            content = get_prompt_fragment("constitution", "01-initialization")
            assert isinstance(content, str)
            assert len(content) > 0
        except FileNotFoundError:
            # May not exist in all test environments
            pytest.skip("Fragment not found in test environment")

    def test_nonexistent_fragment(self):
        """Should raise FileNotFoundError for missing fragment."""
        with pytest.raises(FileNotFoundError):
            get_prompt_fragment("nonexistent-command", "stage99")

    def test_fragment_content(self):
        """Should return markdown content."""
        try:
            content = get_prompt_fragment("constitution", "01-initialization")
            # Should be markdown content
            assert "#" in content or content.strip()
        except FileNotFoundError:
            pytest.skip("Fragment not found in test environment")


class TestRenderPrompt:
    """Tests for render_prompt function."""

    def test_simple_substitution(self):
        """Should substitute simple variables."""
        fragment = "Hello {name}, you are stage {stage}"
        context = {"name": "World", "stage": "1"}

        result = render_prompt(fragment, context)

        assert "Hello World" in result
        assert "stage 1" in result

    def test_default_values(self):
        """Should use default values when variable missing."""
        fragment = "Value: {key:default_value}"
        context = {}

        result = render_prompt(fragment, context)

        assert "Value: default_value" in result

    def test_override_default(self):
        """Should override default when value provided."""
        fragment = "Value: {key:default}"
        context = {"key": "provided"}

        result = render_prompt(fragment, context)

        assert "Value: provided" in result

    def test_escaped_braces(self):
        """Should handle escaped braces."""
        fragment = "Code: {{variable}} and {real}"
        context = {"real": "value"}

        result = render_prompt(fragment, context)

        assert "{variable}" in result
        assert "value" in result

    def test_empty_default(self):
        """Should handle empty default value."""
        fragment = "Optional: {key:}"
        context = {}

        result = render_prompt(fragment, context)

        assert "Optional: " in result

    def test_missing_no_default(self):
        """Should leave empty for missing without default."""
        fragment = "Value: {missing}"
        context = {}

        result = render_prompt(fragment, context)

        assert "Value: " in result

    def test_template_include(self):
        """Should include template from assets/templates/."""
        # Use a known template
        fragment = "Before\n{{include:spec-template.md}}\nAfter"
        context = {}

        result = render_prompt(fragment, context)

        # Template content should be included
        assert "Before" in result
        assert "After" in result
        # Skip if template not found in test environment
        if "[Template not found" in result:
            pytest.skip("Template not found in test environment")
        assert "Feature Specification" in result

    def test_template_include_not_found_graceful(self):
        """Should show error message for missing template in non-strict mode."""
        fragment = "Before\n{{include:nonexistent-template.md}}\nAfter"
        context = {}

        result = render_prompt(fragment, context)

        assert "Before" in result
        assert "After" in result
        assert "[Template not found: nonexistent-template.md]" in result

    def test_template_include_strict_mode_raises(self):
        """Should raise FileNotFoundError in strict mode for missing template."""
        fragment = "Before\n{{include:nonexistent-template.md}}\nAfter"
        context = {}

        with pytest.raises(FileNotFoundError) as exc_info:
            render_prompt(fragment, context, strict=True)

        assert "nonexistent-template.md" in str(exc_info.value)

    def test_template_include_strict_mode_success(self):
        """Should succeed in strict mode when template exists."""
        fragment = "Before\n{{include:spec-template.md}}\nAfter"
        context = {}

        try:
            result = render_prompt(fragment, context, strict=True)
            assert "Before" in result
            assert "After" in result
            assert "Feature Specification" in result
            assert "[Template not found" not in result
        except FileNotFoundError:
            pytest.skip("Template not found in test environment")


class TestGetTemplatesBase:
    """Tests for get_templates_base function."""

    def test_returns_path(self):
        """Should return a Path object."""
        result = get_templates_base()
        assert isinstance(result, Path)

    def test_path_contains_templates(self):
        """Should return path containing 'templates'."""
        result = get_templates_base()
        assert "templates" in str(result)


class TestLoadTemplate:
    """Tests for load_template function."""

    def test_existing_template(self):
        """Should load existing template."""
        try:
            content = load_template("spec-template.md")
            assert isinstance(content, str)
            assert len(content) > 0
        except FileNotFoundError:
            pytest.skip("Template not found in test environment")

    def test_nonexistent_template(self):
        """Should raise FileNotFoundError for missing template."""
        with pytest.raises(FileNotFoundError):
            load_template("nonexistent-template.md")


class TestListFragments:
    """Tests for list_fragments function."""

    def test_returns_list(self):
        """Should return a list."""
        result = list_fragments("constitution")
        assert isinstance(result, list)

    def test_known_command(self):
        """Should find fragments for known command."""
        result = list_fragments("constitution")
        # Should have at least some fragments if directory exists
        assert isinstance(result, list)

    def test_unknown_command(self):
        """Should return empty list for unknown command."""
        result = list_fragments("completely-unknown-command-xyz")
        assert result == []


class TestGetStageOrder:
    """Tests for get_stage_order function."""

    def test_returns_sorted_list(self):
        """Should return sorted list."""
        result = get_stage_order("constitution")
        assert isinstance(result, list)
        if len(result) > 1:
            # Should be sorted
            assert result == sorted(result, key=lambda x: (
                int(x.split("-")[0].rstrip("abcdefghijklmnopqrstuvwxyz")) if x.split("-")[0].rstrip("abcdefghijklmnopqrstuvwxyz").isdigit() else 999,
                x
            ))

    def test_sorts_numeric_prefix(self):
        """Should sort by numeric prefix."""
        # Mock test with known ordering
        stages = ["02-second", "01-first", "03-third"]

        def sort_key(name):
            import re
            match = re.match(r"(\d+)([a-z]?)-?(.*)", name)
            if match:
                num = int(match.group(1))
                letter = match.group(2) or "z"
                rest = match.group(3)
                return (num, letter, rest)
            return (999, "z", name)

        result = sorted(stages, key=sort_key)
        assert result == ["01-first", "02-second", "03-third"]


class TestFragmentExists:
    """Tests for fragment_exists function."""

    def test_existing_fragment(self):
        """Should return True for existing fragment."""
        try:
            content = get_prompt_fragment("constitution", "01-initialization")
            assert fragment_exists("constitution", "01-initialization") is True
        except FileNotFoundError:
            # If fragment doesn't exist, function should return False
            assert fragment_exists("constitution", "01-initialization") is False

    def test_nonexistent_fragment(self):
        """Should return False for nonexistent fragment."""
        result = fragment_exists("fake-command", "fake-stage")
        assert result is False


class TestGetNextStage:
    """Tests for get_next_stage function."""

    def test_returns_next(self):
        """Should return next stage in order."""
        stages = get_stage_order("constitution")
        if len(stages) >= 2:
            first = stages[0]
            expected_next = stages[1]
            result = get_next_stage("constitution", first)
            assert result == expected_next

    def test_last_stage_returns_none(self):
        """Should return None for last stage."""
        stages = get_stage_order("constitution")
        if stages:
            last = stages[-1]
            result = get_next_stage("constitution", last)
            assert result is None

    def test_unknown_stage_returns_none(self):
        """Should return None for unknown stage."""
        result = get_next_stage("constitution", "unknown-stage-xyz")
        assert result is None


class TestCountFragmentLines:
    """Tests for count_fragment_lines function."""

    def test_existing_fragment(self):
        """Should count lines for existing fragment."""
        try:
            content = get_prompt_fragment("constitution", "01-initialization")
            expected = len(content.splitlines())
            result = count_fragment_lines("constitution", "01-initialization")
            assert result == expected
        except FileNotFoundError:
            # Fragment doesn't exist
            result = count_fragment_lines("constitution", "01-initialization")
            assert result == 0

    def test_nonexistent_fragment(self):
        """Should return 0 for nonexistent fragment."""
        result = count_fragment_lines("fake", "fake")
        assert result == 0


class TestCopyTemplateDirective:
    """Tests for copy-template directive in render_prompt."""

    def test_copy_template_success(self, tmp_path):
        """Should copy template to feature_dir."""
        # Create a test feature_dir
        feature_dir = tmp_path / "specs" / "001-test-feature"
        feature_dir.mkdir(parents=True)

        fragment = "Before\n{{copy-template:spec-template.md:spec.md}}\nAfter"
        context = {"feature_dir": str(feature_dir)}

        try:
            result = render_prompt(fragment, context)

            assert "Before" in result
            assert "After" in result

            # Template should be copied
            copied_file = feature_dir / "spec.md"
            if "[Template not found" not in result:
                assert copied_file.exists()
                content = copied_file.read_text()
                assert "Feature Specification" in content
        except FileNotFoundError:
            pytest.skip("Template not found in test environment")

    def test_copy_template_default_destination(self, tmp_path):
        """Should use default destination when not specified."""
        feature_dir = tmp_path / "specs" / "001-test-feature"
        feature_dir.mkdir(parents=True)

        # Without :dest.md, should use template name minus '-template'
        fragment = "{{copy-template:plan-template.md}}"
        context = {"feature_dir": str(feature_dir)}

        try:
            result = render_prompt(fragment, context)

            # If template exists, should copy to plan.md
            copied_file = feature_dir / "plan.md"
            if "[Template not found" not in result:
                assert copied_file.exists()
        except FileNotFoundError:
            pytest.skip("Template not found in test environment")

    def test_copy_template_no_feature_dir(self):
        """Should show error when feature_dir not set."""
        fragment = "{{copy-template:spec-template.md:spec.md}}"
        context = {}  # No feature_dir

        result = render_prompt(fragment, context)

        assert "[Cannot copy template: feature_dir not set]" in result

    def test_copy_template_not_found_graceful(self, tmp_path):
        """Should show error for missing template in non-strict mode."""
        feature_dir = tmp_path / "specs" / "001-test-feature"
        feature_dir.mkdir(parents=True)

        fragment = "{{copy-template:nonexistent-template.md:dest.md}}"
        context = {"feature_dir": str(feature_dir)}

        result = render_prompt(fragment, context)

        assert "[Template not found: nonexistent-template.md]" in result

    def test_copy_template_strict_mode_raises(self, tmp_path):
        """Should raise FileNotFoundError in strict mode for missing template."""
        feature_dir = tmp_path / "specs" / "001-test-feature"
        feature_dir.mkdir(parents=True)

        fragment = "{{copy-template:nonexistent-template.md:dest.md}}"
        context = {"feature_dir": str(feature_dir)}

        with pytest.raises(FileNotFoundError) as exc_info:
            render_prompt(fragment, context, strict=True)

        assert "nonexistent-template.md" in str(exc_info.value)

    def test_copy_template_skips_existing_file(self, tmp_path):
        """Should skip copy and warn if destination file already exists."""
        feature_dir = tmp_path / "specs" / "001-test-feature"
        feature_dir.mkdir(parents=True)

        # Pre-create the destination file with custom content
        dest_file = feature_dir / "spec.md"
        original_content = "# User's custom spec content\n\nDo not overwrite!"
        dest_file.write_text(original_content)

        fragment = "{{copy-template:spec-template.md:spec.md}}"
        context = {"feature_dir": str(feature_dir)}

        result = render_prompt(fragment, context)

        # Should show warning instead of success message
        assert "⚠ Template already exists:" in result
        assert "(not overwritten)" in result

        # Original content should be preserved
        assert dest_file.read_text() == original_content
