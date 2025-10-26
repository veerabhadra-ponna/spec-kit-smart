#!/usr/bin/env pwsh
[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($Help) {
@" 
Usage: ./orchestrate-feature.ps1 [-Json]

Prepares metadata for the /speckit.feature command and ensures status directories exist.
"@
    exit 0
}

. "$PSScriptRoot/common.ps1"

$paths = Get-FeaturePathsEnv
$branchOk = Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit:$paths.HAS_GIT -Quiet:$Json
$statusDir = Join-Path $paths.FEATURE_DIR 'status'
New-Item -ItemType Directory -Path $statusDir -Force | Out-Null

$payload = [ordered]@{
    ok        = $branchOk
    version   = '1.0.0'
    timestamp = (Get-Date).ToString('o')
    branch    = $paths.CURRENT_BRANCH
    paths     = [ordered]@{
        feature_dir = $paths.FEATURE_DIR
        spec        = $paths.FEATURE_SPEC
        plan        = $paths.IMPL_PLAN
        tasks       = $paths.TASKS
        status_dir  = $statusDir
        status_spec = Join-Path $statusDir 'specify.md'
        status_plan = Join-Path $statusDir 'plan.md'
        status_tasks = Join-Path $statusDir 'tasks.md'
        status_feature = Join-Path $statusDir 'feature.md'
    }
    notes     = if ($branchOk) { @() } else { @('Not on a numbered feature branch.') }
}

if ($Json) {
    $payload | ConvertTo-Json -Depth 5 -Compress
    if ($payload.ok) { exit 0 } else { exit 1 }
}

Write-Output "FEATURE_DIR: $($paths.FEATURE_DIR)"
Write-Output "STATUS_DIR: $statusDir"
