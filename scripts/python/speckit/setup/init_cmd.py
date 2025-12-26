"""
Project initialization command for speckitadv.

Creates project structure with embedded launchers - no network required.
"""

import json
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
    get_launcher_extension,
    get_launcher_format,
    get_agent_commands_path,
    get_all_agents,
)

console = Console()


# Agent-specific config file paths and formats
# Each agent has different settings file location and JSON structure for approve lists
AGENT_SETTINGS_CONFIG = {
    "claude": {
        "dir": ".claude",
        "file": "settings.local.json",
        "format": "claude",
        # Structure: {"permissions": {"allow": ["Bash(cmd:*)", "Skill(name)"]}}
    },
    "copilot": {
        "dir": ".vscode",
        "file": "settings.json",
        "format": "vscode",
        # Structure: {"chat.tools.terminal.autoApprove": {"cmd": true}}
    },
    "cursor-agent": {
        "dir": ".cursor",
        "file": "settings.json",
        "format": "cursor",
        # Structure: {"terminalCommands": {"allowedCommands": ["cmd"]}}
    },
    "windsurf": {
        "dir": ".windsurf",
        "file": "settings.json",
        "format": "windsurf",
        # Structure: {"cascade.allowedCommands": ["cmd"]}
    },
    "gemini": {
        "dir": ".gemini",
        "file": "settings.json",
        "format": "gemini",
        # Structure: {"allowedShellCommands": ["cmd"]}
    },
    "auggie": {
        "dir": ".augment",
        "file": "settings.json",
        "format": "auggie",
        # Structure: {"cli": {"approvedCommands": ["cmd"]}}
    },
    "roo": {
        "dir": ".roo",
        "file": "settings.json",
        "format": "roo",
        # Structure: {"terminal": {"autoApprove": ["cmd"]}}
    },
    "kilocode": {
        "dir": ".kilocode",
        "file": "settings.json",
        "format": "kilocode",
        # Structure: {"commands": {"approved": ["cmd"]}}
    },
    "q": {
        "dir": ".amazonq",
        "file": "settings.json",
        "format": "amazonq",
        # Structure: {"shell": {"approvedCommands": ["cmd"]}}
    },
}


def load_approve_list() -> list[str]:
    """Load shared approve patterns from approve-list.json."""
    approve_file = get_assets_base() / "templates" / "approve-list.json"
    if not approve_file.exists():
        console.print(f"[yellow]Warning: Approve list not found: {approve_file}[/yellow]")
        return []
    try:
        data = json.loads(approve_file.read_text(encoding="utf-8"))
        patterns = data.get("patterns", [])
        if not patterns:
            console.print(f"[yellow]Warning: No patterns found in {approve_file}[/yellow]")
        return patterns
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Failed to parse approve list: {e}[/red]")
        return []


def load_agent_specific_permissions(agent: str) -> list[str]:
    """Load agent-specific permissions from template file."""
    template_file = get_assets_base() / "templates" / f"{agent}-settings.json"
    if not template_file.exists():
        # Not an error - agent-specific templates are optional
        return []
    try:
        data = json.loads(template_file.read_text(encoding="utf-8"))
        # Claude format: permissions.allow
        if "permissions" in data and "allow" in data["permissions"]:
            return data["permissions"]["allow"]
        return []
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Failed to parse {agent} settings template: {e}[/red]")
        return []


def extract_command_names(patterns: list[str]) -> set[str]:
    """Extract unique command names from patterns for wildcard format.

    Examples:
        "git status" → "git"
        "git *" → "git"
        "docker-compose" → "docker-compose"
        "speckitadv" → "speckitadv"
    """
    commands = set()
    for pattern in patterns:
        if not pattern or pattern.strip() == "*":
            continue
        # Get first word (the command name)
        cmd = pattern.split()[0].rstrip("*").strip()
        if cmd:
            commands.add(cmd)
    return commands


