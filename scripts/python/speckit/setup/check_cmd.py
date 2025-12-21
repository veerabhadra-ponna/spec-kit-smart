"""
Tool checking command for speckitadv.

Checks for installed AI agent CLI tools and dependencies.
"""

import shutil
from pathlib import Path

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


def run_check() -> None:
    """Check all tools and display results."""
    tree = Tree("[cyan]Tool Check[/cyan]")

    # Check git
    git_branch = tree.add("Git")
    if check_tool("git"):
        git_branch.add("[green]●[/green] available")
    else:
        git_branch.add("[red]●[/red] not found")

    # Check AI agents
    agents_branch = tree.add("AI Agents")
    for agent_key, config in AGENT_CONFIG.items():
        agent_name = config["name"]
        requires_cli = config["requires_cli"]

        if requires_cli:
            if check_tool(agent_key):
                agents_branch.add(f"[green]●[/green] {agent_name}")
            else:
                agents_branch.add(f"[red]●[/red] {agent_name} [dim](not found)[/dim]")
        else:
            agents_branch.add(f"[yellow]○[/yellow] {agent_name} [dim](IDE-based)[/dim]")

    console.print(tree)
    console.print()
    console.print("[bold green]speckitadv is ready to use![/bold green]")
