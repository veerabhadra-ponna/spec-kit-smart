"""
Chain State Management

Manages persistent state across workflow stages.
Enables session recovery and progress tracking.
"""

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class StateSchema(BaseModel):
    """Schema for chain state validation."""

    model_config = ConfigDict(extra="allow")

    schema_version: str = "3.0.0"
    chain_id: str
    stage: str
    timestamp: str
    stages_complete: list[str] = Field(default_factory=list)
    project_path: Optional[str] = None
    project_name: Optional[str] = None
    analysis_dir: Optional[str] = None
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

    State files are stored in .analysis/.state/ directory.
    """

    def __init__(self, state_dir: Path, chain_id: Optional[str] = None):
        self.state_dir = state_dir
        self.chain_id = chain_id or self._generate_id()
        self._data: dict[str, Any] = {}

    @staticmethod
    def _generate_id() -> str:
        """Generate unique chain ID (8 hex chars)."""
        timestamp = str(time.time()).encode()
        return hashlib.md5(timestamp).hexdigest()[:8]

    @classmethod
    def initialize(cls, project_path: Path, workspace_root: Optional[Path] = None) -> "ChainState":
        """
        Initialize a new chain for a project.

        Args:
            project_path: Path to the project being analyzed
            workspace_root: Optional root for .analysis directory (defaults to cwd)

        Returns:
            Initialized ChainState instance
        """
        workspace_root = workspace_root or Path.cwd()
        state_dir = workspace_root / ".analysis" / ".state"
        state_dir.mkdir(parents=True, exist_ok=True)

        chain = cls(state_dir)

        # Create timestamp for workspace directory
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        project_name = project_path.name
        analysis_dir = workspace_root / ".analysis" / f"{project_name}-{timestamp}"
        analysis_dir.mkdir(parents=True, exist_ok=True)

        # Initialize bootstrap state
        bootstrap_data = {
            "schema_version": "3.0.0",
            "chain_id": chain.chain_id,
            "stage": "bootstrap",
            "timestamp": datetime.now().isoformat(),
            "stages_complete": [],
            "project_path": str(project_path.absolute()),
            "project_name": project_name,
            "analysis_dir": str(analysis_dir.absolute()),
        }

        chain._data = bootstrap_data
        chain.save("00-bootstrap", bootstrap_data)

        return chain

    @classmethod
    def load(cls, chain_id: str, workspace_root: Optional[Path] = None) -> "ChainState":
        """
        Load existing chain state.

        Args:
            chain_id: Chain ID to load
            workspace_root: Optional root for .analysis directory

        Returns:
            Loaded ChainState instance

        Raises:
            FileNotFoundError: If chain state not found
        """
        workspace_root = workspace_root or Path.cwd()
        state_dir = workspace_root / ".analysis" / ".state"

        if not state_dir.exists():
            raise FileNotFoundError(f"State directory not found: {state_dir}")

        chain = cls(state_dir, chain_id)

        # Load latest state
        latest_path = state_dir / "latest.json"
        if latest_path.exists():
            chain._data = json.loads(latest_path.read_text())
        else:
            # Find most recent state file
            state_files = sorted(state_dir.glob("*.json"), reverse=True)
            if state_files:
                chain._data = json.loads(state_files[0].read_text())
            else:
                raise FileNotFoundError(f"No state files found for chain: {chain_id}")

        return chain

    def save(self, stage_name: str, data: dict[str, Any]) -> Path:
        """
        Save state for a stage.

        Args:
            stage_name: Name of the stage (e.g., "01-setup-and-scope")
            data: State data to save

        Returns:
            Path to saved state file
        """
        # Merge with existing data
        merged = {**self._data, **data}
        merged["stage"] = stage_name
        merged["timestamp"] = datetime.now().isoformat()
        merged["chain_id"] = self.chain_id

        # Add to stages_complete if not already there
        if stage_name not in merged.get("stages_complete", []):
            merged.setdefault("stages_complete", []).append(stage_name)

        # Validate against schema
        validated = StateSchema(**merged)
        self._data = validated.model_dump()

        # Save stage file
        stage_file = self.state_dir / f"{stage_name}.json"
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
