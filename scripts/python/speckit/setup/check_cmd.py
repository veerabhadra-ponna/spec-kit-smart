"""
Tool checking command for speckitadv.

Checks for installed AI agent CLI tools and dependencies.
Also provides feature directory discovery (replaces check-prerequisites.sh).
"""

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.tree import Tree

from speckit.setup.config import AGENT_CONFIG

console = Console()


def check_tool(tool: str) -> bool:
    """Check if a CLI tool is installed."""
    # Special handling for Claude CLI local path
    if tool == "claude":
        claude_local = Path.home() / ".claude" / "local" / "claude"
        if claude_local.exists():
            return True
    return shutil.which(tool) is not None


def find_repo_root(start_path: Optional[Path] = None) -> Path:
    """Find repository root by searching for .git or memory directory."""
    current = (start_path or Path.cwd()).resolve()
    while current != current.parent:
        if (current / ".git").exists() or (current / "memory").exists():
            return current
        current = current.parent
    return Path.cwd()


def get_current_branch() -> str:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def find_feature_dir(repo_root: Path) -> Optional[Path]:
    """Find current feature directory from branch or latest specs."""
    branch = get_current_branch()

    # Try to match branch to feature directory
    if branch:
        # Extract feature part from branch name (e.g., "feature/001-user-auth" -> "001-user-auth")
        branch_name = branch.split("/")[-1]
        specs_dir = repo_root / "specs"
        if specs_dir.exists():
            feature_path = specs_dir / branch_name
            if feature_path.exists():
                return feature_path

    # Fallback: find latest feature directory by number
    specs_dir = repo_root / "specs"
    if specs_dir.exists():
        highest = 0
        latest = None
        for item in specs_dir.iterdir():
            if item.is_dir():
                match = re.match(r"^(\d{3})-", item.name)
                if match:
                    num = int(match.group(1))
                    if num > highest:
                        highest = num
                        latest = item
        return latest

    return None


def get_available_docs(feature_dir: Path) -> list:
    """List available documentation files in feature directory."""
    docs = []
    doc_files = [
        ("spec.md", "Specification"),
        ("plan.md", "Implementation Plan"),
        ("tasks.md", "Task List"),
        ("research.md", "Research Notes"),
        ("data-model.md", "Data Model"),
        ("quickstart.md", "Quickstart Guide"),
    ]
    for filename, description in doc_files:
        if (feature_dir / filename).exists():
            docs.append({"file": filename, "description": description, "path": str(feature_dir / filename)})
    return docs


def run_check(
    output_json: bool = False,
    paths_only: bool = False,
    require_tasks: bool = False,
    include_tasks: bool = False,
) -> tuple[dict, bool]:
    """
    Check tools and find feature paths.

    Args:
        output_json: Output results in JSON format
        paths_only: Only output paths (no tool checks)
        require_tasks: Require tasks.md to exist
        include_tasks: Include tasks content in output

    Returns:
        Tuple of (results dict, success bool)
    """
    repo_root = find_repo_root()
    feature_dir = find_feature_dir(repo_root)
    branch = get_current_branch()

    result = {
        "REPO_ROOT": str(repo_root),
        "CURRENT_BRANCH": branch,
        "HAS_GIT": check_tool("git"),
    }

    if feature_dir:
        result["FEATURE_DIR"] = str(feature_dir)
        result["FEATURE_SPEC"] = str(feature_dir / "spec.md")
        result["IMPL_PLAN"] = str(feature_dir / "plan.md")
        result["TASKS"] = str(feature_dir / "tasks.md")
        result["AVAILABLE_DOCS"] = get_available_docs(feature_dir)

        if require_tasks and not (feature_dir / "tasks.md").exists():
            result["ERROR"] = "tasks.md not found but required"
            if output_json:
                print(json.dumps(result, indent=2))
            else:
                console.print(f"[red]Error:[/red] tasks.md not found in {feature_dir}")
            return result, False  # Return failure

        if include_tasks and (feature_dir / "tasks.md").exists():
            result["TASKS_CONTENT"] = (feature_dir / "tasks.md").read_text(encoding="utf-8")

    if output_json:
        print(json.dumps(result, indent=2))
        return result, True

    if paths_only:
        for key, value in result.items():
            if key not in ("AVAILABLE_DOCS", "TASKS_CONTENT", "HAS_GIT"):
                print(f"{key}={value}")
        return result, True

    # Rich formatted output
    tree = Tree("[cyan]Tool Check[/cyan]")

    # Check git
    git_branch = tree.add("Git")
    if check_tool("git"):
        git_branch.add("[green]●[/green] available")
        if branch:
            git_branch.add(f"[dim]branch: {branch}[/dim]")
    else:
        git_branch.add("[red]●[/red] not found")

    # Check AI agents
    agents_branch = tree.add("AI Agents")
    for agent_key, config in AGENT_CONFIG.items():
        agent_name = config["name"]
        requires_cli = config.get("requires_cli", False)

        if requires_cli:
            if check_tool(agent_key):
                agents_branch.add(f"[green]●[/green] {agent_name}")
            else:
                agents_branch.add(f"[red]●[/red] {agent_name} [dim](not found)[/dim]")
        else:
            agents_branch.add(f"[yellow]○[/yellow] {agent_name} [dim](IDE-based)[/dim]")

    # Show feature context
    if feature_dir:
        context_branch = tree.add("Feature Context")
        context_branch.add(f"[cyan]{feature_dir.name}[/cyan]")
        for doc in result.get("AVAILABLE_DOCS", []):
            context_branch.add(f"[green]●[/green] {doc['file']}")

    console.print(tree)
    console.print()
    console.print("[bold green]speckitadv is ready to use![/bold green]")

    return result, True
