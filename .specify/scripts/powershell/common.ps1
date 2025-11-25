#!/usr/bin/env pwsh
# Common PowerShell functions analogous to common.sh

function Get-RepoRoot {
    try {
        $result = git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $result
        }
    } catch {
        # Git command failed
    }
    
    # Fall back to script location for non-git repos
    return (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
}

function Get-CurrentBranch {
    # First check if SPECIFY_FEATURE environment variable is set
    if ($env:SPECIFY_FEATURE) {
        return $env:SPECIFY_FEATURE
    }
    
    # Then check git if available
    try {
        $result = git rev-parse --abbrev-ref HEAD 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $result
        }
    } catch {
        # Git command failed
    }
    
    # For non-git repos, try to find the latest feature directory
    $repoRoot = Get-RepoRoot
    $specsDir = Join-Path $repoRoot "specs"
    
    if (Test-Path $specsDir) {
        $latestFeature = ""
        $highest = 0
        
        Get-ChildItem -Path $specsDir -Directory | ForEach-Object {
            if ($_.Name -match '^(\d{3})-') {
                $num = [int]$matches[1]
                if ($num -gt $highest) {
                    $highest = $num
                    $latestFeature = $_.Name
                }
            }
        }
        
        if ($latestFeature) {
            return $latestFeature
        }
    }
    
    # Final fallback
    return "main"
}

