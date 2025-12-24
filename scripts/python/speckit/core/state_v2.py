"""
Simplified state management for spec-kit workflows.

Uses folder paths as implicit chain IDs:
- Feature workflows: specs/{folder}/.state/state.json
- Analysis workflows: .analysis/{folder}/state.json
- Constitution: No state file (file existence check only)
"""

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from speckit.core.utils import safe_json_loads, safe_json_dumps


# Schema version for future migrations
SCHEMA_VERSION = 1


@dataclass
class PromptState:
    """State for a single prompt (specify, plan, tasks, implement)."""

    status: str = "pending"  # pending | in_progress | completed
    current_stage: Optional[str] = None
    started: Optional[str] = None
    completed: Optional[str] = None
    artifacts: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "status": self.status,
            "current_stage": self.current_stage,
            "started": self.started,
            "completed": self.completed,
            "artifacts": self.artifacts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PromptState":
        """Create from dictionary."""
        return cls(
            status=data.get("status", "pending"),
            current_stage=data.get("current_stage"),
            started=data.get("started"),
            completed=data.get("completed"),
            artifacts=data.get("artifacts", []),
        )


@dataclass
class FeatureMetadata:
    """Metadata about a feature."""

    short_name: str
    description: str
    jira: Optional[str] = None
    created: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "short_name": self.short_name,
            "description": self.description,
            "jira": self.jira,
            "created": self.created,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FeatureMetadata":
        """Create from dictionary."""
        return cls(
            short_name=data.get("short_name", ""),
            description=data.get("description", ""),
            jira=data.get("jira"),
            created=data.get("created"),
        )


@dataclass
class FeatureState:
    """Complete state for a feature workflow."""

    schema_version: int = SCHEMA_VERSION
    feature: FeatureMetadata = field(default_factory=lambda: FeatureMetadata("", ""))
    specify: PromptState = field(default_factory=PromptState)
    plan: PromptState = field(default_factory=PromptState)
    tasks: PromptState = field(default_factory=PromptState)
    implement: PromptState = field(default_factory=PromptState)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "schema_version": self.schema_version,
            "feature": self.feature.to_dict(),
            "specify": self.specify.to_dict(),
            "plan": self.plan.to_dict(),
            "tasks": self.tasks.to_dict(),
            "implement": self.implement.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FeatureState":
        """Create from dictionary."""
        return cls(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            feature=FeatureMetadata.from_dict(data.get("feature", {})),
            specify=PromptState.from_dict(data.get("specify", {})),
            plan=PromptState.from_dict(data.get("plan", {})),
            tasks=PromptState.from_dict(data.get("tasks", {})),
            implement=PromptState.from_dict(data.get("implement", {})),
        )

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return safe_json_dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "FeatureState":
        """Create from JSON string."""
        data = safe_json_loads(json_str, default={})
        return cls.from_dict(data)


