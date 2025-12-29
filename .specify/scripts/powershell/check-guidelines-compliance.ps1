<#
.SYNOPSIS
    Corporate Guidelines Compliance Checker (PowerShell)
    Part of Spec Kit Phase 4: Advanced Features

.DESCRIPTION
    Validates project compliance with corporate guidelines using profile-based architecture v3.0

.PARAMETER Strict
    Fail on HIGH severity violations (default: only CRITICAL)

.PARAMETER OutputFormat
    Output format: text (default), json, markdown

.EXAMPLE
    .\check-guidelines-compliance.ps1
    .\check-guidelines-compliance.ps1 -Strict
    .\check-guidelines-compliance.ps1 -OutputFormat json

.NOTES
    Exit codes:
      0 - No violations or only LOW/MEDIUM severity
      1 - HIGH severity violations found
      2 - CRITICAL violations found
      3 - Script error (missing guidelines, etc.)
#>

param(
    [switch]$Strict = $false,
    [ValidateSet('text', 'json', 'markdown')]
    [string]$OutputFormat = 'text'
)

# Configuration
$ProjectRoot = Get-Location
$GuidelinesDir = Join-Path $ProjectRoot ".guidelines"
$GuidelineProfile = ""

# Counters
$script:CriticalCount = 0
$script:HighCount = 0
$script:MediumCount = 0
$script:LowCount = 0

# Violation arrays
$script:CriticalViolations = @()
$script:HighViolations = @()
$script:MediumViolations = @()
$script:LowViolations = @()
$script:PassChecks = @()

#region Helper Functions

function Write-Header {
    param([string]$Message)
    Write-Host "`n$Message" -ForegroundColor White -BackgroundColor DarkBlue
    Write-Host ("=" * 80) -ForegroundColor Blue
}

function Write-Section {
    param([string]$Message)
    Write-Host "`n$Message" -ForegroundColor Cyan
    Write-Host ("-" * 80) -ForegroundColor DarkCyan
}

function Log-Pass {
    param([string]$Message)
    $script:PassChecks += "✅ PASS: $Message"
}

function Log-Critical {
    param([string]$Message)
    $script:CriticalCount++
    $script:CriticalViolations += "❌ CRITICAL: $Message"
}

function Log-High {
    param([string]$Message)
    $script:HighCount++
    $script:HighViolations += "❌ HIGH: $Message"
}

function Log-Medium {
    param([string]$Message)
    $script:MediumCount++
    $script:MediumViolations += "⚠️  MEDIUM: $Message"
}

function Log-Low {
    param([string]$Message)
    $script:LowCount++
    $script:LowViolations += "ℹ️  LOW: $Message"
}

#endregion

#region Profile Detection

function Get-GuidelineProfile {
    # Priority 1: Explicit configuration in .specify/config.json
    $configPath = Join-Path $ProjectRoot ".specify\config.json"
    if (Test-Path $configPath) {
        try {
            $config = Get-Content $configPath -Raw | ConvertFrom-Json
            if ($config.project.guidelineProfile) {
                return $config.project.guidelineProfile
            }
        }
        catch {
            # Ignore JSON parse errors
        }
    }

    # Priority 2: .guidelines-profile file marker
    $profileFile = Join-Path $ProjectRoot ".guidelines-profile"
    if (Test-Path $profileFile) {
        $profile = (Get-Content $profileFile -Raw).Trim()
        if ($profile) {
            return $profile
        }
    }

    # Priority 3: Detect from package.json
    $packageJson = Join-Path $ProjectRoot "package.json"
    if (Test-Path $packageJson) {
        try {
            $pkg = Get-Content $packageJson -Raw | ConvertFrom-Json
            # Check for corporate markers
            if ($pkg.private -eq $true) {
                return "corporate"
            }
            # Check for personal markers
            if ($pkg.license -match "MIT|Apache|GPL") {
                return "personal"
            }
        }
        catch {
            # Ignore JSON parse errors
        }
    }

    # Priority 4: Detect from filesystem markers
    if ((Test-Path ".corporate") -or (Test-Path "CORPORATE_LICENSE") -or (Test-Path "organization.json")) {
        return "corporate"
    }
    if ((Test-Path ".opensource") -or (Test-Path "MIT_LICENSE") -or (Test-Path "CONTRIBUTING.md")) {
        return "personal"
    }

    # Fallback to personal (more permissive)
    return "personal"
}

#endregion

#region Tech Stack Detection

