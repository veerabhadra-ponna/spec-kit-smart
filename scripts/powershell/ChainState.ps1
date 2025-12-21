<#
.SYNOPSIS
Chain State Management Script for PowerShell

.DESCRIPTION
Manages state for chained prompt workflow in analyze-project command

.NOTES
Version: 1.0.0
#>

param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$Command,

    [Parameter(Position=1)]
    [string]$Arg1,

    [Parameter(Position=2)]
    [string]$Arg2,

    [switch]$Help
)

$ErrorActionPreference = "Stop"

# Script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Source common functions
. (Join-Path $ScriptDir "common.ps1")

# Get repository root
$RepoRoot = Get-RepoRoot

# Handle -Help
if ($Help -or $Command -eq "help" -or $Command -eq "--help" -or $Command -eq "-h") {
    Write-Host @"
Usage: ChainState.ps1 <command> [args]

Commands:
  generate-id              Generate unique chain ID
  init                     Initialize state directory
  save <stage> <json>      Save state for stage
  load <stage>             Load state for stage
  load-latest              Load latest state
  last-stage               Get last completed stage
  is-complete <stage>      Check if stage is complete
  chain-id                 Get chain ID from latest state
  init-state <chain_id>    Create initial state
  merge <old> <new>        Merge state objects
  mark-complete <state> <stage>  Mark stage as complete
  validate <json>          Validate state schema

Examples:
  ChainState.ps1 generate-id
  ChainState.ps1 init
  ChainState.ps1 save 01-init '{"chain_id":"abc123",...}'
  ChainState.ps1 load 01-init
  ChainState.ps1 last-stage
"@
    exit 0
}

# Command is required if not showing help
if ([string]::IsNullOrEmpty($Command)) {
    Write-Error "Command is required. Use -Help for usage information."
    exit 1
}

# State directory (always at repo root for consistency)
$StateDir = Join-Path $RepoRoot ".analysis\.state"

# Functions

function Generate-ChainId {
    <#
    .SYNOPSIS
    Generate unique chain ID
    #>
    # Generate 8-character hexadecimal string
    $bytes = New-Object byte[] 4
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    return [System.BitConverter]::ToString($bytes).Replace("-", "").ToLower()
}

function Initialize-StateDirectory {
    <#
    .SYNOPSIS
    Initialize state directory
    #>
    if (-not (Test-Path $StateDir)) {
        New-Item -Path $StateDir -ItemType Directory -Force | Out-Null
    }
    Write-Host "✓ Initialized state directory: $StateDir"
}

function Save-State {
    <#
    .SYNOPSIS
    Save state to file
    #>
    param(
        [string]$StageName,
        [string]$StateJson
    )

    # Validate JSON format before saving (prevent injection)
    try {
        $null = $StateJson | ConvertFrom-Json -ErrorAction Stop
    } catch {
        Write-Error "❌ ERROR: Invalid JSON format - cannot save state: $_"
        return
    }

    # Validate state schema (check required fields)
    if (-not (Test-StateValid -StateJson $StateJson)) {
        Write-Error "❌ ERROR: State validation failed - cannot save"
        return
    }

    $stateFile = Join-Path $StateDir "$StageName.json"

    # Write validated JSON safely (re-format to ensure clean output)
    $StateJson | ConvertFrom-Json | ConvertTo-Json -Depth 10 | Out-File -FilePath $stateFile -Encoding utf8 -Force

    # Also save as latest
    $latestFile = Join-Path $StateDir "latest.json"
    $StateJson | ConvertFrom-Json | ConvertTo-Json -Depth 10 | Out-File -FilePath $latestFile -Encoding utf8 -Force

    Write-Host "✓ State saved: $stateFile"
}

function Load-State {
    <#
    .SYNOPSIS
    Load state from file
    #>
    param(
        [string]$StageName
    )

    $stateFile = Join-Path $StateDir "$StageName.json"

    if (Test-Path $stateFile) {
        Get-Content $stateFile -Raw
    } else {
        Write-Error "State file not found: $stateFile"
        return "{}"
    }
}

function Load-LatestState {
    <#
    .SYNOPSIS
    Load latest state
    #>
    $stateFile = Join-Path $StateDir "latest.json"

    if (Test-Path $stateFile) {
        Get-Content $stateFile -Raw
    } else {
        Write-Error "Latest state file not found"
        return "{}"
    }
}

function Get-LastCompletedStage {
    <#
    .SYNOPSIS
    Get last completed stage
    #>
    if (-not (Test-Path $StateDir)) {
        return "none"
    }

    # Find the highest numbered stage file
    $stageFiles = Get-ChildItem -Path $StateDir -Filter "*.json" -File |
        Where-Object { $_.Name -match '^\d{2}[ab]?-.*\.json$' } |
        Sort-Object Name -Descending |
        Select-Object -First 1

    if ($null -eq $stageFiles) {
        return "none"
    } else {
        return $stageFiles.BaseName
    }
}

function Test-StageComplete {
    <#
    .SYNOPSIS
    Check if stage is complete
    #>
    param(
        [string]$StageName
    )

    $stateFile = Join-Path $StateDir "$StageName.json"
    return (Test-Path $stateFile)
}

function Get-ChainId {
    <#
    .SYNOPSIS
    Get chain ID from state
    #>
    $stateFile = Join-Path $StateDir "latest.json"

    if (Test-Path $stateFile) {
        try {
            $state = Get-Content $stateFile -Raw | ConvertFrom-Json
            return $state.chain_id
        } catch {
            return "unknown"
        }
    } else {
        return "unknown"
    }
}

