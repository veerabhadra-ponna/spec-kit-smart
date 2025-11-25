# Quickstart Guide: Codebase Indexing System

**Feature**: C00000-0001-codebase-indexing
**For**: Developers implementing or using the indexing system
**Last Updated**: 2025-01-25

## For Users: Getting Started

### Prerequisites

**Required**:
- Bash 4.0+ (macOS/Linux) or PowerShell 5.1+ (Windows)
- jq JSON processor

**Installation**:

```bash
# macOS
brew install jq

# Linux (Ubuntu/Debian)
sudo apt-get install jq

# Linux (RHEL/CentOS)
sudo yum install jq

# Windows (Chocolatey)
choco install jq

# Windows (Scoop)
scoop install jq
```

**Optional**:
- Git (for automatic repo root detection)

---

### Basic Usage

#### 1. Build Index (First Time)

```bash
# Default: Full index of entire repository
/speckitsmart.index

# Expected output:
# Building codebase index...
# Found 189 files (TypeScript: 145, JavaScript: 32, JSON: 12)
# ...
# ✓ Index built successfully in 42 seconds
# ✓ Files indexed: 189
# ✓ Location: .analysis/index/
```

#### 2. Update Index (After Code Changes)

```bash
# Incremental update (only changed files)
/speckitsmart.index --incremental

# Expected output:
# Updating codebase index (incremental mode)...
# Found 3 changed files since last index
# ...
# ✓ Index updated successfully in 5 seconds
```

#### 3. Analyze Project (Using Index)

```bash
# Reverse engineer codebase (requires index)
/speckitsmart.analyze-project

# If index missing, you'll see:
# ❌ ERROR: Codebase index not found
# Run /speckitsmart.index first
```

#### 4. Generate Documentation (Optional)

```bash
# Generate DeepWiki docs from index
/speckitsmart.wiki

# Output location: .deepwiki/
```

#### 5. Query Codebase (Optional)

```bash
# Ask questions about the codebase
/speckitsmart.ask "How does authentication work?"
/speckitsmart.ask "What database tables exist?"
/speckitsmart.ask "Show me all user management endpoints"
```

---

### Advanced Options

```bash
# Index specific directory only
/speckitsmart.index --path src/

# Filter by language
/speckitsmart.index --languages ts,js

# Exclude patterns
/speckitsmart.index --exclude "**/*.test.ts,dist/**"

# Verbose output (see detailed progress)
/speckitsmart.index --verbose

# JSON output (for scripting)
/speckitsmart.index --json

# Force full rebuild
/speckitsmart.index --full
```

---

### Troubleshooting

**Q: Index build fails with "jq: command not found"**

A: Install jq (see Prerequisites above)

**Q: Index build is slow (>5 minutes)**

A: This is normal for very large repos (>50K files). Try:
- Index subdirectories only: `/speckitsmart.index --path src/`
- Exclude test files: `/speckitsmart.index --exclude "**/*.test.ts"`

**Q: Index is stale warning**

A: Run incremental update: `/speckitsmart.index --incremental`

**Q: Some files not indexed**

A: Check verbose output for reasons:
```bash
/speckitsmart.index --verbose
```

Common reasons:
- File >10MB (increase limit with `--max-file-size`)
- Parse errors (check file syntax)
- Binary files (skipped automatically)

---

## For Developers: Implementation Guide

### Project Structure

```text
.specify/scripts/
├── bash/
│   ├── build-codebase-index.sh        # Core indexing script
│   ├── check-index-prerequisite.sh    # Hard prerequisite check
│   ├── check-index-optional.sh        # Soft prerequisite check
│   └── load-index-for-analysis.sh     # Load index data
│
└── powershell/
    ├── Build-CodebaseIndex.ps1        # PowerShell equivalent
    ├── Check-IndexPrerequisite.ps1    # PowerShell equivalent
    ├── Check-IndexOptional.ps1        # PowerShell equivalent
    └── Load-IndexForAnalysis.ps1      # PowerShell equivalent
```

### Key Implementation Files

1. **Commands** (`.claude/commands/`):
   - `index.md` - `/speckitsmart.index` command
   - `wiki.md` - `/speckitsmart.wiki` command
   - `ask.md` - `/speckitsmart.ask` command

2. **Scripts** (`.specify/scripts/bash/` and `.specify/scripts/powershell/`):
   - `build-codebase-index.sh/ps1` - Main indexing logic
   - `check-index-prerequisite.sh/ps1` - Validates index exists
   - `check-index-optional.sh/ps1` - Optional index check
   - `load-index-for-analysis.sh/ps1` - Loads index for analysis

3. **Contracts** (`specs/C00000-0001-codebase-indexing/contracts/`):
   - `metadata-schema.json` - Metadata structure
   - `prerequisite-check-schema.json` - Prerequisite check output
   - Additional schemas for structure, data-models, api-endpoints

### Development Workflow

#### Phase 1: Core Indexing (P1)

1. **Implement prerequisite checks**:
   - Bash: `check-index-prerequisite.sh`
   - PowerShell: `Check-IndexPrerequisite.ps1`
   - Test: Verify JSON output format

