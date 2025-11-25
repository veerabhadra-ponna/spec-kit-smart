#!/usr/bin/env bash
#
# load-index-for-analysis.sh - Load pre-extracted index data for analyze-project
#
# This script loads data from the codebase index to accelerate analysis:
# - Code structure (classes, functions, interfaces)
# - Data models (database schemas, ORM entities)
# - API endpoints (REST, GraphQL, WebSocket)
# - External integrations (third-party services, env vars)
# - Dependency graph (imports, exports)
#
# Usage: bash load-index-for-analysis.sh [--format json|summary] [--section <section>]
#
# Sections: all, structure, data-models, api-endpoints, external-apis, dependencies
#
# Exit codes:
#   0 - Success
#   1 - Index not found or invalid
#   2 - Invalid arguments
#
# Output: JSON or formatted summary to stdout

set -euo pipefail

# Configuration
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX_DIR="${REPO_ROOT}/.analysis/index"
FORMAT="json"
SECTION="all"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --section)
            SECTION="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--format json|summary] [--section <section>]"
            echo ""
            echo "Sections: all, structure, data-models, api-endpoints, external-apis, dependencies"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 2
            ;;
    esac
done

# Validate format
if [[ "$FORMAT" != "json" && "$FORMAT" != "summary" ]]; then
    echo "Invalid format: $FORMAT. Use 'json' or 'summary'." >&2
    exit 2
fi

# Check if index exists
if [[ ! -d "$INDEX_DIR" ]]; then
    echo '{"error": "Index not found. Run /speckitsmart.index first."}' >&2
    exit 1
fi

# Check if metadata exists
if [[ ! -f "${INDEX_DIR}/metadata.json" ]]; then
    echo '{"error": "Index metadata missing. Run /speckitsmart.index --full to rebuild."}' >&2
    exit 1
fi

# Load section data
load_structure() {
    if [[ -f "${INDEX_DIR}/structure.json" ]]; then
        cat "${INDEX_DIR}/structure.json"
    else
        echo '{"classes": [], "functions": [], "interfaces": []}'
    fi
}

load_data_models() {
    if [[ -f "${INDEX_DIR}/data-models.json" ]]; then
        cat "${INDEX_DIR}/data-models.json"
    else
        echo '{"database_schemas": [], "orm_entities": [], "type_definitions": []}'
    fi
}

load_api_endpoints() {
    if [[ -f "${INDEX_DIR}/api-endpoints.json" ]]; then
        cat "${INDEX_DIR}/api-endpoints.json"
    else
        echo '{"rest_endpoints": [], "graphql_resolvers": [], "websocket_handlers": []}'
    fi
}

load_external_apis() {
    if [[ -f "${INDEX_DIR}/external-apis.json" ]]; then
        cat "${INDEX_DIR}/external-apis.json"
    else
        echo '{"third_party_services": [], "environment_variables": []}'
    fi
}

load_dependencies() {
    if [[ -f "${INDEX_DIR}/dependencies.json" ]]; then
        cat "${INDEX_DIR}/dependencies.json"
    else
        echo '{"files": []}'
    fi
}

load_metadata() {
    cat "${INDEX_DIR}/metadata.json"
}