def extract_existing_permissions(content: str, agent_format: str) -> list[str]:
    """Extract existing permissions from an agent config file.

    Args:
        content: JSON content of existing config file
        agent_format: The format identifier (claude, vscode, etc.)

    Returns:
        List of existing permission patterns
    """
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return []

    if agent_format == "claude":
        return data.get("permissions", {}).get("allow", [])
    elif agent_format == "vscode":
        return list(data.get("chat.tools.terminal.autoApprove", {}).keys())
    elif agent_format == "cursor":
        return data.get("terminalCommands", {}).get("allowedCommands", [])
    elif agent_format == "windsurf":
        return data.get("cascade.allowedCommands", [])
    elif agent_format == "gemini":
        return data.get("allowedShellCommands", [])
    elif agent_format == "auggie":
        return data.get("cli", {}).get("approvedCommands", [])
    elif agent_format == "roo":
        return data.get("terminal", {}).get("autoApprove", [])
    elif agent_format == "kilocode":
        return data.get("commands", {}).get("approved", [])
    elif agent_format == "amazonq":
        return data.get("shell", {}).get("approvedCommands", [])
    else:
        return data.get("approvedCommands", [])


def generate_agent_settings(
    agent_format: str,
    patterns: list[str],
    agent_permissions: list[str],
    existing_permissions: list[str] | None = None,
) -> str:
    """
    Generate agent-specific settings JSON with auto-approve patterns.

    Args:
        agent_format: The format identifier (claude, vscode, cursor, etc.)
        patterns: Shared approve patterns from approve-list.json
        agent_permissions: Agent-specific permissions (Skills, etc.)
        existing_permissions: Existing permissions to merge (preserve user customizations)

    Returns:
        JSON string with agent-specific structure
    """
    existing = existing_permissions or []

    if agent_format == "vscode":
        # VS Code Copilot: {"chat.tools.terminal.autoApprove": {"cmd": true}}
        # VS Code does NOT support wildcards - must use exact patterns
        all_patterns = list(set(patterns + existing))
        auto_approve = {pattern: True for pattern in sorted(all_patterns)}
        settings = {
            "chat.tools.terminal.autoApprove": auto_approve,
            "terminal.integrated.allowChords": False,
            "terminal.integrated.commandsToSkipShell": [],
        }

    elif agent_format == "claude":
        # Claude: {"permissions": {"allow": ["Bash(cmd:*)", "Skill(name)"]}}
        # Claude supports wildcards - use Bash(cmd:*) format for compact list
        all_permissions = list(agent_permissions)

        # Add existing permissions (preserve user customizations)
        for perm in existing:
            if perm not in all_permissions:
                all_permissions.append(perm)

        # Extract unique command names and add as Bash(cmd:*) wildcards
        commands = extract_command_names(patterns)
        for cmd in sorted(commands):
            bash_perm = f"Bash({cmd}:*)"
            if bash_perm not in all_permissions:
                all_permissions.append(bash_perm)

        settings = {"permissions": {"allow": all_permissions}}

    elif agent_format == "cursor":
        # Cursor: {"terminalCommands": {"allowedCommands": ["cmd"]}}
        all_patterns = list(set(patterns + existing))
        settings = {"terminalCommands": {"allowedCommands": sorted(all_patterns)}}

    elif agent_format == "windsurf":
        # Windsurf: {"cascade.allowedCommands": ["cmd"]}
        all_patterns = list(set(patterns + existing))
        settings = {"cascade.allowedCommands": sorted(all_patterns)}

    elif agent_format == "gemini":
        # Gemini: {"allowedShellCommands": ["cmd"]}
        all_patterns = list(set(patterns + existing))
        settings = {"allowedShellCommands": sorted(all_patterns)}

    elif agent_format == "auggie":
        # Auggie: {"cli": {"approvedCommands": ["cmd"]}}
        all_patterns = list(set(patterns + existing))
        settings = {"cli": {"approvedCommands": sorted(all_patterns)}}

    elif agent_format == "roo":
        # Roo: {"terminal": {"autoApprove": ["cmd"]}}
        all_patterns = list(set(patterns + existing))
        settings = {"terminal": {"autoApprove": sorted(all_patterns)}}

    elif agent_format == "kilocode":
        # Kilocode: {"commands": {"approved": ["cmd"]}}
        all_patterns = list(set(patterns + existing))
        settings = {"commands": {"approved": sorted(all_patterns)}}

    elif agent_format == "amazonq":
        # Amazon Q: {"shell": {"approvedCommands": ["cmd"]}}
        all_patterns = list(set(patterns + existing))
        settings = {"shell": {"approvedCommands": sorted(all_patterns)}}

    else:
        # Fallback: simple array format
        all_patterns = list(set(patterns + existing))
        settings = {"approvedCommands": sorted(all_patterns)}

    return json.dumps(settings, indent=2)


