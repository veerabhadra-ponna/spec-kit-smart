#!/usr/bin/env pwsh

#
# check-artifactory.ps1 - Query Artifactory for library availability
#
# Usage:
#   ./check-artifactory.ps1 <artifactory-url> <library-name> [api-key] [repos]
#   ./check-artifactory.ps1 -ArtifactoryUrl <url> -LibraryName <name> [-ApiKey <key>] [-Repos <repos>]
#
# Returns:
#   Exit 0: Library found (prints download URL)
#   Exit 1: Library not found
#   Exit 2: Authentication error
#   Exit 3: API error (network, timeout, etc.)
#   Exit 4: Artifactory URL not configured (skip check)
#

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false, Position=0)]
    [string]$ArtifactoryUrl = "",

    [Parameter(Mandatory=$false, Position=1)]
    [string]$LibraryName = "",

    [Parameter(Mandatory=$false, Position=2)]
    [string]$ApiKey = "",

    [Parameter(Mandatory=$false, Position=3)]
    [string]$Repos = "",

    [switch]$Help
)

$ErrorActionPreference = 'Stop'

# Use PowerShell's built-in debug mechanism
# When -Debug is passed, $DebugPreference is set to 'Continue'
# Also check DEBUG environment variable for compatibility
$IsDebugEnabled = ($DebugPreference -eq 'Continue') -or ($env:DEBUG -eq "true")

# Show help if requested
if ($Help) {
    Write-Output "Usage: $($MyInvocation.MyCommand.Name) <artifactory-url> <library-name> [api-key] [repos]"
    Write-Output "       $($MyInvocation.MyCommand.Name) -ArtifactoryUrl <url> -LibraryName <name> [-ApiKey <key>] [-Repos <repos>]"
    Write-Output ""
    Write-Output "Query Artifactory for library availability."
    Write-Output ""
    Write-Output "Parameters:"
    Write-Output "  ArtifactoryUrl    URL of the Artifactory instance"
    Write-Output "                    Examples:"
    Write-Output "                      - https://artifactory.company.com/artifactory"
    Write-Output "                      - https://artifactory.company.com"
    Write-Output "                    Note: Include /artifactory path if your installation requires it"
    Write-Output "  LibraryName       Name of the library to check (e.g., axios, lodash, jackson-databind)"
    Write-Output "  ApiKey           Optional API key/token for authentication (or set ARTIFACTORY_API_KEY env var)"
    Write-Output "                    Supports: Bearer tokens (recommended), API keys, Reference tokens"
    Write-Output "  Repos            Optional comma-separated list of repositories to search"
    Write-Output "                    Example: libs-release,libs-snapshot"
    Write-Output "                    If omitted, searches all repositories"
    Write-Output "  -Help            Show this help message"
    Write-Output "  -Debug           Enable verbose debug output"
    Write-Output ""
    Write-Output "Environment Variables:"
    Write-Output "  ARTIFACTORY_API_KEY  API key/token for authentication"
    Write-Output "  DEBUG                Set to 'true' to enable verbose debug output"
    Write-Output ""
    Write-Output "Exit Codes:"
    Write-Output "  0  Library found (prints download URL)"
    Write-Output "  1  Library not found (not whitelisted)"
    Write-Output "  2  Authentication error"
    Write-Output "  3  API error (network, timeout, etc.)"
    Write-Output "  4  Artifactory URL not configured (skip check)"
    Write-Output ""
    Write-Output "Examples:"
    Write-Output "  # Check if axios is available (all repositories)"
    Write-Output "  .\$($MyInvocation.MyCommand.Name) https://artifactory.company.com/artifactory axios"
    Write-Output ""
    Write-Output "  # Search in specific repositories"
    Write-Output "  .\$($MyInvocation.MyCommand.Name) https://artifactory.company.com/artifactory axios `"`" `"libs-release,npm-local`""
    Write-Output ""
    Write-Output "  # With Bearer token (recommended)"
    Write-Output "  .\$($MyInvocation.MyCommand.Name) https://artifactory.company.com/artifactory axios YOUR_BEARER_TOKEN"
    Write-Output ""
    Write-Output "  # Using named parameters"
    Write-Output "  .\$($MyInvocation.MyCommand.Name) -ArtifactoryUrl https://artifactory.company.com/artifactory -LibraryName axios"
    Write-Output ""
    Write-Output "  # Using environment variable for token"
    Write-Output "  `$env:ARTIFACTORY_API_KEY = `"YOUR_TOKEN`""
    Write-Output "  .\$($MyInvocation.MyCommand.Name) https://artifactory.company.com/artifactory axios"
    Write-Output ""
    Write-Output "  # With debug output"
    Write-Output "  .\$($MyInvocation.MyCommand.Name) -ArtifactoryUrl https://artifactory.company.com/artifactory -LibraryName axios -Debug"
    Write-Output ""
    Write-Output "  # Skip validation if URL not configured"
    Write-Output "  .\$($MyInvocation.MyCommand.Name) `"Not configured`" axios"
    Write-Output ""
    exit 0
}

