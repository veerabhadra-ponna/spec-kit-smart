"""
Analyze-Project Command

Implements the progressive analysis workflow with enforced chunking.
This is the most complex command with 16 stages and dynamic branching.

Uses folder-based state management via AnalysisStateManager.
Analysis folder pattern: .analysis/{project-name}-{timestamp}
"""

import getpass
from datetime import datetime
from pathlib import Path
from typing import Optional

from speckit.core.emit import emit_stage, emit_chunk, emit_error
from speckit.core.prompts import get_prompt_fragment, render_prompt
from speckit.core.state import AnalysisStateManager, find_latest_analysis_folder


# Stage mapping: numeric stage -> fragment identifier
# Maps to actual files in templates/commands/analyze/
STAGE_MAP = {
    1: "01a-initialization",      # Stage 1.1: Setup
    2: "01b-input-collection",    # Stage 1.2: Input collection
    3: "01c-script-execution",    # Stage 1.3: Script execution
    4: "02a-category-scan",       # Stage 2.1: Category scan
    5: "02b-deep-dive",           # Stage 2.2: Deep dive
    6: "02c-config-analysis",     # Stage 2.3: Config analysis
    7: "02d-test-audit",          # Stage 2.4: Test audit
    8: "02e-quality-gates",       # Stage 2.5: Quality gates
    9: "03a-full-app",            # Stage 3A: Full app analysis (Scope A)
    10: "03b-cross-cutting",      # Stage 3B: Cross-cutting (Scope B)
    11: "04a-report-chunks-1-3",  # Stage 4.1: Report chunks 1-3
    12: "04b-report-chunks-4-6",  # Stage 4.2: Report chunks 4-6
    13: "04c-report-chunks-7-9",  # Stage 4.3: Report chunks 7-9
    14: "04d-report-verification",# Stage 4.4: Report verification
    15: "05a-executive-summary",  # Stage 5: Executive summary
    16: "06-scope-artifacts",     # Stage 6: Scope-specific artifacts
}

# Chunk map for stages that use sub-prompts (Stage 3A has 4 sub-prompts, Stage 3B has 3)
CHUNK_MAP = {
    9: {  # Stage 3A: Full app (4 sub-prompts)
        1: "03a1-questions-part1",
        2: "03a2-questions-part2",
        3: "03a3-validation-scoring",
        4: "03a4-recommendations",
    },
    10: {  # Stage 3B: Cross-cutting (3 sub-prompts)
        1: "03b1-abstraction-assessment",
        2: "03b2-migration-strategy",
        3: "03b3-effort-success",
    },
}

# Stage 16 chunks are scope-specific
STAGE_16_CHUNKS = {
    "A": {  # Full app: 4 sub-prompts for functional/technical specs
        1: "06a-functional-spec-legacy",
        2: "06b-functional-spec-target",
        3: "06c-technical-spec",
        4: "06d-stage-prompts",
    },
    "B": {  # Cross-cutting: 1 sub-prompt for cross-cutting artifacts
        1: "06e-cross-cutting-artifacts",
    },
}

# Total stages by scope
TOTAL_STAGES = {
    "A": 16,  # Full analysis (stages 1-8, 9, 11-16)
    "B": 16,  # Cross-cutting concern (stages 1-8, 10, 11-16)
}


