#Requires -Version 5.1

<#
.SYNOPSIS
    Find reusable code from the codebase index

.DESCRIPTION
    Analyzes task description and searches for similar implementations,
    utilities, patterns, and test examples.

.PARAMETER Task
    The task description to search for

.PARAMETER Format
    Output format: 'text' (default) or 'json'

.PARAMETER Threshold
    Minimum similarity threshold (0-100, default: 60)

.EXAMPLE
    .\Find-ReusableCode.ps1 -Task "implement user authentication" -Format json

.NOTES
    Exit codes: 0=Success, 1=Index missing, 2=No matches
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Task,

    [ValidateSet('text', 'json')]
    [string]$Format = 'text',

    [ValidateRange(0, 100)]
    [int]$Threshold = 60
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-RepoRoot {
    try {
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($gitRoot) { return $gitRoot -replace '/', '\' }
    } catch {}
    return (Get-Location).Path
}

function Get-Keywords {
    param([string]$Text)

    $stopWords = @('the','a','an','is','are','was','were','be','been','being','have','has','had','do','does','did','will','would','could','should','may','might','must','shall','can','need','want','to','of','in','for','on','with','at','by','from','as','into','through','during','before','after','above','below','between','under','again','further','then','once','here','there','when','where','why','how','all','each','every','both','few','more','most','other','some','such','no','not','only','own','same','so','than','too','very','just','also','now','new','old','first','last','and','or','but','if','else','this','that','these','those','what','who','which')

    $words = $Text.ToLower() -split '[^a-z]+' | Where-Object { $_.Length -ge 3 -and $_ -notin $stopWords }
    return $words | Sort-Object -Unique
}

function Get-Similarity {
    param([string]$Text1, [string]$Text2)

    $words1 = Get-Keywords $Text1
    $words2 = Get-Keywords $Text2

    if ($words1.Count -eq 0 -or $words2.Count -eq 0) { return 0 }

    $common = ($words1 | Where-Object { $_ -in $words2 }).Count
    $union = $words1.Count + $words2.Count - $common

    if ($union -eq 0) { return 0 }
    return [int](($common / $union) * 100)
}

try {
    $repoRoot = Get-RepoRoot
    $indexDir = Join-Path (Join-Path $repoRoot '.analysis') 'index'

    if (-not (Test-Path $indexDir)) {
        if ($Format -eq 'json') {
            @{ error = "Index not found" } | ConvertTo-Json
        } else {
            Write-Error "Index not found. Run /speckitsmart.index first."
        }
        exit 1
    }

    $keywords = Get-Keywords $Task
    $similarImplementations = @()
    $utilities = @()
    $patterns = @()
    $testExamples = @()

    # Load structure
    $structurePath = Join-Path $indexDir 'structure.json'
    if (Test-Path $structurePath) {
        $structure = Get-Content $structurePath -Raw | ConvertFrom-Json

        # Search classes
        foreach ($class in $structure.classes) {
            foreach ($keyword in $keywords) {
                if ($class.name -match $keyword) {
                    $similarity = Get-Similarity $Task $class.name
                    if ($similarity -ge $Threshold) {
                        $similarImplementations += [PSCustomObject]@{
                            name = $class.name
                            file = $class.file
                            line = $class.line
                            similarity = $similarity
                            type = 'class'
                        }
                    }
                    break
                }
            }
        }

        # Search functions
        foreach ($func in $structure.functions) {
            # Check for utilities
            if ($func.file -match 'util|helper|common|shared|lib') {
                $utilities += [PSCustomObject]@{
                    name = $func.name
                    file = $func.file
                    line = $func.line
                    type = 'utility'
                }
            }

            foreach ($keyword in $keywords) {
                if ($func.name -match $keyword) {
                    $similarity = Get-Similarity $Task $func.name
                    $similarImplementations += [PSCustomObject]@{
                        name = $func.name
                        file = $func.file
                        line = $func.line
                        similarity = $similarity
                        type = 'function'
                    }
                    break
                }
            }
        }

        # Detect patterns
        if ($structure.classes | Where-Object { $_.name -match 'Service$' }) {
            $patterns += [PSCustomObject]@{
                pattern = 'Service Layer'
                description = 'Use *Service classes for business logic'
            }
        }
        if ($structure.classes | Where-Object { $_.name -match 'Controller$' }) {
            $patterns += [PSCustomObject]@{
                pattern = 'Controller Pattern'
                description = 'Use *Controller classes for request handling'
            }
        }
    }

    # Search for test examples
    $depsPath = Join-Path $indexDir 'dependencies.json'
    if (Test-Path $depsPath) {
        $deps = Get-Content $depsPath -Raw | ConvertFrom-Json
        $testFiles = $deps.files | Where-Object { $_.source_file -match 'test|spec' } |
            Select-Object -ExpandProperty source_file -Unique | Select-Object -First 5

        foreach ($tf in $testFiles) {
            $testExamples += [PSCustomObject]@{ file = $tf; type = 'test_example' }
        }
    }

    $totalResults = $similarImplementations.Count + $utilities.Count + $patterns.Count + $testExamples.Count

    if ($Format -eq 'json') {
        @{
            task = $Task
            summary = @{
                similar_implementations = $similarImplementations.Count
                utilities = $utilities.Count
                patterns = $patterns.Count
                test_examples = $testExamples.Count
            }
            results = @{
                similar = $similarImplementations
                utilities = $utilities
                patterns = $patterns
                tests = $testExamples
            }
        } | ConvertTo-Json -Depth 5
    } else {
        Write-Host ""
        Write-Host "Task: $Task"
        Write-Host "Keywords: $($keywords -join ', ')"
        Write-Host ""

        if ($totalResults -eq 0) {
            Write-Host "No reusable code suggestions found."
            exit 2
        }

        if ($similarImplementations.Count -gt 0) {
            Write-Host "=== Similar Implementations ===" -ForegroundColor Cyan
            foreach ($impl in $similarImplementations) {
                if ($impl.similarity -ge 90) {
                    Write-Host "  [HIGH MATCH] $($impl.name) ($($impl.type))" -ForegroundColor Green
                    Write-Host "    Similarity: $($impl.similarity)%"
                    Write-Host "    Location: $($impl.file):$($impl.line)"
                } else {
                    Write-Host "  $($impl.name) ($($impl.type)) - $($impl.similarity)% similar"
                    Write-Host "    Location: $($impl.file):$($impl.line)"
                }
            }
            Write-Host ""
        }

        if ($utilities.Count -gt 0) {
            Write-Host "=== Reusable Utilities ===" -ForegroundColor Cyan
            foreach ($util in $utilities) {
                Write-Host "  $($util.name)"
                Write-Host "    File: $($util.file)"
            }
            Write-Host ""
        }

        if ($patterns.Count -gt 0) {
            Write-Host "=== Architecture Patterns ===" -ForegroundColor Cyan
            foreach ($pattern in $patterns) {
                Write-Host "  $($pattern.pattern)"
                Write-Host "    $($pattern.description)"
            }
            Write-Host ""
        }

        if ($testExamples.Count -gt 0) {
            Write-Host "=== Test Examples ===" -ForegroundColor Cyan
            foreach ($test in $testExamples) {
                Write-Host "  $($test.file)"
            }
        }
    }

    exit 0
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
