"""
Chain State Management

Manages persistent state across workflow stages.
Enables session recovery and progress tracking.

State Location Strategy:
- analyze-project: .analysis/.state/
- constitution: memory/.state/
- specify, plan, tasks, implement: specs/{feature}/.state/
  (only persists from stage 3+ after feature folder exists)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field

from speckit.core.utils import generate_chain_id


# Commands that use feature-scoped state (specs/{feature}/.state/)
FEATURE_SCOPED_COMMANDS = {"specify", "plan", "tasks", "implement"}

# Minimum stage for feature-scoped commands to persist state
# (stage 3 = branch-setup, when feature folder is created)
FEATURE_STATE_MIN_STAGE = 3


class StateSchema(BaseModel):
    """Schema for chain state validation."""

    model_config = ConfigDict(extra="allow")

    schema_version: str = "3.0.0"
    chain_id: str
    command: str = ""  # Command that owns this state
    stage: str
    timestamp: str
    stages_complete: list[str] = Field(default_factory=list)
    project_path: Optional[str] = None
    project_name: Optional[str] = None
    analysis_dir: Optional[str] = None
    feature_dir: Optional[str] = None  # For feature-scoped commands
    user_inputs: dict = Field(default_factory=dict)
    tech_stack: dict = Field(default_factory=dict)
    file_structure: dict = Field(default_factory=dict)
    workspace_files: dict = Field(default_factory=dict)
    patterns_found: dict = Field(default_factory=dict)
    dependencies: dict = Field(default_factory=dict)
    files_analyzed: int = 0
    analysis_quality: dict = Field(default_factory=dict)


class ChainState:
    """
    Manages chain state for workflow persistence.

    State locations by command:
    - analyze-project: .analysis/.state/
    - constitution: memory/.state/
    - specify, plan, tasks, implement: specs/{feature}/.state/
    """

    def __init__(
        self,
        state_dir: Path,
        chain_id: Optional[str] = None,
        command: str = "",
    ):
        self.state_dir = state_dir
        self.chain_id = chain_id or generate_chain_id()
        self.command = command
        self._data: dict[str, Any] = {}

    @staticmethod
    def get_state_dir(
        command: str,
        workspace_root: Optional[Path] = None,
        feature_dir: Optional[Path] = None,
    ) -> Path:
        """
        Determine state directory based on command.

        Args:
            command: Command name (analyze-project, constitution, specify, etc.)
            workspace_root: Root directory (defaults to cwd)
            feature_dir: Feature directory for feature-scoped commands

        Returns:
            Path to state directory
        """
        workspace_root = workspace_root or Path.cwd()

        if command == "analyze-project":
            return workspace_root / ".analysis" / ".state"
        elif command == "constitution":
            return workspace_root / "memory" / ".state"
        elif command in FEATURE_SCOPED_COMMANDS:
            if feature_dir:
                return feature_dir / ".state"
            # No feature dir yet - use pending location (state not persisted for early stages)
            return workspace_root / "specs" / ".pending" / ".state"
        else:
            # Default fallback
            return workspace_root / ".analysis" / ".state"

    @classmethod
    def initialize(
        cls,
        project_path: Path,
        command: str = "analyze-project",
        workspace_root: Optional[Path] = None,
        feature_dir: Optional[Path] = None,
    ) -> "ChainState":
        """
        Initialize a new chain for a project.

        Args:
            project_path: Path to the project being analyzed
            command: Command name for state location routing
            workspace_root: Optional root directory (defaults to cwd)
            feature_dir: Optional feature directory for feature-scoped commands

        Returns:
            Initialized ChainState instance
        """
        workspace_root = workspace_root or Path.cwd()
        state_dir = cls.get_state_dir(command, workspace_root, feature_dir)
        state_dir.mkdir(parents=True, exist_ok=True)

        chain = cls(state_dir, command=command)

        # Create timestamp for workspace directory (only for analyze-project)
        if command == "analyze-project":
            timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            project_name = project_path.name
            analysis_dir = workspace_root / ".analysis" / f"{project_name}-{timestamp}"
            analysis_dir.mkdir(parents=True, exist_ok=True)
        else:
            project_name = project_path.name
            analysis_dir = None

        # Initialize bootstrap state
        bootstrap_data = {
            "schema_version": "3.0.0",
            "chain_id": chain.chain_id,
            "command": command,
            "stage": "bootstrap",
            "timestamp": datetime.now().isoformat(),
            "stages_complete": [],
            "project_path": str(project_path.absolute()),
            "project_name": project_name,
            "analysis_dir": str(analysis_dir.absolute()) if analysis_dir else None,
            "feature_dir": str(feature_dir.absolute()) if feature_dir else None,
        }

        chain._data = bootstrap_data

        # Only save bootstrap for commands that persist early stages
        # Note: save() adds command prefix, so just pass "00-bootstrap"
        if command not in FEATURE_SCOPED_COMMANDS:
            chain.save("00-bootstrap", bootstrap_data)

        return chain

    @classmethod
    def load(
        cls,
        chain_id: str,
        command: str = "",
        workspace_root: Optional[Path] = None,
        feature_dir: Optional[Path] = None,
    ) -> "ChainState":
        """
        Load existing chain state.

        Note: Only the latest chain is retained in state files. When a new chain
        starts, it overwrites previous chain state. This method validates that
        the requested chain_id matches the current state.

        Args:
            chain_id: Chain ID to load
            command: Command name for state location routing
            workspace_root: Optional root directory
            feature_dir: Optional feature directory for feature-scoped commands

        Returns:
            Loaded ChainState instance

        Raises:
            FileNotFoundError: If state directory or files not found
            ValueError: If chain_id doesn't match current state
        """
        workspace_root = workspace_root or Path.cwd()

        # Try command-specific locations in order
        state_dirs_to_try = []

        if command:
            state_dirs_to_try.append(cls.get_state_dir(command, workspace_root, feature_dir))

        # Also try feature dir if provided
        if feature_dir and feature_dir.exists():
            state_dirs_to_try.append(feature_dir / ".state")

        # Fallback locations
        state_dirs_to_try.extend([
            workspace_root / "memory" / ".state",
            workspace_root / ".analysis" / ".state",
        ])

        # Find first existing state directory with matching chain
        state_dir = None
        loaded_data = None

        for try_dir in state_dirs_to_try:
            if not try_dir.exists():
                continue

            latest_path = try_dir / "latest.json"
            if latest_path.exists():
                data = json.loads(latest_path.read_text())
                if data.get("chain_id") == chain_id:
                    state_dir = try_dir
                    loaded_data = data
                    break

        if not state_dir or not loaded_data:
            raise FileNotFoundError(
                f"No state found for chain ID: {chain_id}. "
                f"Searched in: {[str(d) for d in state_dirs_to_try]}"
            )

        chain = cls(state_dir, chain_id, command=loaded_data.get("command", command))
        chain._data = loaded_data

        return chain

    def save(
        self,
        stage_name: str,
        data: dict[str, Any],
        stage_num: Optional[int] = None,
    ) -> Optional[Path]:
        """
        Save state for a stage.

        For feature-scoped commands (specify, plan, tasks, implement),
        state is only persisted from stage 3+ (after feature folder exists).

        Args:
            stage_name: Name of the stage (e.g., "01-setup-and-scope")
            data: State data to save
            stage_num: Optional stage number for feature-scoped commands

        Returns:
            Path to saved state file, or None if not persisted
        """
        # Check if we should skip persistence for early stages of feature commands
        if self.command in FEATURE_SCOPED_COMMANDS:
            if stage_num is not None and stage_num < FEATURE_STATE_MIN_STAGE:
                # Don't persist state for stages 1-2 of feature-scoped commands
                # Just update in-memory state
                self._data = {**self._data, **data}
                self._data["stage"] = stage_name
                self._data["command"] = self.command
                return None

        # Merge with existing data
        merged = {**self._data, **data}
        merged["stage"] = stage_name
        merged["timestamp"] = datetime.now().isoformat()
        merged["chain_id"] = self.chain_id
        merged["command"] = self.command

        # Create command-prefixed stage name for file
        file_stage_name = f"{self.command}-{stage_name}" if self.command else stage_name

        # Add to stages_complete if not already there
        if file_stage_name not in merged.get("stages_complete", []):
            merged.setdefault("stages_complete", []).append(file_stage_name)

        # Validate against schema
        validated = StateSchema(**merged)
        self._data = validated.model_dump()

        # Ensure state directory exists
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # Save stage file with command prefix
        stage_file = self.state_dir / f"{file_stage_name}.json"
        stage_file.write_text(json.dumps(self._data, indent=2))

        # Update latest symlink/file
        latest_file = self.state_dir / "latest.json"
        latest_file.write_text(json.dumps(self._data, indent=2))

        return stage_file

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from state."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set value in state (not persisted until save())."""
        self._data[key] = value

    def to_dict(self) -> dict[str, Any]:
        """Return state as dictionary."""
        return dict(self._data)

    def to_json(self) -> str:
        """Return state as JSON string."""
        return json.dumps(self._data, indent=2)

    def get_last_stage(self) -> Optional[str]:
        """Get the last completed stage name."""
        stages = self._data.get("stages_complete", [])
        return stages[-1] if stages else None

    def is_complete(self, stage_name: str) -> bool:
        """Check if a stage is complete."""
        return stage_name in self._data.get("stages_complete", [])

    @property
    def project_path(self) -> Optional[Path]:
        """Get project path."""
        path = self._data.get("project_path")
        return Path(path) if path else None

    @property
    def project_name(self) -> Optional[str]:
        """Get project name."""
        return self._data.get("project_name")

    @property
    def analysis_dir(self) -> Optional[Path]:
        """Get analysis directory path."""
        path = self._data.get("analysis_dir")
        return Path(path) if path else None

    @property
    def workspace_files(self) -> dict:
        """Get workspace file paths."""
        return self._data.get("workspace_files", {})

    @property
    def feature_dir(self) -> Optional[Path]:
        """Get feature directory path."""
        path = self._data.get("feature_dir")
        return Path(path) if path else None

    def set_feature_dir(self, feature_dir: Path) -> None:
        """
        Set feature directory and update state location.

        Called when feature folder is created (stage 3 of specify).
        Updates the state directory to use the feature folder.

        Args:
            feature_dir: Path to the feature directory (e.g., specs/001-user-auth/)
        """
        self._data["feature_dir"] = str(feature_dir.absolute())

        # Update state directory to feature-scoped location
        if self.command in FEATURE_SCOPED_COMMANDS:
            self.state_dir = feature_dir / ".state"
            self.state_dir.mkdir(parents=True, exist_ok=True)
