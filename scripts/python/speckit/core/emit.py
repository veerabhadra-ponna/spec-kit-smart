"""
Stage Emission System

Provides consistent output format for progressive prompt injection.
AI agents parse this output to understand what to do next.
"""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Box drawing characters for consistent output
BOX_TOP = "┌" + "─" * 66 + "┐"
BOX_BOTTOM = "└" + "─" * 66 + "┘"
BOX_SIDE = "│"


def _wrap_content(content: str, width: int = 64) -> list[str]:
    """Wrap content to fit within box."""
    lines = []
    for line in content.split("\n"):
        if len(line) <= width:
            lines.append(line)
        else:
            # Simple word wrap
            words = line.split(" ")
            current = ""
            for word in words:
                if len(current) + len(word) + 1 <= width:
                    current = f"{current} {word}".strip()
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)
    return lines


def _format_box_line(text: str, width: int = 64) -> str:
    """Format a line to fit in the box."""
    return f"{BOX_SIDE} {text:<{width}} {BOX_SIDE}"


def emit_stage(
    stage_num: int,
    total_stages: int,
    title: str,
    content: str,
    next_cmd: str,
    alt_cmd: Optional[str] = None,
    context: Optional[dict] = None,
) -> None:
    """
    Emit a stage prompt for the AI agent to follow.

    Args:
        stage_num: Current stage number (1-indexed)
        total_stages: Total number of stages
        title: Stage title
        content: Instructions for this stage
        next_cmd: Command to run after completing this stage
        alt_cmd: Alternative command (optional)
        context: Context data to include (optional)
    """
    print(BOX_TOP)
    print(_format_box_line(f"STAGE: {stage_num}/{total_stages} - {title}"))
    print(_format_box_line(""))

    for line in _wrap_content(content):
        print(_format_box_line(line))

    if context:
        print(_format_box_line(""))
        print(_format_box_line("Context:"))
        for key, value in context.items():
            print(_format_box_line(f"  {key}: {value}"))

    print(_format_box_line(""))
    print(_format_box_line(f"NEXT: {next_cmd}"))

    if alt_cmd:
        print(_format_box_line(f"  OR: {alt_cmd}"))

    print(BOX_BOTTOM)


def emit_chunk(
    chunk_num: int,
    total_chunks: int,
    title: str,
    content: str,
    file_path: str,
    mode: str,
    line_range: tuple[int, int],
    next_cmd: str,
) -> None:
    """
    Emit a chunk prompt for enforced document chunking.

    NOTE: This function is DISPLAY-ONLY. It prints guidance/instructions to stdout
    for the AI agent to follow. It does NOT write any files. The AI agent is
    responsible for creating the actual artifacts based on the displayed guidance.

    Args:
        chunk_num: Current chunk number (1-indexed)
        total_chunks: Total number of chunks
        title: Chunk title (e.g., "Executive Summary")
        content: Instructions for this chunk
        file_path: Suggested file path (displayed as guidance, not written)
        mode: CREATE or APPEND (guidance for AI)
        line_range: (min_lines, max_lines) expected
        next_cmd: Command to run after completing this chunk
    """
    min_lines, max_lines = line_range

    print(BOX_TOP)
    print(_format_box_line(f"REPORT CHUNK: {chunk_num}/{total_chunks} - {title}"))
    print(_format_box_line(""))
    print(_format_box_line(f"Generate ONLY this section ({min_lines}-{max_lines} lines)."))
    print(_format_box_line(""))

    for line in _wrap_content(content):
        print(_format_box_line(line))

    print(_format_box_line(""))
    print(_format_box_line(f"Write to: {file_path}"))
    print(_format_box_line(f"Mode: {mode}"))
    print(_format_box_line(""))
    print(_format_box_line(f"NEXT: {next_cmd}"))
    print(BOX_BOTTOM)


def emit_complete(
    title: str = "Workflow Complete",
    summary: str = "",
    message: str = "",
    next_steps: Optional[list[str]] = None,
    artifacts: Optional[list[str]] = None,
) -> None:
    """
    Emit workflow completion message.

    Args:
        title: Completion title (displayed in header)
        summary: Brief summary of what was completed
        message: Detailed completion message (legacy, use summary instead)
        next_steps: Optional list of suggested next steps
        artifacts: Optional list of generated artifacts
    """
    # Support both old 'message' and new 'summary' parameter
    display_message = summary or message

    print(BOX_TOP)
    print(_format_box_line(f"COMPLETE: {title}"))
    print(_format_box_line(""))

    for line in _wrap_content(display_message):
        print(_format_box_line(line))

    if artifacts:
        print(_format_box_line(""))
        print(_format_box_line("Generated artifacts:"))
        for artifact in artifacts:
            print(_format_box_line(f"  - {artifact}"))

    if next_steps:
        print(_format_box_line(""))
        print(_format_box_line("Next steps:"))
        for step in next_steps:
            print(_format_box_line(f"  - {step}"))

    print(BOX_BOTTOM)


def emit_error(
    error_type: str,
    message: str,
    recovery_cmd: Optional[str] = None,
    details: Optional[str] = None,
) -> None:
    """
    Emit error message with optional recovery instructions.

    Args:
        error_type: Type of error (e.g., "VALIDATION_ERROR", "STATE_ERROR")
        message: Error message
        recovery_cmd: Optional command to recover
        details: Optional detailed error information
    """
    print(BOX_TOP)
    print(_format_box_line(f"ERROR: {error_type}"))
    print(_format_box_line(""))

    for line in _wrap_content(message):
        print(_format_box_line(line))

    if details:
        print(_format_box_line(""))
        print(_format_box_line("Details:"))
        for line in _wrap_content(details):
            print(_format_box_line(f"  {line}"))

    if recovery_cmd:
        print(_format_box_line(""))
        print(_format_box_line(f"RECOVERY: {recovery_cmd}"))

    print(BOX_BOTTOM)


def emit_template(
    stage_info: dict,
    template_content: str,
    context: dict,
    output_file: str,
) -> None:
    """
    Emit stage with inline template for agent to fill.

    Args:
        stage_info: Dict with num, total, title, next_cmd
        template_content: Template content to include
        context: Data for filling template
        output_file: Where to save filled template
    """
    print(BOX_TOP)
    print(_format_box_line(f"STAGE: {stage_info['num']}/{stage_info['total']} - {stage_info['title']}"))
    print(_format_box_line(""))
    print(_format_box_line(f"Create file: {output_file}"))
    print(_format_box_line(""))
    print(_format_box_line("Use this template:"))
    print(_format_box_line("═" * 60))

    for line in template_content.split("\n"):
        print(_format_box_line(line[:64]))

    print(_format_box_line("═" * 60))
    print(_format_box_line(""))
    print(_format_box_line("Fill with:"))

    for key, value in context.items():
        value_str = str(value)[:50]
        print(_format_box_line(f"  {key}: {value_str}"))

    print(_format_box_line(""))
    print(_format_box_line(f"NEXT: {stage_info['next_cmd']}"))
    print(BOX_BOTTOM)
