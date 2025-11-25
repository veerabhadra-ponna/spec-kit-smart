#!/usr/bin/env bash
#
# generate-deepwiki.sh - Generate comprehensive DeepWiki documentation
#
# This script generates 4-tier documentation from the codebase index:
# - Tier 1: Overview (overview.md)
# - Tier 2: Functional Summary (functional-summary.md)
# - Tier 3: Architecture diagrams (architecture/*.md)
# - Tier 4: Detailed module docs (modules/*.md)
#
# Also generates:
# - API Reference (api-reference/*.md)
# - Data Models documentation (data-models/*.md)
# - Mermaid diagrams for visualizations
#
# Usage: bash generate-deepwiki.sh [--tiers <list>] [--output <dir>] [--verbose]
#
# Exit codes:
#   0 - Success
#   1 - Index not found or invalid
#   2 - Invalid arguments
#

set -euo pipefail

# Configuration
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX_DIR="${REPO_ROOT}/.analysis/index"
OUTPUT_DIR="${REPO_ROOT}/.deepwiki"
TIERS="1,2,3,4"
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --tiers)
            TIERS="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--tiers <list>] [--output <dir>] [--verbose]"
            echo ""
            echo "Options:"
            echo "  --tiers <list>    Comma-separated tier numbers (default: 1,2,3,4)"
            echo "  --output <dir>    Output directory (default: .deepwiki)"
            echo "  --verbose         Show detailed progress"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 2
            ;;
    esac
done

# Logging
log_info() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo "[INFO] $*" >&2
    fi
}

log_error() {
    echo "[ERROR] $*" >&2
}

# Check prerequisites
if [[ ! -d "$INDEX_DIR" ]]; then
    log_error "Codebase index not found. Run /speckitsmart.index first."
    exit 1
fi

if [[ ! -f "${INDEX_DIR}/metadata.json" ]]; then
    log_error "Index metadata missing. Run /speckitsmart.index --full to rebuild."
    exit 1
fi

# Create output directory structure
log_info "Creating output directory: $OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/architecture"
mkdir -p "$OUTPUT_DIR/modules"
mkdir -p "$OUTPUT_DIR/api-reference"
mkdir -p "$OUTPUT_DIR/data-models"

CURRENT_DATE=$(date +"%Y-%m-%d")
PROJECT_NAME=$(basename "$REPO_ROOT")

# Load index data
log_info "Loading index data..."
METADATA=$(cat "${INDEX_DIR}/metadata.json")
STRUCTURE=$(cat "${INDEX_DIR}/structure.json")
API_ENDPOINTS=$(cat "${INDEX_DIR}/api-endpoints.json")
EXTERNAL_APIS=$(cat "${INDEX_DIR}/external-apis.json")
DATA_MODELS=$(cat "${INDEX_DIR}/data-models.json")
DEPENDENCIES=$(cat "${INDEX_DIR}/dependencies.json")

# Extract statistics
TOTAL_FILES=$(echo "$METADATA" | jq -r '.statistics.indexed_files // 0')
TOTAL_CLASSES=$(echo "$METADATA" | jq -r '.statistics.total_classes // 0')
TOTAL_FUNCTIONS=$(echo "$METADATA" | jq -r '.statistics.total_functions // 0')
TOTAL_INTERFACES=$(echo "$METADATA" | jq -r '.statistics.total_interfaces // 0')
TOTAL_REST=$(echo "$METADATA" | jq -r '.statistics.total_rest_endpoints // 0')
TOTAL_GRAPHQL=$(echo "$METADATA" | jq -r '.statistics.total_graphql_resolvers // 0')
TOTAL_WEBSOCKET=$(echo "$METADATA" | jq -r '.statistics.total_websocket_handlers // 0')
TOTAL_EXTERNAL=$(echo "$METADATA" | jq -r '.statistics.total_external_apis // 0')
TOTAL_ENV_VARS=$(echo "$METADATA" | jq -r '.statistics.total_env_vars // 0')
TOTAL_DB_SCHEMAS=$(echo "$METADATA" | jq -r '.statistics.total_database_schemas // 0')
TOTAL_ORM=$(echo "$METADATA" | jq -r '.statistics.total_orm_entities // 0')

