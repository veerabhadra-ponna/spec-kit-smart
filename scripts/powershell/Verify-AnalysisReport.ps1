<#
.SYNOPSIS
Verification gate for Stage 6 analysis report

.DESCRIPTION
Enforces quality checks before proceeding to Stage 7

.PARAMETER ReportFile
Path to the analysis report file

.EXAMPLE
.\Verify-AnalysisReport.ps1 .analysis/myproject-20251114/analysis-report.md
#>

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$ReportFile,

    [switch]$Help
)

$ErrorActionPreference = "Stop"

# Handle -Help
if ($Help) {
    Write-Host @"
Usage: Verify-AnalysisReport.ps1 <report_file>

Verification gate for Stage 6 analysis report.

Checks:
  - All 9 phases present
  - Minimum 3,000 lines
  - 50+ file:line references
  - No placeholders (TODO, TBD)
  - Severity ratings present

Examples:
  Verify-AnalysisReport.ps1 .analysis/myproject-20251114/analysis-report.md

Exit codes:
  0 - All checks passed
  1 - One or more checks failed
"@
    exit 0
}

# ReportFile is required if not showing help
if ([string]::IsNullOrEmpty($ReportFile)) {
    Write-Error "ReportFile is required. Use -Help for usage information."
    exit 1
}

Write-Host "=== Analysis Report Verification Gate ===" -ForegroundColor Blue
Write-Host "Report: $ReportFile"
Write-Host ""

# Track failures
$Failed = 0

# Check 1: File exists
if (-not (Test-Path $ReportFile)) {
    Write-Host "❌ FAIL: Report file not found" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Report file exists" -ForegroundColor Green

# Check 2: All 9 phases present
Write-Host ""
Write-Host "Checking for all 9 phases..."
$phases = @("Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6", "Phase 7", "Phase 8", "Phase 9")
$content = Get-Content $ReportFile -Raw

foreach ($phase in $phases) {
    if ($content -match $phase) {
        Write-Host "✓ $phase found" -ForegroundColor Green
    } else {
        Write-Host "❌ MISSING: $phase" -ForegroundColor Red
        $Failed = 1
    }
}

# Check 3: Minimum line count
Write-Host ""
$lines = (Get-Content $ReportFile).Count
if ($lines -ge 3000) {
    Write-Host "✓ Line count: $lines (minimum: 3000)" -ForegroundColor Green
} else {
    Write-Host "❌ Report too short: $lines lines (minimum: 3000)" -ForegroundColor Red
    $Failed = 1
}

# Check 4: File:line references
Write-Host ""
$refCount = (Select-String -Path $ReportFile -Pattern ":\d+" -AllMatches).Matches.Count
if ($refCount -ge 50) {
    Write-Host "✓ File:line references: $refCount (minimum: 50)" -ForegroundColor Green
} else {
    Write-Host "⚠  Few file:line references: $refCount (recommended: 50+)" -ForegroundColor Yellow
}

# Check 5: No placeholders
Write-Host ""
$placeholders = Select-String -Path $ReportFile -Pattern "TODO|TBD|will be analyzed|\[TBD\]" -AllMatches
if ($placeholders) {
    Write-Host "❌ Report contains placeholders (TODO, TBD, etc.)" -ForegroundColor Red
    Write-Host "Found:"
    $placeholders | Select-Object -First 5 | ForEach-Object { Write-Host "  Line $($_.LineNumber): $($_.Line.Trim())" }
    $Failed = 1
} else {
    Write-Host "✓ No placeholders found" -ForegroundColor Green
}

# Check 6: Severity ratings present
Write-Host ""
$severityCount = (Select-String -Path $ReportFile -Pattern "HIGH|MEDIUM|LOW" -AllMatches).Matches.Count
if ($severityCount -ge 20) {
    Write-Host "✓ Severity ratings: $severityCount (minimum: 20)" -ForegroundColor Green
} else {
    Write-Host "⚠  Few severity ratings: $severityCount (recommended: 20+)" -ForegroundColor Yellow
}

# Final verdict
Write-Host ""
Write-Host "========================================"
if ($Failed -eq 0) {
    Write-Host "✅ VERIFICATION PASSED" -ForegroundColor Green
    Write-Host "Report meets all quality gates."
    Write-Host "You may proceed to Stage 7."
    exit 0
} else {
    Write-Host "❌ VERIFICATION FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "The report does not meet quality standards."
    Write-Host "Please:"
    Write-Host "  1. Identify incomplete sections"
    Write-Host "  2. Regenerate missing/problematic chunks"
    Write-Host "  3. Re-run verification"
    Write-Host ""
    Write-Host "DO NOT proceed to Stage 7 until verification passes."
    exit 1
}