def create_agent_settings(project_path: Path, agent: str, force: bool = False) -> bool:
    """
    Create or update agent-specific settings file with auto-approve patterns.

    If file exists, merges new patterns with existing permissions (preserves user customizations).
    If file doesn't exist, creates new file with all patterns.

    Args:
        project_path: Path to project directory
        agent: AI agent identifier
        force: Overwrite existing files completely (don't merge)

    Returns:
        True if file was created/updated
    """
    config = AGENT_SETTINGS_CONFIG.get(agent)
    if not config:
        return False

    target_dir = project_path / config["dir"]
    target_file = target_dir / config["file"]

    # Load shared patterns from approve-list.json
    patterns = load_approve_list()

    # Load agent-specific permissions (e.g., Claude Skills)
    agent_permissions = load_agent_specific_permissions(agent)

    # Check for existing permissions to merge
    existing_permissions: list[str] = []
    if target_file.exists() and not force:
        try:
            existing_content = target_file.read_text(encoding="utf-8")
            existing_permissions = extract_existing_permissions(existing_content, config["format"])
            if existing_permissions:
                console.print(f"[cyan]Merging with existing {config['dir']}/{config['file']} ({len(existing_permissions)} patterns)[/cyan]")
        except (OSError, IOError) as e:
            console.print(f"[yellow]Warning: Could not read existing config: {e}[/yellow]")

    # Generate settings with agent-specific JSON structure (merging existing)
    content = generate_agent_settings(config["format"], patterns, agent_permissions, existing_permissions)

    # Write settings file
    target_dir.mkdir(exist_ok=True)
    target_file.write_text(content, encoding="utf-8")

    if existing_permissions:
        console.print(f"[green]Updated {config['dir']}/{config['file']} with merged auto-approve patterns[/green]")
    else:
        console.print(f"[green]Generated {config['dir']}/{config['file']} with auto-approve patterns[/green]")

    return True


# Gitignore rules for agent-specific settings directories
AGENT_GITIGNORE_RULES = {
    "claude": (".claude/*", "!.claude/settings.local.json"),
    "copilot": (".vscode/*", "!.vscode/settings.json"),
    "cursor-agent": (".cursor/*", "!.cursor/settings.json"),
    "windsurf": (".windsurf/*", "!.windsurf/settings.json"),
    "gemini": (".gemini/*", "!.gemini/settings.json"),
    "auggie": (".augment/*", "!.augment/settings.json"),
    "roo": (".roo/*", "!.roo/settings.json"),
    "kilocode": (".kilocode/*", "!.kilocode/settings.json"),
    "q": (".amazonq/*", "!.amazonq/settings.json"),
}


def ensure_gitignore_rules(project_path: Path, agent: str) -> bool:
    """
    Ensure agent-specific gitignore rules exist in .gitignore.

    If .gitignore exists but lacks the rules, appends them.
    Does nothing if .gitignore doesn't exist (will be created with full content elsewhere).

    Args:
        project_path: Path to project directory
        agent: AI agent identifier

    Returns:
        True if rules were added
    """
    gitignore_file = project_path / ".gitignore"
    rules = AGENT_GITIGNORE_RULES.get(agent)

    if not rules or not gitignore_file.exists():
        return False

    try:
        current = gitignore_file.read_text(encoding="utf-8")
    except (OSError, IOError):
        return False

    # Check which rules are missing
    missing_rules = [r for r in rules if r not in current]

    if not missing_rules:
        return False

    # Append missing rules
    addition = f"\n# {agent.title()} agent settings\n" + "\n".join(missing_rules) + "\n"
    new_content = current.rstrip() + "\n" + addition
    gitignore_file.write_text(new_content, encoding="utf-8")
    console.print(f"[yellow]Updated .gitignore with {agent} rules[/yellow]")
    return True


def get_default_config() -> str:
    """Get default config.json content from embedded assets or fallback."""
    base = get_assets_base()
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
    "enableCheckArtifactory": false
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


