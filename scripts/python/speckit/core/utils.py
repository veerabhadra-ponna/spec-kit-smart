"""
Utility Functions

Common utilities used across the speckit package.
"""

import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any, Optional


def get_repo_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Find the git repository root directory.

    Args:
        start_path: Starting path to search from (defaults to cwd)

    Returns:
        Path to repository root, or None if not in a git repo
    """
    current = start_path or Path.cwd()
    current = current.resolve()

    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent

    return None


def detect_os() -> str:
    """
    Detect the current operating system.

    Returns:
        "windows" or "unix"
    """
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    return "unix"  # Linux, Darwin, FreeBSD, etc.


def generate_chain_id() -> str:
    """
    Generate a unique chain ID (8 hex characters).

    Returns:
        8-character hex string
    """
    timestamp = str(time.time()).encode()
    return hashlib.md5(timestamp).hexdigest()[:8]


def safe_json_loads(text: str, default: Any = None) -> Any:
    """
    Safely parse JSON string.

    Args:
        text: JSON string to parse
        default: Default value if parsing fails

    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, indent: int = 2) -> str:
    """
    Safely serialize object to JSON string.

    Args:
        obj: Object to serialize
        indent: Indentation level

    Returns:
        JSON string
    """
    try:
        return json.dumps(obj, indent=indent, default=str)
    except (TypeError, ValueError):
        return "{}"


def run_command(
    cmd: list[str],
    cwd: Optional[Path] = None,
    capture: bool = True,
    check: bool = True,
) -> Optional[str]:
    """
    Run a shell command.

    Args:
        cmd: Command and arguments
        cwd: Working directory
        capture: Capture output
        check: Raise on non-zero exit

    Returns:
        Command output if capture=True, else None
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            check=check,
        )
        return result.stdout.strip() if capture else None
    except subprocess.CalledProcessError:
        return None


def is_git_repo(path: Optional[Path] = None) -> bool:
    """
    Check if a path is inside a git repository.

    Args:
        path: Path to check (defaults to cwd)

    Returns:
        True if inside a git repo
    """
    check_path = path or Path.cwd()
    return get_repo_root(check_path) is not None


def get_file_info(path: Path) -> dict[str, Any]:
    """
    Get file metadata.

    Args:
        path: Path to file

    Returns:
        Dict with size, modified, extension, etc.
    """
    if not path.exists():
        return {}

    stat = path.stat()
    return {
        "path": str(path),
        "name": path.name,
        "extension": path.suffix.lower(),
        "size": stat.st_size,
        "modified": stat.st_mtime,
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists.

    Args:
        path: Directory path

    Returns:
        The path (for chaining)
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def atomic_write(path: Path, content: str, encoding: str = "utf-8") -> None:
    """
    Atomically write content to a file.

    Writes to a temp file first, then renames to avoid corruption.

    Args:
        path: Target file path
        content: Content to write
        encoding: File encoding
    """
    temp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        temp_path.write_text(content, encoding=encoding)
        temp_path.replace(path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def get_relative_path(path: Path, base: Optional[Path] = None) -> str:
    """
    Get relative path from base directory.

    Args:
        path: Path to convert
        base: Base directory (defaults to cwd)

    Returns:
        Relative path string
    """
    base = base or Path.cwd()
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def count_lines(path: Path) -> int:
    """
    Count lines in a file.

    Args:
        path: Path to file

    Returns:
        Number of lines
    """
    if not path.exists() or not path.is_file():
        return 0

    try:
        return len(path.read_text().splitlines())
    except Exception:
        return 0
