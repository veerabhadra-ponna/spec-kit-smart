"""Tests for speckit.core.state module (simplified state management)."""

import json
import pytest
from pathlib import Path

from speckit.core.state import (
    AnalysisInputs,
    FeatureMetadata,
    FeatureState,
    FeatureStateManager,
    PromptState,
    AnalysisState,
    AnalysisStateManager,
    has_placeholders,
    get_placeholders,
    check_constitution_complete,
    find_latest_feature_folder,
    resolve_feature_folder,
    SCHEMA_VERSION,
)


class TestPromptState:
    """Tests for PromptState dataclass."""

    def test_default_values(self):
        """Should have sensible defaults."""
        state = PromptState()
        assert state.status == "pending"
        assert state.current_stage is None
        assert state.started is None
        assert state.completed is None
        assert state.artifacts == []

    def test_to_dict(self):
        """Should convert to dictionary."""
        state = PromptState(
            status="completed",
            current_stage="04-generate",
            artifacts=["spec.md"],
        )
        d = state.to_dict()
        assert d["status"] == "completed"
        assert d["current_stage"] == "04-generate"
        assert d["artifacts"] == ["spec.md"]

    def test_from_dict(self):
        """Should create from dictionary."""
        data = {
            "status": "in_progress",
            "current_stage": "02-setup",
            "started": "2025-01-15T10:00:00",
        }
        state = PromptState.from_dict(data)
        assert state.status == "in_progress"
        assert state.current_stage == "02-setup"
        assert state.started == "2025-01-15T10:00:00"


class TestFeatureMetadata:
    """Tests for FeatureMetadata dataclass."""

    def test_required_fields(self):
        """Should require short_name and description."""
        metadata = FeatureMetadata(
            short_name="user-auth",
            description="Add user authentication",
        )
        assert metadata.short_name == "user-auth"
        assert metadata.description == "Add user authentication"
        assert metadata.jira is None

    def test_with_jira(self):
        """Should handle optional JIRA field."""
        metadata = FeatureMetadata(
            short_name="fix-bug",
            description="Fix login bug",
            jira="PROJ-123",
        )
        assert metadata.jira == "PROJ-123"


class TestFeatureState:
    """Tests for FeatureState dataclass."""

    def test_default_state(self):
        """Should have all prompts in pending state."""
        state = FeatureState()
        assert state.schema_version == SCHEMA_VERSION
        assert state.specify.status == "pending"
        assert state.plan.status == "pending"
        assert state.tasks.status == "pending"
        assert state.implement.status == "pending"

    def test_to_json(self):
        """Should serialize to JSON."""
        state = FeatureState(
            feature=FeatureMetadata("test", "Test feature"),
        )
        json_str = state.to_json()
        data = json.loads(json_str)
        assert data["schema_version"] == SCHEMA_VERSION
        assert data["feature"]["short_name"] == "test"

    def test_from_json(self):
        """Should deserialize from JSON."""
        json_str = json.dumps({
            "schema_version": 1,
            "feature": {"short_name": "auth", "description": "Auth feature"},
            "specify": {"status": "completed"},
        })
        state = FeatureState.from_json(json_str)
        assert state.feature.short_name == "auth"
        assert state.specify.status == "completed"


