"""
Workflow helper commands for speckitadv.

Ports functionality from:
- setup-plan.sh
- update-agent-context.sh
"""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console

from speckit.core.prompts import get_templates_base, load_template
from speckit.core.utils import find_repo_root

console = Console()


def has_git() -> bool:
    """Check if current directory is a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_current_branch() -> str:
    """Get current branch name or feature from environment."""
    # Check environment variable first
    if os.environ.get("SPECIFY_FEATURE"):
        return os.environ["SPECIFY_FEATURE"]

    # Try git
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback: find latest feature directory
    repo_root = find_repo_root()
    specs_dir = repo_root / "specs"

    if specs_dir.exists():
        highest = 0
        latest_feature = ""

        for item in specs_dir.iterdir():
            if item.is_dir():
                match = re.match(r"^(\d{3})-", item.name)
                if match:
                    num = int(match.group(1))
                    if num > highest:
                        highest = num
                        latest_feature = item.name

        if latest_feature:
            return latest_feature

    return "main"


def get_feature_paths(repo_root: Optional[Path] = None) -> dict:
    """Get all feature-related paths."""
    root = repo_root or find_repo_root()
    branch = get_current_branch()

    # Extract folder name from branch (after last /)
    folder_name = branch.split("/")[-1].split("\\")[-1]

    feature_dir = root / "specs" / folder_name

    return {
        "REPO_ROOT": root,
        "CURRENT_BRANCH": branch,
        "HAS_GIT": has_git(),
        "FEATURE_DIR": feature_dir,
        "FEATURE_SPEC": feature_dir / "spec.md",
        "IMPL_PLAN": feature_dir / "plan.md",
        "TASKS": feature_dir / "tasks.md",
        "RESEARCH": feature_dir / "research.md",
        "DATA_MODEL": feature_dir / "data-model.md",
        "QUICKSTART": feature_dir / "quickstart.md",
        "CONTRACTS_DIR": feature_dir / "contracts",
    }


def run_setup_plan(
    arguments: Optional[str] = None,
    output_json: bool = False,
) -> dict:
    """
    Set up plan file from template.

    Replaces setup-plan.sh functionality.

    Args:
        arguments: Optional user description to record in plan template
        output_json: Output results in JSON format

    Returns:
        Dictionary with path information
    """
    paths = get_feature_paths()

    repo_root = paths["REPO_ROOT"]
    branch = paths["CURRENT_BRANCH"]
    feature_dir = paths["FEATURE_DIR"]
    impl_plan = paths["IMPL_PLAN"]
    feature_spec = paths["FEATURE_SPEC"]

    # Validate branch (for git repos)
    if paths["HAS_GIT"] and not re.match(r"^\d{3}-", branch.split("/")[-1].split("\\")[-1]):
        console.print(f"[yellow]Warning:[/yellow] Not on a feature branch. Current: {branch}")

    # Ensure feature directory exists
    feature_dir.mkdir(parents=True, exist_ok=True)

    # Skip if plan already exists (avoid overwriting user edits on re-run)
    if impl_plan.exists():
        console.print(
            f"[yellow]⚠[/yellow] Plan already exists at {impl_plan} (not overwritten)"
        )
    else:
        # Load template using centralized function (handles frozen builds + project overrides)
        try:
            content = load_template("plan-template.md", workspace_root=repo_root)

            # Replace Input line if arguments provided
            if arguments:
                # Escape special characters
                escaped = arguments.replace("\\", "\\\\").replace("&", "\\&")
                content = re.sub(
                    r"\*\*Input\*\*:.*",
                    f'**Input**: User description: "{escaped}"',
                    content,
                )

            impl_plan.write_text(content, encoding="utf-8")
            console.print(f"[green][ok][/green] Copied plan template to {impl_plan}")
        except FileNotFoundError:
            console.print("[yellow]Warning:[/yellow] Plan template not found")
            impl_plan.touch()

    result = {
        "FEATURE_SPEC": str(feature_spec),
        "IMPL_PLAN": str(impl_plan),
        "SPECS_DIR": str(feature_dir),
        "BRANCH": branch,
        "HAS_GIT": str(paths["HAS_GIT"]).lower(),
    }

    if output_json:
        print(json.dumps(result))
    else:
        for key, value in result.items():
            console.print(f"{key}: {value}")

    return result


# Agent file configurations
AGENT_FILES = {
    "claude": ("CLAUDE.md", "Claude Code"),
    "gemini": ("GEMINI.md", "Gemini CLI"),
    "copilot": (".github/copilot-instructions.md", "GitHub Copilot"),
    "cursor-agent": (".cursor/commands/speckitadv-rules.md", "Cursor IDE"),
    "qwen": ("QWEN.md", "Qwen Code"),
    "opencode": ("AGENTS.md", "opencode"),
    "codex": ("AGENTS.md", "Codex CLI"),
    "windsurf": (".windsurf/rules/specify-rules.md", "Windsurf"),
    "kilocode": (".kilocode/rules/specify-rules.md", "Kilo Code"),
    "auggie": (".augment/rules/specify-rules.md", "Auggie CLI"),
    "roo": (".roo/rules/specify-rules.md", "Roo Code"),
    "codebuddy": ("CODEBUDDY.md", "CodeBuddy CLI"),
    "amp": ("AGENTS.md", "Amp"),
    "q": ("AGENTS.md", "Amazon Q Developer CLI"),
}


def extract_plan_field(plan_content: str, field: str) -> str:
    """Extract field value from plan.md content."""
    pattern = rf"^\*\*{re.escape(field)}\*\*:\s*(.+)$"
    match = re.search(pattern, plan_content, re.MULTILINE)
    if match:
        value = match.group(1).strip()
        if value and value not in ("NEEDS CLARIFICATION", "N/A"):
            return value
    return ""


def parse_plan_data(plan_path: Path) -> dict:
    """Parse plan.md to extract project information."""
    if not plan_path.exists():
        return {}

    content = plan_path.read_text(encoding="utf-8")

    return {
        "language": extract_plan_field(content, "Language/Version"),
        "framework": extract_plan_field(content, "Primary Dependencies"),
        "database": extract_plan_field(content, "Storage"),
        "project_type": extract_plan_field(content, "Project Type"),
    }


def format_technology_stack(lang: str, framework: str) -> str:
    """Format technology stack string."""
    parts = []
    if lang:
        parts.append(lang)
    if framework:
        parts.append(framework)
    return " + ".join(parts) if parts else ""


def get_commands_for_language(lang: str) -> str:
    """Get build/test commands for a language."""
    lang_lower = lang.lower()
    if "python" in lang_lower:
        return "cd src && pytest && ruff check ."
    if "rust" in lang_lower:
        return "cargo test && cargo clippy"
    if "javascript" in lang_lower or "typescript" in lang_lower:
        return "npm test && npm run lint"
    if "java" in lang_lower:
        return "mvn test"
    if "go" in lang_lower:
        return "go test ./..."
    return f"# Add commands for {lang}"


def update_agent_file(
    target_file: Path,
    agent_name: str,
    plan_data: dict,
    branch: str,
    template_path: Optional[Path] = None,
) -> bool:
    """
    Update or create an agent context file.

    Args:
        target_file: Path to agent file
        agent_name: Display name of agent
        plan_data: Parsed plan data
        branch: Current branch name
        template_path: Optional path to template file

    Returns:
        True if successful
    """
    # Ensure parent directory exists
    target_file.parent.mkdir(parents=True, exist_ok=True)

    current_date = datetime.now().strftime("%Y-%m-%d")
    lang = plan_data.get("language", "")
    framework = plan_data.get("framework", "")
    database = plan_data.get("database", "")
    project_type = plan_data.get("project_type", "")

    tech_stack = format_technology_stack(lang, framework)

    if not target_file.exists():
        # Create new file from template
        if template_path and template_path.exists():
            content = template_path.read_text(encoding="utf-8")

            # Replace placeholders
            content = content.replace("[PROJECT NAME]", target_file.parent.parent.name)
            content = content.replace("[DATE]", current_date)

            tech_entry = f"- {tech_stack} ({branch})" if tech_stack else f"- ({branch})"
            content = content.replace("[EXTRACTED FROM ALL PLAN.MD FILES]", tech_entry)

            structure = "backend/\nfrontend/\ntests/" if "web" in project_type.lower() else "src/\ntests/"
            content = content.replace("[ACTUAL STRUCTURE FROM PLANS]", structure)

            commands = get_commands_for_language(lang)
            content = content.replace("[ONLY COMMANDS FOR ACTIVE TECHNOLOGIES]", commands)

            conventions = f"{lang}: Follow standard conventions" if lang else "Follow standard conventions"
            content = content.replace("[LANGUAGE-SPECIFIC, ONLY FOR LANGUAGES IN USE]", conventions)

            recent = f"- {branch}: Added {tech_stack}" if tech_stack else f"- {branch}: Initial setup"
            content = content.replace("[LAST 3 FEATURES AND WHAT THEY ADDED]", recent)

            target_file.write_text(content, encoding="utf-8")
            console.print(f"[green][ok][/green] Created new {agent_name} context file")
        else:
            # Create minimal file
            content = f"""# {agent_name} Context

