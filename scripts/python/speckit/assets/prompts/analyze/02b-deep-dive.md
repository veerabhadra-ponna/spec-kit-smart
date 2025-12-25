---
stage: file_analysis_phase2
requires: 02a-category-scan complete
outputs: deep_patterns
version: 3.4.0
next: 02c-config-analysis.md
time_allocation: 40%
---

# Stage 2B: Deep Dive (Phase 2)

## Purpose

Focus on HIGH-PRIORITY areas with 60-80% file coverage. This is where detailed pattern extraction happens for authentication, database, and API layers.

**Time Allocation:** 40% of file analysis effort (largest phase)

---

## State Management

The CLI provides all context via template variables. **Do not read state.json directly.**

**Available template variables:**

- `{project_path}`, `{analysis_dir}`, `{scope}`, `{context}`
- `{data_dir}` - Data folder for JSON files (`{analysis_dir}/data/`)
- `{reports_dir}` - Reports folder for MD files (`{analysis_dir}/reports/`)
- `{concern_type}`, `{current_impl}`, `{target_impl}` (Scope B)

**CLI Utility Commands:**

- `speckitadv write-data <filename> --stage=<stage-id> --content '<json>'` - Write JSON to data/ folder (tracks artifacts)

---

## Pre-Check: Verify Previous Substage

1. Verify `{data_dir}/category-patterns.json` exists (from Phase 1)
2. Load category patterns for priority determination

**IF not complete:** STOP - Return to 02a-category-scan

---

## Priority Areas

| Priority | Area | Target Coverage | Rationale |
|----------|------|-----------------|-----------|
| **P1** | Authentication/Security | 80% | Critical for security assessment |
| **P2** | Database Access | 80% | Understand data layer completely |
| **P3** | API Endpoints | 70% | Map complete API surface |
| **P4** | Core Business Logic | 60% | Understand key workflows |

---

## Step 1: Authentication/Security Deep Dive (P1)

---
⏸️ **[STOP: DEEP_DIVE_AUTH]**

Analyze ALL security-related files (80% coverage minimum):

**Files to Analyze:**
- Security configuration files
- Authentication controllers/handlers
- Authorization filters/middleware
- Token providers/managers
- Password utilities
- RBAC/Permission implementations

**Extract for EACH file:**

1. **Authentication Flow:**
   - Registration process
   - Login mechanism
   - Token generation (JWT/Session)
   - Token refresh logic
   - Logout handling

2. **User Storage:**
   - Database table/collection
   - External provider (LDAP, OAuth)
   - User schema/fields

3. **Password Handling:**
   - Hashing algorithm (bcrypt, scrypt, argon2)
   - Salt strategy
   - Password requirements

4. **Token Configuration:**
   - Token type (JWT, opaque, session)
   - Algorithm (HS256, RS256)
   - Expiration settings
   - Refresh mechanism

5. **Authorization:**
   - Permission model (RBAC, ABAC, ACL)
   - Role definitions
   - Permission checks

6. **Security Issues:**
   - Missing validations
   - Hardcoded secrets
   - Weak algorithms
   - Missing rate limiting

**Progress Output (every 5 files):**

```text
[Phase 2 - Deep Dive: Authentication]
✓ 5/{total} security files analyzed
✓ 10/{total} security files analyzed
...

```

**Output Format:**

```text
Authentication System Analysis:

Type: {Custom JWT | OAuth 2.0 | Session-based | etc}
User Storage: {database table | LDAP | external}
Password Hashing: {algorithm} (cost factor: {n})
Token: {JWT with {algo}}, {expiration} expiration
Refresh: {mechanism} ({TTL})
Authorization: {RBAC | ABAC} ({role_count} roles)

Security Issues Found:
  🔴 HIGH: {issue} (file:line)
  🟡 MEDIUM: {issue} (file:line)
  🟢 LOW: {issue} (file:line)

Coverage: {analyzed}/{total} files ({percentage}%)

```

---

## Step 2: Database Layer Deep Dive (P2)

---
⏸️ **[STOP: DEEP_DIVE_DATABASE]**

Analyze ALL database-related files (80% coverage minimum):

**Files to Analyze:**
- Entity/Model definitions
- Repository/DAO implementations
- Migration files
- Database configurations
- Query builders

**Extract for EACH entity:**

1. **Entity Definition:**
   - Table/collection name
   - Primary key strategy
   - Fields with types

2. **Relationships:**
   - OneToOne, OneToMany, ManyToMany
   - Cascade behaviors
   - Orphan removal
   - Lazy vs Eager loading

3. **Constraints:**
   - NOT NULL fields
   - UNIQUE constraints
   - Foreign keys
   - Check constraints

4. **Queries:**
   - Native SQL queries (count)
   - Complex JPA/ORM queries
   - Query complexity rating

5. **Performance Issues:**
   - N+1 query patterns
   - Missing indexes
   - Eager loading overuse
   - Unbounded queries

**Progress Output (every 5 files):**

```text
[Phase 2 - Deep Dive: Database]
✓ 5/{total} database files analyzed
✓ 10/{total} database files analyzed
...

```

**Output Format:**

