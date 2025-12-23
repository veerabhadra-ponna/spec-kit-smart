"""
Prompt Fragment System

Loads and renders prompt fragments for progressive injection.
Fragments are small (<100 lines) focused prompts for each workflow stage.
"""

import sys
from pathlib import Path
from typing import Optional

from speckit.core.utils import safe_json_loads


def get_prompts_base() -> Path:
    """
    Get the base path for prompts.

    Returns:
        Path to prompts directory (handles dev, pip install, and frozen modes)
    """
    if getattr(sys, "frozen", False):
        # Running as compiled executable (PyInstaller)
        # Assets are embedded at assets/prompts/
        return Path(sys._MEIPASS) / "assets" / "prompts"  # type: ignore

    # Check for package assets first (pip install)
    package_assets = Path(__file__).parent.parent / "assets" / "prompts"
    if package_assets.exists() and any(package_assets.glob("**/*.md")):
        return package_assets

    # Fall back to repo templates (development mode)
    repo_templates = Path(__file__).parent.parent.parent.parent.parent / "templates" / "commands"
    if repo_templates.exists() and any(repo_templates.glob("**/*.md")):
        return repo_templates

    # Default to package assets path (may not exist yet)
    return package_assets


def get_templates_base() -> Path:
    """
    Get the base path for templates.

    Returns:
        Path to templates directory (handles dev, pip install, and frozen modes)
    """
    if getattr(sys, "frozen", False):
        # Running as compiled executable (PyInstaller)
        return Path(sys._MEIPASS) / "assets" / "templates"  # type: ignore

    # Check for package assets first (pip install)
    package_assets = Path(__file__).parent.parent / "assets" / "templates"
    if package_assets.exists():
        return package_assets

    # Default to package assets path
    return package_assets


def load_template(template_path: str) -> str:
    """
    Load a template file from assets/templates/.

    Args:
        template_path: Relative path to template (e.g., "spec-template.md" or "stage-prompt-templates/clarify-prompt-template.md")

    Returns:
        Template content

    Raises:
        FileNotFoundError: If template not found
    """
    templates_base = get_templates_base()
    full_path = templates_base / template_path

    if full_path.exists():
        return full_path.read_text(encoding="utf-8")

    raise FileNotFoundError(f"Template not found: {template_path}")


def get_prompt_fragment(command: str, stage: str) -> str:
    """
    Load a prompt fragment for a specific command and stage.

    Args:
        command: Command name (e.g., "analyze-project", "constitution")
        stage: Stage identifier (e.g., "01-setup", "02a-category-scan")
               Use empty string for single-file prompts

    Returns:
        Prompt fragment content

    Raises:
        FileNotFoundError: If fragment not found
    """
    prompts_base = get_prompts_base()

    # Try multiple naming patterns
    search_paths = [
        # New fragmented structure: analyze/01a-initialization.md
        prompts_base / command.replace("-", "/") / f"{stage}.md",
        prompts_base / command / f"{stage}.md",
        # Nested structure: analyze-project/stage1.md
        prompts_base / command / f"stage{stage}.md",
        # Flat structure: analyze-project-stage1.md
        prompts_base / f"{command}-{stage}.md",
        # Direct match for analyze subfolder
        prompts_base / "analyze" / f"{stage}.md",
        # Single-file prompts (no staging): orchestrate.md, resume.md
        prompts_base / f"{command}.md",
    ]

    for path in search_paths:
        if path.exists():
            return path.read_text(encoding="utf-8")

    raise FileNotFoundError(f"Prompt fragment not found: {command}/{stage}")


def render_prompt(fragment: str, context: dict) -> str:
    """
    Render a prompt fragment with context variables and template includes.

    Supports:
    - {variable} - Simple substitution
    - {variable:default} - With default value
    - {{escaped}} - Literal braces (preserved as single braces)
    - {{include:template.md}} - Include template file from assets/templates/

    Args:
        fragment: Prompt fragment content
        context: Variables to substitute

    Returns:
        Rendered prompt
    """
    import re

    result = fragment

    # First, handle template includes: {{include:path/to/template.md}}
    # This must happen before escaping braces
    def include_template(match: re.Match) -> str:
        template_path = match.group(1).strip()
        try:
            template_content = load_template(template_path)
            # Recursively render the included template (for nested includes and variables)
            return render_prompt(template_content, context)
        except FileNotFoundError:
            return f"[Template not found: {template_path}]"

    result = re.sub(r"\{\{include:([^}]+)\}\}", include_template, result)

    # Handle escaped braces (convert to placeholders)
    result = result.replace("{{", "\x00LBRACE\x00")
    result = result.replace("}}", "\x00RBRACE\x00")

    # Handle default values: {key:default}
    def replace_with_default(match: re.Match) -> str:
        key = match.group(1)
        default = match.group(2) if match.group(2) else ""
        return str(context.get(key, default))

    result = re.sub(r"\{(\w+)(?::([^}]*))?\}", replace_with_default, result)

    # Restore escaped braces
    result = result.replace("\x00LBRACE\x00", "{")
    result = result.replace("\x00RBRACE\x00", "}")

    return result


def list_fragments(command: str) -> list[str]:
    """
    List all available fragments for a command.

    Args:
        command: Command name

    Returns:
        List of stage identifiers
    """
    prompts_base = get_prompts_base()
    fragments = []

    # Check command subdirectory
    command_dir = prompts_base / command
    if command_dir.exists():
        for path in command_dir.glob("*.md"):
            fragments.append(path.stem)

    # Check analyze subdirectory (special case for analyze-project)
    if command in ("analyze-project", "analyze"):
        analyze_dir = prompts_base / "analyze"
        if analyze_dir.exists():
            for path in analyze_dir.glob("*.md"):
                if path.stem not in fragments:
                    fragments.append(path.stem)

    return sorted(fragments)


def get_stage_order(command: str) -> list[str]:
    """
    Get the ordered list of stages for a command.

    Args:
        command: Command name

    Returns:
        Ordered list of stage identifiers
    """
    fragments = list_fragments(command)

    # Sort by numeric prefix if present
    def sort_key(name: str) -> tuple:
        # Extract numeric prefix: "01a-setup" -> (1, "a", "setup")
        import re

        match = re.match(r"(\d+)([a-z]?)-?(.*)", name)
        if match:
            num = int(match.group(1))
            letter = match.group(2) or "z"  # No letter sorts last
            rest = match.group(3)
            return (num, letter, rest)
        return (999, "z", name)

    return sorted(fragments, key=sort_key)


def fragment_exists(command: str, stage: str) -> bool:
    """
    Check if a prompt fragment exists.

    Args:
        command: Command name
        stage: Stage identifier

    Returns:
        True if fragment exists
    """
    try:
        get_prompt_fragment(command, stage)
        return True
    except FileNotFoundError:
        return False


def get_next_stage(command: str, current_stage: str) -> Optional[str]:
    """
    Get the next stage after the current one.

    Args:
        command: Command name
        current_stage: Current stage identifier

    Returns:
        Next stage identifier, or None if at end
    """
    stages = get_stage_order(command)

    try:
        idx = stages.index(current_stage)
        if idx + 1 < len(stages):
            return stages[idx + 1]
    except ValueError:
        pass

    return None


def count_fragment_lines(command: str, stage: str) -> int:
    """
    Count lines in a fragment.

    Args:
        command: Command name
        stage: Stage identifier

    Returns:
        Number of lines
    """
    try:
        fragment = get_prompt_fragment(command, stage)
        return len(fragment.splitlines())
    except FileNotFoundError:
        return 0
