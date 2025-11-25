#!/usr/bin/env bash
#
# check-index-prerequisite.sh - Hard prerequisite check for codebase index
# Used by commands that REQUIRE an index to function (e.g., /speckitsmart.wiki, /speckitsmart.ask)
#
# Exit codes:
#   0 - Index exists and is valid
#   1 - Index missing or invalid (command should fail)
#
# Output: JSON to stdout

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
  "error": "Codebase index not found. Run /speckitsmart.index to build it first."
}
EOF
    exit 1
fi

# Check if metadata.json exists
if [[ ! -f "$METADATA_FILE" ]]; then
    cat <<EOF
{
  "index_exists": false,
  "error": "Index metadata missing (corrupted index). Run /speckitsmart.index --full to rebuild."
}
EOF
    exit 1
fi

# Validate metadata.json structure
if ! jq -e '.version and .freshness and .statistics' "$METADATA_FILE" >/dev/null 2>&1; then
    cat <<EOF
{
  "index_exists": false,
  "error": "Invalid index metadata format (corrupted). Run /speckitsmart.index --full to rebuild."
}
EOF
    exit 1
fi

# Extract metadata fields
VERSION=$(jq -r '.version' "$METADATA_FILE")
FRESHNESS=$(jq -r '.freshness' "$METADATA_FILE")
FILES_INDEXED=$(jq -r '.statistics.indexed_files' "$METADATA_FILE")

# Calculate age
AGE_DAYS=$(calculate_age_days "$FRESHNESS")
IS_STALE="false"
if [[ "$AGE_DAYS" -gt 7 ]]; then
    IS_STALE="true"
fi

# Output success JSON
cat <<EOF
{
  "index_exists": true,
  "index_path": "$INDEX_DIR",
  "freshness": "$FRESHNESS",
  "age_days": $AGE_DAYS,
  "is_stale": $IS_STALE,
  "files_indexed": $FILES_INDEXED
}
EOF

exit 0