class TestFeatureStateManager:
    """Tests for FeatureStateManager."""

    def test_initialize_creates_state_file(self, tmp_path):
        """Should create state directory and file."""
        folder = tmp_path / "specs" / "001-test"
        folder.mkdir(parents=True)

        manager = FeatureStateManager(folder)
        metadata = FeatureMetadata("test", "Test feature")
        state = manager.initialize(metadata)

        assert manager.state_file.exists()
        assert state.feature.short_name == "test"
        assert state.feature.created is not None

    def test_load_existing_state(self, tmp_path):
        """Should load existing state file."""
        folder = tmp_path / "specs" / "001-test"
        state_dir = folder / ".state"
        state_dir.mkdir(parents=True)

        state_data = {
            "schema_version": 1,
            "feature": {"short_name": "test", "description": "Test"},
            "specify": {"status": "completed"},
            "plan": {"status": "in_progress", "current_stage": "02-setup"},
            "tasks": {"status": "pending"},
            "implement": {"status": "pending"},
        }
        (state_dir / "state.json").write_text(json.dumps(state_data))

        manager = FeatureStateManager(folder)
        state = manager.load()

        assert state.specify.status == "completed"
        assert state.plan.status == "in_progress"
        assert state.plan.current_stage == "02-setup"

    def test_update_prompt(self, tmp_path):
        """Should update specific prompt state."""
        folder = tmp_path / "specs" / "001-test"
        folder.mkdir(parents=True)

        manager = FeatureStateManager(folder)
        manager.initialize(FeatureMetadata("test", "Test"))

        state = manager.update_prompt(
            prompt="specify",
            stage="04-generate",
            status="completed",
            artifacts=["spec.md"],
        )

        assert state.specify.status == "completed"
        assert state.specify.current_stage == "04-generate"
        assert state.specify.artifacts == ["spec.md"]
        assert state.specify.completed is not None

    def test_get_next_action_finds_in_progress(self, tmp_path):
        """Should find in_progress prompt first."""
        folder = tmp_path / "specs" / "001-test"
        folder.mkdir(parents=True)

        manager = FeatureStateManager(folder)
        manager.initialize(FeatureMetadata("test", "Test"))
        manager.update_prompt("specify", "02-research", "in_progress")

        prompt, stage = manager.get_next_action()
        assert prompt == "specify"
        assert stage == "02-research"

    def test_get_next_action_finds_pending(self, tmp_path):
        """Should find first pending prompt if none in progress."""
        folder = tmp_path / "specs" / "001-test"
        folder.mkdir(parents=True)

        manager = FeatureStateManager(folder)
        manager.initialize(FeatureMetadata("test", "Test"))
        manager.update_prompt("specify", "04-generate", "completed")

        prompt, stage = manager.get_next_action()
        assert prompt == "plan"
        # Now returns actual first stage ID from get_stage_order
        assert stage == "01-initialization"

    def test_get_prompt_context(self, tmp_path):
        """Should return context for prompt."""
        folder = tmp_path / "specs" / "001-test"
        folder.mkdir(parents=True)

        manager = FeatureStateManager(folder)
        manager.initialize(FeatureMetadata(
            short_name="test",
            description="Test feature",
            jira="PROJ-123",
        ))

        context = manager.get_prompt_context("specify", "01")
        assert context["feature_dir"] == str(folder)
        assert context["feature_name"] == "test"
        assert context["feature_description"] == "Test feature"
        assert context["jira"] == "PROJ-123"


class TestPlaceholderDetection:
    """Tests for placeholder detection functions."""

    def test_has_placeholders_true(self):
        """Should detect placeholders."""
        content = "## Preamble\n[PROJECT_MISSION]\n## Principles\n[PRINCIPLES]"
        assert has_placeholders(content) is True

    def test_has_placeholders_false(self):
        """Should not detect non-placeholders."""
        content = "## Preamble\nThis is the mission.\n## Principles\n- Principle 1"
        assert has_placeholders(content) is False

    def test_has_placeholders_ignores_lowercase(self):
        """Should ignore lowercase brackets."""
        content = "See [this link] for details"
        assert has_placeholders(content) is False

    def test_get_placeholders(self):
        """Should return list of placeholder names."""
        content = "[PROJECT_MISSION]\n[PRINCIPLES]\n[DATE]"
        placeholders = get_placeholders(content)
        assert "PROJECT_MISSION" in placeholders
        assert "PRINCIPLES" in placeholders
        assert "DATE" in placeholders

    def test_check_constitution_complete_missing(self, tmp_path):
        """Should detect missing constitution."""
        is_complete, msg = check_constitution_complete(tmp_path)
        assert is_complete is False
        assert "does not exist" in msg

    def test_check_constitution_complete_with_placeholders(self, tmp_path):
        """Should detect incomplete constitution."""
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").write_text("# Constitution\n[PROJECT_MISSION]")

        is_complete, msg = check_constitution_complete(tmp_path)
        assert is_complete is False
        assert "placeholders" in msg

    def test_check_constitution_complete_filled(self, tmp_path):
        """Should detect complete constitution."""
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").write_text(
            "# Constitution\n\nThis project builds amazing software."
        )

        is_complete, msg = check_constitution_complete(tmp_path)
        assert is_complete is True
        assert "complete" in msg.lower()


