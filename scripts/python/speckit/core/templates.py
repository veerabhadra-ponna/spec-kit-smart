"""
Template System

Handles loading and extraction of embedded templates.
Templates can be embedded in the EXE or loaded from filesystem.
"""

import sys
from pathlib import Path
from typing import Optional

from speckit.core.utils import ensure_dir


def get_assets_base() -> Path:
    """
    Get the base path for assets.

    Returns:
        Path to assets directory (handles both dev and frozen modes)
    """
    if getattr(sys, "frozen", False):
        # Running as compiled executable (PyInstaller)
        return Path(sys._MEIPASS) / "assets"  # type: ignore
    else:
        # Running in development
        return Path(__file__).parent.parent / "assets"


def get_templates_path() -> Path:
    """Get path to templates directory."""
    return get_assets_base() / "templates"


def get_embedded_template(name: str) -> str:
    """
    Load a template from embedded assets.

    Args:
        name: Template name (without .md extension)

    Returns:
        Template content

    Raises:
        FileNotFoundError: If template not found
    """
    # Try multiple locations
    search_paths = [
        get_templates_path() / f"{name}.md",
        get_templates_path() / name / "template.md",
        get_templates_path() / f"{name}-template.md",
    ]

    for path in search_paths:
        if path.exists():
            return path.read_text(encoding="utf-8")

    # If not in embedded assets, try source templates directory
    repo_templates = Path(__file__).parent.parent.parent.parent.parent / "templates"
    if repo_templates.exists():
        # Check analyze templates
        analyze_template = repo_templates / "analyze" / f"{name}.md"
        if analyze_template.exists():
            return analyze_template.read_text(encoding="utf-8")

        # Check main templates
        main_template = repo_templates / f"{name}.md"
        if main_template.exists():
            return main_template.read_text(encoding="utf-8")

    raise FileNotFoundError(f"Template not found: {name}")


def extract_template(name: str, dest_dir: Path) -> Path:
    """
    Extract an embedded template to the filesystem.

    Args:
        name: Template name
        dest_dir: Destination directory

    Returns:
        Path to extracted template file
    """
    content = get_embedded_template(name)

    # Create templates subdirectory
    templates_dir = ensure_dir(dest_dir / "templates")
    dest_path = templates_dir / f"{name}.md"

    dest_path.write_text(content, encoding="utf-8")
    return dest_path


def template_exists(name: str) -> bool:
    """
    Check if a template exists.

    Args:
        name: Template name

    Returns:
        True if template exists
    """
    try:
        get_embedded_template(name)
        return True
    except FileNotFoundError:
        return False


def list_templates() -> list[str]:
    """
    List all available templates.

    Returns:
        List of template names
    """
    templates = []
    templates_path = get_templates_path()

    if templates_path.exists():
        for path in templates_path.rglob("*.md"):
            name = path.stem
            if name not in templates:
                templates.append(name)

    return sorted(templates)


def render_template(template: str, context: dict) -> str:
    """
    Render a template with context variables.

    Simple {placeholder} replacement.

    Args:
        template: Template content
        context: Variables to substitute

    Returns:
        Rendered template
    """
    result = template

    for key, value in context.items():
        placeholder = "{" + key + "}"
        result = result.replace(placeholder, str(value))

    return result


def emit_with_template(
    stage_info: dict,
    template_name: str,
    context: dict,
    output_file: str,
    inline_threshold: int = 100,
) -> None:
    """
    Emit a stage with template - inline if small, extract if large.

    Args:
        stage_info: Dict with num, total, title, next_cmd
        template_name: Name of template to use
        context: Data for filling template
        output_file: Where to save filled template
        inline_threshold: Max lines for inline output
    """
    from speckit.core.emit import emit_template as _emit_template

    template_content = get_embedded_template(template_name)
    line_count = len(template_content.splitlines())

    if line_count <= inline_threshold:
        # Inline the template in output
        _emit_template(stage_info, template_content, context, output_file)
    else:
        # Extract to filesystem and reference
        workspace = context.get("workspace", ".")
        dest_path = extract_template(template_name, Path(workspace))

        from speckit.core.emit import emit_stage

        emit_stage(
            stage_num=stage_info["num"],
            total_stages=stage_info["total"],
            title=stage_info["title"],
            content=f"""Template extracted to: {dest_path}

1. Read the template file
2. Fill all {{placeholders}} with data below
3. Save to: {output_file}

Data for template:
""" + "\n".join(f"  {k}: {v}" for k, v in context.items()),
            next_cmd=stage_info["next_cmd"],
        )
