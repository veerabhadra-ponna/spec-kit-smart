# Research: Codebase Indexing System

**Feature**: C00000-0001-codebase-indexing
**Date**: 2025-01-25
**Status**: Phase 0 Complete

## Overview

This document captures research findings and technical decisions for implementing the codebase indexing system. All decisions are derived from the technical specification document (`docs/codebase-indexing-technical-spec.md`) which provides detailed implementation guidance.

---

## Decision 1: Cross-Platform Script Strategy

**Context**: Need to support Windows, macOS, and Linux for codebase indexing

**Decision**: Dual implementation - Bash for Unix/Linux/macOS, PowerShell for Windows

**Rationale**:
- **Bash 4.0+**: Widely available on modern Unix systems (Ubuntu 18.04+, macOS 10.15+)
  - Rich text processing tools (grep, sed, awk) built-in
  - Standard for Unix shell scripting
  - No additional runtime installation needed

- **PowerShell 5.1+**: Bundled with Windows 10+
  - Native Windows scripting environment
  - Equivalent cmdlets for Unix tools (Get-ChildItem vs find)
  - No additional installation needed on modern Windows

- **OS Detection**: Scripts auto-detect platform via `uname` (Unix) or `$env:OS` (Windows)
  - Environment variable override: `SPEC_KIT_PLATFORM` (unix/windows/auto)
  - Config file support: `.specify/config.json` osEnv field

**Alternatives Considered**:
1. **Node.js scripts**: Rejected - would require Node.js installation (additional dependency)
2. **Python scripts**: Rejected - would require Python installation (not guaranteed on all systems)
3. **Single bash with WSL requirement**: Rejected - not all Windows users have WSL installed

**Implementation Notes**:
- Maintain parallel bash/.sh and PowerShell/.ps1 versions for all scripts
- Share JSON schemas for consistent output format
- Test matrix: Ubuntu 22.04, macOS 13+, Windows 11

**References**:
- Technical spec §6 (Script Implementation)
- Technical spec §8.3 (Cross-Platform Tests)

---

## Decision 2: Index Storage Format

**Context**: Need structured storage for extracted code data that's queryable and human-readable

**Decision**: JSON files in `.analysis/index/` directory (6 separate files by domain)

**Structure**:
```
.analysis/index/
├── structure.json       # Code elements (classes, functions, interfaces)
├── data-models.json     # Database schemas, ORM entities
├── api-endpoints.json   # REST/GraphQL/WebSocket handlers
├── external-apis.json   # Third-party service integrations
├── dependencies.json    # Import/export graphs
└── metadata.json        # Statistics, freshness, build info
```

**Rationale**:
- **Human-readable**: JSON is text-based, easy to inspect/debug without special tools
- **Queryable**: jq provides powerful JSON query/transformation capabilities
- **Structured**: JSON schemas provide validation and documentation
- **Separation of concerns**: 6 domain files allow loading only needed data
- **Performance**: File-based is fast for local CLI tool (<1% of codebase size)
- **Git-friendly**: Plain text format (though gitignored for generated content)

**Alternatives Considered**:
1. **SQLite database**: Rejected - requires SQLite installation, less transparent, harder to debug
2. **Single JSON file**: Rejected - would be large, loading all data when only subset needed
3. **Binary format (Protocol Buffers)**: Rejected - not human-readable, requires special tools
4. **YAML**: Rejected - slower parsing, less tooling support than JSON

**JSON Schema Versioning**:
- Version field in each JSON file (currently "1.0")
- Breaking changes require major version bump
- Scripts validate version before loading

**References**:
- Technical spec §5 (Index Storage Format)
- Technical spec §5.2 (Schema Definitions)

---

## Decision 3: Code Extraction Strategy (Phase 1)