def run_analyze_project(
    stage: Optional[int] = None,
    chunk: Optional[int] = None,
    analysis_dir: Optional[str] = None,
    path: Optional[str] = None,
    scope: Optional[str] = None,
    context: Optional[str] = None,
    concern_type: Optional[str] = None,
    current_impl: Optional[str] = None,
    target_impl: Optional[str] = None,
    verify: bool = False,
) -> None:
    """
    Execute analyze-project workflow at specified stage.

    This function implements progressive prompt injection:
    - Each invocation outputs ONLY the prompt for current stage
    - Prompt is 50-80 lines max (focused, digestible)
    - State is persisted in folder-based state management
    - AI agent runs next command from output

    All arguments are auto-detected from state when not provided.
    Only provide arguments when starting a new workflow or overriding state.

    Args:
        stage: Current workflow stage (1-16). Auto-detected from state if None.
        chunk: Report chunk number for chunked stages
        analysis_dir: Analysis folder path. Auto-detected (latest) if None.
        path: Project path to analyze. Loaded from state if None.
        scope: Analysis scope (A=full, B=cross-cutting). Loaded from state if None.
        context: Additional context
        concern_type: Type of cross-cutting concern. Loaded from state if None.
        current_impl: Current implementation details. Loaded from state if None.
        target_impl: Target implementation details. Loaded from state if None.
        verify: Run verification after final stage completes
    """
    # Try to find existing analysis folder first
    analysis_dir_path = None
    state_manager = None
    state = None

    import json

    if analysis_dir:
        analysis_dir_path = Path(analysis_dir)
        state_manager = AnalysisStateManager(analysis_dir_path)
        if state_manager.exists():
            try:
                state = state_manager.load()
            except json.JSONDecodeError as e:
                emit_error(
                    "Corrupted state file",
                    f"state.json is corrupted: {e}",
                    recovery_cmd=f"rm {analysis_dir_path}/state.json && speckitadv analyze-project --path=<project-path>",
                )
                return
    else:
        # Try to find latest analysis folder
        try:
            analysis_dir_path = find_latest_analysis_folder()
            state_manager = AnalysisStateManager(analysis_dir_path)
            if state_manager.exists():
                try:
                    state = state_manager.load()
                except json.JSONDecodeError as e:
                    emit_error(
                        "Corrupted state file",
                        f"state.json is corrupted: {e}",
                        recovery_cmd=f"rm {analysis_dir_path}/state.json && speckitadv analyze-project --path=<project-path>",
                    )
                    return
        except FileNotFoundError:
            pass  # No existing analysis - will create new one

    # Auto-detect stage from state if not provided
    if stage is None:
        if state:
            stage = _auto_detect_stage_from_state(state)
            # Check if workflow is already complete
            if stage is None:
                from speckit.core.emit import emit_complete
                # Verify expected artifacts exist before declaring complete
                report_path = analysis_dir_path / "analysis-report.md"
                if report_path.exists():
                    emit_complete(
                        title="Analysis Complete",
                        summary="This analysis workflow has already been completed.",
                        artifacts=[str(report_path)],
                        next_steps=["Review the analysis report", "Start a new analysis with --path=<project>"],
                    )
                else:
                    # State says complete but artifacts missing - warn user
                    emit_error(
                        "Incomplete analysis",
                        f"Workflow marked complete but analysis-report.md not found at {report_path}",
                        recovery_cmd=f"speckitadv analyze-project --stage=16 --analysis-dir={analysis_dir_path}",
                    )
                return
        else:
            stage = 1  # New workflow starts at stage 1

    # Determine project path
    if path:
        project_path = Path(path)
    elif state and state.project_path:
        project_path = Path(state.project_path)
    else:
        project_path = Path.cwd()

    # Initialize new workflow if needed
    if stage == 1 and state is None:
        # Stage 1 without existing state = new workflow
        if not project_path.exists():
            emit_error(
                "Project path not found",
                f"Path does not exist: {project_path}",
                recovery_cmd="speckitadv analyze-project --path=<valid-path>",
            )
            return

        # Create new analysis folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        # Use resolve() to get actual directory name (Path(".").name returns empty string)
        project_name = project_path.resolve().name
        analysis_dir_path = Path(".analysis") / f"{project_name}-{timestamp}"
        state_manager = AnalysisStateManager(analysis_dir_path)
        state = state_manager.initialize(project_path)
    elif state is None:
        # Trying to resume but no state found
        emit_error(
            "No analysis found",
            "No analysis in progress. Start a new analysis first.",
            recovery_cmd="speckitadv analyze-project --path=<project-path>",
        )
        return

    # Load values from state.inputs, override with CLI args if provided
    # CLI args take precedence when explicitly provided
    effective_scope = scope or state.inputs.scope or "A"

    # Validate scope - must be A or B
    if effective_scope not in ("A", "B"):
        emit_error(
            "Invalid scope",
            f"Scope must be 'A' (full application) or 'B' (cross-cutting concern), got: {effective_scope}",
            recovery_cmd="speckitadv analyze-project --scope=A",
        )
        return

    effective_concern_type = concern_type or state.inputs.concern_type or ""
    effective_context = context or state.inputs.context or ""
    resolved_current = current_impl or state.inputs.current_impl or ""
    resolved_target = target_impl or state.inputs.target_impl or ""
    total_stages = TOTAL_STAGES.get(effective_scope, 16)

    # Update state.inputs if CLI args provided new values
    if any([scope, context, concern_type, current_impl, target_impl]):
        state_manager.update_inputs(
            scope=effective_scope,
            context=effective_context,
            concern_type=effective_concern_type,
            current_impl=resolved_current,
            target_impl=resolved_target,
        )

    # Build context for prompt rendering using state manager
    # This ensures prompts get consistent values from state.json
    base_context = state_manager.get_context_for_prompt()

    # Merge with stage-specific values
    render_context = {
        **base_context,
        "stage": stage,
        "total_stages": total_stages,
    }

    # Handle chunked stages
    if chunk is not None:
        _emit_chunk_stage(stage, chunk, analysis_dir_path, render_context, state_manager)
        return

    # Get fragment for current stage
    fragment_id = STAGE_MAP.get(stage)
    if not fragment_id:
        emit_error(
            "Invalid stage",
            f"Stage {stage} is not valid for analyze-project",
            recovery_cmd=f"speckitadv analyze-project --stage=1 --path={project_path}",
        )
        return

    # Load and render prompt fragment
    try:
        fragment = get_prompt_fragment("analyze-project", fragment_id)
    except FileNotFoundError:
        # Try alternate path
        try:
            fragment = get_prompt_fragment("analyze", fragment_id)
        except FileNotFoundError:
            emit_error(
                "Fragment not found",
                f"Prompt fragment not found: {fragment_id}",
                recovery_cmd=f"speckitadv analyze-project --stage={stage} --analysis-dir={analysis_dir_path}",
            )
            return

    rendered = render_prompt(fragment, render_context)

    # Determine next command with scope-aware branching
    # Scope A: stages 1-8 → 9 (Full App) → 11-16 (skip 10)
    # Scope B: stages 1-8 → 10 (Cross-cutting) → 11-16 (skip 9)
    if stage < total_stages:
        if stage == 8:
            # After quality gates, branch based on scope
            next_stage = 9 if effective_scope == "A" else 10
        elif stage == 9:
            # After Full App (scope A), skip Cross-cutting
            next_stage = 11
        elif stage == 10:
            # After Cross-cutting (scope B), continue to reports
            next_stage = 11
        else:
            next_stage = stage + 1
    else:
        next_stage = None
    # CLI auto-detects stage and analysis_dir from state - no args needed
    if next_stage:
        next_cmd = "speckitadv analyze-project"
    else:
        next_cmd = None

    # Check if this stage has chunks (report generation)
    # Stage 16 uses scope-specific chunk map
    has_chunks = stage in CHUNK_MAP or stage == 16
    if has_chunks:
        # This stage requires chunking - redirect to chunk 1
        # Need --chunk since auto-detection doesn't handle chunks
        next_cmd = f"speckitadv analyze-project --chunk=1"
        emit_stage(
            stage_num=stage,
            total_stages=total_stages,
            title=_get_stage_title(stage),
            content=f"""This stage requires chunked report generation.

Starting chunked output mode. Each chunk will contain a focused section.

Run the following command to begin:""",
            next_cmd=next_cmd,
        )
        return

    # Complete any previous in_progress stage before starting new one
    # This ensures stages are only marked complete AFTER work is done
    # IMPORTANT: Only complete if it's a DIFFERENT stage (not re-running same stage)
    current_stage_id = STAGE_MAP.get(stage, f"stage_{stage}")
    current_state = state_manager.load()
    for stage_id, stage_info in current_state.stages.items():
        if stage_info.get("status") == "in_progress" and stage_id != current_stage_id:
            state_manager.update_stage(
                stage=stage_id,
                status="completed",
            )
            break

    # Mark current stage as in_progress (not completed yet)
    # Stage will be marked complete when NEXT stage starts
    state_manager.update_stage(
        stage=STAGE_MAP.get(stage, f"stage_{stage}"),
        status="in_progress",
        artifacts=[],
        stage_num=stage,
    )

    # Emit the stage prompt
    emit_stage(
        stage_num=stage,
        total_stages=total_stages,
        title=_get_stage_title(stage),
        content=rendered,
        next_cmd=next_cmd,
        context=render_context if stage == 1 else None,  # Show context on first stage
    )

    # Mark workflow complete when final stage finishes
    if next_cmd is None:
        state_manager.mark_complete()

    # Run verification if this is the final stage and verify flag is set
    if next_cmd is None and verify:
        from speckit.commands.project import verify_analysis_report
        report_path = analysis_dir_path / "analysis-report.md"
        if report_path.exists():
            print("\n")  # Add spacing
            verify_analysis_report(str(report_path))
        else:
            print(f"\n[Note] Verification skipped: report not found at {report_path}")


