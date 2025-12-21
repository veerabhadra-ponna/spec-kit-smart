"""
Spec Kit Smart Core Modules

Core infrastructure for state management, configuration, and utilities.
"""

from speckit.core.emit import emit_stage, emit_chunk, emit_complete, emit_error
from speckit.core.state import ChainState
from speckit.core.config import Config
from speckit.core.utils import get_repo_root, detect_os, generate_chain_id

__all__ = [
    "emit_stage",
    "emit_chunk",
    "emit_complete",
    "emit_error",
    "ChainState",
    "Config",
    "get_repo_root",
    "detect_os",
    "generate_chain_id",
]
