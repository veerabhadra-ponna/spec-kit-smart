#!/usr/bin/env bash
# Common functions and variables for all scripts

# Get repository root, with fallback for non-git repositories
get_repo_root() {
    if git rev-parse --show-toplevel >/dev/null 2>&1; then
        git rev-parse --show-toplevel
    else
        # Fall back to script location for non-git repos
        local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        (cd "$script_dir/../../.." && pwd)
    fi
}

# Get current branch, with fallback for non-git repositories
get_current_branch() {
    # First check if SPECIFY_FEATURE environment variable is set
    if [[ -n "${SPECIFY_FEATURE:-}" ]]; then
        echo "$SPECIFY_FEATURE"
        return
    fi

    # Then check git if available
    if git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
        git rev-parse --abbrev-ref HEAD
        return
    fi

    # For non-git repos, try to find the latest feature directory
    local repo_root=$(get_repo_root)
    local specs_dir="$repo_root/specs"

    if [[ -d "$specs_dir" ]]; then
        local latest_feature=""
        local highest=0

        for dir in "$specs_dir"/*; do
            if [[ -d "$dir" ]]; then
                local dirname=$(basename "$dir")
                if [[ "$dirname" =~ ^([0-9]{3})- ]]; then
                    local number=${BASH_REMATCH[1]}
                    number=$((10#$number))
                    if [[ "$number" -gt "$highest" ]]; then
                        highest=$number
                        latest_feature=$dirname
                    fi
                fi
            fi
        done

        if [[ -n "$latest_feature" ]]; then
            echo "$latest_feature"
            return
        fi
    fi

    echo "main"  # Final fallback
}

# Check if we have git available
has_git() {
    git rev-parse --show-toplevel >/dev/null 2>&1
}

check_feature_branch() {
    local branch="$1"
    local has_git_repo="$2"

    # For non-git repos, we can't enforce branch naming but still provide output
    if [[ "$has_git_repo" != "true" ]]; then
        echo "[specify] Warning: Git repository not detected; skipped branch validation" >&2
        return 0
    fi

    if [[ ! "$branch" =~ ^[0-9]{3}- ]]; then
        echo "ERROR: Not on a feature branch. Current branch: $branch" >&2
        echo "Feature branches should be named like: 001-feature-name" >&2
        return 1
    fi

    return 0
}

# Find feature directory - extract folder name from branch name
# Splits branch name by '/' or '\' and takes the last part
# Example: "feature/C12345-6789-new-app" → "C12345-6789-new-app"
find_feature_dir_by_prefix() {
    local repo_root="$1"
    local branch_name="$2"
    local specs_dir="$repo_root/specs"

    # Extract the last part of branch name (after last '/' or '\')
    local folder_name="${branch_name##*/}"     # Remove everything up to last /
    folder_name="${folder_name##*\\}"          # Remove everything up to last \

    # Ensure folder name doesn't contain any slashes (defensive check)
    folder_name="${folder_name//\//\-}"        # Replace / with -
    folder_name="${folder_name//\\/\-}"        # Replace \ with -

    # Return specs/folder_name path
    echo "$specs_dir/$folder_name"
}

get_feature_paths() {
    local repo_root=$(get_repo_root)
    local current_branch=$(get_current_branch)
    local has_git_repo="false"

    if has_git; then
        has_git_repo="true"
    fi

    # Use prefix-based lookup to support multiple branches per spec
    local feature_dir=$(find_feature_dir_by_prefix "$repo_root" "$current_branch")

    cat <<EOF
REPO_ROOT='$repo_root'
CURRENT_BRANCH='$current_branch'
HAS_GIT='$has_git_repo'
FEATURE_DIR='$feature_dir'
FEATURE_SPEC='$feature_dir/spec.md'
IMPL_PLAN='$feature_dir/plan.md'
TASKS='$feature_dir/tasks.md'
RESEARCH='$feature_dir/research.md'
DATA_MODEL='$feature_dir/data-model.md'
QUICKSTART='$feature_dir/quickstart.md'
CONTRACTS_DIR='$feature_dir/contracts'
EOF
}