```text
Database Layer Analysis:

ORM: {Hibernate/JPA | Sequelize | Prisma | etc}
Database: {PostgreSQL | MySQL | MongoDB | etc}
Entities: {count}
Relationships: {count}
Native Queries: {count} (complexity: {rating})

Entity Summary:
  {Entity1}: {field_count} fields, {relationship_count} relationships
  {Entity2}: {field_count} fields, {relationship_count} relationships
  ...

Performance Issues Found:
  🔴 HIGH: N+1 in {file:line}
  🟡 MEDIUM: Missing index on {table.column}
  🟢 LOW: Eager loading in {file:line}

Migrations: {tool} ({count} migration files)
Coverage: {analyzed}/{total} files ({percentage}%)

```

---

## Step 3: API Endpoints Deep Dive (P3)

---
⏸️ **[STOP: DEEP_DIVE_API]**

Analyze ALL API endpoint files (70% coverage minimum):

**Files to Analyze:**
- Controller classes
- Route definitions
- Request handlers
- API middleware

**Extract for EACH endpoint:**

1. **Endpoint Definition:**
   - HTTP method (GET, POST, PUT, DELETE, PATCH)
   - Path pattern
   - Purpose/description

2. **Request/Response:**
   - Request DTO/body
   - Query parameters
   - Path parameters
   - Response DTO

3. **Authentication:**
   - Required (Yes/No)
   - Auth type (Bearer, API Key, Session)
   - Roles/permissions required

4. **Validation:**
   - Input validation rules
   - Error responses

5. **API Issues:**
   - Missing authentication
   - Missing validation
   - Inconsistent responses
   - Missing rate limiting

**Progress Output (every 10 endpoints):**

```text
[Phase 2 - Deep Dive: API Endpoints]
✓ 10/{total} endpoints documented
✓ 20/{total} endpoints documented
...

```

**Output Format:**

```text
API Surface Analysis:

Style: {REST | GraphQL | RPC | Mixed}
Total Endpoints: {count}
Versioning: {URI | Header | None}
Documentation: {OpenAPI | Swagger | None}

Endpoints by Category:
  Authentication: {count} endpoints
  Users: {count} endpoints
  {Resource}: {count} endpoints
  ...

Endpoint Sample:
  {METHOD} {path} - {purpose}
    Auth: {required/optional} ({roles})
    Request: {DTO or params}
    Response: {DTO}

API Issues Found:
  🔴 HIGH: {issue} (file:line)
  🟡 MEDIUM: {issue} (file:line)

Coverage: {analyzed}/{total} files ({percentage}%)

```

---

## Step 4: Core Business Logic Deep Dive (P4)

---
⏸️ **[STOP: DEEP_DIVE_BUSINESS]**

Analyze key business logic files (60% coverage minimum):

**Focus Areas:**
- Critical business workflows
- Complex algorithms
- State machines
- Business rules
- Integration orchestration

**Extract:**

1. **Key Workflows:**
   - Workflow name
   - Steps/stages
   - Decision points
   - Error handling

2. **Business Rules:**
   - Rule description
   - Implementation location
   - Dependencies

3. **Integrations:**
   - External services called
   - Message queues used
   - Event publishing

**Output Format:**

```text
Business Logic Analysis:

Key Workflows: {count}
  {Workflow1}: {step_count} steps, complexity: {rating}
  {Workflow2}: {step_count} steps, complexity: {rating}

Business Rules: {count}
  {Rule1}: {description} (file:line)
  {Rule2}: {description} (file:line)

External Integrations: {count}
  {Integration1}: {purpose} (file:line)
  {Integration2}: {purpose} (file:line)

Coverage: {analyzed}/{total} files ({percentage}%)

```

---

## Step 5: Compile Deep Dive Results

Merge all deep dive findings:

```json
{
  "deep_dive": {
    "authentication": {
      "type": "{mechanism}",
      "user_storage": "{type}",
      "password_hashing": "{algorithm}",
      "token": {
        "type": "{JWT/session/etc}",
        "algorithm": "{HS256/RS256/etc}",
        "expiration": "{duration}"
      },
      "authorization": "{RBAC/ABAC}",
      "roles": ["{list}"],
      "issues": [
        {"severity": "HIGH", "issue": "{description}", "location": "{file:line}"}
      ],
      "coverage": "{percentage}%"
    },
    "database": {
      "orm": "{framework}",
      "engine": "{database}",
      "entities": {count},
      "relationships": {count},
      "native_queries": {count},
      "issues": [
        {"severity": "HIGH", "issue": "{description}", "location": "{file:line}"}
      ],
      "coverage": "{percentage}%"
    },
    "api": {
      "style": "{REST/GraphQL}",
      "endpoints": {count},
      "versioning": "{strategy}",
      "auth_required": "{percentage}%",
      "issues": [
        {"severity": "HIGH", "issue": "{description}", "location": "{file:line}"}
      ],
      "coverage": "{percentage}%"
    },
    "business_logic": {
      "workflows": {count},
      "rules": {count},
      "integrations": {count},
      "coverage": "{percentage}%"
    }
  }
}

```

---

## Output Summary

```text
═══════════════════════════════════════════════════════════
  SUBSTAGE COMPLETE: 02b-deep-dive (Phase 2)

  Time Used: 40% allocation

  Coverage Achieved:
    Authentication: {percentage}% (target: 80%)
    Database: {percentage}% (target: 80%)
    API: {percentage}% (target: 70%)
    Business Logic: {percentage}% (target: 60%)

  Issues Found:
    🔴 HIGH: {count}
    🟡 MEDIUM: {count}
    🟢 LOW: {count}

  Proceeding to Phase 3: Configuration Analysis
═══════════════════════════════════════════════════════════

```

---

## Next Substage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
