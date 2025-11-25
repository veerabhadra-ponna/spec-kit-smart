#Requires -Version 5.1

<#
.SYNOPSIS
    Hard prerequisite check for codebase index

.DESCRIPTION
    Validates that a codebase index exists and is valid.
    Used by commands that REQUIRE an index (e.g., /speckitsmart.wiki, /speckitsmart.ask)

.OUTPUTS
    JSON object with index status

.EXAMPLE
    & scripts\powershell\Check-IndexPrerequisite.ps1

.NOTES
    Exit codes:
      0 - Index exists and is valid
      1 - Index missing or invalid
#>

[CmdletBinding()]
param(
    [switch]$Help
)

# Handle -Help parameter
if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-RepoRoot {
    try {
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($gitRoot) {
            return $gitRoot -replace '/', '\'
        }
    }
    catch {
        # Git not available or not in a repo
    }
    return (Get-Location).Path
}

function Get-AgeDays {
    param([string]$FreshnessDate)

    try {
        $freshness = [DateTime]::Parse($FreshnessDate)
        $current = [DateTime]::UtcNow
        $diff = $current - $freshness
        return [int]$diff.TotalDays
    }
    catch {
        return 0
    }
}

try {
    $repoRoot = Get-RepoRoot
    $indexDir = Join-Path $repoRoot '.analysis' 'index'
    $metadataFile = Join-Path $indexDir 'metadata.json'

    # Check if index directory exists
    if (-not (Test-Path $indexDir -PathType Container)) {
        $output = @{
            index_exists = $false
            error = "Codebase index not found. Run /speckitsmart.index to build it first."
        }
        Write-Output ($output | ConvertTo-Json -Compress)
        exit 1
    }

    # Check if metadata.json exists
    if (-not (Test-Path $metadataFile -PathType Leaf)) {
        $output = @{
            index_exists = $false
            error = "Index metadata missing (corrupted index). Run /speckitsmart.index --full to rebuild."
        }
        Write-Output ($output | ConvertTo-Json -Compress)
        exit 1
    }

    # Parse and validate metadata
    try {
        $metadata = Get-Content $metadataFile -Raw | ConvertFrom-Json

        if (-not $metadata.version -or -not $metadata.freshness -or -not $metadata.statistics) {
            throw "Missing required fields"
        }

        $ageDays = Get-AgeDays -FreshnessDate $metadata.freshness
        $isStale = $ageDays -gt 7

        $output = @{
            index_exists = $true
            index_path = $indexDir
            freshness = $metadata.freshness
            age_days = $ageDays
            is_stale = $isStale
            files_indexed = $metadata.statistics.indexed_files
        }

        Write-Output ($output | ConvertTo-Json -Compress)
        exit 0
    }
    catch {
        $output = @{
            index_exists = $false
            error = "Invalid index metadata format (corrupted). Run /speckitsmart.index --full to rebuild."
        }
        Write-Output ($output | ConvertTo-Json -Compress)
        exit 1
    }
}
catch {
    $output = @{
        index_exists = $false
        error = "Failed to check index: $_"
    }
    Write-Output ($output | ConvertTo-Json -Compress)
    exit 1
}
