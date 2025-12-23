"""
Tests for speckit.core.state module.
"""

import json
from pathlib import Path
import pytest

from speckit.core.state import ChainState, StateSchema
from speckit.core.utils import generate_chain_id


class TestStateSchema:
    """Tests for StateSchema model."""

    def test_minimal_valid_schema(self):
        """Should accept minimal valid data."""
        data = {
            "chain_id": "abc12345",
            "stage": "test",
            "timestamp": "2025-01-01T00:00:00",
        }
        schema = StateSchema(**data)
        assert schema.chain_id == "abc12345"
        assert schema.stage == "test"

    def test_default_values(self):
        """Should have sensible defaults."""
        data = {
            "chain_id": "abc12345",
            "stage": "test",
            "timestamp": "2025-01-01T00:00:00",
        }
        schema = StateSchema(**data)
        assert schema.stages_complete == []
        assert schema.user_inputs == {}
        assert schema.tech_stack == {}
        assert schema.files_analyzed == 0

    def test_full_schema(self):
        """Should accept full schema data."""
        data = {
            "schema_version": "3.0.0",
            "chain_id": "abc12345",
            "stage": "02-analysis",
            "timestamp": "2025-01-01T12:00:00",
            "stages_complete": ["01-setup"],
            "project_path": "/path/to/project",
            "project_name": "my-project",
            "analysis_dir": "/path/to/.analysis",
            "user_inputs": {"scope": "A"},
            "tech_stack": {"language": "python"},
            "files_analyzed": 42,
        }
        schema = StateSchema(**data)
        assert schema.project_name == "my-project"
        assert schema.files_analyzed == 42

    def test_extra_fields_allowed(self):
        """Should allow extra fields."""
        data = {
            "chain_id": "abc12345",
            "stage": "test",
            "timestamp": "2025-01-01T00:00:00",
            "custom_field": "custom_value",
        }
        schema = StateSchema(**data)
        assert schema.custom_field == "custom_value"


class TestChainStateGenerateId:
    """Tests for chain ID generation (uses generate_chain_id from utils)."""

    def test_generates_8_char_id(self):
        """Should generate 8-character ID."""
        chain_id = generate_chain_id()
        assert len(chain_id) == 8

    def test_generates_hex_id(self):
        """Should generate valid hex ID."""
        chain_id = generate_chain_id()
        int(chain_id, 16)  # Should not raise


class TestChainStateInitialize:
    """Tests for ChainState.initialize."""

    def test_creates_state_directory(self, tmp_path):
        """Should create .analysis/.state directory."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        state_dir = tmp_path / ".analysis" / ".state"
        assert state_dir.exists()

    def test_creates_analysis_directory(self, tmp_path):
        """Should create timestamped analysis directory."""
        project_path = tmp_path / "my-project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        analysis_dirs = list((tmp_path / ".analysis").glob("my-project-*"))
        assert len(analysis_dirs) == 1

    def test_returns_chain_with_id(self, tmp_path):
        """Should return chain with valid ID."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        assert len(chain.chain_id) == 8

    def test_saves_bootstrap_state(self, tmp_path):
        """Should save initial bootstrap state with command prefix."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Default command is analyze-project
        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        # Bootstrap file now has command prefix
        bootstrap_file = tmp_path / ".analysis" / ".state" / "analyze-project-00-bootstrap.json"
        assert bootstrap_file.exists()

        data = json.loads(bootstrap_file.read_text())
        assert data["stage"] == "00-bootstrap"
        assert data["project_name"] == "project"
        assert data["command"] == "analyze-project"


class TestChainStateLoad:
    """Tests for ChainState.load."""

    def test_load_existing_chain(self, tmp_path):
        """Should load existing chain state."""
        # First initialize
        project_path = tmp_path / "project"
        project_path.mkdir()
        original = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain_id = original.chain_id

        # Then load
        loaded = ChainState.load(chain_id, workspace_root=tmp_path)

        assert loaded.chain_id == chain_id
        assert loaded.project_name == "project"

    def test_load_nonexistent_chain(self, tmp_path):
        """Should raise FileNotFoundError for missing chain."""
        with pytest.raises(FileNotFoundError):
            ChainState.load("nonexistent", workspace_root=tmp_path)

    def test_load_mismatched_chain_id(self, tmp_path):
        """Should raise FileNotFoundError when chain ID doesn't match any state."""
        # Initialize a chain
        project_path = tmp_path / "project"
        project_path.mkdir()
        original = ChainState.initialize(project_path, workspace_root=tmp_path)
        original_id = original.chain_id

        # Try to load with a different chain ID
        wrong_id = "deadbeef"
        assert wrong_id != original_id

        # Now raises FileNotFoundError since we search for matching chain_id
        with pytest.raises(FileNotFoundError) as exc_info:
            ChainState.load(wrong_id, workspace_root=tmp_path)

        # Verify error message contains helpful info
        error_msg = str(exc_info.value)
        assert wrong_id in error_msg


