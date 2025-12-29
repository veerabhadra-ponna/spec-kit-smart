# Feature Specification: Codebase Indexing System

**Feature Branch**: `feature/C00000-0001-codebase-indexing`
**Created**: 2025-01-25
**Status**: Draft
**Input**: User description: "Codebase indexing system with slash commands for building searchable code index, generating documentation (DeepWiki), and enabling AI-powered code analysis and reusability detection"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build Codebase Index for Fast Analysis (Priority: P1)

As a developer analyzing a legacy codebase, I want to build a searchable index of the code structure so that I can quickly understand the architecture without reading every file manually.

**Why this priority**: This is the foundational capability that enables all other features. Without the index, none of the other commands (wiki, ask, analyze-project enhancements) can function. Building the index is the critical first step that unlocks 10x faster analysis and 80% token reduction.

**Independent Test**: Can be fully tested by running `/speckitsmart.index` on a sample project and verifying that JSON index files are created in `.analysis/index/` with accurate code structure data.

**Acceptance Scenarios**:

1. **Given** a project with <1,000 source files, **When** I run `/speckitsmart.index`, **Then** the index builds in under 10 seconds and creates structure.json, data-models.json, api-endpoints.json, external-apis.json, and metadata.json files
2. **Given** a project with 1,000-10,000 source files, **When** I run `/speckitsmart.index`, **Then** the index builds in under 60 seconds with progress indicators showing files processed
3. **Given** an existing codebase index, **When** I modify one file and run `/speckitsmart.index --incremental`, **Then** only the changed file is re-indexed and the update completes in under 5 seconds
4. **Given** a project with TypeScript, JavaScript, Python, Java, C#, or Go files, **When** I run `/speckitsmart.index`, **Then** all classes, functions, interfaces, data models, API endpoints, and external integrations are extracted and stored in the index
5. **Given** a successful index build, **When** I check the output, **Then** I see statistics showing total files indexed, classes found, functions found, API endpoints detected, and data models discovered
6. **Given** a project with syntax errors in some files, **When** I run `/speckitsmart.index`, **Then** the indexing continues, skips invalid files, and displays warnings about files that failed to parse

---

### User Story 2 - Reverse Engineer Legacy Code with Index (Priority: P1)

As a tech lead planning a modernization project, I want `/speckitsmart.analyze-project` to use the codebase index so that reverse engineering completes 10x faster with more accurate results.

**Why this priority**: This delivers immediate value by dramatically accelerating the analyze-project workflow. Users already use this command for reverse engineering, and making it require an index (with prerequisite checks) ensures they get the full benefits of indexed data.

**Independent Test**: Can be tested by running `/speckitsmart.analyze-project` on a legacy codebase after building the index, and verifying that the analysis completes in 2-5 minutes instead of 20+ minutes, with comprehensive architecture, data models, and API surface information extracted from the index.

**Acceptance Scenarios**:

1. **Given** no codebase index exists, **When** I run `/speckitsmart.analyze-project`, **Then** the command stops with an error message explaining that index is required and instructing me to run `/speckitsmart.index` first
2. **Given** a fresh codebase index exists (< 24 hours old), **When** I run `/speckitsmart.analyze-project`, **Then** the command displays a confirmation message showing index freshness and files indexed, then proceeds with analysis
3. **Given** a stale codebase index exists (>7 days old), **When** I run `/speckitsmart.analyze-project`, **Then** the command displays a warning about stale data, recommends running incremental update, asks for user confirmation to continue, and proceeds only after user confirms
4. **Given** a valid index, **When** `/speckitsmart.analyze-project` runs, **Then** it loads pre-extracted architecture data (modules, entry points, patterns), data models (entities, schemas), API surface (endpoints, authentication), and external integrations (services, env vars) from the index instead of reading files manually
5. **Given** analysis with index, **When** the analysis completes, **Then** the total time is under 5 minutes for a 10K file codebase (vs 20+ minutes without index), and the analysis report includes comprehensive sections for architecture patterns, data models, API endpoints, and external services

---

### User Story 3 - Generate Comprehensive Documentation (Priority: P2)

