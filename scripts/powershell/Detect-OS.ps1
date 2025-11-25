#Requires -Version 5.1

<#
.SYNOPSIS
    Central OS detection utility for cross-platform script routing

.DESCRIPTION
    Detects the operating system platform and returns standardized output
    for routing to platform-specific scripts.

.OUTPUTS
    System.String - Platform type: "unix" or "windows"

.EXAMPLE
    $platform = & .specify\scripts\powershell\Detect-OS.ps1
    if ($platform -eq "windows") {
        # Run Windows-specific commands
    }

.NOTES
    Exit codes:
      0 - Success
      1 - Unable to detect platform
#>

[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

try {
    # Check for SPEC_KIT_PLATFORM environment variable override
    $envPlatform = $env:SPEC_KIT_PLATFORM

    if ($envPlatform) {
        switch ($envPlatform.ToLower()) {
            'unix' {
                Write-Output 'unix'
                exit 0
            }
            'windows' {
                Write-Output 'windows'
                exit 0
            }
            'auto' {
                # Continue with automatic detection
            }
            default {
                Write-Error "Invalid SPEC_KIT_PLATFORM value: $envPlatform (expected: unix, windows, or auto)"
                exit 1
            }
        }
    }

    # Detect platform using $IsWindows, $IsLinux, $IsMacOS (PowerShell Core)
    if ($PSVersionTable.PSVersion.Major -ge 6) {
        if ($IsWindows) {
            Write-Output 'windows'
            exit 0
        }

        if ($IsLinux -or $IsMacOS) {
            Write-Output 'unix'
            exit 0
        }
    }

    # Fallback for Windows PowerShell 5.1 (always runs on Windows)
    if ($PSVersionTable.PSVersion.Major -eq 5) {
        Write-Output 'windows'
        exit 0
    }

    # Check for common Windows environment variables
    if ($env:WINDIR -or $env:SYSTEMROOT) {
        Write-Output 'windows'
        exit 0
    }

    # Final fallback: Check OS using [System.Environment]
    $osVersion = [System.Environment]::OSVersion.Platform

    switch ($osVersion) {
        'Win32NT' {
            Write-Output 'windows'
            exit 0
        }
        'Unix' {
            Write-Output 'unix'
            exit 0
        }
        default {
            # Unknown platform, default to windows since we're running PowerShell
            Write-Output 'windows'
            exit 0
        }
    }
}
catch {
    Write-Error "Failed to detect platform: $_"
    exit 1
}
