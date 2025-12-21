"""
Project initialization command for speckitadv.

Creates project structure with embedded launchers - no network required.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from speckit.setup.config import (
    AGENT_CONFIG,
    WORKFLOW_COMMANDS,
    get_launcher_content,
    get_agent_commands_path,
    get_all_agents,
)

console = Console()


def get_default_config() -> str:
    """Get default config.json content from embedded assets or fallback."""
    if getattr(sys, "frozen", False):
        # PyInstaller binary
        base = Path(sys._MEIPASS) / "assets"  # type: ignore
    else:
        # Development or pip install
        base = Path(__file__).parent.parent / "assets"

    config_file = base / "config-template.json"
    if config_file.exists():
        return config_file.read_text(encoding="utf-8")

    # Fallback default config
    return """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "description": "Spec Kit configuration",
  "version": "2.0",
  "project": {
    "type": "personal",
    "guidelineProfile": "personal"
  },
  "workflow": {
    "enableCheckArtifactory": false,
    "osEnv": "auto"
  },
  "branching": {
    "pattern": "feature/<num>-<jira>-<shortname>",
    "prefix": "feature/",
    "separator": "-",
    "number_format": {
      "digits": 3,
      "zero_padded": true
    },
    "jira": {
      "required": false,
      "format": "C12345-7890",
      "regex": "^C[0-9]{5}-[0-9]{4}$"
    },
    "directory": {
      "includes_prefix": false,
      "base_path": "specs"
    }
  }
}
"""


def get_agents_md_content() -> str:
    """Get AGENTS.md content from embedded assets."""
    if getattr(sys, "frozen", False):
        # PyInstaller binary
        base = Path(sys._MEIPASS) / "assets"  # type: ignore
    else:
        # Development or pip install
        base = Path(__file__).parent.parent / "assets"

    agents_file = base / "AGENTS.md"
    if agents_file.exists():
        return agents_file.read_text(encoding="utf-8")

    # Fallback minimal AGENTS.md
    return """# AGENTS.md

This file provides instructions for AI agents working on this project.

## Project Structure

- `memory/` - Project artifacts (constitution, specs, plans)
- `.analysis/` - Analysis reports (created by analyze-project)

## Workflow Commands

Use the speckitadv slash commands in order:
1. /speckitadv.constitution - Establish project principles
2. /speckitadv.specify - Create baseline specification
3. /speckitadv.plan - Create implementation plan
4. /speckitadv.tasks - Generate actionable tasks
5. /speckitadv.implement - Execute implementation

## Optional Commands

- /speckitadv.clarify - Ask structured questions (before plan)
- /speckitadv.analyze - Cross-artifact consistency check
- /speckitadv.checklist - Generate quality checklist
- /speckitadv.analyze-project - Analyze existing project
"""


def check_tool(tool: str) -> bool:
    """Check if a CLI tool is installed."""
    # Special handling for Claude CLI local path
    if tool == "claude":
        claude_local = Path.home() / ".claude" / "local" / "claude"
        if claude_local.exists():
            return True
    return shutil.which(tool) is not None


def is_git_repo(path: Path) -> bool:
    """Check if path is inside a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path) -> tuple[bool, Optional[str]]:
    """Initialize a git repository."""
    try:
        subprocess.run(
            ["git", "init"],
            check=True,
            capture_output=True,
            cwd=project_path,
        )
        subprocess.run(
            ["git", "add", "."],
            check=True,
            capture_output=True,
            cwd=project_path,
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from speckitadv"],
            check=True,
            capture_output=True,
            cwd=project_path,
        )
        return True, None
    except subprocess.CalledProcessError as e:
        return False, str(e.stderr.decode() if e.stderr else e)
    except FileNotFoundError:
        return False, "git not found"


