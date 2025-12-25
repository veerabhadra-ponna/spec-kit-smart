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
from speckit.core.prompts import get_stage_order


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
    clarify: PromptState = field(default_factory=PromptState)
    plan: PromptState = field(default_factory=PromptState)
    tasks: PromptState = field(default_factory=PromptState)
    checklist: PromptState = field(default_factory=PromptState)
    implement: PromptState = field(default_factory=PromptState)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "schema_version": self.schema_version,
            "feature": self.feature.to_dict(),
            "specify": self.specify.to_dict(),
            "clarify": self.clarify.to_dict(),
            "plan": self.plan.to_dict(),
            "tasks": self.tasks.to_dict(),
            "checklist": self.checklist.to_dict(),
            "implement": self.implement.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FeatureState":
        """Create from dictionary."""
        return cls(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            feature=FeatureMetadata.from_dict(data.get("feature", {})),
            specify=PromptState.from_dict(data.get("specify", {})),
            clarify=PromptState.from_dict(data.get("clarify", {})),
            plan=PromptState.from_dict(data.get("plan", {})),
            tasks=PromptState.from_dict(data.get("tasks", {})),
            checklist=PromptState.from_dict(data.get("checklist", {})),
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
        """Load state from file.

        Raises:
            FileNotFoundError: If state file doesn't exist
            json.JSONDecodeError: If state file is corrupted (fail-fast)
        """
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")

        content = self.state_file.read_text(encoding="utf-8")

        # Validate JSON syntax first - fail fast on corruption
        # (FeatureState.from_json uses safe_json_loads which swallows errors)
        json.loads(content)  # Raises JSONDecodeError if invalid

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

        # Only set timestamps when absent to preserve original timing for audit fidelity
        if status == "in_progress" and prompt_state.started is None:
            prompt_state.started = datetime.now().isoformat()

        if status == "completed" and prompt_state.completed is None:
            prompt_state.completed = datetime.now().isoformat()

        if artifacts is not None:
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

        # All prompts that can be in_progress (including optional ones)
        all_prompts = ["specify", "clarify", "plan", "tasks", "checklist", "implement"]

        # Main workflow prompts (checked for pending status)
        main_workflow = ["specify", "plan", "tasks", "implement"]

        # First, check ALL prompts for in_progress (resume interrupted work)
        for prompt in all_prompts:
            prompt_state = getattr(state, prompt)
            if prompt_state.status == "in_progress":
                return (prompt, prompt_state.current_stage)

        # Then, check main workflow for pending (start next step)
        for prompt in main_workflow:
            prompt_state = getattr(state, prompt)
            if prompt_state.status == "pending":
                # Get actual first stage ID from fragment order
                stages = get_stage_order(prompt)
                first_stage = stages[0] if stages else "01-initialization"
                return (prompt, first_stage)

        return (None, None)


@dataclass
class AnalysisInputs:
    """User inputs collected during analysis workflow (stage 1b)."""

    scope: str = ""  # "A" (full app) or "B" (cross-cutting)
    context: str = ""  # Additional context provided by user
    # Scope B specific fields
    concern_type: str = ""  # e.g., "Authentication", "Database"
    current_impl: str = ""  # e.g., "Custom JWT"
    target_impl: str = ""  # e.g., "Okta"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "scope": self.scope,
            "context": self.context,
            "concern_type": self.concern_type,
            "current_impl": self.current_impl,
            "target_impl": self.target_impl,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisInputs":
        """Create from dictionary."""
        return cls(
            scope=data.get("scope", ""),
            context=data.get("context", ""),
            concern_type=data.get("concern_type", ""),
            current_impl=data.get("current_impl", ""),
            target_impl=data.get("target_impl", ""),
        )


@dataclass
class AnalysisState:
    """State for an analysis workflow.

    Provides comprehensive state tracking for the analyze-project workflow,
    mirroring the approach used in feature-scoped prompts. The state file
    serves as the primary communication method between sub-stages.

    Location: {analysis_dir}/state.json (e.g., .analysis/project-20251224-164004/state.json)
    """

    schema_version: int = SCHEMA_VERSION
    # Workflow metadata
    workflow: str = "analyze-project"
    current_stage: str = ""  # e.g., "01a-initialization"
    current_stage_num: int = 1
    workflow_complete: bool = False
    # Timestamps
    started: Optional[str] = None
    completed: Optional[str] = None
    # Project being analyzed
    project_path: str = ""
    # User inputs (collected in stage 1b)
    inputs: AnalysisInputs = field(default_factory=AnalysisInputs)
    # Per-stage state for detailed tracking (legacy format, still used)
    stages: dict = field(default_factory=dict)
    # Stages completed (list of stage IDs like "01a-initialization")
    stages_complete: list = field(default_factory=list)
    # Modernization preferences (collected in stage 3A via 10 questions)
    modernization_preferences: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "schema_version": self.schema_version,
            "workflow": self.workflow,
            "current_stage": self.current_stage,
            "current_stage_num": self.current_stage_num,
            "workflow_complete": self.workflow_complete,
            "started": self.started,
            "completed": self.completed,
            "project_path": self.project_path,
            "inputs": self.inputs.to_dict(),
            "stages": self.stages,
            "stages_complete": self.stages_complete,
            "modernization_preferences": self.modernization_preferences,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisState":
        """Create from dictionary."""
        return cls(
            schema_version=data.get("schema_version", SCHEMA_VERSION),
            workflow=data.get("workflow", "analyze-project"),
            current_stage=data.get("current_stage", ""),
            current_stage_num=data.get("current_stage_num", 1),
            workflow_complete=data.get("workflow_complete", False),
            started=data.get("started"),
            completed=data.get("completed"),
            project_path=data.get("project_path", ""),
            inputs=AnalysisInputs.from_dict(data.get("inputs", {})),
            stages=data.get("stages", {}),
            stages_complete=data.get("stages_complete", []),
            modernization_preferences=data.get("modernization_preferences", {}),
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
    """Manages state for an analysis workflow.

    Provides comprehensive state management for analyze-project workflow,
    storing all inputs and tracking progress through sub-stages.
    """

    def __init__(self, folder_path: Path):
        """Initialize with analysis folder path."""
        self.folder = Path(folder_path)
        self.state_file = self.folder / "state.json"
        self.data_folder = self.folder / "data"
        self.reports_folder = self.folder / "reports"

    @property
    def data_path(self) -> Path:
        """Get path to data folder for AI artifacts (JSON)."""
        return self.data_folder

    @property
    def reports_path(self) -> Path:
        """Get path to reports folder for user deliverables (MD)."""
        return self.reports_folder

    def initialize(self, project_path: Path) -> AnalysisState:
        """Initialize new analysis state with folder structure.

        Creates:
            {analysis_dir}/
            ├── state.json          # Workflow state
            ├── data/               # AI artifacts (JSON)
            └── reports/            # User deliverables (MD)
        """
        self.folder.mkdir(parents=True, exist_ok=True)
        self.data_folder.mkdir(parents=True, exist_ok=True)
        self.reports_folder.mkdir(parents=True, exist_ok=True)

        state = AnalysisState(
            project_path=str(project_path),
            started=datetime.now().isoformat(),
            current_stage="01a-initialization",
            current_stage_num=1,
        )
        self.save(state)
        return state

    def exists(self) -> bool:
        """Check if state file exists."""
        return self.state_file.exists()

    def load(self) -> AnalysisState:
        """Load state from file.

        Raises:
            FileNotFoundError: If state file doesn't exist
            json.JSONDecodeError: If state file is corrupted (fail-fast)
        """
        if not self.state_file.exists():
            raise FileNotFoundError(f"State file not found: {self.state_file}")

        content = self.state_file.read_text(encoding="utf-8")

        # Validate JSON syntax first - fail fast on corruption
        # (AnalysisState.from_json uses safe_json_loads which swallows errors)
        json.loads(content)  # Raises JSONDecodeError if invalid

        return AnalysisState.from_json(content)

    def save(self, state: AnalysisState) -> None:
        """Save state to file."""
        self.folder.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(state.to_json(), encoding="utf-8")

    def update_inputs(
        self,
        scope: str = None,
        context: str = None,
        concern_type: str = None,
        current_impl: str = None,
        target_impl: str = None,
    ) -> AnalysisState:
        """Update user inputs in state.

        Called after stage 1b (input collection) to persist user choices.
        """
        state = self.load()

        if scope is not None:
            state.inputs.scope = scope
        if context is not None:
            state.inputs.context = context
        if concern_type is not None:
            state.inputs.concern_type = concern_type
        if current_impl is not None:
            state.inputs.current_impl = current_impl
        if target_impl is not None:
            state.inputs.target_impl = target_impl

        self.save(state)
        return state

    def update_stage(
        self,
        stage: str,
        status: str,
        artifacts: list = None,
        stage_num: int = None,
    ) -> AnalysisState:
        """Update state for a specific stage."""
        state = self.load()

        if stage not in state.stages:
            state.stages[stage] = {"status": "pending", "artifacts": []}

        state.stages[stage]["status"] = status

        if artifacts is not None:
            state.stages[stage]["artifacts"] = artifacts

        # Capture timestamps for auditing and resume scenarios
        # Only set timestamps when absent to preserve original timing
        if status == "in_progress":
            if "started" not in state.stages[stage] or state.stages[stage]["started"] is None:
                state.stages[stage]["started"] = datetime.now().isoformat()
        elif status == "completed":
            if "completed" not in state.stages[stage] or state.stages[stage]["completed"] is None:
                state.stages[stage]["completed"] = datetime.now().isoformat()

        # Always update current stage tracking (not just in_progress)
        # This ensures get_context_for_prompt() returns correct values
        state.current_stage = stage
        if stage_num is not None:
            state.current_stage_num = stage_num

        # Track completed stages
        if status == "completed":
            if stage not in state.stages_complete:
                state.stages_complete.append(stage)

        self.save(state)
        return state

    def mark_complete(self) -> AnalysisState:
        """Mark the entire workflow as complete.

        Also completes ALL in_progress stages to ensure all work is recorded,
        including setting the completed timestamp for audit/duration tracking.
        This self-heals state files that may have multiple in_progress stages
        due to manual edits or interrupted operations.
        """
        state = self.load()

        # Complete ALL in_progress stages (self-healing for inconsistent state)
        for stage_id, stage_info in state.stages.items():
            if stage_info.get("status") == "in_progress":
                state.stages[stage_id]["status"] = "completed"
                # Preserve existing completed timestamp for audit fidelity
                if "completed" not in state.stages[stage_id] or state.stages[stage_id]["completed"] is None:
                    state.stages[stage_id]["completed"] = datetime.now().isoformat()
                if stage_id not in state.stages_complete:
                    state.stages_complete.append(stage_id)

        state.workflow_complete = True
        # Preserve existing workflow completion timestamp for audit fidelity
        if state.completed is None:
            state.completed = datetime.now().isoformat()
        self.save(state)
        return state

    def write_data(self, filename: str, content: str, stage: str = None) -> Path:
        """Write JSON data artifact to data/ folder.

        Args:
            filename: Name of the JSON file (e.g., 'category-patterns.json')
            content: JSON content to write
            stage: Optional stage to track artifact against

        Returns:
            Path to the written file
        """
        self.data_folder.mkdir(parents=True, exist_ok=True)
        file_path = self.data_folder / filename
        file_path.write_text(content, encoding="utf-8")

        # Track artifact in state if stage provided
        if stage:
            self._add_artifact_to_stage(stage, f"data/{filename}")

        return file_path

    def write_report(self, filename: str, content: str, append: bool = False, stage: str = None) -> Path:
        """Write Markdown report to reports/ folder.

        Args:
            filename: Name of the MD file (e.g., 'analysis-report.md')
            content: Markdown content to write
            append: If True, append to existing file
            stage: Optional stage to track artifact against

        Returns:
            Path to the written file
        """
        self.reports_folder.mkdir(parents=True, exist_ok=True)
        file_path = self.reports_folder / filename

        if append and file_path.exists():
            existing = file_path.read_text(encoding="utf-8")
            content = existing + "\n" + content

        file_path.write_text(content, encoding="utf-8")

        # Track artifact in state if stage provided
        if stage:
            self._add_artifact_to_stage(stage, f"reports/{filename}")

        return file_path

    def update_modernization_preferences(self, preferences: dict) -> AnalysisState:
        """Update modernization preferences in state.

        Args:
            preferences: Dict with Q1-Q10 answers from 03a1 and 03a2 stages

        Returns:
            Updated AnalysisState
        """
        state = self.load()
        # Merge with existing preferences (allows incremental updates)
        state.modernization_preferences.update(preferences)
        self.save(state)
        return state

    def _add_artifact_to_stage(self, stage: str, artifact_path: str) -> None:
        """Add artifact path to stage's artifact list."""
        state = self.load()
        if stage in state.stages:
            artifacts = state.stages[stage].get("artifacts", [])
            if artifact_path not in artifacts:
                artifacts.append(artifact_path)
                state.stages[stage]["artifacts"] = artifacts
                self.save(state)

    def get_file_stats(self, filepath: str) -> dict:
        """Get statistics about a file.

        Args:
            filepath: Path to file (relative to analysis folder or absolute)

        Returns:
            Dict with lines, size_bytes, size_kb, exists
        """
        # Resolve path
        path = Path(filepath)
        if not path.is_absolute():
            path = self.folder / filepath

        if not path.exists():
            return {"exists": False, "lines": 0, "size_bytes": 0, "size_kb": 0}

        content = path.read_text(encoding="utf-8")
        size_bytes = path.stat().st_size

        return {
            "exists": True,
            "lines": len(content.splitlines()),
            "size_bytes": size_bytes,
            "size_kb": round(size_bytes / 1024, 2),
        }

    def count_pattern_matches(self, filepath: str, pattern: str) -> int:
        """Count regex pattern matches in a file.

        Args:
            filepath: Path to file
            pattern: Regex pattern to match

        Returns:
            Count of matches
        """
        import re

        path = Path(filepath)
        if not path.is_absolute():
            path = self.folder / filepath

        if not path.exists():
            return 0

        content = path.read_text(encoding="utf-8")
        return len(re.findall(pattern, content))

    def get_current_stage(self) -> tuple:
        """Get current stage to resume from.

        Returns:
            (stage_name, status) where status is "in_progress", "completed", or "pending"
            (None, None) only if workflow_complete=True or no stages exist
        """
        state = self.load()

        # Check if workflow is complete - nothing to resume
        if state.workflow_complete:
            return (None, None)

        # First check for in_progress stages
        for stage, info in state.stages.items():
            if info.get("status") == "in_progress":
                return (stage, "in_progress")

        # Return current_stage with its actual status from state.stages
        # This allows callers to distinguish "completed stage, more work pending"
        # from "workflow fully complete"
        if state.current_stage:
            stage_info = state.stages.get(state.current_stage, {})
            actual_status = stage_info.get("status", "pending")
            # Return the stage with its status - caller can determine next action
            return (state.current_stage, actual_status)

        return (None, None)

    def get_context_for_prompt(self) -> dict:
        """Get context variables for prompt rendering.

        Returns a dict with all values needed by prompts,
        reading from state.json for consistency.

        Template variables available:
            {analysis_dir} - Root analysis folder
            {data_dir} - Folder for AI artifacts (JSON)
            {reports_dir} - Folder for user deliverables (MD)
            {project_path} - Project being analyzed
            {scope} - Analysis scope (A or B)
            etc.
        """
        state = self.load()

        return {
            "analysis_dir": str(self.folder),
            "data_dir": str(self.data_folder),
            "reports_dir": str(self.reports_folder),
            "project_path": state.project_path,
            "scope": state.inputs.scope or "A",
            "context": state.inputs.context or "",
            "concern_type": state.inputs.concern_type or "",
            "current_impl": state.inputs.current_impl or "",
            "target_impl": state.inputs.target_impl or "",
            "current_implementation": state.inputs.current_impl or "",
            "target_implementation": state.inputs.target_impl or "",
            "current_stage": state.current_stage,
            "current_stage_num": state.current_stage_num,
            "stages_complete": state.stages_complete,
            "workflow_complete": state.workflow_complete,
            "modernization_preferences": state.modernization_preferences,
        }


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
