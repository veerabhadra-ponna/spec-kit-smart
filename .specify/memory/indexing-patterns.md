# Codebase Indexing Patterns Reference

This document describes patterns and best practices for the codebase indexing system.

## Index Structure Patterns

### Flat vs Hierarchical
The index uses a **flat file structure** with JSON files:
```
.analysis/index/
├── metadata.json       # Index metadata and statistics
├── structure.json      # Code structure (classes, functions)
├── data-models.json    # Database models and schemas
├── api-endpoints.json  # API endpoint definitions
├── external-apis.json  # Third-party integrations
└── dependencies.json   # Import/export relationships
```

**Rationale**: Flat structure enables:
- Fast random access to any index component
- Easy partial loading (load only what's needed)
- Simple incremental updates
- Cross-platform compatibility

### Schema Versioning
Each index file includes version information:
```json
{
  "version": "1.0",
  "generated": "2025-01-25T10:00:00Z",
  "tool_version": "1.0.0"
}
```

**Version Compatibility Rules**:
- Major version change = breaking change, requires full rebuild
- Minor version change = backward compatible, incremental works
- Tool must validate version before reading

## Extraction Patterns

### Class Detection
Pattern-based extraction across languages:

**TypeScript/JavaScript**:
```regex
(?:export\s+)?(?:abstract\s+)?class\s+(\w+)
```

**Python**:
```regex
class\s+(\w+)(?:\([^)]*\))?:
```

**Java/C#**:
```regex
(?:public|private|protected)?\s*(?:abstract|static)?\s*class\s+(\w+)
```

### Function Detection
**Named functions**:
```regex
(?:export\s+)?(?:async\s+)?function\s+(\w+)
```

**Arrow functions** (with name):
```regex
(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[^=])\s*=>
```

**Method definitions**:
```regex
(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{
```

### API Endpoint Detection

**Express.js**:
```regex
(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*['"`]([^'"`]+)['"`]
```

**Decorators** (NestJS, Spring):
```regex
@(Get|Post|Put|Delete|Patch)\s*\(\s*['"`]([^'"`]+)['"`]
```

**Flask/FastAPI**:
```regex
@(?:app|router)\.(get|post|put|delete)\s*\(\s*['"`]([^'"`]+)['"`]
```

### External API Detection

**SDK Patterns**:
```regex
require\s*\(\s*['"`](stripe|aws-sdk|firebase|twilio|sendgrid)['"`]\)
```

**HTTP Client Calls**:
```regex
(?:axios|fetch|http|request)\.(get|post|put|delete)\s*\(\s*['"`](https?://[^'"`]+)['"`]
```

**Environment Variables**:
```regex
process\.env\.(\w+)|os\.environ(?:\.get)?\s*\(\s*['"`](\w+)['"`]
```

## Performance Patterns

### Incremental Updates
Use MD5 hash tracking for efficient updates:

1. **Hash Calculation**: Store file hash on index
2. **Change Detection**: Compare current hash vs stored
3. **Selective Update**: Only re-parse changed files
4. **Merge Strategy**: Update changed entries, preserve unchanged

```json
{
  "file_hashes": {
    "src/auth/login.ts": "a1b2c3d4e5f6...",
    "src/api/users.ts": "f6e5d4c3b2a1..."
  }
}
```

### Large File Handling
For files > 10MB:
1. Skip binary files automatically
2. Truncate at 10MB for text files
3. Log warning about truncation
4. Extract what's available

### Memory Optimization
- Stream file reading (don't load entire file)
- Process one file at a time
- Write index incrementally
- Garbage collect after each directory

## Query Patterns

### Keyword-Based Search
1. Extract keywords from query (remove stop words)
2. Search each index file for keyword matches
3. Score by match count and location
4. Return top N results with confidence

### Confidence Scoring
```
confidence = (matched_keywords / total_keywords) * 100
```

Boost factors:
- Exact name match: +20%
- File path match: +10%
- Multiple matches in same file: +5% per match

### Result Ranking
Priority order:
1. Exact class/function name match
2. API endpoint path match
3. File path contains keyword
4. Code content contains keyword

## Integration Patterns

### With Analyze-Project
```bash
# Load index before analysis
INDEX_STATUS=$(bash check-index-optional.sh)
if [[ $(echo "$INDEX_STATUS" | jq -r '.index_available') == "true" ]]; then
    # Use pre-extracted data
    STRUCTURE=$(bash load-index-for-analysis.sh --section structure)
else
    # Fall back to direct parsing
    analyze_directly
fi
```

### With Implementation
```bash
# Find reusable code before implementing
REUSABLE=$(bash find-reusable-code.sh --task "$TASK_DESCRIPTION")
SIMILAR_COUNT=$(echo "$REUSABLE" | jq '.summary.similar_implementations')
if [[ $SIMILAR_COUNT -gt 0 ]]; then
    echo "Found similar implementations:"
    echo "$REUSABLE" | jq '.results.similar[]'
fi
```

## Error Handling Patterns

### Graceful Degradation
```bash
# Always provide fallback
parse_file() {
    local file="$1"
    result=$(extract_structure "$file" 2>/dev/null) || {
        # On error, return empty structure
        echo '{"classes":[],"functions":[]}'
        return 0
    }
    echo "$result"
}
```

### Validation Before Use
```bash
# Validate index before loading
validate_index() {
    local metadata="$1"

    # Check required fields
    if ! jq -e '.version and .freshness and .statistics' "$metadata" >/dev/null 2>&1; then
        return 1
    fi

    # Check version compatibility
    local version=$(jq -r '.version' "$metadata")
    local major=${version%%.*}
    if [[ "$major" != "1" ]]; then
        return 2  # Incompatible version
    fi

    return 0
}
```

## Best Practices

### DO
- Always validate index before use
- Use incremental updates for daily development
- Run full rebuild after major refactoring
- Include meaningful progress output for --verbose
- Handle encoding issues gracefully (UTF-8 preferred)

### DON'T
- Don't parse files > 10MB
- Don't include secrets in index
- Don't block on single file failures
- Don't assume file encoding
- Don't store absolute paths (use repo-relative)

## Troubleshooting

### Common Issues

**Empty Index Results**
- Check file extensions match language filters
- Verify files aren't in excluded directories
- Ensure regex patterns match actual code style

**Slow Indexing**
- Check for large binary files in source
- Exclude `node_modules`, `vendor`, etc.
- Use `--path` to index specific directories

**Stale Index**
- Run `--incremental` after code changes
- Check if `.analysis/` is gitignored
- Verify file modification times are accurate

---

*This document is auto-referenced by the indexing system for self-documentation.*
