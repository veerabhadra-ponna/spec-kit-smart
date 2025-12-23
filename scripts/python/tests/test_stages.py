"""
Tests for speckit.core.stages module.
"""

import json
import pytest
from pathlib import Path

from speckit.core.stages import _find_existing_chain_for_command


class TestFindExistingChainForCommand:
    """Tests for _find_existing_chain_for_command function."""

    def test_finds_chain_in_feature_dir(self, tmp_path):
        """Should find chain_id from provided feature directory."""
        feature_dir = tmp_path / "specs" / "001-my-feature"
        state_dir = feature_dir / ".state"
        state_dir.mkdir(parents=True)

        state_data = {
            "chain_id": "abc12345",
            "command": "specify",
            "stage": "03-branch-setup",
            "timestamp": "2025-01-01T00:00:00",
        }
        (state_dir / "latest.json").write_text(json.dumps(state_data))

        result = _find_existing_chain_for_command(
            "specify", feature_dir=feature_dir, workspace_root=tmp_path
        )

        assert result == "abc12345"

    def test_finds_chain_in_pending(self, tmp_path):
        """Should find chain_id from pending state directory."""
        pending_state = tmp_path / "specs" / ".pending" / ".state"
        pending_state.mkdir(parents=True)

        state_data = {
            "chain_id": "pending123",
            "command": "specify",
            "stage": "03-branch-setup",
            "timestamp": "2025-01-01T00:00:00",
        }
        (pending_state / "latest.json").write_text(json.dumps(state_data))

        result = _find_existing_chain_for_command("specify", workspace_root=tmp_path)

        assert result == "pending123"

    def test_scans_feature_directories(self, tmp_path):
        """Should scan feature directories when no feature_dir provided."""
        # Create multiple feature directories
        feature1 = tmp_path / "specs" / "001-older-feature" / ".state"
        feature1.mkdir(parents=True)
        (feature1 / "latest.json").write_text(json.dumps({
            "chain_id": "older111",
            "command": "specify",
            "stage": "06-complete",
            "timestamp": "2025-01-01T00:00:00",
        }))

        feature2 = tmp_path / "specs" / "002-newer-feature" / ".state"
        feature2.mkdir(parents=True)
        (feature2 / "latest.json").write_text(json.dumps({
            "chain_id": "newer222",
            "command": "specify",
            "stage": "04-generate-spec",
            "timestamp": "2025-01-02T00:00:00",
        }))

        # Should find the most recent (sorted by name, reverse order)
        result = _find_existing_chain_for_command("specify", workspace_root=tmp_path)

        assert result == "newer222"

    def test_ignores_different_command(self, tmp_path):
        """Should ignore state files from different commands."""
        pending_state = tmp_path / "specs" / ".pending" / ".state"
        pending_state.mkdir(parents=True)

        state_data = {
            "chain_id": "plan12345",
            "command": "plan",  # Different command
            "stage": "02-setup",
            "timestamp": "2025-01-01T00:00:00",
        }
        (pending_state / "latest.json").write_text(json.dumps(state_data))

        result = _find_existing_chain_for_command("specify", workspace_root=tmp_path)

        assert result is None

    def test_returns_none_when_no_state(self, tmp_path):
        """Should return None when no state files exist."""
        (tmp_path / "specs").mkdir(parents=True)

        result = _find_existing_chain_for_command("specify", workspace_root=tmp_path)

        assert result is None

    def test_skips_malformed_json(self, tmp_path):
        """Should skip malformed JSON files and continue searching."""
        # Create malformed state in pending
        pending_state = tmp_path / "specs" / ".pending" / ".state"
        pending_state.mkdir(parents=True)
        (pending_state / "latest.json").write_text("{ invalid json }")

        # Create valid state in feature directory
        feature_state = tmp_path / "specs" / "001-my-feature" / ".state"
        feature_state.mkdir(parents=True)
        (feature_state / "latest.json").write_text(json.dumps({
            "chain_id": "valid123",
            "command": "specify",
            "stage": "04-generate-spec",
            "timestamp": "2025-01-01T00:00:00",
        }))

        result = _find_existing_chain_for_command("specify", workspace_root=tmp_path)

        assert result == "valid123"

    def test_feature_dir_takes_priority(self, tmp_path):
        """Feature directory state should take priority over pending."""
        # Create state in pending
        pending_state = tmp_path / "specs" / ".pending" / ".state"
        pending_state.mkdir(parents=True)
        (pending_state / "latest.json").write_text(json.dumps({
            "chain_id": "pending123",
            "command": "specify",
            "stage": "03-branch-setup",
            "timestamp": "2025-01-01T00:00:00",
        }))

        # Create state in feature directory
        feature_dir = tmp_path / "specs" / "001-my-feature"
        feature_state = feature_dir / ".state"
        feature_state.mkdir(parents=True)
        (feature_state / "latest.json").write_text(json.dumps({
            "chain_id": "feature456",
            "command": "specify",
            "stage": "04-generate-spec",
            "timestamp": "2025-01-02T00:00:00",
        }))

        # When feature_dir is provided, it should take priority
        result = _find_existing_chain_for_command(
            "specify", feature_dir=feature_dir, workspace_root=tmp_path
        )

        assert result == "feature456"
