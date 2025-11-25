#Requires -Version 5.1

<#
.SYNOPSIS
    Load pre-extracted index data for analyze-project

.DESCRIPTION
    This script loads data from the codebase index to accelerate analysis:
    - Code structure (classes, functions, interfaces)
    - Data models (database schemas, ORM entities)
    - API endpoints (REST, GraphQL, WebSocket)
    - External integrations (third-party services, env vars)
    - Dependency graph (imports, exports)

.PARAMETER Format
    Output format: 'json' (default) or 'summary'

.PARAMETER Section
    Which section to load: 'all' (default), 'structure', 'data-models', 'api-endpoints', 'external-apis', 'dependencies'

.EXAMPLE
    .\Load-IndexForAnalysis.ps1 -Format json -Section all

.EXAMPLE
    .\Load-IndexForAnalysis.ps1 -Format summary

.NOTES
    Exit codes:
      0 - Success
      1 - Index not found or invalid
      2 - Invalid arguments
#>

[CmdletBinding()]
param(
    [ValidateSet('json', 'summary')]
    [string]$Format = 'json',

    [ValidateSet('all', 'structure', 'data-models', 'api-endpoints', 'external-apis', 'dependencies')]
    [string]$Section = 'all'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Helper functions
function Get-RepoRoot {
    try {
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($gitRoot) {
            return $gitRoot -replace '/', '\'
        }
    }
    catch {
        # Git not available
    }
    return (Get-Location).Path
}

function Load-JsonFile {
    param([string]$Path, [PSCustomObject]$Default)

    if (Test-Path $Path) {
        try {
            return Get-Content $Path -Raw | ConvertFrom-Json
        }
        catch {
            return $Default
        }
    }
    return $Default
}

try {
    $repoRoot = Get-RepoRoot
    $indexDir = Join-Path (Join-Path $repoRoot '.analysis') 'index'

    # Check if index exists
    if (-not (Test-Path $indexDir)) {
        Write-Error "Index not found. Run /speckitsmart.index first."
        exit 1
    }

    $metadataPath = Join-Path $indexDir 'metadata.json'
    if (-not (Test-Path $metadataPath)) {
        Write-Error "Index metadata missing. Run /speckitsmart.index --full to rebuild."
        exit 1
    }

    # Define default objects
    $defaultStructure = [PSCustomObject]@{
        classes    = @()
        functions  = @()
        interfaces = @()
    }

    $defaultDataModels = [PSCustomObject]@{
        database_schemas  = @()
        orm_entities      = @()
        type_definitions  = @()
    }

    $defaultApiEndpoints = [PSCustomObject]@{
        rest_endpoints      = @()
        graphql_resolvers   = @()
        websocket_handlers  = @()
    }

    $defaultExternalApis = [PSCustomObject]@{
        third_party_services  = @()
        environment_variables = @()
    }

    $defaultDependencies = [PSCustomObject]@{
        files = @()
    }

    # Load index data
    $metadata = Load-JsonFile (Join-Path $indexDir 'metadata.json') $null
    $structure = Load-JsonFile (Join-Path $indexDir 'structure.json') $defaultStructure
    $dataModels = Load-JsonFile (Join-Path $indexDir 'data-models.json') $defaultDataModels
    $apiEndpoints = Load-JsonFile (Join-Path $indexDir 'api-endpoints.json') $defaultApiEndpoints
    $externalApis = Load-JsonFile (Join-Path $indexDir 'external-apis.json') $defaultExternalApis
    $dependencies = Load-JsonFile (Join-Path $indexDir 'dependencies.json') $defaultDependencies

    if ($Format -eq 'summary') {
        # Generate summary output
        Write-Host "=== Codebase Index Summary ==="
        Write-Host "Generated: $($metadata.freshness)"
        Write-Host "Type: $($metadata.index_type)"
        Write-Host ""
        Write-Host "=== Statistics ==="
        Write-Host "Files indexed: $($metadata.statistics.indexed_files)"
        Write-Host "Classes: $($metadata.statistics.total_classes)"
        Write-Host "Functions: $($metadata.statistics.total_functions)"
        Write-Host "Interfaces: $($metadata.statistics.total_interfaces)"
        Write-Host "REST endpoints: $($metadata.statistics.total_rest_endpoints)"
        Write-Host "GraphQL resolvers: $($metadata.statistics.total_graphql_resolvers)"
        Write-Host "WebSocket handlers: $($metadata.statistics.total_websocket_handlers)"
        Write-Host "External APIs: $($metadata.statistics.total_external_apis)"
        Write-Host "Environment variables: $($metadata.statistics.total_env_vars)"
        Write-Host "Dependencies: $($metadata.statistics.total_dependencies)"
        Write-Host "Database schemas: $($metadata.statistics.total_database_schemas)"
        Write-Host "ORM entities: $($metadata.statistics.total_orm_entities)"
        Write-Host ""

        if ($Section -in @('all', 'structure')) {
            Write-Host "=== Code Structure ==="
            Write-Host "Classes:"
            foreach ($class in $structure.classes) {
                Write-Host "  - $($class.name) ($($class.file):$($class.line))"
            }
            if ($structure.classes.Count -eq 0) { Write-Host "  (none)" }

            Write-Host "Functions:"
            foreach ($func in $structure.functions) {
                Write-Host "  - $($func.name) ($($func.file):$($func.line))"
            }
            if ($structure.functions.Count -eq 0) { Write-Host "  (none)" }

            Write-Host "Interfaces:"
            foreach ($iface in $structure.interfaces) {
                Write-Host "  - $($iface.name) ($($iface.file):$($iface.line))"
            }
            if ($structure.interfaces.Count -eq 0) { Write-Host "  (none)" }
            Write-Host ""
        }

        if ($Section -in @('all', 'api-endpoints')) {
            Write-Host "=== API Endpoints ==="
            Write-Host "REST:"
            foreach ($endpoint in $apiEndpoints.rest_endpoints) {
                Write-Host "  - [$($endpoint.method)] $($endpoint.path) ($($endpoint.file):$($endpoint.line))"
            }
            if ($apiEndpoints.rest_endpoints.Count -eq 0) { Write-Host "  (none)" }

            Write-Host "GraphQL:"
            foreach ($resolver in $apiEndpoints.graphql_resolvers) {
                Write-Host "  - $($resolver.type) ($($resolver.file):$($resolver.line))"
            }
            if ($apiEndpoints.graphql_resolvers.Count -eq 0) { Write-Host "  (none)" }

            Write-Host "WebSocket:"
            foreach ($handler in $apiEndpoints.websocket_handlers) {
                Write-Host "  - $($handler.event) ($($handler.file):$($handler.line))"
            }
            if ($apiEndpoints.websocket_handlers.Count -eq 0) { Write-Host "  (none)" }
            Write-Host ""
        }

        if ($Section -in @('all', 'external-apis')) {
            Write-Host "=== External Integrations ==="
            Write-Host "Third-party services:"
            foreach ($service in $externalApis.third_party_services) {
                Write-Host "  - $($service.service) ($($service.file):$($service.line))"
            }
            if ($externalApis.third_party_services.Count -eq 0) { Write-Host "  (none)" }

            Write-Host "Environment variables:"
            foreach ($envVar in $externalApis.environment_variables) {
                Write-Host "  - $($envVar.name) ($($envVar.file):$($envVar.line))"
            }
            if ($externalApis.environment_variables.Count -eq 0) { Write-Host "  (none)" }
            Write-Host ""
        }

        if ($Section -in @('all', 'data-models')) {
            Write-Host "=== Data Models ==="
            Write-Host "Database schemas:"
            foreach ($schema in $dataModels.database_schemas) {
                Write-Host "  - $($schema.table) ($($schema.file):$($schema.line))"
            }
            if ($dataModels.database_schemas.Count -eq 0) { Write-Host "  (none)" }

            Write-Host "ORM entities:"
            foreach ($entity in $dataModels.orm_entities) {
                Write-Host "  - $($entity.entity) -> $($entity.table) ($($entity.file):$($entity.line))"
            }
            if ($dataModels.orm_entities.Count -eq 0) { Write-Host "  (none)" }
            Write-Host ""
        }
    }
    else {
        # Generate JSON output
        $output = switch ($Section) {
            'all' {
                [PSCustomObject]@{
                    metadata       = $metadata
                    structure      = $structure
                    data_models    = $dataModels
                    api_endpoints  = $apiEndpoints
                    external_apis  = $externalApis
                    dependencies   = $dependencies
                }
            }
            'structure' { $structure }
            'data-models' { $dataModels }
            'api-endpoints' { $apiEndpoints }
            'external-apis' { $externalApis }
            'dependencies' { $dependencies }
        }

        $output | ConvertTo-Json -Depth 10
    }

    exit 0
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
