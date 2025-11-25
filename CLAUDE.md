# spec-kit-smart Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-25

## Active Technologies

- Bash 4.0+ (Unix/Linux/macOS), PowerShell 5.1+ (Windows) (feature/C00000-0001-codebase-indexing)
- jq 1.6+ - JSON processing for indexing system
- git - Repository root detection (optional with fallback)
- tree-sitter - AST parsing (Phase 2, regex fallback in Phase 1)

## Project Structure

```text
src/
tests/
```

## Commands

### Codebase Indexing System

- `/speckitsmart.index` - Build or update codebase index in `.analysis/index/`
  - Supports: `--full`, `--incremental`, `--path <dir>`, `--verbose`, `--json`
  - Extracts: classes, functions, interfaces, data models, API endpoints, external services

- `/speckitsmart.wiki` - Generate DeepWiki documentation from index in `.deepwiki/`

- `/speckitsmart.ask` - Query codebase using natural language with index data

- `/speckitsmart.analyze-project` - MODIFIED: Now checks for index availability (soft prerequisite)

- `/speckitsmart.implement` - MODIFIED: Now suggests reusable code from index (optional)

## Code Style

Bash 4.0+ (Unix/Linux/macOS), PowerShell 5.1+ (Windows): Follow standard conventions

## Recent Changes

- feature/C00000-0001-codebase-indexing: Added Bash 4.0+ (Unix/Linux/macOS), PowerShell 5.1+ (Windows)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
