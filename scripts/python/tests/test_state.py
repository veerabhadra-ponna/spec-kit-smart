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
        """Should save initial bootstrap state."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)

        bootstrap_file = tmp_path / ".analysis" / ".state" / "00-bootstrap.json"
        assert bootstrap_file.exists()

        data = json.loads(bootstrap_file.read_text())
        assert data["stage"] == "00-bootstrap"
        assert data["project_name"] == "project"


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
        """Should raise ValueError when chain ID doesn't match current state."""
        # Initialize a chain
        project_path = tmp_path / "project"
        project_path.mkdir()
        original = ChainState.initialize(project_path, workspace_root=tmp_path)
        original_id = original.chain_id

        # Try to load with a different chain ID
        wrong_id = "deadbeef"
        assert wrong_id != original_id

        with pytest.raises(ValueError) as exc_info:
            ChainState.load(wrong_id, workspace_root=tmp_path)

        # Verify error message contains helpful info
        error_msg = str(exc_info.value)
        assert "mismatch" in error_msg.lower()
        assert wrong_id in error_msg
        assert original_id in error_msg


class TestChainStateSave:
    """Tests for ChainState.save method."""

    def test_saves_stage_file(self, tmp_path):
        """Should save stage-specific file."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-test-stage", {"custom": "data"})

        stage_file = tmp_path / ".analysis" / ".state" / "01-test-stage.json"
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
        """Should track completed stages."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-first", {})
        chain.save("02-second", {})

        assert "01-first" in chain._data["stages_complete"]
        assert "02-second" in chain._data["stages_complete"]

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
        """Should return last completed stage."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-first", {})
        chain.save("02-second", {})

        assert chain.get_last_stage() == "02-second"

    def test_is_complete(self, tmp_path):
        """Should check stage completion."""
        project_path = tmp_path / "project"
        project_path.mkdir()

        chain = ChainState.initialize(project_path, workspace_root=tmp_path)
        chain.save("01-done", {})

        assert chain.is_complete("01-done") is True
        assert chain.is_complete("02-not-done") is False

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