function Get-TechStacks {
    $stacks = @()

    # Check for React
    if (Test-Path "package.json") {
        $pkg = Get-Content "package.json" -Raw | ConvertFrom-Json
        if ($pkg.dependencies.react) {
            $stacks += "reactjs"
        }
        elseif ($pkg.dependencies.express -or $pkg.dependencies.fastify) {
            $stacks += "nodejs"
        }
        else {
            $stacks += "nodejs"
        }
    }

    # Check for Java
    if ((Test-Path "pom.xml") -or (Test-Path "build.gradle")) {
        $stacks += "java"
    }

    # Check for .NET
    if ((Get-ChildItem -Filter "*.csproj" -ErrorAction SilentlyContinue) -or
        (Get-ChildItem -Filter "*.sln" -ErrorAction SilentlyContinue)) {
        $stacks += "dotnet"
    }

    # Check for Python
    if ((Test-Path "requirements.txt") -or (Test-Path "pyproject.toml") -or (Test-Path "setup.py")) {
        $stacks += "python"
    }

    # Check for Go
    if (Test-Path "go.mod") {
        $stacks += "go"
    }

    return $stacks
}

#endregion

#region Guideline Loading

function Get-GuidelineFiles {
    param([string]$Stack)

    $profile = $script:GuidelineProfile
    if (-not $profile) { $profile = "personal" }

    # Profile-based architecture v3.0
    $baseGuideline = Join-Path $GuidelinesDir "base\$Stack-base.md"
    $profileOverride = Join-Path $GuidelinesDir "profiles\$profile\$Stack-overrides.md"
    $legacyGuideline = Join-Path $GuidelinesDir "$Stack-guidelines.md"

    $files = @()

    # Check for new profile-based architecture
    if (Test-Path $baseGuideline) {
        $files += $baseGuideline
        if (Test-Path $profileOverride) {
            $files += $profileOverride
        }
        return $files
    }

    # Fallback to legacy single-file guideline
    if (Test-Path $legacyGuideline) {
        $files += $legacyGuideline
        return $files
    }

    return $null
}

#endregion

#region Compliance Checks

function Test-PackageRegistry {
    param([string]$Stack, [string[]]$GuidelineFiles)

    Write-Section "Checking Package Registry Configuration"

    switch ($Stack) {
        "reactjs" {
            if (Test-Path ".npmrc") {
                Log-Pass "Found .npmrc configuration"
            }
            else {
                Log-Medium ".npmrc file missing (recommended for package registry configuration)"
            }
        }
        "nodejs" {
            if (Test-Path ".npmrc") {
                Log-Pass "Found .npmrc configuration"
            }
            else {
                Log-Medium ".npmrc file missing (recommended for package registry configuration)"
            }
        }
        "java" {
            if (Test-Path "settings.xml") {
                Log-Pass "Found Maven settings.xml"
            }
            else {
                Log-Low "Maven settings.xml not found (may be in user directory)"
            }
        }
        "python" {
            if ((Test-Path "pip.conf") -or (Test-Path ".pypirc")) {
                Log-Pass "Found Python package registry configuration"
            }
            else {
                Log-Low "pip.conf or .pypirc not found"
            }
        }
        "dotnet" {
            if (Test-Path "nuget.config") {
                Log-Pass "Found NuGet configuration"
            }
            else {
                Log-Low "nuget.config not found (may be using global config)"
            }
        }
    }
}

function Test-SecurityRequirements {
    param([string]$Stack)

    Write-Section "Checking Security Requirements"

    # Check for .env in .gitignore
    if (Test-Path ".gitignore") {
        $gitignore = Get-Content ".gitignore" -Raw
        if ($gitignore -match "\.env") {
            Log-Pass ".env files are gitignored"
        }
        else {
            Log-High ".env not in .gitignore - secrets may be exposed"
        }
    }
    else {
        Log-Medium ".gitignore file missing"
    }

    # Check for hardcoded secrets (basic check)
    $suspiciousPatterns = @(
        "password\s*=\s*['""][^'""]+['""]",
        "api[_-]?key\s*=\s*['""][^'""]+['""]",
        "secret\s*=\s*['""][^'""]+['""]"
    )

    $foundSecrets = $false
    Get-ChildItem -Recurse -File -Include *.js, *.ts, *.java, *.py, *.cs -ErrorAction SilentlyContinue | ForEach-Object {
        $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
        foreach ($pattern in $suspiciousPatterns) {
            if ($content -match $pattern) {
                Log-Critical "Potential hardcoded secret found in $($_.Name)"
                $foundSecrets = $true
                break
            }
        }
    }

    if (-not $foundSecrets) {
        Log-Pass "No obvious hardcoded secrets detected"
    }
}