As a team lead onboarding new developers, I want to generate comprehensive documentation (DeepWiki) automatically from the codebase index so that new team members can understand the system faster without extensive code reading.

**Why this priority**: Documentation generation is valuable but depends on having an index first (P1). It's a strong P2 because it directly addresses onboarding pain and provides long-term value, but it's not required for basic analysis workflows.

**Independent Test**: Can be tested by running `/speckitsmart.wiki` after building an index, and verifying that markdown documentation files are generated in `.deepwiki/` with 4-tier documentation structure (overview, functional summary, architecture details, and per-module docs).

**Acceptance Scenarios**:

1. **Given** no codebase index exists, **When** I run `/speckitsmart.wiki`, **Then** the command stops with an error message explaining that index is required and instructing me to run `/speckitsmart.index` first
2. **Given** a valid index exists, **When** I run `/speckitsmart.wiki`, **Then** documentation is generated in `.deepwiki/` directory with structure: `index.md`, `overview.md`, `functional-summary.md`, `architecture/`, `modules/`, and `api-reference/`
3. **Given** successful wiki generation, **When** I open the documentation, **Then** I see Tier 1 (overview), Tier 2 (functional summary), Tier 3 (high-level architecture with diagrams), and Tier 4 (detailed module documentation with code references)
4. **Given** the generated documentation, **When** I review API reference, **Then** I see all REST endpoints listed with methods, paths, request/response schemas, and authentication requirements
5. **Given** the generated documentation, **When** I review data models, **Then** I see all database tables and ORM entities with schemas, relationships, and source file references
6. **Given** optional generation flags, **When** I run `/speckitsmart.wiki --tiers 1,2`, **Then** only Tier 1 and Tier 2 documentation is generated (faster for quick overviews)

---

### User Story 4 - Query Codebase with Natural Language (Priority: P2)

As a developer working on a feature, I want to ask natural language questions about the codebase so that I can get instant answers with code examples and file references without manually searching.

**Why this priority**: This is a powerful productivity feature but depends on index (P1) and optionally DeepWiki (P2). It's P2 because it's valuable for ongoing development but not critical for initial analysis or onboarding workflows.

**Independent Test**: Can be tested by running `/speckitsmart.ask "How does authentication work?"` after building index/wiki, and verifying that a clear answer is returned with code examples, file paths with line numbers, and source citations.

**Acceptance Scenarios**:

1. **Given** no codebase index exists, **When** I run `/speckitsmart.ask "any question"`, **Then** the command stops with an error message explaining that index is required and instructing me to build index and optionally generate wiki
2. **Given** index exists but DeepWiki is missing, **When** I run `/speckitsmart.ask`, **Then** the command displays a warning that answers will be based on code index only (lower quality), suggests generating wiki, and asks for confirmation to continue
3. **Given** both index and DeepWiki exist, **When** I ask a question like "How does authentication work?", **Then** I receive a structured answer with: explanation in plain language, code examples with file references, related information, and source citations
4. **Given** a valid question, **When** the answer is returned, **Then** all code references include file paths and line numbers (e.g., `src/auth/jwt.ts:45-67`)
5. **Given** a question about data models like "What database tables exist?", **When** the answer is returned, **Then** I see a list of tables with schemas, relationships, and ORM entity mappings
6. **Given** a question about APIs like "Show me all user management endpoints", **When** the answer is returned, **Then** I see REST/GraphQL endpoints with methods, paths, handlers, and authentication requirements
7. **Given** a question about external services like "What third-party services does this use?", **When** the answer is returned, **Then** I see a list of services (Stripe, AWS, SendGrid, etc.) with SDK usage locations and required environment variables
8. **Given** an answer is returned, **When** I review the response, **Then** I see a confidence indicator (e.g., "High confidence - Based on 3 sources from knowledge base") and citations linking to source documents

---

### User Story 5 - Detect Code Reusability During Implementation (Priority: P3)

As a developer implementing a new feature, I want the system to automatically suggest existing implementations I can reuse so that I avoid duplicating code and maintain architectural consistency.

**Why this priority**: This is valuable for code quality and consistency, but it's optional (soft prerequisite). Implementation can proceed without it, making it P3. It enhances development but isn't blocking for any critical workflows.