def _emit_chunk_stage(
    stage: int,
    chunk: int,
    analysis_dir_path: Path,
    context: dict,
    state_manager: AnalysisStateManager,
) -> None:
    """
    Emit a specific chunk of a chunked stage.

    Enforced chunking ensures the AI can't skip chunks.
    Each chunk is a separate command invocation.
    """
    # Get chunk info - stage 16 uses scope-specific chunk map
    if stage == 16:
        effective_scope = context.get("scope", "A")
        chunk_info = STAGE_16_CHUNKS.get(effective_scope, STAGE_16_CHUNKS["A"])
    else:
        chunk_info = CHUNK_MAP.get(stage)

    if not chunk_info:
        emit_error(
            "Stage not chunked",
            f"Stage {stage} does not support chunking",
            recovery_cmd=f"speckitadv analyze-project --stage={stage} --analysis-dir={analysis_dir_path}",
        )
        return

    total_chunks = len(chunk_info)
    if chunk < 1 or chunk > total_chunks:
        emit_error(
            "Invalid chunk",
            f"Chunk {chunk} is not valid (1-{total_chunks})",
            recovery_cmd=f"speckitadv analyze-project --stage={stage} --chunk=1 --analysis-dir={analysis_dir_path}",
        )
        return

    fragment_id = chunk_info.get(chunk)

    # Load fragment and extract chunk-specific content
    try:
        fragment = get_prompt_fragment("analyze", fragment_id)
    except FileNotFoundError:
        emit_error(
            "Fragment not found",
            f"Chunk fragment not found: {fragment_id}",
            recovery_cmd=f"speckitadv analyze-project --stage={stage} --analysis-dir={analysis_dir_path}",
        )
        return

    # Chunk the fragment content
    chunk_content = _extract_chunk(fragment, chunk, total_chunks)
    rendered = render_prompt(chunk_content, context)

    # On chunk 1, complete previous in_progress stage and mark current as in_progress
    # IMPORTANT: Only complete if it's a DIFFERENT stage (not re-running same stage)
    current_stage_id = STAGE_MAP.get(stage, f"stage_{stage}")
    if chunk == 1:
        current_state = state_manager.load()
        for stage_id, stage_info in current_state.stages.items():
            if stage_info.get("status") == "in_progress" and stage_id != current_stage_id:
                state_manager.update_stage(
                    stage=stage_id,
                    status="completed",
                )
                break
        # Mark this chunked stage as in_progress
        state_manager.update_stage(
            stage=current_stage_id,
            status="in_progress",
            artifacts=[],
            stage_num=stage,
        )

    # Determine next command
    # CLI auto-detects stage and analysis_dir from state
    if chunk < total_chunks:
        next_cmd = f"speckitadv analyze-project --chunk={chunk + 1}"
    else:
        # Final chunk - mark stage as completed in state
        state_manager.update_stage(
            stage=STAGE_MAP.get(stage, f"stage_{stage}"),
            status="completed",
            artifacts=[],
            stage_num=stage,
        )

        # Move to next stage with scope-aware branching
        # Scope A: stages 1-8 → 9 (Full App) → 11-16 (skip 10)
        # Scope B: stages 1-8 → 10 (Cross-cutting) → 11-16 (skip 9)
        effective_scope = context.get("scope", "A")
        total_stages = context.get("total_stages", 16)
        if stage < total_stages:
            if stage == 9:
                # After Full App (scope A), skip Cross-cutting
                next_stage = 11
            elif stage == 10:
                # After Cross-cutting (scope B), continue to reports
                next_stage = 11
            else:
                next_stage = stage + 1
        else:
            next_stage = None
        # CLI auto-detects from state - no args needed
        if next_stage:
            next_cmd = "speckitadv analyze-project"
        else:
            next_cmd = None
            # Mark workflow complete when final chunk of final stage finishes
            state_manager.mark_complete()

    # Emit chunk - use analysis_dir from context
    analysis_dir = context.get("analysis_dir", str(analysis_dir_path))
    emit_chunk(
        chunk_num=chunk,
        total_chunks=total_chunks,
        title=f"{_get_stage_title(stage)} - Chunk {chunk}",
        content=rendered,
        file_path=f"{analysis_dir}/stage{stage}-chunk{chunk}.md",
        mode="append" if chunk > 1 else "create",
        line_range=((chunk-1)*50+1, chunk*50),
        next_cmd=next_cmd,
    )


