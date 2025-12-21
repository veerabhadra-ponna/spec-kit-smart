"""
Configuration Management

Loads configuration from memory/config.json and environment variables.
"""

import json
import os
import platform
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from speckit.core.utils import get_repo_root


class WorkflowConfig(BaseModel):
    """Workflow configuration options."""

    os_env: str = "auto"  # auto, windows, unix
    enable_check_artifactory: bool = True


class SpecKitConfig(BaseModel):
    """Main configuration schema."""

    model_config = ConfigDict(extra="allow")

    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)


class Config:
    """
    Configuration manager for Spec Kit.

    Loads from:
    1. memory/config.json (preferred - new location)
    2. .specify/config.json (legacy fallback)
    3. Environment variables (override)
    """

    def __init__(self, config_path: Optional[Path] = None):
        self._config_path = config_path
        self._config: SpecKitConfig = SpecKitConfig()
        self._load()

    def _load(self) -> None:
        """Load configuration from file and environment."""
        # Try to find config file
        if self._config_path is None:
            repo_root = self._find_repo_root()

            # Search paths in priority order (memory/ is preferred)
            search_paths = []
            if repo_root:
                search_paths.append(repo_root / "memory" / "config.json")
                search_paths.append(repo_root / ".specify" / "config.json")
            search_paths.append(Path.cwd() / "memory" / "config.json")
            search_paths.append(Path.cwd() / ".specify" / "config.json")
            search_paths.append(Path.cwd() / "config.json")

            for path in search_paths:
                if path.exists():
                    self._config_path = path
                    break

        # Load from file if found
        if self._config_path and self._config_path.exists():
            try:
                data = json.loads(self._config_path.read_text())
                self._config = SpecKitConfig(**data)
            except (json.JSONDecodeError, Exception):
                pass  # Use defaults

        # Apply environment overrides
        self._apply_env_overrides()

    def _find_repo_root(self) -> Path:
        """Find git repository root using shared utility."""
        return get_repo_root()

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # OS environment override
        os_env = os.getenv("SPEC_KIT_OS_ENV") or os.getenv("SPEC_KIT_PLATFORM")
        if os_env:
            self._config.workflow.os_env = os_env

        # Artifactory check override
        check_artifactory = os.getenv("SPEC_KIT_CHECK_ARTIFACTORY")
        if check_artifactory is not None:
            self._config.workflow.enable_check_artifactory = (
                check_artifactory.lower() in ("true", "1", "yes")
            )

    @property
    def os_env(self) -> str:
        """Get the configured OS environment."""
        env = self._config.workflow.os_env
        if env == "auto":
            return self.detect_os()
        return env

    @staticmethod
    def detect_os() -> str:
        """Detect the current operating system."""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        return "unix"  # Linux, Darwin, etc.

    @property
    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return self.os_env == "windows"

    @property
    def is_unix(self) -> bool:
        """Check if running on Unix-like system."""
        return self.os_env == "unix"

    @property
    def check_artifactory(self) -> bool:
        """Check if artifactory checks are enabled."""
        return self._config.workflow.enable_check_artifactory

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key."""
        parts = key.split(".")
        value: Any = self._config.model_dump()

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default

        return value

    def to_dict(self) -> dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.model_dump()
