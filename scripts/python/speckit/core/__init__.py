"""
Spec Kit Smart Core Modules

Core infrastructure for state management, configuration, utilities,
template handling, and prompt fragment system.
"""

from speckit.core.emit import (
    emit_stage,
    emit_chunk,
    emit_complete,
    emit_error,
    emit_template,
)
from speckit.core.state import ChainState
from speckit.core.config import Config
from speckit.core.utils import (
    get_repo_root,
    generate_chain_id,
    safe_json_loads,
    safe_json_dumps,
    run_command,
    is_git_repo,
    get_file_info,
    ensure_dir,
    atomic_write,
    get_relative_path,
    count_lines,
)
from speckit.core.templates import (
    get_embedded_template,
    extract_template,
    template_exists,
    list_templates,
    render_template,
    emit_with_template,
)
from speckit.core.prompts import (
    get_prompt_fragment,
    render_prompt,
    list_fragments,
    get_stage_order,
    fragment_exists,
    get_next_stage,
    count_fragment_lines,
)

__all__ = [
    # Emit system
    "emit_stage",
    "emit_chunk",
    "emit_complete",
    "emit_error",
    "emit_template",
    # State management
    "ChainState",
    # Configuration
    "Config",
    # Utilities
    "get_repo_root",
    "generate_chain_id",
    "safe_json_loads",
    "safe_json_dumps",
    "run_command",
    "is_git_repo",
    "get_file_info",
    "ensure_dir",
    "atomic_write",
    "get_relative_path",
    "count_lines",
    # Templates
    "get_embedded_template",
    "extract_template",
    "template_exists",
    "list_templates",
    "render_template",
    "emit_with_template",
    # Prompts
    "get_prompt_fragment",
    "render_prompt",
    "list_fragments",
    "get_stage_order",
    "fragment_exists",
    "get_next_stage",
    "count_fragment_lines",
]