#=============================================================================
# Tier 1: Overview
#=============================================================================
generate_tier1() {
    log_info "Generating Tier 1: Overview..."

    cat > "${OUTPUT_DIR}/overview.md" << EOF
# ${PROJECT_NAME} - Codebase Overview

> Auto-generated documentation from codebase index
> Generated: ${CURRENT_DATE}

## Quick Statistics

| Metric | Count |
|--------|-------|
| Files Indexed | ${TOTAL_FILES} |
| Classes | ${TOTAL_CLASSES} |
| Functions | ${TOTAL_FUNCTIONS} |
| Interfaces | ${TOTAL_INTERFACES} |
| REST Endpoints | ${TOTAL_REST} |
| GraphQL Resolvers | ${TOTAL_GRAPHQL} |
| WebSocket Handlers | ${TOTAL_WEBSOCKET} |
| External APIs | ${TOTAL_EXTERNAL} |
| Environment Variables | ${TOTAL_ENV_VARS} |
| Database Schemas | ${TOTAL_DB_SCHEMAS} |
| ORM Entities | ${TOTAL_ORM} |

## Project Structure

This codebase contains:

$(if [[ "$TOTAL_CLASSES" -gt 0 ]]; then echo "- **${TOTAL_CLASSES} classes** defining core business logic"; fi)
$(if [[ "$TOTAL_FUNCTIONS" -gt 0 ]]; then echo "- **${TOTAL_FUNCTIONS} functions** implementing various operations"; fi)
$(if [[ "$TOTAL_INTERFACES" -gt 0 ]]; then echo "- **${TOTAL_INTERFACES} interfaces** defining contracts and types"; fi)
$(if [[ "$TOTAL_REST" -gt 0 ]]; then echo "- **${TOTAL_REST} REST endpoints** exposing API functionality"; fi)
$(if [[ "$TOTAL_EXTERNAL" -gt 0 ]]; then echo "- **${TOTAL_EXTERNAL} external service integrations**"; fi)

## Documentation Index

- [Functional Summary](functional-summary.md) - What the system does
- [Architecture](architecture/README.md) - System design and patterns
- [Modules](modules/README.md) - Detailed component documentation
- [API Reference](api-reference/README.md) - Complete API documentation
- [Data Models](data-models/README.md) - Database schemas and entities

---
*This documentation was auto-generated by DeepWiki from the codebase index.*
EOF
}

#=============================================================================
# Tier 2: Functional Summary
#=============================================================================
generate_tier2() {
    log_info "Generating Tier 2: Functional Summary..."

    cat > "${OUTPUT_DIR}/functional-summary.md" << EOF
# ${PROJECT_NAME} - Functional Summary

> High-level overview of system capabilities

## Core Capabilities

EOF

    # List classes with brief descriptions
    if [[ "$TOTAL_CLASSES" -gt 0 ]]; then
        cat >> "${OUTPUT_DIR}/functional-summary.md" << EOF
### Classes

$(echo "$STRUCTURE" | jq -r '.classes[]? | "- **\(.name)** - \(.file):\(.line)"' 2>/dev/null || echo "No classes found")

EOF
    fi

    # List major functions
    if [[ "$TOTAL_FUNCTIONS" -gt 0 ]]; then
        cat >> "${OUTPUT_DIR}/functional-summary.md" << EOF
### Functions

$(echo "$STRUCTURE" | jq -r '.functions[]? | "- `\(.name)` - \(.file):\(.line)"' 2>/dev/null || echo "No functions found")

EOF
    fi

    # API capabilities
    if [[ "$TOTAL_REST" -gt 0 ]]; then
        cat >> "${OUTPUT_DIR}/functional-summary.md" << EOF
### API Capabilities

The system exposes ${TOTAL_REST} REST endpoints:

$(echo "$API_ENDPOINTS" | jq -r '.rest_endpoints[]? | "- **\(.method)** `\(.path)` - \(.file):\(.line)"' 2>/dev/null || echo "No endpoints found")

EOF
    fi

    # External integrations
    if [[ "$TOTAL_EXTERNAL" -gt 0 ]]; then
        cat >> "${OUTPUT_DIR}/functional-summary.md" << EOF
### External Integrations

The system integrates with:

$(echo "$EXTERNAL_APIS" | jq -r '.third_party_services[]? | "- **\(.service)** - \(.file):\(.line)"' 2>/dev/null | sort -u || echo "No external services")

EOF
    fi
}

