"""
Constitution Command

Creates and manages project constitution with non-negotiable principles.
Implements a 3-stage workflow: initialize, collect, generate.

Uses embedded prompt assets and supports interactive mode.

Note: Constitution uses file-existence check instead of chain state.
If constitution.md exists and has no placeholders, it's considered complete.
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
from speckit.core.state import check_constitution_complete

console = Console()


# Default principles - displayed to user before applying
# Matches original templates/commands/constitution.md from main branch
DEFAULT_PRINCIPLES = {
    "Engineering Principles": [
        ("Good Engineering", "MUST follow established software engineering principles (SOLID, DRY, separation of concerns)"),
        ("Lean & Simple", "MUST keep solutions lean - avoid over-engineering, unnecessary abstractions, or premature optimization"),
        ("Minimal Dependencies", "MUST minimize external dependencies - use standard libraries first, evaluate necessity before adding packages"),
    ],
    "Code Quality": [
        ("Readability First", "MUST prioritize code readability over cleverness - clear is better than concise"),
        ("Composition Over Inheritance", "SHOULD prefer composition patterns over deep inheritance hierarchies"),
        ("Code Reuse", "MUST check for existing methods before creating duplicates - refactor to enable reuse when needed"),
    ],
    "Documentation": [
        ("Self-Documenting Code", "MUST write code that explains itself through naming and structure"),
        ("Intent Documentation", "MUST document WHY (intent/rationale), not WHAT (implementation details)"),
        ("Selective Comments", "MUST document classes, important methods, and complex logic - MUST NOT document entities, DTOs, or trivial code"),
    ],
    "Testing & Quality": [
        ("Test Behavior", "MUST write tests that verify behavior, not implementation details"),
        ("Edge Case Coverage", "MUST consider all edge cases when writing tests, implementing features, or fixing bugs - test boundaries, null values, empty collections, and error conditions"),
        ("Explicit Error Handling", "MUST handle errors explicitly - no silent failures or swallowed exceptions"),
    ],
    "Build Quality": [
        ("Zero Warnings", "MUST resolve all build errors and warnings before commit - solutions should be free from compiler/linter warnings"),
        ("Warning-Free Code Generation", "MUST generate warning-free code from the start - anticipate and avoid patterns that cause warnings to minimize fix iterations"),
    ],
    "Versioning": [
        ("LTS Versions", "SHOULD default to latest LTS (Long-Term Support) versions for languages and frameworks when not specified"),
    ],
}


def _display_defaults() -> None:
    """Display default principles to user."""
    console.print("\n[bold cyan]Default Constitution Principles:[/bold cyan]\n")
    for category, principles in DEFAULT_PRINCIPLES.items():
        console.print(f"  [bold yellow]{category}:[/bold yellow]")
        for name, desc in principles:
            console.print(f"    [green][ok][/green] [bold]{name}[/bold] - {desc}")
        console.print()


def _format_principles_for_prompt(principles: dict[str, list[tuple[str, str]]] | list[tuple[str, str]]) -> str:
    """Format principles for prompt injection."""
    if isinstance(principles, dict):
        # Categorized principles (default format)
        lines = []
        for category, items in principles.items():
            lines.append(f"\n{category}:")
            for name, desc in items:
                lines.append(f"- {name}: {desc}")
        return "\n".join(lines)
    else:
        # Flat list of principles
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
        console.print("\n[dim][i] Using default principles. Run with --principles to customize later.[/dim]\n")
        return _format_principles_for_prompt(DEFAULT_PRINCIPLES), True

    # Custom principles mode
    console.print("\n[bold]Enter your principles[/bold] (one per line, format: 'Name: Description')")
    console.print("[dim]Enter a blank line when done, or Ctrl+C to cancel.[/dim]\n")

    lines = []
    blank_count = 0
    while True:
        try:
            line = Prompt.ask("", default="")
            if not line:
                blank_count += 1
                if lines:
                    # At least one principle entered, blank line ends input
                    break
                elif blank_count >= 2:
                    # Two consecutive blank lines with no input = use defaults
                    console.print("[yellow]No principles entered. Using defaults.[/yellow]")
                    return _format_principles_for_prompt(DEFAULT_PRINCIPLES), True
                continue
            blank_count = 0
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
    path: Optional[str] = None,
) -> None:
    """
    Execute constitution workflow at specified stage.

    Stage 1: Initialize and verify AGENTS.md
    Stage 2: Collect principles (interactive or from args)
    Stage 3: Generate formal constitution document

    Note: Constitution uses file-existence check instead of chain state.
    If constitution.md exists and has no placeholders, it's considered complete.

    Args:
        stage: Current workflow stage (1-3)
        principles: User-provided principles text
        defaults: Use default principles (skip interactive)
        path: Project path (defaults to current directory)
    """
    project_path = Path(path) if path else Path.cwd()

    # Check if constitution already exists and is complete
    is_complete, message = check_constitution_complete(project_path)
    if is_complete:
        console.print(f"[yellow]{message}[/yellow]")
        return

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

    # Build context (no chain_id needed)
    context = {
        "stage": stage,
        "total_stages": total_stages,
        "project_path": str(project_path),
        "principles": "",
        "source": "User input",  # Will be updated based on how principles are provided
    }

    # Stage 2 special handling: collect principles
    if stage == 2:
        if principles:
            # Principles provided via CLI
            context["principles"] = principles
            context["source"] = "User input (CLI)"
        elif defaults:
            # Defaults explicitly requested
            _display_defaults()
            console.print("[dim][i] Applied default constitution principles.[/dim]\n")
            context["principles"] = _format_principles_for_prompt(DEFAULT_PRINCIPLES)
            context["source"] = "Defaults (--defaults flag)"
        else:
            # Interactive mode - no args provided
            collected, used_defaults = _interactive_collect()
            context["principles"] = collected
            context["source"] = "Defaults (interactive)" if used_defaults else "User input (interactive)"

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

    # Determine next command (no chain_id needed)
    if stage < total_stages:
        if stage == 1:
            next_cmd = "speckitadv constitution --stage=2 --defaults  # or --principles='...'"
        else:
            next_cmd = f"speckitadv constitution --stage={stage + 1}"
    else:
        next_cmd = None

    # Emit stage output (no state saving needed - constitution uses file existence)
    emit_stage(
        stage_num=stage,
        total_stages=total_stages,
        title=title,
        content=rendered,
        next_cmd=next_cmd or "Workflow complete - Run /speckitadv.specify next",
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