def _extract_chunk(fragment: str, chunk: int, total_chunks: int) -> str:
    """
    Extract a specific chunk from a large fragment.

    Divides content into roughly equal sections.
    """
    lines = fragment.splitlines()
    total_lines = len(lines)

    # Find section boundaries (markdown headers)
    sections = []
    current_section_start = 0

    for i, line in enumerate(lines):
        if line.startswith("## ") or line.startswith("### "):
            if i > current_section_start:
                sections.append((current_section_start, i))
            current_section_start = i

    # Add final section
    if current_section_start < total_lines:
        sections.append((current_section_start, total_lines))

    # Distribute sections across chunks
    if not sections:
        # No sections found - divide by lines
        chunk_size = total_lines // total_chunks
        start = (chunk - 1) * chunk_size
        end = start + chunk_size if chunk < total_chunks else total_lines
        return "\n".join(lines[start:end])

    # Assign sections to chunks
    sections_per_chunk = max(1, len(sections) // total_chunks)
    start_section = (chunk - 1) * sections_per_chunk
    end_section = start_section + sections_per_chunk if chunk < total_chunks else len(sections)

    if start_section >= len(sections):
        return "# Chunk Complete\n\nNo additional content for this chunk."

    start_line = sections[start_section][0]
    end_line = sections[min(end_section, len(sections)) - 1][1] if end_section <= len(sections) else total_lines

    return "\n".join(lines[start_line:end_line])


def _get_stage_title(stage: int) -> str:
    """Get human-readable title for a stage."""
    titles = {
        1: "Initialization",
        2: "Input Collection",
        3: "Script Execution",
        4: "Category Scan",
        5: "Deep Dive Analysis",
        6: "Config Analysis",
        7: "Test Audit",
        8: "Quality Gates",
        9: "Full App Analysis",
        10: "Cross-Cutting Analysis",
        11: "Report Chunks 1-3",
        12: "Report Chunks 4-6",
        13: "Report Chunks 7-9",
        14: "Report Verification",
        15: "Executive Summary",
        16: "Scope Artifacts",
    }
    return titles.get(stage, f"Stage {stage}")


def _auto_detect_stage_from_state(state) -> Optional[int]:
    """
    Auto-detect the next stage from analysis state.

    Uses state.current_stage_num and state.inputs.scope for deterministic behavior.
    Handles scope-aware branching:
    - Scope A: stages 1-8 → 9 (Full App) → 11-16 (skip 10)
    - Scope B: stages 1-8 → 10 (Cross-cutting) → 11-16 (skip 9)

    Returns:
        Stage number to run (1-indexed), or None if workflow is complete
    """
    # Check if workflow is complete - nothing to run
    if state.workflow_complete:
        return None

    # Get scope from state.inputs (primary) or default to A
    effective_scope = state.inputs.scope or "A"

    # Find highest completed stage from stages_complete list
    highest_completed = 0
    for stage_id in state.stages_complete:
        # Extract stage number from stage ID like "01a-initialization" or STAGE_MAP values
        stage_num = _get_stage_num_from_id(stage_id)
        if stage_num:
            highest_completed = max(highest_completed, stage_num)

    # Fallback: check legacy stages dict for backwards compatibility
    if highest_completed == 0:
        for stage_name, stage_info in state.stages.items():
            if stage_info.get("status") == "completed":
                # Handle both "stage_N" and stage ID formats
                try:
                    if stage_name.startswith("stage_"):
                        stage_num = int(stage_name.split("_")[1])
                    else:
                        stage_num = _get_stage_num_from_id(stage_name)
                    if stage_num:
                        highest_completed = max(highest_completed, stage_num)
                except (IndexError, ValueError):
                    pass

    # Apply scope-aware branching logic
    if highest_completed == 8:
        # After quality gates, branch based on scope
        return 9 if effective_scope == "A" else 10
    elif highest_completed == 9:
        # After Full App (scope A), skip Cross-cutting to reports
        return 11
    elif highest_completed == 10:
        # After Cross-cutting (scope B), continue to reports
        return 11

    # Default: next stage after highest completed
    next_stage = highest_completed + 1
    if next_stage > 16:
        return None  # All stages complete

    return next_stage


def _get_stage_num_from_id(stage_id: str) -> int:
    """Extract stage number from stage ID like '01a-initialization' or 'stage_1'.

    Returns:
        Stage number (1-indexed) or 0 if not parseable
    """
    if not stage_id:
        return 0

    # Handle "stage_N" format
    if stage_id.startswith("stage_"):
        try:
            return int(stage_id.split("_")[1])
        except (IndexError, ValueError):
            return 0

    # Reverse lookup from STAGE_MAP
    for num, frag_id in STAGE_MAP.items():
        if frag_id == stage_id:
            return num

    # Try extracting from "01a-...", "02b-...", etc.
    try:
        # Extract first two digits
        prefix = stage_id[:2]
        return int(prefix)
    except (ValueError, IndexError):
        return 0


# Export function for CLI
analyze_project = run_analyze_project
