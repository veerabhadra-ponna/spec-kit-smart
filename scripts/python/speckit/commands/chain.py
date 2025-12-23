"""
Chain state management for speckitadv.

Ports functionality from chain-state.sh.

State Location Strategy:
- analyze-project: .analysis/.state/
- constitution: memory/.state/
- specify, plan, tasks, implement: specs/{feature}/.state/
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console

from speckit.core.utils import find_repo_root, generate_chain_id
from speckit.core.state import FEATURE_SCOPED_COMMANDS

console = Console()


def get_state_dir(
    command: str = "analyze-project",
    repo_root: Optional[Path] = None,
    feature_dir: Optional[Path] = None,
) -> Path:
    """
    Get the state directory path based on command.

    Args:
        command: Command name for state location routing
        repo_root: Optional repository root
        feature_dir: Optional feature directory for feature-scoped commands

    Returns:
        Path to state directory
    """
    root = repo_root or find_repo_root()

    if command == "analyze-project":
        return root / ".analysis" / ".state"
    elif command == "constitution":
        return root / "memory" / ".state"
    elif command in FEATURE_SCOPED_COMMANDS:
        if feature_dir:
            return feature_dir / ".state"
        return root / "specs" / ".pending" / ".state"
    else:
        return root / ".analysis" / ".state"


def find_all_state_dirs(repo_root: Optional[Path] = None) -> list[Path]:
    """
    Find all state directories in the repository.

    Returns:
        List of existing state directories
    """
    root = repo_root or find_repo_root()
    state_dirs = []

    # Check standard locations
    standard_dirs = [
        root / ".analysis" / ".state",
        root / "memory" / ".state",
        root / "specs" / ".pending" / ".state",
    ]

    for d in standard_dirs:
        if d.exists():
            state_dirs.append(d)

    # Check feature directories
    specs_dir = root / "specs"
    if specs_dir.exists():
        for feature_dir in specs_dir.iterdir():
            if feature_dir.is_dir() and not feature_dir.name.startswith("."):
                state_dir = feature_dir / ".state"
                if state_dir.exists():
                    state_dirs.append(state_dir)

    return state_dirs


def init_state_dir(
    command: str = "analyze-project",
    repo_root: Optional[Path] = None,
) -> Path:
    """Initialize state directory for a command."""
    state_dir = get_state_dir(command, repo_root)
    state_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]✓[/green] Initialized state directory: {state_dir}")
    return state_dir


def validate_state(state: dict) -> bool:
    """Validate state schema - check required fields."""
    chain_id = state.get("chain_id")
    timestamp = state.get("timestamp")

    if not chain_id or not timestamp:
        console.print("[red]✗[/red] Invalid state: missing chain_id or timestamp")
        return False
    return True


def save_state(
    stage_name: str,
    state: dict,
    command: str = "analyze-project",
    repo_root: Optional[Path] = None,
) -> bool:
    """
    Save state to file.

    Args:
        stage_name: Stage identifier (e.g., '00-bootstrap', '01-init')
        state: State dictionary to save
        command: Command name for state location and file prefix
        repo_root: Optional repository root

    Returns:
        True if successful
    """
    if not validate_state(state):
        console.print("[red]✗[/red] State validation failed - cannot save")
        return False

    state_dir = get_state_dir(command, repo_root)
    state_dir.mkdir(parents=True, exist_ok=True)

    # Use command-prefixed filename
    file_stage_name = f"{command}-{stage_name}" if command else stage_name
    state_file = state_dir / f"{file_stage_name}.json"
    latest_file = state_dir / "latest.json"

    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

        with open(latest_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

        console.print(f"[green]✓[/green] State saved: {state_file}")
        return True
    except (OSError, IOError) as e:
        console.print(f"[red]✗[/red] Failed to save state: {e}")
        return False


def load_state(
    stage_name: str,
    command: str = "analyze-project",
    repo_root: Optional[Path] = None,
) -> Optional[dict]:
    """
    Load state from file.

    Args:
        stage_name: Stage identifier
        command: Command name for state location and file prefix
        repo_root: Optional repository root

    Returns:
        State dictionary or None if not found
    """
    state_dir = get_state_dir(command, repo_root)
    file_stage_name = f"{command}-{stage_name}" if command else stage_name
    state_file = state_dir / f"{file_stage_name}.json"

    if not state_file.exists():
        return None

    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, IOError, json.JSONDecodeError):
        return None


def load_latest_state(
    command: str = "",
    repo_root: Optional[Path] = None,
) -> Optional[dict]:
    """
    Load the latest state.

    If command is specified, searches that command's state dir first.
    Otherwise searches all state directories.
    """
    if command:
        state_dir = get_state_dir(command, repo_root)
        latest_file = state_dir / "latest.json"
        if latest_file.exists():
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, IOError, json.JSONDecodeError):
                pass

    # Search all state directories
    for state_dir in find_all_state_dirs(repo_root):
        latest_file = state_dir / "latest.json"
        if latest_file.exists():
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, IOError, json.JSONDecodeError):
                continue

    return None


def get_last_completed_stage(
    command: str = "",
    repo_root: Optional[Path] = None,
) -> str:
    """Get the last completed stage name."""
    if command:
        state_dir = get_state_dir(command, repo_root)
        state_dirs = [state_dir] if state_dir.exists() else []
    else:
        state_dirs = find_all_state_dirs(repo_root)

    if not state_dirs:
        return "none"

    # Find stage files matching pattern (with optional command prefix)
    stage_files = []
    for state_dir in state_dirs:
        for f in state_dir.glob("*.json"):
            # Match: command-NN-stage.json or NN-stage.json
            # Use [\w-]* to handle hyphenated commands like "analyze-project"
            if re.match(r"(?:[a-zA-Z][\w-]*-)?(\d{2}[ab]?-.*)\.json$", f.name) and f.name != "latest.json":
                stage_files.append(f.name)

    if not stage_files:
        return "none"

    # Sort and get last
    stage_files.sort(reverse=True)
    return stage_files[0].replace(".json", "")


def is_stage_complete(
    stage_name: str,
    command: str = "analyze-project",
    repo_root: Optional[Path] = None,
) -> bool:
    """Check if a stage is complete."""
    state_dir = get_state_dir(command, repo_root)
    file_stage_name = f"{command}-{stage_name}" if command else stage_name
    state_file = state_dir / f"{file_stage_name}.json"
    return state_file.exists()


def get_chain_id_from_state(
    command: str = "",
    repo_root: Optional[Path] = None,
) -> str:
    """Get chain ID from latest state."""
    state = load_latest_state(command, repo_root)
    if state:
        return state.get("chain_id", "unknown")
    return "unknown"


def create_initial_state(chain_id: str) -> dict:
    """Create initial state structure."""
    timestamp = datetime.now().isoformat()
    return {
        "chain_id": chain_id,
        "start_time": timestamp,
        "timestamp": timestamp,
        "stage": "initialization",
        "stages_complete": [],
        "current_stage": None,
    }


def merge_states(old_state: dict, new_fields: dict) -> dict:
    """Merge new fields into existing state."""
    result = old_state.copy()
    result.update(new_fields)
    return result


def mark_stage_complete(state: dict, stage_name: str) -> dict:
    """Add stage to completed list in state."""
    result = state.copy()
    stages_complete = result.get("stages_complete", [])
    if stage_name not in stages_complete:
        stages_complete.append(stage_name)
    result["stages_complete"] = stages_complete
    result["timestamp"] = datetime.now().isoformat()
    return result


def run_chain_state_command(
    command: str,
    stage: Optional[str] = None,
    state_json: Optional[str] = None,
    new_fields_json: Optional[str] = None,
) -> None:
    """
    Run chain state management command.

    Replaces chain-state.sh CLI functionality.
    """
    if command == "generate-id":
        print(generate_chain_id())

    elif command == "init":
        init_state_dir()

    elif command == "save":
        if not stage or not state_json:
            console.print("[red]Error:[/red] save requires stage and state_json")
            return
        try:
            state = json.loads(state_json)
            save_state(stage, state)
        except json.JSONDecodeError:
            console.print("[red]Error:[/red] Invalid JSON")

    elif command == "load":
        if not stage:
            console.print("[red]Error:[/red] load requires stage name")
            return
        state = load_state(stage)
        if state:
            print(json.dumps(state, indent=2))
        else:
            console.print("[red]Error:[/red] State not found", stderr=True)
            raise SystemExit(1)

    elif command == "load-latest":
        state = load_latest_state()
        if state:
            print(json.dumps(state, indent=2))
        else:
            console.print("[red]Error:[/red] No state found", stderr=True)
            raise SystemExit(1)

    elif command == "last-stage":
        print(get_last_completed_stage())

    elif command == "is-complete":
        if not stage:
            console.print("[red]Error:[/red] is-complete requires stage name")
            return
        print("true" if is_stage_complete(stage) else "false")

    elif command == "chain-id":
        print(get_chain_id_from_state())

    elif command == "init-state":
        if not stage:
            console.print("[red]Error:[/red] init-state requires chain_id")
            return
        state = create_initial_state(stage)  # stage is chain_id here
        print(json.dumps(state, indent=2))

    elif command == "validate":
        if not state_json:
            console.print("[red]Error:[/red] validate requires state_json")
            raise SystemExit(1)
        try:
            state = json.loads(state_json)
            if validate_state(state):
                console.print("[green]✓[/green] Valid state")
            else:
                console.print("[red]✗[/red] Invalid state")
                raise SystemExit(1)
        except json.JSONDecodeError:
            console.print("[red]Error:[/red] Invalid JSON")
            raise SystemExit(1)

    else:
        console.print(f"[red]Error:[/red] Unknown command: {command}")
        console.print("Commands: generate-id, init, save, load, load-latest, last-stage, is-complete, chain-id, init-state, validate")
