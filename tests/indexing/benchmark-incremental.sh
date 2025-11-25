#!/usr/bin/env bash
#
# benchmark-incremental.sh - Benchmark incremental update performance
#
# Tests incremental update against spec targets:
# - Incremental update: < 5 seconds
# - No-change update: < 2 seconds
# - Single file change: < 3 seconds
# - Multiple file changes: < 5 seconds
#
# Usage: bash tests/indexing/benchmark-incremental.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
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

log_header() {
    echo ""
    echo -e "${CYAN}=========================================${NC}"
    echo -e "${CYAN} $* ${NC}"
    echo -e "${CYAN}=========================================${NC}"
    echo ""
}

log_metric() {
    printf "%-40s %s\n" "$1:" "$2"
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
    echo -e "${YELLOW}[INFO]${NC} $*"
}

# Get current time in milliseconds
get_time_ms() {
    if [[ "$(uname)" == "Darwin" ]]; then
        perl -MTime::HiRes=time -e 'printf "%.0f\n", time()*1000'
    else
        date +%s%3N
    fi
}

setup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis

    log_info "Building initial full index..."
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
}

cleanup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis
    rm -f src/temp-*.ts
}

#=============================================================================
# BENCHMARK 1: No Changes
#=============================================================================

benchmark_no_change() {
    log_header "Benchmark 1: Incremental Update (No Changes)"

    local TARGET_MS=2000  # 2 seconds

    cd "$FIXTURE_DIR"
    log_metric "Target time" "<${TARGET_MS}ms (2s)"

    # Run incremental with no changes
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Actual time" "${DURATION_MS}ms"

    if [[ $DURATION_MS -lt $TARGET_MS ]]; then
        log_pass "No-change incremental under target"
    else
        log_fail "No-change incremental exceeded target"
    fi
}

#=============================================================================
# BENCHMARK 2: Single File Change
#=============================================================================

benchmark_single_file() {
    log_header "Benchmark 2: Incremental Update (Single File Change)"

    local TARGET_MS=3000  # 3 seconds

    cd "$FIXTURE_DIR"
    log_metric "Target time" "<${TARGET_MS}ms (3s)"

    # Create a new file
    cat > src/temp-single.ts << 'EOF'
export interface TempEntity {
    id: string;
    name: string;
}

export class TempService {
    async getEntity(id: string): Promise<TempEntity> {
        return { id, name: 'test' };
    }
}
EOF

    # Run incremental
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Actual time" "${DURATION_MS}ms"

    if [[ $DURATION_MS -lt $TARGET_MS ]]; then
        log_pass "Single file incremental under target"
    else
        log_fail "Single file incremental exceeded target"
    fi

    # Cleanup
    rm -f src/temp-single.ts
}

#=============================================================================
# BENCHMARK 3: Multiple File Changes
#=============================================================================

benchmark_multiple_files() {
    log_header "Benchmark 3: Incremental Update (Multiple File Changes)"

    local TARGET_MS=5000  # 5 seconds
    local FILE_COUNT=10

    cd "$FIXTURE_DIR"
    log_metric "Files changed" "$FILE_COUNT"
    log_metric "Target time" "<${TARGET_MS}ms (5s)"

    # Create multiple new files
    for i in $(seq 1 $FILE_COUNT); do
        cat > "src/temp-multi-${i}.ts" << EOF
export interface TempEntity${i} {
    id: string;
    value: number;
}

export class TempService${i} {
    async process(): Promise<void> {
        console.log('Processing ${i}');
    }
}
EOF
    done

    # Run incremental
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Actual time" "${DURATION_MS}ms"

    if [[ $DURATION_MS -lt $TARGET_MS ]]; then
        log_pass "Multiple files incremental under target"
    else
        log_fail "Multiple files incremental exceeded target"
    fi

    # Calculate per-file rate
    local rate=$((DURATION_MS / FILE_COUNT))
    log_metric "Time per file" "${rate}ms"

    # Cleanup
    rm -f src/temp-multi-*.ts
}

#=============================================================================
# BENCHMARK 4: File Modification
#=============================================================================

