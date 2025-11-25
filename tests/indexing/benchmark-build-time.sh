#!/usr/bin/env bash
#
# benchmark-build-time.sh - Benchmark index build time for different project sizes
#
# Tests build time against spec targets:
# - <1K files: < 10 seconds
# - 1K-10K files: < 60 seconds
# - 10K-50K files: < 5 minutes
#
# Usage: bash tests/indexing/benchmark-build-time.sh [--size small|medium|large|all]
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_SCRIPT="$REPO_ROOT/scripts/bash/build-codebase-index.sh"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Benchmark parameters
SIZE="${1:-all}"
TEMP_DIR=""

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

# Create synthetic test project with specified file count
create_test_project() {
    local file_count="$1"
    local project_dir="$2"

    log_info "Creating test project with $file_count files..."

    mkdir -p "$project_dir/src/controllers"
    mkdir -p "$project_dir/src/services"
    mkdir -p "$project_dir/src/models"
    mkdir -p "$project_dir/src/utils"
    mkdir -p "$project_dir/tests"

    local created=0
    local dirs=("src/controllers" "src/services" "src/models" "src/utils" "tests")

    while [[ $created -lt $file_count ]]; do
        local dir_idx=$((created % ${#dirs[@]}))
        local dir="${dirs[$dir_idx]}"
        local file_num=$((created / ${#dirs[@]}))
        local file_path="$project_dir/$dir/file${file_num}.ts"

        # Generate realistic TypeScript content
        cat > "$file_path" << EOF
// File: $dir/file${file_num}.ts
// Generated for benchmarking

import { Logger } from '../utils/logger';
import { BaseService } from '../services/base';

export interface Entity${file_num} {
    id: string;
    name: string;
    createdAt: Date;
}

export class Service${file_num} extends BaseService {
    private logger: Logger;

    constructor() {
        super();
        this.logger = new Logger('Service${file_num}');
    }

    async getEntity(id: string): Promise<Entity${file_num}> {
        this.logger.info(\`Fetching entity \${id}\`);
        return { id, name: 'test', createdAt: new Date() };
    }

    async createEntity(data: Partial<Entity${file_num}>): Promise<Entity${file_num}> {
        return { id: 'new', ...data, createdAt: new Date() } as Entity${file_num};
    }

    async updateEntity(id: string, data: Partial<Entity${file_num}>): Promise<Entity${file_num}> {
        const entity = await this.getEntity(id);
        return { ...entity, ...data };
    }

    async deleteEntity(id: string): Promise<void> {
        this.logger.info(\`Deleting entity \${id}\`);
    }
}

export function processEntity${file_num}(entity: Entity${file_num}): string {
    return JSON.stringify(entity);
}
EOF
        ((created++))

        # Show progress every 100 files
        if [[ $((created % 100)) -eq 0 ]]; then
            echo -ne "\r  Created $created / $file_count files..."
        fi
    done

    echo -e "\r  Created $file_count files                     "
}

cleanup() {
    if [[ -n "$TEMP_DIR" ]] && [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

#=============================================================================
# BENCHMARK: Small Project (<1K files)
#=============================================================================

benchmark_small() {
    log_header "Benchmark: Small Project (<1K files)"

    TEMP_DIR=$(mktemp -d)
    trap cleanup EXIT

    local FILE_COUNT=500
    local TARGET_MS=10000  # 10 seconds

    create_test_project $FILE_COUNT "$TEMP_DIR"

    cd "$TEMP_DIR"
    log_metric "File count" "$FILE_COUNT"
    log_metric "Target time" "<${TARGET_MS}ms (10s)"

    # Run benchmark
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Actual time" "${DURATION_MS}ms"

    if [[ $DURATION_MS -lt $TARGET_MS ]]; then
        log_pass "Small project build time under target"
    else
        log_fail "Small project build time exceeded target"
    fi

    # Calculate rate
    local rate=$((DURATION_MS / FILE_COUNT))
    log_metric "Time per file" "${rate}ms"

    cleanup
    TEMP_DIR=""
}

#=============================================================================
# BENCHMARK: Medium Project (1K-10K files)
#=============================================================================

benchmark_medium() {
    log_header "Benchmark: Medium Project (1K-10K files)"

    TEMP_DIR=$(mktemp -d)
    trap cleanup EXIT

    local FILE_COUNT=2000
    local TARGET_MS=60000  # 60 seconds

    create_test_project $FILE_COUNT "$TEMP_DIR"

    cd "$TEMP_DIR"
    log_metric "File count" "$FILE_COUNT"
    log_metric "Target time" "<${TARGET_MS}ms (60s)"

    # Run benchmark
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Actual time" "${DURATION_MS}ms"

    if [[ $DURATION_MS -lt $TARGET_MS ]]; then
        log_pass "Medium project build time under target"
    else
        log_fail "Medium project build time exceeded target"
    fi

    # Calculate rate
    local rate=$((DURATION_MS / FILE_COUNT))
    log_metric "Time per file" "${rate}ms"

    cleanup
    TEMP_DIR=""
}

#=============================================================================
# BENCHMARK: Large Project (10K-50K files)
#=============================================================================

benchmark_large() {
    log_header "Benchmark: Large Project (10K-50K files)"

    log_info "Note: Large benchmark creates 10K+ files and takes several minutes"
    log_info "Skipping by default. Use --size large to run this benchmark."

    if [[ "$SIZE" != "large" ]] && [[ "$SIZE" != "all" ]]; then
        log_info "Skipped (use --size large to run)"
        return
    fi

    TEMP_DIR=$(mktemp -d)
    trap cleanup EXIT

    local FILE_COUNT=10000
    local TARGET_MS=300000  # 5 minutes

    create_test_project $FILE_COUNT "$TEMP_DIR"

    cd "$TEMP_DIR"
    log_metric "File count" "$FILE_COUNT"
    log_metric "Target time" "<${TARGET_MS}ms (5min)"

    # Run benchmark
    START_MS=$(get_time_ms)
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
    END_MS=$(get_time_ms)
    DURATION_MS=$((END_MS - START_MS))

    log_metric "Actual time" "${DURATION_MS}ms ($((DURATION_MS / 1000))s)"

    if [[ $DURATION_MS -lt $TARGET_MS ]]; then
        log_pass "Large project build time under target"
    else
        log_fail "Large project build time exceeded target"
    fi

    # Calculate rate
    local rate=$((DURATION_MS / FILE_COUNT))
    log_metric "Time per file" "${rate}ms"

    cleanup
    TEMP_DIR=""
}

#=============================================================================
# Main
#=============================================================================

main() {
    echo ""
    echo -e "${CYAN}=========================================${NC}"
    echo -e "${CYAN}   INDEX BUILD TIME BENCHMARK SUITE     ${NC}"
    echo -e "${CYAN}=========================================${NC}"
    echo ""
    echo "Platform: $(uname -s)"
    echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo ""
    echo "Performance targets (from spec):"
    echo "  - Small (<1K files): < 10 seconds"
    echo "  - Medium (1K-10K files): < 60 seconds"
    echo "  - Large (10K-50K files): < 5 minutes"
    echo ""

    case "$SIZE" in
        small)
            benchmark_small
            ;;
        medium)
            benchmark_medium
            ;;
        large)
            benchmark_large
            ;;
        all)
            benchmark_small
            benchmark_medium
            # Skip large by default unless explicitly requested
            log_info "Skipping large benchmark (use --size large to include)"
            ;;
        *)
            echo "Usage: $0 [--size small|medium|large|all]"
            exit 1
            ;;
    esac

    log_header "Benchmark Complete"
}

main "$@"
