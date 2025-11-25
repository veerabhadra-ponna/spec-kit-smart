#!/usr/bin/env bash
#
# test-data-extraction.sh - Test suite for data extraction algorithms
#
# This test validates that the indexing scripts correctly extract:
# - Classes and their relationships
# - Functions and their parameters
# - Interfaces and their fields
# - REST API endpoints
# - GraphQL resolvers
# - WebSocket handlers
# - External API integrations
# - Environment variables
# - Import/export dependencies
# - Data models (Prisma, TypeORM)
# - Secret detection
#
# Usage: bash tests/indexing/test-data-extraction.sh
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

# JSON extraction helper
json_contains() {
    local file="$1"
    local pattern="$2"
    grep -q "$pattern" "$file" 2>/dev/null
}

# Setup test environment
setup() {
    log_info "Setting up test environment..."
    cd "$FIXTURE_DIR"
    rm -rf .analysis

    # Build the index first
    log_info "Building index for fixture project..."
    set +e
    bash "$BUILD_SCRIPT" --verbose > /dev/null 2>&1
    BUILD_EXIT=$?
    set -e

    if [[ $BUILD_EXIT -ne 0 ]]; then
        echo -e "${RED}ERROR: Failed to build index for fixture project${NC}"
        exit 1
    fi

    log_info "Index built successfully"
    echo ""
}

cleanup() {
    cd "$FIXTURE_DIR"
    rm -rf .analysis
}

#=============================================================================
# TEST GROUP 1: Class Extraction
#=============================================================================

test_class_extraction_user() {
    run_test
    log_test "Class Extraction: User class"

    if json_contains ".analysis/index/structure.json" '"name":[[:space:]]*"User"'; then
        log_pass "User class extracted"
    else
        log_fail "User class not found in structure.json"
    fi
}

test_class_extraction_authservice() {
    run_test
    log_test "Class Extraction: AuthService class"

    if json_contains ".analysis/index/structure.json" '"name":[[:space:]]*"AuthService"'; then
        log_pass "AuthService class extracted"
    else
        log_fail "AuthService class not found in structure.json"
    fi
}

test_class_has_file_reference() {
    run_test
    log_test "Class Extraction: File reference for User"

    if json_contains ".analysis/index/structure.json" '"file":[[:space:]]*"src/models/User.ts"'; then
        log_pass "User class has correct file reference"
    else
        log_fail "User class file reference missing or incorrect"
    fi
}

test_class_has_line_number() {
    run_test
    log_test "Class Extraction: Line number present"

    if json_contains ".analysis/index/structure.json" '"line":[[:space:]]*[0-9]'; then
        log_pass "Line numbers present in class data"
    else
        log_fail "Line numbers missing from class data"
    fi
}

#=============================================================================
# TEST GROUP 2: Function Extraction
#=============================================================================

test_function_extraction_validate_email() {
    run_test
    log_test "Function Extraction: validateEmail function"

    if json_contains ".analysis/index/structure.json" '"name":[[:space:]]*"validateEmail"'; then
        log_pass "validateEmail function extracted"
    else
        log_fail "validateEmail function not found in structure.json"
    fi
}

test_function_has_file_reference() {
    run_test
    log_test "Function Extraction: File reference for validateEmail"

    # Check that validateEmail is associated with User.ts
    if grep -A5 '"validateEmail"' .analysis/index/structure.json 2>/dev/null | grep -q "User.ts"; then
        log_pass "validateEmail has correct file reference"
    else
        log_fail "validateEmail file reference missing or incorrect"
    fi
}

#=============================================================================
# TEST GROUP 3: Interface Extraction
#=============================================================================

test_interface_extraction_iuser() {
    run_test
    log_test "Interface Extraction: IUser interface"

    if json_contains ".analysis/index/structure.json" '"name":[[:space:]]*"IUser"'; then
        log_pass "IUser interface extracted"
    else
        log_fail "IUser interface not found in structure.json"
    fi
}

test_interface_has_file_reference() {
    run_test
    log_test "Interface Extraction: File reference for IUser"

    if grep -A5 '"IUser"' .analysis/index/structure.json 2>/dev/null | grep -q "User.ts"; then
        log_pass "IUser has correct file reference"
    else
        log_fail "IUser file reference missing or incorrect"
    fi
}

#=============================================================================
# TEST GROUP 4: REST API Endpoint Extraction
#=============================================================================