**Context**: Need to extract code structure from 6 languages (TypeScript, JavaScript, Python, Java, C#, Go)

**Decision**: Regex-based parsing for Phase 1, tree-sitter AST parsing for Phase 2

**Phase 1 (Regex-based)**:
- **Advantages**:
  - No external dependencies (uses built-in grep/sed/awk)
  - Fast implementation (pattern matching)
  - Sufficient for 80%+ of common cases

- **Limitations**:
  - May miss complex nested structures
  - Limited context awareness
  - Edge cases in minified/obfuscated code

- **Patterns** (examples for TypeScript):
  - Classes: `(export\s+)?class\s+([A-Za-z0-9_]+)`
  - Functions: `(export\s+)?function\s+([A-Za-z0-9_]+)` and `const\s+([A-Za-z0-9_]+)\s*=\s*(\(.*\)|async)`
  - Interfaces: `(export\s+)?interface\s+([A-Za-z0-9_]+)`

**Phase 2 (tree-sitter AST)**:
- **Advantages**:
  - 100% accurate parsing (uses language grammars)
  - Full context awareness (AST nodes)
  - Handles all edge cases

- **Trade-offs**:
  - Requires tree-sitter installation
  - More complex implementation
  - Slightly slower (AST construction overhead)

**Rationale for Phase 1 Approach**:
- Deliver value faster (no tree-sitter dependency initially)
- Regex sufficient for majority use cases (typical enterprise code)
- Allows user feedback before investing in AST parsing
- Can upgrade to tree-sitter transparently (same JSON output format)

**Fallback Strategy**:
- If regex extraction fails (syntax errors), log warning and skip file
- Mark in metadata as "partial extraction" with error count
- Continue indexing other files (graceful degradation)

**Alternatives Considered**:
1. **Tree-sitter from day 1**: Rejected - adds dependency and complexity for MVP
2. **Language-specific parsers** (TypeScript Compiler API, etc.): Rejected - requires runtime (Node.js for TS)
3. **Static analysis tools** (ESLint, Pylint): Rejected - heavier dependencies, slower

**References**:
- Technical spec §4 (Data Extraction Algorithms)
- Technical spec §9.2 (Query Performance - Phase 2 upgrade path)

---

## Decision 4: Prerequisite Check System

**Context**: Some commands require index (hard dependency), others benefit from it (soft dependency)

**Decision**: Two-tier prerequisite check system - hard (fail) and soft (warn)

**Hard Prerequisites** (fail if index missing):
- `/speckitsmart.analyze-project` - Cannot analyze without pre-extracted data
- `/speckitsmart.wiki` - Cannot generate docs without index source
- `/speckitsmart.ask` - Cannot answer questions without knowledge base

**Script**: `check-index-prerequisite.sh` / `Check-IndexPrerequisite.ps1`

**Behavior**:
- Check if `.analysis/index/` exists
- Validate `metadata.json` presence (integrity check)
- Calculate index age (staleness: >7 days)
- Return JSON with: `index_exists`, `index_path`, `freshness`, `age_days`, `is_stale`, `files_indexed`
- Exit code 1 if missing (hard failure)

**Soft Prerequisites** (warn but continue):
- `/speckitsmart.implement` - Benefits from code reusability checks, but can proceed without

**Script**: `check-index-optional.sh` / `Check-IndexOptional.ps1`

**Behavior**:
- Same checks as hard prerequisite
- If missing: Display warning about disabled features, continue with exit code 0
- If present: Display confirmation of enabled features

**Staleness Handling**:
- Fresh: <24 hours (confirmed, proceed immediately)
- Valid: <7 days (confirmed, proceed immediately)
- Stale: >7 days (warning, ask user confirmation before proceeding)

**Rationale**:
- Clear separation between required and optional dependencies
- User-friendly error messages with remediation steps
- Allows graceful degradation (implement works without index, just less helpful)
- Staleness checks prevent using outdated data unknowingly

**Alternatives Considered**:
1. **Single prerequisite check**: Rejected - doesn't distinguish hard vs soft requirements
2. **Automatic index rebuild on missing**: Rejected - unexpected side effects, could take time
3. **No staleness checks**: Rejected - users might unknowingly use old data

**References**:
- Technical spec §3 (Prerequisite Check System)
- Technical spec §3.1 (Check Types)

---

## Decision 5: Incremental Index Updates

**Context**: Full rebuilds on large codebases (>10K files) take minutes; need faster updates after small changes

**Decision**: MD5 hash-based change detection for incremental updates

**Algorithm**:
1. During full build: Compute MD5 hash for each indexed file, store in `cache/file-hashes.json`
2. During incremental update:
   - Compute MD5 hash for each file
   - Compare with cached hash
   - Re-index only files with changed hashes
   - Update hashes in cache

**Storage**:
```json
{
  "src/models/User.ts": "a1b2c3d4e5f6...",
  "src/routes/auth.ts": "f6e5d4c3b2a1...",
  ...
}
```

**Performance**:
- MD5 computation: ~1ms per file (negligible overhead)
- Target: <5 seconds for single file changes [FR-059, SC-002]
- Hash comparison: O(n) where n = total files, but hash computation is fast

**Edge Cases**:
- **No previous index**: Automatically fall back to full build
- **File deleted**: Remove from hash cache, remove from index
- **File renamed**: Detected as delete + add (re-index both)
- **Corrupted cache**: Fall back to full build

**Rationale**:
- MD5 is fast and sufficient for change detection (not using for security)
- File-level granularity balances simplicity vs performance
- Hash caching allows O(n) comparison (linear in file count)
- Transparent fallback to full build ensures reliability

**Alternatives Considered**:
1. **Timestamp-based**: Rejected - unreliable (file touches, git operations change timestamps without content changes)
2. **Git diff**: Rejected - only works in git repos, doesn't handle uncommitted changes
3. **SHA-256**: Rejected - slower than MD5, security not needed for change detection
4. **Content comparison**: Rejected - requires reading entire file twice (slower than hash)

**References**:
- Technical spec §9.1 (Indexing Performance - Incremental updates)
- Functional spec FR-010 (Incremental update support)

---

## Decision 6: Secret Redaction Strategy

**Context**: Code may contain hardcoded secrets (API keys, passwords, tokens) that shouldn't be indexed

**Decision**: Pattern-based secret detection and redaction before storing in index

**Patterns**:
```bash
# API keys, secrets, passwords
(API_KEY|SECRET|PASSWORD)\s*=\s*["']([^"']+)["'] → \1=***REDACTED***

# JWT tokens
eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+ → ***JWT_REDACTED***

# Bearer tokens
(token|auth|bearer)\s*:\s*["']([^"']+)["'] → \1: "***REDACTED***"
```

**Scope**:
- Redact before storing in index (not in original source files)
- Log redaction count in metadata.json for transparency
- Environment variable values redacted (keep names, redact values)

**Rationale**:
- Defense in depth: Even though index is local-only and gitignored, avoid storing secrets
- Pattern matching covers 95%+ of common cases
- Redaction is one-way (cannot recover original) - ensures secrets not leaked via index
- Non-intrusive: Only affects index, not source code

**Limitations**:
- May miss obfuscated secrets (base64-encoded, split strings)
- False positives possible (e.g., literal string "PASSWORD" in comments)
- Not a replacement for proper secret management (just additional safety)

**Alternatives Considered**:
1. **No redaction**: Rejected - security risk if index accidentally shared/committed
2. **Comprehensive secret detection** (Trufflehog, etc.): Rejected - heavy dependency, slower, overkill for local tool
3. **Encrypt index**: Rejected - complicates tooling, keys management, still need redaction for plaintext viewing

**References**:
- Technical spec §10 (Security Considerations)
- Technical spec §10.1 (Secret Detection)
- Functional spec FR-015 (Secret redaction requirement)

---

## Decision 7: Performance Targets & Optimization

**Context**: Need to set realistic performance expectations and plan optimizations

**Targets** (from functional spec):
- Small projects (<1K files): <10 seconds [FR-058]
- Medium projects (1K-10K files): <60 seconds [FR-058, SC-001]
- Large projects (10K-50K files): <5 minutes [FR-058]
- Incremental updates: <5 seconds for single file [FR-059, SC-002]
- Memory usage: <500MB for 50K files [SC-012]
- Index size: <1% of codebase size [SC-011]

**Phase 1 Strategy** (Single-threaded):
- **File scanning**: Use `find` with filters (exclude node_modules, .git, etc.)
- **Regex extraction**: Simple pattern matching (fast, no AST overhead)
- **Smart skipping**: Skip binary files, large files (>10MB), parse errors
- **Progress indicators**: Optional `--verbose` mode for user feedback

**Phase 2 Optimizations** (If needed based on Phase 1 results):
1. **Parallel file processing**:
   - Use `xargs -P` for bash (process N files in parallel)
   - Use `ForEach-Object -Parallel` for PowerShell 7+
   - Target: 4x speedup on multi-core systems

2. **Batching**:
   - Process files in batches of 100
   - Reduce memory footprint for very large repos

3. **Caching**:
   - Cache frequently accessed patterns (e.g., framework detection)
   - Precompute common queries

**Rationale for Phased Approach**:
- Start simple (single-threaded) to validate feasibility
- Measure actual performance before optimizing
- Avoid premature optimization (may not be needed if targets met)
- Parallel processing adds complexity (error handling, progress tracking)

**Monitoring**:
- Track metrics in metadata.json: duration_seconds, files_processed, parse_errors
- Log warnings for slow files (>1s per file)
- Provide --verbose mode for debugging slow indexing

**Alternatives Considered**:
1. **Parallel from day 1**: Rejected - adds complexity, may not be needed
2. **Database indexing**: Rejected - slower than file-based for this use case
3. **Incremental writing** (stream to files): Rejected - complicates atomic writes

**References**:
- Technical spec §9 (Performance Optimization)
- Functional spec Success Criteria (SC-001 through SC-015)

---

## Decision 8: Testing Strategy

**Context**: Need comprehensive testing across 3 platforms (Linux, macOS, Windows) and 6 languages

**Strategy**: Unit tests + Integration tests + Cross-platform tests

**Unit Tests** (Bash test framework - bats):
- **Prerequisite checks**: Verify correct JSON output for exists/missing/stale scenarios
- **Data extraction**: Test regex patterns against fixture code samples
- **Hash computation**: Verify MD5 calculation and cache updates
- **Error handling**: Test parse failures, permission errors, missing dependencies

**Coverage Targets**:
- Prerequisite scripts: 100%
- Data extraction: 90%
- Index building: 90%
- Query functions: 85%

**Integration Tests**:
- **Full workflow**: index → analyze → wiki → ask
- **Prerequisite enforcement**: Try commands without index, verify failures
- **Incremental updates**: Modify file, verify only changed file re-indexed
- **Cross-language**: Test extraction on TypeScript, JavaScript, Python, Java, C#, Go fixtures

**Test Fixtures** (Sample projects):
```
tests/fixtures/sample-projects/
├── typescript-express/     # TypeScript + Express + TypeORM + Prisma
├── python-fastapi/         # Python + FastAPI + SQLAlchemy
└── java-spring-boot/       # Java + Spring Boot + Hibernate
```

**Cross-Platform Tests** (GitHub Actions matrix):
- Ubuntu 22.04 (bash)
- macOS 13+ (bash)
- Windows 11 (PowerShell)

**Test Matrix**:
| OS | Shell | Commands Tested | Scripts Tested |
|----|-------|----------------|----------------|
| Ubuntu 22.04 | bash | All | All .sh |
| macOS 13 | bash | All | All .sh |
| Windows 11 | PowerShell | All | All .ps1 |

**Rationale**:
- High coverage ensures reliability across platforms
- Fixture projects validate real-world extraction accuracy
- CI/CD automation catches platform-specific regressions early
- Unit tests fast (seconds), integration tests comprehensive (minutes)

**Alternatives Considered**:
1. **Manual testing only**: Rejected - error-prone, doesn't scale
2. **Single platform testing**: Rejected - misses platform-specific bugs
3. **Mock-based unit tests**: Rejected - integration with real files more valuable

**References**:
- Technical spec §8 (Testing Strategy)
- Technical spec §8.3 (Cross-Platform Tests)

---

## Open Questions for Implementation

### Q1: Custom File Extension Support
**Question**: Should we support custom file extensions via config file?

**Context**: Some projects use non-standard extensions (.tsx.snap, .spec.ts, etc.)

**Options**:
- A) Command-line flag only: `--languages ts,js,tsx`
- B) Config file: `.specify/config.json` with extension mappings
- C) Both flag and config (config as default, flag as override)

