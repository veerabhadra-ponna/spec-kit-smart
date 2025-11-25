#Requires -Version 5.1

<#
.SYNOPSIS
    Optional prerequisite check for codebase index

.DESCRIPTION
    Used by commands that BENEFIT from index but can work without it (e.g., /speckitsmart.implement)

    Unlike the hard prerequisite check, this script:
    - Always exits with 0 (success)
    - Returns JSON with status and recommendations
    - Allows callers to decide whether to proceed without index

.EXAMPLE
    & .\Check-IndexOptional.ps1

.NOTES
    Exit codes:
      0 - Always (soft check doesn't block)

    Output: JSON with status and recommendations
#>

[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'SilentlyContinue'

# Helper functions
function Get-RepoRoot {
    try {
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($gitRoot) {
            return $gitRoot -replace '/', '\'
        }
    }
    catch {
        # Git not available
    }
    return (Get-Location).Path
}

function Get-AgeDays {
    param([string]$FreshnessDate)

    try {
        $freshnessDateTime = [DateTime]::Parse($FreshnessDate)
        $currentDateTime = [DateTime]::UtcNow
        $diff = $currentDateTime - $freshnessDateTime
        return [int]$diff.TotalDays
    }
    catch {
        return 0
    }
}

$repoRoot = Get-RepoRoot
$indexDir = Join-Path (Join-Path $repoRoot '.analysis') 'index'
$metadataFile = Join-Path $indexDir 'metadata.json'

# Check if index directory exists
if (-not (Test-Path $indexDir)) {
    @{
        index_exists           = $false
        index_available        = $false
        status                 = 'missing'
        recommendation         = 'Run /speckitsmart.index to enable enhanced features'
        disabled_features      = @(
            'Code reusability checks (40-60% potential reuse)',
            'Architecture pattern detection',
            'Similar implementation suggestions',
            'Test example templates'
        )
        continue_without_index = $true
        message                = 'Index not found. Running without enhanced features.'
    } | ConvertTo-Json -Depth 5
    exit 0
}

# Check if metadata.json exists
if (-not (Test-Path $metadataFile)) {
    @{
        index_exists           = $false
        index_available        = $false
        status                 = 'corrupted'
        recommendation         = 'Run /speckitsmart.index --full to rebuild the index'
        disabled_features      = @(
            'Code reusability checks',
            'Architecture pattern detection',
            'Similar implementation suggestions'
        )
        continue_without_index = $true
        message                = 'Index metadata missing (corrupted). Running without enhanced features.'
    } | ConvertTo-Json -Depth 5
    exit 0
}

# Try to read and validate metadata
try {
    $metadata = Get-Content $metadataFile -Raw | ConvertFrom-Json

    if (-not $metadata.version -or -not $metadata.freshness -or -not $metadata.statistics) {
        throw "Invalid metadata structure"
    }

    $version = $metadata.version
    $freshness = $metadata.freshness
    $filesIndexed = $metadata.statistics.indexed_files
    $totalClasses = $metadata.statistics.total_classes
    $totalFunctions = $metadata.statistics.total_functions

    $ageDays = Get-AgeDays $freshness
    $isStale = $ageDays -gt 7
    $status = if ($isStale) { 'stale' } else { 'fresh' }

    $enabledFeatures = @(
        'Code reusability checks',
        'Architecture pattern detection',
        'Similar implementation suggestions',
        'Test example templates'
    )

    if ($isStale) {
        @{
            index_exists           = $true
            index_available        = $true
            status                 = $status
            index_path             = $indexDir
            freshness              = $freshness
            age_days               = $ageDays
            is_stale               = $isStale
            files_indexed          = $filesIndexed
            total_classes          = $totalClasses
            total_functions        = $totalFunctions
            recommendation         = 'Consider running /speckitsmart.index --incremental to update'
            enabled_features       = $enabledFeatures
            warning                = "Index is $ageDays days old and may be stale. Results may not reflect recent changes."
            continue_without_index = $false
            message                = 'Index available but stale. Enhanced features enabled with potential outdated data.'
        } | ConvertTo-Json -Depth 5
    }
    else {
        @{
            index_exists           = $true
            index_available        = $true
            status                 = $status
            index_path             = $indexDir
            freshness              = $freshness
            age_days               = $ageDays
            is_stale               = $isStale
            files_indexed          = $filesIndexed
            total_classes          = $totalClasses
            total_functions        = $totalFunctions
            enabled_features       = $enabledFeatures
            continue_without_index = $false
            message                = 'Index available and fresh. All enhanced features enabled.'
        } | ConvertTo-Json -Depth 5
    }
}
catch {
    @{
        index_exists           = $true
        index_available        = $false
        status                 = 'invalid'
        recommendation         = 'Run /speckitsmart.index --full to rebuild the index'
        disabled_features      = @(
            'Code reusability checks',
            'Architecture pattern detection'
        )
        continue_without_index = $true
        message                = 'Invalid index format. Running without enhanced features.'
    } | ConvertTo-Json -Depth 5
}

exit 0