class TestFindFeatureFolder:
    """Tests for folder finding utilities."""

    def test_find_latest_feature_folder(self, tmp_path):
        """Should find most recently modified folder."""
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()

        # Create two feature folders
        folder1 = specs_dir / "001-old"
        folder1.mkdir()
        state1 = folder1 / ".state"
        state1.mkdir()
        (state1 / "state.json").write_text("{}")

        folder2 = specs_dir / "002-new"
        folder2.mkdir()
        state2 = folder2 / ".state"
        state2.mkdir()
        (state2 / "state.json").write_text("{}")

        result = find_latest_feature_folder(specs_dir)
        assert result.name == "002-new"

    def test_resolve_feature_folder_explicit(self, tmp_path):
        """Should return explicit folder path."""
        specs_dir = tmp_path / "specs"
        folder = specs_dir / "001-test"
        folder.mkdir(parents=True)

        result = resolve_feature_folder("001-test", specs_dir)
        assert result == folder

    def test_resolve_feature_folder_latest(self, tmp_path):
        """Should find latest when no folder specified."""
        specs_dir = tmp_path / "specs"
        folder = specs_dir / "001-test"
        folder.mkdir(parents=True)
        state_dir = folder / ".state"
        state_dir.mkdir()
        (state_dir / "state.json").write_text("{}")

        result = resolve_feature_folder(None, specs_dir)
        assert result.name == "001-test"


class TestAnalysisStateManager:
    """Tests for AnalysisStateManager."""

    def test_initialize(self, tmp_path):
        """Should create analysis state."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)

        state = manager.initialize(tmp_path)

        assert manager.state_file.exists()
        assert state.project_path == str(tmp_path)
        assert state.started is not None

    def test_update_stage(self, tmp_path):
        """Should update stage status."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)

        state = manager.update_stage(
            stage="02a-category-scan",
            status="completed",
            artifacts=["categories.json"],
        )

        assert state.stages["02a-category-scan"]["status"] == "completed"
        assert state.stages["02a-category-scan"]["artifacts"] == ["categories.json"]

    def test_update_inputs(self, tmp_path):
        """Should update user inputs in state."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)

        state = manager.update_inputs(
            scope="B",
            context="Testing context",
            concern_type="Authentication",
            current_impl="Custom JWT",
            target_impl="Okta",
        )

        assert state.inputs.scope == "B"
        assert state.inputs.context == "Testing context"
        assert state.inputs.concern_type == "Authentication"
        assert state.inputs.current_impl == "Custom JWT"
        assert state.inputs.target_impl == "Okta"

    def test_update_inputs_partial(self, tmp_path):
        """Should update only provided inputs."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)

        # First update
        manager.update_inputs(scope="A", context="Initial context")

        # Partial update - should preserve scope and context
        state = manager.update_inputs(concern_type="Database")

        assert state.inputs.scope == "A"
        assert state.inputs.context == "Initial context"
        assert state.inputs.concern_type == "Database"

    def test_mark_complete(self, tmp_path):
        """Should mark workflow as complete."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)

        state = manager.mark_complete()

        assert state.workflow_complete is True
        assert state.completed is not None

    def test_get_context_for_prompt(self, tmp_path):
        """Should return context dict with all prompt variables."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)
        manager.update_inputs(
            scope="B",
            context="Test context",
            concern_type="Auth",
            current_impl="JWT",
            target_impl="Okta",
        )

        context = manager.get_context_for_prompt()

        assert context["analysis_dir"] == str(folder)
        assert context["project_path"] == str(tmp_path)
        assert context["scope"] == "B"
        assert context["context"] == "Test context"
        assert context["concern_type"] == "Auth"
        assert context["current_impl"] == "JWT"
        assert context["target_impl"] == "Okta"
        # Both short and long form names
        assert context["current_implementation"] == "JWT"
        assert context["target_implementation"] == "Okta"

    def test_update_stage_with_stage_num(self, tmp_path):
        """Should update stage with stage number for tracking."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)

        state = manager.update_stage(
            stage="02a-category-scan",
            status="completed",
            stage_num=4,
        )

        assert state.stages["02a-category-scan"]["status"] == "completed"
        assert "02a-category-scan" in state.stages_complete

    def test_stages_complete_list(self, tmp_path):
        """Should track completed stages in list."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)

        # Complete multiple stages
        manager.update_stage("01a-initialization", "completed", stage_num=1)
        manager.update_stage("01b-input-collection", "completed", stage_num=2)
        state = manager.update_stage("02a-category-scan", "completed", stage_num=4)

        assert len(state.stages_complete) == 3
        assert "01a-initialization" in state.stages_complete
        assert "01b-input-collection" in state.stages_complete
        assert "02a-category-scan" in state.stages_complete