class TestChainStateSave:
    """Tests for ChainState.save method."""

    def test_saves_stage_file(self, tmp_path):
        """Should save stage-specific file with command prefix."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Default command is analyze-project
        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-test-stage", {"custom": "data"})

        # Stage file now has command prefix
        stage_file = tmp_path / ".analysis" / ".state" / "analyze-project-01-test-stage.json"
        assert stage_file.exists()

    def test_updates_latest_file(self, tmp_path):
        """Should update latest.json file."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-test-stage", {"custom": "data"})

        latest_file = tmp_path / ".analysis" / ".state" / "latest.json"
        assert latest_file.exists()

        data = json.loads(latest_file.read_text())
        assert data["stage"] == "01-test-stage"

    def test_tracks_stages_complete(self, tmp_path):
        """Should track completed stages with command prefix."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Default command is analyze-project
        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-first", {})
        chain.save("02-second", {})

        # Stages are prefixed with command name
        assert "analyze-project-01-first" in chain._data["stages_complete"]
        assert "analyze-project-02-second" in chain._data["stages_complete"]

    def test_merges_data(self, tmp_path):
        """Should merge new data with existing."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-stage", {"tech_stack": {"language": "python"}})

        assert chain._data["tech_stack"]["language"] == "python"
        assert chain._data["project_name"] == "project"  # Original data preserved


class TestChainStateProperties:
    """Tests for ChainState properties."""

    def test_project_path(self, tmp_path):
        """Should return project path."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        assert chain.project_path == project_path.absolute()

    def test_project_name(self, tmp_path):
        """Should return project name."""
        project_path = tmp_path / "my-app"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        assert chain.project_name == "my-app"

    def test_analysis_dir(self, tmp_path):
        """Should return analysis directory."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        assert chain.analysis_dir is not None
        assert chain.analysis_dir.exists()


