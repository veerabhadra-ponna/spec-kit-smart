#!/usr/bin/env bash
#
# test-analyze-integration.sh - Test suite for analyze-project integration
#
# This test validates that:
# - Index data loader scripts work correctly
# - Optional prerequisite checks behave properly
# - Pre-extracted data is correctly formatted for analysis
# - Staleness warnings work as expected
#
# Usage: bash tests/indexing/test-analyze-integration.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_SCRIPT="$REPO_ROOT/scripts/bash/build-codebase-index.sh"
LOAD_SCRIPT="$REPO_ROOT/.specify/scripts/bash/load-index-for-analysis.sh"
OPTIONAL_CHECK="$REPO_ROOT/.specify/scripts/bash/check-index-optional.sh"
REQUIRED_CHECK="$REPO_ROOT/scripts/bash/check-index-prerequisite.sh"
FIXTURE_DIR="$REPO_ROOT/tests/fixtures/sample-projects/typescript-express"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_test() {
    echo -e "${YELLOW}[TEST]${NC} $*"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $*"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $*"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

run_test() {
    TESTS_RUN=$((TESTS_RUN + 1))
}

# Setup test environment
setup() {
    log_info "Setting up test environment..."
    cd "$FIXTURE_DIR"
    rm -rf .analysis
}

cleanup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis
}

build_index() {
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
}

#=============================================================================
# TEST GROUP 1: Script Existence
#=============================================================================

test_scripts_exist() {
    run_test
    log_test "Script Existence: All integration scripts exist"

    local all_exist=true

    if [[ -f "$LOAD_SCRIPT" ]]; then
        log_pass "load-index-for-analysis.sh exists"
    else
        log_fail "load-index-for-analysis.sh not found"
        all_exist=false
    fi

    if [[ -f "$OPTIONAL_CHECK" ]]; then
        log_pass "check-index-optional.sh exists"
    else
        log_fail "check-index-optional.sh not found"
        all_exist=false
    fi

    if [[ -f "$REQUIRED_CHECK" ]]; then
        log_pass "check-index-prerequisite.sh exists"
    else
        log_fail "check-index-prerequisite.sh not found"
        all_exist=false
    fi
}

#=============================================================================
# TEST GROUP 2: Optional Check - No Index
#=============================================================================

test_optional_check_no_index() {
    run_test
    log_test "Optional Check: Returns success when no index"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    OUTPUT=$(bash "$OPTIONAL_CHECK" 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Optional check exits with 0 when no index"
    else
        log_fail "Optional check should exit 0, got $EXIT_CODE"
    fi
}

test_optional_check_missing_status() {
    run_test
    log_test "Optional Check: Reports missing status"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    OUTPUT=$(bash "$OPTIONAL_CHECK" 2>&1)

    if echo "$OUTPUT" | jq -e '.status == "missing"' > /dev/null 2>&1; then
        log_pass "Reports status: missing"
    else
        log_fail "Should report status: missing"
    fi

    if echo "$OUTPUT" | jq -e '.continue_without_index == true' > /dev/null 2>&1; then
        log_pass "Reports continue_without_index: true"
    else
        log_fail "Should allow continuing without index"
    fi
}

test_optional_check_disabled_features() {
    run_test
    log_test "Optional Check: Lists disabled features"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    OUTPUT=$(bash "$OPTIONAL_CHECK" 2>&1)

    if echo "$OUTPUT" | jq -e '.disabled_features | length > 0' > /dev/null 2>&1; then
        log_pass "Lists disabled features"
    else
        log_fail "Should list disabled features"
    fi
}

#=============================================================================
# TEST GROUP 3: Optional Check - With Index
#=============================================================================

test_optional_check_with_index() {
    run_test
    log_test "Optional Check: Reports fresh index"

    cd "$FIXTURE_DIR"
    build_index

    OUTPUT=$(bash "$OPTIONAL_CHECK" 2>&1)

    if echo "$OUTPUT" | jq -e '.index_available == true' > /dev/null 2>&1; then
        log_pass "Reports index_available: true"
    else
        log_fail "Should report index_available: true"
    fi

    if echo "$OUTPUT" | jq -e '.status == "fresh"' > /dev/null 2>&1; then
        log_pass "Reports status: fresh"
    else
        log_fail "Should report status: fresh"
    fi
}

test_optional_check_enabled_features() {
    run_test
    log_test "Optional Check: Lists enabled features"

    cd "$FIXTURE_DIR"

    OUTPUT=$(bash "$OPTIONAL_CHECK" 2>&1)

    if echo "$OUTPUT" | jq -e '.enabled_features | length > 0' > /dev/null 2>&1; then
        log_pass "Lists enabled features"
    else
        log_fail "Should list enabled features"
    fi
}

test_optional_check_statistics() {
    run_test
    log_test "Optional Check: Includes statistics"

    cd "$FIXTURE_DIR"

    OUTPUT=$(bash "$OPTIONAL_CHECK" 2>&1)

    if echo "$OUTPUT" | jq -e '.files_indexed' > /dev/null 2>&1; then
        log_pass "Includes files_indexed"
    else
        log_fail "Should include files_indexed"
    fi

    if echo "$OUTPUT" | jq -e '.age_days >= 0' > /dev/null 2>&1; then
        log_pass "Includes age_days"
    else
        log_fail "Should include age_days"
    fi
}

#=============================================================================
# TEST GROUP 4: Required Check - No Index
#=============================================================================

test_required_check_no_index() {
    run_test
    log_test "Required Check: Fails when no index"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    OUTPUT=$(bash "$REQUIRED_CHECK" 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 1 ]]; then
        log_pass "Required check exits with 1 when no index"
    else
        log_fail "Required check should exit 1, got $EXIT_CODE"
    fi
}