**Independent Test**: Can be tested by running `/speckitsmart.implement` with an index present, and verifying that before implementing each task, the system displays suggestions for existing implementations, utilities, patterns, and test examples to reuse.

**Acceptance Scenarios**:

1. **Given** no codebase index exists, **When** I run `/speckitsmart.implement`, **Then** the command displays a warning explaining that code reusability checks are disabled, lists the benefits I'm missing (40-60% code reuse, pattern detection, etc.), suggests building index, but continues with standard implementation mode
2. **Given** a valid index exists, **When** I run `/speckitsmart.implement`, **Then** the command displays a confirmation that code reusability checks are enabled and explains what will be checked for each task (existing implementations, utilities, patterns, test examples)
3. **Given** index is available and I'm implementing a task, **When** the system analyzes the task description, **Then** it runs a reusability check and displays suggestions for: existing implementations with similarity scores, reusable utilities and helpers, architecture patterns to follow, and test examples as templates
4. **Given** a high-similarity match is found (>90%), **When** the suggestion is displayed, **Then** the recommendation is marked as "HIGH MATCH - Reuse this instead of reimplementing" with file path, line number, and code preview
5. **Given** reusable utilities are found, **When** suggestions are displayed, **Then** I see file paths, exported functions, relevance scores, and recommendations for which operations to use them for
6. **Given** architecture patterns are detected, **When** suggestions are displayed, **Then** I see pattern names (e.g., "Middleware Pattern", "Repository Pattern"), example files following the pattern, and recommendations for how to structure new code consistently

---

### Edge Cases

- What happens when the index directory `.analysis/index/` exists but metadata.json is missing or corrupted?
  - System treats index as non-existent, displays error message, suggests running full index rebuild

- What happens when a file exceeds the maximum size limit (10MB) during indexing?
  - System skips the file, logs a warning in verbose mode, continues indexing other files, and includes skip count in final statistics

- What happens when a file has syntax errors that prevent AST parsing?
  - System attempts regex-based fallback extraction, logs warning if verbose mode enabled, continues with other files, and includes parse failure count in statistics

- What happens when a user runs incremental index update but no previous index exists?
  - System automatically falls back to full index build, displays a message explaining the fallback, and proceeds with full indexing

- What happens when a user runs `/speckitsmart.analyze-project` with a stale index (>7 days) and chooses not to update?
  - System proceeds with analysis using stale data, but includes warnings in the analysis report about potentially missing recent changes

- What happens when a command requires index but the user is in a CI/CD environment where indexing isn't practical?
  - User can set environment variable SPEC_KIT_SKIP_INDEX_CHECK=true to bypass prerequisite checks (documented for advanced use cases only)

- What happens when the system detects hardcoded secrets (API keys, passwords) during indexing?
  - System redacts sensitive patterns (API_KEY=..., PASSWORD=..., JWT tokens) before storing in index, logs redaction count in metadata

- What happens when `/speckitsmart.ask` receives a question that has no relevant information in the index?
  - System returns a message explaining no relevant results found, suggests checking if index is up to date, and optionally suggests alternative keywords

- What happens when multiple language versions exist in the codebase (e.g., TypeScript and JavaScript)?
  - System indexes all supported languages, tracks counts per language in statistics, and allows filtering by language in query results

- What happens when a user wants to exclude certain directories from indexing (e.g., generated code, vendor libs)?
  - User can pass `--exclude <pattern>` flag with glob patterns to skip directories, and the exclusions are stored in index metadata

## Requirements *(mandatory)*

### Functional Requirements

#### Core Indexing

