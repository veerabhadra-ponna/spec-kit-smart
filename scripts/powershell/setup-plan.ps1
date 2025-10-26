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
Usage: ./setup-plan.ps1 [-Json]

Ensures plan scaffolding exists for the active feature and returns key paths.
"@
    exit 0
}

. "$PSScriptRoot/common.ps1"

$paths = Get-FeaturePathsEnv
$branchOk = Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit $paths.HAS_GIT -Quiet:$Json

New-Item -ItemType Directory -Path $paths.FEATURE_DIR -Force | Out-Null

$template = Join-Path $paths.REPO_ROOT '.specify/templates/plan-template.md'
if (Test-Path $template) {
    Copy-Item $template $paths.IMPL_PLAN -Force
} else {
    New-Item -ItemType File -Path $paths.IMPL_PLAN -Force | Out-Null
}

$payload = [ordered]@{
    ok        = $branchOk
    version   = '1.0.0'
    timestamp = (Get-Date).ToString('o')
    branch    = $paths.CURRENT_BRANCH
    paths     = [ordered]@{
        feature_spec = $paths.FEATURE_SPEC
        plan         = $paths.IMPL_PLAN
        feature_dir  = $paths.FEATURE_DIR
    }
    notes     = @()
}

if (-not (Test-Path $template)) {
    $payload.notes += "Plan template not found at $template"
}
if (-not $branchOk) {
    $payload.notes += "Not on a numbered feature branch."
}

if ($Json) {
    $payload | ConvertTo-Json -Depth 5 -Compress
    if ($payload.ok) { exit 0 } else { exit 1 }
}

Write-Output "FEATURE_SPEC: $($paths.FEATURE_SPEC)"
Write-Output "IMPL_PLAN: $($paths.IMPL_PLAN)"
Write-Output "SPECS_DIR: $($paths.FEATURE_DIR)"
Write-Output "BRANCH: $($paths.CURRENT_BRANCH)"
Write-Output "HAS_GIT: $($paths.HAS_GIT)"
if ($payload.notes) {
    Write-Output "NOTES: $([string]::Join('; ', $payload.notes))"
}
