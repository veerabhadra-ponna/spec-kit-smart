#!/usr/bin/env bash

set -e

# Get script directory and load common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Auto-detect OS and redirect if needed
OS=$(detect_os)
if [[ "$OS" == "windows" ]]; then
    # Convert bash arguments to PowerShell parameters
    ps_args=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --json)
                ps_args+=("-Json")
                shift
                ;;
            --arguments)
                ps_args+=("-Arguments")
                ps_args+=("$2")
                shift 2
                ;;
            --help|-h)
                ps_args+=("-Help")
                shift
                ;;
            *)
                echo "ERROR: Unknown option '$1'" >&2
                exit 1
                ;;
        esac
    done
    # Safe array expansion (handles empty array with set -u)
    if [[ ${#ps_args[@]} -eq 0 ]]; then
        exec pwsh -File "$SCRIPT_DIR/../powershell/setup-plan.ps1"
    else
        exec pwsh -File "$SCRIPT_DIR/../powershell/setup-plan.ps1" "${ps_args[@]}"
    fi
fi

# Parse command line arguments
JSON_MODE=false
ARGUMENTS=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --json)
            JSON_MODE=true
            shift
            ;;
        --arguments)
            if [[ -z "$2" || "$2" == -* ]]; then
                echo "ERROR: --arguments requires a value" >&2
                exit 1
            fi
            ARGUMENTS="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--json] [--arguments <description>]"
            echo "  --json         Output results in JSON format"
            echo "  --arguments    Optional user description to record in plan template"
            echo "  --help         Show this help message"
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$1'. Use --help for usage information." >&2
            exit 1
            ;;
    esac
done

# Get all paths and variables from common functions
eval $(get_feature_paths)

# Check if we're on a proper feature branch (only for git repos)
check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

# Ensure the feature directory exists
mkdir -p "$FEATURE_DIR"

# Copy plan template if it exists
TEMPLATE="$REPO_ROOT/.specify/templates/plan-template.md"
if [[ -f "$TEMPLATE" ]]; then
    cp "$TEMPLATE" "$IMPL_PLAN"

    # Replace the Input line with user arguments if provided
    if [[ -n "$ARGUMENTS" ]]; then
        # Escape special characters for sed replacement (escape &, \, /, and |)
        ESCAPED_ARGS=$(printf '%s\n' "$ARGUMENTS" | sed 's/[&\/|\\]/\\&/g')
        sed -i.bak "s|\*\*Input\*\*:.*|\*\*Input\*\*: User description: \"$ESCAPED_ARGS\"|" "$IMPL_PLAN"
        rm -f "$IMPL_PLAN.bak"
    fi

    echo "Copied plan template to $IMPL_PLAN"
else
    echo "Warning: Plan template not found at $TEMPLATE"
    # Create a basic plan file if template doesn't exist
    touch "$IMPL_PLAN"
fi

# Output results
if $JSON_MODE; then
    printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s","HAS_GIT":"%s"}\n' \
        "$FEATURE_SPEC" "$IMPL_PLAN" "$FEATURE_DIR" "$CURRENT_BRANCH" "$HAS_GIT"
else
    echo "FEATURE_SPEC: $FEATURE_SPEC"
    echo "IMPL_PLAN: $IMPL_PLAN" 
    echo "SPECS_DIR: $FEATURE_DIR"
    echo "BRANCH: $CURRENT_BRANCH"
    echo "HAS_GIT: $HAS_GIT"
fi