- **FR-001**: System MUST provide `/speckitsmart.index` slash command that builds a searchable index of code structure, data models, API endpoints, external integrations, and dependencies
- **FR-002**: System MUST support indexing TypeScript, JavaScript, Python, Java, C#, and Go source files
- **FR-003**: System MUST extract classes, functions, interfaces, methods, and their relationships from source files using AST-based parsing with regex fallback
- **FR-004**: System MUST extract data models including database schemas (Prisma, SQL), ORM entities (TypeORM, Sequelize, Django, Hibernate), and type definitions
- **FR-005**: System MUST extract API endpoints including REST routes (Express, Fastify, FastAPI, Spring Boot), GraphQL resolvers, and WebSocket handlers
- **FR-006**: System MUST detect external API integrations including third-party SDKs (Stripe, AWS, SendGrid, Auth0), HTTP API calls, and required environment variables
- **FR-007**: System MUST build dependency graphs showing imports, exports, and function call relationships
- **FR-008**: System MUST store extracted data in JSON format at `.analysis/index/` with files: structure.json, data-models.json, api-endpoints.json, external-apis.json, dependencies.json, and metadata.json
- **FR-009**: System MUST support full index rebuild via `--full` flag
- **FR-010**: System MUST support incremental updates via `--incremental` flag that only re-indexes changed files based on MD5 hash comparison
- **FR-010a**: When `--incremental` flag is specified but no base index exists, system MUST automatically fallback to full index build mode and display explanation message: "No existing index found. Running full index build instead of incremental update."
- **FR-011**: System MUST allow users to specify target directory via `--path <dir>` flag to index specific subdirectories
- **FR-012**: System MUST allow users to filter by language via `--languages <list>` flag (comma-separated)
- **FR-013**: System MUST allow users to exclude patterns via `--exclude <pattern>` flag using glob syntax
- **FR-014**: System MUST provide verbose output via `--verbose` flag showing detailed progress and parse errors
- **FR-015**: System MUST redact sensitive data (API keys, passwords, JWT tokens) before storing in index
- **FR-016**: System MUST automatically add `.analysis/index/` to .gitignore if not already present

#### Prerequisite Checks

- **FR-017**: System MUST provide prerequisite check scripts (check-index-prerequisite.sh / Check-IndexPrerequisite.ps1) that verify index exists and return freshness metadata
- **FR-018**: System MUST provide optional check scripts (check-index-optional.sh / Check-IndexOptional.ps1) that warn if index missing but allow continuation
- **FR-019**: Prerequisite check scripts MUST return JSON with fields: index_exists (boolean), index_path (string), freshness (ISO 8601 timestamp from metadata.json), age_days (integer, calculated from freshness to current date), is_stale (boolean, true if age_days > 7), files_indexed (integer from metadata.statistics)
- **FR-020**: System MUST consider index stale if >7 days old
- **FR-021**: System MUST validate index integrity by checking for metadata.json presence and required fields

#### Analyze-Project Integration

- **FR-022**: `/speckitsmart.analyze-project` command MUST require codebase index as hard prerequisite (fail if missing)
- **FR-023**: Before analysis starts, system MUST run prerequisite check and stop with error if index not found
- **FR-024**: If index is stale (>7 days), system MUST display warning, recommend incremental update, and wait for user confirmation before proceeding
- **FR-025**: If index is fresh (<7 days), system MUST display confirmation message and proceed immediately
- **FR-026**: System MUST load pre-extracted data from index via load-index-for-analysis script instead of reading files manually
- **FR-027**: Loaded index data MUST include: code structure (classes, functions, entry points), data models (entities, schemas), API surface (endpoints, authentication), and external integrations (services, env vars)

#### DeepWiki Documentation Generation

- **FR-028**: System MUST provide `/speckitsmart.wiki` slash command that generates comprehensive documentation from codebase index
- **FR-029**: `/speckitsmart.wiki` MUST require index as hard prerequisite (fail if missing)
- **FR-030**: System MUST generate documentation in `.deepwiki/` directory with structure: index.md, overview.md, functional-summary.md, architecture/, modules/, api-reference/
- **FR-031**: System MUST generate 4-tier documentation: Tier 1 (overview), Tier 2 (functional summary), Tier 3 (architecture), Tier 4 (detailed per-module docs)
- **FR-032**: System MUST generate component diagrams, data flow diagrams, and dependency graphs in Mermaid format
- **FR-033**: System MUST allow users to specify tier subset via `--tiers <list>` flag (e.g., `--tiers 1,2` for quick overviews)
- **FR-034**: Generated documentation MUST include file paths and line numbers for all code references
- **FR-035**: Generated API reference MUST list all REST endpoints with methods, paths, handlers, request/response schemas, middleware, and authentication requirements
- **FR-036**: Generated API reference MUST list all GraphQL queries and mutations with resolvers, arguments, and return types
- **FR-037**: Generated data models section MUST document all database tables with schemas, columns, types, constraints, indexes, and relationships
- **FR-038**: Generated data models section MUST document all ORM entities with mappings to database tables

