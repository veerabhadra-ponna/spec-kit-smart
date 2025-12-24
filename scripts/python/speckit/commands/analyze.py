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

    if analysis_dir:
        analysis_dir_path = Path(analysis_dir)
        state_manager = AnalysisStateManager(analysis_dir_path)
        if state_manager.exists():
            state = state_manager.load()
    else:
        # Try to find latest analysis folder
        try:
            analysis_dir_path = find_latest_analysis_folder()
            state_manager = AnalysisStateManager(analysis_dir_path)
            if state_manager.exists():
                state = state_manager.load()
        except FileNotFoundError:
            pass  # No existing analysis - will create new one

    # Auto-detect stage from state if not provided
    if stage is None:
        if state:
            stage = _auto_detect_stage_from_state(state)
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
        project_name = project_path.name
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

    # Load values from state, override with CLI args if provided
    # Scope
    state_scope = None
    state_concern_type = None
    state_context = None
    for stage_name, stage_info in state.stages.items():
        if stage_info.get("scope"):
            state_scope = stage_info.get("scope")
        if stage_info.get("concern_type"):
            state_concern_type = stage_info.get("concern_type")
        if stage_info.get("context"):
            state_context = stage_info.get("context")

    effective_scope = scope or state_scope or "A"
    effective_concern_type = concern_type or state_concern_type or ""
    effective_context = context or state_context or ""
    total_stages = TOTAL_STAGES.get(effective_scope, 16)

    # Resolve implementation values from state
    state_current = ""
    state_target = ""
    for stage_name, stage_info in state.stages.items():
        if stage_info.get("current_impl"):
            state_current = stage_info.get("current_impl")
        if stage_info.get("target_impl"):
            state_target = stage_info.get("target_impl")

    resolved_current = current_impl or state_current or ""
    resolved_target = target_impl or state_target or ""

    # Build context for prompt rendering
    render_context = {
        "analysis_dir": str(analysis_dir_path),
        "stage": stage,
        "total_stages": total_stages,
        "project_path": str(project_path),
        "scope": effective_scope,
        "context": effective_context,
        "concern_type": effective_concern_type,
        # Short names (used in some prompts)
        "current_impl": resolved_current,
        "target_impl": resolved_target,
        # Long names (used in other prompts)
        "current_implementation": resolved_current,
        "target_implementation": resolved_target,
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

    # Save state for this stage
    state_manager.update_stage(
        stage=f"stage_{stage}",
        status="completed",
        artifacts=[],
    )
    # Store additional context in stage info (use resolved values, not raw CLI args)
    state = state_manager.load()
    state.stages[f"stage_{stage}"]["scope"] = effective_scope
    state.stages[f"stage_{stage}"]["context"] = effective_context
    state.stages[f"stage_{stage}"]["concern_type"] = effective_concern_type
    state.stages[f"stage_{stage}"]["current_impl"] = resolved_current
    state.stages[f"stage_{stage}"]["target_impl"] = resolved_target
    state_manager.save(state)

    # Emit the stage prompt
    emit_stage(
        stage_num=stage,
        total_stages=total_stages,
        title=_get_stage_title(stage),
        content=rendered,
        next_cmd=next_cmd,
        context=render_context if stage == 1 else None,  # Show context on first stage
    )

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

    # Determine next command
    # CLI auto-detects stage and analysis_dir from state
    if chunk < total_chunks:
        next_cmd = f"speckitadv analyze-project --chunk={chunk + 1}"
    else:
        # Final chunk - mark stage as completed in state
        state_manager.update_stage(
            stage=f"stage_{stage}",
            status="completed",
            artifacts=[],
        )
        # Store metadata in stage info (matching non-chunked stage behavior)
        state = state_manager.load()
        state.stages[f"stage_{stage}"]["scope"] = context.get("scope", "A")
        state.stages[f"stage_{stage}"]["context"] = context.get("context", "")
        state.stages[f"stage_{stage}"]["concern_type"] = context.get("concern_type", "")
        state.stages[f"stage_{stage}"]["current_impl"] = context.get("current_impl", "")
        state.stages[f"stage_{stage}"]["target_impl"] = context.get("target_impl", "")
        state_manager.save(state)

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


def _auto_detect_stage_from_state(state) -> int:
    """
    Auto-detect the next stage from analysis state.

    Handles scope-aware branching:
    - Scope A: stages 1-8 → 9 (Full App) → 11-16 (skip 10)
    - Scope B: stages 1-8 → 10 (Cross-cutting) → 11-16 (skip 9)

    Returns:
        Stage number to run (1-indexed)
    """
    # Find highest completed stage and scope from state
    highest_completed = 0
    effective_scope = "A"  # Default to scope A
    for stage_name, stage_info in state.stages.items():
        if stage_info.get("status") == "completed":
            # Extract stage number from "stage_N" format
            try:
                stage_num = int(stage_name.split("_")[1])
                highest_completed = max(highest_completed, stage_num)
            except (IndexError, ValueError):
                pass
        # Get scope from any stage that has it stored
        if stage_info.get("scope"):
            effective_scope = stage_info.get("scope")

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
        return 16  # Cap at final stage

    return next_stage


# Export function for CLI
analyze_project = run_analyze_project
