#!/usr/bin/env pwsh

[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$RequireTasks,
    [switch]$IncludeTasks,
    [switch]$PathsOnly,
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($Help) {
@" 
Usage: ./check-prerequisites.ps1 [OPTIONS]

Options:
  -Json             Emit JSON only
  -RequireTasks     Fail if tasks.md is missing
  -IncludeTasks     Add tasks.md to AVAILABLE_DOCS when present
  -PathsOnly        Return path metadata without validation
  -Help             Display this help message
"@
    exit 0
}

. "$PSScriptRoot/common.ps1"

$paths = Get-FeaturePathsEnv
$branchOk = Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit:$paths.HAS_GIT -Quiet:$Json

$payload = [ordered]@{
    ok          = $true
    version     = '1.0.0'
    timestamp   = (Get-Date).ToString('o')
    branch      = $paths.CURRENT_BRANCH
    require_tasks = [bool]$RequireTasks
    paths       = [ordered]@{
        repo_root    = $paths.REPO_ROOT
        feature_dir  = $paths.FEATURE_DIR
        feature_spec = $paths.FEATURE_SPEC
        plan         = $paths.IMPL_PLAN
        tasks        = $paths.TASKS
    }
    available_docs = @()
    missing     = @()
    notes       = @()
}

if (-not $branchOk) {
    $payload.ok = $false
    $payload.notes += "Not on a numbered feature branch."
    if (-not $Json) {
        Write-Output "ERROR: Not on a feature branch. Current branch: $($paths.CURRENT_BRANCH)"
        Write-Output "Feature branches should be named like: 001-feature-name"
    }
}

if ($PathsOnly) {
    if ($Json) {
        $payload | Select-Object -Property ok,version,timestamp,branch,@{Name='paths';Expression={$_.paths}} | ConvertTo-Json -Depth 4 -Compress
    } else {
        Write-Output "REPO_ROOT: $($paths.REPO_ROOT)"
        Write-Output "BRANCH: $($paths.CURRENT_BRANCH)"
        Write-Output "FEATURE_DIR: $($paths.FEATURE_DIR)"
        Write-Output "FEATURE_SPEC: $($paths.FEATURE_SPEC)"
        Write-Output "IMPL_PLAN: $($paths.IMPL_PLAN)"
        Write-Output "TASKS: $($paths.TASKS)"
    }
    if ($payload.ok) { exit 0 } else { exit 1 }
}

$errors = @()
if (-not (Test-Path $paths.FEATURE_DIR -PathType Container)) {
    $payload.ok = $false
    $errors += "Feature directory not found: $($paths.FEATURE_DIR)"
}
if (-not (Test-Path $paths.IMPL_PLAN -PathType Leaf)) {
    $payload.ok = $false
    $errors += "plan.md not found in $($paths.FEATURE_DIR)"
}
if ($RequireTasks -and -not (Test-Path $paths.TASKS -PathType Leaf)) {
    $payload.ok = $false
    $errors += "tasks.md not found in $($paths.FEATURE_DIR)"
}

$docs = @()
if (Test-Path $paths.RESEARCH) { $docs += 'research.md' }
if (Test-Path $paths.DATA_MODEL) { $docs += 'data-model.md' }
if ((Test-Path $paths.CONTRACTS_DIR) -and (Get-ChildItem -Path $paths.CONTRACTS_DIR -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Select-Object -First 1)) {
    $docs += 'contracts/'
}
if (Test-Path $paths.QUICKSTART) { $docs += 'quickstart.md' }
if ($IncludeTasks -and (Test-Path $paths.TASKS -PathType Leaf)) { $docs += 'tasks.md' }

$payload.available_docs = $docs
$payload.missing = $errors

if ($Json) {
    if (-not $payload.ok -and $errors.Count -gt 0) {
        $payload.notes += $errors
    }
    $payload | ConvertTo-Json -Depth 6 -Compress
    if ($payload.ok) { exit 0 } else { exit 1 }
}

if ($errors.Count -gt 0) {
    foreach ($err in $errors) {
        Write-Output "ERROR: $err"
    }
    if (-not (Test-Path $paths.FEATURE_DIR -PathType Container)) {
        Write-Output "Run /speckit.specify first to create the feature structure."
    } elseif (-not (Test-Path $paths.IMPL_PLAN -PathType Leaf)) {
        Write-Output "Run /speckit.plan first to create the implementation plan."
    } elseif ($RequireTasks) {
        Write-Output "Run /speckit.tasks first to create the task list."
    }
    exit 1
}

Write-Output "FEATURE_DIR:$($paths.FEATURE_DIR)"
Write-Output "AVAILABLE_DOCS:"
Test-FileExists -Path $paths.RESEARCH -Description 'research.md' | Out-Null
Test-FileExists -Path $paths.DATA_MODEL -Description 'data-model.md' | Out-Null
Test-DirHasFiles -Path $paths.CONTRACTS_DIR -Description 'contracts/' | Out-Null
Test-FileExists -Path $paths.QUICKSTART -Description 'quickstart.md' | Out-Null
if ($IncludeTasks) {
    Test-FileExists -Path $paths.TASKS -Description 'tasks.md' | Out-Null
}