function Test-HasGit {
    try {
        git rev-parse --show-toplevel 2>$null | Out-Null
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

function Test-FeatureBranch {
    param(
        [string]$Branch,
        [bool]$HasGit = $true
    )
    
    # For non-git repos, we can't enforce branch naming but still provide output
    if (-not $HasGit) {
        Write-Warning "[specify] Warning: Git repository not detected; skipped branch validation"
        return $true
    }
    
    if ($Branch -notmatch '^[0-9]{3}-') {
        Write-Output "ERROR: Not on a feature branch. Current branch: $Branch"
        Write-Output "Feature branches should be named like: 001-feature-name"
        return $false
    }
    return $true
}

# Find feature directory - extract folder name from branch name
# Splits branch name by '/' or '\' and takes the last part
# Example: "feature/C12345-6789-new-app" → "C12345-6789-new-app"
function Find-FeatureDirByPrefix {
    param(
        [string]$RepoRoot,
        [string]$BranchName
    )

    $specsDir = Join-Path $RepoRoot "specs"

    # Extract the last part of branch name (after last '/' or '\')
    # Filter out empty strings to handle edge cases
    $parts = $BranchName.Split(@('/', '\')) | Where-Object { $_ -ne '' }
    if ($parts.Count -gt 0) {
        $folderName = $parts[-1]
    } else {
        $folderName = $BranchName
    }

    # Ensure folder name doesn't contain any slashes (defensive check)
    $folderName = $folderName -replace '[/\\]', '-'

    # Return specs/folder_name path
    return (Join-Path $specsDir $folderName)
}

function Get-FeaturePathsEnv {
    $repoRoot = Get-RepoRoot
    $currentBranch = Get-CurrentBranch
    $hasGit = Test-HasGit

    # Use prefix-based lookup to support multiple branches per spec
    $featureDir = Find-FeatureDirByPrefix -RepoRoot $repoRoot -BranchName $currentBranch

    [PSCustomObject]@{
        REPO_ROOT     = $repoRoot
        CURRENT_BRANCH = $currentBranch
        HAS_GIT       = $hasGit
        FEATURE_DIR   = $featureDir
        FEATURE_SPEC  = Join-Path $featureDir 'spec.md'
        IMPL_PLAN     = Join-Path $featureDir 'plan.md'
        TASKS         = Join-Path $featureDir 'tasks.md'
        RESEARCH      = Join-Path $featureDir 'research.md'
        DATA_MODEL    = Join-Path $featureDir 'data-model.md'
        QUICKSTART    = Join-Path $featureDir 'quickstart.md'
        CONTRACTS_DIR = Join-Path $featureDir 'contracts'
    }
}

function Test-FileExists {
    param([string]$Path, [string]$Description)
    if (Test-Path -Path $Path -PathType Leaf) {
        Write-Output "  [OK] $Description"
        return $true
    } else {
        Write-Output "  [X] $Description"
        return $false
    }
}

function Test-DirHasFiles {
    param([string]$Path, [string]$Description)
    if ((Test-Path -Path $Path -PathType Container) -and (Get-ChildItem -Path $Path -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Select-Object -First 1)) {
        Write-Output "  [OK] $Description"
        return $true
    } else {
        Write-Output "  [X] $Description"
        return $false
    }
}

# Load Spec Kit configuration from .specify/config.json
# Sets environment variables:
#   SPEC_KIT_OS_ENV - OS override from config ("windows", "unix", "auto")
#   SPEC_KIT_CHECK_ARTIFACTORY - Whether to check artifactory ("true" or "false")
function Load-SpecKitConfig {
    $repoRoot = Get-RepoRoot
    $configFile = Join-Path $repoRoot ".specify\config.json"

    # Defaults
    $env:SPEC_KIT_OS_ENV = "auto"
    $env:SPEC_KIT_CHECK_ARTIFACTORY = "false"

    # Try to read config if exists
    if (Test-Path $configFile) {
        try {
            $config = Get-Content $configFile -Raw | ConvertFrom-Json

            # Get osEnv and checkArt from nested workflow structure with defaults
            $osEnv = if ($config.workflow -and $config.workflow.PSObject.Properties.Name -contains "osEnv") { $config.workflow.osEnv } else { "auto" }
            $checkArt = if ($config.workflow -and $config.workflow.PSObject.Properties.Name -contains "enableCheckArtifactory") { $config.workflow.enableCheckArtifactory } else { $false }

            # Validate osEnv value
            if ($osEnv -eq "windows" -or $osEnv -eq "unix" -or $osEnv -eq "auto") {
                $env:SPEC_KIT_OS_ENV = $osEnv
            } else {
                Write-Warning "WARNING: Invalid osEnv value in .specify/config.json: `"$osEnv`""
                Write-Warning "Valid values: `"windows`", `"unix`", `"auto`""
                Write-Warning "Falling back to `"auto`" (OS auto-detection)"
                $env:SPEC_KIT_OS_ENV = "auto"
            }

            # Set check_artifactory
            if ($checkArt -eq $true) {
                $env:SPEC_KIT_CHECK_ARTIFACTORY = "true"
            } else {
                $env:SPEC_KIT_CHECK_ARTIFACTORY = "false"
            }
        } catch {
            # JSON parsing failed, use defaults
            Write-Warning "Failed to parse .specify/config.json: $($_.Exception.Message)"
        }
    }
}

# Detect operating system using config priority:
# 1. Config file (.specify/config.json osEnv)
# 2. Environment variable (SPEC_KIT_PLATFORM)
# 3. Auto-detection ($env:OS check)
# Returns: "windows" or "unix"
function Get-DetectedOS {
    # Load config if not already loaded
    if (-not $env:SPEC_KIT_OS_ENV) {
        Load-SpecKitConfig
    }

    # Priority 1: Config file override
    if ($env:SPEC_KIT_OS_ENV -eq "windows") {
        return "windows"
    } elseif ($env:SPEC_KIT_OS_ENV -eq "unix") {
        return "unix"
    }

    # Priority 2: Environment variable override
    if ($env:SPEC_KIT_PLATFORM -eq "windows") {
        return "windows"
    } elseif ($env:SPEC_KIT_PLATFORM -eq "unix") {
        return "unix"
    }

    # Priority 3: Auto-detect
    if ($env:OS -eq "Windows_NT") {
        return "windows"
    } else {
        return "unix"
    }
}

