"""Test prompt content for consistency and correctness."""

import re
from pathlib import Path

import pytest


def get_assets_dir() -> Path:
    """Get the assets directory path."""
    return Path(__file__).parent.parent / "speckit" / "assets"


def get_prompt_files() -> list[Path]:
    """Get all prompt markdown files."""
    prompts_dir = get_assets_dir() / "prompts"
    if prompts_dir.exists():
        return list(prompts_dir.rglob("*.md"))
    return []


class TestPromptContent:
    """Test prompt files for content consistency."""

    def test_no_powershell_in_bash_blocks(self):
        """Test that bash code blocks don't contain PowerShell-specific syntax."""
        powershell_patterns = [
            r'\$null\b',
            r'\$env:',
            r'\$LASTEXITCODE\b',
            r'@"[\s\S]*?"@',  # PowerShell here-string
        ]

        violations = []
        for prompt_file in get_prompt_files():
            content = prompt_file.read_text(encoding="utf-8")

            # Find bash code blocks
            bash_blocks = re.findall(r'```bash\n(.*?)```', content, re.DOTALL)

            for block in bash_blocks:
                for pattern in powershell_patterns:
                    matches = re.findall(pattern, block)
                    if matches:
                        rel_path = prompt_file.relative_to(get_assets_dir())
                        violations.append(f"{rel_path}: PowerShell pattern '{pattern}' in bash block")

        assert not violations, f"PowerShell syntax in bash blocks:\n" + "\n".join(violations)


class TestAgentsGuidelines:
    """Test AGENTS.md guidelines file."""

    def test_agents_md_has_critical_rules(self):
        """Test that AGENTS.md has expected critical rules."""
        agents_file = get_assets_dir() / "AGENTS.md"
        assert agents_file.exists(), "AGENTS.md not found"

        content = agents_file.read_text(encoding="utf-8")

        required_rules = [
            "CLI First",
            "CLI Flags",
            "Bash Only",
            "ASCII-Only",
            "Mermaid Diagrams",
        ]

        for rule in required_rules:
            assert rule in content, f"AGENTS.md missing required rule: {rule}"

    def test_agents_md_version_format(self):
        """Test that AGENTS.md has valid version format."""
        agents_file = get_assets_dir() / "AGENTS.md"
        content = agents_file.read_text(encoding="utf-8")

        # Check for version line
        version_match = re.search(r'\*\*Version:\*\*\s+(\d+\.\d+)', content)
        assert version_match, "AGENTS.md missing version number"

        version = version_match.group(1)
        major, minor = map(int, version.split('.'))
        assert major >= 3, f"AGENTS.md version {version} seems outdated"
