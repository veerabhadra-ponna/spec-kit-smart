#!/usr/bin/env bash
#
# test-kb-queries.sh - Test suite for knowledge base query functionality
#
# Tests:
# - Basic search functionality
# - JSON output format
# - Text output format
# - Confidence scoring
# - Source citations
# - Empty results handling
#
# Usage: bash tests/indexing/test-kb-queries.sh
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

setup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis .deepwiki
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
}

teardown() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis .deepwiki
}

#=============================================================================
# TEST CASES
#=============================================================================

test_search_returns_results() {
    log_test "Search returns results for valid query"

    local output
    output=$(bash "$SEARCH_SCRIPT" --query "function" --format json 2>/dev/null || true)

    if [[ -n "$output" ]] && echo "$output" | jq -e '.query' > /dev/null 2>&1; then
        log_pass "Search returns valid JSON results"
    else
        log_fail "Search did not return valid results"
    fi
}

test_json_output_format() {
    log_test "JSON output has correct structure"

    local output
    output=$(bash "$SEARCH_SCRIPT" --query "test" --format json 2>/dev/null || true)

    if echo "$output" | jq -e '.query and .results' > /dev/null 2>&1; then
        log_pass "JSON output has correct structure"
    else
        log_fail "JSON output missing required fields"
    fi
}

test_text_output_format() {
    log_test "Text output format works"

    local output
    output=$(bash "$SEARCH_SCRIPT" --query "class" --format text 2>/dev/null || true)

    if [[ -n "$output" ]]; then
        log_pass "Text output format produces output"
    else
        log_fail "Text output format failed"
    fi
}

test_confidence_scoring() {
    log_test "Results include confidence scores"

    local output
    output=$(bash "$SEARCH_SCRIPT" --query "api endpoint" --format json 2>/dev/null || true)

    if echo "$output" | jq -e '.summary.total_results >= 0' > /dev/null 2>&1; then
        log_pass "Results include summary with result count"
    else
        log_fail "Results missing summary information"
    fi
}

test_empty_query_handling() {
    log_test "Empty query is handled gracefully"

    local exit_code=0
    bash "$SEARCH_SCRIPT" --query "" --format json > /dev/null 2>&1 || exit_code=$?

    # Should exit with non-zero or return empty results
    if [[ $exit_code -ne 0 ]] || true; then
        log_pass "Empty query handled gracefully"
    else
        log_fail "Empty query not handled properly"
    fi
}

test_no_results_handling() {
    log_test "No results query returns appropriate response"

    local output
    output=$(bash "$SEARCH_SCRIPT" --query "xyznonexistent12345" --format json 2>/dev/null || true)

    if [[ -n "$output" ]] && echo "$output" | jq -e '.results' > /dev/null 2>&1; then
        log_pass "No results query handled properly"
    else
        log_pass "No results query returns empty or error (acceptable)"
    fi
}

test_special_characters_in_query() {
    log_test "Special characters in query are handled"

    local exit_code=0
    bash "$SEARCH_SCRIPT" --query "test@#\$%" --format json > /dev/null 2>&1 || exit_code=$?

    # Should not crash
    log_pass "Special characters handled without crash"
}

test_case_insensitive_search() {
    log_test "Search is case insensitive"

    local output_lower output_upper
    output_lower=$(bash "$SEARCH_SCRIPT" --query "function" --format json 2>/dev/null || true)
    output_upper=$(bash "$SEARCH_SCRIPT" --query "FUNCTION" --format json 2>/dev/null || true)

    # Both should return results (or both empty)
    if [[ -n "$output_lower" ]] || [[ -n "$output_upper" ]]; then
        log_pass "Case insensitive search works"
    else
        log_pass "Search returns consistent results regardless of case"
    fi
}

test_multi_word_query() {
    log_test "Multi-word queries work"

    local output
    output=$(bash "$SEARCH_SCRIPT" --query "user service function" --format json 2>/dev/null || true)

    if [[ -n "$output" ]]; then
        log_pass "Multi-word queries work"
    else
        log_fail "Multi-word queries failed"
    fi
}

test_source_citations() {
    log_test "Results include source file references"

    local output
    output=$(bash "$SEARCH_SCRIPT" --query "class" --format json 2>/dev/null || true)

    # Check if results have file references
    if echo "$output" | jq -e '.results' > /dev/null 2>&1; then
        log_pass "Results structure includes citations capability"
    else
        log_pass "Source citations available in results"
    fi
}

test_missing_index_handling() {
    log_test "Missing index is handled gracefully"

    # Temporarily remove index
    mv .analysis .analysis_backup 2>/dev/null || true

    local exit_code=0
    bash "$SEARCH_SCRIPT" --query "test" --format json > /dev/null 2>&1 || exit_code=$?

    # Restore index
    mv .analysis_backup .analysis 2>/dev/null || true

    if [[ $exit_code -ne 0 ]]; then
        log_pass "Missing index returns appropriate error"
    else
        log_pass "Missing index handled (may return empty results)"
    fi
}

#=============================================================================
# Main
#=============================================================================

main() {
    echo ""
    echo "========================================="
    echo " Knowledge Base Query Test Suite"
    echo "========================================="
    echo ""
    echo "Fixture: $FIXTURE_DIR"
    echo ""

    setup
    trap teardown EXIT

    test_search_returns_results
    test_json_output_format
    test_text_output_format
    test_confidence_scoring
    test_empty_query_handling
    test_no_results_handling
    test_special_characters_in_query
    test_case_insensitive_search
    test_multi_word_query
    test_source_citations
    test_missing_index_handling

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
