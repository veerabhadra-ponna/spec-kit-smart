#!/usr/bin/env bash
#
# build-codebase-index.sh - Build searchable codebase index
#
# Usage: bash build-codebase-index.sh [--full|--incremental] [--path <dir>] [--verbose] [--json]
#
# Output: Creates JSON index files in .analysis/index/
#

set -euo pipefail

# Configuration
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX_DIR="${REPO_ROOT}/.analysis/index"
CACHE_DIR="${INDEX_DIR}/cache"
VERBOSE=false
JSON_OUTPUT=false
MODE="auto"
TARGET_PATH="${REPO_ROOT}"
LANGUAGES="ts,tsx,js,jsx,py,java,cs,go"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --full)
            MODE="full"
            shift
            ;;
        --incremental)
            MODE="incremental"
            shift
            ;;
        --path)
            TARGET_PATH="$2"
            shift 2
            ;;
        --languages)
            LANGUAGES="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Logging functions
log_info() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo "[INFO] $*" >&2
    fi
}

log_warn() {
    echo "[WARN] $*" >&2
}

log_error() {
    echo "[ERROR] $*" >&2
}

# Check dependencies
if ! command -v jq >/dev/null 2>&1; then
    log_error "jq is required but not installed."
    echo ""
    echo "Installation instructions:"
    echo "  macOS:   brew install jq"
    echo "  Linux:   apt-get install jq  or  yum install jq"
    echo "  Windows: choco install jq  or download from https://jqlang.github.io/jq/"
    exit 2
fi

# Determine mode
if [[ "$MODE" == "auto" ]]; then
    if [[ -f "${INDEX_DIR}/metadata.json" ]]; then
        MODE="full"
        log_info "No mode specified, defaulting to full rebuild"
    else
        MODE="full"
        log_info "No existing index found, running full build"
    fi
fi

# Check for incremental with no base
if [[ "$MODE" == "incremental" ]] && [[ ! -f "${INDEX_DIR}/metadata.json" ]]; then
    log_warn "No existing index found. Running full index build instead of incremental update."
    MODE="full"
fi

# Create directories
mkdir -p "$INDEX_DIR" "$CACHE_DIR"
chmod 700 "$INDEX_DIR"

START_TIME=$(date +%s)
CURRENT_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log_info "Starting codebase index build ($MODE mode)"
log_info "Target path: $TARGET_PATH"

# Initialize counters
TOTAL_FILES=0
INDEXED_FILES=0
SKIPPED_FILES=0
TOTAL_CLASSES=0
TOTAL_FUNCTIONS=0
TOTAL_INTERFACES=0

# Initialize JSON arrays
CLASSES_JSON="[]"
FUNCTIONS_JSON="[]"
INTERFACES_JSON="[]"

# File extensions map
declare -A LANG_EXTENSIONS
LANG_EXTENSIONS=(
    ["typescript"]="\\.tsx?$"
    ["javascript"]="\\.jsx?$"
    ["python"]="\\.py$"
    ["java"]="\\.java$"
    ["csharp"]="\\.cs$"
    ["go"]="\\.go$"
)

# Build find pattern from languages
FIND_PATTERN=""
IFS=',' read -ra LANG_ARRAY <<< "$LANGUAGES"
for lang in "${LANG_ARRAY[@]}"; do
    case "$lang" in
        ts|tsx)
            FIND_PATTERN="${FIND_PATTERN} -name '*.ts' -o -name '*.tsx' -o"
            ;;
        js|jsx)
            FIND_PATTERN="${FIND_PATTERN} -name '*.js' -o -name '*.jsx' -o"
            ;;
        py)
            FIND_PATTERN="${FIND_PATTERN} -name '*.py' -o"
            ;;
        java)
            FIND_PATTERN="${FIND_PATTERN} -name '*.java' -o"
            ;;
        cs)
            FIND_PATTERN="${FIND_PATTERN} -name '*.cs' -o"
            ;;
        go)
            FIND_PATTERN="${FIND_PATTERN} -name '*.go' -o"
            ;;
    esac
