---
stage: technical_spec_legacy
requires: functional-spec-target complete
condition: state.analysis_scope == "A"
outputs: technical_spec_legacy_complete
version: 3.1.0
next: 06c2-technical-spec-target.md
---

# Stage 6C1: Technical Specification - Legacy System

## Purpose

Generate technical specification documenting HOW the LEGACY/EXISTING system is built. This captures the current architecture, technology stack, and implementation patterns before modernization.

---

## Pre-Check

1. Read `{analysis_dir}/state.json`
2. Confirm `functional_spec_target_complete` = true
3. Confirm `analysis_scope` = "A"

**IF not complete:** STOP - Return to 06b-functional-spec-target.md

---

## Source of Truth

**Use ONLY these sources:**
- `{reports_dir}/analysis-report.md` Phase 2 (Codebase Analysis)
- `{data_dir}/tech-stack.json` (detected technologies)
- `{data_dir}/category-patterns.json` (code patterns)
- `{data_dir}/deep-dive-patterns.json` (detailed patterns)
- `{data_dir}/config-analysis.json` (configuration details)

**Template:**

{{include:technical-spec-template.md}}

---

## Content Rules

| Rule | Requirement |
|------|-------------|
| Technology | Document as-implemented (current state) |
| References | Every component MUST include `file:line` notation |
| Tense | Present tense ("The system uses...", "Authentication is handled by...") |
| Scope | Document what EXISTS, not recommendations |
| Diagrams | Use Mermaid for all architecture diagrams |

**Forbidden:** Do NOT include modernization preferences, target stack, or future state.

---

## Chunk 1: Introduction + Architecture Overview

Generate Sections 1 and 2.

---
⏸️ **[STOP: GENERATE_CHUNK_1]**

### Section 1: Introduction

- Document purpose and scope
- Technical audience
- System overview

### Section 2: Architecture Overview

```markdown
## 2. Architecture Overview

### 2.1 System Context (C4 Level 1)

{Mermaid diagram showing system in context with external systems}

### 2.2 Container View (C4 Level 2)

{Mermaid diagram showing containers/services/databases}

### 2.3 Component View (C4 Level 3)

{Mermaid diagram showing key components within main container}

### 2.4 Architecture Style

- **Pattern:** {Monolith | Microservices | Modular Monolith | Layered}
- **Evidence:** {file}:{line}

### 2.5 Architecture Characteristics

| Characteristic | Current State | Evidence |
|----------------|---------------|----------|
| Scalability | {horizontal/vertical/none} | {file:line} |
| Availability | {HA/single point of failure} | {file:line} |
| Maintainability | {high/medium/low} | {reasoning} |

```

Write to: `{reports_dir}/technical-spec-legacy.md`

**Verify:** Read file, confirm diagrams render correctly.

**Output:**

```text
technical-spec-legacy.md Chunk 1/5 complete: Introduction + Architecture
  - Diagrams: [COUNT]
  - Lines: [COUNT]

```

---

## Chunk 2: Technology Stack + Data Architecture

Generate Sections 3 and 4.

---
⏸️ **[STOP: GENERATE_CHUNK_2]**

### Section 3: Technology Stack

```markdown
## 3. Technology Stack

### 3.1 Runtime & Language

| Component | Technology | Version | Source |
|-----------|------------|---------|--------|
| Language | {Java/Python/etc} | {version} | {file:line} |
| Runtime | {JVM/Node/etc} | {version} | {config file} |
| Framework | {Spring/Django/etc} | {version} | {build file} |

### 3.2 Database

| Database | Type | Version | Purpose |
|----------|------|---------|---------|
| {name} | {SQL/NoSQL} | {version} | {primary/cache/etc} |

**Connection Configuration:** {file}:{line}
**Pool Settings:** min={n}, max={m}

### 3.3 Build & Package Management

- **Build Tool:** {Maven/Gradle/npm/etc}
- **Config File:** {pom.xml/package.json/etc}
- **Dependencies:** {count} direct, {count} transitive

### 3.4 External Services

| Service | Purpose | Integration |
|---------|---------|-------------|
| {service} | {purpose} | {REST/SOAP/gRPC} |

```

### Section 4: Data Architecture

