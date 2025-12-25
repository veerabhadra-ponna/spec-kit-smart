"""Tests for speckit.commands.analyze module."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from speckit.core.state import AnalysisState, AnalysisInputs, AnalysisStateManager
from speckit.commands.analyze import (
    _auto_detect_stage_from_state,
    _get_stage_num_from_id,
    analyze_project,
)


class TestGetStageNumFromId:
    """Tests for _get_stage_num_from_id helper function.

    Stage numbers are CLI command numbers (1-16), mapped via STAGE_MAP.
    """

    def test_extracts_stage_from_stage_map(self):
        """Should extract stage number using STAGE_MAP reverse lookup."""
        # These map to their CLI stage numbers via STAGE_MAP
        assert _get_stage_num_from_id("01a-initialization") == 1
        assert _get_stage_num_from_id("01b-input-collection") == 2  # Stage 2 in CLI
        assert _get_stage_num_from_id("02a-category-scan") == 4  # Stage 4 in CLI
        assert _get_stage_num_from_id("06a-functional-spec-legacy") == 16  # Stage 16 in CLI

    def test_handles_stage_n_format(self):
        """Should handle stage_N format."""
        assert _get_stage_num_from_id("stage_1") == 1
        assert _get_stage_num_from_id("stage_5") == 5
        assert _get_stage_num_from_id("stage_16") == 16

    def test_returns_zero_for_invalid_format(self):
        """Should return 0 for invalid formats (not None)."""
        assert _get_stage_num_from_id("invalid") == 0
        assert _get_stage_num_from_id("") == 0
        assert _get_stage_num_from_id("unknown-stage") == 0


class TestAutoDetectStageFromState:
    """Tests for _auto_detect_stage_from_state function.

    This is a regression test suite to document and verify the intended behavior
    of treating in_progress stages as effectively completed for auto-detection.
    """

    def test_returns_none_when_workflow_complete(self):
        """Should return None when workflow is marked complete."""
        state = AnalysisState(workflow_complete=True)
        assert _auto_detect_stage_from_state(state) is None

    def test_returns_stage_1_when_no_progress(self):
        """Should return stage 1 when no stages completed."""
        state = AnalysisState()
        assert _auto_detect_stage_from_state(state) == 1

    def test_advances_after_completed_stage(self):
        """Should advance to next stage after completed stage."""
        state = AnalysisState(
            stages_complete=["01a-initialization", "01b-input-collection"],
        )
        # 01a-initialization = stage 1, 01b-input-collection = stage 2
        # Highest completed is 2, next should be 3
        result = _auto_detect_stage_from_state(state)
        assert result == 3  # Highest is 2, next is 3

    def test_in_progress_stage_treated_as_completed_for_advancement(self):
        """REGRESSION TEST: in_progress stages should be treated as completed.

        This is intentional design: when a user runs analyze-project and a stage
        is in_progress, it means they've started that stage and want to advance.
        The AI agent handles resuming incomplete work within its own context.
        """
        state = AnalysisState(
            stages={
                "stage_3": {"status": "in_progress", "started": "2025-01-01T10:00:00"},
            },
            stages_complete=["01a-initialization", "01b-input-collection"],
        )
        # Stage 3 is in_progress - should advance to stage 4
        result = _auto_detect_stage_from_state(state)
        assert result == 4, "in_progress stage should be treated as completed for advancement"

    def test_in_progress_higher_than_completed_advances_correctly(self):
        """REGRESSION TEST: in_progress stage higher than completed stages advances."""
        state = AnalysisState(
            stages={
                "stage_5": {"status": "in_progress"},
            },
            stages_complete=["01a-initialization"],  # Stage 1 completed
        )
        # Stage 5 in_progress should be highest, advance to 6
        result = _auto_detect_stage_from_state(state)
        assert result == 6

    def test_scope_a_branches_correctly_after_stage_8(self):
        """Should branch to stage 9 (Full App) for scope A after stage 8."""
        state = AnalysisState(
            stages_complete=["02e-quality-gates"],  # Stage 8 in STAGE_MAP
            inputs=AnalysisInputs(scope="A"),
        )
        result = _auto_detect_stage_from_state(state)
        assert result == 9  # Full App analysis

    def test_scope_b_branches_correctly_after_stage_8(self):
        """Should branch to stage 10 (Cross-cutting) for scope B after stage 8."""
        state = AnalysisState(
            stages_complete=["02e-quality-gates"],  # Stage 8 in STAGE_MAP
            inputs=AnalysisInputs(scope="B"),
        )
        result = _auto_detect_stage_from_state(state)
        assert result == 10  # Cross-cutting concern analysis

    def test_scope_a_skips_stage_10_after_stage_9(self):
        """Should skip stage 10 and go to 11 after stage 9 for scope A."""
        state = AnalysisState(
            stages_complete=["03a-full-app"],  # Stage 9 in STAGE_MAP
            inputs=AnalysisInputs(scope="A"),
        )
        result = _auto_detect_stage_from_state(state)
        assert result == 11  # Skip cross-cutting, go to reports

    def test_scope_b_continues_to_11_after_stage_10(self):
        """Should continue to stage 11 after stage 10 for scope B."""
        state = AnalysisState(
            stages_complete=["03b-cross-cutting"],  # Stage 10 in STAGE_MAP
            inputs=AnalysisInputs(scope="B"),
        )
        result = _auto_detect_stage_from_state(state)
        assert result == 11

    def test_default_scope_a_when_not_specified(self):
        """Should default to scope A when scope not specified."""
        state = AnalysisState(
            stages_complete=["02e-quality-gates"],  # Stage 8 in STAGE_MAP
            inputs=AnalysisInputs(scope=""),  # Empty scope
        )
        result = _auto_detect_stage_from_state(state)
        assert result == 9  # Default to Full App (scope A)

    def test_mixed_completed_and_in_progress_uses_highest(self):
        """REGRESSION TEST: Mixed states should use highest stage for advancement."""
        state = AnalysisState(
            stages={
                "stage_3": {"status": "completed"},
                "stage_5": {"status": "in_progress"},
                "stage_4": {"status": "completed"},
            },
            stages_complete=["01a-initialization", "02a-category-scan"],
        )
        # Highest: stage 5 (in_progress), should advance to 6
        result = _auto_detect_stage_from_state(state)
        assert result == 6

    def test_chunked_stage_in_progress_returns_same_stage(self):
        """Chunked stages (9, 10, 16) in_progress should return same stage for chunk handling.

        This is critical for Stage 3A (9), Stage 3B (10), and Stage 6 (16) which have
        multiple chunks. When in_progress, the CLI needs to redirect to chunk handling,
        not advance to the next stage.
        """
        # Stage 9 (Full App) in_progress should return 9, not 11
        state = AnalysisState(
            stages={
                "03a-full-app": {"status": "in_progress"},
            },
            stages_complete=["02e-quality-gates"],  # Stage 8 completed
            inputs=AnalysisInputs(scope="A"),
        )
        result = _auto_detect_stage_from_state(state)
        assert result == 9, "Stage 9 in_progress should return 9 for chunk handling"

    def test_chunked_stage_completed_advances_correctly(self):
        """Chunked stages that are completed should advance to next stage."""
        # Stage 9 completed should advance to 11 (skipping 10 for scope A)
        state = AnalysisState(
            stages={
                "03a-full-app": {"status": "completed"},
            },
            stages_complete=["02e-quality-gates", "03a-full-app"],
            inputs=AnalysisInputs(scope="A"),
        )
        result = _auto_detect_stage_from_state(state)
        assert result == 11, "Stage 9 completed should advance to 11"

    def test_scope_b_chunked_stage_in_progress(self):
        """Stage 10 (Cross-cutting) in_progress should return 10 for chunk handling."""
        state = AnalysisState(
            stages={
                "03b-cross-cutting": {"status": "in_progress"},
            },
            stages_complete=["02e-quality-gates"],  # Stage 8 completed
            inputs=AnalysisInputs(scope="B"),
        )
        result = _auto_detect_stage_from_state(state)
        assert result == 10, "Stage 10 in_progress should return 10 for chunk handling"


class TestAnalyzeProjectCorruptedState:
    """Tests for JSON decode error handling in analyze_project command."""

    def test_corrupted_state_with_explicit_analysis_dir(self, tmp_path, capsys):
        """Should emit error with recovery command for corrupted state (explicit dir)."""
        # Setup corrupted state file
        analysis_dir = tmp_path / ".analysis" / "test-run"
        analysis_dir.mkdir(parents=True)
        (analysis_dir / "state.json").write_text("{invalid json content")

        # Call analyze_project with explicit analysis_dir
        with patch('speckit.commands.analyze.emit_error') as mock_emit:
            analyze_project(analysis_dir=str(analysis_dir))

            # Verify error was emitted with recovery command
            mock_emit.assert_called_once()
            call_args = mock_emit.call_args
            assert "Corrupted state file" in call_args[0][0]
            assert "corrupted" in call_args[0][1]
            assert "recovery_cmd" in call_args[1]
            assert "rm" in call_args[1]["recovery_cmd"]

    def test_corrupted_state_in_latest_analysis(self, tmp_path, capsys):
        """Should emit error with recovery command for corrupted state (auto-detect)."""
        # Setup corrupted state file in latest analysis folder
        analysis_dir = tmp_path / ".analysis" / "project-20251225-100000"
        analysis_dir.mkdir(parents=True)
        (analysis_dir / "state.json").write_text("not valid json {{{")

        with patch('speckit.commands.analyze.find_latest_analysis_folder', return_value=analysis_dir):
            with patch('speckit.commands.analyze.emit_error') as mock_emit:
                analyze_project()

                # Verify error was emitted
                mock_emit.assert_called_once()
                call_args = mock_emit.call_args
                assert "Corrupted state file" in call_args[0][0]

    def test_valid_state_loads_successfully(self, tmp_path):
        """Should load valid state without errors."""
        analysis_dir = tmp_path / ".analysis" / "test-run"
        analysis_dir.mkdir(parents=True)

        valid_state = {
            "schema_version": 1,
            "project_path": "/some/path",
            "started": "2025-01-01T10:00:00",
            "stages": {},
            "stages_complete": [],
            "inputs": {"scope": "A"},
            "workflow_complete": False,
        }
        (analysis_dir / "state.json").write_text(json.dumps(valid_state))

        # Should not raise or call emit_error
        with patch('speckit.commands.analyze.emit_error') as mock_emit:
            with patch('speckit.commands.analyze.emit_stage'):
                with patch('speckit.commands.analyze.get_prompt_fragment', return_value="prompt"):
                    with patch('speckit.commands.analyze.render_prompt', return_value="rendered"):
                        # This will try to run the workflow, just verify no corruption error
                        analyze_project(analysis_dir=str(analysis_dir), stage=1)
                        # emit_error might be called for other reasons, but not for corruption
                        for call in mock_emit.call_args_list:
                            assert "Corrupted" not in str(call)


class TestStageProgressionWithInProgress:
    """Integration tests for stage progression with in_progress states."""

    def test_workflow_resumes_after_interruption(self, tmp_path):
        """Simulates workflow resumption after AI agent interruption.

        Scenario: User runs stage 5, AI agent is interrupted mid-run.
        Stage 5 is left as in_progress. User runs again expecting to continue.
        Expected: Should advance to stage 6 (not restart stage 5).
        """
        analysis_dir = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(analysis_dir)
        state = manager.initialize(tmp_path)

        # Simulate completed stages 1-4
        manager.update_stage("01a-initialization", "completed", stage_num=1)
        manager.update_stage("01b-input-collection", "completed", stage_num=2)
        manager.update_stage("01c-script-execution", "completed", stage_num=3)
        manager.update_stage("02a-category-scan", "completed", stage_num=4)

        # Stage 5 interrupted (in_progress)
        manager.update_stage("02b-deep-dive", "in_progress", stage_num=5)

        # Reload state and auto-detect
        state = manager.load()
        next_stage = _auto_detect_stage_from_state(state)

        # Should advance past in_progress stage
        assert next_stage == 6, "Should advance to stage 6 after in_progress stage 5"

    def test_scope_branching_with_in_progress_boundary(self, tmp_path):
        """Tests scope branching when stage 8 is in_progress.

        When stage 8 is in_progress, it should be treated as completed,
        allowing proper scope-based branching to stage 9 or 10.
        """
        analysis_dir = tmp_path / ".analysis" / "test-run"
        manager = AnalysisStateManager(analysis_dir)
        manager.initialize(tmp_path)

        # Complete stages 1-7
        for i in range(1, 8):
            manager.update_stage(f"stage_{i}", "completed", stage_num=i)

        # Stage 8 in_progress with scope B (02e-quality-gates is stage 8 in STAGE_MAP)
        manager.update_stage("02e-quality-gates", "in_progress", stage_num=8)
        manager.update_inputs(scope="B")

        state = manager.load()
        next_stage = _auto_detect_stage_from_state(state)

        # Should branch to stage 10 (cross-cutting) for scope B
        assert next_stage == 10, "Should branch to stage 10 for scope B after in_progress stage 8"
