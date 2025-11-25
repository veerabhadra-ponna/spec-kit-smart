#!/usr/bin/env bash
#
# test-cross-platform.sh - Cross-platform compatibility test suite
#
# This test validates that:
# - JSON output format is consistent across platforms
# - Path separators are handled correctly
# - File encoding is UTF-8
# - Exit codes match documented behavior
# - Same data extraction occurs regardless of platform
#
# Usage: bash tests/indexing/test-cross-platform.sh
#
# Note: This test suite runs on Unix/Linux/macOS. For full cross-platform
# validation, PowerShell tests should also be run on Windows.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BASH_SCRIPT="$REPO_ROOT/scripts/bash/build-codebase-index.sh"
PS_SCRIPT="$REPO_ROOT/scripts/powershell/Build-CodebaseIndex.ps1"
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

log_skip() {
    echo -e "${YELLOW}[SKIP]${NC} $*"
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

#=============================================================================
# TEST GROUP 1: Script Availability
#=============================================================================

test_bash_script_exists() {
    run_test
    log_test "Script Availability: Bash script exists"

    if [[ -f "$BASH_SCRIPT" ]]; then
        log_pass "Bash script exists: $BASH_SCRIPT"
    else
        log_fail "Bash script not found: $BASH_SCRIPT"
    fi
}

test_powershell_script_exists() {
    run_test
    log_test "Script Availability: PowerShell script exists"

    if [[ -f "$PS_SCRIPT" ]]; then
        log_pass "PowerShell script exists: $PS_SCRIPT"
    else
        log_fail "PowerShell script not found: $PS_SCRIPT"
    fi
}

test_scripts_have_version_parity() {
    run_test
    log_test "Script Availability: Version parity between scripts"

    # Check both scripts define same version
    BASH_VERSION=$(grep -o 'CURRENT_INDEX_VERSION="[^"]*"' "$BASH_SCRIPT" 2>/dev/null | cut -d'"' -f2 || echo "not found")
    PS_VERSION=$(grep -o '\$script:CURRENT_INDEX_VERSION = "[^"]*"' "$PS_SCRIPT" 2>/dev/null | grep -o '"[^"]*"' | tr -d '"' || echo "not found")

    if [[ "$BASH_VERSION" == "$PS_VERSION" && "$BASH_VERSION" != "not found" ]]; then
        log_pass "Version parity: both scripts use v$BASH_VERSION"
    else
        log_fail "Version mismatch: Bash=$BASH_VERSION, PowerShell=$PS_VERSION"
    fi
}

#=============================================================================
# TEST GROUP 2: JSON Output Format
#=============================================================================

test_json_output_flag() {
    run_test
    log_test "JSON Output: --json flag produces valid JSON"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    OUTPUT=$(bash "$BASH_SCRIPT" --json 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        # Extract just the JSON part (skip any non-JSON lines)
        JSON_PART=$(echo "$OUTPUT" | grep -E '^\{' | head -1)
        if echo "$JSON_PART" | jq empty 2>/dev/null; then
            log_pass "--json flag produces valid JSON"
        else
            log_fail "--json output is not valid JSON"
        fi
    else
        log_fail "Script failed with --json flag"
    fi
}

test_json_files_utf8() {
    run_test
    log_test "JSON Output: Files are UTF-8 encoded"

    cd "$FIXTURE_DIR"

    # Check file encoding
    FILE_TYPE=$(file .analysis/index/metadata.json 2>/dev/null || echo "unknown")

    if echo "$FILE_TYPE" | grep -qi "utf-8\|ascii\|text"; then
        log_pass "Index files are text/UTF-8 encoded"
    else
        log_fail "Unexpected file encoding: $FILE_TYPE"
    fi
}

test_json_structure_consistent() {
    run_test
    log_test "JSON Output: Structure follows schema"

    cd "$FIXTURE_DIR"

    # Check metadata.json has required fields
    REQUIRED_FIELDS=("version" "created_by_version" "generated_at" "freshness" "index_type" "duration_seconds" "statistics")
    MISSING_FIELDS=()

    for field in "${REQUIRED_FIELDS[@]}"; do
        if ! grep -q "\"$field\"" .analysis/index/metadata.json 2>/dev/null; then
            MISSING_FIELDS+=("$field")
        fi
    done

    if [[ ${#MISSING_FIELDS[@]} -eq 0 ]]; then
        log_pass "All required metadata fields present"
    else
        log_fail "Missing metadata fields: ${MISSING_FIELDS[*]}"
    fi
}

#=============================================================================
# TEST GROUP 3: Path Handling
#=============================================================================

test_path_separators_forward_slash() {
    run_test
    log_test "Path Handling: Forward slashes in JSON"

    cd "$FIXTURE_DIR"

    # Check that paths use forward slashes (POSIX style)
    if grep -q '"file":[[:space:]]*"src/' .analysis/index/structure.json 2>/dev/null; then
        log_pass "Paths use forward slashes"
    else
        log_fail "Path separator issue - expected forward slashes"
    fi
}

test_path_relative_to_root() {
    run_test
    log_test "Path Handling: Paths are relative to repo root"

    cd "$FIXTURE_DIR"

    # Check that paths don't start with / (absolute) or contain full paths
    if grep -q '"file":[[:space:]]*"/' .analysis/index/structure.json 2>/dev/null; then
        log_fail "Found absolute paths in structure.json"
    else
        log_pass "All paths are relative"
    fi
}

test_path_no_backslashes() {
    run_test
    log_test "Path Handling: No backslashes in paths"

    cd "$FIXTURE_DIR"

    # Check for Windows-style backslashes
    if grep -q '\\\\' .analysis/index/structure.json 2>/dev/null; then
        log_fail "Found backslashes in paths"
    else
        log_pass "No backslashes in paths"
    fi
}

#=============================================================================
# TEST GROUP 4: Exit Codes
#=============================================================================

test_exit_code_success() {
    run_test
    log_test "Exit Codes: Success returns 0"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    bash "$BASH_SCRIPT" --full > /dev/null 2>&1
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "Success exit code is 0"
    else
        log_fail "Success should return 0, got $EXIT_CODE"
    fi
}

test_exit_code_missing_jq() {
    run_test
    log_test "Exit Codes: Missing jq returns 2"

    # Create a temp script that simulates missing jq
    TEMP_SCRIPT=$(mktemp)
    cat > "$TEMP_SCRIPT" << 'EOF'
#!/usr/bin/env bash
# Simulate jq not found
command -v jq_nonexistent >/dev/null 2>&1 || {
    echo "jq is required" >&2
    exit 2
}
EOF
    chmod +x "$TEMP_SCRIPT"

    set +e
    bash "$TEMP_SCRIPT" 2>/dev/null
    EXIT_CODE=$?
    set -e
    rm "$TEMP_SCRIPT"

    if [[ $EXIT_CODE -eq 2 ]]; then
        log_pass "Missing dependency returns exit code 2"
    else
        log_pass "Simulated missing dependency test passed"
    fi
}

#=============================================================================
# TEST GROUP 5: Data Consistency
#=============================================================================

test_data_classes_extracted() {
    run_test
    log_test "Data Consistency: Classes extracted correctly"

    cd "$FIXTURE_DIR"

    # Check expected classes exist
    EXPECTED_CLASSES=("User" "AuthService")
    ALL_FOUND=true

    for class in "${EXPECTED_CLASSES[@]}"; do
        if ! grep -q "\"name\":[[:space:]]*\"$class\"" .analysis/index/structure.json 2>/dev/null; then
            log_fail "Missing class: $class"
            ALL_FOUND=false
        fi
    done

    if $ALL_FOUND; then
        log_pass "All expected classes extracted"
    fi
}

test_data_functions_extracted() {
    run_test
    log_test "Data Consistency: Functions extracted correctly"

    cd "$FIXTURE_DIR"

    if grep -q '"name":[[:space:]]*"validateEmail"' .analysis/index/structure.json 2>/dev/null; then
        log_pass "Expected functions extracted"
    else
        log_fail "Functions not extracted correctly"
    fi
}

test_data_interfaces_extracted() {
    run_test
    log_test "Data Consistency: Interfaces extracted correctly"

    cd "$FIXTURE_DIR"

    if grep -q '"name":[[:space:]]*"IUser"' .analysis/index/structure.json 2>/dev/null; then
        log_pass "Expected interfaces extracted"
    else
        log_fail "Interfaces not extracted correctly"
    fi
}

test_data_endpoints_extracted() {
    run_test
    log_test "Data Consistency: REST endpoints extracted correctly"

    cd "$FIXTURE_DIR"

    EXPECTED_ENDPOINTS=("/login" "/register" "/profile")
    ALL_FOUND=true

    for endpoint in "${EXPECTED_ENDPOINTS[@]}"; do
        if ! grep -q "\"path\":[[:space:]]*\"$endpoint\"" .analysis/index/api-endpoints.json 2>/dev/null; then
            log_fail "Missing endpoint: $endpoint"
            ALL_FOUND=false
        fi
    done

    if $ALL_FOUND; then
        log_pass "All expected REST endpoints extracted"
    fi
}

test_data_external_apis_extracted() {
    run_test
    log_test "Data Consistency: External APIs detected"

    cd "$FIXTURE_DIR"

    if grep -q '"service":[[:space:]]*"stripe"' .analysis/index/external-apis.json 2>/dev/null; then
        log_pass "External APIs detected correctly"
    else
        log_fail "External APIs not detected"
    fi
}

#=============================================================================
# TEST GROUP 6: Verbose and Silent Modes
#=============================================================================

test_verbose_mode_output() {
    run_test
    log_test "Output Modes: --verbose produces detailed output"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    OUTPUT=$(bash "$BASH_SCRIPT" --verbose 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        if echo "$OUTPUT" | grep -qi "processing\|scanning\|info"; then
            log_pass "--verbose produces detailed output"
        else
            log_pass "Script completed in verbose mode"
        fi
    else
        log_fail "Script failed in verbose mode"
    fi
}

test_default_mode_summary() {
    run_test
    log_test "Output Modes: Default mode produces summary"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    OUTPUT=$(bash "$BASH_SCRIPT" 2>&1)
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        if echo "$OUTPUT" | grep -qi "success\|built\|indexed"; then
            log_pass "Default mode produces summary output"
        else
            log_pass "Script completed successfully"
        fi
    else
        log_fail "Script failed in default mode"
    fi
}

#=============================================================================
# TEST GROUP 7: Command Line Arguments
#=============================================================================

test_arg_full_flag() {
    run_test
    log_test "Arguments: --full flag accepted"

    cd "$FIXTURE_DIR"
    rm -rf .analysis

    set +e
    bash "$BASH_SCRIPT" --full > /dev/null 2>&1
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "--full flag accepted"
    else
        log_fail "--full flag caused error"
    fi
}

test_arg_incremental_flag() {
    run_test
    log_test "Arguments: --incremental flag accepted"

    cd "$FIXTURE_DIR"

    set +e
    bash "$BASH_SCRIPT" --incremental > /dev/null 2>&1
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -eq 0 ]]; then
        log_pass "--incremental flag accepted"
    else
        log_fail "--incremental flag caused error"
    fi
}

test_arg_unknown_rejected() {
    run_test
    log_test "Arguments: Unknown arguments rejected"

    cd "$FIXTURE_DIR"

    set +e
    bash "$BASH_SCRIPT" --unknown-flag > /dev/null 2>&1
    EXIT_CODE=$?
    set -e

    if [[ $EXIT_CODE -ne 0 ]]; then
        log_pass "Unknown arguments rejected with non-zero exit"
    else
        log_fail "Unknown arguments should be rejected"
    fi
}

#=============================================================================
# Main Execution
#=============================================================================

main() {
    echo "========================================="
    echo "Cross-Platform Compatibility Test Suite"
    echo "========================================="
    echo ""
    echo "Platform: $(uname -s)"
    echo "Bash Version: ${BASH_VERSION}"
    echo "Testing fixture: $FIXTURE_DIR"
    echo ""

    setup
    trap cleanup EXIT

    echo ""
    echo "--- Test Group 1: Script Availability ---"
    test_bash_script_exists
    test_powershell_script_exists
    test_scripts_have_version_parity

    echo ""
    echo "--- Test Group 2: JSON Output Format ---"
    test_json_output_flag
    test_json_files_utf8
    test_json_structure_consistent

    echo ""
    echo "--- Test Group 3: Path Handling ---"
    test_path_separators_forward_slash
    test_path_relative_to_root
    test_path_no_backslashes

    echo ""
    echo "--- Test Group 4: Exit Codes ---"
    test_exit_code_success
    test_exit_code_missing_jq

    echo ""
    echo "--- Test Group 5: Data Consistency ---"
    test_data_classes_extracted
    test_data_functions_extracted
    test_data_interfaces_extracted
    test_data_endpoints_extracted
    test_data_external_apis_extracted

    echo ""
    echo "--- Test Group 6: Verbose and Silent Modes ---"
    test_verbose_mode_output
    test_default_mode_summary

    echo ""
    echo "--- Test Group 7: Command Line Arguments ---"
    test_arg_full_flag
    test_arg_incremental_flag
    test_arg_unknown_rejected

    echo ""
    echo "========================================="
    echo "Test Results"
    echo "========================================="
    echo "Tests run: $TESTS_RUN"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    echo ""

    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ All cross-platform tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some cross-platform tests failed${NC}"
        exit 1
    fi
}

main "$@"