2. **Implement index builder**:
   - Bash: `build-codebase-index.sh`
   - PowerShell: `Build-CodebaseIndex.ps1`
   - Start with 1-2 languages (TypeScript, JavaScript)
   - Add remaining languages incrementally

3. **Implement index loader**:
   - Bash: `load-index-for-analysis.sh`
   - PowerShell: `Load-IndexForAnalysis.ps1`
   - Test: Verify aggregated JSON output

4. **Create slash commands**:
   - `index.md` - Calls build script with args
   - Update `analyze-project.md` - Add prerequisite check
   - Update `implement.md` - Add optional check

5. **Testing**:
   - Unit tests for each script
   - Integration test: index → analyze workflow
   - Cross-platform tests (Linux, macOS, Windows)

#### Phase 2: Documentation & Query (P2)

1. **Implement DeepWiki generator**:
   - Bash: `generate-deepwiki.sh`
   - PowerShell: `Generate-DeepWiki.ps1`
   - Generate 4-tier docs from index

2. **Implement query engine**:
   - Bash: `search-knowledge-base.sh`
   - PowerShell: `Search-KnowledgeBase.ps1`
   - Keyword-based search (Phase 1)
   - Semantic search (Phase 2 - vector embeddings)

3. **Create slash commands**:
   - `wiki.md` - Calls wiki generator
   - `ask.md` - Calls query engine

#### Phase 3: Code Reusability (P3)

1. **Implement reuse finder**:
   - Bash: `find-reusable-code.sh`
   - PowerShell: `Find-ReusableCode.ps1`
   - Search index for similar code

2. **Integrate with implement**:
   - Update `implement.md` - Call reuse finder per task

### Testing Strategy

**Unit Tests** (Bash test framework - bats):
```bash
# tests/indexing/test-prerequisite-checks.sh
test_prerequisite_index_exists() {
    # Setup: Create mock index
    mkdir -p .analysis/index
    echo '{"freshness":"2025-01-25T10:30:00Z","statistics":{"indexed_files":100}}' > .analysis/index/metadata.json

    # Execute
    result=$(./scripts/bash/check-index-prerequisite.sh)

    # Assert
    assert_equals "$(echo "$result" | jq -r '.index_exists')" "true"

    # Cleanup
    rm -rf .analysis/index
}
```

**Integration Tests**:
```bash
# tests/indexing/test-index-building.sh
test_full_index_workflow() {
    # Build index
    ./scripts/bash/build-codebase-index.sh --path tests/fixtures/typescript-express

    # Verify index files created
    assert_file_exists .analysis/index/metadata.json
    assert_file_exists .analysis/index/structure.json

    # Verify metadata
    version=$(jq -r '.version' .analysis/index/metadata.json)
    assert_equals "$version" "1.0"
}
```

**Cross-Platform Tests** (GitHub Actions):
```yaml
# .github/workflows/test-indexing.yml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-22.04, macos-13, windows-2022]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - name: Install jq
        run: |
          # Platform-specific jq installation
      - name: Run tests
        run: |
          # Run bash tests on Unix, PowerShell tests on Windows
```

### Performance Targets

| Metric | Target | Test Method |
|--------|--------|-------------|
| Small repo (<1K files) | <10s | Benchmark on typescript-express fixture |
| Medium repo (1K-10K files) | <60s | Benchmark on real-world projects |
| Large repo (10K-50K files) | <5min | Benchmark on open-source repos |
| Incremental update | <5s | Modify 1 file, re-index, measure time |
| Memory usage | <500MB | Monitor during large repo indexing |
| Index size | <1% of codebase | Compare `.analysis/index/` size vs repo size |

### Security Checklist

- [ ] Secret redaction patterns implemented
- [ ] `.analysis/` auto-added to .gitignore
- [ ] File permissions set to 700 (owner only)
- [ ] No network access (all local processing)
- [ ] Input validation for paths (prevent directory traversal)
- [ ] Error messages don't leak sensitive info

### Deployment Checklist

- [ ] Bash scripts tested on Ubuntu 22.04
- [ ] Bash scripts tested on macOS 13+
- [ ] PowerShell scripts tested on Windows 11
- [ ] jq installation documented for all platforms
- [ ] JSON schemas validated
- [ ] AGENTS.md updated with indexing section
- [ ] Sample fixture projects created
- [ ] Integration tests passing on all platforms

---

## Next Steps

**After Phase 1 Complete**:
1. Run `/speckitsmart.tasks` to generate implementation tasks
2. Implement tasks in priority order (P1 → P2 → P3)
3. Test each component on all platforms
4. Gather user feedback on MVP (Phase 1)
5. Plan Phase 2 enhancements (tree-sitter AST, semantic search)

**Phase 2 Enhancements**:
- Tree-sitter AST parsing (100% accuracy vs 80% regex)
- Vector embeddings for semantic search
- Parallelization for faster indexing
- Additional language support (Rust, Ruby, PHP, Swift)
