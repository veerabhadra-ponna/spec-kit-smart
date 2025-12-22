"""
Tests for speckit.core.utils module.
"""

import json
from pathlib import Path
import pytest

from speckit.core.utils import (
    generate_chain_id,
    safe_json_loads,
    safe_json_dumps,
    get_repo_root,
    is_git_repo,
    get_file_info,
    ensure_dir,
    atomic_write,
    get_relative_path,
    count_lines,
)


class TestGenerateChainId:
    """Tests for generate_chain_id function."""

    def test_returns_string(self):
        """Should return a string."""
        result = generate_chain_id()
        assert isinstance(result, str)

    def test_returns_8_chars(self):
        """Should return 8-character hex string."""
        result = generate_chain_id()
        assert len(result) == 8

    def test_is_hex(self):
        """Should be valid hex string."""
        result = generate_chain_id()
        int(result, 16)  # Should not raise

    def test_unique_ids(self):
        """Should generate unique IDs using cryptographically secure random."""
        ids = [generate_chain_id() for _ in range(10)]
        # All should be unique (using secrets.token_hex)
        assert len(set(ids)) == 10


class TestSafeJsonLoads:
    """Tests for safe_json_loads function."""

    def test_valid_json(self):
        """Should parse valid JSON."""
        result = safe_json_loads('{"key": "value"}')
        assert result == {"key": "value"}

    def test_invalid_json_returns_default(self):
        """Should return default for invalid JSON."""
        result = safe_json_loads("not json", default={})
        assert result == {}

    def test_none_default(self):
        """Should return None by default on error."""
        result = safe_json_loads("not json")
        assert result is None

    def test_empty_string(self):
        """Should handle empty string."""
        result = safe_json_loads("", default=[])
        assert result == []

    def test_none_input(self):
        """Should handle None input."""
        result = safe_json_loads(None, default="fallback")
        assert result == "fallback"


class TestSafeJsonDumps:
    """Tests for safe_json_dumps function."""

    def test_valid_object(self):
        """Should serialize valid objects."""
        result = safe_json_dumps({"key": "value"})
        assert json.loads(result) == {"key": "value"}

    def test_handles_path(self):
        """Should handle Path objects via default=str."""
        result = safe_json_dumps({"path": Path("/some/path")})
        parsed = json.loads(result)
        assert parsed["path"] == "/some/path"

    def test_indentation(self):
        """Should respect indentation parameter."""
        result = safe_json_dumps({"a": 1}, indent=4)
        assert "    " in result


class TestGetRepoRoot:
    """Tests for get_repo_root function."""

    def test_in_git_repo(self, tmp_path):
        """Should find git root when in a git repo."""
        # Create a fake git repo
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        subdir = tmp_path / "subdir" / "nested"
        subdir.mkdir(parents=True)

        result = get_repo_root(subdir)
        assert result == tmp_path

    def test_not_in_git_repo(self, tmp_path):
        """Should return cwd as fallback when not in a git repo."""
        result = get_repo_root(tmp_path)
        # Returns Path.cwd() as fallback (no repo markers found)
        assert result is not None


class TestIsGitRepo:
    """Tests for is_git_repo function."""

    def test_in_git_repo(self, tmp_path):
        """Should return True when in a git repo."""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        assert is_git_repo(tmp_path) is True

    def test_not_in_git_repo(self, tmp_path):
        """Should return False when not in a git repo."""
        assert is_git_repo(tmp_path) is False


class TestGetFileInfo:
    """Tests for get_file_info function."""

    def test_existing_file(self, tmp_path):
        """Should return info for existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")

        result = get_file_info(test_file)

        assert result["name"] == "test.txt"
        assert result["extension"] == ".txt"
        assert result["size"] == 5
        assert result["is_file"] is True
        assert result["is_dir"] is False

    def test_nonexistent_file(self, tmp_path):
        """Should return empty dict for nonexistent file."""
        result = get_file_info(tmp_path / "missing.txt")
        assert result == {}

    def test_directory(self, tmp_path):
        """Should handle directory."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        result = get_file_info(subdir)

        assert result["is_file"] is False
        assert result["is_dir"] is True


class TestEnsureDir:
    """Tests for ensure_dir function."""

    def test_creates_directory(self, tmp_path):
        """Should create directory if it doesn't exist."""
        new_dir = tmp_path / "new" / "nested" / "dir"

        result = ensure_dir(new_dir)

        assert new_dir.exists()
        assert new_dir.is_dir()
        assert result == new_dir

    def test_existing_directory(self, tmp_path):
        """Should not fail if directory already exists."""
        existing = tmp_path / "existing"
        existing.mkdir()

        result = ensure_dir(existing)

        assert result == existing
        assert existing.exists()


class TestAtomicWrite:
    """Tests for atomic_write function."""

    def test_writes_content(self, tmp_path):
        """Should write content to file."""
        test_file = tmp_path / "test.txt"

        atomic_write(test_file, "hello world")

        assert test_file.read_text() == "hello world"

    def test_overwrites_existing(self, tmp_path):
        """Should overwrite existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("old content")

        atomic_write(test_file, "new content")

        assert test_file.read_text() == "new content"

    def test_cleans_up_temp_on_success(self, tmp_path):
        """Should not leave temp file after success."""
        test_file = tmp_path / "test.txt"

        atomic_write(test_file, "content")

        temp_file = test_file.with_suffix(".txt.tmp")
        assert not temp_file.exists()


class TestGetRelativePath:
    """Tests for get_relative_path function."""

    def test_relative_path(self, tmp_path):
        """Should return relative path."""
        subfile = tmp_path / "subdir" / "file.txt"

        result = get_relative_path(subfile, tmp_path)

        assert result == "subdir/file.txt" or result == "subdir\\file.txt"

    def test_non_relative_path(self, tmp_path):
        """Should return absolute path if not relative."""
        other_path = Path("/some/other/path")

        result = get_relative_path(other_path, tmp_path)

        assert result == str(other_path)


class TestCountLines:
    """Tests for count_lines function."""

    def test_count_lines(self, tmp_path):
        """Should count lines in file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3")

        result = count_lines(test_file)

        assert result == 3

    def test_empty_file(self, tmp_path):
        """Should return 0 for empty file."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")

        result = count_lines(test_file)

        assert result == 0

    def test_nonexistent_file(self, tmp_path):
        """Should return 0 for nonexistent file."""
        result = count_lines(tmp_path / "missing.txt")
        assert result == 0
