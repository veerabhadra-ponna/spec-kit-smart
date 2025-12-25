---
stage: technical_spec_legacy
requires: functional-spec-target complete
condition: state.analysis_scope == "A"
outputs: technical_spec_legacy_complete
version: 3.2.0
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

## ⚠️ MANDATORY CHUNKING REQUIREMENT

🛑 **STOP - READ THIS FIRST BEFORE GENERATING ANYTHING**

**DO NOT generate the entire technical spec in one operation.**

**DO NOT create all sections at once.**

**DO NOT skip the chunking strategy below.**

**YOU MUST generate the spec in 5 separate chunks as specified below.**

Attempting to generate the full spec in one operation WILL result in:

- Incomplete sections due to token limits
- Missing file:line references
- Missing or broken Mermaid diagrams
- Placeholder content (TODO, TBD)
- Verification failures
- Wasted time and compute resources

**If you are about to say "I'll create it in one operation" → STOP and read the chunking strategy below.**

---

## Chunking Strategy

**CRITICAL**: The technical-spec-legacy.md size will vary based on project complexity:

- **Small projects** (< 5,000 LOC): **800-2,000 lines**
- **Medium projects** (5,000-50,000 LOC): **2,000-5,000 lines**
- **Large projects** (> 50,000 LOC): **4,000-10,000+ lines**

**⚠️ COMPLETION-BASED CHUNKING (NOT size-based)**:

Use **completion-based chunking**, NOT size-based chunking:

- Generate complete logical sections in each chunk
- Each chunk ends with a distinct completion point
- Display progress after each chunk (MANDATORY)
- NO placeholders allowed (no TODO, TBD, "will be analyzed")

**Why chunking is critical**:

- Technical specs require detailed diagrams that take space
- Large specs may hit token limits without chunking
- Progress tracking improves user experience
- Verification gates ensure quality at each step

---

## Resume Detection (BEFORE Starting)

**BEFORE generating any chunks**, check for interrupted generation:

**Step 1: Check for existing spec**:

```bash
# Check if technical-spec-legacy.md already exists
if [ -f "{reports_dir}/technical-spec-legacy.md" ]; then
  # Spec exists - check content to determine resume point
  # Look for section headers to determine last completed chunk
fi
```

**Step 2: Determine resume point from spec content**:

**IF** technical-spec-legacy.md exists AND is incomplete:

1. Read `{reports_dir}/technical-spec-legacy.md`
2. Identify last completed chunk by checking which section headers exist
3. Display resume message:

   ```text
   ⚠️ RESUMING INTERRUPTED GENERATION

   Last completed: Chunk 2 (Technology Stack + Data Architecture)
   Resuming from: Chunk 3 (API Design + Integration Architecture)

   Continuing generation...
   ```

4. Skip completed chunks
5. Start generation from next incomplete chunk

**IF** technical-spec-legacy.md does NOT exist:

- Start fresh from Chunk 1

---

## Spec Structure (5 Chunks)

Generate spec in `{reports_dir}/technical-spec-legacy.md`

**⚠️ GENERATION ORDER - STRICTLY ENFORCED**:

1. Generate ONLY Chunk 1 first
2. Wait for Chunk 1 completion
3. THEN generate Chunk 2
4. Continue sequentially through all 5 chunks

**DO NOT**:

- ❌ Generate multiple chunks in one response
- ❌ Generate all sections at once
- ❌ Skip progress display

**IF** you find yourself generating more than one chunk at a time → **STOP IMMEDIATELY**

---

### Chunk 1: Introduction + Architecture Overview

Generate Sections 1 and 2.

---

⏸️ **[STOP: GENERATE_CHUNK_1]**

#### Section 1: Introduction

- Document purpose and scope
- Technical audience
- System overview

#### Section 2: Architecture Overview

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

**Completion Criteria**:

- ✓ C4 diagrams at all 3 levels
- ✓ Architecture style identified with evidence
- ✓ Characteristics documented
- ✓ NO placeholders

**After Chunk 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `{reports_dir}/technical-spec-legacy.md`
   - Content: Complete Sections 1-2

