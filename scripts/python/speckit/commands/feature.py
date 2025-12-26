"""
Feature creation command for speckitadv.

Creates feature branches and initializes spec directories.
Replaces the bash/PowerShell create-new-feature scripts with full functionality.
"""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel

from speckit.core.state import FeatureMetadata, FeatureStateManager
from speckit.core.utils import find_repo_root

console = Console()

# Default configuration values
DEFAULT_CONFIG = {
    "branching": {
        "prefix": "feature/",
        "pattern": "feature/<num>-<jira>-<shortname>",
        "separator": "-",
        "jira": {
            "required": False,
            "regex": r"^C[0-9]{5}-[0-9]{4}$",
            "format": "C12345-7890",
        },
        "number_format": {
            "digits": 3,
            "zero_padded": True,
        },
        "directory": {
            "includes_prefix": False,
            "base_path": "specs",
        },
    }
}

# Common stop words to filter out when generating short names
STOP_WORDS = {
    "i", "a", "an", "the", "to", "for", "of", "in", "on", "at", "by", "with",
    "from", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "should", "could", "can",
    "may", "might", "must", "shall", "this", "that", "these", "those", "my",
    "your", "our", "their", "want", "need", "add", "get", "set",
}


def load_branch_config(project_root: Path) -> dict:
    """
    Load branching configuration from config file.

    Search order:
    1. memory/config.json (preferred)
    2. .specify/config.json (fallback)

    Falls back to defaults if file doesn't exist or parsing fails.
    """
    # Search paths in priority order
    config_paths = [
        project_root / "memory" / "config.json",
        project_root / ".specify" / "config.json",
    ]

    config_file = None
    for path in config_paths:
        if path.exists():
            config_file = path
            break

    if config_file and config_file.exists():
        try:
            with open(config_file, encoding="utf-8") as f:
                user_config = json.load(f)

            # Deep merge with defaults
            config = DEFAULT_CONFIG.copy()
            if "branching" in user_config:
                branching = user_config["branching"]
                for key in ["prefix", "pattern", "separator"]:
                    if key in branching:
                        config["branching"][key] = branching[key]

                if "jira" in branching:
                    for key in ["required", "regex", "format"]:
                        if key in branching["jira"]:
                            config["branching"]["jira"][key] = branching["jira"][key]

                if "number_format" in branching:
                    for key in ["digits", "zero_padded"]:
                        if key in branching["number_format"]:
                            config["branching"]["number_format"][key] = branching["number_format"][key]

                if "directory" in branching:
                    for key in ["includes_prefix", "base_path"]:
                        if key in branching["directory"]:
                            config["branching"]["directory"][key] = branching["directory"][key]

            return config
        except (json.JSONDecodeError, KeyError):
            pass

    return DEFAULT_CONFIG.copy()


def slugify(text: str) -> str:
    """
    Convert text to a URL-friendly slug.
    """
    slug = text.lower()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


def generate_short_name(description: str) -> str:
    """
    Generate a short name from feature description with smart filtering.

    Matches the original bash script's generate_branch_name function:
    - Filters stop words
    - Keeps words >= 3 chars or uppercase acronyms
    - Returns first 3-4 meaningful words
    """
    # Convert to lowercase and split
    clean = re.sub(r"[^a-z0-9\s]", " ", description.lower())
    words = clean.split()

    # Filter meaningful words
    meaningful = []
    for word in words:
        if not word:
            continue
        # Keep if NOT a stop word AND (length >= 3 OR is uppercase in original)
        if word not in STOP_WORDS:
            if len(word) >= 3:
                meaningful.append(word)
            elif word.upper() in description:
                # Keep short words that appear as uppercase (likely acronyms)
                meaningful.append(word)

    # Use first 3-4 meaningful words
    if meaningful:
        max_words = 4 if len(meaningful) == 4 else 3
        return "-".join(meaningful[:max_words])

    # Fallback to basic slugify
    return slugify(description)[:30]


def validate_jira_number(jira: str, config: dict) -> tuple[bool, str]:
    """
    Validate JIRA number against configured regex.

    Returns:
        Tuple of (is_valid, error_message)
    """
    jira_config = config["branching"]["jira"]
    regex = jira_config["regex"]
    jira_format = jira_config["format"]

    if not re.match(regex, jira):
        return False, f"JIRA number must match format {jira_format} (pattern: {regex})"
    return True, ""