#=============================================================================
# Tier 3: Architecture
#=============================================================================
generate_tier3() {
    log_info "Generating Tier 3: Architecture..."

    # Architecture README
    cat > "${OUTPUT_DIR}/architecture/README.md" << EOF
# Architecture Overview

## Component Diagram

\`\`\`mermaid
graph TB
    subgraph "Application Layer"
$(echo "$STRUCTURE" | jq -r '.classes[]? | "        \(.name)[\"\(.name)\"]"' 2>/dev/null | head -10 || echo "        App[\"Application\"]")
    end

    subgraph "API Layer"
$(if [[ "$TOTAL_REST" -gt 0 ]]; then echo "        REST[\"REST API (${TOTAL_REST} endpoints)\"]"; fi)
$(if [[ "$TOTAL_GRAPHQL" -gt 0 ]]; then echo "        GQL[\"GraphQL (${TOTAL_GRAPHQL} resolvers)\"]"; fi)
$(if [[ "$TOTAL_WEBSOCKET" -gt 0 ]]; then echo "        WS[\"WebSocket (${TOTAL_WEBSOCKET} handlers)\"]"; fi)
    end

    subgraph "External Services"
$(echo "$EXTERNAL_APIS" | jq -r '.third_party_services[]? | "        \(.service | gsub("[^a-zA-Z0-9]"; ""))[\"\(.service)\"]"' 2>/dev/null | sort -u | head -5 || echo "        Ext[\"External APIs\"]")
    end
\`\`\`

## Architectural Patterns

Based on the codebase structure, this project appears to use:

$(if [[ "$TOTAL_REST" -gt 0 ]]; then echo "- **REST API Architecture** - ${TOTAL_REST} HTTP endpoints"; fi)
$(if [[ "$TOTAL_GRAPHQL" -gt 0 ]]; then echo "- **GraphQL API** - ${TOTAL_GRAPHQL} resolvers"; fi)
$(if [[ "$TOTAL_ORM" -gt 0 ]]; then echo "- **ORM Pattern** - ${TOTAL_ORM} entity mappings"; fi)
$(if echo "$STRUCTURE" | jq -e '.classes[]? | select(.name | test("Service$"))' > /dev/null 2>&1; then echo "- **Service Layer Pattern** - Business logic encapsulation"; fi)
$(if echo "$STRUCTURE" | jq -e '.classes[]? | select(.name | test("Controller$"))' > /dev/null 2>&1; then echo "- **Controller Pattern** - Request handling"; fi)
$(if echo "$STRUCTURE" | jq -e '.classes[]? | select(.name | test("Repository$"))' > /dev/null 2>&1; then echo "- **Repository Pattern** - Data access abstraction"; fi)

## Module Dependencies

See [dependency-graph.md](dependency-graph.md) for detailed import relationships.
EOF

    # Dependency graph
    cat > "${OUTPUT_DIR}/architecture/dependency-graph.md" << EOF
# Dependency Graph

## Import Relationships

\`\`\`mermaid
graph LR
$(echo "$DEPENDENCIES" | jq -r '.files[]? | select(.imported_from | startswith(".")) | "    \(.source_file | gsub("[^a-zA-Z0-9]"; "_")) --> \(.imported_from | gsub("[^a-zA-Z0-9]"; "_"))"' 2>/dev/null | head -20 || echo "    App --> Modules")
\`\`\`

## External Dependencies

$(echo "$DEPENDENCIES" | jq -r '.files[]? | select(.imported_from | startswith(".") | not) | "- `\(.imported_from)` - used in \(.source_file)"' 2>/dev/null | sort -u | head -20 || echo "No external dependencies tracked")
EOF
}

#=============================================================================
# Tier 4: Module Documentation
#=============================================================================
generate_tier4() {
    log_info "Generating Tier 4: Module Documentation..."

    # Modules README
    cat > "${OUTPUT_DIR}/modules/README.md" << EOF
# Module Documentation

Detailed documentation for each module in the codebase.

## Classes

$(echo "$STRUCTURE" | jq -r '.classes[]? | "- [\(.name)](\(.name).md) - \(.file):\(.line)"' 2>/dev/null || echo "No classes documented")

## Interfaces

$(echo "$STRUCTURE" | jq -r '.interfaces[]? | "- \(.name) - \(.file):\(.line)"' 2>/dev/null || echo "No interfaces documented")
EOF

    # Generate individual class docs
    echo "$STRUCTURE" | jq -c '.classes[]?' 2>/dev/null | while read -r class; do
        NAME=$(echo "$class" | jq -r '.name')
        FILE=$(echo "$class" | jq -r '.file')
        LINE=$(echo "$class" | jq -r '.line')

        cat > "${OUTPUT_DIR}/modules/${NAME}.md" << EOF
# ${NAME}

> Auto-generated module documentation

## Location

- **File**: \`${FILE}\`
- **Line**: ${LINE}

## Description

Class \`${NAME}\` is defined in \`${FILE}\`.

## Related Files

$(echo "$DEPENDENCIES" | jq -r ".files[]? | select(.source_file == \"$FILE\") | \"- Imports: \`\(.imported_from)\`\"" 2>/dev/null || echo "No imports tracked")

---
*Generated by DeepWiki*
EOF
    done
}

#=============================================================================
# API Reference
#=============================================================================
generate_api_reference() {
    log_info "Generating API Reference..."

    cat > "${OUTPUT_DIR}/api-reference/README.md" << EOF
# API Reference

Complete API documentation for ${PROJECT_NAME}.

## REST Endpoints

| Method | Path | File | Line |
|--------|------|------|------|
$(echo "$API_ENDPOINTS" | jq -r '.rest_endpoints[]? | "| \(.method) | `\(.path)` | \(.file) | \(.line) |"' 2>/dev/null || echo "| - | - | - | - |")

## GraphQL Resolvers

$(if [[ "$TOTAL_GRAPHQL" -gt 0 ]]; then
    echo "| Type | File | Line |"
    echo "|------|------|------|"
    echo "$API_ENDPOINTS" | jq -r '.graphql_resolvers[]? | "| \(.type) | \(.file) | \(.line) |"' 2>/dev/null
else
    echo "No GraphQL resolvers found."
fi)

## WebSocket Handlers

$(if [[ "$TOTAL_WEBSOCKET" -gt 0 ]]; then
    echo "| Event | File | Line |"
    echo "|-------|------|------|"
    echo "$API_ENDPOINTS" | jq -r '.websocket_handlers[]? | "| \(.event) | \(.file) | \(.line) |"' 2>/dev/null
else
    echo "No WebSocket handlers found."
fi)
EOF
}

#=============================================================================
# Data Models Documentation
#=============================================================================
generate_data_models() {
    log_info "Generating Data Models Documentation..."

    cat > "${OUTPUT_DIR}/data-models/README.md" << EOF
# Data Models

Database schemas and ORM entity documentation.

## Database Schemas

$(if [[ "$TOTAL_DB_SCHEMAS" -gt 0 ]]; then
    echo "| Table | File | Line | Type |"
    echo "|-------|------|------|------|"
    echo "$DATA_MODELS" | jq -r '.database_schemas[]? | "| \(.table) | \(.file) | \(.line) | \(.schema_type) |"' 2>/dev/null
else
    echo "No database schemas found."
fi)

## ORM Entities

$(if [[ "$TOTAL_ORM" -gt 0 ]]; then
    echo "| Entity | Table | File | Line | ORM |"
    echo "|--------|-------|------|------|-----|"
    echo "$DATA_MODELS" | jq -r '.orm_entities[]? | "| \(.entity) | \(.table) | \(.file) | \(.line) | \(.orm_type) |"' 2>/dev/null
else
    echo "No ORM entities found."
fi)

## Environment Variables

$(if [[ "$TOTAL_ENV_VARS" -gt 0 ]]; then
    echo "| Variable | File | Line |"
    echo "|----------|------|------|"
    echo "$EXTERNAL_APIS" | jq -r '.environment_variables[]? | "| `\(.name)` | \(.file) | \(.line) |"' 2>/dev/null
else
    echo "No environment variables tracked."
fi)
EOF
}

#=============================================================================
# Main Index
#=============================================================================
generate_index() {
    log_info "Generating main index..."

    cat > "${OUTPUT_DIR}/index.md" << EOF
# ${PROJECT_NAME} Documentation

> Auto-generated by DeepWiki

## Contents

1. [Overview](overview.md) - Quick introduction and statistics
2. [Functional Summary](functional-summary.md) - System capabilities
3. [Architecture](architecture/README.md) - Design patterns and diagrams
4. [Modules](modules/README.md) - Detailed component docs
5. [API Reference](api-reference/README.md) - REST, GraphQL, WebSocket
6. [Data Models](data-models/README.md) - Schemas and entities

## Quick Start

This documentation was generated from the codebase index.
To regenerate, run: \`/speckitsmart.wiki\`

---
Generated: ${CURRENT_DATE}
EOF
}

#=============================================================================
# Main Execution
#=============================================================================

# Parse tier selection
GENERATE_T1=false
GENERATE_T2=false
GENERATE_T3=false
GENERATE_T4=false

IFS=',' read -ra TIER_ARRAY <<< "$TIERS"
for tier in "${TIER_ARRAY[@]}"; do
    case "$tier" in
        1) GENERATE_T1=true ;;
        2) GENERATE_T2=true ;;
        3) GENERATE_T3=true ;;
        4) GENERATE_T4=true ;;
    esac
done

echo "Generating DeepWiki documentation..."
echo "Output directory: $OUTPUT_DIR"
echo "Tiers: $TIERS"
echo ""

# Generate selected tiers
generate_index

if [[ "$GENERATE_T1" == "true" ]]; then
    generate_tier1
fi

if [[ "$GENERATE_T2" == "true" ]]; then
    generate_tier2
fi

if [[ "$GENERATE_T3" == "true" ]]; then
    generate_tier3
fi

if [[ "$GENERATE_T4" == "true" ]]; then
    generate_tier4
fi

# Always generate API and Data Model docs
generate_api_reference
generate_data_models

echo ""
echo "✓ DeepWiki documentation generated successfully!"
echo "✓ Location: $OUTPUT_DIR"
echo ""
echo "Files generated:"
find "$OUTPUT_DIR" -name "*.md" | wc -l | xargs echo "  - Markdown files:"
echo ""
echo "Next steps:"
echo "  - View documentation: open $OUTPUT_DIR/index.md"
echo "  - Query codebase: /speckitsmart.ask \"your question\""

exit 0
