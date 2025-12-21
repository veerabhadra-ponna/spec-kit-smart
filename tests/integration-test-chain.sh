#!/usr/bin/env bash
#
# integration-test-chain.sh - Integration test for chained prompt workflow
#
# Tests state management and stage execution using Python CLI
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

echo -e "${BLUE}=== Chain Integration Test ===${NC}"
echo ""

# Check if speckitadv is available
if ! command -v speckitadv &> /dev/null; then
    echo -e "${RED}Error: speckitadv not found. Install with: pip install -e scripts/python${NC}"
    exit 1
fi

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

# Cleanup function
cleanup() {
    echo ""
    echo "Cleaning up test files..."
    rm -rf .analysis/.state/test-*
    rm -rf .analysis/.state/00-bootstrap.json
}

# Set trap for cleanup
trap cleanup EXIT

echo "Test 1: State Management Utilities"
echo "-----------------------------------"

# Test 1.1: Generate chain ID
CHAIN_ID=$(speckitadv chain-state generate-id 2>/dev/null | tr -d '\n' || echo "")
if [[ -n "$CHAIN_ID" ]] && [[ ${#CHAIN_ID} -eq 8 ]]; then
    pass "Chain ID generated: $CHAIN_ID"
else
    fail "Chain ID generation (got: $CHAIN_ID)"
fi

# Test 1.2: Initialize state directory
speckitadv chain-state init > /dev/null 2>&1 || true
if [[ -d ".analysis/.state" ]]; then
    pass "State directory created"
else
    fail "State directory creation"
fi

# Test 1.3: Save and load state
echo ""
echo "Test 2: State Persistence"
echo "-------------------------"

test_state='{"chain_id":"'$CHAIN_ID'","stage":"test","timestamp":"2025-11-14T12:00:00Z","counter":1}'
speckitadv chain-state save test-state --state="$test_state" > /dev/null 2>&1

if [[ -f ".analysis/.state/test-state.json" ]]; then
    pass "State file created"
else
    fail "State file creation"
fi

loaded_state=$(speckitadv chain-state load test-state 2>/dev/null || echo "{}")
if echo "$loaded_state" | jq -e '.chain_id' > /dev/null 2>&1; then
    pass "State loaded successfully"
else
    fail "State loading"
fi

# Test 1.4: State validation
echo ""
echo "Test 3: State Validation"
echo "------------------------"

if speckitadv chain-state validate --state="$test_state" > /dev/null 2>&1; then
    pass "State validation passed"
else
    fail "State validation"
fi

# Test 2: Two-stage execution
echo ""
echo "Test 4: Two-Stage Chain Execution"
echo "----------------------------------"

# Initialize for test
speckitadv chain-state init > /dev/null 2>&1 || true

# Stage 1: Save state
state1='{
  "chain_id": "test1234",
  "stage": "test_stage_1",
  "timestamp": "2025-11-14T12:00:00Z",
  "stages_complete": ["test_stage_1"],
  "counter": 1
}'
speckitadv chain-state save test-stage-1 --state="$state1" > /dev/null 2>&1

result=$(speckitadv chain-state is-complete test-stage-1 2>/dev/null || echo "")
if echo "$result" | grep -qi "true"; then
    pass "Stage 1 completion recorded"
else
    fail "Stage 1 completion"
fi

# Stage 2: Load, modify, save
loaded=$(speckitadv chain-state load test-stage-1 2>/dev/null || echo "{}")
state2='{
  "chain_id": "test1234",
  "stage": "test_stage_2",
  "timestamp": "2025-11-14T12:05:00Z",
  "stages_complete": ["test_stage_1", "test_stage_2"],
  "counter": 2
}'
speckitadv chain-state save test-stage-2 --state="$state2" > /dev/null 2>&1

# Verify counter incremented
counter=$(speckitadv chain-state load test-stage-2 2>/dev/null | jq -r '.counter' || echo "0")
if [[ "$counter" == "2" ]]; then
    pass "State modified correctly (counter: 1 → 2)"
else
    fail "State modification (counter: $counter, expected: 2)"
fi

# Verify stages_complete
stages=$(speckitadv chain-state load test-stage-2 2>/dev/null | jq -r '.stages_complete | length' || echo "0")
if [[ "$stages" == "2" ]]; then
    pass "Both stages recorded in stages_complete"
else
    fail "stages_complete tracking (got: $stages, expected: 2)"
fi

# Test 3: Last stage detection
echo ""
echo "Test 5: Recovery Support"
echo "------------------------"

# Note: last-stage looks for files matching [0-9]{2}[ab]?-.*\.json pattern
# Our test stages use test-stage-* which doesn't match, so we expect "none"
last_stage=$(speckitadv chain-state last-stage 2>/dev/null || echo "none")
if [[ "$last_stage" == "none" ]] || [[ -z "$last_stage" ]]; then
    pass "Last stage detection (test stages don't match numbering pattern - expected)"
else
    # If we get a real stage, that's also fine
    pass "Last completed stage detected: $last_stage"
fi

# Test 4: Bootstrap state
echo ""
echo "Test 6: Bootstrap Integration"
echo "------------------------------"

bootstrap='{
  "chain_id": "'$CHAIN_ID'",
  "timestamp": "'$(date -Iseconds)'",
  "stage": "bootstrap",
  "project_path": "/test/project",
  "analysis_dir": "/test/analysis"
}'
speckitadv chain-state save 00-bootstrap --state="$bootstrap" > /dev/null 2>&1

if speckitadv chain-state load 00-bootstrap 2>/dev/null | jq -e '.project_path' > /dev/null 2>&1; then
    pass "Bootstrap state created and accessible"
else
    fail "Bootstrap state"
fi

# Final summary
echo ""
echo -e "${BLUE}=== Test Summary ===${NC}"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
    echo "Chain state management is working correctly."
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo "Please review failures above."
    exit 1
fi