class TestChainStateHelpers:
    """Tests for ChainState helper methods."""

    def test_get_and_set(self, tmp_path):
        """Should get and set values."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.set("custom_key", "custom_value")

        assert chain.get("custom_key") == "custom_value"
        assert chain.get("missing_key", "default") == "default"

    def test_get_last_stage(self, tmp_path):
        """Should return last completed stage with command prefix."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-first", {})
        chain.save("02-second", {})

        # Returns command-prefixed stage name
        assert chain.get_last_stage() == "analyze-project-02-second"

    def test_is_complete(self, tmp_path):
        """Should check stage completion with command prefix."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-done", {})

        # Use command-prefixed stage name
        assert chain.is_complete("analyze-project-01-done") is True
        assert chain.is_complete("analyze-project-02-not-done") is False

    def test_to_dict(self, tmp_path):
        """Should return state as dict."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        result = chain.to_dict()

        assert isinstance(result, dict)
        assert result["chain_id"] == chain.chain_id

    def test_to_json(self, tmp_path):
        """Should return state as JSON string."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        result = chain.to_json()

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed["chain_id"] == chain.chain_id


class TestStateLocationRouting:
    """Tests for command-specific state locations."""

    def test_analyze_project_uses_analysis_state(self, tmp_path):
        """analyze-project should use .analysis/.state/"""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, command="analyze-project", workspace_root=tmp_path)

        assert chain.state_dir == tmp_path / ".analysis" / ".state"
        assert (tmp_path / ".analysis" / ".state").exists()

    def test_constitution_uses_memory_state(self, tmp_path):
        """constitution should use memory/.state/"""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, command="constitution", workspace_root=tmp_path)

        assert chain.state_dir == tmp_path / "memory" / ".state"
        assert (tmp_path / "memory" / ".state").exists()
        # Constitution should save bootstrap
        bootstrap_file = tmp_path / "memory" / ".state" / "constitution-00-bootstrap.json"
        assert bootstrap_file.exists()

    def test_feature_command_uses_pending_initially(self, tmp_path):
        """Feature commands should use specs/.pending/.state/ initially."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, command="specify", workspace_root=tmp_path)

        assert chain.state_dir == tmp_path / "specs" / ".pending" / ".state"
        # Feature commands don't save bootstrap
        bootstrap_file = tmp_path / "specs" / ".pending" / ".state" / "specify-00-bootstrap.json"
        assert not bootstrap_file.exists()

    def test_feature_command_skips_early_stages(self, tmp_path):
        """Feature commands should not persist state for stages 1-2."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, command="specify", workspace_root=tmp_path)

        # Stage 1 - should not persist
        result = chain.save("01-initialization", {"data": "test"}, stage_num=1)
        assert result is None

        # Stage 2 - should not persist
        result = chain.save("02-input-collection", {"data": "test"}, stage_num=2)
        assert result is None

        # Stage 3 - should persist
        result = chain.save("03-branch-setup", {"data": "test"}, stage_num=3)
        assert result is not None
        assert result.exists()

    def test_set_feature_dir_updates_state_location(self, tmp_path):
        """set_feature_dir should update state directory."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        feature_dir = tmp_path / "specs" / "001-my-feature"
        feature_dir.mkdir(parents=True)

        chain = ChainState.initialize(project_path, command="specify", workspace_root=tmp_path)

        # Initially uses pending
        assert chain.state_dir == tmp_path / "specs" / ".pending" / ".state"

        # Set feature dir
        chain.set_feature_dir(feature_dir)

        # Now uses feature-specific state dir
        assert chain.state_dir == feature_dir / ".state"
        assert (feature_dir / ".state").exists()

    def test_load_finds_constitution_state(self, tmp_path):
        """ChainState.load should find constitution state in memory/.state/"""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Initialize constitution
        chain = ChainState.initialize(project_path, command="constitution", workspace_root=tmp_path)
        chain_id = chain.chain_id

        # Load it back
        loaded = ChainState.load(chain_id, command="constitution", workspace_root=tmp_path)

        assert loaded.chain_id == chain_id
        assert loaded.command == "constitution"

    def test_set_feature_dir_migrates_state_from_pending(self, tmp_path):
        """set_feature_dir should migrate state from pending and clean up."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Create feature directory
        feature_dir = tmp_path / "specs" / "001-my-feature"
        feature_dir.mkdir(parents=True)

        # Initialize specify chain (goes to pending)
        chain = ChainState.initialize(project_path, command="specify", workspace_root=tmp_path)
        chain_id = chain.chain_id

        # Save stage 3 state (this is when feature folder would be created)
        chain.save("03-branch-setup", {"data": "test"}, stage_num=3)

        # Verify state is in pending
        pending_state = tmp_path / "specs" / ".pending" / ".state"
        assert pending_state.exists()
        assert (pending_state / "latest.json").exists()

        # Now set feature dir (simulates what happens after create-feature)
        chain.set_feature_dir(feature_dir)

        # State should be in feature directory
        feature_state = feature_dir / ".state"
        assert feature_state.exists()
        assert (feature_state / "latest.json").exists()

        # Pending should be cleaned up (or only contain other chains' state)
        # Check our chain's state was removed from pending
        if pending_state.exists():
            for state_file in pending_state.glob("*.json"):
                import json
                data = json.loads(state_file.read_text())
                assert data.get("chain_id") != chain_id, "Chain state should be migrated from pending"

    def test_set_feature_dir_cleans_pending_when_initialized_with_feature_dir(self, tmp_path):
        """set_feature_dir should clean up empty pending even when chain started with feature_dir."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Create empty pending state dir (simulates leftover from previous failed workflow)
        pending_state = tmp_path / "specs" / ".pending" / ".state"
        pending_state.mkdir(parents=True)

        # Create feature directory
        feature_dir = tmp_path / "specs" / "001-my-feature"
        feature_dir.mkdir(parents=True)

        # Initialize chain DIRECTLY with feature_dir (simulates stage 4 restart with --feature-dir)
        chain = ChainState.initialize(
            project_path, command="specify", workspace_root=tmp_path, feature_dir=feature_dir
        )

        # State should be in feature directory directly
        assert chain.state_dir == feature_dir / ".state"

        # Now call set_feature_dir (as stages.py does)
        chain.set_feature_dir(feature_dir, workspace_root=tmp_path)

        # Pending should be cleaned up since it's empty
        assert not pending_state.exists(), "Empty .pending/.state should be removed"
        assert not (tmp_path / "specs" / ".pending").exists(), "Empty .pending should be removed"

    def test_load_scans_feature_directories(self, tmp_path):
        """ChainState.load should find state in feature directories."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Create feature directory with state
        feature_dir = tmp_path / "specs" / "001-my-feature"
        feature_state = feature_dir / ".state"
        feature_state.mkdir(parents=True)

        # Create state file directly in feature directory
        chain_id = "test1234"
        state_data = {
            "chain_id": chain_id,
            "command": "specify",
            "stage": "03-branch-setup",
            "timestamp": "2025-01-01T00:00:00",
        }
        import json
        (feature_state / "latest.json").write_text(json.dumps(state_data))

        # Load should find it
        loaded = ChainState.load(chain_id, command="specify", workspace_root=tmp_path)
        assert loaded.chain_id == chain_id
        assert loaded.state_dir == feature_state

    def test_load_skips_malformed_json(self, tmp_path):
        """ChainState.load should skip malformed JSON files and continue searching."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        # Create a malformed JSON file in the first location
        malformed_state = tmp_path / "specs" / ".pending" / ".state"
        malformed_state.mkdir(parents=True)
        (malformed_state / "latest.json").write_text("{ invalid json }")

        # Create valid state in a feature directory
        feature_dir = tmp_path / "specs" / "001-my-feature"
        feature_state = feature_dir / ".state"
        feature_state.mkdir(parents=True)

        chain_id = "test5678"
        state_data = {
            "chain_id": chain_id,
            "command": "specify",
            "stage": "03-branch-setup",
            "timestamp": "2025-01-01T00:00:00",
        }
        import json
        (feature_state / "latest.json").write_text(json.dumps(state_data))

        # Load should skip malformed file and find the valid one
        loaded = ChainState.load(chain_id, command="specify", workspace_root=tmp_path)
        assert loaded.chain_id == chain_id
        assert loaded.state_dir == feature_state
