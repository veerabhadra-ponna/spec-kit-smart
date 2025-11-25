#!/usr/bin/env bash
#
# test-question-categories.sh - Validation test suite for all 6 question categories
#
# Tests the knowledge base against sample questions from each category:
# 1. Architecture/patterns
# 2. Data models
# 3. API endpoints
# 4. External integrations
# 5. Authentication flows
# 6. Business logic
#
# Usage: bash tests/indexing/test-question-categories.sh
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
BLUE='\033[0;34m'
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

log_category() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE} Category: $*${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
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

# Run search and return exit code
search_query() {
    local query="$1"
    bash "$SEARCH_SCRIPT" --query "$query" --format json 2>/dev/null
    return $?
}

#=============================================================================
# CATEGORY 1: Architecture/Patterns
#=============================================================================

test_architecture_patterns() {
    log_category "1. Architecture/Patterns"

    local questions=(
        "What architectural patterns are used?"
        "How is the codebase organized?"
        "What design patterns are implemented?"
        "Where is the service layer?"
        "How are controllers structured?"
    )

    for question in "${questions[@]}"; do
        log_test "Q: $question"
        if search_query "$question" > /dev/null; then
            log_pass "Query handled successfully"
        else
            log_fail "Query failed"
        fi
    done
}

#=============================================================================
# CATEGORY 2: Data Models
#=============================================================================

test_data_models() {
    log_category "2. Data Models"

    local questions=(
        "What data models exist?"
        "How are entities defined?"
        "What is the database schema?"
        "Where are types defined?"
        "What interfaces are used for data?"
    )

    for question in "${questions[@]}"; do
        log_test "Q: $question"
        if search_query "$question" > /dev/null; then
            log_pass "Query handled successfully"
        else
            log_fail "Query failed"
        fi
    done
}

#=============================================================================
# CATEGORY 3: API Endpoints
#=============================================================================

test_api_endpoints() {
    log_category "3. API Endpoints"

    local questions=(
        "What API endpoints are available?"
        "How are routes defined?"
        "What REST endpoints exist?"
        "Where are HTTP handlers?"
        "What methods are exposed?"
    )

    for question in "${questions[@]}"; do
        log_test "Q: $question"
        if search_query "$question" > /dev/null; then
            log_pass "Query handled successfully"
        else
            log_fail "Query failed"
        fi
    done
}

#=============================================================================
# CATEGORY 4: External Integrations
#=============================================================================

test_external_integrations() {
    log_category "4. External Integrations"

    local questions=(
        "What external APIs are used?"
        "What third-party services are integrated?"
        "Where are external calls made?"
        "What SDKs are used?"
        "How are external dependencies managed?"
    )

    for question in "${questions[@]}"; do
        log_test "Q: $question"
        if search_query "$question" > /dev/null; then
            log_pass "Query handled successfully"
        else
            log_fail "Query failed"
        fi
    done
}

#=============================================================================
# CATEGORY 5: Authentication Flows
#=============================================================================

test_authentication_flows() {
    log_category "5. Authentication Flows"

    local questions=(
        "How is authentication implemented?"
        "Where is user login handled?"
        "What auth middleware exists?"
        "How are sessions managed?"
        "Where is authorization checked?"
    )

    for question in "${questions[@]}"; do
        log_test "Q: $question"
        if search_query "$question" > /dev/null; then
            log_pass "Query handled successfully"
        else
            log_fail "Query failed"
        fi
    done
}

#=============================================================================
# CATEGORY 6: Business Logic
#=============================================================================

test_business_logic() {
    log_category "6. Business Logic"

    local questions=(
        "Where is the main business logic?"
        "How are core functions implemented?"
        "What services handle business rules?"
        "Where is data validation done?"
        "How are calculations performed?"
    )

    for question in "${questions[@]}"; do
        log_test "Q: $question"
        if search_query "$question" > /dev/null; then
            log_pass "Query handled successfully"
        else
            log_fail "Query failed"
        fi
    done
}

#=============================================================================
# VALIDATION SUMMARY
#=============================================================================

print_category_coverage() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN} Question Category Coverage Summary${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "1. Architecture/Patterns  - 5 sample questions"
    echo "2. Data Models            - 5 sample questions"
    echo "3. API Endpoints          - 5 sample questions"
    echo "4. External Integrations  - 5 sample questions"
    echo "5. Authentication Flows   - 5 sample questions"
    echo "6. Business Logic         - 5 sample questions"
    echo ""
    echo "Total: 30 sample questions across 6 categories"
    echo ""
}

#=============================================================================
# Main
#=============================================================================

main() {
    echo ""
    echo "========================================="
    echo " Question Categories Validation Suite"
    echo "========================================="
    echo ""
    echo "Fixture: $FIXTURE_DIR"
    echo ""
    echo "This test validates that the knowledge base"
    echo "can handle questions from all 6 categories"
    echo "specified in the requirements."

    setup
    trap teardown EXIT

    test_architecture_patterns
    test_data_models
    test_api_endpoints
    test_external_integrations
    test_authentication_flows
    test_business_logic

    print_category_coverage

    echo ""
    echo "========================================="
    echo " Test Results"
    echo "========================================="
    echo ""
    echo "Tests run:    $TESTS_RUN"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo ""

    local pass_rate=$((TESTS_PASSED * 100 / TESTS_RUN))
    echo "Pass rate: ${pass_rate}%"
    echo ""

    if [[ $pass_rate -ge 80 ]]; then
        echo -e "${GREEN}✓ Knowledge base meets category coverage requirements${NC}"
    else
        echo -e "${YELLOW}⚠ Knowledge base may need improvement for full category coverage${NC}"
    fi
    echo ""

    if [[ $TESTS_FAILED -gt 0 ]]; then
        exit 1
    fi

    exit 0
}

main "$@"
