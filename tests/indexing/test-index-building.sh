#!/usr/bin/env bash
#
# test-index-building.sh - Test suite for index building scripts
#
# Usage: bash tests/indexing/test-index-building.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_SCRIPT="$REPO_ROOT/scripts/bash/build-codebase-index.sh"
FIXTURE_DIR="$REPO_ROOT/tests/fixtures/sample-projects/typescript-express"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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

run_test() {
    TESTS_RUN=$((TESTS_RUN + 1))
}

# Setup test environment
setup() {
    # Work in fixture directory
    cd "$FIXTURE_DIR"
    # Clean any existing index
    rm -rf .analysis
}

cleanup() {
    # Clean up test index
    cd "$FIXTURE_DIR"
    rm -rf .analysis
}

# Test 1: Build index on fixture project
test_build_index() {
    run_test
    log_test "Test 1: Build index on fixture project"

    cd "$FIXTURE_DIR"
    set +e
    OUTPUT=$(bash "$BUILD_SCRIPT" --verbose 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Index build completed successfully"
    else
        log_fail "Index build failed with exit code $EXIT_CODE"
        echo "Output: $OUTPUT"
        return
    fi

    # Check if index directory was created
    if [[ -d ".analysis/index" ]]; then
        log_pass "Index directory created"
    else
        log_fail "Index directory not found"
    fi

    # Check if all required files exist
    REQUIRED_FILES=(
        ".analysis/index/metadata.json"
        ".analysis/index/structure.json"
        ".analysis/index/data-models.json"
        ".analysis/index/api-endpoints.json"
        ".analysis/index/external-apis.json"
        ".analysis/index/dependencies.json"
    )

    for file in "${REQUIRED_FILES[@]}"; do
        if [[ -f "$file" ]]; then
            log_pass "File exists: $(basename "$file")"
        else
            log_fail "Missing file: $file"
        fi
    done
}

# Test 2: Validate structure extraction
test_structure_extraction() {
    run_test
    log_test "Test 2: Validate structure extraction"

    cd "$FIXTURE_DIR"

    if [[ ! -f ".analysis/index/structure.json" ]]; then
        log_fail "structure.json not found, skipping test"
        return
    fi

    # Check for expected classes
    if grep -q '"name":[[:space:]]*"User"' .analysis/index/structure.json; then
        log_pass "Found User class"
    else
        log_fail "User class not found in structure"
    fi

    if grep -q '"name":[[:space:]]*"AuthService"' .analysis/index/structure.json; then
        log_pass "Found AuthService class"
    else
        log_fail "AuthService class not found in structure"
    fi

    # Check for expected interface
    if grep -q '"name":[[:space:]]*"IUser"' .analysis/index/structure.json; then
        log_pass "Found IUser interface"
    else
        log_fail "IUser interface not found in structure"
    fi

    # Check for expected function
    if grep -q '"name":[[:space:]]*"validateEmail"' .analysis/index/structure.json; then
        log_pass "Found validateEmail function"
    else
        log_fail "validateEmail function not found in structure"
    fi
}

# Test 3: Validate metadata
test_metadata() {
    run_test
    log_test "Test 3: Validate metadata"

    cd "$FIXTURE_DIR"

    if [[ ! -f ".analysis/index/metadata.json" ]]; then
        log_fail "metadata.json not found, skipping test"
        return
    fi

    # Check required fields
    if grep -q '"version"' .analysis/index/metadata.json && \
       grep -q '"freshness"' .analysis/index/metadata.json && \
       grep -q '"statistics"' .analysis/index/metadata.json; then
        log_pass "All required metadata fields present"
    else
        log_fail "Missing required metadata fields"
    fi

    # Check statistics
    if grep -q '"total_files"' .analysis/index/metadata.json; then
        log_pass "Statistics include file counts"
    fi

    if grep -q '"total_classes"' .analysis/index/metadata.json; then
        log_pass "Statistics include class counts"
    fi
}

# Test 4: Incremental build
test_incremental_build() {
    run_test
    log_test "Test 4: Incremental build"

    cd "$FIXTURE_DIR"

    # First build is already done from test 1
    # Try incremental build
    set +e
    OUTPUT=$(bash "$BUILD_SCRIPT" --incremental 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Incremental build completed"
    else
        log_fail "Incremental build failed with exit code $EXIT_CODE"
        echo "Output: $OUTPUT"
    fi
}

# Main execution
main() {
    echo "========================================="
    echo "Index Building Test Suite"
    echo "========================================="
    echo ""
    echo "Testing fixture: $FIXTURE_DIR"
    echo ""

    setup
    trap cleanup EXIT

    test_build_index
    echo ""
    test_structure_extraction
    echo ""
    test_metadata
    echo ""
    test_incremental_build

    echo ""
    echo "========================================="
    echo "Test Results"
    echo "========================================="
    echo "Tests run: $TESTS_RUN"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    echo ""

    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some tests failed${NC}"
        exit 1
    fi
}

main "$@"
