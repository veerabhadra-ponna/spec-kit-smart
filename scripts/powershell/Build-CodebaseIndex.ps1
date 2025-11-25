#Requires -Version 5.1

<#
.SYNOPSIS
    Build searchable codebase index

.DESCRIPTION
    Scans codebase and creates JSON index files containing:
    - Code structure (classes, functions, interfaces)
    - Data models (database schemas, ORM entities)
    - API endpoints (REST, GraphQL, WebSocket)
    - External integrations (third-party services)

.PARAMETER Full
    Force full rebuild

.PARAMETER Incremental
    Update only changed files

.PARAMETER Path
    Index specific directory

.PARAMETER Languages
    Comma-separated list of languages to index (ts,js,py,java,cs,go)

.PARAMETER Verbose
    Show detailed progress

.PARAMETER Json
    Output results as JSON

.EXAMPLE
    & scripts\powershell\Build-CodebaseIndex.ps1 -Full -Verbose

.EXAMPLE
    & scripts\powershell\Build-CodebaseIndex.ps1 -Incremental -Path src\services

.NOTES
    Exit codes:
      0 - Success
      1 - General error
      2 - Dependency missing (jq)
#>

[CmdletBinding()]
param(
    [switch]$Full,
    [switch]$Incremental,
    [string]$Path,
    [string]$Languages = "ts,tsx,js,jsx,py,java,cs,go",
    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Helper functions
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    if ($VerbosePreference -eq 'Continue' -or $Level -ne "INFO") {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $(
            switch ($Level) {
                "ERROR" { "Red" }
                "WARN" { "Yellow" }
                default { "Gray" }
            }
        )
    }
}

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

# Check dependencies (jq is optional for PowerShell version - we use ConvertTo-Json)
# Kept for bash script parity documentation only