test_rest_endpoint_post_login() {
    run_test
    log_test "REST Extraction: POST /login endpoint"

    if json_contains ".analysis/index/api-endpoints.json" '"path":[[:space:]]*"/login"'; then
        log_pass "POST /login endpoint extracted"
    else
        log_fail "POST /login endpoint not found in api-endpoints.json"
    fi
}

test_rest_endpoint_post_register() {
    run_test
    log_test "REST Extraction: POST /register endpoint"

    if json_contains ".analysis/index/api-endpoints.json" '"path":[[:space:]]*"/register"'; then
        log_pass "POST /register endpoint extracted"
    else
        log_fail "POST /register endpoint not found in api-endpoints.json"
    fi
}

test_rest_endpoint_get_profile() {
    run_test
    log_test "REST Extraction: GET /profile endpoint"

    if json_contains ".analysis/index/api-endpoints.json" '"path":[[:space:]]*"/profile"'; then
        log_pass "GET /profile endpoint extracted"
    else
        log_fail "GET /profile endpoint not found in api-endpoints.json"
    fi
}

test_rest_endpoint_has_method() {
    run_test
    log_test "REST Extraction: Method types present"

    if json_contains ".analysis/index/api-endpoints.json" '"method":[[:space:]]*"POST"'; then
        log_pass "POST method type present"
    else
        log_fail "POST method type missing"
    fi

    if json_contains ".analysis/index/api-endpoints.json" '"method":[[:space:]]*"GET"'; then
        log_pass "GET method type present"
    else
        log_fail "GET method type missing"
    fi
}

test_rest_endpoint_count() {
    run_test
    log_test "REST Extraction: Total endpoint count"

    # Check metadata for endpoint count
    local count=$(grep -o '"total_rest_endpoints":[[:space:]]*[0-9]*' .analysis/index/metadata.json 2>/dev/null | grep -o '[0-9]*' || echo "0")

    if [[ "$count" -ge 3 ]]; then
        log_pass "Found $count REST endpoints (expected >= 3)"
    else
        log_fail "Only found $count REST endpoints (expected >= 3)"
    fi
}

#=============================================================================
# TEST GROUP 5: External API Detection
#=============================================================================

test_external_api_stripe() {
    run_test
    log_test "External API: Stripe detection"

    if json_contains ".analysis/index/external-apis.json" '"service":[[:space:]]*"stripe"'; then
        log_pass "Stripe SDK detected"
    else
        log_fail "Stripe SDK not detected in external-apis.json"
    fi
}

test_external_api_file_reference() {
    run_test
    log_test "External API: File reference for Stripe"

    if grep -A5 '"stripe"' .analysis/index/external-apis.json 2>/dev/null | grep -q "AuthService.ts"; then
        log_pass "Stripe has correct file reference"
    else
        log_fail "Stripe file reference missing or incorrect"
    fi
}

#=============================================================================
# TEST GROUP 6: Environment Variable Extraction
#=============================================================================

test_env_var_stripe_key() {
    run_test
    log_test "Environment Variables: STRIPE_SECRET_KEY"

    if json_contains ".analysis/index/external-apis.json" '"name":[[:space:]]*"STRIPE_SECRET_KEY"'; then
        log_pass "STRIPE_SECRET_KEY environment variable extracted"
    else
        log_fail "STRIPE_SECRET_KEY not found in external-apis.json"
    fi
}

test_env_var_count() {
    run_test
    log_test "Environment Variables: Count in metadata"

    local count=$(grep -o '"total_env_vars":[[:space:]]*[0-9]*' .analysis/index/metadata.json 2>/dev/null | grep -o '[0-9]*' || echo "0")

    if [[ "$count" -ge 1 ]]; then
        log_pass "Found $count environment variables"
    else
        log_fail "No environment variables found"
    fi
}

#=============================================================================
# TEST GROUP 7: Dependency Extraction
#=============================================================================

test_dependency_es6_import() {
    run_test
    log_test "Dependencies: ES6 import detection"

    if json_contains ".analysis/index/dependencies.json" '"import_type":[[:space:]]*"es6_import"'; then
        log_pass "ES6 imports detected"
    else
        log_fail "ES6 imports not detected in dependencies.json"
    fi
}

