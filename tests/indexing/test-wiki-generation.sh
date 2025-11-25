#!/usr/bin/env bash
#
# test-wiki-generation.sh - Test suite for DeepWiki generation
#
# Usage: bash tests/indexing/test-wiki-generation.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_SCRIPT="$REPO_ROOT/scripts/bash/build-codebase-index.sh"
WIKI_SCRIPT="$REPO_ROOT/.specify/scripts/bash/generate-deepwiki.sh"
FIXTURE_DIR="$REPO_ROOT/tests/fixtures/sample-projects/typescript-express"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_test() { echo -e "${YELLOW}[TEST]${NC} $*"; }
log_pass() { echo -e "${GREEN}[PASS]${NC} $*"; TESTS_PASSED=$((TESTS_PASSED + 1)); }
log_fail() { echo -e "${RED}[FAIL]${NC} $*"; TESTS_FAILED=$((TESTS_FAILED + 1)); }
run_test() { TESTS_RUN=$((TESTS_RUN + 1)); }

setup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis .deepwiki
    bash "$BUILD_SCRIPT" --full > /dev/null 2>&1
}

cleanup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis .deepwiki
}

test_wiki_script_exists() {
    run_test
    log_test "Script exists"
    if [[ -f "$WIKI_SCRIPT" ]]; then
        log_pass "Wiki generation script exists"
    else
        log_fail "Wiki generation script not found"
    fi
}

test_wiki_generates_files() {
    run_test
    log_test "Generates documentation files"
    cd "$FIXTURE_DIR"

    bash "$WIKI_SCRIPT" > /dev/null 2>&1

    if [[ -d ".deepwiki" ]]; then
        log_pass "Output directory created"
    else
        log_fail "Output directory not created"
        return
    fi

    if [[ -f ".deepwiki/index.md" ]]; then log_pass "index.md generated"; else log_fail "index.md missing"; fi
    if [[ -f ".deepwiki/overview.md" ]]; then log_pass "overview.md generated"; else log_fail "overview.md missing"; fi
    if [[ -f ".deepwiki/functional-summary.md" ]]; then log_pass "functional-summary.md generated"; else log_fail "functional-summary.md missing"; fi
}

test_wiki_directory_structure() {
    run_test
    log_test "Directory structure"
    cd "$FIXTURE_DIR"

    if [[ -d ".deepwiki/architecture" ]]; then log_pass "architecture/ created"; else log_fail "architecture/ missing"; fi
    if [[ -d ".deepwiki/modules" ]]; then log_pass "modules/ created"; else log_fail "modules/ missing"; fi
    if [[ -d ".deepwiki/api-reference" ]]; then log_pass "api-reference/ created"; else log_fail "api-reference/ missing"; fi
    if [[ -d ".deepwiki/data-models" ]]; then log_pass "data-models/ created"; else log_fail "data-models/ missing"; fi
}

test_wiki_tier_selection() {
    run_test
    log_test "Tier selection (--tiers 1,2)"
    cd "$FIXTURE_DIR"
    rm -rf .deepwiki

    bash "$WIKI_SCRIPT" --tiers "1,2" > /dev/null 2>&1

    if [[ -f ".deepwiki/overview.md" ]]; then log_pass "Tier 1 generated"; else log_fail "Tier 1 not generated"; fi
    if [[ -f ".deepwiki/functional-summary.md" ]]; then log_pass "Tier 2 generated"; else log_fail "Tier 2 not generated"; fi
}

test_wiki_contains_statistics() {
    run_test
    log_test "Contains statistics"
    cd "$FIXTURE_DIR"

    if grep -q "Files Indexed" .deepwiki/overview.md 2>/dev/null; then
        log_pass "Statistics present in overview"
    else
        log_fail "Statistics missing from overview"
    fi
}

test_wiki_contains_classes() {
    run_test
    log_test "Contains class documentation"
    cd "$FIXTURE_DIR"

    if grep -q "User" .deepwiki/functional-summary.md 2>/dev/null; then
        log_pass "User class documented"
    else
        log_fail "User class not documented"
    fi
}

test_wiki_contains_endpoints() {
    run_test
    log_test "Contains API endpoints"
    cd "$FIXTURE_DIR"

    if grep -q "/login" .deepwiki/api-reference/README.md 2>/dev/null; then
        log_pass "REST endpoints documented"
    else
        log_fail "REST endpoints not documented"
    fi
}

test_wiki_no_index_fails() {
    run_test
    log_test "Fails without index"
    cd "$FIXTURE_DIR"
    rm -rf .analysis .deepwiki

    set +e
    bash "$WIKI_SCRIPT" > /dev/null 2>&1
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 1 ]]; then
        log_pass "Fails correctly when index missing"
    else
        log_fail "Should fail when index missing"
    fi
}

main() {
    echo "========================================="
    echo "DeepWiki Generation Test Suite"
    echo "========================================="
    echo ""

    setup
    trap cleanup EXIT

    test_wiki_script_exists
    test_wiki_generates_files
    test_wiki_directory_structure
    test_wiki_tier_selection
    test_wiki_contains_statistics
    test_wiki_contains_classes
    test_wiki_contains_endpoints
    test_wiki_no_index_fails

    echo ""
    echo "========================================="
    echo "Tests: $TESTS_RUN | ${GREEN}Passed: $TESTS_PASSED${NC} | ${RED}Failed: $TESTS_FAILED${NC}"
    echo "========================================="

    [[ $TESTS_FAILED -eq 0 ]] && exit 0 || exit 1
}

main "$@"