2. **Verify:** Read file, confirm diagrams render correctly.

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 1/5 complete: Introduction + Architecture
     - C4 Diagrams: 3
     - Architecture style: [STYLE]
     - Lines generated: [COUNT]

   ```

---

### Chunk 2: Technology Stack + Data Architecture

Generate Sections 3 and 4.

---

⏸️ **[STOP: GENERATE_CHUNK_2]**

#### Section 3: Technology Stack

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

#### Section 4: Data Architecture

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

**Completion Criteria**:

- ✓ All technologies documented with versions
- ✓ ERD diagram included
- ✓ Every component has file:line reference
- ✓ NO placeholders

**After Chunk 2 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 3 and 4 to technical-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 2/5 complete: Technology Stack + Data Architecture
     - Technologies documented: [COUNT]
     - Entities documented: [COUNT]
     - ERD diagram: ✓
     - Lines generated: [COUNT]

   ```

---

### Chunk 3: API Design + Integration Architecture

Generate Sections 5 and 6.

---

⏸️ **[STOP: GENERATE_CHUNK_3]**

#### Section 5: API Design

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

\`\`\`json
{sample request}
\`\`\`

**Example Response:**

\`\`\`json
{sample response}
\`\`\`

### 5.4 Error Handling

| Code | Meaning | Response Format |
|------|---------|-----------------|
| {code} | {meaning} | {format} |

**Error Handler:** {file}:{line}
\`\`\`

#### Section 6: Integration Architecture

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

**Completion Criteria**:

- ✓ All API endpoints documented
- ✓ Integration sequence diagrams included
- ✓ Every endpoint has file:line reference
- ✓ NO placeholders

**After Chunk 3 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 5 and 6 to technical-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 3/5 complete: API Design + Integration Architecture
     - Endpoints documented: [COUNT]
     - Integrations documented: [COUNT]
     - Sequence diagrams: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Chunk 4: Security + Deployment

Generate Sections 7 and 8.

---

⏸️ **[STOP: GENERATE_CHUNK_4]**

#### Section 7: Security Architecture

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

#### Section 8: Deployment Architecture

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

**Completion Criteria**:

- ✓ Security mechanisms documented with evidence
- ✓ Security issues identified with severity
- ✓ Deployment diagram included
- ✓ Every component has file:line reference
- ✓ NO placeholders

**After Chunk 4 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 7 and 8 to technical-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 4/5 complete: Security + Deployment
     - Security issues documented: [COUNT]
     - Environments documented: [COUNT]
     - Deployment diagram: ✓
     - Lines generated: [COUNT]

   ```

---

### Chunk 5: Testing + Observability + Technical Debt

Generate Sections 9, 10, and 11.

---

⏸️ **[STOP: GENERATE_CHUNK_5]**

#### Section 9: Testing Infrastructure

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

#### Section 10: Observability

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

#### Section 11: Technical Debt Summary

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

**Completion Criteria**:

- ✓ Testing infrastructure documented
- ✓ Observability stack documented
- ✓ Technical debt items categorized
- ✓ All components have file:line references
- ✓ NO placeholders

**After Chunk 5 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 9, 10, and 11 to technical-spec-legacy.md

2. **Verify:** Read complete file, confirm:
   - All 11 sections present
   - All components have file:line references
   - Diagrams render correctly
   - No placeholders or TODOs

3. **MANDATORY - Display progress and final summary**:

   ```text
   ✓ Chunk 5/5 complete: Testing + Observability + Technical Debt
     - Test categories documented: [COUNT]
     - Technical debt items: [COUNT]
     - Lines generated: [COUNT]

   ✅ technical-spec-legacy.md GENERATION COMPLETE
      Total sections: 11
      Total diagrams: [COUNT]
      Total lines: [COUNT]
      File path: {reports_dir}/technical-spec-legacy.md

   ```

---

## Verification Gate (HARD STOP)

⚠️ **VERIFICATION GATE - CANNOT PROCEED WITHOUT PASSING**

**BEFORE** proceeding to 06c2-technical-spec-target.md, verify spec quality:

### Verification Checklist

Read technical-spec-legacy.md and verify:

- [ ] File exists at expected path: `{reports_dir}/technical-spec-legacy.md`
- [ ] All 11 section headers present:
      - [ ] Section 1: Introduction
      - [ ] Section 2: Architecture Overview (with C4 diagrams)
      - [ ] Section 3: Technology Stack
      - [ ] Section 4: Data Architecture (with ERD)
      - [ ] Section 5: API Design
      - [ ] Section 6: Integration Architecture
      - [ ] Section 7: Security Architecture
      - [ ] Section 8: Deployment Architecture
      - [ ] Section 9: Testing Infrastructure
      - [ ] Section 10: Observability
      - [ ] Section 11: Technical Debt Summary
