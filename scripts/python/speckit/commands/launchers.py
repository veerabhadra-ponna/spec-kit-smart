"""
Generate launcher files for AI agents.

Creates minimal launcher files that invoke the speckitadv CLI
for various AI agent platforms (Claude, Copilot, Cursor, etc.).
"""

from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()

# Commands and their descriptions
COMMANDS = {
    "analyze-project": "Analyze existing project for modernization",
    "analyze": "Cross-artifact consistency and quality analysis",
    "constitution": "Create project constitution with guiding principles",
    "specify": "Create baseline specification from requirements",
    "plan": "Create implementation plan from specification",
    "tasks": "Generate actionable tasks from plan",
    "implement": "Execute implementation with quality checks",
    "clarify": "Ask structured clarification questions",
    "checklist": "Generate quality validation checklist",
    "orchestrate": "Orchestrate complete spec-driven workflow",
    "resume": "Resume workflow from saved state",
    "generate-guidelines": "Generate corporate coding guidelines",
}

# Agent configurations with their destination paths
MARKDOWN_AGENTS = {
    "claude": ".claude/commands",
    "copilot": ".github/prompts",
    "cursor-agent": ".cursor/commands",
    "opencode": ".opencode/command",
    "codex": ".codex/commands",
    "windsurf": ".windsurf/workflows",
    "kilocode": ".kilocode/rules",
    "auggie": ".augment/rules",
    "roo": ".roo/rules",
    "codebuddy": ".codebuddy/commands",
    "q": ".amazonq/prompts",
    "amp": ".agents/commands",
}

TOML_AGENTS = {
    "gemini": ".gemini/commands",
    "qwen": ".qwen/commands",
}

ALL_AGENTS = {**MARKDOWN_AGENTS, **TOML_AGENTS}


def markdown_launcher(command: str, description: str) -> str:
    """Generate markdown launcher content."""
    return f"""---
description: {description}
---
Run: speckitadv {command} $ARGUMENTS
"""


def toml_launcher(command: str, description: str) -> str:
    """Generate TOML launcher content."""
    return f'''description = "{description}"
prompt = "Run: speckitadv {command} {{{{args}}}}"
'''


def generate_launchers(
    output_dir: Optional[Path] = None,
    agent: Optional[str] = None,
) -> int:
    """
    Generate launcher files for AI agents.

    Args:
        output_dir: Directory to output launcher files (default: ./launchers)
        agent: Specific agent to generate for, or None for all

    Returns:
        Total number of launcher files generated
    """
    base_dir = output_dir or Path.cwd() / "launchers"
    base_dir.mkdir(exist_ok=True)

    total = 0

    # Determine which agents to generate for
    if agent:
        if agent not in ALL_AGENTS:
            console.print(f"[red]Error:[/red] Unknown agent: {agent}")
            console.print(f"Available agents: {', '.join(sorted(ALL_AGENTS.keys()))}")
            return 0
        md_agents = {agent: MARKDOWN_AGENTS[agent]} if agent in MARKDOWN_AGENTS else {}
        toml_agents = {agent: TOML_AGENTS[agent]} if agent in TOML_AGENTS else {}
    else:
        md_agents = MARKDOWN_AGENTS
        toml_agents = TOML_AGENTS

    # Generate markdown launchers
    for agent_name, dest_path in md_agents.items():
        agent_dir = base_dir / agent_name
        agent_dir.mkdir(exist_ok=True)

        for command, description in COMMANDS.items():
            launcher_file = agent_dir / f"{command}.md"
            launcher_file.write_text(markdown_launcher(command, description))

        console.print(f"[green]✓[/green] Generated {len(COMMANDS)} launchers for {agent_name} → {dest_path}")
        total += len(COMMANDS)

    # Generate TOML launchers
    for agent_name, dest_path in toml_agents.items():
        agent_dir = base_dir / agent_name
        agent_dir.mkdir(exist_ok=True)

        for command, description in COMMANDS.items():
            launcher_file = agent_dir / f"{command}.toml"
            launcher_file.write_text(toml_launcher(command, description))

        console.print(f"[green]✓[/green] Generated {len(COMMANDS)} launchers for {agent_name} → {dest_path}")
        total += len(COMMANDS)

    return total


def run_generate_launchers(
    output_dir: Optional[str] = None,
    agent: Optional[str] = None,
    list_agents: bool = False,
) -> None:
    """
    CLI entry point for generate-launchers command.

    Args:
        output_dir: Directory to output launcher files
        agent: Specific agent to generate for
        list_agents: List available agents and exit
    """
    if list_agents:
        console.print("[bold]Available agents:[/bold]")
        console.print("\n[dim]Markdown format:[/dim]")
        for name, path in sorted(MARKDOWN_AGENTS.items()):
            console.print(f"  {name:15} → {path}")
        console.print("\n[dim]TOML format:[/dim]")
        for name, path in sorted(TOML_AGENTS.items()):
            console.print(f"  {name:15} → {path}")
        return

    out_path = Path(output_dir) if output_dir else None
    total = generate_launchers(output_dir=out_path, agent=agent)

    if total > 0:
        console.print(f"\n[bold green]Total: {total} launcher files generated[/bold green]")
