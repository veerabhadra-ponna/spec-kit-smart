#!/usr/bin/env bash

#
# check-artifactory.sh - Query Artifactory for library availability
#
# Usage:
#   ./check-artifactory.sh <artifactory-url> <library-name> [api-key] [repos]
#
# Returns:
#   Exit 0: Library found (prints download URL)
#   Exit 1: Library not found
#   Exit 2: Authentication error
#   Exit 3: API error (network, timeout, etc.)
#   Exit 4: Artifactory URL not configured (skip check)
#

set -euo pipefail

# Debug mode (set DEBUG=true to enable verbose output)
DEBUG="${DEBUG:-false}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Show help if requested
if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    cat <<EOF
Usage: $(basename "$0") <artifactory-url> <library-name> [api-key] [repos]

Query Artifactory for library availability.

Arguments:
  artifactory-url    URL of the Artifactory instance
                     Examples:
                       - https://artifactory.company.com/artifactory
                       - https://artifactory.company.com
                     Note: Include /artifactory path if your installation requires it
  library-name       Name of the library to check (e.g., axios, lodash, jackson-databind)
  api-key           Optional API key/token for authentication (or set ARTIFACTORY_API_KEY env var)
                     Supports: Bearer tokens (recommended), API keys, Reference tokens
  repos             Optional comma-separated list of repositories to search
                     Example: libs-release,libs-snapshot
                     If omitted, searches all repositories

Environment Variables:
  ARTIFACTORY_API_KEY  API key/token for authentication
  DEBUG                Set to 'true' to enable verbose debug output

Exit Codes:
  0  Library found (prints download URL)
  1  Library not found (not whitelisted)
  2  Authentication error
  3  API error (network, timeout, etc.)
  4  Artifactory URL not configured (skip check)

Examples:
  # Check if axios is available (all repositories)
  $(basename "$0") https://artifactory.company.com/artifactory axios

  # Search in specific repositories
  $(basename "$0") https://artifactory.company.com/artifactory axios "" "libs-release,npm-local"

  # With Bearer token (recommended)
  $(basename "$0") https://artifactory.company.com/artifactory axios YOUR_BEARER_TOKEN

  # Using environment variable for token
  export ARTIFACTORY_API_KEY=YOUR_TOKEN
  $(basename "$0") https://artifactory.company.com/artifactory axios

  # With debug output
  DEBUG=true $(basename "$0") https://artifactory.company.com/artifactory axios

  # Skip validation if URL not configured
  $(basename "$0") "Not configured" axios
EOF
    exit 0
fi

# Parse arguments
ARTIFACTORY_URL="${1:-}"
LIBRARY_NAME="${2:-}"
API_KEY="${3:-${ARTIFACTORY_API_KEY:-}}"
REPOS="${4:-}"

# Function to print status
print_status() {
    local status="$1"
    local message="$2"
    case "$status" in
        FOUND)
            echo -e "${GREEN}✅ FOUND${NC}: $message"
            ;;
        NOT_FOUND)
            echo -e "${YELLOW}❌ NOT FOUND${NC}: $message"
            ;;
        SKIPPED)
            echo -e "${YELLOW}⊘ SKIPPED${NC}: $message"
            ;;
        ERROR)
            echo -e "${RED}⚠️  ERROR${NC}: $message"
            ;;
    esac
}

# Validate inputs
if [ -z "$LIBRARY_NAME" ]; then
    echo "ERROR: Library name is required" >&2
    echo "Usage: $0 <artifactory-url> <library-name> [api-key]" >&2
    exit 3
fi

# Check if Artifactory URL is configured
if [ -z "$ARTIFACTORY_URL" ] || [ "$ARTIFACTORY_URL" = "Not configured" ] || [ "$ARTIFACTORY_URL" = "null" ]; then
    print_status "SKIPPED" "Artifactory URL not configured - skipping validation for $LIBRARY_NAME"
    exit 4
fi

# Normalize URL - remove trailing /api if present
ARTIFACTORY_URL="${ARTIFACTORY_URL%/api}"
ARTIFACTORY_URL="${ARTIFACTORY_URL%/}"

# Build API endpoint with optional repos parameter
if [ -n "$REPOS" ]; then
    API_ENDPOINT="${ARTIFACTORY_URL}/api/search/artifact?name=${LIBRARY_NAME}&repos=${REPOS}"
else
    API_ENDPOINT="${ARTIFACTORY_URL}/api/search/artifact?name=${LIBRARY_NAME}"
fi