# Generate summary format
generate_summary() {
    local metadata=$(load_metadata)
    local freshness=$(echo "$metadata" | jq -r '.freshness')
    local index_type=$(echo "$metadata" | jq -r '.index_type')
    local stats=$(echo "$metadata" | jq '.statistics')

    echo "=== Codebase Index Summary ==="
    echo "Generated: $freshness"
    echo "Type: $index_type"
    echo ""
    echo "=== Statistics ==="
    echo "Files indexed: $(echo "$stats" | jq -r '.indexed_files')"
    echo "Classes: $(echo "$stats" | jq -r '.total_classes')"
    echo "Functions: $(echo "$stats" | jq -r '.total_functions')"
    echo "Interfaces: $(echo "$stats" | jq -r '.total_interfaces')"
    echo "REST endpoints: $(echo "$stats" | jq -r '.total_rest_endpoints')"
    echo "GraphQL resolvers: $(echo "$stats" | jq -r '.total_graphql_resolvers')"
    echo "WebSocket handlers: $(echo "$stats" | jq -r '.total_websocket_handlers')"
    echo "External APIs: $(echo "$stats" | jq -r '.total_external_apis')"
    echo "Environment variables: $(echo "$stats" | jq -r '.total_env_vars')"
    echo "Dependencies: $(echo "$stats" | jq -r '.total_dependencies')"
    echo "Database schemas: $(echo "$stats" | jq -r '.total_database_schemas')"
    echo "ORM entities: $(echo "$stats" | jq -r '.total_orm_entities')"
    echo ""

    if [[ "$SECTION" == "all" || "$SECTION" == "structure" ]]; then
        echo "=== Code Structure ==="
        local structure=$(load_structure)
        echo "Classes:"
        echo "$structure" | jq -r '.classes[]? | "  - \(.name) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo "Functions:"
        echo "$structure" | jq -r '.functions[]? | "  - \(.name) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo "Interfaces:"
        echo "$structure" | jq -r '.interfaces[]? | "  - \(.name) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo ""
    fi

    if [[ "$SECTION" == "all" || "$SECTION" == "api-endpoints" ]]; then
        echo "=== API Endpoints ==="
        local endpoints=$(load_api_endpoints)
        echo "REST:"
        echo "$endpoints" | jq -r '.rest_endpoints[]? | "  - [\(.method)] \(.path) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo "GraphQL:"
        echo "$endpoints" | jq -r '.graphql_resolvers[]? | "  - \(.type) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo "WebSocket:"
        echo "$endpoints" | jq -r '.websocket_handlers[]? | "  - \(.event) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo ""
    fi

    if [[ "$SECTION" == "all" || "$SECTION" == "external-apis" ]]; then
        echo "=== External Integrations ==="
        local external=$(load_external_apis)
        echo "Third-party services:"
        echo "$external" | jq -r '.third_party_services[]? | "  - \(.service) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo "Environment variables:"
        echo "$external" | jq -r '.environment_variables[]? | "  - \(.name) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo ""
    fi

    if [[ "$SECTION" == "all" || "$SECTION" == "data-models" ]]; then
        echo "=== Data Models ==="
        local models=$(load_data_models)
        echo "Database schemas:"
        echo "$models" | jq -r '.database_schemas[]? | "  - \(.table) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo "ORM entities:"
        echo "$models" | jq -r '.orm_entities[]? | "  - \(.entity) -> \(.table) (\(.file):\(.line))"' 2>/dev/null || echo "  (none)"
        echo ""
    fi
}

# Generate JSON output
generate_json() {
    case "$SECTION" in
        all)
            jq -n \
                --slurpfile metadata "${INDEX_DIR}/metadata.json" \
                --slurpfile structure "${INDEX_DIR}/structure.json" \
                --slurpfile dataModels "${INDEX_DIR}/data-models.json" \
                --slurpfile apiEndpoints "${INDEX_DIR}/api-endpoints.json" \
                --slurpfile externalApis "${INDEX_DIR}/external-apis.json" \
                --slurpfile dependencies "${INDEX_DIR}/dependencies.json" \
                '{
                    metadata: $metadata[0],
                    structure: $structure[0],
                    data_models: $dataModels[0],
                    api_endpoints: $apiEndpoints[0],
                    external_apis: $externalApis[0],
                    dependencies: $dependencies[0]
                }' 2>/dev/null || {
                    # Fallback if some files are missing
                    echo '{"error": "Some index files are missing. Run /speckitsmart.index --full to rebuild."}'
                    exit 1
                }
            ;;
        structure)
            load_structure
            ;;
        data-models)
            load_data_models
            ;;
        api-endpoints)
            load_api_endpoints
            ;;
        external-apis)
            load_external_apis
            ;;
        dependencies)
            load_dependencies
            ;;
        *)
            echo "Unknown section: $SECTION" >&2
            exit 2
            ;;
    esac
}

# Main execution
if [[ "$FORMAT" == "summary" ]]; then
    generate_summary
else
    generate_json
fi

exit 0