#### Knowledge Base Querying

- **FR-039**: System MUST provide `/speckitsmart.ask "<question>"` slash command for natural language queries
- **FR-040**: `/speckitsmart.ask` MUST require index as hard prerequisite (fail if missing)
- **FR-041**: If DeepWiki is missing, system MUST display warning that answers will be lower quality, suggest generating wiki, and ask for user confirmation to continue
- **FR-042**: System MUST return structured answers with: explanation in plain language, code examples with file references, related information, and source citations
- **FR-043**: All code references in answers MUST include file paths and line numbers (format: `file.ts:start-end`)
- **FR-044**: System MUST provide confidence indicator for answers (e.g., "High confidence - Based on N sources")
- **FR-045**: System MUST cite sources including .deepwiki documentation sections and index file references
- **FR-046**: System MUST support questions about: architecture/patterns, data models, API endpoints, external integrations, authentication flows, and business logic. Each category MUST be validated with representative test questions returning relevant answers with >80% accuracy.

#### Code Reusability Checks

- **FR-047**: System MUST provide optional code reusability checks during `/speckitsmart.implement` when index is available
- **FR-048**: If index missing during implementation, system MUST display warning explaining disabled features but continue with standard mode
- **FR-049**: If index available during implementation, system MUST display confirmation and explain what will be checked per task
- **FR-050**: System MUST provide find-reusable-code script that searches index for similar implementations, utilities, patterns, and test examples
- **FR-051**: For each implementation task, system MUST query index and return: existing implementations with similarity scores, reusable utilities with exports, architecture patterns with examples, and test examples as templates
- **FR-052**: System MUST mark high-similarity matches (>90%) with "HIGH MATCH" recommendation
- **FR-053**: Reusability suggestions MUST include file paths, line numbers, code previews, and actionable recommendations

#### Cross-Platform Support

- **FR-054**: System MUST provide both Bash scripts (.sh) and PowerShell scripts (.ps1) for all commands and utilities
- **FR-055**: Scripts MUST auto-detect OS and execute appropriate version (bash for Unix/Linux/macOS, PowerShell for Windows)
- **FR-056**: Scripts MUST support manual OS override via SPEC_KIT_PLATFORM environment variable (values: unix, windows, auto)
- **FR-057**: All JSON output MUST be consistently formatted across platforms for parsing compatibility

#### Performance & Quality

- **FR-058**: Index build MUST complete in <10 seconds for projects with <1K files, <60 seconds for 1K-10K files, <5 minutes for 10K-50K files
- **FR-059**: Incremental index updates MUST complete in <5 seconds for single file changes
- **FR-060**: System MUST provide progress indicators during indexing when --verbose flag is enabled
- **FR-061**: System MUST skip files exceeding 10MB size limit and log warnings
- **FR-062**: System MUST continue indexing if individual files fail to parse, log warnings, and report skip count in statistics
- **FR-063**: System MUST validate index structure on load and report corruption errors with clear recovery instructions

#### Index Version Management

- **FR-064**: System MUST validate index format version (metadata.version field) on load and compare against current tool version
- **FR-065**: When index version is incompatible with current tool version, system MUST display error message explaining incompatibility and recommend full index rebuild with `--full` flag
- **FR-066**: System MUST store tool version that created index in metadata.json (field: created_by_version)

### Key Entities *(include if feature involves data)*

- **Index**: Searchable representation of codebase stored in `.analysis/index/` directory containing structure.json (code elements), data-models.json (schemas/entities), api-endpoints.json (REST/GraphQL), external-apis.json (third-party services), dependencies.json (import graph), and metadata.json (statistics/freshness)

- **Code Structure**: Extracted representation of classes, functions, interfaces, and methods with properties including name, file path, line number, parameters, return types, decorators, and relationships (extends, implements, calls)