class TestCorruptedStateHandling:
    """Tests for corrupted state.json handling (fail-fast behavior)."""

    def test_feature_state_manager_corrupted_json(self, tmp_path):
        """FeatureStateManager.load() should raise JSONDecodeError on corrupted JSON."""
        folder = tmp_path / "specs" / "001-test"
        state_dir = folder / ".state"
        state_dir.mkdir(parents=True)

        # Write corrupted JSON
        (state_dir / "state.json").write_text("{invalid json content")

        manager = FeatureStateManager(folder)
        with pytest.raises(json.JSONDecodeError):
            manager.load()

    def test_analysis_state_manager_corrupted_json(self, tmp_path):
        """AnalysisStateManager.load() should raise JSONDecodeError on corrupted JSON."""
        folder = tmp_path / ".analysis" / "test-run"
        folder.mkdir(parents=True)

        # Write corrupted JSON
        (folder / "state.json").write_text("not valid json {{{")

        manager = AnalysisStateManager(folder)
        with pytest.raises(json.JSONDecodeError):
            manager.load()

    def test_feature_state_manager_valid_json(self, tmp_path):
        """FeatureStateManager.load() should succeed with valid JSON."""
        folder = tmp_path / "specs" / "001-test"
        state_dir = folder / ".state"
        state_dir.mkdir(parents=True)

        valid_state = {
            "schema_version": 1,
            "feature": {"short_name": "test", "description": "Test feature"},
            "specify": {"status": "pending"},
        }
        (state_dir / "state.json").write_text(json.dumps(valid_state))

        manager = FeatureStateManager(folder)
        state = manager.load()
        assert state.feature.short_name == "test"


class TestMarkCompleteTimestamp:
    """Tests for mark_complete() timestamp handling."""

    def test_mark_complete_sets_stage_timestamp(self, tmp_path):
        """mark_complete() should set completed timestamp for final in_progress stage."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)

        # Set a stage as in_progress (simulating the final stage)
        manager.update_stage("16-completion", "in_progress", stage_num=16)

        # Now mark complete
        state = manager.mark_complete()

        # Verify the stage has a completed timestamp
        assert state.stages["16-completion"]["status"] == "completed"
        assert state.stages["16-completion"]["completed"] is not None
        assert state.workflow_complete is True


class TestGetCurrentStageCompletedBehavior:
    """Tests for get_current_stage() returning completed stages."""

    def test_returns_completed_stage_when_workflow_not_complete(self, tmp_path):
        """get_current_stage() should return (stage, 'completed') when stage is done but workflow isn't."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)

        # Complete a stage but don't mark workflow complete
        manager.update_stage("03-analysis", "completed", stage_num=3)

        stage, status = manager.get_current_stage()

        # Should return the completed stage with its status, not (None, None)
        assert stage == "03-analysis"
        assert status == "completed"

    def test_returns_none_when_workflow_complete(self, tmp_path):
        """get_current_stage() should return (None, None) when workflow is complete."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)
        manager.mark_complete()

        stage, status = manager.get_current_stage()

        assert stage is None
        assert status is None

    def test_returns_in_progress_stage(self, tmp_path):
        """get_current_stage() should return in_progress stage when one exists."""
        folder = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(folder)
        manager.initialize(tmp_path)
        manager.update_stage("05-review", "in_progress", stage_num=5)

        stage, status = manager.get_current_stage()

        assert stage == "05-review"
        assert status == "in_progress"


class TestAnalysisInputs:
    """Tests for AnalysisInputs dataclass."""

    def test_default_values(self):
        """Should have empty string defaults."""
        inputs = AnalysisInputs()
        assert inputs.scope == ""
        assert inputs.context == ""
        assert inputs.concern_type == ""
        assert inputs.current_impl == ""
        assert inputs.target_impl == ""

    def test_to_dict(self):
        """Should convert to dictionary."""
        inputs = AnalysisInputs(
            scope="B",
            context="Test",
            concern_type="Auth",
            current_impl="JWT",
            target_impl="Okta",
        )
        d = inputs.to_dict()
        assert d["scope"] == "B"
        assert d["context"] == "Test"
        assert d["concern_type"] == "Auth"
        assert d["current_impl"] == "JWT"
        assert d["target_impl"] == "Okta"

    def test_from_dict(self):
        """Should create from dictionary."""
        data = {
            "scope": "A",
            "context": "Context text",
            "concern_type": "",
            "current_impl": "",
            "target_impl": "",
        }
        inputs = AnalysisInputs.from_dict(data)
        assert inputs.scope == "A"
        assert inputs.context == "Context text"
        assert inputs.concern_type == ""
