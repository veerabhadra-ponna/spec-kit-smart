#!/usr/bin/env bash
#
# benchmark-analyze-performance.sh - Performance benchmark tests
#
# This script measures and compares:
# - Index build time for different project sizes
# - Incremental update performance vs full rebuild
# - Data loader performance
# - Memory usage during indexing (if possible)
#
# Usage: bash tests/indexing/benchmark-analyze-performance.sh
#
# Note: Results will vary based on hardware. These benchmarks establish
# baseline metrics to detect performance regressions.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_SCRIPT="$REPO_ROOT/scripts/bash/build-codebase-index.sh"
LOAD_SCRIPT="$REPO_ROOT/.specify/scripts/bash/load-index-for-analysis.sh"
FIXTURE_DIR="$REPO_ROOT/tests/fixtures/sample-projects/typescript-express"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
log_header() {
    echo ""
    echo -e "${CYAN}=========================================${NC}"
    echo -e "${CYAN} $* ${NC}"
    echo -e "${CYAN}=========================================${NC}"
    echo ""
}

log_metric() {
    printf "%-40s %s\n" "$1:" "$2"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $*"
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $*"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

# Get current time in milliseconds
get_time_ms() {
    if [[ "$(uname)" == "Darwin" ]]; then
        # macOS - use perl for ms precision
        perl -MTime::HiRes=time -e 'printf "%.0f\n", time()*1000'
    else
        # Linux - use date with nanoseconds
        date +%s%3N
    fi
}

# Setup
setup() {
    log_info "Setting up benchmark environment..."
    cd "$FIXTURE_DIR"
    rm -rf .analysis
}

cleanup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis
}

#=============================================================================
# BENCHMARK 1: Full Index Build Time
#=============================================================================

