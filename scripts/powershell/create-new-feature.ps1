#!/usr/bin/env pwsh
[CmdletBinding()]
param(
    [switch]$Json,
    [string]$ShortName,
    [int]$Number = 0,
    [switch]$Help,
    [string]$EncodedArgs,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$FeatureDescription
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Show-Help {
    @"
Usage: ./create-new-feature.ps1 [-Json] [-ShortName <name>] [-Number N] [-EncodedArgs <base64>] <feature description>

Options:
  -Json             Output machine-readable JSON only
  -ShortName <name> Provide a custom short name for the branch
  -Number N         Override automatic numbering
  -EncodedArgs      Base64 encoded feature description (UTF-8)
  -Help             Show this help message
"@
}

if ($Help) {
    Show-Help
    exit 0
}

function Decode-FeatureText {
    param([string]$Encoded, [string[]]$Fallback)
    if ($Encoded) {
        try {
            $bytes = [Convert]::FromBase64String($Encoded)
            return [Text.Encoding]::UTF8.GetString($bytes)
        }
        catch {
            throw "Unable to decode EncodedArgs. Ensure the value is base64-encoded UTF-8 text."
        }
    }
    if ($Fallback -and $Fallback.Count -gt 0) {
        return ($Fallback -join ' ').Trim()
    }
    return ''
}

$featureDesc = Decode-FeatureText -Encoded $EncodedArgs -Fallback $FeatureDescription
if (-not $featureDesc) {
    throw "Feature description is required."
}

function Find-RepositoryRoot {
    param(
        [string]$StartDir,
        [string[]]$Markers = @('.git', '.specify')
    )
    $current = Resolve-Path $StartDir
    while ($true) {
        foreach ($marker in $Markers) {
            if (Test-Path (Join-Path $current $marker)) {
                return $current
            }
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current) { return $current }
        $current = $parent
    }
}

function Get-NextBranchNumber {
    param([string]$ShortName, [string]$SpecsDir)
    $numbers = @()
    try { git fetch --all --prune 2>$null | Out-Null } catch { }

    try {
        $remoteRefs = git ls-remote --heads origin 2>$null
        if ($remoteRefs) {
            $remoteRefs | ForEach-Object {
                if ($_ -match "refs/heads/(\\d+)-$([regex]::Escape($ShortName))$") {
                    $numbers += [int]$matches[1]
                }
            }
        }
    } catch { }

    try {
        $branches = git branch --format '%(refname:short)' 2>$null
        if ($branches) {
            $branches | ForEach-Object {
                if ($_ -match "^(\\d+)-$([regex]::Escape($ShortName))$") {
                    $numbers += [int]$matches[1]
                }
            }
        }
    } catch { }

    if (Test-Path $SpecsDir) {
        Get-ChildItem -Path $SpecsDir -Directory | ForEach-Object {
            if ($_.Name -match "^(\\d+)-$([regex]::Escape($ShortName))$") {
                $numbers += [int]$matches[1]
            }
        }
    }

    if ($numbers.Count -eq 0) { return 1 }
    return ([int]($numbers | Measure-Object -Maximum).Maximum) + 1
}

$repoRoot = $null
$hasGit = $false
try {
    $repoRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0 -and $repoRoot) { $hasGit = $true }
} catch {
    $repoRoot = $null
}

if (-not $repoRoot) {
    $repoRoot = (Find-RepositoryRoot -StartDir $PSScriptRoot)
}

if (-not $repoRoot) {
    throw "Unable to resolve repository root."
}

Push-Location $repoRoot
try {
    $specsDir = Join-Path $repoRoot 'specs'
    New-Item -ItemType Directory -Path $specsDir -Force | Out-Null

    function Build-BranchSuffix {
        param([string]$Text)
        $stopWords = @('i','a','an','the','to','for','of','in','on','at','by','with','from','is','are','was','were','be','been','being','have','has','had','do','does','did','will','would','should','could','can','may','might','must','shall','this','that','these','those','my','your','our','their','want','need','add','get','set')
        $clean = $Text.ToLower() -replace '[^a-z0-9\s]', ' '
        $words = $clean -split '\s+' | Where-Object { $_ }
        $selected = @()
        foreach ($word in $words) {
            if ($stopWords -contains $word) { continue }
            if ($word.Length -ge 3 -or $Text -match "\b$($word.ToUpper())\b") {
                $selected += $word
            }
        }
        if ($selected.Count -eq 0) {
            $fallback = $Text.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', ''
            return (($fallback -split '-') | Where-Object { $_ } | Select-Object -First 3) -join '-'
        }
        return ($selected | Select-Object -First 4) -join '-'
    }

    if ($ShortName) {
        $branchSuffix = ($ShortName.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', '')
    } else {
        $branchSuffix = Build-BranchSuffix -Text $featureDesc
    }
    if (-not $branchSuffix) { $branchSuffix = 'feature' }

    if ($Number -le 0) {
        $Number = Get-NextBranchNumber -ShortName $branchSuffix -SpecsDir $specsDir
    }

    $featureNum = ('{0:000}' -f $Number)
    $branchName = "$featureNum-$branchSuffix"
    $notes = @()

    $maxLength = 244
    if ($branchName.Length -gt $maxLength) {
        $maxSuffixLength = $maxLength - 4
        $truncatedSuffix = $branchSuffix.Substring(0, [Math]::Min($branchSuffix.Length, $maxSuffixLength)) -replace '-$', ''
        $notes += "Branch truncated to meet GitHub length limits."
        $branchName = "$featureNum-$truncatedSuffix"
    }

    if ($hasGit) {
        try {
            git rev-parse --verify $branchName 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) {
                $notes += "Branch $branchName already exists locally; not creating a new branch."
            } else {
                git checkout -b $branchName 2>$null | Out-Null
            }
        } catch {
            $notes += "Unable to create branch $branchName: $($_.Exception.Message)"
        }
    } else {
        $notes += "Git repository not detected; skipping branch creation."
    }

    $featureDir = Join-Path $specsDir $branchName
    New-Item -ItemType Directory -Path $featureDir -Force | Out-Null

    $template = Join-Path $repoRoot '.specify/templates/spec-template.md'
    $specFile = Join-Path $featureDir 'spec.md'
    if (Test-Path $template) {
        Copy-Item $template $specFile -Force
    } else {
        New-Item -ItemType File -Path $specFile -Force | Out-Null
        $notes += "Spec template not found; created empty spec.md."
    }

    $env:SPECIFY_FEATURE = $branchName

    $payload = [ordered]@{
        ok       = $true
        version  = '1.0.0'
        timestamp = (Get-Date).ToString('o')
        branch   = $branchName
        feature_number = $featureNum
        has_git  = $hasGit
        paths    = [ordered]@{
            repo_root  = $repoRoot
            feature_dir = $featureDir
            spec        = $specFile
        }
        notes    = $notes
        description = $featureDesc
    }

    if ($Json) {
        $payload | ConvertTo-Json -Depth 6 -Compress
    } else {
        "BRANCH_NAME: $branchName"
        "FEATURE_NUM: $featureNum"
        "SPEC_FILE: $specFile"
        "HAS_GIT: $hasGit"
        if ($notes) { "NOTES: $([string]::Join('; ', $notes))" }
    }
}
catch {
    $message = $_.Exception.Message
    if ($Json) {
        [ordered]@{
            ok = $false
            timestamp = (Get-Date).ToString('o')
            error = $message
        } | ConvertTo-Json -Compress
    } else {
        Write-Error $message
    }
    exit 1
}
finally {
    Pop-Location | Out-Null
}
