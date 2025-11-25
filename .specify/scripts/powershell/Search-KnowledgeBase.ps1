#Requires -Version 5.1

<#
.SYNOPSIS
    Search codebase knowledge base

.DESCRIPTION
    Searches the index and DeepWiki documentation to answer questions.

.PARAMETER Query
    The search query

.PARAMETER Format
    Output format: 'text' (default) or 'json'

.PARAMETER Sources
    Search sources: 'all' (default), 'index', or 'wiki'

.EXAMPLE
    .\Search-KnowledgeBase.ps1 -Query "authentication" -Format json

.NOTES
    Exit codes: 0=Success, 1=Index missing, 2=No results
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Query,

    [ValidateSet('text', 'json')]
    [string]$Format = 'text',

    [ValidateSet('all', 'index', 'wiki')]
    [string]$Sources = 'all'
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

try {
    $repoRoot = Get-RepoRoot
    $indexDir = Join-Path (Join-Path $repoRoot '.analysis') 'index'
    $wikiDir = Join-Path $repoRoot '.deepwiki'

    if (-not (Test-Path $indexDir)) {
        if ($Format -eq 'json') {
            @{ error = "Index not found"; results = @() } | ConvertTo-Json
        } else {
            Write-Error "Index not found. Run /speckitsmart.index first."
        }
        exit 1
    }

    $queryLower = $Query.ToLower()
    $results = @()

    # Search index files
    if ($Sources -in @('all', 'index')) {
        $indexFiles = @(
            @{ file = 'structure.json'; category = 'code_structure' }
            @{ file = 'api-endpoints.json'; category = 'api_endpoints' }
            @{ file = 'data-models.json'; category = 'data_models' }
            @{ file = 'external-apis.json'; category = 'external_apis' }
            @{ file = 'dependencies.json'; category = 'dependencies' }
        )

        foreach ($idx in $indexFiles) {
            $filePath = Join-Path $indexDir $idx.file
            if (Test-Path $filePath) {
                $content = Get-Content $filePath -Raw | ConvertFrom-Json

                # Search through objects
                $searchProps = @('name', 'path', 'service', 'table', 'entity')
                foreach ($prop in $content.PSObject.Properties) {
                    if ($prop.Value -is [Array]) {
                        foreach ($item in $prop.Value) {
                            foreach ($sp in $searchProps) {
                                if ($item.$sp -and $item.$sp.ToLower().Contains($queryLower)) {
                                    $results += [PSCustomObject]@{
                                        type = $idx.category
                                        name = $item.$sp
                                        file = $item.file
                                        line = $item.line
                                        source = "index:$($idx.category)"
                                    }
                                    break
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Search wiki files
    if ($Sources -in @('all', 'wiki') -and (Test-Path $wikiDir)) {
        $wikiFiles = Get-ChildItem $wikiDir -Recurse -Filter "*.md"
        foreach ($wikiFile in $wikiFiles) {
            $content = Get-Content $wikiFile.FullName -Raw
            if ($content -match $Query) {
                $relPath = $wikiFile.FullName.Replace($wikiDir, '').TrimStart('\', '/')
                $context = ($content -split "`n" | Where-Object { $_ -match $Query } | Select-Object -First 3) -join "`n"
                $results += [PSCustomObject]@{
                    type = 'wiki'
                    name = $relPath
                    file = $relPath
                    context = $context
                    source = "wiki:$relPath"
                }
            }
        }
    }

    # Determine confidence
    $confidence = switch ($results.Count) {
        { $_ -ge 5 } { 'high' }
        { $_ -ge 2 } { 'medium' }
        { $_ -ge 1 } { 'low' }
        default { 'none' }
    }

    if ($Format -eq 'json') {
        @{
            query = $Query
            confidence = $confidence
            result_count = $results.Count
            results = $results
        } | ConvertTo-Json -Depth 5
    } else {
        Write-Host ""
        Write-Host "Query: $Query"
        Write-Host "Confidence: $confidence (based on $($results.Count) sources)"
        Write-Host ""

        if ($results.Count -eq 0) {
            Write-Host "No relevant results found."
            exit 2
        }

        Write-Host "Results:"
        Write-Host "--------"
        foreach ($result in $results) {
            Write-Host ""
            Write-Host "  [$($result.source)] $($result.name)"
            if ($result.file) {
                Write-Host "    Location: $($result.file):$($result.line)"
            }
        }
    }

    exit 0
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
