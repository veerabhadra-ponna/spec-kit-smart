# Codebase Indexing - Functional Specification

**Version:** 1.0.0
**Status:** Draft
**Last Updated:** 2025-01-15
**Author:** Spec Kit Smart Team

---

## Executive Summary

Codebase indexing is a foundational feature that creates a searchable, structured representation of a codebase to enable intelligent code analysis, reverse engineering, and implementation assistance. This feature significantly improves developer productivity by providing fast semantic search, code reusability detection, and comprehensive codebase understanding.

**Key Benefits:**
- **10x faster** reverse engineering and analysis
- **40-60% code reuse** through automatic duplicate detection
- **80% reduction** in AI token usage
- **Better accuracy** through AST-based understanding vs regex patterns

---

## 1. Overview

### 1.1 Purpose

The codebase indexing system extracts and organizes information from source code into a queryable index that enables:

1. **Fast Code Intelligence**: Semantic search across entire codebase
2. **Reverse Engineering**: Automatic extraction of architecture, data models, and APIs
3. **Code Reusability**: Detection of existing implementations to prevent duplication
4. **Documentation Generation**: Auto-generation of comprehensive documentation (DeepWiki)
5. **AI Assistance**: Providing grounded context to AI agents for better code generation

### 1.2 Scope

**In Scope:**
- Source code structure indexing (classes, functions, methods, interfaces)
- Data model indexing (database schemas, ORM entities, type definitions)
- API endpoint indexing (REST, GraphQL, WebSocket)
- External API usage indexing (third-party services, webhooks)
- Dependency graph generation (imports, exports, function calls)
- Multi-language support (TypeScript, JavaScript, Python, Java, C#, Go)

**Out of Scope (Phase 1):**
- Real-time indexing (incremental updates supported, but not live)
- Semantic code embeddings (planned for Phase 2)
- Runtime behavior analysis
- Performance profiling data

### 1.3 Target Users

- **Software Engineers**: Reverse engineering legacy code, implementing new features
- **Tech Leads**: Understanding system architecture, planning migrations
- **AI Coding Assistants**: Claude Code, GitHub Copilot, Cursor, etc.

---

## 2. User Stories

### 2.1 Reverse Engineering

**As a** developer joining a new project
**I want to** quickly understand the codebase structure
**So that** I can contribute effectively without spending weeks reading code

**Acceptance Criteria:**
- Index builds in <5 minutes for projects with <10K files
- Index extracts all classes, functions, and their relationships
- Index identifies data models, API endpoints, and external integrations
- Results are searchable and browsable

---

### 2.2 Code Reusability

**As a** developer implementing a new feature
**I want to** find existing code that I can reuse
**So that** I don't duplicate implementations and maintain consistency

**Acceptance Criteria:**
- Index identifies similar implementations with >80% similarity
- Index suggests reusable utilities and helpers
- Index shows architecture patterns to follow
- Results include file paths and line numbers

---

### 2.3 Documentation Generation

**As a** tech lead
**I want to** automatically generate comprehensive documentation
**So that** new team members can onboard faster

**Acceptance Criteria:**
- DeepWiki generates 4-tier documentation automatically
- Documentation includes architecture diagrams
- Documentation stays up-to-date with code changes
- Documentation is searchable via Q&A interface

---

### 2.4 API Discovery

**As a** developer integrating with an existing system
**I want to** discover all available API endpoints
**So that** I know what APIs exist and how to use them

**Acceptance Criteria:**
- Index lists all REST endpoints with methods, paths, and schemas
- Index lists all GraphQL queries and mutations
- Index shows request/response formats
- Index identifies authentication requirements

---

## 3. Feature Specifications

### 3.1 Command: `/speckitsmart.index`

**Purpose:** Build or rebuild the codebase index

#### 3.1.1 Basic Usage

```bash
# First time - full index build
/speckitsmart.index

# Update after code changes - incremental
/speckitsmart.index --incremental

# Index specific directory
/speckitsmart.index --path src/

# Index only TypeScript and Python
/speckitsmart.index --languages typescript,python

# Verbose output for debugging
/speckitsmart.index --verbose
```

#### 3.1.2 Arguments

| Argument | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `--full` | flag | No | Force full rebuild | `--full` |
| `--incremental` | flag | No | Update changed files only | `--incremental` |
| `--path <dir>` | string | No | Index specific directory | `--path src/` |
| `--languages <list>` | string | No | Comma-separated languages | `--languages typescript,python` |
| `--exclude <pattern>` | string | No | Exclude glob patterns | `--exclude tests/**` |
| `--verbose` | flag | No | Detailed progress output | `--verbose` |

#### 3.1.3 Output

**Success Output:**

```json
{
  "success": true,
  "index_path": ".analysis/index",
  "statistics": {
    "total_files": 247,
    "indexed_files": 189,
    "skipped_files": 58,
    "total_classes": 45,
    "total_functions": 312,
    "total_interfaces": 28,
    "total_api_endpoints": 34,
    "total_data_models": 23
  },
  "languages": {
    "TypeScript": 145,
    "Python": 23,
    "JavaScript": 21
  },
  "duration_seconds": 12.4
}
```

**User-Facing Display:**

```
✓ Index built successfully!

📊 Statistics:
  - Files indexed: 189/247
  - Classes: 45
  - Functions: 312
  - Interfaces: 28
  - API Endpoints: 34
  - Data Models: 23

🔤 Languages:
  - TypeScript: 145 files
  - Python: 23 files
  - JavaScript: 21 files

⏱️ Duration: 12.4 seconds
📁 Location: .analysis/index

🎯 Next: Run /speckitsmart.analyze-project
```

#### 3.1.4 Performance Requirements

| Codebase Size | Build Time | Update Time |
|---------------|------------|-------------|
| Small (<1K files) | <10 seconds | <2 seconds |
| Medium (1K-10K) | <60 seconds | <5 seconds |
| Large (10K-50K) | <5 minutes | <20 seconds |
| Very Large (>50K) | <30 minutes | <60 seconds |

#### 3.1.5 Error Handling

| Error | User Message | Action |
|-------|--------------|--------|
| No source files found | "No source files found. Check path and language filters." | Exit with code 1 |
| Permission denied | "Cannot write to .analysis/ directory. Check permissions." | Exit with code 1 |
| Out of memory | "Insufficient memory. Try --path to limit scope or --batch-size." | Exit with code 1 |
| Parser errors | "Warning: N files failed to parse. Use --verbose for details." | Continue, show warnings |

---

### 3.2 Command: `/speckitsmart.wiki`

**Purpose:** Generate comprehensive documentation (DeepWiki) from index

**Prerequisites:** Requires index (must run `/speckitsmart.index` first)

#### 3.2.1 Basic Usage

```bash
# Generate all documentation tiers
/speckitsmart.wiki

# Generate specific tiers only
/speckitsmart.wiki --tiers 1,2

# Generate with diagrams
/speckitsmart.wiki --diagrams

# Export to HTML
/speckitsmart.wiki --format html
```

#### 3.2.2 Output Structure

```
.deepwiki/
├── index.md                    # Landing page
├── overview.md                 # Tier 1: What is this repo?
├── functional-summary.md       # Tier 2: Problems it solves
├── architecture/
│   ├── quick-start.md          # Tier 3: High-level architecture
│   ├── detailed.md             # Tier 4: Deep dive
│   └── diagrams/
│       ├── components.mmd      # Component diagram (Mermaid)
│       ├── dataflow.mmd        # Data flow diagram
│       └── dependencies.mmd    # Dependency graph
├── modules/
│   ├── authentication.md       # Per-module documentation
│   ├── user-management.md
│   └── payment-processing.md
└── api-reference/
    ├── rest-endpoints.md       # All REST APIs
    ├── graphql-schema.md       # GraphQL schema
    └── data-models.md          # Database schemas
```

#### 3.2.3 Prerequisite Check

**If index not found:**

```
❌ ERROR: Codebase index required

DeepWiki generation requires a codebase index.

🔧 Solution:
Run this command first:
  /speckitsmart.index

Then re-run:
  /speckitsmart.wiki
```

---

### 3.3 Command: `/speckitsmart.ask`

**Purpose:** Query codebase knowledge base using natural language

**Prerequisites:** Requires index and optionally DeepWiki

#### 3.3.1 Basic Usage

```bash
# Ask a question
/speckitsmart.ask "How does authentication work?"

# Ask about data models
/speckitsmart.ask "What database tables exist?"

# Ask about APIs
/speckitsmart.ask "Show me all API endpoints for user management"

# Ask about external integrations
/speckitsmart.ask "What third-party services does this use?"
```

#### 3.3.2 Response Format

```markdown
## Answer

Authentication works in 3 phases:

1. **JWT Token Validation**: The system validates JWT tokens using
   the `validateJWT` function in `src/auth/jwt.ts`. It checks token
   signature, expiration, and issuer.

2. **User Lookup**: After validation, the user is fetched from the
   database using the `UserRepository.findById` method.

3. **Permission Check**: Finally, the user's permissions are verified
   against the required role using the `checkPermissions` middleware.

### Code Example
```typescript
// From src/auth/jwt.ts:45-67
export async function validateJWT(token: string) {
  const payload = jwt.verify(token, process.env.JWT_SECRET);
  return payload;
}
```

### Related Information

- Authentication uses JWT with 24-hour expiration
- Refresh tokens stored in Redis cache
- Support for OAuth2 providers (Google, GitHub)

### Sources

- .deepwiki/modules/authentication.md (Section: JWT Flow)
- src/auth/jwt.ts:45-120
- src/middleware/authenticate.ts:12-45

✓ High confidence - Based on 3 sources from knowledge base

```

#### 3.3.3 Prerequisite Check

**If index not found:**
```

❌ ERROR: Index required

The ask command requires a codebase index to answer questions.

🔧 Solution:
1. Build index: /speckitsmart.index
2. (Optional) Generate docs: /speckitsmart.wiki
3. Then ask questions: /speckitsmart.ask "your question"

```

**If index found but DeepWiki missing:**
```

⚠️ WARNING: DeepWiki not generated

Answers will be based on code index only (lower quality).

💡 For better answers, run:
  /speckitsmart.wiki

Continue anyway? [Y/n]

```

---

### 3.4 Integration: `/speckitsmart.analyze-project`

**Purpose:** Reverse engineer legacy codebases

**Prerequisites:** **REQUIRES** index (hard requirement)

#### 3.4.1 Prerequisite Check

**Before analysis starts:**

**If index not found:**
```

❌ ERROR: Codebase index not found

This command requires a codebase index for efficient reverse engineering.

🔧 Solution:
Run this command first to build the index:
  /speckitsmart.index

Why indexing is required:
- 10x faster analysis (uses index instead of reading every file)
- 80% token reduction (pre-extracted structure)
- Better accuracy (AST-based vs regex)

Estimated time to build index: 30-60 seconds (one-time cost)

After indexing completes, re-run:
  /speckitsmart.analyze-project

```

**STOP execution. DO NOT proceed without index.**

**If index is stale (>7 days old):**
```

⚠️ WARNING: Index is stale (last updated 12 days ago)

Analysis will continue, but results may not reflect recent code changes.

Recommendation: Update index with:
  /speckitsmart.index --incremental

This will take ~5-10 seconds and ensure accurate analysis.

Continue anyway? (Press Enter to continue, Ctrl+C to abort)

```

Wait for user confirmation.

**If index is fresh:**
```

✓ Index found and fresh (updated 2 hours ago)
✓ 189 files indexed

Proceeding with reverse engineering analysis...

```

#### 3.4.2 Enhanced Analysis with Index

**Instead of reading files manually, load pre-extracted data:**

```json
{
  "architecture": {
    "total_modules": 23,
    "entry_points": ["src/index.ts", "src/cli.ts"],
    "patterns": ["Repository Pattern", "Service Layer", "MVC"]
  },
  "data_models": {
    "total_entities": 23,
    "entities": [
      {"name": "User", "table": "users", "fields": 8},
      {"name": "Order", "table": "orders", "fields": 12}
    ]
  },
  "api_surface": {
    "total_endpoints": 45,
    "rest": 38,
    "graphql": 7,
    "authentication": "JWT"
  },
  "external_integrations": {
    "services": ["Stripe", "AWS S3", "SendGrid", "Auth0"],
    "required_env_vars": 12
  }
}
```

**Benefits:**
- Analysis completes in ~2 minutes vs 20+ minutes
- More accurate (AST-based vs regex)
- Comprehensive (includes data models and APIs)

---

### 3.5 Integration: `/speckitsmart.implement`

**Purpose:** Execute implementation tasks

**Prerequisites:** Index is **OPTIONAL** (but highly recommended)

#### 3.5.1 Optional Check

**If index not found:**

```
⚠️ Codebase index not available

You can continue implementation, but you'll miss these benefits:
  - 40-60% code reuse (avoid duplicate implementations)
  - Automatic detection of existing utilities
  - Consistent architecture patterns
  - 80% token reduction in AI queries

💡 To enable code reusability features:
   1. Run: /speckitsmart.index (takes ~30-60 seconds)
   2. Re-run: /speckitsmart.implement

⏭️ Proceeding without index...
```

**Continue with standard implementation (no reusability checks).**

**If index found:**

```
✓ Index available (189 files indexed)
✓ Code reusability checks enabled

For each task, I'll check for:
  - Existing implementations to reuse
  - Utilities and helpers
  - Architecture patterns to follow
  - Test examples
```

**Proceed with enhanced implementation (with reusability checks).**

#### 3.5.2 Reusability Checks

**For each task in tasks.md, before implementing:**

1. Query index for similar implementations
2. Query index for reusable utilities
3. Query index for architecture patterns
4. Display suggestions to developer/AI

**Example:**

**Task:** "Implement JWT token validation"

**Index Query Results:**

```json
{
  "existing_implementations": [
    {
      "file": "src/auth/jwt.ts",
      "function": "validateJWT",
      "similarity": 0.92,
      "recommendation": "⚠️ REUSE THIS - Don't reimplement"
    }
  ],
  "reusable_utilities": [
    {
      "file": "src/utils/crypto.ts",
      "exports": ["hashPassword", "verifyPassword"],
      "recommendation": "Use these for password operations"
    }
  ],
  "architecture_patterns": [
    {
      "pattern": "Middleware Pattern",
      "examples": ["src/middleware/authenticate.ts"],
      "recommendation": "Follow this pattern for auth middleware"
    }
  ]
}
```

**AI Action:**

```typescript
// ✅ GOOD: Reuse existing (from index suggestion)
import { validateJWT } from '@/auth/jwt';

export const authMiddleware = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  const payload = await validateJWT(token); // Reusing existing
  req.user = payload;
  next();
};

// ❌ BAD: Duplicate implementation
export const authMiddleware = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  const payload = jwt.verify(token, secret); // Reimplementing!
  req.user = payload;
  next();
};
```

---

## 4. Index Data Model

### 4.1 Code Structure (`structure.json`)

```json
{
  "version": "1.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "classes": [
    {
      "name": "UserService",
      "file": "src/services/user.ts",
      "line": 12,
      "methods": ["create", "findById", "update", "delete"],
      "dependencies": ["UserRepository", "EmailService"]
    }
  ],
  "functions": [
    {
      "name": "validateEmail",
      "file": "src/utils/validation.ts",
      "line": 45,
      "parameters": ["email: string"],
      "return_type": "boolean"
    }
  ],
  "interfaces": [
    {
      "name": "User",
      "file": "src/types/user.ts",
      "properties": ["id", "email", "password", "role"]
    }
  ]
}
```

### 4.2 Data Models (`data-models.json`)

```json
{
  "version": "1.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "database_schemas": [
    {
      "table": "users",
      "file": "prisma/schema.prisma",
      "columns": [
        {"name": "id", "type": "uuid", "primary_key": true},
        {"name": "email", "type": "string", "unique": true},
        {"name": "password_hash", "type": "string"},
        {"name": "created_at", "type": "timestamp"}
      ],
      "indexes": [{"columns": ["email"], "unique": true}],
      "relationships": [
        {"type": "hasMany", "target": "orders", "foreign_key": "user_id"}
      ]
    }
  ],
  "orm_entities": [
    {
      "entity": "User",
      "file": "src/entities/User.ts",
      "orm": "typeorm",
      "table": "users",
      "fields": [
        {"name": "id", "type": "number", "decorators": ["PrimaryGeneratedColumn"]},
        {"name": "email", "type": "string", "decorators": ["Column", "IsEmail"]}
      ]
    }
  ],
  "type_definitions": [
    {
      "name": "UserDTO",
      "file": "src/types/user.ts",
      "kind": "interface",
      "properties": [
        {"name": "id", "type": "string"},
        {"name": "email", "type": "string"}
      ]
    }
  ]
}
```

### 4.3 API Endpoints (`api-endpoints.json`)

```json
{
  "version": "1.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "rest_endpoints": [
    {
      "method": "POST",
      "path": "/api/users",
      "file": "src/routes/users.ts",
      "handler": "createUser",
      "middleware": ["authenticate", "validateBody"],
      "request_schema": {
        "body": {"email": "string", "password": "string"}
      },
      "response_schema": {
        "200": {"id": "string", "email": "string"},
        "400": {"error": "string"}
      },
      "authentication": "JWT"
    }
  ],
  "graphql_resolvers": [
    {
      "type": "Query",
      "field": "user",
      "file": "src/graphql/resolvers/user.ts",
      "arguments": [{"name": "id", "type": "ID"}],
      "return_type": "User"
    }
  ]
}
```

### 4.4 External APIs (`external-apis.json`)

```json
{
  "version": "1.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "third_party_services": [
    {
      "service": "Stripe",
      "file": "src/services/payment.ts",
      "sdk": "stripe",
      "version": "^12.0.0",
      "api_calls": [
        {
          "method": "stripe.customers.create",
          "file": "src/services/payment.ts",
          "line": 45,
          "purpose": "Create customer for payment"
        }
      ],
      "env_vars": ["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"]
    }
  ],
  "http_api_calls": [
    {
      "method": "POST",
      "url": "https://api.sendgrid.com/v3/mail/send",
      "file": "src/services/email.ts",
      "library": "axios",
      "purpose": "Send transactional email"
    }
  ],
  "environment_variables": [
    {
      "name": "STRIPE_SECRET_KEY",
      "required": true,
      "used_in": ["src/services/payment.ts"]
    }
  ]
}
```

---

## 5. Non-Functional Requirements

### 5.1 Performance

- **Index build time**: <1 minute for 10K files (90th percentile)
- **Query latency**: <100ms for semantic search (95th percentile)
- **Memory usage**: <500MB for indexing 50K files
- **Storage overhead**: <1% of codebase size

### 5.2 Reliability

- **Index freshness detection**: Warn if >7 days old
- **Graceful degradation**: Commands work without index (with warnings)
- **Error recovery**: Resume from last checkpoint if indexing fails
- **Data integrity**: Validate index structure on load

### 5.3 Usability

- **Clear error messages**: Tell users exactly what to do
- **Progress indicators**: Show indexing progress in verbose mode
- **Helpful warnings**: Explain benefits when index missing
- **Sensible defaults**: Intelligent behavior without arguments

### 5.4 Security

- **No secrets in index**: Redact API keys, passwords
- **Local-only**: Index never leaves developer machine
- **Gitignore by default**: Add `.analysis/index/` to .gitignore
- **Permission checks**: Verify read/write access before indexing

### 5.5 Compatibility

- **Cross-platform**: Works on Windows, macOS, Linux
- **Multi-language**: TypeScript, JavaScript, Python, Java, C#, Go
- **Version control**: Index works with Git, SVN, Mercurial
- **IDE agnostic**: Works with all AI coding assistants

---

## 6. Success Metrics

### 6.1 Adoption Metrics

- **Index usage rate**: >80% of users build index before analysis
- **Reusability improvement**: 40-60% reduction in duplicate code
- **Time to first contribution**: 50% faster for new developers

### 6.2 Performance Metrics

- **Analysis speed**: 10x faster with index vs without
- **Token efficiency**: 80% reduction in AI token usage
- **Query accuracy**: >90% of ask queries return relevant results

### 6.3 Quality Metrics

- **Index completeness**: >95% of source files successfully indexed
- **False positive rate**: <5% for reusability suggestions
- **Documentation coverage**: 100% of modules documented in DeepWiki

---

## 7. Future Enhancements

### 7.1 Phase 2 (Planned)

- **Semantic embeddings**: Vector search for better semantic matching
- **Real-time updates**: Live index updates on file save
- **Custom extractors**: Plugin system for custom code patterns
- **Index sharing**: Export/import indexes for team collaboration

### 7.2 Phase 3 (Exploratory)

- **Multi-repo indexing**: Index across multiple repositories
- **Runtime analysis**: Include runtime behavior data
- **ML-based suggestions**: Learn from developer decisions
- **Visual code exploration**: Interactive graph visualization

---

## 8. Appendices

### 8.1 Supported Languages

| Language | Parser | Status | Notes |
|----------|--------|--------|-------|
| TypeScript | tree-sitter | ✅ Full | Classes, interfaces, types |
| JavaScript | tree-sitter | ✅ Full | ES6+ syntax |
| Python | tree-sitter | ✅ Full | Classes, functions, decorators |
| Java | tree-sitter | ✅ Full | Classes, interfaces, annotations |
| C# | tree-sitter | ✅ Full | Classes, interfaces, LINQ |
| Go | tree-sitter | ✅ Full | Structs, interfaces, methods |
| Rust | tree-sitter | 🔄 Partial | Structs, traits (Phase 2) |

### 8.2 Supported Frameworks

**ORM Detection:**
- TypeORM, Prisma, Sequelize (TypeScript/JavaScript)
- Django ORM, SQLAlchemy (Python)
- Hibernate, JPA (Java)
- Entity Framework (C#)

**API Framework Detection:**
- Express, Fastify, NestJS (Node.js)
- FastAPI, Django REST (Python)
- Spring Boot (Java)
- ASP.NET Core (C#)

**GraphQL Detection:**
- Apollo Server, GraphQL Yoga
- Strawberry (Python)
- GraphQL Java

### 8.3 File Size Limits

- **Maximum file size**: 10MB (configurable)
- **Maximum line length**: 10,000 characters
- **Maximum depth**: 1,000 levels (nested structures)

Files exceeding limits are skipped with warnings.

---

## 9. Glossary

- **Index**: Structured, searchable representation of codebase
- **AST**: Abstract Syntax Tree - parsed code structure
- **DeepWiki**: Auto-generated comprehensive documentation
- **Semantic Search**: Search by meaning, not just keywords
- **Code Reusability**: Finding and using existing code
- **Prerequisite Check**: Validation that required data exists

---

**End of Functional Specification**
