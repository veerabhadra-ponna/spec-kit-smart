"""
Analyze-Project Command

Implements the progressive analysis workflow with enforced chunking.
This is the most complex command with 16 stages and dynamic branching.
"""

from pathlib import Path
from typing import Optional

from speckit.core.emit import emit_stage, emit_chunk, emit_error
from speckit.core.prompts import get_prompt_fragment, render_prompt
from speckit.core.state import ChainState


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
    16: {  # Stage 6: Scope-specific artifacts (5 sub-prompts for A, 1 for B)
        1: "06a-functional-spec-legacy",
        2: "06b-functional-spec-target",
        3: "06c-technical-spec",
        4: "06d-stage-prompts",
        5: "06e-cross-cutting-artifacts",
    },
}

# Total stages by scope
TOTAL_STAGES = {
    "A": 16,  # Full analysis (stages 1-8, 9, 11-16)
    "B": 16,  # Cross-cutting concern (stages 1-8, 10, 11-16)
}


def run_analyze_project(
    stage: int = 1,
    chunk: Optional[int] = None,
    chain_id: Optional[str] = None,
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
    - State is persisted between invocations
    - AI agent runs next command from output

    Args:
        stage: Current workflow stage (1-16)
        chunk: Report chunk number for chunked stages
        chain_id: Chain ID for state persistence
        path: Project path to analyze
        scope: Analysis scope (A=full, B=cross-cutting)
        context: Additional context
        concern_type: Type of cross-cutting concern (for scope B)
        current_impl: Current implementation details
        target_impl: Target implementation details
        verify: Run verification after final stage completes
    """
    # Initialize or load chain state
    if chain_id:
        try:
            state = ChainState.load(chain_id)
        except FileNotFoundError:
            emit_error(
                "Chain state not found",
                f"No state found for chain ID: {chain_id}",
                recovery_cmd=f"speckitadv analyze-project --stage=1 --path={path or '.'}",
            )
            return
    else:
        # New workflow - initialize state
        project_path = Path(path) if path else Path.cwd()
        if not project_path.exists():
            emit_error(
                "Project path not found",
                f"Path does not exist: {project_path}",
                recovery_cmd="speckitadv analyze-project --stage=1 --path=<valid-path>",
            )
            return

        state = ChainState.initialize(project_path)
        chain_id = state.chain_id

    # Determine total stages based on scope
    effective_scope = scope or state.get("scope") or "A"
    total_stages = TOTAL_STAGES.get(effective_scope, 9)

    # Build context for prompt rendering
    analysis_dir = state.analysis_dir
    render_context = {
        "chain_id": chain_id,
        "stage": stage,
        "total_stages": total_stages,
        "project_path": str(state.project_path),
        "analysis_dir": str(analysis_dir) if analysis_dir else "",
        "scope": effective_scope,
        "context": context or state.get("context") or "",
        "concern_type": concern_type or state.get("concern_type") or "",
        "current_impl": current_impl or state.get("current_impl") or "",
        "target_impl": target_impl or state.get("target_impl") or "",
    }

    # Handle chunked stages
    if chunk is not None:
        _emit_chunk_stage(stage, chunk, chain_id, render_context, state)
        return

    # Get fragment for current stage
    fragment_id = STAGE_MAP.get(stage)
    if not fragment_id:
        emit_error(
            "Invalid stage",
            f"Stage {stage} is not valid for analyze-project",
            recovery_cmd=f"speckitadv analyze-project --stage=1 --chain={chain_id}",
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
                recovery_cmd=f"speckitadv analyze-project --stage={stage} --chain={chain_id}",
            )
            return

    rendered = render_prompt(fragment, render_context)

    # Determine next command
    next_stage = stage + 1 if stage < total_stages else None
    if next_stage:
        next_cmd = f"speckitadv analyze-project --stage={next_stage} --chain={chain_id}"
    else:
        next_cmd = None

    # Check if this stage has chunks (report generation)
    if stage in CHUNK_MAP:
        # This stage requires chunking - redirect to chunk 1
        next_cmd = f"speckitadv analyze-project --stage={stage} --chunk=1 --chain={chain_id}"
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
    state.save(
        stage_name=f"stage_{stage}",
        data={
            "stage": stage,
            "scope": effective_scope,
            "context": context,
            "rendered_prompt_lines": len(rendered.splitlines()),
        },
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

    # Run verification if this is the final stage and verify flag is set
    if next_cmd is None and verify:
        from speckit.commands.project import verify_analysis_report
        if analysis_dir:
            report_path = Path(analysis_dir) / "analysis-report.md"
        else:
            report_path = state.project_path / ".analysis" / "analysis-report.md"
        if report_path.exists():
            print("\n")  # Add spacing
            verify_analysis_report(str(report_path))
        else:
            print(f"\n[Note] Verification skipped: report not found at {report_path}")


def _emit_chunk_stage(
    stage: int,
    chunk: int,
    chain_id: str,
    context: dict,
    state: ChainState,
) -> None:
    """
    Emit a specific chunk of a chunked stage.

    Enforced chunking ensures the AI can't skip chunks.
    Each chunk is a separate command invocation.
    """
    chunk_info = CHUNK_MAP.get(stage)
    if not chunk_info:
        emit_error(
            "Stage not chunked",
            f"Stage {stage} does not support chunking",
            recovery_cmd=f"speckitadv analyze-project --stage={stage} --chain={chain_id}",
        )
        return

    total_chunks = len(chunk_info)
    if chunk < 1 or chunk > total_chunks:
        emit_error(
            "Invalid chunk",
            f"Chunk {chunk} is not valid (1-{total_chunks})",
            recovery_cmd=f"speckitadv analyze-project --stage={stage} --chunk=1 --chain={chain_id}",
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
            recovery_cmd=f"speckitadv analyze-project --stage={stage} --chain={chain_id}",
        )
        return

    # Chunk the fragment content
    chunk_content = _extract_chunk(fragment, chunk, total_chunks)
    rendered = render_prompt(chunk_content, context)

    # Determine next command
    if chunk < total_chunks:
        next_cmd = f"speckitadv analyze-project --stage={stage} --chunk={chunk + 1} --chain={chain_id}"
    else:
        # Move to next stage
        next_stage = stage + 1 if stage < context["total_stages"] else None
        if next_stage:
            next_cmd = f"speckitadv analyze-project --stage={next_stage} --chain={chain_id}"
        else:
            next_cmd = None

    # Emit chunk - use analysis_dir if available
    analysis_dir = context.get("analysis_dir", ".analysis")
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


# Export function for CLI
analyze_project = run_analyze_project
