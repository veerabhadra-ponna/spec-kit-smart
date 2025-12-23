"""
Generic Stage Command Handler

Provides a generic handler for commands that use the fragment system.
Each command can use this to load and emit its staged prompts.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from rich.console import Console

from speckit.core.emit import emit_stage, emit_error, emit_complete
from speckit.core.prompts import (
    get_prompt_fragment,
    render_prompt,
    get_stage_order,
    fragment_exists,
)
from speckit.core.state import ChainState, FEATURE_SCOPED_COMMANDS, FEATURE_STATE_MIN_STAGE

import json

console = Console()


@dataclass
class ChainMatch:
    """Result of chain auto-detection."""

    chain_id: str
    source: str  # Description of where it was found
    total_matches: int  # How many matching chains were found


def _find_existing_chain_for_command(
    command: str,
    feature_dir: Optional[Path] = None,
    workspace_root: Optional[Path] = None,
) -> Optional[ChainMatch]:
    """
    Find an existing chain_id for a command without requiring --chain flag.

    This enables deterministic chain resumption for stage 4+ when the AI
    doesn't pass --chain explicitly.

    Search order:
    1. Feature directory state (if --feature-dir provided)
    2. Pending state directory
    3. Any feature directory with matching command state

    Args:
        command: Command name (specify, plan, etc.)
        feature_dir: Optional feature directory to check first
        workspace_root: Optional workspace root

    Returns:
        ChainMatch with chain_id, source, and total matches count; None if not found
    """
    root = workspace_root or Path.cwd()
    specs_dir = root / "specs"
    all_matches: list[tuple[str, str]] = []  # (chain_id, source)

    # 1. Check provided feature directory first
    if feature_dir:
        state_file = feature_dir / ".state" / "latest.json"
        if state_file.exists():
            try:
                data = json.loads(state_file.read_text())
                if data.get("command") == command:
                    chain_id = data.get("chain_id")
                    if chain_id:
                        # When feature_dir is explicitly provided, return immediately
                        # (no ambiguity - user specified the feature)
                        return ChainMatch(
                            chain_id=chain_id,
                            source=feature_dir.name,
                            total_matches=1,
                        )
            except (json.JSONDecodeError, OSError):
                pass

    if not specs_dir.exists():
        return None

    # 2. Scan feature directories FIRST for matching command state
    # Feature directories represent properly migrated state and should take precedence
    for subdir in sorted(specs_dir.iterdir(), reverse=True):  # Most recent first
        if subdir.is_dir() and not subdir.name.startswith("."):
            state_file = subdir / ".state" / "latest.json"
            if state_file.exists():
                try:
                    data = json.loads(state_file.read_text())
                    if data.get("command") == command:
                        chain_id = data.get("chain_id")
                        if chain_id:
                            all_matches.append((chain_id, subdir.name))
                except (json.JSONDecodeError, OSError):
                    continue

    # 3. Check pending state only if NO feature directories matched
    # This prevents stale pending state from abandoned workflows taking precedence
    if not all_matches:
        pending_state = specs_dir / ".pending" / ".state" / "latest.json"
        if pending_state.exists():
            try:
                data = json.loads(pending_state.read_text())
                if data.get("command") == command:
                    chain_id = data.get("chain_id")
                    if chain_id:
                        all_matches.append((chain_id, ".pending"))
            except (json.JSONDecodeError, OSError):
                pass

    if not all_matches:
        return None

    # Return the first match (most recent by sorted order) with total count
    first_chain_id, first_source = all_matches[0]
    return ChainMatch(
        chain_id=first_chain_id,
        source=first_source,
        total_matches=len(all_matches),
    )


def _detect_feature_dir_for_chain(chain_id: str, workspace_root: Optional[Path] = None) -> Optional[Path]:
    """
    Auto-detect feature directory by scanning specs/ for state files with matching chain_id,
    or by matching the current git branch to a feature directory.

    This handles the case where stage 3 created the folder but --feature-dir wasn't passed.
    """
    from speckit.setup.check_cmd import find_feature_dir

    root = workspace_root or Path.cwd()
    specs_dir = root / "specs"
    if not specs_dir.exists():
        return None

    # Check pending state for stored feature_dir
    pending_state = specs_dir / ".pending" / ".state" / "latest.json"
    if pending_state.exists():
        try:
            data = json.loads(pending_state.read_text())
            if data.get("chain_id") == chain_id and data.get("feature_dir"):
                feature_path = Path(data["feature_dir"])
                if feature_path.exists():
                    return feature_path
        except (json.JSONDecodeError, OSError):
            pass

    # Scan feature directories for matching chain_id in state
    for subdir in sorted(specs_dir.iterdir(), reverse=True):  # Most recent first by name
        if subdir.is_dir() and not subdir.name.startswith("."):
            state_file = subdir / ".state" / "latest.json"
            if state_file.exists():
                try:
                    data = json.loads(state_file.read_text())
                    if data.get("chain_id") == chain_id:
                        return subdir
                except (json.JSONDecodeError, OSError):
                    continue

    # Fallback: use git branch name to find matching feature directory
    # This is safer than mtime as it uses explicit naming convention
    return find_feature_dir(root)


def run_staged_command(
    command: str,
    stage: int = 1,
    chain_id: Optional[str] = None,
    path: Optional[str] = None,
    feature_dir: Optional[str] = None,
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
        feature_dir: Optional feature directory path (for feature-scoped commands stage 3+)
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

    # Convert feature_dir to Path if provided
    feature_dir_path = Path(feature_dir) if feature_dir else None

    # For feature-scoped commands at stage 4+, auto-resume chain if not explicitly provided
    # This ensures deterministic behavior even if AI doesn't pass --chain
    if not chain_id and command in FEATURE_SCOPED_COMMANDS and stage >= FEATURE_STATE_MIN_STAGE + 1:
        chain_match = _find_existing_chain_for_command(command, feature_dir_path)
        if chain_match:
            chain_id = chain_match.chain_id
            # Warn if multiple matching chains found (ambiguous selection)
            if chain_match.total_matches > 1:
                console.print(
                    f"[yellow]⚠ Multiple {command} chains found ({chain_match.total_matches}). "
                    f"Auto-resuming: {chain_match.chain_id} from {chain_match.source}[/yellow]"
                )
                console.print(
                    f"[dim]  Use --chain=<id> or --feature-dir to specify explicitly.[/dim]"
                )

    # Initialize or load chain state
    if chain_id:
        try:
            state = ChainState.load(chain_id, command=command, feature_dir=feature_dir_path)
        except FileNotFoundError:
            emit_error(
                "Chain state not found",
                f"No state found for chain ID: {chain_id}",
                recovery_cmd=f"speckitadv {command} --stage=1 --path={path or '.'}",
            )
            return
        except ValueError as e:
            emit_error(
                "Chain ID mismatch",
                str(e),
                recovery_cmd=f"speckitadv {command} --stage=1 --path={path or '.'}",
            )
            return
    else:
        # New workflow - initialize state
        project_path = Path(path) if path else Path.cwd()
        state = ChainState.initialize(project_path, command=command, feature_dir=feature_dir_path)
        chain_id = state.chain_id

    # Update feature directory if provided (for stage 3+ of feature-scoped commands)
    if feature_dir_path and command in FEATURE_SCOPED_COMMANDS:
        state.set_feature_dir(feature_dir_path)
    elif command in FEATURE_SCOPED_COMMANDS:
        # Auto-detect feature directory by scanning specs/ for matching chain_id
        # This handles the case where stage 3 created the folder but --feature-dir wasn't passed
        # NOTE: For specify, skip auto-detect at stage 3 - the folder is created BY that stage
        # For other commands (plan, tasks, implement), the feature folder should already exist
        # from a prior specify workflow, so allow auto-detect at any stage
        should_auto_detect = command != "specify" or stage > FEATURE_STATE_MIN_STAGE
        if should_auto_detect:
            detected_dir = _detect_feature_dir_for_chain(state.chain_id)
            if detected_dir:
                state.set_feature_dir(detected_dir)
                feature_dir_path = detected_dir

    # Build render context
    render_context = {
        "chain_id": chain_id,
        "stage": stage,
        "total_stages": total_stages,
        "project_path": str(state.project_path or Path.cwd()),
        "command": command,
        "feature_dir": str(feature_dir_path) if feature_dir_path else (str(state.feature_dir) if state.feature_dir else ""),
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
        next_stage = stage + 1
        # For feature-scoped commands, don't include --chain until state is persisted
        # State is only persisted from stage 3+ (after feature folder exists)
        # So stages 1 and 2 don't output --chain (state not saved yet)
        if command in FEATURE_SCOPED_COMMANDS and stage < FEATURE_STATE_MIN_STAGE:
            next_cmd = f"speckitadv {command} --stage={next_stage}"
        else:
            next_cmd = f"speckitadv {command} --stage={next_stage} --chain={chain_id}"
            # Include --feature-dir for feature-scoped commands when we have a feature directory
            if command in FEATURE_SCOPED_COMMANDS and feature_dir_path:
                next_cmd += f" --feature-dir={feature_dir_path}"
    else:
        next_cmd = None

    # Save state for this stage (may be skipped for early stages of feature commands)
    state.save(
        stage_name=stage_id,
        data={
            "stage": stage,
            "stage_id": stage_id,
            "command": command,
        },
        stage_num=stage,
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
    }
    return next_steps_map.get(command, ["Review output", "Continue to next command"])