def has_git() -> bool:
    """Check if we're in a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_next_feature_number(specs_dir: Path, config: dict) -> int:
    """
    Find the next available feature number.

    Checks:
    - Remote branches
    - Local branches
    - Existing spec directories

    Uses 3-digit pattern matching to avoid false positives.
    """
    max_num = 0
    digits = config["branching"]["number_format"]["digits"]
    digit_pattern = r"\d{" + str(digits) + r"}"

    # Check spec directories
    if specs_dir.exists():
        for item in specs_dir.iterdir():
            if item.is_dir():
                match = re.match(rf"^({digit_pattern})-", item.name)
                if match:
                    num = int(match.group(1))
                    max_num = max(max_num, num)

    # Check git branches if available
    if has_git():
        try:
            # Fetch latest
            subprocess.run(
                ["git", "fetch", "--all", "--prune"],
                capture_output=True,
                check=False,
            )

            # Check remote branches
            result = subprocess.run(
                ["git", "ls-remote", "--heads", "origin"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    # Match both old pattern (001-name) and new pattern (feature/001-name)
                    match = re.search(rf"refs/heads/(?:feature/)?({digit_pattern})-", line)
                    if match:
                        num = int(match.group(1))
                        max_num = max(max_num, num)

            # Check local branches
            result = subprocess.run(
                ["git", "branch"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    match = re.search(rf"(?:feature/)?({digit_pattern})-", line)
                    if match:
                        num = int(match.group(1))
                        max_num = max(max_num, num)

        except FileNotFoundError:
            pass  # Git not available

    return max_num + 1


def format_feature_number(number: int, config: dict) -> str:
    """Format feature number according to configuration."""
    num_config = config["branching"]["number_format"]
    digits = num_config["digits"]
    zero_padded = num_config["zero_padded"]

    if zero_padded:
        return f"{number:0{digits}d}"
    return str(number)


def build_branch_name(
    feature_num: str,
    short_name: str,
    jira: Optional[str],
    config: dict,
) -> str:
    """
    Build branch name from pattern in configuration.

    Handles placeholders: <num>, <jira>, <shortname>
    """
    pattern = config["branching"]["pattern"]
    separator = config["branching"]["separator"]

    branch_name = pattern
    branch_name = branch_name.replace("<num>", feature_num)
    branch_name = branch_name.replace("<shortname>", short_name)

    if jira:
        branch_name = branch_name.replace("<jira>", jira)
    else:
        # Remove jira placeholder and extra separators
        branch_name = branch_name.replace(f"{separator}<jira>{separator}", separator)
        branch_name = branch_name.replace(f"{separator}<jira>", "")
        branch_name = branch_name.replace(f"<jira>{separator}", "")
        branch_name = branch_name.replace("<jira>", "")

    # GitHub enforces 244-byte limit
    MAX_BRANCH_LENGTH = 244
    if len(branch_name) > MAX_BRANCH_LENGTH:
        console.print(
            f"[yellow]Warning:[/yellow] Branch name exceeds GitHub's 244-byte limit",
            file=console.stderr,
        )
        console.print(
            f"[yellow]Original:[/yellow] {branch_name} ({len(branch_name)} bytes)",
            file=console.stderr,
        )
        # Truncate short_name to fit
        prefix = config["branching"]["prefix"]
        prefix_len = len(prefix) + len(feature_num) + 1
        if jira:
            prefix_len += len(jira) + 1
        max_suffix = MAX_BRANCH_LENGTH - prefix_len
        truncated = short_name[:max_suffix].rstrip("-")

        if jira:
            branch_name = f"{prefix}{feature_num}-{jira}-{truncated}"
        else:
            branch_name = f"{prefix}{feature_num}-{truncated}"

        console.print(
            f"[yellow]Truncated to:[/yellow] {branch_name} ({len(branch_name)} bytes)",
            file=console.stderr,
        )

    return branch_name


def create_git_branch(branch_name: str) -> tuple[bool, str]:
    """
    Create and checkout a new git branch.

    Returns:
        Tuple of (success, message)
    """
    if not has_git():
        return False, "Git repository not detected; skipped branch creation"

    try:
        # Check if branch already exists
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch_name],
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return False, f"Branch '{branch_name}' already exists"

        # Create and checkout branch
        result = subprocess.run(
            ["git", "checkout", "-b", branch_name],
            capture_output=True,
            text=True,
            check=True,
        )
        return True, f"Created and checked out branch: {branch_name}"

    except subprocess.CalledProcessError as e:
        return False, f"Git error: {e.stderr or e.stdout}"


def create_spec_directory(
    project_root: Path,
    branch_name: str,
    feature_num: str,
    short_name: str,
    jira: Optional[str],
    description: str,
    config: dict,
) -> tuple[Path, str]:
    """
    Create spec directory structure and initialize state.

    Template files (spec.md, plan.md, tasks.md) are created by AI during
    the workflow stages, not here. This ensures AI writes complete
    content rather than editing placeholders.

    Returns:
        Tuple of (feature_dir_path, state_file_path)
    """
    dir_config = config["branching"]["directory"]
    base_path = dir_config["base_path"]
    includes_prefix = dir_config["includes_prefix"]
    prefix = config["branching"]["prefix"]

    specs_dir = project_root / base_path
    specs_dir.mkdir(parents=True, exist_ok=True)

    # Build directory name
    if includes_prefix:
        dir_name = branch_name
    else:
        # Remove branch prefix
        dir_name = branch_name.removeprefix(prefix)

    feature_dir = specs_dir / dir_name
    feature_dir.mkdir(parents=True, exist_ok=True)

    # Create checklists directory
    checklists_dir = feature_dir / "checklists"
    checklists_dir.mkdir(exist_ok=True)

    # Initialize feature state
    state_manager = FeatureStateManager(feature_dir)
    metadata = FeatureMetadata(
        short_name=short_name,
        description=description,
        jira=jira,
    )
    state_manager.initialize(metadata)

    # Mark specify as in_progress at stage 3 so auto-detect advances past stages 1-2
    # (create-feature is called during stage 2, so next stage is 3)
    state_manager.update_prompt("specify", "03-branch-setup", "in_progress")

    state_file = feature_dir / ".state" / "state.json"
    return feature_dir, str(state_file)


def run_create_feature(
    description: str,
    jira: Optional[str] = None,
    short_name: Optional[str] = None,
    number: Optional[int] = None,
    no_branch: bool = False,
    output_json: bool = False,
) -> dict:
    """
    Create a new feature with branch, spec directory, and initialized state.

    This is the CLI helper command for AI to call during specify stage 1.
    Returns structured JSON for deterministic folder creation.

    Returns:
        Dictionary with success status, folder path, branch name, and state file.
    """
    # Find project root
    project_root = find_repo_root(Path.cwd())

    # Load configuration
    config = load_branch_config(project_root)
    jira_config = config["branching"]["jira"]

    # Validate JIRA if required
    if jira_config.get("required", False) and not jira:
        error_result = {
            "success": False,
            "error": "JIRA number is required by configuration",
            "jira_format": jira_config.get("format", ""),
        }
        if output_json:
            print(json.dumps(error_result))
        else:
            console.print(
                "[red]Error:[/red] JIRA number is required by configuration",
                file=console.stderr,
            )
            console.print(
                f"Use --jira to specify (format: {jira_config['format']})",
                file=console.stderr,
            )
        return error_result

    # Validate JIRA format if provided
    if jira:
        is_valid, error_msg = validate_jira_number(jira, config)
        if not is_valid:
            # Check if strict format validation is enabled
            if jira_config.get("strict_format", False):
                error_result = {"success": False, "error": error_msg}
                if output_json:
                    print(json.dumps(error_result))
                else:
                    console.print(f"[red]Error:[/red] {error_msg}", file=console.stderr)
                return error_result
            else:
                # Just warn, don't block
                if not output_json:
                    console.print(f"[yellow]Warning:[/yellow] {error_msg}")

    # Generate short name if not provided
    if not short_name:
        short_name = generate_short_name(description)
    else:
        short_name = slugify(short_name)

    # Get next number if not provided
    specs_dir = project_root / config["branching"]["directory"]["base_path"]
    if number is None:
        number = get_next_feature_number(specs_dir, config)

    # Format feature number
    feature_num = format_feature_number(number, config)

    # Build branch name
    branch_name = build_branch_name(feature_num, short_name, jira, config)

    # Create git branch
    branch_created = False
    branch_message = ""
    if not no_branch:
        branch_created, branch_message = create_git_branch(branch_name)

    # Create spec directory and initialize state
    feature_dir, state_file = create_spec_directory(
        project_root=project_root,
        branch_name=branch_name,
        feature_num=feature_num,
        short_name=short_name,
        jira=jira,
        description=description,
        config=config,
    )

    # Set environment variable (for current process, parent shell won't see it)
    os.environ["SPECIFY_FEATURE"] = branch_name

    # Build result
    result = {
        "success": True,
        "folder": str(feature_dir),
        "branch": branch_name,
        "state_file": state_file,
        "feature_num": feature_num,
        "short_name": short_name,
    }

    # Output result
    if output_json:
        print(json.dumps(result))
    else:
        console.print(f"[green][ok][/green] Created feature folder: {feature_dir}")
        console.print(f"  Branch: {branch_name}")
        console.print(f"  State: {state_file}")

        if branch_created:
            console.print(f"  [green][ok][/green] {branch_message}")
        elif not no_branch and branch_message:
            console.print(f"  [yellow]![/yellow] {branch_message}")

    return result