```markdown
## 4. Data Architecture

### 4.1 Database Schema

{Mermaid ERD diagram showing entity relationships}

### 4.2 Key Entities

| Entity | Table | Key Fields | Relationships |
|--------|-------|------------|---------------|
| {entity} | {table} | {fields} | {relations} |

**Source:** {model file}:{line}

### 4.3 Data Access Patterns

- **ORM:** {JPA/Hibernate/Sequelize/etc}
- **Repository Pattern:** {yes/no}
- **Query Style:** {JPQL/native SQL/Query Builder}

### 4.4 Caching Strategy

- **Cache:** {Redis/Memcached/In-memory/None}
- **Cache Keys:** {pattern}
- **TTL:** {duration}
- **Invalidation:** {strategy}

```

Append to: `{reports_dir}/technical-spec-legacy.md`

**Output:**

```text
technical-spec-legacy.md Chunk 2/5 complete: Tech Stack + Data
  - Technologies: [COUNT]
  - Entities: [COUNT]
  - Lines: [COUNT]

```

---

## Chunk 3: API Design + Integration Architecture

Generate Sections 5 and 6.

---
⏸️ **[STOP: GENERATE_CHUNK_3]**

### Section 5: API Design

```markdown
## 5. API Design

### 5.1 API Style

- **Style:** {REST | SOAP | GraphQL | RPC}
- **Evidence:** {file}:{line}

### 5.2 Endpoint Catalog

| Endpoint | Method | Purpose | Auth | Source |
|----------|--------|---------|------|--------|
| {path} | {method} | {purpose} | {type} | {file:line} |

### 5.3 Request/Response Patterns

**Example Request:**
```json
{sample request}
```

**Example Response:**
```json
{sample response}
```

### 5.4 Error Handling

| Code | Meaning | Response Format |
|------|---------|-----------------|
| {code} | {meaning} | {format} |

**Error Handler:** {file}:{line}

```

### Section 6: Integration Architecture

```markdown
## 6. Integration Architecture

### 6.1 External Integrations

{Sequence diagram showing external system interactions}

### 6.2 Integration Points

| System | Protocol | Direction | Data Format | Source |
|--------|----------|-----------|-------------|--------|
| {system} | {protocol} | {in/out/both} | {format} | {file:line} |

### 6.3 Message Queues (if any)

- **Technology:** {RabbitMQ/Kafka/SQS/None}
- **Topics/Queues:** {list}
- **Patterns:** {Pub/Sub/Request-Reply/etc}

### 6.4 Synchronous vs Asynchronous

| Operation | Type | Rationale |
|-----------|------|-----------|
| {operation} | {sync/async} | {reason} |

```

Append to: `{reports_dir}/technical-spec-legacy.md`

**Output:**

```text
technical-spec-legacy.md Chunk 3/5 complete: API + Integrations
  - Endpoints: [COUNT]
  - Integrations: [COUNT]
  - Lines: [COUNT]

```

---

## Chunk 4: Security + Deployment

Generate Sections 7 and 8.

---
⏸️ **[STOP: GENERATE_CHUNK_4]**

### Section 7: Security Architecture

```markdown
## 7. Security Architecture

### 7.1 Authentication

- **Mechanism:** {JWT/Session/OAuth/Basic}
- **Implementation:** {file}:{line}
- **Token Storage:** {cookie/localStorage/header}
- **Session Duration:** {duration}

### 7.2 Authorization

- **Model:** {RBAC/ABAC/ACL/Custom}
- **Implementation:** {file}:{line}
- **Roles Defined:** {list}

### 7.3 Password Handling

- **Hashing:** {bcrypt/argon2/SHA/plain}
- **Salt Strategy:** {per-user/global/none}
- **Evidence:** {file}:{line}

### 7.4 Data Protection

| Data Type | Protection | Location |
|-----------|------------|----------|
| Passwords | {hashing algo} | {file:line} |
| PII | {encrypted/plain} | {file:line} |
| Secrets | {vault/env/config} | {file:line} |

### 7.5 Security Issues Detected

| Issue | Severity | Location | Description |
|-------|----------|----------|-------------|
| {issue} | {HIGH/MEDIUM/LOW} | {file:line} | {description} |

```

### Section 8: Deployment Architecture

```markdown
## 8. Deployment Architecture

### 8.1 Current Environment

- **Platform:** {AWS/Azure/GCP/On-prem/etc}
- **Deployment:** {VMs/Containers/Serverless}
- **Evidence:** {Dockerfile/k8s yaml/etc}

### 8.2 Deployment Diagram

{Mermaid diagram showing current deployment topology}

### 8.3 Infrastructure Configuration

| Component | Configuration | Source |
|-----------|---------------|--------|
| {component} | {config} | {file} |

### 8.4 CI/CD Pipeline

- **Platform:** {Jenkins/GitHub Actions/GitLab/etc}
- **Pipeline File:** {path}
- **Stages:** {list}

### 8.5 Environment Management

| Environment | Purpose | Config Source |
|-------------|---------|---------------|
| {env} | {purpose} | {file/vault} |

```