test_required_check_error_message() {
    run_test
    log_test "Required Check: Provides error message"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    OUTPUT=$(bash "$REQUIRED_CHECK" 2>&1)
    set -e

    if echo "$OUTPUT" | jq -e '.error' > /dev/null 2>&1; then
        log_pass "Provides error message"
    else
        log_fail "Should provide error message"
    fi
}

#=============================================================================
# TEST GROUP 5: Required Check - With Index
#=============================================================================

test_required_check_with_index() {
    run_test
    log_test "Required Check: Succeeds with valid index"

    cd "$FIXTURE_DIR"
    build_index

    set +e
    OUTPUT=$(bash "$REQUIRED_CHECK" 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Required check exits with 0 when index exists"
    else
        log_fail "Required check should exit 0, got $EXIT_CODE"
    fi
}

test_required_check_returns_metadata() {
    run_test
    log_test "Required Check: Returns metadata"

    cd "$FIXTURE_DIR"

    OUTPUT=$(bash "$REQUIRED_CHECK" 2>&1)

    if echo "$OUTPUT" | jq -e '.index_exists == true' > /dev/null 2>&1; then
        log_pass "Reports index_exists: true"
    else
        log_fail "Should report index_exists: true"
    fi

    if echo "$OUTPUT" | jq -e '.freshness' > /dev/null 2>&1; then
        log_pass "Returns freshness timestamp"
    else
        log_fail "Should return freshness timestamp"
    fi
}

#=============================================================================
# TEST GROUP 6: Index Data Loader
#=============================================================================

test_loader_json_output() {
    run_test
    log_test "Data Loader: JSON output format"

    cd "$FIXTURE_DIR"
    build_index

    set +e
    OUTPUT=$(bash "$LOAD_SCRIPT" --format json --section all 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Loader exits with 0"
    else
        log_fail "Loader should exit 0, got $EXIT_CODE"
    fi

    if echo "$OUTPUT" | jq empty 2>/dev/null; then
        log_pass "Output is valid JSON"
    else
        log_fail "Output is not valid JSON"
    fi
}

test_loader_contains_sections() {
    run_test
    log_test "Data Loader: Contains all sections"

    cd "$FIXTURE_DIR"

    OUTPUT=$(bash "$LOAD_SCRIPT" --format json --section all 2>&1)

    if echo "$OUTPUT" | jq -e '.metadata' > /dev/null 2>&1; then
        log_pass "Contains metadata section"
    else
        log_fail "Missing metadata section"
    fi

    if echo "$OUTPUT" | jq -e '.structure' > /dev/null 2>&1; then
        log_pass "Contains structure section"
    else
        log_fail "Missing structure section"
    fi

    if echo "$OUTPUT" | jq -e '.api_endpoints' > /dev/null 2>&1; then
        log_pass "Contains api_endpoints section"
    else
        log_fail "Missing api_endpoints section"
    fi

    if echo "$OUTPUT" | jq -e '.external_apis' > /dev/null 2>&1; then
        log_pass "Contains external_apis section"
    else
        log_fail "Missing external_apis section"
    fi
}

test_loader_section_filter() {
    run_test
    log_test "Data Loader: Section filter works"

    cd "$FIXTURE_DIR"

    # Test structure section only
    OUTPUT=$(bash "$LOAD_SCRIPT" --format json --section structure 2>&1)

    if echo "$OUTPUT" | jq -e '.classes' > /dev/null 2>&1; then
        log_pass "Structure section contains classes"
    else
        log_fail "Structure section should contain classes"
    fi

    # Test api-endpoints section only
    OUTPUT=$(bash "$LOAD_SCRIPT" --format json --section api-endpoints 2>&1)

    if echo "$OUTPUT" | jq -e '.rest_endpoints' > /dev/null 2>&1; then
        log_pass "API endpoints section contains rest_endpoints"
    else
        log_fail "API endpoints section should contain rest_endpoints"
    fi
}

test_loader_summary_output() {
    run_test
    log_test "Data Loader: Summary format"

    cd "$FIXTURE_DIR"

    OUTPUT=$(bash "$LOAD_SCRIPT" --format summary 2>&1)

    if echo "$OUTPUT" | grep -q "Codebase Index Summary"; then
        log_pass "Summary format has header"
    else
        log_fail "Summary format missing header"
    fi

    if echo "$OUTPUT" | grep -q "Statistics"; then
        log_pass "Summary includes statistics"
    else
        log_fail "Summary missing statistics"
    fi
}

test_loader_no_index() {
    run_test
    log_test "Data Loader: Handles missing index"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    OUTPUT=$(bash "$LOAD_SCRIPT" --format json 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 1 ]]; then
        log_pass "Loader exits with 1 when no index"
    else
        log_fail "Loader should exit 1 when no index"
    fi
}

#=============================================================================
# TEST GROUP 7: Data Quality
#=============================================================================

test_loaded_data_classes() {
    run_test
    log_test "Data Quality: Classes loaded correctly"

    cd "$FIXTURE_DIR"
    build_index

    OUTPUT=$(bash "$LOAD_SCRIPT" --format json --section structure 2>&1)

    if echo "$OUTPUT" | jq -e '.classes[]? | select(.name == "User")' > /dev/null 2>&1; then
        log_pass "User class present in loaded data"
    else
        log_fail "User class missing from loaded data"
    fi

    if echo "$OUTPUT" | jq -e '.classes[]? | select(.name == "AuthService")' > /dev/null 2>&1; then
        log_pass "AuthService class present in loaded data"
    else
        log_fail "AuthService class missing from loaded data"
    fi
}

test_loaded_data_endpoints() {
    run_test
    log_test "Data Quality: Endpoints loaded correctly"

    cd "$FIXTURE_DIR"

    OUTPUT=$(bash "$LOAD_SCRIPT" --format json --section api-endpoints 2>&1)

    if echo "$OUTPUT" | jq -e '.rest_endpoints[]? | select(.path == "/login")' > /dev/null 2>&1; then
        log_pass "/login endpoint present in loaded data"
    else
        log_fail "/login endpoint missing from loaded data"
    fi
}

test_loaded_data_external_apis() {
    run_test
    log_test "Data Quality: External APIs loaded correctly"

    cd "$FIXTURE_DIR"

    OUTPUT=$(bash "$LOAD_SCRIPT" --format json --section external-apis 2>&1)

    if echo "$OUTPUT" | jq -e '.third_party_services[]? | select(.service == "stripe")' > /dev/null 2>&1; then
        log_pass "Stripe service present in loaded data"
    else
        log_fail "Stripe service missing from loaded data"
    fi
}

#=============================================================================
# Main Execution
#=============================================================================

main() {
    echo "========================================="
    echo "Analyze-Project Integration Test Suite"
    echo "========================================="
    echo ""
    echo "Testing fixture: $FIXTURE_DIR"
    echo ""

    setup
    trap cleanup EXIT

    echo ""
    echo "--- Test Group 1: Script Existence ---"
    test_scripts_exist

    echo ""
    echo "--- Test Group 2: Optional Check - No Index ---"
    test_optional_check_no_index
    test_optional_check_missing_status
    test_optional_check_disabled_features

    echo ""
    echo "--- Test Group 3: Optional Check - With Index ---"
    test_optional_check_with_index
    test_optional_check_enabled_features
    test_optional_check_statistics

    echo ""
    echo "--- Test Group 4: Required Check - No Index ---"
    test_required_check_no_index
    test_required_check_error_message

    echo ""
    echo "--- Test Group 5: Required Check - With Index ---"
    test_required_check_with_index
    test_required_check_returns_metadata

    echo ""
    echo "--- Test Group 6: Index Data Loader ---"
    test_loader_json_output
    test_loader_contains_sections
    test_loader_section_filter
    test_loader_summary_output
    test_loader_no_index

    echo ""
    echo "--- Test Group 7: Data Quality ---"
    test_loaded_data_classes
    test_loaded_data_endpoints
    test_loaded_data_external_apis

    echo ""
    echo "========================================="
    echo "Test Results"
    echo "========================================="
    echo "Tests run: $TESTS_RUN"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    echo ""

    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ All analyze integration tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some analyze integration tests failed${NC}"
        exit 1
    fi
}

main "$@"
