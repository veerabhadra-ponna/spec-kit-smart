"""
Generic Stage Command Handler

Provides a generic handler for commands that use the fragment system.
Each command can use this to load and emit its staged prompts.
"""

from pathlib import Path
from typing import Optional

from speckit.core.emit import emit_stage, emit_error, emit_complete
from speckit.core.prompts import (
    get_prompt_fragment,
    render_prompt,
    get_stage_order,
    fragment_exists,
)
from speckit.core.state import ChainState


def run_staged_command(
    command: str,
    stage: int = 1,
    chain_id: Optional[str] = None,
    path: Optional[str] = None,
    context: Optional[dict] = None,
) -> None:
    """
    Execute a staged command workflow.

    This generic handler loads the appropriate fragment for the current stage,
    renders it with context, and emits it for the AI agent.

    Args:
        command: Command name (e.g., "constitution", "specify", "plan")
        stage: Current stage number (1-indexed)
        chain_id: Optional chain ID for state persistence
        path: Optional project path
        context: Optional additional context variables
    """
    # Get ordered list of stages for this command
    stages = get_stage_order(command)

    if not stages:
        emit_error(
            "No fragments found",
            f"No prompt fragments found for command: {command}",
            recovery_cmd=f"speckitadv list-fragments {command}",
        )
        return

    total_stages = len(stages)

    # Validate stage number
    if stage < 1 or stage > total_stages:
        emit_error(
            "Invalid stage",
            f"Stage {stage} is not valid. Command '{command}' has {total_stages} stages.",
            recovery_cmd=f"speckitadv {command} --stage=1",
        )
        return

    # Get the stage identifier (e.g., "01-initialization")
    stage_id = stages[stage - 1]

    # Initialize or load chain state
    if chain_id:
        try:
            state = ChainState.load(chain_id)
        except FileNotFoundError:
            emit_error(
                "Chain state not found",
                f"No state found for chain ID: {chain_id}",
                recovery_cmd=f"speckitadv {command} --stage=1 --path={path or '.'}",
            )
            return
    else:
        # New workflow - initialize state
        project_path = Path(path) if path else Path.cwd()
        state = ChainState.initialize(project_path)
        chain_id = state.chain_id

    # Build render context
    render_context = {
        "chain_id": chain_id,
        "stage": stage,
        "total_stages": total_stages,
        "project_path": str(state.project_path or Path.cwd()),
        "command": command,
        **(context or {}),
    }

    # Load and render the fragment
    try:
        fragment = get_prompt_fragment(command, stage_id)
    except FileNotFoundError:
        emit_error(
            "Fragment not found",
            f"Prompt fragment not found: {command}/{stage_id}",
            recovery_cmd=f"speckitadv list-fragments {command}",
        )
        return

    rendered = render_prompt(fragment, render_context)

    # Extract title from fragment (first # heading)
    title = _extract_title(rendered, stage_id)

    # Determine next command
    if stage < total_stages:
        next_cmd = f"speckitadv {command} --stage={stage + 1} --chain={chain_id}"
    else:
        next_cmd = None

    # Save state for this stage
    state.save(
        stage_name=stage_id,
        data={
            "stage": stage,
            "stage_id": stage_id,
            "command": command,
        },
    )

    # Check if this is the final stage
    if stage == total_stages:
        emit_complete(
            message=f"{command.title()} workflow complete.",
            next_steps=_get_next_steps(command),
            artifacts=[str(state.project_path / ".analysis" if state.project_path else ".")],
        )
    else:
        emit_stage(
            stage_num=stage,
            total_stages=total_stages,
            title=title,
            content=rendered,
            next_cmd=next_cmd,
            context=render_context if stage == 1 else None,
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


def _get_next_steps(command: str) -> list[str]:
    """Get suggested next steps for a command."""
    next_steps_map = {
        "constitution": [
            "Review constitution.md",
            "Run /specify to create feature specifications",
        ],
        "specify": [
            "Review spec.md for accuracy",
            "Run /clarify if clarifications remain",
            "Run /plan to create implementation plan",
        ],
        "clarify": [
            "Review updated spec",
            "Run /plan to create implementation plan",
        ],
        "plan": [
            "Review design artifacts",
            "Run /tasks to generate task breakdown",
        ],
        "tasks": [
            "Review tasks.md",
            "Run /implement to execute tasks",
        ],
        "implement": [
            "Review code changes",
            "Run full test suite",
            "Create pull request",
        ],
        "checklist": [
            "Review checklist items",
            "Complete checklist before implementation",
        ],
    }
    return next_steps_map.get(command, ["Review output", "Continue to next command"])
