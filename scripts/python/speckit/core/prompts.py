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


def load_template(template_path: str, workspace_root: Path = None) -> str:
    """
    Load a template file, checking project overrides before CLI embedded templates.

    Search order (matching workflow.py behavior):
    1. memory/templates/ (project-level)
    2. .specify/templates/ (project-level)
    3. templates/ (project-level)
    4. CLI embedded templates (fallback - from speckit package)

    Args:
        template_path: Relative path to template (e.g., "spec-template.md")
        workspace_root: Optional workspace root for finding project overrides

    Returns:
        Template content

    Raises:
        FileNotFoundError: If template not found in any location
    """
    from speckit.core.utils import find_repo_root

    # Determine workspace root for project overrides
    if workspace_root is None:
        try:
            workspace_root = find_repo_root()
        except (FileNotFoundError, RuntimeError):
            workspace_root = Path.cwd()

    # Search paths in priority order (project overrides first)
    search_paths = [
        workspace_root / "memory" / "templates" / template_path,
        workspace_root / ".specify" / "templates" / template_path,
        workspace_root / "templates" / template_path,
        get_templates_base() / template_path,  # Fallback to CLI embedded templates
    ]

    for full_path in search_paths:
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


def render_prompt(fragment: str, context: dict, *, strict: bool = False) -> str:
    """
    Render a prompt fragment with context variables and template includes.

    Supports:
    - {variable} - Simple substitution
    - {variable:default} - With default value
    - {{escaped}} - Literal braces (preserved as single braces)
    - {{include:template.md}} - Include template file inline from assets/templates/
    - {{copy-template:source.md:dest.md}} - Copy template to feature_dir/dest.md

    Args:
        fragment: Prompt fragment content
        context: Variables to substitute (must include 'feature_dir' for copy-template)
        strict: If True, raise FileNotFoundError for missing templates (for CI/tests).
                If False (default), return placeholder text for graceful degradation.

    Returns:
        Rendered prompt

    Raises:
        FileNotFoundError: If strict=True and a template is not found
    """
    import re

    result = fragment
    missing_templates: list[str] = []

    # Determine workspace root from context for template override resolution
    # This ensures templates are found even when CLI runs from outside the project
    workspace_root = None
    if context.get("project_path"):
        workspace_root = Path(context["project_path"])
    elif context.get("feature_dir"):
        # Derive from feature_dir (specs/XXX -> project root)
        feature_path = Path(context["feature_dir"])
        if feature_path.parent.name == "specs":
            workspace_root = feature_path.parent.parent

    # Handle template copy: {{copy-template:source.md:dest.md}}
    # This copies the template to feature_dir/dest.md and returns a confirmation
    def copy_template(match: re.Match) -> str:
        template_path = match.group(1).strip()
        dest_filename = match.group(2).strip() if match.group(2) else template_path.replace("-template", "")
        feature_dir = context.get("feature_dir", "")

        if not feature_dir:
            return f"[Cannot copy template: feature_dir not set]"

        try:
            dest_path = Path(feature_dir) / dest_filename

            # Skip if file already exists (avoid overwriting user edits on re-run)
            if dest_path.exists():
                return f"⚠ Template already exists: `{dest_path}` (not overwritten)"

            template_content = load_template(template_path, workspace_root=workspace_root)

            # Ensure directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the template content
            dest_path.write_text(template_content, encoding="utf-8")

            return f"[ok] Template copied: `{dest_path}`"
        except FileNotFoundError:
            if strict:
                missing_templates.append(template_path)
            return f"[Template not found: {template_path}]"
        except OSError as e:
            return f"[Failed to copy template: {e}]"

    result = re.sub(r"\{\{copy-template:([^:}]+)(?::([^}]+))?\}\}", copy_template, result)

    # Handle template includes: {{include:path/to/template.md}}
    # This must happen before escaping braces
    def include_template(match: re.Match) -> str:
        template_path = match.group(1).strip()
        try:
            template_content = load_template(template_path, workspace_root=workspace_root)
            # Recursively render the included template (for nested includes and variables)
            return render_prompt(template_content, context, strict=strict)
        except FileNotFoundError:
            if strict:
                missing_templates.append(template_path)
            return f"[Template not found: {template_path}]"

    result = re.sub(r"\{\{include:([^}]+)\}\}", include_template, result)

    # In strict mode, fail after processing all includes to report all missing templates
    if strict and missing_templates:
        raise FileNotFoundError(f"Missing templates: {', '.join(missing_templates)}")

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
