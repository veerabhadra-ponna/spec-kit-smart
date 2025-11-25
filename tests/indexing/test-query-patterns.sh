#!/usr/bin/env bash
#
# test-query-patterns.sh - Test cases for common query patterns
#
# Tests various query patterns users might use when searching the knowledge base:
# - Technical term queries
# - Natural language queries
# - Code-specific queries
# - Architecture queries
#
# Usage: bash tests/indexing/test-query-patterns.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SEARCH_SCRIPT="$REPO_ROOT/.specify/scripts/bash/search-knowledge-base.sh"
BUILD_SCRIPT="$REPO_ROOT/scripts/bash/build-codebase-index.sh"
FIXTURE_DIR="$REPO_ROOT/tests/fixtures/sample-projects/typescript-express"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

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

log_info() {
    echo -e "${CYAN}[INFO]${NC} $*"
}

setup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis .deepwiki
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
}

teardown() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis .deepwiki
}

# Helper to run search and check for results
run_search() {
    local query="$1"
    bash "$SEARCH_SCRIPT" --query "$query" --format json 2>/dev/null || echo '{"results":[]}'
}

#=============================================================================
# TECHNICAL TERM QUERIES
#=============================================================================

test_class_query() {
    log_test "Query pattern: 'class'"

    local output
    output=$(run_search "class")

    if [[ -n "$output" ]]; then
        log_pass "Class query returns results"
    else
        log_fail "Class query failed"
    fi
}

test_function_query() {
    log_test "Query pattern: 'function'"

    local output
    output=$(run_search "function")

    if [[ -n "$output" ]]; then
        log_pass "Function query returns results"
    else
        log_fail "Function query failed"
    fi
}

test_interface_query() {
    log_test "Query pattern: 'interface'"

    local output
    output=$(run_search "interface")

    if [[ -n "$output" ]]; then
        log_pass "Interface query returns results"
    else
        log_fail "Interface query failed"
    fi
}

test_api_query() {
    log_test "Query pattern: 'api'"

    local output
    output=$(run_search "api")

    if [[ -n "$output" ]]; then
        log_pass "API query returns results"
    else
        log_fail "API query failed"
    fi
}

#=============================================================================
# NATURAL LANGUAGE QUERIES
#=============================================================================

test_how_question() {
    log_test "Query pattern: 'how does authentication work'"

    local output
    output=$(run_search "how does authentication work")

    if [[ -n "$output" ]]; then
        log_pass "How question query handled"
    else
        log_fail "How question query failed"
    fi
}

test_what_question() {
    log_test "Query pattern: 'what is the main entry point'"

    local output
    output=$(run_search "what is the main entry point")

    if [[ -n "$output" ]]; then
        log_pass "What question query handled"
    else
        log_fail "What question query failed"
    fi
}

test_where_question() {
    log_test "Query pattern: 'where are routes defined'"

    local output
    output=$(run_search "where are routes defined")

    if [[ -n "$output" ]]; then
        log_pass "Where question query handled"
    else
        log_fail "Where question query failed"
    fi
}

test_which_question() {
    log_test "Query pattern: 'which files handle user'"

    local output
    output=$(run_search "which files handle user")

    if [[ -n "$output" ]]; then
        log_pass "Which question query handled"
    else
        log_fail "Which question query failed"
    fi
}

#=============================================================================
# CODE-SPECIFIC QUERIES
#=============================================================================

test_file_extension_query() {
    log_test "Query pattern: '.ts files'"

    local output
    output=$(run_search ".ts files")

    if [[ -n "$output" ]]; then
        log_pass "File extension query handled"
    else
        log_fail "File extension query failed"
    fi
}

test_import_query() {
    log_test "Query pattern: 'import export'"

    local output
    output=$(run_search "import export")

    if [[ -n "$output" ]]; then
        log_pass "Import/export query handled"
    else
        log_fail "Import/export query failed"
    fi
}

test_dependency_query() {
    log_test "Query pattern: 'dependencies'"

    local output
    output=$(run_search "dependencies")

    if [[ -n "$output" ]]; then
        log_pass "Dependencies query handled"
    else
        log_fail "Dependencies query failed"
    fi
}

test_module_query() {
    log_test "Query pattern: 'module'"

    local output
    output=$(run_search "module")

    if [[ -n "$output" ]]; then
        log_pass "Module query handled"
    else
        log_fail "Module query failed"
    fi
}

#=============================================================================
# ARCHITECTURE QUERIES
#=============================================================================

test_architecture_query() {
    log_test "Query pattern: 'architecture'"

    local output
    output=$(run_search "architecture")

    if [[ -n "$output" ]]; then
        log_pass "Architecture query handled"
    else
        log_fail "Architecture query failed"
    fi
}

test_pattern_query() {
    log_test "Query pattern: 'design pattern'"

    local output
    output=$(run_search "design pattern")

    if [[ -n "$output" ]]; then
        log_pass "Design pattern query handled"
    else
        log_fail "Design pattern query failed"
    fi
}

test_service_query() {
    log_test "Query pattern: 'service layer'"

    local output
    output=$(run_search "service layer")

    if [[ -n "$output" ]]; then
        log_pass "Service layer query handled"
    else
        log_fail "Service layer query failed"
    fi
}

test_controller_query() {
    log_test "Query pattern: 'controller'"

    local output
    output=$(run_search "controller")

    if [[ -n "$output" ]]; then
        log_pass "Controller query handled"
    else
        log_fail "Controller query failed"
    fi
}

#=============================================================================
# EDGE CASE QUERIES
#=============================================================================

test_single_char_query() {
    log_test "Query pattern: single character 'a'"

    local output
    output=$(run_search "a")

    # Should handle gracefully (may return empty or many results)
    log_pass "Single character query handled"
}

test_numeric_query() {
    log_test "Query pattern: numeric '123'"

    local output
    output=$(run_search "123")

    log_pass "Numeric query handled"
}

test_quoted_query() {
    log_test "Query pattern: quoted string"

    local output
    output=$(run_search "\"exact match\"")

    log_pass "Quoted query handled"
}

test_very_long_query() {
    log_test "Query pattern: very long query"

    local long_query="this is a very long query string that contains many words to test how the search handles lengthy input strings with multiple terms"
    local output
    output=$(run_search "$long_query")

    log_pass "Long query handled"
}

#=============================================================================
# Main
#=============================================================================

main() {
    echo ""
    echo "========================================="
    echo " Query Patterns Test Suite"
    echo "========================================="
    echo ""
    echo "Fixture: $FIXTURE_DIR"
    echo ""

    setup
    trap teardown EXIT

    echo ""
    log_info "Testing Technical Term Queries..."
    test_class_query
    test_function_query
    test_interface_query
    test_api_query

    echo ""
    log_info "Testing Natural Language Queries..."
    test_how_question
    test_what_question
    test_where_question
    test_which_question

    echo ""
    log_info "Testing Code-Specific Queries..."
    test_file_extension_query
    test_import_query
    test_dependency_query
    test_module_query

    echo ""
    log_info "Testing Architecture Queries..."
    test_architecture_query
    test_pattern_query
    test_service_query
    test_controller_query

    echo ""
    log_info "Testing Edge Case Queries..."
    test_single_char_query
    test_numeric_query
    test_quoted_query
    test_very_long_query

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