- [ ] Quality checks:
      - [ ] 30+ file:line references present throughout
      - [ ] C4 diagrams at 3 levels (Context, Container, Component)
      - [ ] ERD diagram for data model
      - [ ] Deployment diagram present
      - [ ] All API endpoints have file:line references
      - [ ] Security issues have severity ratings
      - [ ] Technical debt items categorized
      - [ ] No placeholders (TODO, TBD, "will be analyzed", "coming soon")
      - [ ] All Mermaid diagrams render correctly
- [ ] Completeness (verify based on project size/complexity):
      - [ ] **Small projects (< 5,000 LOC)**:
            - Total lines: 800+ (minimum)
            - Diagrams: 4+ (C4x3, ERD, deployment)
            - Technical debt items: 5-15
      - [ ] **Medium projects (5,000-50,000 LOC)**:
            - Total lines: 2,000+ (minimum)
            - Diagrams: 6+ (C4x3, ERD, deployment, sequence)
            - Technical debt items: 15-40
      - [ ] **Large projects (> 50,000 LOC)**:
            - Total lines: 4,000+ (minimum)
            - Diagrams: 8+ (multiple of each type)
            - Technical debt items: 40-100

---

### Recovery Actions (IF ANY CHECKBOX FAILS)

**IF ANY checkbox is unchecked**:

```text
❌ VERIFICATION FAILED

technical-spec-legacy.md is incomplete. Issues found:
- [List specific missing items from checklist above]
```

**RECOVERY DECISION TREE**:

**1. Identify incomplete sections**:

List which sections or quality checks failed verification.

**2. Determine recovery approach**:

**IF** entire sections missing (e.g., Section 7 not found in file):

- **Action**: Regenerate ONLY the missing sections
- **Method**:
  1. Check technical-spec-legacy.md content to identify last completed section
  2. Resume generation from first missing section
  3. Use Edit tool to append missing sections to existing file
  4. Re-run verification after regeneration

**IF** quality issues in existing sections (e.g., diagrams not rendering):

- **Action**: Fix the problematic diagrams or add missing details
- **Method**:
  1. Read the problematic section from technical-spec-legacy.md
  2. Identify specific issues (broken Mermaid syntax, missing refs, etc.)
  3. Regenerate that section with proper detail
  4. Use Edit tool to replace the incomplete section
  5. Re-run verification after enhancement

**IF** multiple critical failures (>3 sections missing OR >5 quality issues):

- **Action**: Recommend full regeneration from scratch
- **Display**:

  ```text
  ⚠️ MULTIPLE CRITICAL ISSUES DETECTED

  Issues found:
  - Missing sections: [COUNT]
  - Quality failures: [COUNT]

  Recommendation: Full regeneration recommended due to extent of issues.
  ```

- **Ask user**:

  ```text
  Recovery options:
  [A] Regenerate entire technical-spec-legacy.md from scratch
  [B] Fix individual sections (may take longer)
  [C] Proceed anyway (NOT RECOMMENDED - will cause issues in next stage)

  Your choice: ___
  ```

**3. Execute recovery**:

- Based on failure type, perform specific recovery actions
- Use appropriate tools (Edit for fixes, Write for full regen)
- Re-run verification after recovery
- **DO NOT proceed to 06c2 until verification passes**

⚠️ **STOP HERE** - DO NOT CONTINUE TO NEXT STAGE UNTIL VERIFICATION PASSES

---

### Verification Success

**IF ALL checkboxes are checked**:

```text
✅ VERIFICATION PASSED

technical-spec-legacy.md is complete and meets quality standards:
- All 11 sections present and complete
- 30+ file:line references found
- C4 diagrams at all 3 levels
- ERD and deployment diagrams present
- Security issues documented with severity
- Technical debt categorized
- No placeholders or incomplete sections
- Total lines: [COUNT] (comprehensive spec)

Proceeding to 06c2-technical-spec-target.md...
```

**Only after passing verification**: Proceed to next stage

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
