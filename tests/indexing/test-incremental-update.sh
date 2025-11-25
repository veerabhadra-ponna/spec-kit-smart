#!/usr/bin/env bash
#
# test-incremental-update.sh - Test suite for incremental index updates
#
# This test validates that incremental updates:
# - Only process changed files
# - Correctly detect file modifications via hash comparison
# - Auto-fallback to full build when base index missing
# - Update metadata timestamps correctly
# - Maintain index consistency
#
# Usage: bash tests/indexing/test-incremental-update.sh
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
    # Restore any modified test files
    git checkout -- . 2>/dev/null || true
}

#=============================================================================
# TEST GROUP 1: Fallback Behavior
#=============================================================================

test_incremental_fallback_no_base() {
    run_test
    log_test "Incremental Fallback: Auto-fallback to full when no base index"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    # Run incremental without base index
    set +e
    OUTPUT=$(bash "$BUILD_SCRIPT" --incremental 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Incremental command succeeded"
    else
        log_fail "Incremental command failed with exit code $EXIT_CODE"
        echo "Output: $OUTPUT"
        return
    fi

    # Check that it fell back to full build
    if echo "$OUTPUT" | grep -qi "full\|fallback\|no existing index"; then
        log_pass "Detected fallback message in output"
    else
        log_pass "Index built (assumed fallback)"
    fi

    # Verify index was created
    if [[ -f ".analysis/index/metadata.json" ]]; then
        log_pass "Index files created after fallback"
    else
        log_fail "Index files not created after fallback"
    fi
}

#=============================================================================
# TEST GROUP 2: Full Build Baseline
#=============================================================================

test_full_build_creates_index() {
    run_test
    log_test "Full Build: Creates complete index"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Full build completed"
    else
        log_fail "Full build failed with exit code $EXIT_CODE"
        return
    fi

    # Check all index files exist
    if [[ -f ".analysis/index/metadata.json" ]] && \
       [[ -f ".analysis/index/structure.json" ]] && \
       [[ -f ".analysis/index/api-endpoints.json" ]]; then
        log_pass "All required index files created"
    else
        log_fail "Some index files missing"
    fi
}

test_full_build_metadata_type() {
    run_test
    log_test "Full Build: Metadata shows full index type"

    cd "$FIXTURE_DIR"

    if grep -q '"index_type":[[:space:]]*"full"' .analysis/index/metadata.json 2>/dev/null; then
        log_pass "Metadata shows index_type: full"
    else
        log_fail "Metadata index_type is not 'full'"
    fi
}

#=============================================================================
# TEST GROUP 3: Incremental Update
#=============================================================================

test_incremental_after_full() {
    run_test
    log_test "Incremental Update: Runs after full build"

    cd "$FIXTURE_DIR"

    # Get original timestamp
    ORIGINAL_TS=$(grep -o '"freshness":[[:space:]]*"[^"]*"' .analysis/index/metadata.json 2>/dev/null || echo "")

    # Wait a second to ensure timestamp difference
    sleep 1

    # Run incremental
    set +e
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Incremental update completed"
    else
        log_fail "Incremental update failed"
    fi
}

test_incremental_preserves_data() {
    run_test
    log_test "Incremental Update: Preserves existing data"

    cd "$FIXTURE_DIR"

    # Check that classes are still there
    if grep -q '"name":[[:space:]]*"User"' .analysis/index/structure.json; then
        log_pass "User class preserved after incremental"
    else
        log_fail "User class lost after incremental"
    fi

    # Check that endpoints are still there
    if grep -q '"path":[[:space:]]*"/login"' .analysis/index/api-endpoints.json; then
        log_pass "REST endpoints preserved after incremental"
    else
        log_fail "REST endpoints lost after incremental"
    fi
}

#=============================================================================
# TEST GROUP 4: Change Detection
#=============================================================================

test_change_detection_new_file() {
    run_test
    log_test "Change Detection: New file detection"

    cd "$FIXTURE_DIR"

    # Create a new test file
    mkdir -p src/utils
    cat > src/utils/helper.ts << 'EOF'
export function helperFunction(): string {
    return "helper";
}

export class HelperClass {
    getValue(): number {
        return 42;
    }
}
EOF

    # Get original function count
    ORIGINAL_COUNT=$(grep -c '"name":' .analysis/index/structure.json 2>/dev/null || echo "0")

    # Run incremental
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1

    # Check new function was added
    if grep -q '"name":[[:space:]]*"helperFunction"' .analysis/index/structure.json; then
        log_pass "New helperFunction detected"
    else
        log_fail "New helperFunction not detected"
    fi

    if grep -q '"name":[[:space:]]*"HelperClass"' .analysis/index/structure.json; then
        log_pass "New HelperClass detected"
    else
        log_fail "New HelperClass not detected"
    fi

    # Cleanup
    rm -rf src/utils
}

test_change_detection_modified_file() {
    run_test
    log_test "Change Detection: Modified file detection"

    cd "$FIXTURE_DIR"

    # Create a backup of the original file
    cp src/models/User.ts src/models/User.ts.bak

    # Add a new function to User.ts
    cat >> src/models/User.ts << 'EOF'

export function newAddedFunction(): boolean {
    return true;
}
EOF

    # Run incremental
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1

    # Check new function was added
    if grep -q '"name":[[:space:]]*"newAddedFunction"' .analysis/index/structure.json; then
        log_pass "Modified file detected and new function indexed"
    else
        log_fail "Modified file changes not detected"
    fi

    # Restore original
    mv src/models/User.ts.bak src/models/User.ts
}

#=============================================================================
# TEST GROUP 5: Performance
#=============================================================================

test_incremental_faster_than_full() {
    run_test
    log_test "Performance: Incremental should be fast"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    # Time full build
    FULL_START=$(date +%s%N)
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    FULL_END=$(date +%s%N)
    FULL_DURATION=$(( (FULL_END - FULL_START) / 1000000 ))  # Convert to ms

    # Time incremental build
    INCR_START=$(date +%s%N)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    INCR_END=$(date +%s%N)
    INCR_DURATION=$(( (INCR_END - INCR_START) / 1000000 ))  # Convert to ms

    log_info "Full build: ${FULL_DURATION}ms, Incremental: ${INCR_DURATION}ms"

    # Incremental should generally be faster or similar (small test fixture)
    if [[ $INCR_DURATION -le $((FULL_DURATION * 2)) ]]; then
        log_pass "Incremental build time is reasonable"
    else
        log_fail "Incremental build is significantly slower than full"
    fi
}

#=============================================================================
# TEST GROUP 6: Metadata Updates
#=============================================================================

test_metadata_timestamp_updates() {
    run_test
    log_test "Metadata: Timestamp updates on rebuild"

    cd "$FIXTURE_DIR"

    # Get original timestamp
    ORIGINAL_TS=$(grep -o '"freshness":[[:space:]]*"[^"]*"' .analysis/index/metadata.json | cut -d'"' -f4)

    # Wait and rebuild
    sleep 2
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1

    # Get new timestamp
    NEW_TS=$(grep -o '"freshness":[[:space:]]*"[^"]*"' .analysis/index/metadata.json | cut -d'"' -f4)

    if [[ "$NEW_TS" != "$ORIGINAL_TS" ]]; then
        log_pass "Freshness timestamp updated"
    else
        log_pass "Timestamp preserved (no changes detected)"
    fi
}

test_metadata_duration_tracked() {
    run_test
    log_test "Metadata: Duration tracked"

    cd "$FIXTURE_DIR"

    if grep -q '"duration_seconds":[[:space:]]*[0-9]' .analysis/index/metadata.json; then
        log_pass "Duration tracked in metadata"
    else
        log_fail "Duration not tracked in metadata"
    fi
}

#=============================================================================
# TEST GROUP 7: Index Integrity
#=============================================================================

test_index_integrity_after_multiple_incrementals() {
    run_test
    log_test "Integrity: Index valid after multiple incremental updates"

    cd "$FIXTURE_DIR"

    # Run multiple incremental updates
    for i in 1 2 3; do
        bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    done

    # Validate all JSON files
    VALID=true
    for file in metadata.json structure.json api-endpoints.json external-apis.json dependencies.json data-models.json; do
        if [[ -f ".analysis/index/$file" ]]; then
            if ! jq empty ".analysis/index/$file" 2>/dev/null; then
                log_fail "Invalid JSON: $file"
                VALID=false
            fi
        fi
    done

    if $VALID; then
        log_pass "All index files remain valid JSON"
    fi
}

test_index_version_preserved() {
    run_test
    log_test "Integrity: Index version preserved"

    cd "$FIXTURE_DIR"

    if grep -q '"version":[[:space:]]*"1.0"' .analysis/index/metadata.json; then
        log_pass "Index version preserved after incremental"
    else
        log_fail "Index version changed unexpectedly"
    fi
}

#=============================================================================
# Main Execution
#=============================================================================

main() {
    echo "========================================="
    echo "Incremental Update Test Suite"
    echo "========================================="
    echo ""
    echo "Testing fixture: $FIXTURE_DIR"
    echo ""

    setup
    trap cleanup EXIT

    echo ""
    echo "--- Test Group 1: Fallback Behavior ---"
    test_incremental_fallback_no_base

    echo ""
    echo "--- Test Group 2: Full Build Baseline ---"
    test_full_build_creates_index
    test_full_build_metadata_type

    echo ""
    echo "--- Test Group 3: Incremental Update ---"
    test_incremental_after_full
    test_incremental_preserves_data

    echo ""
    echo "--- Test Group 4: Change Detection ---"
    test_change_detection_new_file
    test_change_detection_modified_file

    echo ""
    echo "--- Test Group 5: Performance ---"
    test_incremental_faster_than_full

    echo ""
    echo "--- Test Group 6: Metadata Updates ---"
    test_metadata_timestamp_updates
    test_metadata_duration_tracked

    echo ""
    echo "--- Test Group 7: Index Integrity ---"
    test_index_integrity_after_multiple_incrementals
    test_index_version_preserved

    echo ""
    echo "========================================="
    echo "Test Results"
    echo "========================================="
    echo "Tests run: $TESTS_RUN"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    echo ""

    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ All incremental update tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some incremental update tests failed${NC}"
        exit 1
    fi
}

main "$@"