done
# Remove trailing -o
FIND_PATTERN="${FIND_PATTERN% -o}"

# Scan for source files
log_info "Scanning for source files..."
TEMP_FILE_LIST=$(mktemp)

eval "find \"$TARGET_PATH\" -type f \( $FIND_PATTERN \) \
    ! -path '*/node_modules/*' \
    ! -path '*/dist/*' \
    ! -path '*/build/*' \
    ! -path '*/.analysis/*' \
    ! -path '*/.git/*' \
    ! -path '*/vendor/*' \
    ! -path '*/venv/*' \
    > \"$TEMP_FILE_LIST\""

TOTAL_FILES=$(wc -l < "$TEMP_FILE_LIST")
log_info "Found $TOTAL_FILES files to process"

# Process each file
while IFS= read -r file; do
    INDEXED_FILES=$((INDEXED_FILES + 1))
    REL_PATH="${file#$REPO_ROOT/}"

    log_info "Processing: $REL_PATH"

    # Check file size (skip if >10MB)
    FILE_SIZE=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
    if [[ "$FILE_SIZE" -gt 10485760 ]]; then
        log_warn "Skipping large file (>10MB): $REL_PATH"
        SKIPPED_FILES=$((SKIPPED_FILES + 1))
        continue
    fi

    # Extract classes (simple regex for Phase 1)
    CLASS_MATCHES=$(grep -n "^\\s*\\(export \\)\\?class " "$file" 2>/dev/null || true)
    if [[ -n "$CLASS_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            CLASS_NAME=$(echo "$match" | sed -E 's/.*class[[:space:]]+([A-Za-z0-9_]+).*/\1/')

            CLASS_OBJ=$(jq -n \
                --arg name "$CLASS_NAME" \
                --arg file "$REL_PATH" \
                --argjson line "$LINE_NUM" \
                '{name: $name, file: $file, line: $line, methods: []}')

            CLASSES_JSON=$(echo "$CLASSES_JSON" | jq ". + [$CLASS_OBJ]")
            TOTAL_CLASSES=$((TOTAL_CLASSES + 1))
        done <<< "$CLASS_MATCHES"
    fi

    # Extract functions
    FUNC_MATCHES=$(grep -n "^\\s*\\(export \\)\\?function " "$file" 2>/dev/null || true)
    if [[ -n "$FUNC_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            FUNC_NAME=$(echo "$match" | sed -E 's/.*function[[:space:]]+([A-Za-z0-9_]+).*/\1/')

            FUNC_OBJ=$(jq -n \
                --arg name "$FUNC_NAME" \
                --arg file "$REL_PATH" \
                --argjson line "$LINE_NUM" \
                '{name: $name, file: $file, line: $line, parameters: []}')

            FUNCTIONS_JSON=$(echo "$FUNCTIONS_JSON" | jq ". + [$FUNC_OBJ]")
            TOTAL_FUNCTIONS=$((TOTAL_FUNCTIONS + 1))
        done <<< "$FUNC_MATCHES"
    fi

    # Extract interfaces (TypeScript)
    if [[ "$file" =~ \.(ts|tsx)$ ]]; then
        INTERFACE_MATCHES=$(grep -n "^\\s*\\(export \\)\\?interface " "$file" 2>/dev/null || true)
        if [[ -n "$INTERFACE_MATCHES" ]]; then
            while IFS= read -r match; do
                LINE_NUM=$(echo "$match" | cut -d: -f1)
                INTERFACE_NAME=$(echo "$match" | sed -E 's/.*interface[[:space:]]+([A-Za-z0-9_]+).*/\1/')

                INTERFACE_OBJ=$(jq -n \
                    --arg name "$INTERFACE_NAME" \
                    --arg file "$REL_PATH" \
                    --argjson line "$LINE_NUM" \
                    '{name: $name, file: $file, line: $line, fields: []}')

                INTERFACES_JSON=$(echo "$INTERFACES_JSON" | jq ". + [$INTERFACE_OBJ]")
                TOTAL_INTERFACES=$((TOTAL_INTERFACES + 1))
            done <<< "$INTERFACE_MATCHES"
        fi
    fi

done < "$TEMP_FILE_LIST"

rm "$TEMP_FILE_LIST"

# Calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

log_info "Index build completed in ${DURATION} seconds"

# Write structure.json
STRUCTURE_JSON=$(jq -n \
    --arg version "1.0" \
    --arg timestamp "$CURRENT_TIMESTAMP" \
    --argjson classes "$CLASSES_JSON" \
    --argjson functions "$FUNCTIONS_JSON" \
    --argjson interfaces "$INTERFACES_JSON" \
    '{version: $version, timestamp: $timestamp, classes: $classes, functions: $functions, interfaces: $interfaces}')

echo "$STRUCTURE_JSON" | jq '.' > "${INDEX_DIR}/structure.json"

# Write metadata.json
METADATA_JSON=$(jq -n \
    --arg version "1.0" \
    --arg created_by_version "1.0.0" \
    --arg generated_at "$CURRENT_TIMESTAMP" \
    --arg freshness "$CURRENT_TIMESTAMP" \
    --arg index_type "$MODE" \
    --argjson duration "$DURATION" \
    --argjson total_files "$TOTAL_FILES" \
    --argjson indexed_files "$INDEXED_FILES" \
    --argjson skipped_files "$SKIPPED_FILES" \
    --argjson total_classes "$TOTAL_CLASSES" \
    --argjson total_functions "$TOTAL_FUNCTIONS" \
    --argjson total_interfaces "$TOTAL_INTERFACES" \
    '{version: $version, created_by_version: $created_by_version, generated_at: $generated_at, freshness: $freshness, index_type: $index_type, duration_seconds: $duration, statistics: {total_files: $total_files, indexed_files: $indexed_files, skipped_files: $skipped_files, total_classes: $total_classes, total_functions: $total_functions, total_interfaces: $total_interfaces}}')

echo "$METADATA_JSON" | jq '.' > "${INDEX_DIR}/metadata.json"

# Create empty files for other schemas (Phase 1 minimal)
echo '{"version":"1.0","timestamp":"'"$CURRENT_TIMESTAMP"'","database_schemas":[],"orm_entities":[],"type_definitions":[]}' | jq '.' > "${INDEX_DIR}/data-models.json"
echo '{"version":"1.0","timestamp":"'"$CURRENT_TIMESTAMP"'","rest_endpoints":[],"graphql_resolvers":[],"websocket_handlers":[]}' | jq '.' > "${INDEX_DIR}/api-endpoints.json"
echo '{"version":"1.0","timestamp":"'"$CURRENT_TIMESTAMP"'","third_party_services":[],"environment_variables":[]}' | jq '.' > "${INDEX_DIR}/external-apis.json"
echo '{"version":"1.0","timestamp":"'"$CURRENT_TIMESTAMP"'","files":[]}' | jq '.' > "${INDEX_DIR}/dependencies.json"

# Output summary
if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo "$METADATA_JSON" | jq '.'
else
    echo ""
    echo "✓ Index built successfully in ${DURATION} seconds"
    echo "✓ Files indexed: $INDEXED_FILES"
    echo "✓ Classes: $TOTAL_CLASSES"
    echo "✓ Functions: $TOTAL_FUNCTIONS"
    echo "✓ Interfaces: $TOTAL_INTERFACES"
    echo "✓ Location: $INDEX_DIR"
    echo ""
    echo "Next steps:"
    echo "  - Generate documentation: /speckitsmart.wiki"
    echo "  - Query codebase: /speckitsmart.ask \"your question\""
fi

exit 0