**Recommendation**: Option C - Start with flag (A) for MVP, add config (C) in Phase 2 based on user feedback

**Impact**: Determines extensibility model for language detection

---

### Q2: DeepWiki Commit Strategy
**Question**: Should generated `.deepwiki/` docs be committed to git or gitignored?

**Context**: Trade-off between always-fresh (gitignore) vs searchable-in-repo (commit)

**Options**:
- A) Gitignore (default): Generated on-demand, always fresh, no repo bloat
- B) Commit: Searchable in GitHub, PR-friendly, but stale if not regenerated
- C) User choice: Make configurable via flag/config

**Recommendation**: Option A for MVP - Gitignore by default, add `--commit` flag in Phase 2 if requested

**Impact**: Affects default .gitignore patterns and user onboarding guidance

---

### Q3: Large Repo Handling (>50K files)
**Question**: What's acceptable index build time for very large repos?

**Context**: Target is <5 min for 10K-50K files, but what about >50K?

**Options**:
- A) Support up to 100K files with longer build times (10-30 min acceptable)
- B) Hard limit at 50K files, recommend subdirectory indexing (`--path`)
- C) Implement parallelization if users report >50K file repos

**Recommendation**: Option C - Start with 50K target, monitor feedback, optimize if needed

**Impact**: May require parallelization implementation (Phase 2 optimization)

---

## Research Completion Summary

**Status**: ✅ All major technical decisions resolved

**Key Decisions**:
1. Cross-platform: Bash + PowerShell dual implementation
2. Storage: JSON files in `.analysis/index/` (6 domain files)
3. Extraction: Regex (Phase 1), tree-sitter (Phase 2)
4. Prerequisites: Two-tier check system (hard fail vs soft warn)
5. Incremental: MD5 hash-based change detection
6. Security: Pattern-based secret redaction
7. Performance: Single-threaded Phase 1, parallelization Phase 2 if needed
8. Testing: Comprehensive unit/integration/cross-platform coverage

**Open Questions**: 3 questions for Phase 1 implementation (custom extensions, DeepWiki commits, large repo limits)

**Next Phase**: Phase 1 - Data model design, API contracts, quickstart guide

**References**:
- Primary source: `docs/codebase-indexing-technical-spec.md`
- Functional requirements: `specs/C00000-0001-codebase-indexing/spec.md`