**Last updated**: {current_date}

## Active Technologies

- {tech_stack} ({branch})

## Recent Changes

- {branch}: Added {tech_stack if tech_stack else 'initial setup'}
"""
            target_file.write_text(content, encoding="utf-8")
            console.print(f"[green][ok][/green] Created minimal {agent_name} context file")

        return True

    # Update existing file
    content = target_file.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    new_lines = []

    in_tech_section = False
    in_changes_section = False
    tech_added = False
    changes_count = 0

    new_tech_entry = f"- {tech_stack} ({branch})\n" if tech_stack else None
    new_change_entry = f"- {branch}: Added {tech_stack}\n" if tech_stack else None

    # Check if entries already exist (avoid duplicates)
    tech_already_exists = new_tech_entry and new_tech_entry.strip() in content
    change_already_exists = new_change_entry and new_change_entry.strip() in content

    for line in lines:
        # Update timestamp
        if "**Last updated**:" in line:
            line = re.sub(r"\d{4}-\d{2}-\d{2}", current_date, line)

        # Handle Active Technologies section
        if line.strip() == "## Active Technologies":
            new_lines.append(line)
            in_tech_section = True
            continue

        if in_tech_section:
            if line.startswith("## "):
                # End of section - add new entry before next heading if not added
                if not tech_added and new_tech_entry and not tech_already_exists:
                    new_lines.append(new_tech_entry)
                    new_lines.append("\n")  # Blank line before heading
                in_tech_section = False
                # Fall through to append the heading line
            elif line.strip() == "":
                # Blank line - add new entry before it if not added yet
                if not tech_added and new_tech_entry and not tech_already_exists:
                    new_lines.append(new_tech_entry)
                    tech_added = True
                # Preserve the blank line
                new_lines.append(line)
                continue
            elif line.startswith("- "):
                # Existing tech entry - always preserve it
                new_lines.append(line)
                continue

        # Handle Recent Changes section
        if line.strip() == "## Recent Changes":
            new_lines.append(line)
            in_changes_section = True
            # Add new change right after heading (before existing entries) if not duplicate
            if new_change_entry and not change_already_exists:
                new_lines.append("\n")  # Blank line after heading
                new_lines.append(new_change_entry)
            continue

        if in_changes_section:
            if line.startswith("## "):
                in_changes_section = False
                # Fall through to append the heading
            elif line.startswith("- "):
                changes_count += 1
                if changes_count > 2:
                    continue  # Keep only 3 most recent changes (including the new one)
                # Preserve existing change entries
                new_lines.append(line)
                continue
            elif line.strip() == "":
                # Skip extra blank lines in changes section
                if changes_count == 0:
                    continue  # Skip blank line right after heading (we added our own)

        new_lines.append(line)

    target_file.write_text("".join(new_lines), encoding="utf-8")
    console.print(f"[green][ok][/green] Updated {agent_name} context file")
    return True


def run_update_agent_context(agent_type: Optional[str] = None) -> bool:
    """
    Update agent context files with information from plan.md.

    Replaces update-agent-context.sh functionality.

    Args:
        agent_type: Specific agent to update, or None for all

    Returns:
        True if successful
    """
    paths = get_feature_paths()
    repo_root = paths["REPO_ROOT"]
    branch = paths["CURRENT_BRANCH"]
    plan_path = paths["IMPL_PLAN"]

    if not plan_path.exists():
        console.print(f"[red]Error:[/red] No plan.md found at {plan_path}")
        return False

    console.print(f"[bold]=== Updating agent context for {branch} ===[/bold]\n")

    # Parse plan data
    plan_data = parse_plan_data(plan_path)

    if plan_data.get("language"):
        console.print(f"[dim]Found language: {plan_data['language']}[/dim]")
    if plan_data.get("framework"):
        console.print(f"[dim]Found framework: {plan_data['framework']}[/dim]")

    # Check for template in priority order (use get_templates_base for frozen build support)
    template_path = None
    search_paths = [
        repo_root / "memory" / "templates" / "agent-file-template.md",
        repo_root / ".specify" / "templates" / "agent-file-template.md",
        repo_root / "templates" / "agent-file-template.md",
        get_templates_base() / "agent-file-template.md",
    ]
    for path in search_paths:
        if path.exists():
            template_path = path
            break

    success = True

    if agent_type:
        # Update specific agent
        if agent_type not in AGENT_FILES:
            console.print(f"[red]Error:[/red] Unknown agent type: {agent_type}")
            console.print(f"Available: {', '.join(AGENT_FILES.keys())}")
            return False

        rel_path, name = AGENT_FILES[agent_type]
        target_file = repo_root / rel_path
        success = update_agent_file(target_file, name, plan_data, branch, template_path)
    else:
        # Update all existing agent files
        found_agent = False

        for agent_id, (rel_path, name) in AGENT_FILES.items():
            target_file = repo_root / rel_path

            if target_file.exists():
                found_agent = True
                if not update_agent_file(target_file, name, plan_data, branch, template_path):
                    success = False

        # If no agent files exist, create default Claude file
        if not found_agent:
            console.print("[dim]No existing agent files found, creating default Claude file...[/dim]")
            target_file = repo_root / AGENT_FILES["claude"][0]
            success = update_agent_file(target_file, "Claude Code", plan_data, branch, template_path)

    # Print summary
    console.print("\n[bold]Summary of changes:[/bold]")
    if plan_data.get("language"):
        console.print(f"  - Added language: {plan_data['language']}")
    if plan_data.get("framework"):
        console.print(f"  - Added framework: {plan_data['framework']}")
    if plan_data.get("database") and plan_data["database"] != "N/A":
        console.print(f"  - Added database: {plan_data['database']}")

    console.print()
    if success:
        console.print("[green][ok][/green] Agent context update completed")
    else:
        console.print("[red][x][/red] Agent context update completed with errors")

    return success