try {
    $repoRoot = Get-RepoRoot
    $indexDir = Join-Path (Join-Path $repoRoot '.analysis') 'index'
    $cacheDir = Join-Path $indexDir 'cache'

    # Determine mode
    $mode = "auto"
    if ($Full) { $mode = "full" }
    elseif ($Incremental) { $mode = "incremental" }

    if ($mode -eq "auto") {
        if (Test-Path (Join-Path $indexDir 'metadata.json')) {
            $mode = "full"
            Write-Log "No mode specified, defaulting to full rebuild"
        }
        else {
            $mode = "full"
            Write-Log "No existing index found, running full build"
        }
    }

    # Check for incremental with no base
    if ($mode -eq "incremental" -and -not (Test-Path (Join-Path $indexDir 'metadata.json'))) {
        Write-Log "No existing index found. Running full index build instead of incremental update." "WARN"
        $mode = "full"
    }

    # Determine target path
    $targetPath = if ($Path) { $Path } else { $repoRoot }

    # Create directories
    New-Item -ItemType Directory -Force -Path $indexDir | Out-Null
    New-Item -ItemType Directory -Force -Path $cacheDir | Out-Null

    $startTime = Get-Date
    $currentTimestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

    Write-Log "Starting codebase index build ($mode mode)"
    Write-Log "Target path: $targetPath"

    # Initialize counters
    $totalFiles = 0
    $indexedFiles = 0
    $skippedFiles = 0
    $totalClasses = 0
    $totalFunctions = 0
    $totalInterfaces = 0
    $totalRestEndpoints = 0
    $totalGraphQLResolvers = 0
    $totalWebSocketHandlers = 0
    $totalExternalApis = 0
    $totalEnvVars = 0
    $totalDependencies = 0

    # Initialize arrays
    $classes = @()
    $functions = @()
    $interfaces = @()
    $restEndpoints = @()
    $graphqlResolvers = @()
    $websocketHandlers = @()
    $externalApis = @()
    $envVars = @()
    $dependencies = @()

    # Build file patterns
    $includePatterns = @()
    foreach ($lang in $Languages -split ',') {
        switch ($lang.Trim()) {
            { $_ -in @('ts', 'tsx') } { $includePatterns += '*.ts', '*.tsx' }
            { $_ -in @('js', 'jsx') } { $includePatterns += '*.js', '*.jsx' }
            'py' { $includePatterns += '*.py' }
            'java' { $includePatterns += '*.java' }
            'cs' { $includePatterns += '*.cs' }
            'go' { $includePatterns += '*.go' }
        }
    }

    $excludePaths = @(
        'node_modules',
        'dist',
        'build',
        '.analysis',
        '.git',
        'vendor',
        'venv',
        '__pycache__'
    )

    # Scan for files
    Write-Log "Scanning for source files..."
    $files = Get-ChildItem -Path $targetPath -Recurse -File -Include $includePatterns |
        Where-Object {
            $exclude = $false
            foreach ($excludePath in $excludePaths) {
                if ($_.FullName -like "*\$excludePath\*") {
                    $exclude = $true
                    break
                }
            }
            -not $exclude
        }

    $totalFiles = $files.Count
    Write-Log "Found $totalFiles files to process"

    # Process each file
    foreach ($file in $files) {
        $indexedFiles++
        $relPath = $file.FullName.Substring($repoRoot.Length + 1) -replace '\\', '/'

        Write-Log "Processing: $relPath"

        # Check file size
        if ($file.Length -gt 10485760) {
            Write-Log "Skipping large file (>10MB): $relPath" "WARN"
            $skippedFiles++
            continue
        }

        try {
            $content = Get-Content $file.FullName -Raw -ErrorAction Stop

            # Extract classes
            $classRegex = [regex]::new('^\s*(export\s+)?class\s+([A-Za-z0-9_]+)', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $classMatches = $classRegex.Matches($content)
            foreach ($match in $classMatches) {
                $className = $match.Groups[2].Value
                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count

                $classes += [PSCustomObject]@{
                    name    = $className
                    file    = $relPath
                    line    = $lineNum
                    methods = @()
                }
                $totalClasses++
            }

            # Extract functions
            $funcRegex = [regex]::new('^\s*(export\s+)?function\s+([A-Za-z0-9_]+)', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $funcMatches = $funcRegex.Matches($content)
            foreach ($match in $funcMatches) {
                $funcName = $match.Groups[2].Value
                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count

                $functions += [PSCustomObject]@{
                    name       = $funcName
                    file       = $relPath
                    line       = $lineNum
                    parameters = @()
                }
                $totalFunctions++
            }

            # Extract interfaces (TypeScript)
            if ($file.Extension -in @('.ts', '.tsx')) {
                $interfaceRegex = [regex]::new('^\s*(export\s+)?interface\s+([A-Za-z0-9_]+)', [System.Text.RegularExpressions.RegexOptions]::Multiline)
                $interfaceMatches = $interfaceRegex.Matches($content)
                foreach ($match in $interfaceMatches) {
                    $interfaceName = $match.Groups[2].Value
                    $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count

                    $interfaces += [PSCustomObject]@{
                        name   = $interfaceName
                        file   = $relPath
                        line   = $lineNum
                        fields = @()
                    }
                    $totalInterfaces++
                }
            }

            # Extract REST API endpoints (Express.js, FastAPI style)
            $restRegex = [regex]::new('(?:router|app)\.(get|post|put|patch|delete|all)\([''"]([^''"]+)[''"]', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $restMatches = $restRegex.Matches($content)
            foreach ($match in $restMatches) {
                $method = $match.Groups[1].Value.ToUpper()
                $path = $match.Groups[2].Value
                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count

                $restEndpoints += [PSCustomObject]@{
                    method = $method
                    path   = $path
                    file   = $relPath
                    line   = $lineNum
                }
                $totalRestEndpoints++
            }

            # Extract GraphQL resolvers
            $graphqlRegex = [regex]::new('(?:Query|Mutation|Subscription)\s*:\s*\{', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $graphqlMatches = $graphqlRegex.Matches($content)
            foreach ($match in $graphqlMatches) {
                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                $graphqlResolvers += [PSCustomObject]@{
                    type = $match.Value -replace '\s*:\s*\{', ''
                    file = $relPath
                    line = $lineNum
                }
                $totalGraphQLResolvers++
            }

            # Extract WebSocket handlers
            $wsRegex = [regex]::new('\.on\([''"](?:connection|message|disconnect|error)[''"]', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $wsMatches = $wsRegex.Matches($content)
            foreach ($match in $wsMatches) {
                $event = $match.Value -replace '\.on\([''"]|[''"]', ''
                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                $websocketHandlers += [PSCustomObject]@{
                    event = $event
                    file  = $relPath
                    line  = $lineNum
                }
                $totalWebSocketHandlers++
            }

            # Extract third-party API integrations (known SDKs)
            $apiRegex = [regex]::new('(?:import|require).*?from\s+[''"]([^''"]+)[''"]', [System.Text.RegularExpressions.RegexOptions]::Multiline -bor [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
            $knownServices = @('stripe', 'aws-sdk', '@aws-sdk', 'firebase', '@google-cloud', 'sendgrid', 'twilio', 'mailgun', 'pusher', 'socket.io-client', 'axios', 'node-fetch', 'got', 'request', 'superagent')
            $apiMatches = $apiRegex.Matches($content)
            foreach ($match in $apiMatches) {
                $service = $match.Groups[1].Value
                $isKnownService = $false
                foreach ($known in $knownServices) {
                    if ($service -eq $known -or $service.StartsWith("$known/")) {
                        $isKnownService = $true
                        break
                    }
                }
                if ($isKnownService) {
                    $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                    if ($service -match '@') { $service = $service -replace '@.*/', '' }
                    $service = $service.Split('/')[0]

                    $externalApis += [PSCustomObject]@{
                        service = $service
                        file    = $relPath
                        line    = $lineNum
                    }
                    $totalExternalApis++
                }
            }

            # Extract environment variables (API keys, secrets, configs)
            $envRegex = [regex]::new('process\.env\.([A-Z_][A-Z0-9_]*)', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $envMatches = $envRegex.Matches($content)
            $seenEnvVars = @{}
            foreach ($match in $envMatches) {
                $envVar = $match.Groups[1].Value
                # Skip if already seen in this file
                if ($seenEnvVars.ContainsKey($envVar)) { continue }
                $seenEnvVars[$envVar] = $true

                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                $envVars += [PSCustomObject]@{
                    name = $envVar
                    file = $relPath
                    line = $lineNum
                }
                $totalEnvVars++
            }

            # Extract dependencies (imports and requires)
            # Track unique dependencies per file to avoid duplicates
            $seenImports = @{}

            # Extract ES6 imports: import ... from '...'
            $importRegex = [regex]::new('import\s+.*from\s+[''"]([^''"]+)[''"]', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $importMatches = $importRegex.Matches($content)
            foreach ($match in $importMatches) {
                $importedFrom = $match.Groups[1].Value
                # Skip if already seen in this file
                if ($seenImports.ContainsKey($importedFrom)) { continue }
                $seenImports[$importedFrom] = $true

                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                $dependencies += [PSCustomObject]@{
                    source_file  = $relPath
                    imported_from = $importedFrom
                    line         = $lineNum
                    import_type  = "es6_import"
                }
                $totalDependencies++
            }

            # Extract CommonJS requires: require('...')
            $requireRegex = [regex]::new('require\([''"]([^''"]+)[''"]\)', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $requireMatches = $requireRegex.Matches($content)
            foreach ($match in $requireMatches) {
                $importedFrom = $match.Groups[1].Value
                # Skip if already seen in this file
                if ($seenImports.ContainsKey($importedFrom)) { continue }
                $seenImports[$importedFrom] = $true

                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                $dependencies += [PSCustomObject]@{
                    source_file  = $relPath
                    imported_from = $importedFrom
                    line         = $lineNum
                    import_type  = "commonjs_require"
                }
                $totalDependencies++
            }

            # Extract dynamic imports: import('...')
            $dynamicImportRegex = [regex]::new('import\([''"]([^''"]+)[''"]\)', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $dynamicImportMatches = $dynamicImportRegex.Matches($content)
            foreach ($match in $dynamicImportMatches) {
                $importedFrom = $match.Groups[1].Value
                # Skip if already seen in this file
                if ($seenImports.ContainsKey($importedFrom)) { continue }
                $seenImports[$importedFrom] = $true

                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                $dependencies += [PSCustomObject]@{
                    source_file  = $relPath
                    imported_from = $importedFrom
                    line         = $lineNum
                    import_type  = "dynamic_import"
                }
                $totalDependencies++
            }

            # Extract re-exports: export ... from '...'
            $reexportRegex = [regex]::new('export\s+.*from\s+[''"]([^''"]+)[''"]', [System.Text.RegularExpressions.RegexOptions]::Multiline)
            $reexportMatches = $reexportRegex.Matches($content)
            foreach ($match in $reexportMatches) {
                $importedFrom = $match.Groups[1].Value
                # Skip if already seen in this file
                if ($seenImports.ContainsKey($importedFrom)) { continue }
                $seenImports[$importedFrom] = $true

                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                $dependencies += [PSCustomObject]@{
                    source_file  = $relPath
                    imported_from = $importedFrom
                    line         = $lineNum
                    import_type  = "re_export"
                }
                $totalDependencies++
            }
        }
        catch {
            Write-Log "Failed to process file $relPath`: $($_.Exception.Message)" "WARN"
            $skippedFiles++
        }
    }

    # Calculate duration
    $endTime = Get-Date
    $duration = [int]($endTime - $startTime).TotalSeconds

    Write-Log "Index build completed in $duration seconds"

    # Write structure.json
    $structureJson = @{
        version    = "1.0"
        timestamp  = $currentTimestamp
        classes    = $classes
        functions  = $functions
        interfaces = $interfaces
    } | ConvertTo-Json -Depth 10

    $structureJson | Out-File -FilePath (Join-Path $indexDir 'structure.json') -Encoding UTF8

    # Write metadata.json
    $metadataJson = @{
        version            = "1.0"
        created_by_version = "1.0.0"
        generated_at       = $currentTimestamp
        freshness          = $currentTimestamp
        index_type         = $mode
        duration_seconds   = $duration
        statistics         = @{
            total_files             = $totalFiles
            indexed_files           = $indexedFiles
            skipped_files           = $skippedFiles
            total_classes           = $totalClasses
            total_functions         = $totalFunctions
            total_interfaces        = $totalInterfaces
            total_rest_endpoints    = $totalRestEndpoints
            total_graphql_resolvers = $totalGraphQLResolvers
            total_websocket_handlers = $totalWebSocketHandlers
            total_external_apis     = $totalExternalApis
            total_env_vars          = $totalEnvVars
            total_dependencies      = $totalDependencies
        }
    } | ConvertTo-Json -Depth 10

    $metadataJson | Out-File -FilePath (Join-Path $indexDir 'metadata.json') -Encoding UTF8

    # Write api-endpoints.json
    $apiEndpointsJson = @{
        version             = "1.0"
        timestamp           = $currentTimestamp
        rest_endpoints      = $restEndpoints
        graphql_resolvers   = $graphqlResolvers
        websocket_handlers  = $websocketHandlers
    } | ConvertTo-Json -Depth 10

    $apiEndpointsJson | Out-File -FilePath (Join-Path $indexDir 'api-endpoints.json') -Encoding UTF8

    # Write external-apis.json
    $externalApisJson = @{
        version              = "1.0"
        timestamp            = $currentTimestamp
        third_party_services = $externalApis
        environment_variables = $envVars
    } | ConvertTo-Json -Depth 10

    $externalApisJson | Out-File -FilePath (Join-Path $indexDir 'external-apis.json') -Encoding UTF8

    # Write dependencies.json
    $dependenciesJson = @{
        version   = "1.0"
        timestamp = $currentTimestamp
        files     = $dependencies
    } | ConvertTo-Json -Depth 10

    $dependenciesJson | Out-File -FilePath (Join-Path $indexDir 'dependencies.json') -Encoding UTF8

    # Create empty files for other schemas
    @{version = "1.0"; timestamp = $currentTimestamp; database_schemas = @(); orm_entities = @(); type_definitions = @() } | ConvertTo-Json | Out-File -FilePath (Join-Path $indexDir 'data-models.json') -Encoding UTF8

    # Output summary
    if ($Json) {
        Write-Output $metadataJson
    }
    else {
        Write-Host ""
        Write-Host "[OK] Index built successfully in $duration seconds" -ForegroundColor Green
        Write-Host "[OK] Files indexed: $indexedFiles" -ForegroundColor Green
        Write-Host "[OK] Classes: $totalClasses" -ForegroundColor Green
        Write-Host "[OK] Functions: $totalFunctions" -ForegroundColor Green
        Write-Host "[OK] Interfaces: $totalInterfaces" -ForegroundColor Green
        Write-Host "[OK] REST endpoints: $totalRestEndpoints" -ForegroundColor Green
        Write-Host "[OK] GraphQL resolvers: $totalGraphQLResolvers" -ForegroundColor Green
        Write-Host "[OK] WebSocket handlers: $totalWebSocketHandlers" -ForegroundColor Green
        Write-Host "[OK] External APIs: $totalExternalApis" -ForegroundColor Green
        Write-Host "[OK] Environment variables: $totalEnvVars" -ForegroundColor Green
        Write-Host "[OK] Dependencies: $totalDependencies" -ForegroundColor Green
        Write-Host "[OK] Location: $indexDir" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:"
        Write-Host "  - Generate documentation: /speckitsmart.wiki"
        Write-Host "  - Query codebase: /speckitsmart.ask your-question"
    }

    exit 0
}
catch {
    $errorMsg = $_.Exception.Message
    Write-Host "Error: $errorMsg" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
    exit 1
}
