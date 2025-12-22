"""
Constitution Command

Creates and manages project constitution with non-negotiable principles.
Implements a 3-stage workflow: initialize, collect, generate.

Uses embedded prompt assets and supports interactive mode.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text

from speckit.core.emit import emit_stage, emit_error
from speckit.core.prompts import get_prompt_fragment, render_prompt, get_stage_order
from speckit.core.state import ChainState

console = Console()


# Default principles - displayed to user before applying
DEFAULT_PRINCIPLES = [
    ("Good Engineering", "MUST follow SOLID, DRY, separation of concerns"),
    ("Lean & Simple", "MUST avoid over-engineering and unnecessary abstractions"),
    ("Readability First", "MUST prioritize code clarity over cleverness"),
    ("Self-Documenting", "MUST write code that explains itself through naming"),
    ("Intent Documentation", "MUST document WHY, not WHAT"),
    ("Test Behavior", "MUST write tests that verify behavior, not implementation"),
    ("Explicit Errors", "MUST handle errors explicitly, no silent failures"),
]


def _display_defaults() -> None:
    """Display default principles to user."""
    console.print("\n[bold cyan]Default Constitution Principles:[/bold cyan]\n")
    for name, desc in DEFAULT_PRINCIPLES:
        console.print(f"  [green]•[/green] [bold]{name}[/bold]: {desc}")
    console.print()


def _format_principles_for_prompt(principles: list[tuple[str, str]]) -> str:
    """Format principles list for prompt injection."""
    return "\n".join(f"- {name}: {desc}" for name, desc in principles)


def _interactive_collect() -> tuple[str, bool]:
    """
    Interactive mode: ask user for principles or use defaults.

    Returns:
        Tuple of (principles_text, used_defaults)
    """
    console.print("\n[bold]Constitution Setup[/bold]\n")
    console.print("A constitution defines non-negotiable principles for your project.")
    console.print("These principles guide all technical decisions and code reviews.\n")

    # Show defaults first
    _display_defaults()

    # Ask user preference
    use_defaults = Confirm.ask(
        "[bold]Use default principles?[/bold]",
        default=True,
    )

    if use_defaults:
        console.print("\n[dim]ℹ️  Using default principles. Run with --principles to customize later.[/dim]\n")
        return _format_principles_for_prompt(DEFAULT_PRINCIPLES), True

    # Custom principles mode
    console.print("\n[bold]Enter your principles[/bold] (one per line, format: 'Name: Description')")
    console.print("[dim]Press Enter twice when done, or Ctrl+C to cancel.[/dim]\n")

    lines = []
    while True:
        try:
            line = Prompt.ask("", default="")
            if not line:
                if lines:
                    break
                continue
            lines.append(line)
        except KeyboardInterrupt:
            console.print("\n[yellow]Cancelled. Using defaults.[/yellow]")
            return _format_principles_for_prompt(DEFAULT_PRINCIPLES), True

    if not lines:
        console.print("[yellow]No principles entered. Using defaults.[/yellow]")
        return _format_principles_for_prompt(DEFAULT_PRINCIPLES), True

    return "\n".join(f"- {line}" for line in lines), False


def run_constitution(
    stage: int = 1,
    principles: Optional[str] = None,
    defaults: bool = False,
    chain_id: Optional[str] = None,
) -> None:
    """
    Execute constitution workflow at specified stage.

    Stage 1: Initialize and verify AGENTS.md
    Stage 2: Collect principles (interactive or from args)
    Stage 3: Generate formal constitution document

    Args:
        stage: Current workflow stage (1-3)
        principles: User-provided principles text
        defaults: Use default principles (skip interactive)
        chain_id: Chain ID for state persistence
    """
    # Get ordered stages from embedded prompts
    stages = get_stage_order("constitution")

    if not stages:
        emit_error(
            "No fragments found",
            "No prompt fragments found for constitution command",
            recovery_cmd="speckitadv list-fragments constitution",
        )
        return

    total_stages = len(stages)

    # Validate stage
    if stage < 1 or stage > total_stages:
        emit_error(
            "Invalid stage",
            f"Stage must be between 1 and {total_stages}",
            recovery_cmd="speckitadv constitution --stage=1",
        )
        return

    # Get stage identifier
    stage_id = stages[stage - 1]

    # Initialize or load chain state
    if chain_id:
        try:
            state = ChainState.load(chain_id)
        except FileNotFoundError:
            emit_error(
                "Chain state not found",
                f"No state found for chain ID: {chain_id}",
                recovery_cmd="speckitadv constitution --stage=1",
            )
            return
        except ValueError as e:
            emit_error(
                "Chain ID mismatch",
                str(e),
                recovery_cmd="speckitadv constitution --stage=1",
            )
            return
    else:
        state = ChainState.initialize(Path.cwd())
        chain_id = state.chain_id

    # Build context
    context = {
        "chain_id": chain_id,
        "stage": stage,
        "total_stages": total_stages,
        "project_path": str(state.project_path or Path.cwd()),
        "principles": "",
        "used_defaults": False,
    }

    # Stage 2 special handling: collect principles
    if stage == 2:
        if principles:
            # Principles provided via CLI
            context["principles"] = principles
            context["used_defaults"] = False
        elif defaults:
            # Defaults explicitly requested
            _display_defaults()
            console.print("[dim]ℹ️  Applied default constitution principles.[/dim]\n")
            context["principles"] = _format_principles_for_prompt(DEFAULT_PRINCIPLES)
            context["used_defaults"] = True
        else:
            # Interactive mode - no args provided
            collected, used_defaults = _interactive_collect()
            context["principles"] = collected
            context["used_defaults"] = used_defaults

        if not context["principles"]:
            emit_error(
                "No principles provided",
                "Stage 2 requires principles",
                recovery_cmd="speckitadv constitution --stage=2 --defaults",
            )
            return

    # Load prompt fragment from embedded assets
    try:
        fragment = get_prompt_fragment("constitution", stage_id)
    except FileNotFoundError:
        emit_error(
            "Fragment not found",
            f"Prompt fragment not found: constitution/{stage_id}",
            recovery_cmd="speckitadv list-fragments constitution",
        )
        return

    # Render with context
    rendered = render_prompt(fragment, context)

    # Extract title from fragment
    title = _extract_title(rendered, stage_id)

    # Determine next command
    if stage < total_stages:
        next_cmd = f"speckitadv constitution --stage={stage + 1} --chain={chain_id}"
    else:
        next_cmd = None

    # Save state
    state.save(
        stage_name=stage_id,
        data={
            "stage": stage,
            "stage_id": stage_id,
            "command": "constitution",
            "principles": context.get("principles", ""),
            "used_defaults": context.get("used_defaults", False),
        },
    )

    # Emit stage output
    emit_stage(
        stage_num=stage,
        total_stages=total_stages,
        title=title,
        content=rendered,
        next_cmd=next_cmd or "Workflow complete - review memory/constitution.md",
        context={"chain_id": chain_id} if stage == 1 else None,
    )


def _extract_title(content: str, fallback: str) -> str:
    """Extract title from markdown content."""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    # Convert stage_id to title: "01-initialization" -> "Initialization"
    parts = fallback.split("-", 1)
    if len(parts) > 1:
        return parts[1].replace("-", " ").title()
    return fallback.title()


# Export for CLI
constitution = run_constitution
