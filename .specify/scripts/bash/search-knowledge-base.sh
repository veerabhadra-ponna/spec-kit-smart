#!/usr/bin/env bash
#
# search-knowledge-base.sh - Search codebase knowledge base
#
# Searches the index and DeepWiki documentation to answer questions about:
# - Architecture and patterns
# - Data models
# - API endpoints
# - External integrations
# - Business logic
#
# Usage: bash search-knowledge-base.sh "<query>" [--format json|text] [--sources index|wiki|all]
#
# Exit codes:
#   0 - Success (results found)
#   1 - Index not found
#   2 - No results found
#

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX_DIR="${REPO_ROOT}/.analysis/index"
WIKI_DIR="${REPO_ROOT}/.deepwiki"
FORMAT="text"
SOURCES="all"
QUERY=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --sources)
            SOURCES="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 \"<query>\" [--format json|text] [--sources index|wiki|all]"
            exit 0
            ;;
        *)
            if [[ -z "$QUERY" ]]; then
                QUERY="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$QUERY" ]]; then
    echo "Error: Query required" >&2
    exit 2
fi

# Check prerequisites
if [[ ! -d "$INDEX_DIR" ]]; then
    echo '{"error": "Index not found. Run /speckitsmart.index first.", "results": []}' >&2
    exit 1
fi

# Convert query to lowercase for searching
QUERY_LOWER=$(echo "$QUERY" | tr '[:upper:]' '[:lower:]')

# Initialize results
declare -a RESULTS
declare -a SOURCES_FOUND
CONFIDENCE="low"
RESULT_COUNT=0

# Search function for index files
search_index() {
    local file="$1"
    local category="$2"

    if [[ ! -f "${INDEX_DIR}/${file}" ]]; then
        return
    fi

    local content=$(cat "${INDEX_DIR}/${file}")

    # Search for query terms in the file
    if echo "$content" | grep -qi "$QUERY_LOWER"; then
        # Extract matching items
        local matches=$(echo "$content" | jq -c '.. | objects | select(.name? or .path? or .service? or .table? or .entity?) | select((.name // .path // .service // .table // .entity // "") | ascii_downcase | contains("'"$QUERY_LOWER"'"))' 2>/dev/null || echo "")

        if [[ -n "$matches" ]]; then
            while IFS= read -r match; do
                if [[ -n "$match" ]]; then
                    RESULTS+=("$match")
                    SOURCES_FOUND+=("index:$category")
                    RESULT_COUNT=$((RESULT_COUNT + 1))
                fi
            done <<< "$matches"
        fi
    fi
}

# Search function for wiki files
search_wiki() {
    if [[ ! -d "$WIKI_DIR" ]]; then
        return
    fi

    # Search markdown files
    local matches=$(grep -ril "$QUERY" "$WIKI_DIR" 2>/dev/null || true)

    if [[ -n "$matches" ]]; then
        while IFS= read -r file; do
            if [[ -n "$file" ]]; then
                local rel_path="${file#$WIKI_DIR/}"
                local context=$(grep -i "$QUERY" "$file" | head -3)

                local result=$(jq -n \
                    --arg file "$rel_path" \
                    --arg context "$context" \
                    '{type: "wiki", file: $file, context: $context}')

                RESULTS+=("$result")
                SOURCES_FOUND+=("wiki:$rel_path")
                RESULT_COUNT=$((RESULT_COUNT + 1))
            fi
        done <<< "$matches"
    fi
}

# Detect query category
detect_category() {
    local q="$QUERY_LOWER"

    if echo "$q" | grep -qiE "class|function|interface|method"; then
        echo "structure"
    elif echo "$q" | grep -qiE "endpoint|api|rest|route|path"; then
        echo "api"
    elif echo "$q" | grep -qiE "database|table|schema|model|entity"; then
        echo "data"
    elif echo "$q" | grep -qiE "service|external|integration|stripe|aws"; then
        echo "external"
    elif echo "$q" | grep -qiE "env|environment|variable|config"; then
        echo "config"
    elif echo "$q" | grep -qiE "import|dependency|require"; then
        echo "dependencies"
    else
        echo "general"
    fi
}

# Search based on sources
if [[ "$SOURCES" == "all" || "$SOURCES" == "index" ]]; then
    CATEGORY=$(detect_category)

    case "$CATEGORY" in
        structure)
            search_index "structure.json" "code_structure"
            ;;
        api)
            search_index "api-endpoints.json" "api_endpoints"
            ;;
        data)
            search_index "data-models.json" "data_models"
            ;;
        external|config)
            search_index "external-apis.json" "external_apis"
            ;;
        dependencies)
            search_index "dependencies.json" "dependencies"
            ;;
        *)
            # Search all index files
            search_index "structure.json" "code_structure"
            search_index "api-endpoints.json" "api_endpoints"
            search_index "data-models.json" "data_models"
            search_index "external-apis.json" "external_apis"
            search_index "dependencies.json" "dependencies"
            ;;
    esac
fi

if [[ "$SOURCES" == "all" || "$SOURCES" == "wiki" ]]; then
    search_wiki
fi

# Determine confidence
if [[ $RESULT_COUNT -ge 5 ]]; then
    CONFIDENCE="high"
elif [[ $RESULT_COUNT -ge 2 ]]; then
    CONFIDENCE="medium"
elif [[ $RESULT_COUNT -ge 1 ]]; then
    CONFIDENCE="low"
else
    CONFIDENCE="none"
fi

# Generate output
if [[ "$FORMAT" == "json" ]]; then
    # JSON output
    RESULTS_JSON="["
    for i in "${!RESULTS[@]}"; do
        if [[ $i -gt 0 ]]; then
            RESULTS_JSON+=","
        fi
        RESULTS_JSON+="${RESULTS[$i]}"
    done
    RESULTS_JSON+="]"

    jq -n \
        --arg query "$QUERY" \
        --argjson results "$RESULTS_JSON" \
        --arg confidence "$CONFIDENCE" \
        --argjson count "$RESULT_COUNT" \
        '{
            query: $query,
            confidence: $confidence,
            result_count: $count,
            results: $results
        }'
else
    # Text output
    echo ""
    echo "Query: $QUERY"
    echo "Confidence: $CONFIDENCE (based on $RESULT_COUNT sources)"
    echo ""

    if [[ $RESULT_COUNT -eq 0 ]]; then
        echo "No relevant results found."
        echo ""
        echo "Suggestions:"
        echo "  - Try different keywords"
        echo "  - Check if the index is up to date"
        echo "  - Generate DeepWiki documentation for better search"
        exit 2
    fi

    echo "Results:"
    echo "--------"

    for i in "${!RESULTS[@]}"; do
        result="${RESULTS[$i]}"
        source="${SOURCES_FOUND[$i]}"

        name=$(echo "$result" | jq -r '.name // .path // .service // .table // .entity // .file // "unknown"' 2>/dev/null || echo "unknown")
        file=$(echo "$result" | jq -r '.file // "N/A"' 2>/dev/null || echo "N/A")
        line=$(echo "$result" | jq -r '.line // "N/A"' 2>/dev/null || echo "N/A")

        echo ""
        echo "  [$source] $name"
        if [[ "$file" != "N/A" && "$file" != "null" ]]; then
            echo "    Location: $file:$line"
        fi
    done

    echo ""
    echo "---"
    echo "Sources searched: ${SOURCES_FOUND[*]:-none}"
fi

exit 0
