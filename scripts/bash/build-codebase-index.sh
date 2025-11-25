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
TOTAL_REST_ENDPOINTS=0
TOTAL_GRAPHQL_RESOLVERS=0
TOTAL_WEBSOCKET_HANDLERS=0
TOTAL_EXTERNAL_APIS=0
TOTAL_ENV_VARS=0
TOTAL_DEPENDENCIES=0
TOTAL_SECRETS_DETECTED=0

# Initialize JSON arrays
CLASSES_JSON="[]"
FUNCTIONS_JSON="[]"
INTERFACES_JSON="[]"
REST_ENDPOINTS_JSON="[]"
GRAPHQL_RESOLVERS_JSON="[]"
WEBSOCKET_HANDLERS_JSON="[]"
EXTERNAL_APIS_JSON="[]"
ENV_VARS_JSON="[]"
DEPENDENCIES_JSON="[]"

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

    # Extract REST API endpoints (Express.js, FastAPI patterns)
    REST_MATCHES=$(grep -n "\\(router\\|app\\)\\.\\(get\\|post\\|put\\|patch\\|delete\\|all\\)(['\"]" "$file" 2>/dev/null || true)
    if [[ -n "$REST_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            METHOD=$(echo "$match" | sed -E "s/.*\\.(get|post|put|patch|delete|all)\\(['\"].*/\\1/" | tr '[:lower:]' '[:upper:]')
            PATH=$(echo "$match" | sed -E "s/.*\\.(?:get|post|put|patch|delete|all)\\(['\"]([^'\"]+)['\"].*/\\1/")

            REST_OBJ=$(jq -n \
                --arg method "$METHOD" \
                --arg path "$PATH" \
                --arg file "$REL_PATH" \
                --argjson line "$LINE_NUM" \
                '{method: $method, path: $path, file: $file, line: $line}')

            REST_ENDPOINTS_JSON=$(echo "$REST_ENDPOINTS_JSON" | jq ". + [$REST_OBJ]")
            TOTAL_REST_ENDPOINTS=$((TOTAL_REST_ENDPOINTS + 1))
        done <<< "$REST_MATCHES"
    fi

    # Extract GraphQL resolvers
    GRAPHQL_MATCHES=$(grep -n "\\(Query\\|Mutation\\|Subscription\\)[[:space:]]*:[[:space:]]*{" "$file" 2>/dev/null || true)
    if [[ -n "$GRAPHQL_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            TYPE=$(echo "$match" | sed -E 's/.*(Query|Mutation|Subscription).*/\1/')

            GRAPHQL_OBJ=$(jq -n \
                --arg type "$TYPE" \
                --arg file "$REL_PATH" \
                --argjson line "$LINE_NUM" \
                '{type: $type, file: $file, line: $line}')

            GRAPHQL_RESOLVERS_JSON=$(echo "$GRAPHQL_RESOLVERS_JSON" | jq ". + [$GRAPHQL_OBJ]")
            TOTAL_GRAPHQL_RESOLVERS=$((TOTAL_GRAPHQL_RESOLVERS + 1))
        done <<< "$GRAPHQL_MATCHES"
    fi

    # Extract WebSocket handlers
    WS_MATCHES=$(grep -n "\\.on(['\"]\\(connection\\|message\\|disconnect\\|error\\)['\"]" "$file" 2>/dev/null || true)
    if [[ -n "$WS_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            EVENT=$(echo "$match" | sed -E "s/.*\\.on\\(['\"]([^'\"]+)['\"].*/\\1/")

            WS_OBJ=$(jq -n \
                --arg event "$EVENT" \
                --arg file "$REL_PATH" \
                --argjson line "$LINE_NUM" \
                '{event: $event, file: $file, line: $line}')

            WEBSOCKET_HANDLERS_JSON=$(echo "$WEBSOCKET_HANDLERS_JSON" | jq ". + [$WS_OBJ]")
            TOTAL_WEBSOCKET_HANDLERS=$((TOTAL_WEBSOCKET_HANDLERS + 1))
        done <<< "$WS_MATCHES"
    fi

    # Extract third-party API integrations (known SDKs)
    KNOWN_SDKS="stripe|aws-sdk|@aws-sdk|firebase|@google-cloud|sendgrid|twilio|mailgun|pusher|socket\\.io-client|axios|fetch|node-fetch|got|request|superagent"
    API_MATCHES=$(grep -in "import.*from ['\"]\\($KNOWN_SDKS\\)" "$file" 2>/dev/null || grep -in "require(['\"]\\($KNOWN_SDKS\\)" "$file" 2>/dev/null || true)
    if [[ -n "$API_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            SERVICE=$(echo "$match" | sed -E "s/.*['\"]([^'\"]+)['\"].*/\\1/" | sed 's/@.*\///' | cut -d'/' -f1)

            API_OBJ=$(jq -n \
                --arg service "$SERVICE" \
                --arg file "$REL_PATH" \
                --argjson line "$LINE_NUM" \
                '{service: $service, file: $file, line: $line}')

            EXTERNAL_APIS_JSON=$(echo "$EXTERNAL_APIS_JSON" | jq ". + [$API_OBJ]")
            TOTAL_EXTERNAL_APIS=$((TOTAL_EXTERNAL_APIS + 1))
        done <<< "$API_MATCHES"
    fi

    # Extract environment variables (API keys, secrets, configs)
    ENV_MATCHES=$(grep -on "process\\.env\\.[A-Z_][A-Z0-9_]*" "$file" 2>/dev/null || true)
    if [[ -n "$ENV_MATCHES" ]]; then
        # Track unique env vars per file to avoid duplicates
        declare -A SEEN_ENV_VARS
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            ENV_VAR=$(echo "$match" | sed -E 's/.*process\.env\.([A-Z_][A-Z0-9_]*).*/\1/')

            # Skip if already seen in this file
            if [[ -n "${SEEN_ENV_VARS[$ENV_VAR]}" ]]; then
                continue
            fi
            SEEN_ENV_VARS[$ENV_VAR]=1

            ENV_OBJ=$(jq -n \
                --arg name "$ENV_VAR" \
                --arg file "$REL_PATH" \
                --argjson line "$LINE_NUM" \
                '{name: $name, file: $file, line: $line}')

            ENV_VARS_JSON=$(echo "$ENV_VARS_JSON" | jq ". + [$ENV_OBJ]")
            TOTAL_ENV_VARS=$((TOTAL_ENV_VARS + 1))
        done <<< "$ENV_MATCHES"
    fi

    # Extract dependencies (imports and requires)
    # Track unique dependencies per file to avoid duplicates
    declare -A SEEN_IMPORTS

    # Extract ES6 imports: import ... from '...'
    IMPORT_MATCHES=$(grep -on "import[[:space:]].*from[[:space:]]*['\"]" "$file" 2>/dev/null || true)
    if [[ -n "$IMPORT_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            IMPORTED_FROM=$(echo "$match" | sed -E "s/.*from[[:space:]]*['\"]([^'\"]+)['\"].*/\1/")

            # Skip if already seen in this file
            if [[ -n "${SEEN_IMPORTS[$IMPORTED_FROM]}" ]]; then
                continue
            fi
            SEEN_IMPORTS[$IMPORTED_FROM]=1

            DEP_OBJ=$(jq -n \
                --arg source_file "$REL_PATH" \
                --arg imported_from "$IMPORTED_FROM" \
                --argjson line "$LINE_NUM" \
                --arg import_type "es6_import" \
                '{source_file: $source_file, imported_from: $imported_from, line: $line, import_type: $import_type}')

            DEPENDENCIES_JSON=$(echo "$DEPENDENCIES_JSON" | jq ". + [$DEP_OBJ]")
            TOTAL_DEPENDENCIES=$((TOTAL_DEPENDENCIES + 1))
        done <<< "$IMPORT_MATCHES"
    fi

    # Extract CommonJS requires: require('...')
    REQUIRE_MATCHES=$(grep -on "require(['\"]" "$file" 2>/dev/null || true)
    if [[ -n "$REQUIRE_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            IMPORTED_FROM=$(echo "$match" | sed -E "s/.*require\\(['\"]([^'\"]+)['\"].*/\1/")

            # Skip if already seen in this file
            if [[ -n "${SEEN_IMPORTS[$IMPORTED_FROM]}" ]]; then
                continue
            fi
            SEEN_IMPORTS[$IMPORTED_FROM]=1

            DEP_OBJ=$(jq -n \
                --arg source_file "$REL_PATH" \
                --arg imported_from "$IMPORTED_FROM" \
                --argjson line "$LINE_NUM" \
                --arg import_type "commonjs_require" \
                '{source_file: $source_file, imported_from: $imported_from, line: $line, import_type: $import_type}')

            DEPENDENCIES_JSON=$(echo "$DEPENDENCIES_JSON" | jq ". + [$DEP_OBJ]")
            TOTAL_DEPENDENCIES=$((TOTAL_DEPENDENCIES + 1))
        done <<< "$REQUIRE_MATCHES"
    fi

    # Extract dynamic imports: import('...')
    DYNAMIC_IMPORT_MATCHES=$(grep -on "import(['\"]" "$file" 2>/dev/null || true)
    if [[ -n "$DYNAMIC_IMPORT_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            IMPORTED_FROM=$(echo "$match" | sed -E "s/.*import\\(['\"]([^'\"]+)['\"].*/\1/")

            # Skip if already seen in this file
            if [[ -n "${SEEN_IMPORTS[$IMPORTED_FROM]}" ]]; then
                continue
            fi
            SEEN_IMPORTS[$IMPORTED_FROM]=1

            DEP_OBJ=$(jq -n \
                --arg source_file "$REL_PATH" \
                --arg imported_from "$IMPORTED_FROM" \
                --argjson line "$LINE_NUM" \
                --arg import_type "dynamic_import" \
                '{source_file: $source_file, imported_from: $imported_from, line: $line, import_type: $import_type}')

            DEPENDENCIES_JSON=$(echo "$DEPENDENCIES_JSON" | jq ". + [$DEP_OBJ]")
            TOTAL_DEPENDENCIES=$((TOTAL_DEPENDENCIES + 1))
        done <<< "$DYNAMIC_IMPORT_MATCHES"
    fi

    # Extract re-exports: export ... from '...'
    REEXPORT_MATCHES=$(grep -on "export[[:space:]].*from[[:space:]]*['\"]" "$file" 2>/dev/null || true)
    if [[ -n "$REEXPORT_MATCHES" ]]; then
        while IFS= read -r match; do
            LINE_NUM=$(echo "$match" | cut -d: -f1)
            IMPORTED_FROM=$(echo "$match" | sed -E "s/.*from[[:space:]]*['\"]([^'\"]+)['\"].*/\1/")

            # Skip if already seen in this file
            if [[ -n "${SEEN_IMPORTS[$IMPORTED_FROM]}" ]]; then
                continue
            fi
            SEEN_IMPORTS[$IMPORTED_FROM]=1

            DEP_OBJ=$(jq -n \
                --arg source_file "$REL_PATH" \
                --arg imported_from "$IMPORTED_FROM" \
                --argjson line "$LINE_NUM" \
                --arg import_type "re_export" \
                '{source_file: $source_file, imported_from: $imported_from, line: $line, import_type: $import_type}')

            DEPENDENCIES_JSON=$(echo "$DEPENDENCIES_JSON" | jq ". + [$DEP_OBJ]")
            TOTAL_DEPENDENCIES=$((TOTAL_DEPENDENCIES + 1))
        done <<< "$REEXPORT_MATCHES"
    fi

    # Detect secrets (count only, don't store in index for security)
    # Pattern 1: API keys, secrets, passwords (KEY=value, SECRET=value, PASSWORD=value)
    SECRET_PATTERN1_MATCHES=$(grep -c -E "(API_KEY|SECRET|PASSWORD|PRIVATE_KEY|AUTH_TOKEN)[[:space:]]*=[[:space:]]*['\"]" "$file" 2>/dev/null || echo "0")
    TOTAL_SECRETS_DETECTED=$((TOTAL_SECRETS_DETECTED + SECRET_PATTERN1_MATCHES))

    # Pattern 2: JWT tokens (eyJ...)
    SECRET_PATTERN2_MATCHES=$(grep -c -E "eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+" "$file" 2>/dev/null || echo "0")
    TOTAL_SECRETS_DETECTED=$((TOTAL_SECRETS_DETECTED + SECRET_PATTERN2_MATCHES))

    # Pattern 3: Bearer/auth tokens in JSON (token: "...", auth: "...", bearer: "...")
    SECRET_PATTERN3_MATCHES=$(grep -c -E "(token|auth|bearer)[[:space:]]*:[[:space:]]*['\"]" "$file" 2>/dev/null || echo "0")
    TOTAL_SECRETS_DETECTED=$((TOTAL_SECRETS_DETECTED + SECRET_PATTERN3_MATCHES))

    # Pattern 4: Hardcoded credentials (username:password patterns, connection strings)
    SECRET_PATTERN4_MATCHES=$(grep -c -E "(postgres|mysql|mongodb)://[^:]+:[^@]+@" "$file" 2>/dev/null || echo "0")
    TOTAL_SECRETS_DETECTED=$((TOTAL_SECRETS_DETECTED + SECRET_PATTERN4_MATCHES))

    # If secrets detected in this file, log warning
    FILE_SECRETS=$((SECRET_PATTERN1_MATCHES + SECRET_PATTERN2_MATCHES + SECRET_PATTERN3_MATCHES + SECRET_PATTERN4_MATCHES))
    if [[ $FILE_SECRETS -gt 0 ]]; then
        log_warn "Detected $FILE_SECRETS potential secret(s) in $REL_PATH (not stored in index)"
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
    --argjson total_rest_endpoints "$TOTAL_REST_ENDPOINTS" \
    --argjson total_graphql_resolvers "$TOTAL_GRAPHQL_RESOLVERS" \
    --argjson total_websocket_handlers "$TOTAL_WEBSOCKET_HANDLERS" \
    --argjson total_external_apis "$TOTAL_EXTERNAL_APIS" \
    --argjson total_env_vars "$TOTAL_ENV_VARS" \
    --argjson total_dependencies "$TOTAL_DEPENDENCIES" \
    --argjson secrets_detected "$TOTAL_SECRETS_DETECTED" \
    '{version: $version, created_by_version: $created_by_version, generated_at: $generated_at, freshness: $freshness, index_type: $index_type, duration_seconds: $duration, statistics: {total_files: $total_files, indexed_files: $indexed_files, skipped_files: $skipped_files, total_classes: $total_classes, total_functions: $total_functions, total_interfaces: $total_interfaces, total_rest_endpoints: $total_rest_endpoints, total_graphql_resolvers: $total_graphql_resolvers, total_websocket_handlers: $total_websocket_handlers, total_external_apis: $total_external_apis, total_env_vars: $total_env_vars, total_dependencies: $total_dependencies, secrets_detected: $secrets_detected}}')

echo "$METADATA_JSON" | jq '.' > "${INDEX_DIR}/metadata.json"

# Write api-endpoints.json
API_ENDPOINTS_JSON=$(jq -n \
    --arg version "1.0" \
    --arg timestamp "$CURRENT_TIMESTAMP" \
    --argjson rest_endpoints "$REST_ENDPOINTS_JSON" \
    --argjson graphql_resolvers "$GRAPHQL_RESOLVERS_JSON" \
    --argjson websocket_handlers "$WEBSOCKET_HANDLERS_JSON" \
    '{version: $version, timestamp: $timestamp, rest_endpoints: $rest_endpoints, graphql_resolvers: $graphql_resolvers, websocket_handlers: $websocket_handlers}')

echo "$API_ENDPOINTS_JSON" | jq '.' > "${INDEX_DIR}/api-endpoints.json"

# Write external-apis.json
EXTERNAL_APIS_FILE_JSON=$(jq -n \
    --arg version "1.0" \
    --arg timestamp "$CURRENT_TIMESTAMP" \
    --argjson third_party_services "$EXTERNAL_APIS_JSON" \
    --argjson environment_variables "$ENV_VARS_JSON" \
    '{version: $version, timestamp: $timestamp, third_party_services: $third_party_services, environment_variables: $environment_variables}')

echo "$EXTERNAL_APIS_FILE_JSON" | jq '.' > "${INDEX_DIR}/external-apis.json"

# Write dependencies.json
DEPENDENCIES_FILE_JSON=$(jq -n \
    --arg version "1.0" \
    --arg timestamp "$CURRENT_TIMESTAMP" \
    --argjson files "$DEPENDENCIES_JSON" \
    '{version: $version, timestamp: $timestamp, files: $files}')

echo "$DEPENDENCIES_FILE_JSON" | jq '.' > "${INDEX_DIR}/dependencies.json"

# Create empty files for other schemas (Phase 1 minimal)
echo '{"version":"1.0","timestamp":"'"$CURRENT_TIMESTAMP"'","database_schemas":[],"orm_entities":[],"type_definitions":[]}' | jq '.' > "${INDEX_DIR}/data-models.json"

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
    echo "✓ REST endpoints: $TOTAL_REST_ENDPOINTS"
    echo "✓ GraphQL resolvers: $TOTAL_GRAPHQL_RESOLVERS"
    echo "✓ WebSocket handlers: $TOTAL_WEBSOCKET_HANDLERS"
    echo "✓ External APIs: $TOTAL_EXTERNAL_APIS"
    echo "✓ Environment variables: $TOTAL_ENV_VARS"
    echo "✓ Dependencies: $TOTAL_DEPENDENCIES"
    if [[ $TOTAL_SECRETS_DETECTED -gt 0 ]]; then
        echo "⚠ Secrets detected: $TOTAL_SECRETS_DETECTED (not stored in index)"
    else
        echo "✓ Secrets detected: 0"
    fi
    echo "✓ Location: $INDEX_DIR"
    echo ""
    echo "Next steps:"
    echo "  - Generate documentation: /speckitsmart.wiki"
    echo "  - Query codebase: /speckitsmart.ask \"your question\""
fi

exit 0