class FeatureStateManager:
    """Manages state for a feature workflow."""

    def __init__(self, folder_path: Path):
        """Initialize with feature folder path."""
        self.folder = Path(folder_path)
        self.state_dir = self.folder / ".state"
        self.state_file = self.state_dir / "state.json"

    def initialize(self, metadata: FeatureMetadata) -> FeatureState:
        """Initialize new feature state."""
        self.state_dir.mkdir(parents=True, exist_ok=True)

        if metadata.created is None:
            metadata.created = datetime.now().isoformat()

        state = FeatureState(feature=metadata)
        self.save(state)
        return state

    def exists(self) -> bool:
        """Check if state file exists."""
        return self.state_file.exists()

    def load(self) -> FeatureState:
        """Load state from file."""
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")

        content = self.state_file.read_text(encoding="utf-8")
        return FeatureState.from_json(content)

    def save(self, state: FeatureState) -> None:
        """Save state to file."""
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(state.to_json(), encoding="utf-8")

    def update_prompt(
        self,
        prompt: str,
        stage: str,
        status: str,
        artifacts: list = None,
    ) -> FeatureState:
        """Update state for a specific prompt."""
        state = self.load()
        prompt_state = getattr(state, prompt)

        prompt_state.current_stage = stage
        prompt_state.status = status

        if status == "in_progress" and prompt_state.started is None:
            prompt_state.started = datetime.now().isoformat()

        if status == "completed":
            prompt_state.completed = datetime.now().isoformat()

        if artifacts:
            prompt_state.artifacts = artifacts

        self.save(state)
        return state

    def get_prompt_context(self, prompt: str, stage: str) -> dict:
        """Get context variables needed for a prompt stage.

        Returns only what the prompt needs, not full state.
        """
        state = self.load()

        # Base context
        context = {
            "feature_dir": str(self.folder),
            "feature_name": state.feature.short_name,
            "feature_description": state.feature.description,
        }

        if state.feature.jira:
            context["jira"] = state.feature.jira

        # Add artifacts from completed prompts
        if state.specify.status == "completed":
            spec_path = self.folder / "spec.md"
            if spec_path.exists():
                context["spec_path"] = str(spec_path)

        if state.plan.status == "completed":
            plan_path = self.folder / "plan.md"
            if plan_path.exists():
                context["plan_path"] = str(plan_path)

        if state.tasks.status == "completed":
            tasks_path = self.folder / "tasks.md"
            if tasks_path.exists():
                context["tasks_path"] = str(tasks_path)

        return context

    def get_next_action(self) -> tuple:
        """Determine next prompt and stage to run.

        Returns:
            (prompt_name, stage) or (None, None) if complete
        """
        state = self.load()

        prompt_order = ["specify", "plan", "tasks", "implement"]

        for prompt in prompt_order:
            prompt_state = getattr(state, prompt)

            if prompt_state.status == "in_progress":
                return (prompt, prompt_state.current_stage)

            if prompt_state.status == "pending":
                return (prompt, "01")

        return (None, None)


@dataclass
class AnalysisState:
    """State for an analysis workflow."""

    schema_version: int = SCHEMA_VERSION
    project_path: str = ""
    started: Optional[str] = None
    completed: Optional[str] = None
    stages: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "schema_version": self.schema_version,
            "project_path": self.project_path,
            "started": self.started,
            "completed": self.completed,
            "stages": self.stages,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisState":
        """Create from dictionary."""
        return cls(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            project_path=data.get("project_path", ""),
            started=data.get("started"),
            completed=data.get("completed"),
            stages=data.get("stages", {}),
        )

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return safe_json_dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "AnalysisState":
        """Create from JSON string."""
        data = safe_json_loads(json_str, default={})
        return cls.from_dict(data)


class AnalysisStateManager:
    """Manages state for an analysis workflow."""

    def __init__(self, folder_path: Path):
        """Initialize with analysis folder path."""
        self.folder = Path(folder_path)
        self.state_file = self.folder / "state.json"

    def initialize(self, project_path: Path) -> AnalysisState:
        """Initialize new analysis state."""
        self.folder.mkdir(parents=True, exist_ok=True)

        state = AnalysisState(
            project_path=str(project_path),
            started=datetime.now().isoformat(),
        )
        self.save(state)
        return state

    def exists(self) -> bool:
        """Check if state file exists."""
        return self.state_file.exists()

    def load(self) -> AnalysisState:
        """Load state from file."""
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")

        content = self.state_file.read_text(encoding="utf-8")
        return AnalysisState.from_json(content)

    def save(self, state: AnalysisState) -> None:
        """Save state to file."""
        self.folder.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(state.to_json(), encoding="utf-8")

    def update_stage(
        self,
        stage: str,
        status: str,
        artifacts: list = None,
    ) -> AnalysisState:
        """Update state for a specific stage."""
        state = self.load()

        if stage not in state.stages:
            state.stages[stage] = {"status": "pending", "artifacts": []}

        state.stages[stage]["status"] = status

        if artifacts:
            state.stages[stage]["artifacts"] = artifacts

        self.save(state)
        return state

    def get_current_stage(self) -> tuple:
        """Get current stage to resume from.

        Returns:
            (stage_name, status) or (None, None) if not started
        """
        state = self.load()

        for stage, info in state.stages.items():
            if info.get("status") == "in_progress":
                return (stage, "in_progress")

        # Find first pending or not-started stage
        return (None, None)