benchmark_file_modification() {
    log_header "Benchmark 4: Incremental Update (File Modification)"

    local TARGET_MS=3000  # 3 seconds

    cd "$FIXTURE_DIR"
    log_metric "Target time" "<${TARGET_MS}ms (3s)"

    # Create initial file
    cat > src/temp-modify.ts << 'EOF'
export const VERSION = '1.0.0';
EOF

    # Build index with the file
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1

    # Modify the file
    sleep 1  # Ensure modification time changes
    cat > src/temp-modify.ts << 'EOF'
export const VERSION = '2.0.0';

export function newFunction(): string {
    return VERSION;
}
EOF

    # Run incremental
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Actual time" "${DURATION_MS}ms"

    if [[ $DURATION_MS -lt $TARGET_MS ]]; then
        log_pass "File modification incremental under target"
    else
        log_fail "File modification incremental exceeded target"
    fi

    # Cleanup
    rm -f src/temp-modify.ts
}

#=============================================================================
# BENCHMARK 5: File Deletion
#=============================================================================

benchmark_file_deletion() {
    log_header "Benchmark 5: Incremental Update (File Deletion)"

    local TARGET_MS=3000  # 3 seconds

    cd "$FIXTURE_DIR"
    log_metric "Target time" "<${TARGET_MS}ms (3s)"

    # Create files to delete
    for i in $(seq 1 5); do
        cat > "src/temp-delete-${i}.ts" << EOF
export const FILE_${i} = true;
EOF
    done

    # Build index with the files
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1

    # Delete the files
    rm -f src/temp-delete-*.ts

    # Run incremental
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Actual time" "${DURATION_MS}ms"

    if [[ $DURATION_MS -lt $TARGET_MS ]]; then
        log_pass "File deletion incremental under target"
    else
        log_fail "File deletion incremental exceeded target"
    fi
}

#=============================================================================
# BENCHMARK 6: Consistency Check
#=============================================================================

benchmark_consistency() {
    log_header "Benchmark 6: Incremental Consistency"

    local ITERATIONS=3

    cd "$FIXTURE_DIR"
    log_metric "Iterations" "$ITERATIONS"

    local TIMES=()
    for i in $(seq 1 $ITERATIONS); do
        START_MS=$(get_time_ms)
        bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
        END_MS=$(get_time_ms)
        DURATION=$((END_MS - START_MS))
        TIMES+=("$DURATION")
        log_metric "Run $i" "${DURATION}ms"
    done

    # Calculate average
    local TOTAL=0
    for t in "${TIMES[@]}"; do
        TOTAL=$((TOTAL + t))
    done
    local AVG=$((TOTAL / ITERATIONS))
    log_metric "Average" "${AVG}ms"

    # Calculate variance
    local MIN=${TIMES[0]}
    local MAX=${TIMES[0]}
    for t in "${TIMES[@]}"; do
        [[ $t -lt $MIN ]] && MIN=$t
        [[ $t -gt $MAX ]] && MAX=$t
    done
    local VARIANCE=$((MAX - MIN))
    log_metric "Variance (max-min)" "${VARIANCE}ms"

    # Check variance is acceptable (< 50% of average)
    local MAX_VARIANCE=$((AVG / 2))
    if [[ $VARIANCE -lt $MAX_VARIANCE ]]; then
        log_pass "Incremental timing is consistent"
    else
        log_fail "Incremental timing has high variance"
    fi
}

#=============================================================================
# Main
#=============================================================================

main() {
    echo ""
    echo -e "${CYAN}=========================================${NC}"
    echo -e "${CYAN}  INCREMENTAL UPDATE BENCHMARK SUITE    ${NC}"
    echo -e "${CYAN}=========================================${NC}"
    echo ""
    echo "Platform: $(uname -s)"
    echo "Fixture: $FIXTURE_DIR"
    echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo ""
    echo "Performance targets (from spec):"
    echo "  - Incremental update: < 5 seconds"
    echo "  - No changes: < 2 seconds"
    echo "  - Single file: < 3 seconds"
    echo ""

    setup
    trap cleanup EXIT

    benchmark_no_change
    benchmark_single_file
    benchmark_multiple_files
    benchmark_file_modification
    benchmark_file_deletion
    benchmark_consistency

    log_header "Benchmark Summary"

    echo "Tests run: $TESTS_RUN"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo ""

    if [[ $TESTS_FAILED -gt 0 ]]; then
        exit 1
    fi

    exit 0
}

main "$@"
