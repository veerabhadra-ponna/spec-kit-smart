#!/usr/bin/env bash
#
# check-index-optional.sh - Optional prerequisite check for codebase index
# Used by commands that BENEFIT from index but can work without it (e.g., /speckitsmart.implement)
#
# Unlike the hard prerequisite check, this script:
# - Always exits with 0 (success)
# - Returns JSON with status and recommendations
# - Allows callers to decide whether to proceed without index
#
# Exit codes:
#   0 - Always (soft check doesn't block)
#
# Output: JSON to stdout with status and recommendations

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX_DIR="${REPO_ROOT}/.analysis/index"
METADATA_FILE="${INDEX_DIR}/metadata.json"

# Function to calculate days between two dates
calculate_age_days() {
    local freshness_date="$1"
    local current_date=$(date -u +%s)
    local freshness_epoch=$(date -d "$freshness_date" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$freshness_date" +%s 2>/dev/null || echo "0")

    if [[ "$freshness_epoch" == "0" ]]; then
        echo "0"
        return
    fi

    local diff_seconds=$((current_date - freshness_epoch))
    local diff_days=$((diff_seconds / 86400))
    echo "$diff_days"
}

# Check if index directory exists
if [[ ! -d "$INDEX_DIR" ]]; then
    cat <<EOF
{
  "index_exists": false,
  "index_available": false,
  "status": "missing",
  "recommendation": "Run /speckitsmart.index to enable enhanced features",
  "disabled_features": [
    "Code reusability checks (40-60% potential reuse)",
    "Architecture pattern detection",
    "Similar implementation suggestions",
    "Test example templates"
  ],
  "continue_without_index": true,
  "message": "Index not found. Running without enhanced features."
}
EOF
    exit 0
fi

# Check if metadata.json exists
if [[ ! -f "$METADATA_FILE" ]]; then
    cat <<EOF
{
  "index_exists": false,
  "index_available": false,
  "status": "corrupted",
  "recommendation": "Run /speckitsmart.index --full to rebuild the index",
  "disabled_features": [
    "Code reusability checks",
    "Architecture pattern detection",
    "Similar implementation suggestions"
  ],
  "continue_without_index": true,
  "message": "Index metadata missing (corrupted). Running without enhanced features."
}
EOF
    exit 0
fi

# Validate metadata.json structure
if ! jq -e '.version and .freshness and .statistics' "$METADATA_FILE" >/dev/null 2>&1; then
    cat <<EOF
{
  "index_exists": true,
  "index_available": false,
  "status": "invalid",
  "recommendation": "Run /speckitsmart.index --full to rebuild the index",
  "disabled_features": [
    "Code reusability checks",
    "Architecture pattern detection"
  ],
  "continue_without_index": true,
  "message": "Invalid index format. Running without enhanced features."
}
EOF
    exit 0
fi

# Extract metadata fields
VERSION=$(jq -r '.version' "$METADATA_FILE")
FRESHNESS=$(jq -r '.freshness' "$METADATA_FILE")
FILES_INDEXED=$(jq -r '.statistics.indexed_files' "$METADATA_FILE")
TOTAL_CLASSES=$(jq -r '.statistics.total_classes' "$METADATA_FILE")
TOTAL_FUNCTIONS=$(jq -r '.statistics.total_functions' "$METADATA_FILE")

# Calculate age
AGE_DAYS=$(calculate_age_days "$FRESHNESS")
IS_STALE="false"
STATUS="fresh"
if [[ "$AGE_DAYS" -gt 7 ]]; then
    IS_STALE="true"
    STATUS="stale"
fi

# Output success JSON with full status
if [[ "$IS_STALE" == "true" ]]; then
    cat <<EOF
{
  "index_exists": true,
  "index_available": true,
  "status": "$STATUS",
  "index_path": "$INDEX_DIR",
  "freshness": "$FRESHNESS",
  "age_days": $AGE_DAYS,
  "is_stale": $IS_STALE,
  "files_indexed": $FILES_INDEXED,
  "total_classes": $TOTAL_CLASSES,
  "total_functions": $TOTAL_FUNCTIONS,
  "recommendation": "Consider running /speckitsmart.index --incremental to update",
  "enabled_features": [
    "Code reusability checks",
    "Architecture pattern detection",
    "Similar implementation suggestions",
    "Test example templates"
  ],
  "warning": "Index is $AGE_DAYS days old and may be stale. Results may not reflect recent changes.",
  "continue_without_index": false,
  "message": "Index available but stale. Enhanced features enabled with potential outdated data."
}
EOF
else
    cat <<EOF
{
  "index_exists": true,
  "index_available": true,
  "status": "$STATUS",
  "index_path": "$INDEX_DIR",
  "freshness": "$FRESHNESS",
  "age_days": $AGE_DAYS,
  "is_stale": $IS_STALE,
  "files_indexed": $FILES_INDEXED,
  "total_classes": $TOTAL_CLASSES,
  "total_functions": $TOTAL_FUNCTIONS,
  "enabled_features": [
    "Code reusability checks",
    "Architecture pattern detection",
    "Similar implementation suggestions",
    "Test example templates"
  ],
  "continue_without_index": false,
  "message": "Index available and fresh. All enhanced features enabled."
}
EOF
fi

exit 0
