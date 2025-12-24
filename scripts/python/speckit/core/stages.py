"""
Generic Stage Command Handler

Provides a generic handler for commands that use the fragment system.
Each command can use this to load and emit its staged prompts.

Feature-scoped commands (specify, plan, tasks, implement) use FeatureStateManager
from state module for simplified folder-based state management.

The folder path serves as the implicit chain ID - no abstract chain IDs needed.
"""

import json
from pathlib import Path
from typing import Optional

from rich.console import Console

from speckit.core.emit import emit_stage, emit_error, emit_complete
from speckit.core.prompts import (
    get_prompt_fragment,
    render_prompt,
    get_stage_order,
)
from speckit.core.state import FeatureStateManager, resolve_feature_folder

console = Console()


# Commands that use folder-based state management
FEATURE_SCOPED_COMMANDS = {"specify", "plan", "tasks", "implement", "clarify", "checklist"}

# Stage at which feature folder is expected to exist
# (stage 3 = branch-setup, when folder is created by create-feature command)
FEATURE_STATE_MIN_STAGE = 3


def run_staged_command(
    command: str,
    stage: Optional[int] = None,
    path: Optional[str] = None,
    feature_dir: Optional[str] = None,
    context: Optional[dict] = None,
) -> None:
    """
    Execute a staged command workflow.

    This generic handler loads the appropriate fragment for the current stage,
    renders it with context, and emits it for the AI agent.

    All staged commands use folder-based state management (FeatureStateManager).
    Stage and feature_dir are auto-detected from state when not provided.

    Args:
        command: Command name (e.g., "specify", "plan", "tasks", "implement")
        stage: Current stage number (1-indexed). If None, auto-detected from state.
        path: Optional project path (for early stages)
        feature_dir: Feature directory path. If None, auto-detected.
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

    # Try to auto-detect stage from state if not provided
    if stage is None:
        try:
            stage = _auto_detect_stage(command, feature_dir, stages)
        except json.JSONDecodeError as e:
            # State file is corrupted - show friendly error with recovery guidance
            # Use actual feature_dir in path when available, otherwise use placeholder
            state_path = f"specs/{feature_dir}/.state/state.json" if feature_dir else "specs/<feature-dir>/.state/state.json"
            emit_error(
                "Corrupted state file",
                f"Feature state file is corrupted: {e}",
                recovery_cmd=f"rm {state_path} && speckitadv {command} --stage=1",
            )
            return

    # Validate stage number
    if stage < 1 or stage > total_stages:
        emit_error(
            "Invalid stage",
            f"Stage {stage} is not valid. Command '{command}' has {total_stages} stages.",
            recovery_cmd=f"speckitadv {command} --stage=1",
        )
        return

    stage_id = stages[stage - 1]

    # For early stages (1-2), feature folder may not exist yet
    # Just emit the prompt without state tracking
    if stage < FEATURE_STATE_MIN_STAGE:
        render_context = {
            "stage": stage,
            "total_stages": total_stages,
            "command": command,
            "feature_dir": feature_dir or "",
            **(context or {}),
        }

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
        title = _extract_title(rendered, stage_id)

        # Next command for early stages (still need --stage since no state yet)
        if stage + 1 < FEATURE_STATE_MIN_STAGE:
            next_cmd = f"speckitadv {command} --stage={stage + 1}"
        else:
            # Stage 3+ will have state, so CLI can auto-detect - no args needed
            next_cmd = f"speckitadv {command}"

        emit_stage(
            stage_num=stage,
            total_stages=total_stages,
            title=title,
            content=rendered,
            next_cmd=next_cmd,
            context=render_context if stage == 1 else None,
        )
        return

    # For stage 3+, feature folder should exist
    # Try to resolve the feature folder
    try:
        specs_dir = Path("specs")
        feature_path = resolve_feature_folder(feature_dir, specs_dir)
    except FileNotFoundError:
        if feature_dir:
            # Explicit folder provided but doesn't exist
            emit_error(
                "Feature folder not found",
                f"Feature folder does not exist: {feature_dir}",
                recovery_cmd=f"speckitadv create-feature 'your feature description'",
            )
        else:
            # No folder specified and none found
            emit_error(
                "No feature folder found",
                "No feature folder found. Create one first or specify with --feature-dir",
                recovery_cmd=f"speckitadv create-feature 'your feature description'",
            )
        return

    # Check if explicitly provided folder exists before checking state
    # (resolve_feature_folder only throws for auto-detection, not explicit paths)
    if feature_dir and not feature_path.exists():
        emit_error(
            "Feature folder not found",
            f"Feature folder does not exist: {feature_path}",
            recovery_cmd=f"speckitadv create-feature 'your feature description'",
        )
        return

    # Load or create state manager
    state_manager = FeatureStateManager(feature_path)

    # Check if state exists
    if not state_manager.exists():
        emit_error(
            "State not initialized",
            f"Feature state not found in {feature_path}. Was create-feature run?",
            recovery_cmd=f"speckitadv create-feature 'your feature description'",
        )
        return

    # Load state and get context
    try:
        feature_state = state_manager.load()
        state_context = state_manager.get_prompt_context(command, stage_id)
    except FileNotFoundError as e:
        emit_error(
            "State file error",
            str(e),
            recovery_cmd=f"speckitadv create-feature 'your feature description'",
        )
        return

    # Build render context
    render_context = {
        "stage": stage,
        "total_stages": total_stages,
        "command": command,
        "feature_dir": str(feature_path),
        **state_context,
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
    title = _extract_title(rendered, stage_id)

    # Update state to mark prompt as in_progress
    state_manager.update_prompt(
        prompt=command,
        stage=stage_id,
        status="in_progress",
    )

    # Determine next command - no args needed, CLI reads from state
    if stage < total_stages:
        next_cmd = f"speckitadv {command}"
    else:
        next_cmd = None

    # Emit the stage prompt
    emit_stage(
        stage_num=stage,
        total_stages=total_stages,
        title=title,
        content=rendered,
        next_cmd=next_cmd,
    )

    # Check if this is the final stage
    if stage == total_stages:
        # Mark prompt as completed
        state_manager.update_prompt(
            prompt=command,
            stage=stage_id,
            status="completed",
        )

        emit_complete(
            message=f"{command.title()} workflow complete.",
            next_steps=_get_next_steps(command),
            artifacts=[str(feature_path)],
        )


def _auto_detect_stage(
    command: str,
    feature_dir: Optional[str],
    stages: list[str],
) -> int:
    """
    Auto-detect the next stage from state file.

    Returns:
        Stage number to run (1-indexed)
    """
    # Try to find feature folder
    try:
        specs_dir = Path("specs")
        feature_path = resolve_feature_folder(feature_dir, specs_dir)
    except FileNotFoundError:
        # No feature folder found - start at stage 1
        return 1

    # Try to load state
    state_manager = FeatureStateManager(feature_path)
    if not state_manager.exists():
        # No state file - start at stage 1
        return 1

    try:
        state = state_manager.load()
    except (AttributeError, KeyError):
        # Malformed state structure - start fresh
        return 1
    # Note: JSONDecodeError is NOT caught here - it bubbles up to
    # run_staged_command which shows a friendly error with recovery guidance

    # Get current stage for this command from state
    prompt_state = getattr(state, command, None)
    if prompt_state is None:
        return 1

    # If completed, we're done
    if prompt_state.status == "completed":
        return len(stages)  # Return last stage (will show completion)

    # If in_progress, find current stage index and continue
    if prompt_state.current_stage:
        try:
            current_idx = stages.index(prompt_state.current_stage)
            # Return next stage (current + 1, converted to 1-indexed)
            return min(current_idx + 2, len(stages))
        except ValueError:
            pass

    # If pending, start at stage 1 (workflow has not started yet)
    if prompt_state.status == "pending":
        return 1

    return 1


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
            "Review memory/constitution.md",
            "Run /speckitadv.specify to create feature specifications",
        ],
        "specify": [
            "Review spec.md for accuracy",
            "Run /speckitadv.clarify if clarifications remain",
            "Run /speckitadv.plan to create implementation plan",
        ],
        "clarify": [
            "Review updated spec",
            "Run /speckitadv.plan to create implementation plan",
        ],
        "plan": [
            "Review design artifacts",
            "Run /speckitadv.tasks to generate task breakdown",
        ],
        "tasks": [
            "Review tasks.md",
            "Run /speckitadv.implement to execute tasks",
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
        "analyze-project": [
            "Review analysis report",
            "Use insights for modernization planning",
        ],
    }
    return next_steps_map.get(command, ["Review output", "Continue to next command"])