# Debug output
if [ "$DEBUG" = "true" ]; then
    echo "DEBUG: Artifactory URL: $ARTIFACTORY_URL" >&2
    echo "DEBUG: Library Name: $LIBRARY_NAME" >&2
    echo "DEBUG: Repositories: ${REPOS:-all}" >&2
    echo "DEBUG: API Endpoint: $API_ENDPOINT" >&2
    echo "DEBUG: Using Auth: ${API_KEY:+yes}" >&2
fi

# Query Artifactory with timeout
if [ -n "$API_KEY" ]; then
    # Try Bearer token first (modern method, supports all token types)
    if [ "$DEBUG" = "true" ]; then
        echo "DEBUG: Attempting authentication with Bearer token..." >&2
    fi

    RESPONSE=$(curl -s -w "\n%{http_code}" \
        -H "Authorization: Bearer ${API_KEY}" \
        -H "X-Result-Detail: info" \
        --max-time 5 \
        --connect-timeout 3 \
        "$API_ENDPOINT" 2>/dev/null || echo -e "\n000")

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)

    # If failed with auth error, try legacy X-JFrog-Art-Api header
    if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
        if [ "$DEBUG" = "true" ]; then
            echo "DEBUG: Bearer auth failed, trying legacy X-JFrog-Art-Api header..." >&2
        fi

        RESPONSE=$(curl -s -w "\n%{http_code}" \
            -H "X-JFrog-Art-Api: ${API_KEY}" \
            -H "X-Result-Detail: info" \
            --max-time 5 \
            --connect-timeout 3 \
            "$API_ENDPOINT" 2>/dev/null || echo -e "\n000")
    fi
else
    # Try without authentication (some Artifactory instances allow anonymous read)
    if [ "$DEBUG" = "true" ]; then
        echo "DEBUG: Attempting anonymous access..." >&2
    fi

    RESPONSE=$(curl -s -w "\n%{http_code}" \
        -H "X-Result-Detail: info" \
        --max-time 5 \
        --connect-timeout 3 \
        "$API_ENDPOINT" 2>/dev/null || echo -e "\n000")
fi

# Parse response
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Debug output
if [ "$DEBUG" = "true" ]; then
    echo "DEBUG: HTTP Code: $HTTP_CODE" >&2
    echo "DEBUG: Response Body: $BODY" >&2
fi

# Handle response
case "$HTTP_CODE" in
    200)
        # Check if jq is available
        if command -v jq &> /dev/null; then
            RESULTS=$(echo "$BODY" | jq -r '.results | length' 2>/dev/null || echo "0")
            if [ "$RESULTS" -gt 0 ]; then
                DOWNLOAD_URI=$(echo "$BODY" | jq -r '.results[0].downloadUri' 2>/dev/null || echo "")
                VERSION=$(echo "$DOWNLOAD_URI" | grep -oP '[\d\.]+(?=\.(jar|tar\.gz|zip|whl))' | head -1 || echo "latest")
                print_status "FOUND" "$LIBRARY_NAME${VERSION:+:$VERSION} available in Artifactory"
                echo "$DOWNLOAD_URI"
                exit 0
            else
                print_status "NOT_FOUND" "$LIBRARY_NAME not found in Artifactory"
                exit 1
            fi
        else
            # Fallback without jq - simple check
            if echo "$BODY" | grep -q "downloadUri"; then
                print_status "FOUND" "$LIBRARY_NAME available in Artifactory"
                echo "$BODY"
                exit 0
            else
                print_status "NOT_FOUND" "$LIBRARY_NAME not found in Artifactory"
                exit 1
            fi
        fi
        ;;
    401)
        print_status "ERROR" "Authentication failed (401 Unauthorized). Check your API key/token."
        echo "  Hint: Ensure you're using a valid Bearer token or API key" >&2
        echo "  Set ARTIFACTORY_API_KEY environment variable or pass as 3rd argument" >&2
        exit 2
        ;;
    403)
        print_status "ERROR" "Access forbidden (403 Forbidden). Check permissions for this repository."
        echo "  Your credentials are valid but lack permission to access this resource" >&2
        exit 2
        ;;
    404)
        print_status "ERROR" "API endpoint not found (404). Verify ARTIFACTORY_URL path is correct."
        echo "  Expected format: https://artifactory.company.com/artifactory" >&2
        echo "  Some installations require /artifactory in the path, others don't" >&2
        exit 3
        ;;
    000)
        print_status "ERROR" "Network error or timeout (Artifactory may be unreachable)"
        echo "  Check network connectivity and Artifactory URL" >&2
        exit 3
        ;;
    *)
        print_status "ERROR" "Artifactory API returned HTTP $HTTP_CODE"
        if [ "$DEBUG" = "true" ]; then
            echo "  Response: $BODY" >&2
        fi
        exit 3
        ;;
esac
