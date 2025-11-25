# Generate DeepWiki Documentation

Generate comprehensive, multi-tier documentation from your codebase index.

## Overview

The `/speckitsmart.wiki` command creates structured documentation in `.deepwiki/` directory:

**Tier 1**: High-level overview (README.md style)
**Tier 2**: Functional summary (what the system does)
**Tier 3**: Architecture diagrams (component and data flow)
**Tier 4**: Detailed module documentation

## Prerequisites

**Hard Requirement**: Codebase index must exist

```bash
# Check if index exists
if [[ ! -d ".analysis/index" ]]; then
    echo "Error: Codebase index not found."
    echo "Run /speckitsmart.index first to build the index."
    exit 1
fi
```

## Usage

```bash
/speckitsmart.wiki [--output <dir>] [--tiers <1,2,3,4>] [--format markdown]
```

## Flags

- `--output <dir>` - Output directory (default: `.deepwiki`)
- `--tiers <list>` - Comma-separated tier numbers to generate (default: all)
- `--format <type>` - Output format: markdown (default), html
- `--verbose` - Show detailed progress

## Output Structure

```
.deepwiki/
├── index.md                    # Navigation index
├── overview.md                 # Tier 1: High-level overview
├── functional-summary.md       # Tier 2: What the system does
├── architecture/
│   ├── component-diagram.md    # Tier 3: Component relationships
│   └── data-flow-diagram.md    # Tier 3: Data flow
├── modules/
│   ├── auth/                   # Tier 4: Per-module docs
│   ├── api/
│   └── database/
└── api-reference/
    ├── rest-endpoints.md
    ├── graphql-schema.md
    └── data-models.md
```

## Examples

```bash
# Generate all tiers
/speckitsmart.wiki

# Generate only overview and functional summary
/speckitsmart.wiki --tiers 1,2

# Custom output directory
/speckitsmart.wiki --output docs/generated

# Verbose output
/speckitsmart.wiki --verbose
```

## Generated Content

### Tier 1: Overview

- Project purpose and scope
- Technology stack summary
- Quick start guide
- Key features list

### Tier 2: Functional Summary

- User scenarios and workflows
- System capabilities
- Integration points
- Business logic overview

### Tier 3: Architecture

- Component diagram (Mermaid)
- Data flow diagram (Mermaid)
- System boundaries
- External dependencies

### Tier 4: Module Documentation

- Per-module breakdown
- Class and function documentation
- API endpoint details
- Data model schemas

## Performance

- Small projects (<1K files): 10-20 seconds
- Medium projects (1K-10K files): 30-60 seconds
- Large projects (10K-50K files): 1-2 minutes

## Next Steps

After generating documentation:
- Review `.deepwiki/index.md` for navigation
- Query specific details: `/speckitsmart.ask "question"`
- Share documentation with team

---

## Implementation

**Prerequisites Check**: Use hard prerequisite validation

```bash
# Platform detection
PLATFORM=$(bash scripts/bash/detect-os.sh 2>/dev/null || echo "unix")

# Check index exists
if [[ "$PLATFORM" == "windows" ]]; then
    INDEX_CHECK=$(powershell.exe -ExecutionPolicy Bypass -File scripts/powershell/Check-IndexPrerequisite.ps1)
else
    INDEX_CHECK=$(bash scripts/bash/check-index-prerequisite.sh)
fi

INDEX_EXISTS=$(echo "$INDEX_CHECK" | jq -r '.index_exists')

if [[ "$INDEX_EXISTS" != "true" ]]; then
    echo "Error: $(echo "$INDEX_CHECK" | jq -r '.error')"
    exit 1
fi

# Show staleness warning if applicable
IS_STALE=$(echo "$INDEX_CHECK" | jq -r '.is_stale // false')
AGE_DAYS=$(echo "$INDEX_CHECK" | jq -r '.age_days // 0')

if [[ "$IS_STALE" == "true" ]]; then
    echo "⚠️  Warning: Index is $AGE_DAYS days old (stale)"
    echo "Consider running: /speckitsmart.index --incremental"
    echo ""
fi
```

**Route to Platform Script**:

```bash
if [[ "$PLATFORM" == "windows" ]]; then
    powershell.exe -ExecutionPolicy Bypass -File .specify/scripts/powershell/Generate-DeepWiki.ps1 "$@"
else
    bash .specify/scripts/bash/generate-deepwiki.sh "$@"
fi
```

The command delegates to:
- **Bash**: `.specify/scripts/bash/generate-deepwiki.sh`
- **PowerShell**: `.specify/scripts/powershell/Generate-DeepWiki.ps1`

Both scripts read from `.analysis/index/` and generate markdown documentation in `.deepwiki/`.