def create_project_structure(
    project_path: Path,
    agent: str,
    no_git: bool = False,
    force: bool = False,
) -> bool:
    """
    Create project structure with launchers.

    Args:
        project_path: Path to project directory
        agent: AI agent identifier
        no_git: Skip git initialization
        force: Overwrite existing files

    Returns:
        True if successful
    """
    agent_config = AGENT_CONFIG.get(agent)
    if not agent_config:
        console.print(f"[red]Error:[/red] Unknown agent '{agent}'")
        console.print(f"Available agents: {', '.join(get_all_agents())}")
        return False

    # Create project directory if needed
    project_path.mkdir(parents=True, exist_ok=True)

    # Get agent folder paths
    folder, subfolder = get_agent_commands_path(agent)
    commands_path = project_path / folder / subfolder
    commands_path.mkdir(parents=True, exist_ok=True)

    # Create memory directory with config.json
    memory_path = project_path / "memory"
    memory_path.mkdir(exist_ok=True)

    # Create config.json in memory/
    config_file = memory_path / "config.json"
    if not config_file.exists() or force:
        config_content = get_default_config()
        config_file.write_text(config_content, encoding="utf-8")

    # Write launcher files
    for command, description in WORKFLOW_COMMANDS:
        launcher_file = commands_path / f"speckitadv.{command}.md"
        if launcher_file.exists() and not force:
            console.print(f"[yellow]Skipping existing:[/yellow] {launcher_file.name}")
            continue
        content = get_launcher_content(command, description)
        launcher_file.write_text(content, encoding="utf-8")

    # Write AGENTS.md
    agents_file = project_path / "AGENTS.md"
    if not agents_file.exists() or force:
        agents_file.write_text(get_agents_md_content(), encoding="utf-8")

    # Create basic .gitignore
    gitignore_file = project_path / ".gitignore"
    if not gitignore_file.exists():
        gitignore_content = """# Spec Kit Smart
.analysis/
*.log

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
"""
        gitignore_file.write_text(gitignore_content, encoding="utf-8")

    # Initialize git if requested
    if not no_git:
        if is_git_repo(project_path):
            console.print("[cyan]Git repository already exists[/cyan]")
        elif check_tool("git"):
            success, error = init_git_repo(project_path)
            if success:
                console.print("[green]Git repository initialized[/green]")
            else:
                console.print(f"[yellow]Git init failed:[/yellow] {error}")
        else:
            console.print("[yellow]Git not found - skipping repository init[/yellow]")

    return True


def show_success_message(project_path: Path, agent: str, is_current_dir: bool = False) -> None:
    """Display success message with next steps."""
    agent_config = AGENT_CONFIG[agent]
    folder, subfolder = get_agent_commands_path(agent)

    # Build tree of created structure
    tree = Tree(f"[cyan]{project_path.name}/[/cyan]")
    agent_branch = tree.add(f"[cyan]{folder}/[/cyan]")
    cmd_branch = agent_branch.add(f"[cyan]{subfolder}/[/cyan]")
    for command, _ in WORKFLOW_COMMANDS:
        cmd_branch.add(f"speckitadv.{command}.md")
    memory_branch = tree.add("[cyan]memory/[/cyan]")
    memory_branch.add("config.json")
    tree.add("AGENTS.md")
    tree.add(".gitignore")

    console.print()
    console.print(Panel(tree, title="[bold green]Project Created[/bold green]", border_style="green"))

    # Next steps
    steps = []
    if not is_current_dir:
        steps.append(f"1. [cyan]cd {project_path.name}[/cyan]")
        start_num = 2
    else:
        start_num = 1

    steps.append(f"{start_num}. Start using slash commands with {agent_config['name']}:")
    steps.append(f"   {start_num}.1 [cyan]/speckitadv.constitution[/cyan] - Establish project principles")
    steps.append(f"   {start_num}.2 [cyan]/speckitadv.specify[/cyan] - Create baseline specification")
    steps.append(f"   {start_num}.3 [cyan]/speckitadv.plan[/cyan] - Create implementation plan")
    steps.append(f"   {start_num}.4 [cyan]/speckitadv.tasks[/cyan] - Generate actionable tasks")
    steps.append(f"   {start_num}.5 [cyan]/speckitadv.implement[/cyan] - Execute implementation")

    console.print()
    console.print(Panel("\n".join(steps), title="Next Steps", border_style="cyan"))

    # Optional commands
    optional = [
        "[cyan]/speckitadv.clarify[/cyan] - Ask structured questions (before plan)",
        "[cyan]/speckitadv.analyze[/cyan] - Cross-artifact consistency check",
        "[cyan]/speckitadv.checklist[/cyan] - Generate quality checklist",
        "[cyan]/speckitadv.analyze-project[/cyan] - Analyze existing project",
    ]
    console.print()
    console.print(Panel("\n".join(optional), title="Optional Commands", border_style="dim"))

    # Security notice
    if agent_config.get("requires_cli"):
        console.print()
        console.print(
            Panel(
                f"Consider adding [cyan]{folder}/[/cyan] to .gitignore if it may contain credentials.",
                title="[yellow]Security Note[/yellow]",
                border_style="yellow",
            )
        )