function New-InitialState {
    <#
    .SYNOPSIS
    Create initial state
    #>
    param(
        [string]$ChainId
    )

    $timestamp = Get-Date -Format "o"

    $state = @{
        chain_id = $ChainId
        start_time = $timestamp
        timestamp = $timestamp
        stage = "initialization"
        stages_complete = @()
        current_stage = $null
    }

    return ($state | ConvertTo-Json -Depth 10)
}

function Merge-States {
    <#
    .SYNOPSIS
    Merge states (add new fields to existing state)
    #>
    param(
        [string]$OldStateJson,
        [string]$NewFieldsJson
    )

    try {
        $oldState = $OldStateJson | ConvertFrom-Json -AsHashtable
        $newFields = $NewFieldsJson | ConvertFrom-Json -AsHashtable

        # Merge hashtables (new fields override old)
        foreach ($key in $newFields.Keys) {
            $oldState[$key] = $newFields[$key]
        }

        return ($oldState | ConvertTo-Json -Depth 10)
    } catch {
        Write-Error "Failed to merge states: $_"
        return "{}"
    }
}

function Add-StageComplete {
    <#
    .SYNOPSIS
    Add stage to completed list
    #>
    param(
        [string]$StateJson,
        [string]$StageName
    )

    try {
        $state = $StateJson | ConvertFrom-Json -AsHashtable
        $timestamp = Get-Date -Format "o"

        if ($null -eq $state.stages_complete) {
            $state.stages_complete = @()
        }

        $state.stages_complete += $StageName
        $state.timestamp = $timestamp

        return ($state | ConvertTo-Json -Depth 10)
    } catch {
        Write-Error "Failed to mark stage complete: $_"
        return $StateJson
    }
}

function Test-StateValid {
    <#
    .SYNOPSIS
    Validate state schema
    #>
    param(
        [string]$StateJson
    )

    try {
        $state = $StateJson | ConvertFrom-Json

        # Check required fields
        if ([string]::IsNullOrEmpty($state.chain_id) -or [string]::IsNullOrEmpty($state.timestamp)) {
            Write-Error "Invalid state: missing chain_id or timestamp"
            return $false
        }

        return $true
    } catch {
        Write-Error "Invalid state JSON: $_"
        return $false
    }
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "generate-id" {
        Generate-ChainId
    }
    "init" {
        Initialize-StateDirectory
    }
    "save" {
        if ([string]::IsNullOrEmpty($Arg1) -or [string]::IsNullOrEmpty($Arg2)) {
            Write-Error "Usage: ChainState.ps1 save <stage> <json>"
            exit 1
        }
        Save-State -StageName $Arg1 -StateJson $Arg2
    }
    "load" {
        if ([string]::IsNullOrEmpty($Arg1)) {
            Write-Error "Usage: ChainState.ps1 load <stage>"
            exit 1
        }
        Load-State -StageName $Arg1
    }
    "load-latest" {
        Load-LatestState
    }
    "last-stage" {
        Get-LastCompletedStage
    }
    "is-complete" {
        if ([string]::IsNullOrEmpty($Arg1)) {
            Write-Error "Usage: ChainState.ps1 is-complete <stage>"
            exit 1
        }
        if (Test-StageComplete -StageName $Arg1) {
            Write-Output "true"
        } else {
            Write-Output "false"
        }
    }
    "chain-id" {
        Get-ChainId
    }
    "init-state" {
        if ([string]::IsNullOrEmpty($Arg1)) {
            Write-Error "Usage: ChainState.ps1 init-state <chain_id>"
            exit 1
        }
        New-InitialState -ChainId $Arg1
    }
    "merge" {
        if ([string]::IsNullOrEmpty($Arg1) -or [string]::IsNullOrEmpty($Arg2)) {
            Write-Error "Usage: ChainState.ps1 merge <old_json> <new_json>"
            exit 1
        }
        Merge-States -OldStateJson $Arg1 -NewFieldsJson $Arg2
    }
    "mark-complete" {
        if ([string]::IsNullOrEmpty($Arg1) -or [string]::IsNullOrEmpty($Arg2)) {
            Write-Error "Usage: ChainState.ps1 mark-complete <state_json> <stage>"
            exit 1
        }
        Add-StageComplete -StateJson $Arg1 -StageName $Arg2
    }
    "validate" {
        if ([string]::IsNullOrEmpty($Arg1)) {
            Write-Error "Usage: ChainState.ps1 validate <json>"
            exit 1
        }
        if (Test-StateValid -StateJson $Arg1) {
            Write-Host "✓ Valid state"
        } else {
            Write-Host "❌ Invalid state"
            exit 1
        }
    }
    default {
        Write-Host @"
Usage: ChainState.ps1 <command> [args]

Commands:
  generate-id              Generate unique chain ID
  init                     Initialize state directory
  save <stage> <json>      Save state for stage
  load <stage>             Load state for stage
  load-latest              Load latest state
  last-stage               Get last completed stage
  is-complete <stage>      Check if stage is complete
  chain-id                 Get chain ID from latest state
  init-state <chain_id>    Create initial state
  merge <old> <new>        Merge state objects
  mark-complete <state> <stage>  Mark stage as complete
  validate <json>          Validate state schema

Examples:
  ChainState.ps1 generate-id
  ChainState.ps1 init
  ChainState.ps1 save 01-init '{"chain_id":"abc123",...}'
  ChainState.ps1 load 01-init
  ChainState.ps1 last-stage
"@
        exit 1
    }
}