#endregion

#region Report Generation

function Show-TextReport {
    Write-Header "📋 Guideline Compliance Report"

    Write-Host "`n🎯 Profile: " -NoNewline
    Write-Host $script:GuidelineProfile -ForegroundColor Cyan

    Write-Host "`n📊 Summary:" -ForegroundColor White
    Write-Host "  ✅ Passed: $($script:PassChecks.Count)" -ForegroundColor Green
    Write-Host "  ℹ️  Low: $script:LowCount" -ForegroundColor Gray
    Write-Host "  ⚠️  Medium: $script:MediumCount" -ForegroundColor Yellow
    Write-Host "  ❌ High: $script:HighCount" -ForegroundColor DarkYellow
    Write-Host "  ❌ Critical: $script:CriticalCount" -ForegroundColor Red

    if ($script:PassChecks.Count -gt 0) {
        Write-Host "`n✅ Passed Checks:" -ForegroundColor Green
        $script:PassChecks | ForEach-Object { Write-Host "  $_" -ForegroundColor Green }
    }

    if ($script:LowViolations.Count -gt 0) {
        Write-Host "`nℹ️  Low Severity:" -ForegroundColor Gray
        $script:LowViolations | ForEach-Object { Write-Host "  $_" }
    }

    if ($script:MediumViolations.Count -gt 0) {
        Write-Host "`n⚠️  Medium Severity:" -ForegroundColor Yellow
        $script:MediumViolations | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow }
    }

    if ($script:HighViolations.Count -gt 0) {
        Write-Host "`n❌ High Severity:" -ForegroundColor DarkYellow
        $script:HighViolations | ForEach-Object { Write-Host "  $_" -ForegroundColor DarkYellow }
    }

    if ($script:CriticalViolations.Count -gt 0) {
        Write-Host "`n❌ Critical Severity:" -ForegroundColor Red
        $script:CriticalViolations | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
    }

    Write-Host "`n" -NoNewline
}

function Show-JsonReport {
    $report = @{
        profile           = $script:GuidelineProfile
        summary           = @{
            passed   = $script:PassChecks.Count
            low      = $script:LowCount
            medium   = $script:MediumCount
            high     = $script:HighCount
            critical = $script:CriticalCount
        }
        passed            = $script:PassChecks
        violations        = @{
            low      = $script:LowViolations
            medium   = $script:MediumViolations
            high     = $script:HighViolations
            critical = $script:CriticalViolations
        }
    }

    $report | ConvertTo-Json -Depth 10
}

#endregion

#region Main Execution

try {
    # Validate guidelines directory
    if (-not (Test-Path $GuidelinesDir)) {
        Write-Warning "No .guidelines directory found at $GuidelinesDir"
        Write-Host "Guidelines are optional. If you want guideline compliance checking,"
        Write-Host "create a .guidelines directory with tech stack guidelines."
        exit 3
    }

    # Detect guideline profile
    $script:GuidelineProfile = Get-GuidelineProfile
    Write-Host "🎯 Detected guideline profile: " -NoNewline -ForegroundColor Cyan
    Write-Host $script:GuidelineProfile -ForegroundColor White

    # Detect tech stacks
    $stacks = Get-TechStacks

    if ($stacks.Count -eq 0) {
        Write-Warning "No tech stack detected"
        Write-Host "Could not detect any supported tech stacks (React, Java, .NET, Python, Node.js, Go)."
        exit 3
    }

    Write-Host "📦 Detected stacks: " -NoNewline -ForegroundColor Cyan
    Write-Host ($stacks -join ", ") -ForegroundColor White

    # Run compliance checks for each stack
    foreach ($stack in $stacks) {
        $guidelineFiles = Get-GuidelineFiles -Stack $stack

        if ($guidelineFiles) {
            Write-Header "Checking $stack Guidelines"
            Test-PackageRegistry -Stack $stack -GuidelineFiles $guidelineFiles
            Test-SecurityRequirements -Stack $stack
        }
        else {
            Log-Low "No guidelines found for $stack"
        }
    }

    # Generate report
    if ($OutputFormat -eq "json") {
        Show-JsonReport
    }
    else {
        Show-TextReport
    }

    # Determine exit code
    if ($script:CriticalCount -gt 0) {
        exit 2
    }
    elseif ($Strict -and $script:HighCount -gt 0) {
        exit 1
    }
    else {
        exit 0
    }
}
catch {
    Write-Error "Script error: $_"
    exit 3
}

#endregion