- **Data Model**: Extracted representation of database schemas (tables, columns, types, constraints) and ORM entities (entity name, table mapping, fields, decorators) with relationships (hasMany, belongsTo, hasOne, manyToMany)

- **API Endpoint**: Extracted representation of REST routes (method, path, handler, middleware, request/response schemas, authentication) and GraphQL resolvers (type, field, arguments, return type)

- **External Integration**: Detected usage of third-party services including service name, SDK package, version, API calls with file locations and line numbers, and required environment variables

- **Metadata**: Index freshness information including version, generated timestamp, index type (full/incremental), duration, and statistics (total files, indexed files, skipped files, classes, functions, interfaces, API endpoints, data models)

- **DeepWiki**: Auto-generated documentation in `.deepwiki/` directory with 4-tier structure: Tier 1 overview, Tier 2 functional summary, Tier 3 architecture diagrams, Tier 4 detailed module documentation with code references

- **Reusability Suggestion**: Recommendation for code reuse including existing implementation with similarity score, reusable utility with exports, architecture pattern with examples, or test template with relevance score

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Index builds in under 60 seconds for codebases with 1,000-10,000 files (90th percentile performance)
- **SC-002**: Incremental index updates complete in under 5 seconds for single file changes (95th percentile performance)
- **SC-003**: Index extraction achieves >95% completeness for source files (successfully indexes at least 95% of eligible files)
- **SC-004**: Reverse engineering with `/speckitsmart.analyze-project` completes 10x faster with index vs without (e.g., 2-5 minutes vs 20-50 minutes for 10K file codebase)
- **SC-005**: Code reusability checks during implementation detect 40-60% of duplicate implementations (measured by similarity score >80%)
- **SC-006**: AI token usage reduces by 80% when using index data vs reading full files (measured by token counts in analyze-project workflow)
- **SC-007**: Query response time for `/speckitsmart.ask` is under 5 seconds per question (95th percentile)
- **SC-008**: DeepWiki generation completes in under 2 minutes for typical projects (up to 10K files)
- **SC-009**: >95% of developers successfully build index on first attempt without errors (measured by success rate in user testing)
- **SC-010**: >90% of `/speckitsmart.ask` queries return relevant answers with high confidence (measured by user satisfaction ratings)
- **SC-011**: Index storage overhead is <1% of codebase size (measured by `.analysis/index/` directory size vs total project size)
- **SC-012**: Memory usage during indexing stays below 500MB for codebases with up to 50K files
- **SC-013**: Cross-platform compatibility: all commands work identically on Windows (PowerShell), macOS (bash), and Linux (bash) without modification
- **SC-014**: New developers onboard 50% faster when using DeepWiki documentation vs reading code manually (measured by time to first contribution)
- **SC-015**: False positive rate for reusability suggestions is <5% (measured by AI acceptance rate of high-match suggestions)

## Assumptions

