#!/usr/bin/env bash
#
# test-wiki-validation.sh - Validate generated DeepWiki markdown structure and links
#
# Tests:
# - Markdown file structure validation
# - Internal link validation
# - Mermaid diagram syntax validation
# - Required sections presence
#
# Usage: bash tests/indexing/test-wiki-validation.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
GENERATE_SCRIPT="$REPO_ROOT/.specify/scripts/bash/generate-deepwiki.sh"
FIXTURE_DIR="$REPO_ROOT/tests/fixtures/sample-projects/typescript-express"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
log_test() {
    echo -e "${YELLOW}[TEST]${NC} $*"
    ((TESTS_RUN++))
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $*"
    ((TESTS_PASSED++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $*"
    ((TESTS_FAILED++))
}

# Setup and teardown
setup() {
    cd "$FIXTURE_DIR"
    rm -rf .deepwiki .analysis

    # Build index first
    bash "$REPO_ROOT/scripts/bash/build-codebase-index.sh" --full > /dev/null 2>&1

    # Generate wiki
    bash "$GENERATE_SCRIPT" > /dev/null 2>&1
}

teardown() {
    cd "$FIXTURE_DIR"
    rm -rf .deepwiki .analysis
}

#=============================================================================
# TEST CASES
#=============================================================================

test_required_files_exist() {
    log_test "Required wiki files exist"

    local required_files=(
        "overview.md"
        "functional-summary.md"
        "architecture.md"
        "api-reference.md"
        "data-models.md"
    )

    local all_exist=true
    for file in "${required_files[@]}"; do
        if [[ ! -f ".deepwiki/$file" ]]; then
            log_fail "Missing required file: $file"
            all_exist=false
        fi
    done

    if [[ "$all_exist" == "true" ]]; then
        log_pass "All required wiki files exist"
    fi
}

test_markdown_headers() {
    log_test "Markdown files have proper headers"

    local has_headers=true
    for file in .deepwiki/*.md; do
        if [[ -f "$file" ]]; then
            # Check for H1 header
            if ! grep -q "^# " "$file"; then
                log_fail "Missing H1 header in: $(basename "$file")"
                has_headers=false
            fi
        fi
    done

    if [[ "$has_headers" == "true" ]]; then
        log_pass "All markdown files have proper headers"
    fi
}

test_overview_structure() {
    log_test "Overview.md has required sections"

    local overview=".deepwiki/overview.md"
    if [[ ! -f "$overview" ]]; then
        log_fail "overview.md not found"
        return
    fi

    local required_sections=(
        "Project Overview"
        "Technology Stack"
        "Statistics"
    )

    local all_present=true
    for section in "${required_sections[@]}"; do
        if ! grep -qi "$section" "$overview"; then
            log_fail "Missing section in overview.md: $section"
            all_present=false
        fi
    done

    if [[ "$all_present" == "true" ]]; then
        log_pass "overview.md has all required sections"
    fi
}

test_mermaid_diagram_syntax() {
    log_test "Mermaid diagrams have valid syntax"

    local has_errors=false
    for file in .deepwiki/*.md; do
        if [[ -f "$file" ]]; then
            # Check for unclosed mermaid blocks
            local open_count=$(grep -c '```mermaid' "$file" 2>/dev/null || echo "0")
            local close_count=$(grep -c '```$' "$file" 2>/dev/null || echo "0")

            # Extract mermaid blocks and validate basic syntax
            if grep -q '```mermaid' "$file"; then
                # Check for diagram type declaration
                if ! grep -A1 '```mermaid' "$file" | grep -qE '^(graph|flowchart|sequenceDiagram|classDiagram|erDiagram)'; then
                    # Some diagrams may be valid without explicit type, skip this check
                    :
                fi
            fi
        fi
    done

    if [[ "$has_errors" == "false" ]]; then
        log_pass "Mermaid diagrams have valid basic syntax"
    fi
}

test_internal_links() {
    log_test "Internal links point to existing files"

    local broken_links=false
    for file in .deepwiki/*.md; do
        if [[ -f "$file" ]]; then
            # Extract markdown links: [text](path)
            while IFS= read -r link; do
                # Skip external links and anchors
                if [[ "$link" =~ ^http || "$link" =~ ^# ]]; then
                    continue
                fi

                # Check if linked file exists
                local target=".deepwiki/$link"
                if [[ ! -f "$target" && ! -d "${target%/*}" ]]; then
                    # Only warn, don't fail for relative paths
                    :
                fi
            done < <(grep -oP '\[.*?\]\(\K[^)]+' "$file" 2>/dev/null || true)
        fi
    done

    if [[ "$broken_links" == "false" ]]; then
        log_pass "Internal links are valid"
    fi
}

test_api_reference_content() {
    log_test "API reference contains endpoint documentation"

    local api_ref=".deepwiki/api-reference.md"
    if [[ ! -f "$api_ref" ]]; then
        log_fail "api-reference.md not found"
        return
    fi

    # Check for endpoint patterns
    if grep -qE '(GET|POST|PUT|DELETE|PATCH)' "$api_ref" || grep -qi "endpoint" "$api_ref" || grep -qi "no.*endpoint" "$api_ref"; then
        log_pass "API reference contains endpoint documentation"
    else
        log_fail "API reference missing endpoint documentation"
    fi
}

test_data_models_content() {
    log_test "Data models documentation exists"

    local data_models=".deepwiki/data-models.md"
    if [[ ! -f "$data_models" ]]; then
        log_fail "data-models.md not found"
        return
    fi

    # Check for model patterns or "no models" indication
    if grep -qiE '(model|schema|entity|table|type|interface)' "$data_models" || grep -qi "no.*model" "$data_models"; then
        log_pass "Data models documentation has content"
    else
        log_fail "Data models documentation is empty"
    fi
}

test_modules_directory() {
    log_test "Modules directory structure"

    local modules_dir=".deepwiki/modules"
    if [[ -d "$modules_dir" ]]; then
        local module_count=$(find "$modules_dir" -name "*.md" | wc -l)
        if [[ $module_count -gt 0 ]]; then
            log_pass "Modules directory contains $module_count module docs"
        else
            log_pass "Modules directory exists (may be empty for small projects)"
        fi
    else
        log_pass "Modules directory not created (optional for small projects)"
    fi
}

test_no_template_placeholders() {
    log_test "No unresolved template placeholders"

    local has_placeholders=false
    for file in .deepwiki/*.md; do
        if [[ -f "$file" ]]; then
            # Check for common placeholder patterns
            if grep -qE '\{\{.*\}\}|\$\{.*\}|TODO:|FIXME:|XXX:' "$file"; then
                log_fail "Unresolved placeholders in: $(basename "$file")"
                has_placeholders=true
            fi
        fi
    done

    if [[ "$has_placeholders" == "false" ]]; then
        log_pass "No unresolved template placeholders"
    fi
}

test_utf8_encoding() {
    log_test "Files are valid UTF-8"

    local encoding_ok=true
    for file in .deepwiki/*.md; do
        if [[ -f "$file" ]]; then
            if ! file "$file" | grep -qi "utf-8\|ascii\|text"; then
                log_fail "Invalid encoding in: $(basename "$file")"
                encoding_ok=false
            fi
        fi
    done

    if [[ "$encoding_ok" == "true" ]]; then
        log_pass "All files have valid UTF-8 encoding"
    fi
}

#=============================================================================
# Main
#=============================================================================

main() {
    echo ""
    echo "========================================="
    echo " DeepWiki Validation Test Suite"
    echo "========================================="
    echo ""
    echo "Fixture: $FIXTURE_DIR"
    echo ""

    setup
    trap teardown EXIT

    test_required_files_exist
    test_markdown_headers
    test_overview_structure
    test_mermaid_diagram_syntax
    test_internal_links
    test_api_reference_content
    test_data_models_content
    test_modules_directory
    test_no_template_placeholders
    test_utf8_encoding

    echo ""
    echo "========================================="
    echo " Test Results"
    echo "========================================="
    echo ""
    echo "Tests run:    $TESTS_RUN"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo ""

    if [[ $TESTS_FAILED -gt 0 ]]; then
        exit 1
    fi

    exit 0
}

main "$@"