check_file() { [[ -f "$1" ]] && echo "  [OK] $2" || echo "  [X] $2"; }
check_dir() { [[ -d "$1" && -n $(ls -A "$1" 2>/dev/null) ]] && echo "  [OK] $2" || echo "  [X] $2"; }

# Load Spec Kit configuration from .specify/config.json
# Sets environment variables:
#   SPEC_KIT_OS_ENV - OS override from config ("windows", "unix", "auto")
#   SPEC_KIT_CHECK_ARTIFACTORY - Whether to check artifactory ("true" or "false")
load_spec_kit_config() {
    local repo_root=$(get_repo_root)
    local config_file="$repo_root/.specify/config.json"

    # Defaults
    export SPEC_KIT_OS_ENV="auto"
    export SPEC_KIT_CHECK_ARTIFACTORY="false"

    # Try to read config if exists
    if [[ -f "$config_file" ]]; then
        if command -v jq &> /dev/null; then
            # Use jq if available (preferred) - read from nested workflow structure
            local os_env=$(jq -r '.workflow.osEnv // "auto"' "$config_file" 2>/dev/null)
            local check_art=$(jq -r '.workflow.enableCheckArtifactory // false' "$config_file" 2>/dev/null)

            # Validate osEnv value
            if [[ "$os_env" == "windows" || "$os_env" == "unix" || "$os_env" == "auto" ]]; then
                export SPEC_KIT_OS_ENV="$os_env"
            else
                echo "WARNING: Invalid osEnv value in .specify/config.json: \"$os_env\"" >&2
                echo "Valid values: \"windows\", \"unix\", \"auto\"" >&2
                echo "Falling back to \"auto\" (OS auto-detection)" >&2
                export SPEC_KIT_OS_ENV="auto"
            fi

            export SPEC_KIT_CHECK_ARTIFACTORY="$check_art"
        else
            # Fallback without jq - use grep/sed for simple JSON parsing
            local os_env=$(grep -o '"osEnv"[[:space:]]*:[[:space:]]*"[^"]*"' "$config_file" 2>/dev/null | sed 's/.*"\([^"]*\)".*/\1/')
            local check_art=$(grep -o '"enableCheckArtifactory"[[:space:]]*:[[:space:]]*[a-z]*' "$config_file" 2>/dev/null | sed 's/.*:[[:space:]]*//')

            # Validate and set osEnv
            if [[ "$os_env" == "windows" || "$os_env" == "unix" || "$os_env" == "auto" ]]; then
                export SPEC_KIT_OS_ENV="$os_env"
            elif [[ -n "$os_env" ]]; then
                echo "WARNING: Invalid osEnv value in .specify/config.json: \"$os_env\"" >&2
                echo "Valid values: \"windows\", \"unix\", \"auto\"" >&2
                echo "Falling back to \"auto\" (OS auto-detection)" >&2
            fi

            # Set check_artifactory
            if [[ "$check_art" == "true" ]]; then
                export SPEC_KIT_CHECK_ARTIFACTORY="true"
            fi
        fi
    fi
}

# Detect operating system using config priority:
# 1. Config file (.specify/config.json osEnv)
# 2. Environment variable (SPEC_KIT_PLATFORM)
# 3. Auto-detection (uname or $OS check)
# Returns: "windows" or "unix"
detect_os() {
    # Load config if not already loaded
    if [[ -z "${SPEC_KIT_OS_ENV:-}" ]]; then
        load_spec_kit_config
    fi

    # Priority 1: Config file override
    if [[ "$SPEC_KIT_OS_ENV" == "windows" ]]; then
        echo "windows"
        return
    elif [[ "$SPEC_KIT_OS_ENV" == "unix" ]]; then
        echo "unix"
        return
    fi

    # Priority 2: Environment variable override
    if [[ "${SPEC_KIT_PLATFORM:-}" == "windows" ]]; then
        echo "windows"
        return
    elif [[ "${SPEC_KIT_PLATFORM:-}" == "unix" ]]; then
        echo "unix"
        return
    fi

    # Priority 3: Auto-detect
    if command -v uname &> /dev/null; then
        echo "unix"
    else
        echo "windows"
    fi
}

