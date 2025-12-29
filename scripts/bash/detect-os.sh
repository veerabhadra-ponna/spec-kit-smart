#!/usr/bin/env bash
#
# detect-os.sh - Central OS detection utility
# Returns platform type for cross-platform script routing
#
# Usage:
#   platform=$(bash .specify/scripts/bash/detect-os.sh)
#   if [[ "$platform" == "unix" ]]; then
#     # Run Unix-specific commands
#   fi
#
# Output:
#   - "unix" for Linux/macOS/Unix systems
#   - "windows" for Windows (Git Bash, WSL, Cygwin, MSYS)
#
# Exit codes:
#   0 - Success
#   1 - Unable to detect platform
#

set -euo pipefail

# Check for SPEC_KIT_PLATFORM environment variable override
if [[ -n "${SPEC_KIT_PLATFORM:-}" ]]; then
    case "$SPEC_KIT_PLATFORM" in
        unix|windows)
            echo "$SPEC_KIT_PLATFORM"
            exit 0
            ;;
        auto)
            # Continue with automatic detection
            ;;
        *)
            echo "Error: Invalid SPEC_KIT_PLATFORM value: $SPEC_KIT_PLATFORM (expected: unix, windows, or auto)" >&2
            exit 1
            ;;
    esac
fi

# Detect platform using uname
if command -v uname >/dev/null 2>&1; then
    os_name=$(uname -s)

    case "$os_name" in
        Linux*|Darwin*|FreeBSD*|OpenBSD*|NetBSD*|SunOS*)
            echo "unix"
            exit 0
            ;;
        CYGWIN*|MINGW*|MSYS*|MINGW64*)
            # Git Bash, MSYS2, Cygwin on Windows
            echo "windows"
            exit 0
            ;;
        *)
            # Unknown Unix-like system, default to unix
            echo "unix"
            exit 0
            ;;
    esac
fi

# Fallback: Check for common Windows indicators
if [[ -n "${WINDIR:-}" ]] || [[ -n "${SYSTEMROOT:-}" ]]; then
    echo "windows"
    exit 0
fi

# Final fallback: assume Unix
echo "unix"
exit 0
