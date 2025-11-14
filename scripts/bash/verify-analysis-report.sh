#!/usr/bin/env bash
#
# verify-analysis-report.sh - Verification gate for Stage 6
#
# Enforces quality checks before proceeding to Stage 7
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Handle --help
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "help" ]]; then
    cat <<EOF
Usage: $(basename "$0") <report_file>

Verification gate for Stage 6 analysis report.

Checks:
  - All 9 phases present
  - Minimum 3,000 lines
  - 50+ file:line references
  - No placeholders (TODO, TBD)
  - Severity ratings present

Examples:
  $(basename "$0") .analysis/myproject-20251114/analysis-report.md

Exit codes:
  0 - All checks passed
  1 - One or more checks failed
EOF
    exit 0
fi

# Report file from argument
REPORT_FILE="${1:-}"

if [[ -z "$REPORT_FILE" ]]; then
    echo -e "${RED}❌ Usage: $0 <report_file>${NC}"
    exit 1
fi

echo "=== Analysis Report Verification Gate ==="
echo "Report: $REPORT_FILE"
echo ""

# Track failures
FAILED=0

# Check 1: File exists
if [[ ! -f "$REPORT_FILE" ]]; then
    echo -e "${RED}❌ FAIL: Report file not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Report file exists"

# Check 2: All 9 phases present
echo ""
echo "Checking for all 9 phases..."
for phase in "Phase 1" "Phase 2" "Phase 3" "Phase 4" "Phase 5" "Phase 6" "Phase 7" "Phase 8" "Phase 9"; do
    if grep -q "$phase" "$REPORT_FILE"; then
        echo -e "${GREEN}✓${NC} $phase found"
    else
        echo -e "${RED}❌${NC} MISSING: $phase"
        FAILED=1
    fi
done

# Check 3: Minimum line count
echo ""
lines=$(wc -l < "$REPORT_FILE")
if [[ $lines -ge 3000 ]]; then
    echo -e "${GREEN}✓${NC} Line count: $lines (minimum: 3000)"
else
    echo -e "${RED}❌${NC} Report too short: $lines lines (minimum: 3000)"
    FAILED=1
fi

# Check 4: File:line references
echo ""
ref_count=$(grep -c ":[0-9]\+" "$REPORT_FILE" || echo "0")
if [[ $ref_count -ge 50 ]]; then
    echo -e "${GREEN}✓${NC} File:line references: $ref_count (minimum: 50)"
else
    echo -e "${YELLOW}⚠${NC}  Few file:line references: $ref_count (recommended: 50+)"
fi

# Check 5: No placeholders
echo ""
if grep -q "TODO\|TBD\|will be analyzed\|\[TBD\]" "$REPORT_FILE"; then
    echo -e "${RED}❌${NC} Report contains placeholders (TODO, TBD, etc.)"
    echo "Found:"
    grep -n "TODO\|TBD\|will be analyzed\|\[TBD\]" "$REPORT_FILE" | head -5
    FAILED=1
else
    echo -e "${GREEN}✓${NC} No placeholders found"
fi

# Check 6: Severity ratings present
echo ""
severity_count=$(grep -c "HIGH\|MEDIUM\|LOW" "$REPORT_FILE" || echo "0")
if [[ $severity_count -ge 20 ]]; then
    echo -e "${GREEN}✓${NC} Severity ratings: $severity_count (minimum: 20)"
else
    echo -e "${YELLOW}⚠${NC}  Few severity ratings: $severity_count (recommended: 20+)"
fi

# Final verdict
echo ""
echo "========================================"
if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}✅ VERIFICATION PASSED${NC}"
    echo "Report meets all quality gates."
    echo "You may proceed to Stage 7."
    exit 0
else
    echo -e "${RED}❌ VERIFICATION FAILED${NC}"
    echo ""
    echo "The report does not meet quality standards."
    echo "Please:"
    echo "  1. Identify incomplete sections"
    echo "  2. Regenerate missing/problematic chunks"
    echo "  3. Re-run verification"
    echo ""
    echo "DO NOT proceed to Stage 7 until verification passes."
    exit 1
fi