# Get from environment if not provided
if ($ArtifactoryUrl -eq "" -and $env:ARTIFACTORY_URL) {
    $ArtifactoryUrl = $env:ARTIFACTORY_URL
}

if ($ApiKey -eq "" -and $env:ARTIFACTORY_API_KEY) {
    $ApiKey = $env:ARTIFACTORY_API_KEY
}

# Function to print status with color
function Print-Status {
    param(
        [string]$Status,
        [string]$Message
    )

    switch ($Status) {
        "FOUND" {
            Write-Host "[OK] FOUND: $Message" -ForegroundColor Green
        }
        "NOT_FOUND" {
            Write-Host "[X] NOT FOUND: $Message" -ForegroundColor Yellow
        }
        "SKIPPED" {
            Write-Host "[SKIP] SKIPPED: $Message" -ForegroundColor Yellow
        }
        "ERROR" {
            Write-Host "[WARNING] ERROR: $Message" -ForegroundColor Red
        }
    }
}

# Validate inputs
if ($LibraryName -eq "") {
    Write-Error "ERROR: Library name is required"
    Write-Error "Usage: $($MyInvocation.MyCommand.Name) <artifactory-url> <library-name> [api-key]"
    exit 3
}

# Check if Artifactory URL is configured
if ($ArtifactoryUrl -eq "" -or $ArtifactoryUrl -eq "Not configured" -or $ArtifactoryUrl -eq "null") {
    Print-Status "SKIPPED" "Artifactory URL not configured - skipping validation for $LibraryName"
    exit 4
}

# Normalize URL - remove trailing /api if present
$ArtifactoryUrl = $ArtifactoryUrl.TrimEnd('/api')
$ArtifactoryUrl = $ArtifactoryUrl.TrimEnd('/')

# Build API endpoint with optional repos parameter
if ($Repos -ne "") {
    $apiEndpoint = "${ArtifactoryUrl}/api/search/artifact?name=${LibraryName}&repos=${Repos}"
} else {
    $apiEndpoint = "${ArtifactoryUrl}/api/search/artifact?name=${LibraryName}"
}

# Debug output
if ($IsDebugEnabled) {
    Write-Host "DEBUG: Artifactory URL: $ArtifactoryUrl" -ForegroundColor Cyan
    Write-Host "DEBUG: Library Name: $LibraryName" -ForegroundColor Cyan
    Write-Host "DEBUG: Repositories: $(if ($Repos) { $Repos } else { 'all' })" -ForegroundColor Cyan
    Write-Host "DEBUG: API Endpoint: $apiEndpoint" -ForegroundColor Cyan
    Write-Host "DEBUG: Using Auth: $(if ($ApiKey) { 'yes' } else { 'no' })" -ForegroundColor Cyan
}

