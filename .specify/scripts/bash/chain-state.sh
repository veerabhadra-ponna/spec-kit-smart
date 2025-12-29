#!/usr/bin/env bash
#
# Chain State Management Script
# Manages state for chained prompt workflow
#

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/common.sh"

# Get repository root
REPO_ROOT=$(get_repo_root)

# State directory (always at repo root for consistency)
STATE_DIR="$REPO_ROOT/.analysis/.state"

# Functions

# Generate unique chain ID
generate_chain_id() {
    # Generate 8-character hexadecimal string
    openssl rand -hex 4 2>/dev/null || echo "$(date +%s | md5sum | cut -c1-8)"
}

# Initialize state directory
init_state_dir() {
    mkdir -p "${STATE_DIR}"
    echo "✓ Initialized state directory: ${STATE_DIR}"
}

# Save state to file
# Usage: save_state <stage_name> <state_json>
save_state() {
    local stage_name="$1"
    local state_json="$2"

    # Validate JSON format before saving (prevent injection)
    if ! echo "${state_json}" | jq empty 2>/dev/null; then
        echo "❌ ERROR: Invalid JSON format - cannot save state" >&2
        return 1
    fi

    # Validate state schema (check required fields)
    if ! validate_state "${state_json}"; then
        echo "❌ ERROR: State validation failed - cannot save" >&2
        return 1
    fi

    local state_file="${STATE_DIR}/${stage_name}.json"

    # Write validated JSON safely using jq
    echo "${state_json}" | jq . > "${state_file}"

    # Also save as latest
    echo "${state_json}" | jq . > "${STATE_DIR}/latest.json"

    echo "✓ State saved: ${state_file}"
}

# Load state from file
# Usage: load_state <stage_name>
load_state() {
    local stage_name="$1"
    local state_file="${STATE_DIR}/${stage_name}.json"

    if [[ -f "${state_file}" ]]; then
        cat "${state_file}"
    else
        echo "{}" >&2
        return 1
    fi
}

# Load latest state
load_latest_state() {
    local state_file="${STATE_DIR}/latest.json"

    if [[ -f "${state_file}" ]]; then
        cat "${state_file}"
    else
        echo "{}" >&2
        return 1
    fi
}

# Get last completed stage
get_last_completed_stage() {
    if [[ ! -d "${STATE_DIR}" ]]; then
        echo "none"
        return
    fi

    # Find the highest numbered stage file
    local last_stage=$(ls -1 "${STATE_DIR}"/*.json 2>/dev/null | \
        grep -E '[0-9]{2}[ab]?-.*\.json' | \
        sort -r | \
        head -1 | \
        xargs basename 2>/dev/null || echo "none")

    if [[ "${last_stage}" == "none" ]]; then
        echo "none"
    else
        echo "${last_stage%.json}"
    fi
}

# Check if stage is complete
# Usage: is_stage_complete <stage_name>
is_stage_complete() {
    local stage_name="$1"
    local state_file="${STATE_DIR}/${stage_name}.json"

    [[ -f "${state_file}" ]]
}

# Get chain ID from state
get_chain_id() {
    local state_file="${STATE_DIR}/latest.json"

    if [[ -f "${state_file}" ]]; then
        jq -r '.chain_id // "unknown"' "${state_file}" 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# Create initial state
# Usage: create_initial_state <chain_id>
create_initial_state() {
    local chain_id="$1"
    local timestamp=$(date -Iseconds)

    cat <<EOF
{
  "chain_id": "${chain_id}",
  "start_time": "${timestamp}",
  "timestamp": "${timestamp}",
  "stage": "initialization",
  "stages_complete": [],
  "current_stage": null
}
EOF
}

# Merge states (add new fields to existing state)
# Usage: merge_states <old_state_json> <new_fields_json>
merge_states() {
    local old_state="$1"
    local new_fields="$2"

    # Use jq to merge, with new fields taking precedence
    echo "${old_state}" | jq -s ".[0] * ${new_fields}"
}

# Add stage to completed list
# Usage: mark_stage_complete <state_json> <stage_name>
mark_stage_complete() {
    local state="$1"
    local stage_name="$2"
    local timestamp=$(date -Iseconds)

    echo "${state}" | jq \
        --arg stage "${stage_name}" \
        --arg ts "${timestamp}" \
        '.stages_complete += [$stage] | .timestamp = $ts'
}

# Validate state schema
# Usage: validate_state <state_json>
validate_state() {
    local state="$1"

    # Check required fields
    local chain_id=$(echo "${state}" | jq -r '.chain_id // empty')
    local timestamp=$(echo "${state}" | jq -r '.timestamp // empty')

    if [[ -z "${chain_id}" ]] || [[ -z "${timestamp}" ]]; then
        echo "❌ Invalid state: missing chain_id or timestamp" >&2
        return 1
    fi

    return 0
}

# Main command dispatcher
case "${1:-}" in
    --help|-h|help)
        cat <<EOF
Usage: chain-state.sh <command> [args]

Commands:
  generate-id              Generate unique chain ID
  init                     Initialize state directory
  save <stage> <json>      Save state for stage
  load <stage>             Load state for stage
  load-latest              Load latest state
  last-stage               Get last completed stage
  is-complete <stage>      Check if stage is complete
  chain-id                 Get chain ID from latest state
  init-state <chain_id>    Create initial state
  merge <old> <new>        Merge state objects
  mark-complete <state> <stage>  Mark stage as complete
  validate <json>          Validate state schema

Examples:
  chain-state.sh generate-id
  chain-state.sh init
  chain-state.sh save 01-init '{"chain_id":"abc123",...}'
  chain-state.sh load 01-init
  chain-state.sh last-stage
EOF
        exit 0
        ;;
    generate-id)
        generate_chain_id
        ;;
    init)
        init_state_dir
        ;;
    save)
        save_state "$2" "$3"
        ;;
    load)
        load_state "$2"
        ;;
    load-latest)
        load_latest_state
        ;;
    last-stage)
        get_last_completed_stage
        ;;
    is-complete)
        is_stage_complete "$2" && echo "true" || echo "false"
        ;;
    chain-id)
        get_chain_id
        ;;
    init-state)
        create_initial_state "$2"
        ;;
    merge)
        merge_states "$2" "$3"
        ;;
    mark-complete)
        mark_stage_complete "$2" "$3"
        ;;
    validate)
        validate_state "$2" && echo "✓ Valid state" || echo "❌ Invalid state"
        ;;
    *)
        cat <<EOF
Usage: chain-state.sh <command> [args]

Commands:
  generate-id              Generate unique chain ID
  init                     Initialize state directory
  save <stage> <json>      Save state for stage
  load <stage>             Load state for stage
  load-latest              Load latest state
  last-stage               Get last completed stage
  is-complete <stage>      Check if stage is complete
  chain-id                 Get chain ID from latest state
  init-state <chain_id>    Create initial state
  merge <old> <new>        Merge state objects
  mark-complete <state> <stage>  Mark stage as complete
  validate <json>          Validate state schema

Examples:
  chain-state.sh generate-id
  chain-state.sh init
  chain-state.sh save 01-init '{"chain_id":"abc123",...}'
  chain-state.sh load 01-init
  chain-state.sh last-stage
EOF
        exit 1
        ;;
esac
