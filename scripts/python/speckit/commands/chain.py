"""
Chain state management for speckitadv.

Ports functionality from chain-state.sh.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console

from speckit.core.utils import find_repo_root, generate_chain_id

console = Console()


def get_state_dir(repo_root: Optional[Path] = None) -> Path:
    """Get the state directory path."""
    root = repo_root or find_repo_root()
    return root / ".analysis" / ".state"


def init_state_dir(repo_root: Optional[Path] = None) -> Path:
    """Initialize state directory."""
    state_dir = get_state_dir(repo_root)
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


def save_state(stage_name: str, state: dict, repo_root: Optional[Path] = None) -> bool:
    """
    Save state to file.

    Args:
        stage_name: Stage identifier (e.g., '00-bootstrap', '01-init')
        state: State dictionary to save
        repo_root: Optional repository root

    Returns:
        True if successful
    """
    if not validate_state(state):
        console.print("[red]✗[/red] State validation failed - cannot save")
        return False

    state_dir = get_state_dir(repo_root)
    state_dir.mkdir(parents=True, exist_ok=True)

    state_file = state_dir / f"{stage_name}.json"
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


def load_state(stage_name: str, repo_root: Optional[Path] = None) -> Optional[dict]:
    """
    Load state from file.

    Args:
        stage_name: Stage identifier
        repo_root: Optional repository root

    Returns:
        State dictionary or None if not found
    """
    state_dir = get_state_dir(repo_root)
    state_file = state_dir / f"{stage_name}.json"

    if not state_file.exists():
        return None

    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, IOError, json.JSONDecodeError):
        return None


def load_latest_state(repo_root: Optional[Path] = None) -> Optional[dict]:
    """Load the latest state."""
    state_dir = get_state_dir(repo_root)
    latest_file = state_dir / "latest.json"

    if not latest_file.exists():
        return None

    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, IOError, json.JSONDecodeError):
        return None


def get_last_completed_stage(repo_root: Optional[Path] = None) -> str:
    """Get the last completed stage name."""
    state_dir = get_state_dir(repo_root)

    if not state_dir.exists():
        return "none"

    import re

    # Find stage files matching pattern
    stage_files = []
    for f in state_dir.glob("*.json"):
        if re.match(r"\d{2}[ab]?-.*\.json", f.name):
            stage_files.append(f.name)

    if not stage_files:
        return "none"

    # Sort and get last
    stage_files.sort(reverse=True)
    return stage_files[0].replace(".json", "")


def is_stage_complete(stage_name: str, repo_root: Optional[Path] = None) -> bool:
    """Check if a stage is complete."""
    state_dir = get_state_dir(repo_root)
    state_file = state_dir / f"{stage_name}.json"
    return state_file.exists()


def get_chain_id_from_state(repo_root: Optional[Path] = None) -> str:
    """Get chain ID from latest state."""
    state = load_latest_state(repo_root)
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
            console.print("[yellow]State not found[/yellow]")

    elif command == "load-latest":
        state = load_latest_state()
        if state:
            print(json.dumps(state, indent=2))
        else:
            console.print("[yellow]No state found[/yellow]")

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
            return
        try:
            state = json.loads(state_json)
            if validate_state(state):
                console.print("[green]✓[/green] Valid state")
            else:
                console.print("[red]✗[/red] Invalid state")
        except json.JSONDecodeError:
            console.print("[red]Error:[/red] Invalid JSON")

    else:
        console.print(f"[red]Error:[/red] Unknown command: {command}")
        console.print("Commands: generate-id, init, save, load, load-latest, last-stage, is-complete, chain-id, init-state, validate")