try {
    # Prepare headers with X-Result-Detail to get downloadUri directly
    $headers = @{
        "X-Result-Detail" = "info"
    }

    # Try Bearer token first (modern method, supports all token types)
    $usedBearerAuth = $false
    if ($ApiKey -ne "") {
        if ($IsDebugEnabled) {
            Write-Host "DEBUG: Attempting authentication with Bearer token..." -ForegroundColor Cyan
        }
        $headers["Authorization"] = "Bearer $ApiKey"
        $usedBearerAuth = $true
    }

    # Query Artifactory with timeout
    try {
        $response = Invoke-WebRequest -Uri $apiEndpoint `
            -Headers $headers `
            -TimeoutSec 5 `
            -UseBasicParsing `
            -ErrorAction Stop

        $httpCode = $response.StatusCode
        $body = $response.Content
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__

        # If Bearer auth failed with 401/403, try legacy X-JFrog-Art-Api header
        if ($usedBearerAuth -and ($statusCode -eq 401 -or $statusCode -eq 403)) {
            if ($IsDebugEnabled) {
                Write-Host "DEBUG: Bearer auth failed, trying legacy X-JFrog-Art-Api header..." -ForegroundColor Cyan
            }

            $headers.Remove("Authorization")
            $headers["X-JFrog-Art-Api"] = $ApiKey

            $response = Invoke-WebRequest -Uri $apiEndpoint `
                -Headers $headers `
                -TimeoutSec 5 `
                -UseBasicParsing `
                -ErrorAction Stop

            $httpCode = $response.StatusCode
            $body = $response.Content
        } else {
            throw
        }
    }

    # Debug output
    if ($IsDebugEnabled) {
        Write-Host "DEBUG: HTTP Code: $httpCode" -ForegroundColor Cyan
        Write-Host "DEBUG: Response Body: $body" -ForegroundColor Cyan
    }

    # Handle successful response
    if ($httpCode -eq 200) {
        try {
            $jsonBody = $body | ConvertFrom-Json
            $resultsCount = $jsonBody.results.Count

            if ($resultsCount -gt 0) {
                $downloadUri = $jsonBody.results[0].downloadUri

                # Try to extract version from URI
                $version = "latest"
                if ($downloadUri -match '([\d\.]+)\.(jar|tar\.gz|zip|whl)') {
                    $version = $matches[1]
                }

                if ($version -ne "latest") {
                    Print-Status "FOUND" "${LibraryName}:${version} available in Artifactory"
                } else {
                    Print-Status "FOUND" "$LibraryName available in Artifactory"
                }

                Write-Output $downloadUri
                exit 0
            } else {
                Print-Status "NOT_FOUND" "$LibraryName not found in Artifactory"
                exit 1
            }
        } catch {
            # Fallback without JSON parsing - simple check
            if ($body -match "downloadUri") {
                Print-Status "FOUND" "$LibraryName available in Artifactory"
                Write-Output $body
                exit 0
            } else {
                Print-Status "NOT_FOUND" "$LibraryName not found in Artifactory"
                exit 1
            }
        }
    }
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__

    if ($statusCode -eq 401) {
        Print-Status "ERROR" "Authentication failed (401 Unauthorized). Check your API key/token."
        Write-Host "  Hint: Ensure you're using a valid Bearer token or API key" -ForegroundColor Red
        Write-Host "  Set ARTIFACTORY_API_KEY environment variable or pass as 3rd argument" -ForegroundColor Red
        exit 2
    } elseif ($statusCode -eq 403) {
        Print-Status "ERROR" "Access forbidden (403 Forbidden). Check permissions for this repository."
        Write-Host "  Your credentials are valid but lack permission to access this resource" -ForegroundColor Red
        exit 2
    } elseif ($statusCode -eq 404) {
        Print-Status "ERROR" "API endpoint not found (404). Verify ARTIFACTORY_URL path is correct."
        Write-Host "  Expected format: https://artifactory.company.com/artifactory" -ForegroundColor Red
        Write-Host "  Some installations require /artifactory in the path, others don't" -ForegroundColor Red
        exit 3
    } elseif ($null -eq $statusCode -or $statusCode -eq 0) {
        Print-Status "ERROR" "Network error or timeout (Artifactory may be unreachable)"
        Write-Host "  Check network connectivity and Artifactory URL" -ForegroundColor Red
        exit 3
    } else {
        Print-Status "ERROR" "Artifactory API returned HTTP $statusCode"
        if ($IsDebugEnabled) {
            Write-Host "  Response: $body" -ForegroundColor Red
        }
        exit 3
    }
}