Append to: `{reports_dir}/technical-spec-legacy.md`

**Output:**

```text
technical-spec-legacy.md Chunk 4/5 complete: Security + Deployment
  - Security Issues: [COUNT]
  - Environments: [COUNT]
  - Lines: [COUNT]

```

---

## Chunk 5: Testing + Observability + Technical Debt

Generate Sections 9, 10, and 11.

---
⏸️ **[STOP: GENERATE_CHUNK_5]**

### Section 9: Testing Infrastructure

```markdown
## 9. Testing Infrastructure

### 9.1 Test Framework

- **Framework:** {JUnit/pytest/Jest/etc}
- **Version:** {version}
- **Config:** {file}

### 9.2 Test Coverage

| Category | Test Files | Estimated Coverage |
|----------|------------|-------------------|
| Unit | {count} | {percentage}% |
| Integration | {count} | {percentage}% |
| E2E | {count} | {percentage}% |

### 9.3 Test Patterns

- **Mocking:** {Mockito/Jest mocks/etc}
- **Fixtures:** {factories/fixtures/inline}
- **Assertions:** {avg per test}

### 9.4 Test Gaps

| Component | Gap | Priority |
|-----------|-----|----------|
| {component} | {no tests/partial} | {HIGH/MEDIUM/LOW} |

```

### Section 10: Observability

```markdown
## 10. Observability

### 10.1 Logging

- **Framework:** {Log4j/Winston/etc}
- **Format:** {JSON/text}
- **Levels:** {configured levels}
- **Config:** {file}:{line}

### 10.2 Metrics

- **Tool:** {Prometheus/StatsD/None}
- **Endpoints:** {metrics endpoint if any}
- **Custom Metrics:** {list}

### 10.3 Tracing

- **Tool:** {Jaeger/Zipkin/None}
- **Instrumentation:** {auto/manual}

### 10.4 Health Checks

| Endpoint | Purpose | Source |
|----------|---------|--------|
| {path} | {purpose} | {file:line} |

```

### Section 11: Technical Debt Summary

```markdown
## 11. Technical Debt Summary

### 11.1 Critical Issues

| Issue | Category | Location | Impact |
|-------|----------|----------|--------|
| {issue} | {security/performance/maintainability} | {file:line} | {impact} |

### 11.2 Outdated Dependencies

| Package | Current | Latest | Risk |
|---------|---------|--------|------|
| {pkg} | {ver} | {ver} | {HIGH/MEDIUM/LOW} |

### 11.3 Code Quality Concerns

- **Duplicated Code:** {percentage}%
- **Complex Methods:** {count} with cyclomatic > 10
- **Large Files:** {count} with > 500 LOC

### 11.4 Architecture Concerns

| Concern | Description | Impact |
|---------|-------------|--------|
| {concern} | {description} | {impact} |

```

Append to: `{reports_dir}/technical-spec-legacy.md`

**Verify:** Read complete file, confirm:
- All 11 sections present
- All components have file:line references
- Diagrams render correctly
- No placeholders or TODOs

**Output:**

```text
technical-spec-legacy.md Chunk 5/5 complete: Testing + Observability + Debt
  - Lines: [COUNT]

technical-spec-legacy.md COMPLETE (5/5 chunks)
   Total diagrams: [COUNT]
   Total lines: [COUNT]

```

---

## Completion Marker

```text
═══════════════════════════════════════════════════════════
  ARTIFACT COMPLETE: TECHNICAL-SPEC-LEGACY.md

  Chain ID: {chain_id}
  Sections: 11
  Diagrams: {count}
  Lines: {count}

  This documents the LEGACY system architecture (how it's built today).

  NEXT: Generate technical-spec-target.md (how it will be built)
═══════════════════════════════════════════════════════════

ARTIFACT_COMPLETE:TECHNICAL_SPEC_LEGACY

```

---

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.

**DO NOT:**
- Skip to stage-prompts/
- Mark Stage 6 complete
- Include modernization recommendations

**You MUST generate both technical specs before proceeding.**