benchmark_full_build() {
    log_header "Benchmark 1: Full Index Build"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    # Count files to index
    FILE_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.js" \) ! -path "*/node_modules/*" ! -path "*/.analysis/*" | wc -l | tr -d ' ')
    log_metric "Files to index" "$FILE_COUNT"

    # Measure build time
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Full build time" "${DURATION_MS}ms"

    # Calculate rate
    if [[ $FILE_COUNT -gt 0 ]]; then
        RATE=$(echo "scale=2; $DURATION_MS / $FILE_COUNT" | bc 2>/dev/null || echo "N/A")
        log_metric "Time per file" "${RATE}ms"
    fi

    # Check against target (<10s for small projects)
    if [[ $DURATION_MS -lt 10000 ]]; then
        log_pass "Full build under 10 seconds target"
    else
        log_fail "Full build exceeded 10 seconds target"
    fi

    echo ""
}

#=============================================================================
# BENCHMARK 2: Incremental Update Time
#=============================================================================

benchmark_incremental_update() {
    log_header "Benchmark 2: Incremental Update"

    cd "$FIXTURE_DIR"

    # Ensure index exists
    if [[ ! -f ".analysis/index/metadata.json" ]]; then
        bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    fi

    # Measure incremental time (no changes)
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_NO_CHANGE=$((END_MS - START_MS))

    log_metric "Incremental (no changes)" "${DURATION_NO_CHANGE}ms"

    # Create a temp file to trigger change
    echo "export const tempTest = true;" > src/temp-test.ts

    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_WITH_CHANGE=$((END_MS - START_MS))

    log_metric "Incremental (1 new file)" "${DURATION_WITH_CHANGE}ms"

    # Cleanup temp file
    rm -f src/temp-test.ts

    # Check against target (<5s for single file)
    if [[ $DURATION_WITH_CHANGE -lt 5000 ]]; then
        log_pass "Incremental update under 5 seconds target"
    else
        log_fail "Incremental update exceeded 5 seconds target"
    fi

    echo ""
}

#=============================================================================
# BENCHMARK 3: Full Build vs Incremental Comparison
#=============================================================================

benchmark_comparison() {
    log_header "Benchmark 3: Full vs Incremental Comparison"

    cd "$FIXTURE_DIR"

    # Full build
    rm -rf .analysis
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    END_MS=$(get_time_ms)
    FULL_TIME=$((END_MS - START_MS))

    # Incremental (no changes)
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --incremental > /dev/null 2>&1
    END_MS=$(get_time_ms)
    INCR_TIME=$((END_MS - START_MS))

    log_metric "Full build" "${FULL_TIME}ms"
    log_metric "Incremental (no changes)" "${INCR_TIME}ms"

    if [[ $FULL_TIME -gt 0 ]]; then
        SPEEDUP=$(echo "scale=2; $FULL_TIME / ($INCR_TIME + 1)" | bc 2>/dev/null || echo "N/A")
        log_metric "Speedup ratio" "${SPEEDUP}x"
    fi

    echo ""
}

#=============================================================================
# BENCHMARK 4: Data Loader Performance
#=============================================================================

benchmark_data_loader() {
    log_header "Benchmark 4: Data Loader Performance"

    cd "$FIXTURE_DIR"

    # Ensure index exists
    if [[ ! -f ".analysis/index/metadata.json" ]]; then
        bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    fi

    # Load all sections
    START_MS=$(get_time_ms)
    bash "$LOAD_SCRIPT" --format json --section all > /dev/null 2>&1
    END_MS=$(get_time_ms)
    ALL_SECTIONS=$((END_MS - START_MS))

    log_metric "Load all sections" "${ALL_SECTIONS}ms"

    # Load individual sections
    for section in structure data-models api-endpoints external-apis dependencies; do
        START_MS=$(get_time_ms)
        bash "$LOAD_SCRIPT" --format json --section "$section" > /dev/null 2>&1
        END_MS=$(get_time_ms)
        SECTION_TIME=$((END_MS - START_MS))
        log_metric "Load $section" "${SECTION_TIME}ms"
    done

    # Summary format
    START_MS=$(get_time_ms)
    bash "$LOAD_SCRIPT" --format summary > /dev/null 2>&1
    END_MS=$(get_time_ms)
    SUMMARY_TIME=$((END_MS - START_MS))

    log_metric "Generate summary" "${SUMMARY_TIME}ms"

    echo ""
}

#=============================================================================
# BENCHMARK 5: Index File Sizes
#=============================================================================

benchmark_file_sizes() {
    log_header "Benchmark 5: Index File Sizes"

    cd "$FIXTURE_DIR"

    # Ensure index exists
    if [[ ! -f ".analysis/index/metadata.json" ]]; then
        bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    fi

    # Total index size
    TOTAL_SIZE=$(du -sh .analysis/index 2>/dev/null | cut -f1 || echo "N/A")
    log_metric "Total index size" "$TOTAL_SIZE"

    # Individual file sizes
    for file in metadata.json structure.json data-models.json api-endpoints.json external-apis.json dependencies.json; do
        if [[ -f ".analysis/index/$file" ]]; then
            SIZE=$(ls -lh ".analysis/index/$file" | awk '{print $5}')
            log_metric "$file" "$SIZE"
        fi
    done

    # Compare to source code size
    SOURCE_SIZE=$(du -sh . --exclude='.analysis' --exclude='node_modules' 2>/dev/null | cut -f1 || echo "N/A")
    log_metric "Source code size" "$SOURCE_SIZE"

    echo ""
}

#=============================================================================
# BENCHMARK 6: Multiple Builds
#=============================================================================

benchmark_consistency() {
    log_header "Benchmark 6: Build Time Consistency"

    cd "$FIXTURE_DIR"

    TIMES=()
    ITERATIONS=3

    log_info "Running $ITERATIONS full builds..."

    for i in $(seq 1 $ITERATIONS); do
        rm -rf .analysis
        START_MS=$(get_time_ms)
        bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
        END_MS=$(get_time_ms)
        DURATION=$((END_MS - START_MS))
        TIMES+=("$DURATION")
        log_metric "Build $i" "${DURATION}ms"
    done

    # Calculate average
    TOTAL=0
    for t in "${TIMES[@]}"; do
        TOTAL=$((TOTAL + t))
    done
    AVG=$((TOTAL / ITERATIONS))
    log_metric "Average" "${AVG}ms"

    # Calculate variance (simplified)
    MIN=${TIMES[0]}
    MAX=${TIMES[0]}
    for t in "${TIMES[@]}"; do
        [[ $t -lt $MIN ]] && MIN=$t
        [[ $t -gt $MAX ]] && MAX=$t
    done
    VARIANCE=$((MAX - MIN))
    log_metric "Variance (max-min)" "${VARIANCE}ms"

    echo ""
}

#=============================================================================
# Main Execution
#=============================================================================

main() {
    echo ""
    echo -e "${CYAN}=========================================${NC}"
    echo -e "${CYAN}   CODEBASE INDEXING BENCHMARK SUITE    ${NC}"
    echo -e "${CYAN}=========================================${NC}"
    echo ""
    echo "Platform: $(uname -s)"
    echo "Fixture: $FIXTURE_DIR"
    echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo ""

    setup
    trap cleanup EXIT

    benchmark_full_build
    benchmark_incremental_update
    benchmark_comparison
    benchmark_data_loader
    benchmark_file_sizes
    benchmark_consistency

    log_header "Benchmark Complete"

    echo "Performance targets (from spec):"
    echo "  - Full build <1K files: < 10 seconds"
    echo "  - Full build 1K-10K files: < 60 seconds"
    echo "  - Incremental update: < 5 seconds"
    echo "  - Query response: < 5 seconds"
    echo ""
    echo "Run on larger codebases for production benchmarks."
}

main "$@"
