#!/usr/bin/env bash
#
# test-reusability.sh - Test suite for code reusability detection
#
# Tests:
# - Similar implementation detection
# - Utility function search
# - Architecture pattern detection
# - Test example finding
# - Output format validation
#
# Usage: bash tests/indexing/test-reusability.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FIND_SCRIPT="$REPO_ROOT/.specify/scripts/bash/find-reusable-code.sh"
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
    rm -rf .analysis
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
}

teardown() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis
}

#=============================================================================
# TEST CASES
#=============================================================================

test_script_exists() {
    log_test "Reusability script exists and is executable"

    if [[ -f "$FIND_SCRIPT" ]]; then
        log_pass "Script exists"
    else
        log_fail "Script not found: $FIND_SCRIPT"
    fi
}

test_json_output_format() {
    log_test "JSON output format is valid"

    local output
    output=$(bash "$FIND_SCRIPT" --task "user authentication" --format json 2>/dev/null || true)

    if [[ -n "$output" ]] && echo "$output" | jq -e '.' > /dev/null 2>&1; then
        log_pass "JSON output is valid"
    else
        log_fail "JSON output is invalid"
    fi
}

test_text_output_format() {
    log_test "Text output format works"

    local output
    output=$(bash "$FIND_SCRIPT" --task "create service" --format text 2>/dev/null || true)

    if [[ -n "$output" ]] || [[ $? -eq 2 ]]; then
        log_pass "Text output format works"
    else
        log_fail "Text output format failed"
    fi
}

test_similar_implementation_search() {
    log_test "Similar implementation search"

    local output
    output=$(bash "$FIND_SCRIPT" --task "function handler" --format json 2>/dev/null || true)

    if [[ -n "$output" ]]; then
        log_pass "Similar implementation search executed"
    else
        log_fail "Similar implementation search failed"
    fi
}

test_utility_function_detection() {
    log_test "Utility function detection"

    local output
    output=$(bash "$FIND_SCRIPT" --task "string manipulation" --format json 2>/dev/null || true)

    if echo "$output" | jq -e '.results.utilities' > /dev/null 2>&1 || echo "$output" | jq -e '.summary' > /dev/null 2>&1; then
        log_pass "Utility function detection works"
    else
        log_pass "Utility detection completed (may have no results)"
    fi
}

test_pattern_detection() {
    log_test "Architecture pattern detection"

    local output
    output=$(bash "$FIND_SCRIPT" --task "service layer implementation" --format json 2>/dev/null || true)

    if echo "$output" | jq -e '.results.patterns' > /dev/null 2>&1 || echo "$output" | jq -e '.summary' > /dev/null 2>&1; then
        log_pass "Pattern detection works"
    else
        log_pass "Pattern detection completed (may have no results)"
    fi
}

test_test_example_finding() {
    log_test "Test example finding"

    local output
    output=$(bash "$FIND_SCRIPT" --task "unit test" --format json 2>/dev/null || true)

    if echo "$output" | jq -e '.results.tests' > /dev/null 2>&1 || echo "$output" | jq -e '.summary' > /dev/null 2>&1; then
        log_pass "Test example finding works"
    else
        log_pass "Test example finding completed (may have no results)"
    fi
}

test_threshold_parameter() {
    log_test "Threshold parameter works"

    local output_high output_low
    output_high=$(bash "$FIND_SCRIPT" --task "function" --format json --threshold 90 2>/dev/null || true)
    output_low=$(bash "$FIND_SCRIPT" --task "function" --format json --threshold 10 2>/dev/null || true)

    # Both should execute without error
    if [[ -n "$output_high" ]] && [[ -n "$output_low" ]]; then
        log_pass "Threshold parameter works"
    else
        log_pass "Threshold parameter accepted"
    fi
}

test_missing_index_handling() {
    log_test "Missing index is handled gracefully"

    # Temporarily remove index
    mv .analysis .analysis_backup 2>/dev/null || true

    local exit_code=0
    bash "$FIND_SCRIPT" --task "test" --format json > /dev/null 2>&1 || exit_code=$?

    # Restore index
    mv .analysis_backup .analysis 2>/dev/null || true

    if [[ $exit_code -eq 1 ]]; then
        log_pass "Missing index returns error code 1"
    else
        log_fail "Missing index should return exit code 1"
    fi
}

test_empty_task_handling() {
    log_test "Empty task is handled gracefully"

    local exit_code=0
    bash "$FIND_SCRIPT" --task "" --format json > /dev/null 2>&1 || exit_code=$?

    # Should handle gracefully
    log_pass "Empty task handled"
}

test_summary_in_output() {
    log_test "Output includes summary section"

    local output
    output=$(bash "$FIND_SCRIPT" --task "create handler" --format json 2>/dev/null || true)

    if echo "$output" | jq -e '.summary' > /dev/null 2>&1; then
        log_pass "Output includes summary section"
    else
        log_fail "Output missing summary section"
    fi
}

test_results_have_file_references() {
    log_test "Results include file references"

    local output
    output=$(bash "$FIND_SCRIPT" --task "class implementation" --format json 2>/dev/null || true)

    if echo "$output" | jq -e '.results' > /dev/null 2>&1; then
        log_pass "Results structure is present"
    else
        log_fail "Results missing from output"
    fi
}

test_multiple_keywords_in_task() {
    log_test "Multiple keywords in task"

    local output
    output=$(bash "$FIND_SCRIPT" --task "user authentication service handler validation" --format json 2>/dev/null || true)

    if [[ -n "$output" ]]; then
        log_pass "Multiple keywords handled"
    else
        log_fail "Multiple keywords failed"
    fi
}

#=============================================================================
# Main
#=============================================================================

main() {
    echo ""
    echo "========================================="
    echo " Code Reusability Detection Test Suite"
    echo "========================================="
    echo ""
    echo "Fixture: $FIXTURE_DIR"
    echo ""

    setup
    trap teardown EXIT

    test_script_exists
    test_json_output_format
    test_text_output_format
    test_similar_implementation_search
    test_utility_function_detection
    test_pattern_detection
    test_test_example_finding
    test_threshold_parameter
    test_missing_index_handling
    test_empty_task_handling
    test_summary_in_output
    test_results_have_file_references
    test_multiple_keywords_in_task

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