def get_assets_base() -> Path:
    """Get the base path for embedded assets."""
    if getattr(sys, "frozen", False):
        # PyInstaller binary
        return Path(sys._MEIPASS) / "assets"  # type: ignore
    else:
        # Development or pip install
        return Path(__file__).parent.parent / "assets"


def get_guidelines_path() -> Optional[Path]:
    """Get path to embedded guidelines folder."""
    base = get_assets_base()
    guidelines = base / "guidelines"
    if guidelines.exists() and guidelines.is_dir():
        return guidelines
    return None


def get_agents_md_content() -> str:
    """Get AGENTS.md content from embedded assets."""
    base = get_assets_base()

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

    # Write launcher files with correct format for agent
    launcher_ext = get_launcher_extension(agent)
    launcher_format = get_launcher_format(agent)

    for command, description in WORKFLOW_COMMANDS:
        launcher_file = commands_path / f"speckitadv.{command}{launcher_ext}"
        if launcher_file.exists() and not force:
            console.print(f"[yellow]Skipping existing:[/yellow] {launcher_file.name}")
            continue
        content = get_launcher_content(command, description, launcher_format)
        launcher_file.write_text(content, encoding="utf-8")

    # Write AGENTS.md
    agents_file = project_path / "AGENTS.md"
    if not agents_file.exists() or force:
        agents_file.write_text(get_agents_md_content(), encoding="utf-8")

    # Copy .guidelines folder (baseline guidelines for generate-guidelines command)
    guidelines_dest = project_path / ".guidelines"
    guidelines_src = get_guidelines_path()
    if guidelines_src and (not guidelines_dest.exists() or force):
        if guidelines_dest.exists():
            shutil.rmtree(guidelines_dest)
        shutil.copytree(guidelines_src, guidelines_dest)
        console.print("[green]Copied .guidelines/ baseline[/green]")

    # Generate agent-specific settings with auto-approve patterns
    # This dynamically creates settings from approve-list.json + agent-specific permissions
    create_agent_settings(project_path, agent, force)

    # Also create VS Code settings for copilot compatibility (if not already the agent)
    if agent != "copilot":
        create_agent_settings(project_path, "copilot", force)

    # Create or update .gitignore
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
*.swp

# Agent settings (ignore all except approved settings files)
.vscode/*
!.vscode/settings.json
.claude/*
!.claude/settings.local.json
.cursor/*
!.cursor/settings.json
.windsurf/*
!.windsurf/settings.json
.gemini/*
!.gemini/settings.json
.augment/*
!.augment/settings.json
.roo/*
!.roo/settings.json
.kilocode/*
!.kilocode/settings.json
.amazonq/*
!.amazonq/settings.json
"""
        gitignore_file.write_text(gitignore_content, encoding="utf-8")
    else:
        # .gitignore exists - ensure agent-specific rules are present
        ensure_gitignore_rules(project_path, agent)
        if agent != "copilot":
            ensure_gitignore_rules(project_path, "copilot")

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
    launcher_ext = get_launcher_extension(agent)

    # Build tree of created structure
    tree = Tree(f"[cyan]{project_path.name}/[/cyan]")
    agent_branch = tree.add(f"[cyan]{folder}/[/cyan]")
    cmd_branch = agent_branch.add(f"[cyan]{subfolder}/[/cyan]")
    for command, _ in WORKFLOW_COMMANDS:
        cmd_branch.add(f"speckitadv.{command}{launcher_ext}")
    guidelines_branch = tree.add("[cyan].guidelines/[/cyan]")
    guidelines_branch.add("base/")
    guidelines_branch.add("profiles/")
    guidelines_branch.add("stack-mapping.json")
    memory_branch = tree.add("[cyan]memory/[/cyan]")
    memory_branch.add("config.json")
    # Show agent-specific settings folder (if configured)
    agent_settings = AGENT_SETTINGS_CONFIG.get(agent)
    if agent_settings:
        settings_branch = tree.add(f"[cyan]{agent_settings['dir']}/[/cyan]")
        settings_branch.add(agent_settings['file'])
    vscode_branch = tree.add("[cyan].vscode/[/cyan]")
    vscode_branch.add("settings.json")
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
