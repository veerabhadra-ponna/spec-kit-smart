# Build Codebase Index

Build a searchable index of your codebase containing:
- Code structure (classes, functions, interfaces)
- Data models (database schemas, ORM entities)
- API endpoints (REST, GraphQL, WebSocket)
- External integrations (third-party services)
- Dependency graph (imports/exports)

The index is stored in `.analysis/index/` and used by other commands for fast analysis.

## Usage

```bash
/speckitsmart.index [--full|--incremental] [--path <dir>] [--verbose] [--json]
```

## Flags

- `--full` - Force full rebuild (default if no index exists)
- `--incremental` - Update only changed files (requires existing index)
- `--path <dir>` - Index specific directory instead of entire repository
- `--languages <list>` - Filter by languages (e.g., `--languages ts,js,py`)
- `--exclude <pattern>` - Exclude glob patterns
- `--verbose` - Show detailed progress output
- `--json` - Output results as JSON

## Supported Languages

- TypeScript (.ts, .tsx)
- JavaScript (.js, .jsx)
- Python (.py)
- Java (.java)
- C# (.cs)
- Go (.go)

## Examples

```bash
# Build full index
/speckitsmart.index

# Incremental update
/speckitsmart.index --incremental

# Index specific directory
/speckitsmart.index --path src/services

# Index only TypeScript files
/speckitsmart.index --languages ts

# Verbose output
/speckitsmart.index --verbose
```

## Output

Index files are created in `.analysis/index/`:
- `metadata.json` - Statistics and freshness tracking
- `structure.json` - Classes, functions, interfaces
- `data-models.json` - Database schemas and entities
- `api-endpoints.json` - REST/GraphQL/WebSocket endpoints
- `external-apis.json` - Third-party service integrations
- `dependencies.json` - Import/export graph

## Performance

- Small projects (<1K files): 5-10 seconds
- Medium projects (1K-10K files): 30-60 seconds
- Large projects (10K-50K files): 2-5 minutes
- Incremental updates: <5 seconds

## Next Steps

After building the index, you can:
- Analyze project faster: `/speckitsmart.analyze-project`
- Generate documentation: `/speckitsmart.wiki`
- Query codebase: `/speckitsmart.ask "your question"`

---

## Implementation

**Prerequisites**: Check for jq dependency (required for JSON processing)

```bash
if ! command -v jq >/dev/null 2>&1; then
    echo "Error: jq is required but not installed."
    echo ""
    echo "Installation instructions:"
    echo "  macOS:   brew install jq"
    echo "  Linux:   apt-get install jq  or  yum install jq"
    echo "  Windows: choco install jq  or download from https://jqlang.github.io/jq/"
    exit 1
fi
```

**Platform Detection**: Use central OS detection utility

```bash
# Detect platform
PLATFORM=$(bash scripts/bash/detect-os.sh 2>/dev/null || echo "unix")

# Route to appropriate script
if [[ "$PLATFORM" == "windows" ]]; then
    # Windows: Use PowerShell script
    powershell.exe -ExecutionPolicy Bypass -File scripts/powershell/Build-CodebaseIndex.ps1 "$@"
else
    # Unix/Linux/macOS: Use Bash script
    bash scripts/bash/build-codebase-index.sh "$@"
fi
```

**Parse Arguments**: Handle flags and pass to appropriate script

The command delegates to platform-specific scripts:
- **Bash**: `scripts/bash/build-codebase-index.sh`
- **PowerShell**: `scripts/powershell/Build-CodebaseIndex.ps1`

Both scripts implement the same interface and produce identical JSON output.