1. **AST Parsing**: We assume tree-sitter libraries are available for supported languages (TypeScript, JavaScript, Python, Java, C#, Go). If not, regex-based fallback extraction is used.

2. **File System Access**: We assume the system has read access to all source files and write access to `.analysis/` directory. Permission errors will halt indexing with clear error messages.

3. **Git Repository**: We assume the project is a git repository for determining root directory. If not, current working directory is used as fallback.

4. **JSON Processing**: We assume `jq` (or equivalent JSON processor) is available for parsing JSON output. If not, scripts will fail with instructions to install jq.

5. **Language Detection**: We assume standard file extensions identify languages (.ts/.tsx = TypeScript, .js/.jsx = JavaScript, .py = Python, etc.). Custom extensions require --languages flag.

6. **Framework Detection**: We assume standard framework patterns (Express routes, Prisma models, TypeORM entities) can be detected via import statements and decorators.

7. **Environment Variables**: We assume environment variable names follow common patterns (UPPERCASE_WITH_UNDERSCORES) for detection. Non-standard naming may not be captured.

8. **Single Codebase**: We assume indexing operates on a single repository. Multi-repo indexing is out of scope for Phase 1.

9. **Local Execution**: We assume all indexing and analysis happens locally on developer machine. Cloud-based indexing is out of scope.

10. **Index Freshness**: We assume users will manually update index after significant code changes. Automatic real-time indexing is out of scope for Phase 1.

11. **Documentation Language**: We assume generated DeepWiki documentation is in English. Internationalization is out of scope.

12. **Binary Files**: We assume binary files (.jpg, .png, .pdf, executables) are skipped automatically. No binary analysis is performed.

13. **Large Files**: We assume files >10MB are edge cases and can be skipped with warnings. Configurable limits are available via `--max-file-size` flag.

14. **Semantic Search**: We assume Phase 1 uses keyword-based search for `/speckitsmart.ask`. Vector embeddings for semantic search are planned for Phase 2.

15. **Security**: We assume developers have appropriate access to view source code. Index does not implement additional access control beyond file system permissions.

## Constraints

1. **Technical Constraints**:
   - Index format uses JSON (not binary) for human readability, which limits compression
   - Regex-based parsing in Phase 1 may miss complex language constructs compared to full AST parsing
   - No real-time index updates; requires manual rebuild/incremental update after code changes
   - Keyword-based search may miss semantic relationships that vector embeddings would capture

2. **Performance Constraints**:
   - Index build time scales linearly with file count (no parallelization in Phase 1)
   - Maximum file size limit of 10MB prevents indexing of very large generated files
   - Memory usage increases with codebase size; may require batching for very large projects (>50K files)

3. **Platform Constraints**:
   - Requires bash 4.0+ for Unix/Linux/macOS or PowerShell 5.1+ for Windows
   - Requires jq or equivalent JSON processor for script output parsing
   - Requires git for repository root detection (fallback to pwd if not available)

4. **Language Support Constraints**:
   - Phase 1 supports TypeScript, JavaScript, Python, Java, C#, Go only
   - Rust, Ruby, PHP, Swift support planned for Phase 2
   - Language-specific features (decorators, macros) may not be fully captured

5. **Framework Support Constraints**:
   - REST framework detection supports Express, Fastify, NestJS (Node.js), FastAPI, Django (Python), Spring Boot (Java), ASP.NET (C#)
   - ORM detection supports TypeORM, Prisma, Sequelize (Node.js), Django ORM, SQLAlchemy (Python), Hibernate (Java), Entity Framework (C#)
   - GraphQL detection supports Apollo Server, GraphQL Yoga, Strawberry (Python), GraphQL Java
   - Custom or niche frameworks may not be automatically detected

6. **Integration Constraints**:
   - `/speckitsmart.analyze-project` hard dependency on index is non-negotiable (no fallback to manual file reading)
   - `/speckitsmart.wiki` and `/speckitsmart.ask` require index; no degraded mode available
   - `/speckitsmart.implement` code reusability is optional; continues without index but with warnings

7. **Security Constraints**:
   - Index files are stored locally only; no cloud upload or sharing features
   - Secret redaction uses pattern matching; may miss obfuscated secrets
   - No encryption of index files; relies on file system permissions for security

8. **User Experience Constraints**:
   - All commands must be run via Claude Code CLI; no standalone CLI tool in Phase 1
   - Error messages displayed in terminal only; no GUI notifications
   - Progress indicators require --verbose flag; default mode has minimal output

9. **Operational Constraints**:
   - `.analysis/index/` must be manually added to .gitignore (or automatically by system) to prevent accidental commits
   - Each developer must build index locally; no shared index across team
   - Index must be manually rebuilt after major refactoring; no automatic staleness detection triggers

10. **Documentation Constraints**:
    - DeepWiki documentation generated in markdown only; no HTML, PDF, or other formats in Phase 1
    - Diagrams use Mermaid syntax; require markdown renderer with Mermaid support for visualization
    - Documentation is static; no interactive features or live code previews

11. **Large Project Constraints**:
    - Single-threaded processing in Phase 1 limits performance for >50K files
    - Manual batching recommended: use `--path <subdirectory>` to index in segments
    - Expected build times: 50K files ~8-12 minutes, 100K files ~15-25 minutes
    - For very large projects (>100K files), consider subdirectory indexing with separate index outputs
    - See `large-projects-guide.md` for detailed strategies and workarounds