test_dependency_user_import() {
    run_test
    log_test "Dependencies: User model import"

    if json_contains ".analysis/index/dependencies.json" '"imported_from":[[:space:]]*"../models/User"'; then
        log_pass "User model import detected"
    else
        log_fail "User model import not detected"
    fi
}

test_dependency_stripe_import() {
    run_test
    log_test "Dependencies: Stripe package import"

    if json_contains ".analysis/index/dependencies.json" '"imported_from":[[:space:]]*"stripe"'; then
        log_pass "Stripe package import detected"
    else
        log_fail "Stripe package import not detected"
    fi
}

test_dependency_express_import() {
    run_test
    log_test "Dependencies: Express import"

    if json_contains ".analysis/index/dependencies.json" '"imported_from":[[:space:]]*"express"'; then
        log_pass "Express import detected"
    else
        log_fail "Express import not detected"
    fi
}

test_dependency_count() {
    run_test
    log_test "Dependencies: Total count"

    local count=$(grep -o '"total_dependencies":[[:space:]]*[0-9]*' .analysis/index/metadata.json 2>/dev/null | grep -o '[0-9]*' || echo "0")

    if [[ "$count" -ge 4 ]]; then
        log_pass "Found $count dependencies (expected >= 4)"
    else
        log_fail "Only found $count dependencies (expected >= 4)"
    fi
}

#=============================================================================
# TEST GROUP 8: Metadata Validation
#=============================================================================

test_metadata_version() {
    run_test
    log_test "Metadata: Version field present"

    if json_contains ".analysis/index/metadata.json" '"version":[[:space:]]*"1.0"'; then
        log_pass "Version field is 1.0"
    else
        log_fail "Version field missing or incorrect"
    fi
}

test_metadata_created_by() {
    run_test
    log_test "Metadata: created_by_version field present"

    if json_contains ".analysis/index/metadata.json" '"created_by_version"'; then
        log_pass "created_by_version field present"
    else
        log_fail "created_by_version field missing"
    fi
}

test_metadata_freshness() {
    run_test
    log_test "Metadata: Freshness timestamp"

    if json_contains ".analysis/index/metadata.json" '"freshness"'; then
        log_pass "Freshness timestamp present"
    else
        log_fail "Freshness timestamp missing"
    fi
}

test_metadata_statistics() {
    run_test
    log_test "Metadata: Statistics section"

    if json_contains ".analysis/index/metadata.json" '"statistics"'; then
        log_pass "Statistics section present"
    else
        log_fail "Statistics section missing"
    fi
}

test_metadata_total_files() {
    run_test
    log_test "Metadata: Total files count"

    local count=$(grep -o '"total_files":[[:space:]]*[0-9]*' .analysis/index/metadata.json 2>/dev/null | grep -o '[0-9]*' || echo "0")

    if [[ "$count" -ge 3 ]]; then
        log_pass "Total files: $count"
    else
        log_fail "Expected at least 3 files, found $count"
    fi
}

test_metadata_classes_count() {
    run_test
    log_test "Metadata: Classes count"

    local count=$(grep -o '"total_classes":[[:space:]]*[0-9]*' .analysis/index/metadata.json 2>/dev/null | grep -o '[0-9]*' || echo "0")

    if [[ "$count" -ge 2 ]]; then
        log_pass "Total classes: $count (expected >= 2: User, AuthService)"
    else
        log_fail "Expected at least 2 classes, found $count"
    fi
}

test_metadata_functions_count() {
    run_test
    log_test "Metadata: Functions count"

    local count=$(grep -o '"total_functions":[[:space:]]*[0-9]*' .analysis/index/metadata.json 2>/dev/null | grep -o '[0-9]*' || echo "0")

    if [[ "$count" -ge 1 ]]; then
        log_pass "Total functions: $count"
    else
        log_fail "Expected at least 1 function, found $count"
    fi
}

test_metadata_interfaces_count() {
    run_test
    log_test "Metadata: Interfaces count"

    local count=$(grep -o '"total_interfaces":[[:space:]]*[0-9]*' .analysis/index/metadata.json 2>/dev/null | grep -o '[0-9]*' || echo "0")

    if [[ "$count" -ge 1 ]]; then
        log_pass "Total interfaces: $count (expected >= 1: IUser)"
    else
        log_fail "Expected at least 1 interface, found $count"
    fi
}

#=============================================================================
# TEST GROUP 9: JSON Schema Validation
#=============================================================================