# Placeholder detection for constitution
def has_placeholders(content: str) -> bool:
    """Check if content has unfilled placeholders.

    Placeholders follow pattern: [UPPERCASE_WORD] or [UPPERCASE_WORDS]
    """
    pattern = r"\[([A-Z][A-Z0-9_]*)\]"
    return bool(re.search(pattern, content))


def get_placeholders(content: str) -> list:
    """Return list of placeholder names found in content."""
    pattern = r"\[([A-Z][A-Z0-9_]*)\]"
    return re.findall(pattern, content)


def check_constitution_complete(project_path: Path = None) -> tuple:
    """Check if constitution exists and is complete.

    Returns:
        (is_complete, message)
    """
    if project_path is None:
        project_path = Path.cwd()

    constitution_path = project_path / "memory" / "constitution.md"

    if not constitution_path.exists():
        return (False, "Constitution does not exist")

    content = constitution_path.read_text(encoding="utf-8")
    placeholders = get_placeholders(content)

    if placeholders:
        return (False, f"Constitution has unfilled placeholders: {placeholders}")

    return (True, "Constitution complete. To regenerate, delete memory/constitution.md")


# Utility functions for finding folders
def find_latest_feature_folder(specs_dir: Path = None) -> Path:
    """Find the most recently modified feature folder in specs/.

    Uses state.json mtime as primary sort key, folder name as secondary
    for deterministic selection when mtimes are equal (e.g., in tests).
    Folder names with higher numeric prefixes (e.g., 002-) win ties.
    """
    if specs_dir is None:
        specs_dir = Path("specs")

    if not specs_dir.exists():
        raise FileNotFoundError(f"Specs directory not found: {specs_dir}")

    folders = []
    for item in specs_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            state_file = item / ".state" / "state.json"
            if state_file.exists():
                folders.append((item, state_file.stat().st_mtime))

    if not folders:
        raise FileNotFoundError("No feature folders with state found")

    # Sort by (mtime DESC, folder_name DESC) for deterministic selection
    # Folder names like "002-feature" sort higher than "001-feature"
    folders.sort(key=lambda x: (x[1], x[0].name), reverse=True)
    return folders[0][0]


def find_latest_analysis_folder(analysis_dir: Path = None) -> Path:
    """Find the most recent analysis folder in .analysis/.

    Uses state.json mtime as primary sort key, folder name as secondary
    for deterministic selection when mtimes are equal.
    Folder names with timestamps (e.g., project-20251224-120000) sort naturally.
    """
    if analysis_dir is None:
        analysis_dir = Path(".analysis")

    if not analysis_dir.exists():
        raise FileNotFoundError(f"Analysis directory not found: {analysis_dir}")

    folders = []
    for item in analysis_dir.iterdir():
        if item.is_dir():
            state_file = item / "state.json"
            if state_file.exists():
                folders.append((item, state_file.stat().st_mtime))

    if not folders:
        raise FileNotFoundError("No analysis folders with state found")

    # Sort by (mtime DESC, folder_name DESC) for deterministic selection
    folders.sort(key=lambda x: (x[1], x[0].name), reverse=True)
    return folders[0][0]


def resolve_feature_folder(folder: str = None, specs_dir: Path = None) -> Path:
    """Resolve feature folder from explicit path or find latest.

    Args:
        folder: Explicit folder path or name
        specs_dir: Base specs directory

    Returns:
        Path to feature folder
    """
    if folder:
        folder_path = Path(folder)
        if folder_path.is_absolute():
            return folder_path
        # Relative to specs/
        if specs_dir is None:
            specs_dir = Path("specs")
        return specs_dir / folder

    return find_latest_feature_folder(specs_dir)
