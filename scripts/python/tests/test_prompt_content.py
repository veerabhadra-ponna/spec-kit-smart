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

    def test_no_shell_cross_contamination(self):
        """Test that bash blocks don't contain PowerShell and vice versa."""
        powershell_patterns = [
            r'\$env:',  # PowerShell environment variable
            r'\$null\b',
            r'\$LASTEXITCODE\b',
            r'@"[\s\S]*?"@',  # PowerShell here-string
        ]
        bash_patterns = [
            r'\bcat\s+<<',  # bash heredoc
            r'\bfi\b',  # bash if-fi
            r'\bdone\b',  # bash for-done
        ]

        violations = []
        for prompt_file in get_prompt_files():
            content = prompt_file.read_text(encoding="utf-8")
            rel_path = prompt_file.relative_to(get_assets_dir())

            # Check bash blocks don't have PowerShell
            bash_blocks = re.findall(r'```bash\n(.*?)```', content, re.DOTALL)
            for block in bash_blocks:
                for pattern in powershell_patterns:
                    if re.search(pattern, block):
                        violations.append(f"{rel_path}: PowerShell pattern in bash block")
                        break

            # Check PowerShell blocks don't have bash
            ps_blocks = re.findall(r'```powershell\n(.*?)```', content, re.DOTALL)
            for block in ps_blocks:
                for pattern in bash_patterns:
                    if re.search(pattern, block):
                        violations.append(f"{rel_path}: Bash pattern in powershell block")
                        break

        assert not violations, f"Shell cross-contamination:\n" + "\n".join(violations)


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
            "OS Shell",
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
        assert major >= 1, f"AGENTS.md version {version} is invalid"
