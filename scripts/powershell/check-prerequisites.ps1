#!/usr/bin/env pwsh

# Consolidated prerequisite checking script (PowerShell)
#
# This script provides unified prerequisite checking for Spec-Driven Development workflow.
# It replaces the functionality previously spread across multiple scripts.
#
# Usage: ./check-prerequisites.ps1 [OPTIONS]
#
# OPTIONS:
#   -Json               Output in JSON format
#   -RequireTasks       Require tasks.md to exist (for implementation phase)
#   -IncludeTasks       Include tasks.md in AVAILABLE_DOCS list
#   -PathsOnly          Only output path variables (no validation)
#   -Help, -h           Show help message

[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$RequireTasks,
    [switch]$IncludeTasks,
    [switch]$PathsOnly,
    [switch]$Help,
    [string]$Arguments = ""
)

$ErrorActionPreference = 'Stop'

# Auto-detect OS and redirect if needed
. "$PSScriptRoot/common.ps1"

$OS = Get-DetectedOS
if ($OS -eq "unix") {
    # Running PowerShell on Unix - redirect to bash
    $bashScript = Join-Path $PSScriptRoot "../bash/check-prerequisites.sh"

    # Convert PowerShell switches to bash arguments
    $bashArgs = @()
    if ($Json) { $bashArgs += "--json" }
    if ($RequireTasks) { $bashArgs += "--require-tasks" }
    if ($IncludeTasks) { $bashArgs += "--include-tasks" }
    if ($PathsOnly) { $bashArgs += "--paths-only" }
    if ($Help) { $bashArgs += "--help" }
    if ($Arguments) { $bashArgs += $Arguments }

    & bash $bashScript @bashArgs
    exit $LASTEXITCODE
}

# Continue with PowerShell implementation for Windows

# Show help if requested
if ($Help) {
    Write-Output "Usage: check-prerequisites.ps1 [OPTIONS]"
    Write-Output ""
    Write-Output "Consolidated prerequisite checking for Spec-Driven Development workflow."
    Write-Output ""
    Write-Output "OPTIONS:"
    Write-Output "  -Json               Output in JSON format"
    Write-Output "  -RequireTasks       Require tasks.md to exist (for implementation phase)"
    Write-Output "  -IncludeTasks       Include tasks.md in AVAILABLE_DOCS list"
    Write-Output "  -PathsOnly          Only output path variables (no prerequisite validation)"
    Write-Output "  -Arguments          Optional user description (for consistency with setup-plan)"
    Write-Output "  -Help, -h           Show this help message"
    Write-Output ""
    Write-Output "EXAMPLES:"
    Write-Output "  # Check task prerequisites (plan.md required)"
    Write-Output "  .\check-prerequisites.ps1 -Json"
    Write-Output "  "
    Write-Output "  # Check implementation prerequisites (plan.md + tasks.md required)"
    Write-Output "  .\check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks"
    Write-Output "  "
    Write-Output "  # Get feature paths only (no validation)"
    Write-Output "  .\check-prerequisites.ps1 -PathsOnly"
    Write-Output ""
    exit 0
}

# Source common functions
. "$PSScriptRoot/common.ps1"

# Get feature paths and validate branch
$paths = Get-FeaturePathsEnv

if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit:$paths.HAS_GIT)) { 
    exit 1 
}

# If paths-only mode, output paths and exit (support combined -Json -PathsOnly)
if ($PathsOnly) {
    if ($Json) {
        [PSCustomObject]@{
            REPO_ROOT    = $paths.REPO_ROOT
            BRANCH       = $paths.CURRENT_BRANCH
            FEATURE_DIR  = $paths.FEATURE_DIR
            FEATURE_SPEC = $paths.FEATURE_SPEC
            IMPL_PLAN    = $paths.IMPL_PLAN
            TASKS        = $paths.TASKS
        } | ConvertTo-Json -Compress
    } else {
        Write-Output "REPO_ROOT: $($paths.REPO_ROOT)"
        Write-Output "BRANCH: $($paths.CURRENT_BRANCH)"
        Write-Output "FEATURE_DIR: $($paths.FEATURE_DIR)"
        Write-Output "FEATURE_SPEC: $($paths.FEATURE_SPEC)"
        Write-Output "IMPL_PLAN: $($paths.IMPL_PLAN)"
        Write-Output "TASKS: $($paths.TASKS)"
    }
    exit 0
}

# Validate required directories and files
if (-not (Test-Path $paths.FEATURE_DIR -PathType Container)) {
    Write-Output "ERROR: Feature directory not found: $($paths.FEATURE_DIR)"
    Write-Output "Run /speckitsmart.specify first to create the feature structure."
    exit 1
}

if (-not (Test-Path $paths.IMPL_PLAN -PathType Leaf)) {
    Write-Output "ERROR: plan.md not found in $($paths.FEATURE_DIR)"
    Write-Output "Run /speckitsmart.plan first to create the implementation plan."
    exit 1
}

# Check for tasks.md if required
if ($RequireTasks -and -not (Test-Path $paths.TASKS -PathType Leaf)) {
    Write-Output "ERROR: tasks.md not found in $($paths.FEATURE_DIR)"
    Write-Output "Run /speckitsmart.tasks first to create the task list."
    exit 1
}

# Build list of available documents
$docs = @()

# Always check these optional docs
if (Test-Path $paths.RESEARCH) { $docs += 'research.md' }
if (Test-Path $paths.DATA_MODEL) { $docs += 'data-model.md' }

# Check contracts directory (only if it exists and has files)
if ((Test-Path $paths.CONTRACTS_DIR) -and (Get-ChildItem -Path $paths.CONTRACTS_DIR -ErrorAction SilentlyContinue | Select-Object -First 1)) { 
    $docs += 'contracts/' 
}

if (Test-Path $paths.QUICKSTART) { $docs += 'quickstart.md' }

# Include tasks.md if requested and it exists
if ($IncludeTasks -and (Test-Path $paths.TASKS)) { 
    $docs += 'tasks.md' 
}

# Output results
if ($Json) {
    # JSON output
    [PSCustomObject]@{ 
        FEATURE_DIR = $paths.FEATURE_DIR
        AVAILABLE_DOCS = $docs 
    } | ConvertTo-Json -Compress
} else {
    # Text output
    Write-Output "FEATURE_DIR:$($paths.FEATURE_DIR)"
    Write-Output "AVAILABLE_DOCS:"
    
    # Show status of each potential document
    Test-FileExists -Path $paths.RESEARCH -Description 'research.md' | Out-Null
    Test-FileExists -Path $paths.DATA_MODEL -Description 'data-model.md' | Out-Null
    Test-DirHasFiles -Path $paths.CONTRACTS_DIR -Description 'contracts/' | Out-Null
    Test-FileExists -Path $paths.QUICKSTART -Description 'quickstart.md' | Out-Null
    
    if ($IncludeTasks) {
        Test-FileExists -Path $paths.TASKS -Description 'tasks.md' | Out-Null
    }
}