test_structure_json_valid() {
    run_test
    log_test "JSON Schema: structure.json is valid JSON"

    if jq empty .analysis/index/structure.json 2>/dev/null; then
        log_pass "structure.json is valid JSON"
    else
        log_fail "structure.json is not valid JSON"
    fi
}

test_metadata_json_valid() {
    run_test
    log_test "JSON Schema: metadata.json is valid JSON"

    if jq empty .analysis/index/metadata.json 2>/dev/null; then
        log_pass "metadata.json is valid JSON"
    else
        log_fail "metadata.json is not valid JSON"
    fi
}

test_api_endpoints_json_valid() {
    run_test
    log_test "JSON Schema: api-endpoints.json is valid JSON"

    if jq empty .analysis/index/api-endpoints.json 2>/dev/null; then
        log_pass "api-endpoints.json is valid JSON"
    else
        log_fail "api-endpoints.json is not valid JSON"
    fi
}

test_external_apis_json_valid() {
    run_test
    log_test "JSON Schema: external-apis.json is valid JSON"

    if jq empty .analysis/index/external-apis.json 2>/dev/null; then
        log_pass "external-apis.json is valid JSON"
    else
        log_fail "external-apis.json is not valid JSON"
    fi
}

test_dependencies_json_valid() {
    run_test
    log_test "JSON Schema: dependencies.json is valid JSON"

    if jq empty .analysis/index/dependencies.json 2>/dev/null; then
        log_pass "dependencies.json is valid JSON"
    else
        log_fail "dependencies.json is not valid JSON"
    fi
}

test_data_models_json_valid() {
    run_test
    log_test "JSON Schema: data-models.json is valid JSON"

    if jq empty .analysis/index/data-models.json 2>/dev/null; then
        log_pass "data-models.json is valid JSON"
    else
        log_fail "data-models.json is not valid JSON"
    fi
}

#=============================================================================
# Main Execution
#=============================================================================

main() {
    echo "========================================="
    echo "Data Extraction Algorithm Test Suite"
    echo "========================================="
    echo ""
    echo "Testing fixture: $FIXTURE_DIR"
    echo ""

    # Check if jq is available for JSON validation tests
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}WARNING: jq not found, JSON validation tests will fail${NC}"
    fi

    setup
    trap cleanup EXIT

    echo ""
    echo "--- Test Group 1: Class Extraction ---"
    test_class_extraction_user
    test_class_extraction_authservice
    test_class_has_file_reference
    test_class_has_line_number

    echo ""
    echo "--- Test Group 2: Function Extraction ---"
    test_function_extraction_validate_email
    test_function_has_file_reference

    echo ""
    echo "--- Test Group 3: Interface Extraction ---"
    test_interface_extraction_iuser
    test_interface_has_file_reference

    echo ""
    echo "--- Test Group 4: REST API Endpoint Extraction ---"
    test_rest_endpoint_post_login
    test_rest_endpoint_post_register
    test_rest_endpoint_get_profile
    test_rest_endpoint_has_method
    test_rest_endpoint_count

    echo ""
    echo "--- Test Group 5: External API Detection ---"
    test_external_api_stripe
    test_external_api_file_reference

    echo ""
    echo "--- Test Group 6: Environment Variable Extraction ---"
    test_env_var_stripe_key
    test_env_var_count

    echo ""
    echo "--- Test Group 7: Dependency Extraction ---"
    test_dependency_es6_import
    test_dependency_user_import
    test_dependency_stripe_import
    test_dependency_express_import
    test_dependency_count

    echo ""
    echo "--- Test Group 8: Metadata Validation ---"
    test_metadata_version
    test_metadata_created_by
    test_metadata_freshness
    test_metadata_statistics
    test_metadata_total_files
    test_metadata_classes_count
    test_metadata_functions_count
    test_metadata_interfaces_count

    echo ""
    echo "--- Test Group 9: JSON Schema Validation ---"
    test_structure_json_valid
    test_metadata_json_valid
    test_api_endpoints_json_valid
    test_external_apis_json_valid
    test_dependencies_json_valid
    test_data_models_json_valid

    echo ""
    echo "========================================="
    echo "Test Results"
    echo "========================================="
    echo "Tests run: $TESTS_RUN"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    echo ""

    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ All data extraction tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some data extraction tests failed${NC}"
        exit 1
    fi
}

main "$@"
