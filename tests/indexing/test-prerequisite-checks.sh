#!/usr/bin/env bash
#
# test-prerequisite-checks.sh - Test suite for prerequisite check scripts
#
# Usage: bash tests/indexing/test-prerequisite-checks.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PREREQ_SCRIPT="$REPO_ROOT/scripts/bash/check-index-prerequisite.sh"

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
    TEST_DIR=$(mktemp -d)
    TEST_INDEX_DIR="$TEST_DIR/.analysis/index"
    echo "Test directory: $TEST_DIR"
}

cleanup() {
    if [[ -n "${TEST_DIR:-}" ]] && [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
    fi
}

# Test 1: No index exists
test_no_index() {
    run_test
    log_test "Test 1: No index exists"

    cd "$TEST_DIR"
    set +e
    OUTPUT=$(bash "$PREREQ_SCRIPT" 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 1 ]] && echo "$OUTPUT" | grep -q '"index_exists":[[:space:]]*false'; then
        log_pass "Correctly reports index not found"
        if echo "$OUTPUT" | grep -q '"error"'; then
            log_pass "Error message provided"
        fi
    else
        log_fail "Should return exit code 1 and index_exists=false"
        echo "Output: $OUTPUT"
        echo "Exit code: $EXIT_CODE"
    fi
}

# Test 2: Index exists with valid metadata
test_valid_index() {
    run_test
    log_test "Test 2: Valid index exists"

    mkdir -p "$TEST_INDEX_DIR"

    # Create valid metadata.json
    cat > "$TEST_INDEX_DIR/metadata.json" <<EOF
{
  "version": "1.0",
  "created_by_version": "1.0.0",
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "freshness": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "statistics": {
    "total_files": 10,
    "indexed_files": 10,
    "skipped_files": 0
  }
}
EOF

    cd "$TEST_DIR"
    OUTPUT=$(bash "$PREREQ_SCRIPT" 2>&1)
    EXIT_CODE=$?

    if [[ $EXIT_CODE -eq 0 ]] && echo "$OUTPUT" | grep -q '"index_exists":[[:space:]]*true'; then
        log_pass "Correctly reports valid index"

        # Check required fields
        if echo "$OUTPUT" | grep -q '"index_path"' && \
           echo "$OUTPUT" | grep -q '"freshness"' && \
           echo "$OUTPUT" | grep -q '"files_indexed"'; then
            log_pass "All required fields present"
        else
            log_fail "Missing required fields in output"
            echo "Output: $OUTPUT"
        fi
    else
        log_fail "Should return exit code 0 and index_exists=true"
        echo "Output: $OUTPUT"
        echo "Exit code: $EXIT_CODE"
    fi
}

# Test 3: Index exists but metadata is corrupted
test_corrupted_metadata() {
    run_test
    log_test "Test 3: Corrupted metadata"

    mkdir -p "$TEST_INDEX_DIR"
    echo "invalid json" > "$TEST_INDEX_DIR/metadata.json"

    cd "$TEST_DIR"
    set +e
    OUTPUT=$(bash "$PREREQ_SCRIPT" 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 1 ]] && echo "$OUTPUT" | grep -q '"index_exists":[[:space:]]*false'; then
        log_pass "Correctly detects corrupted metadata"
    else
        log_fail "Should return exit code 1 for corrupted metadata"
        echo "Output: $OUTPUT"
        echo "Exit code: $EXIT_CODE"
    fi
}

# Test 4: Stale index (>7 days old)
test_stale_index() {
    run_test
    log_test "Test 4: Stale index detection"

    mkdir -p "$TEST_INDEX_DIR"

    # Create metadata with old timestamp (10 days ago)
    OLD_DATE=$(date -u -d "10 days ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -v-10d +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null)

    cat > "$TEST_INDEX_DIR/metadata.json" <<EOF
{
  "version": "1.0",
  "created_by_version": "1.0.0",
  "generated_at": "$OLD_DATE",
  "freshness": "$OLD_DATE",
  "statistics": {
    "total_files": 10,
    "indexed_files": 10,
    "skipped_files": 0
  }
}
EOF

    cd "$TEST_DIR"
    OUTPUT=$(bash "$PREREQ_SCRIPT" 2>&1)
    EXIT_CODE=$?

    if [[ $EXIT_CODE -eq 0 ]] && echo "$OUTPUT" | grep -q '"is_stale":[[:space:]]*true'; then
        log_pass "Correctly detects stale index"

        # Extract age_days using grep and sed
        if echo "$OUTPUT" | grep -q '"age_days"'; then
            log_pass "Age calculation included in output"
        fi
    else
        log_fail "Should detect stale index"
        echo "Output: $OUTPUT"
        echo "Exit code: $EXIT_CODE"
    fi
}

# Main execution
main() {
    echo "========================================="
    echo "Prerequisite Check Test Suite"
    echo "========================================="
    echo ""

    setup
    trap cleanup EXIT

    test_no_index
    test_valid_index
    test_corrupted_metadata
    test_stale_index

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
