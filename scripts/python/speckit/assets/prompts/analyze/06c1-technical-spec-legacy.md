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

## [!] IMPORTANT: "Part" vs CLI "--chunk"

This prompt uses **"Part 1-5"** to describe content sections to write incrementally.

**These are NOT CLI `--chunk` parameters!**

- [x] DO NOT run `speckitadv analyze-project --chunk=4` to continue
- [ok] DO continue writing content using `write-report --append`
- [ok] DO run `speckitadv analyze-project` (no --chunk) when this stage is complete

---

## State Management

**Available template variables:**

- `{analysis_dir}` - Analysis folder path (root)
- `{data_dir}` - Data folder for JSON files (`{analysis_dir}/data/`)
- `{reports_dir}` - Reports folder for MD files (`{analysis_dir}/reports/`)

**CLI Utility Commands:**

[!] **OS command line length limits apply (~8000 chars on Windows).**

**IMPORTANT:** Chunking means MULTIPLE write operations, NOT reduced content. Generate FULL comprehensive output.

```bash
# ALWAYS use --append (creates if not exists, appends if exists)
speckitadv write-report <filename> --stage=06c1-technical-spec-legacy --append --content '<content>'
```

**For content > 2000 chars, use stdin mode:**

```powershell
@"
<markdown content here>
"@ | speckitadv write-report <filename> --stage=06c1-technical-spec-legacy --append --stdin
```

---

## [!] CRITICAL: File Write Policy

**ALWAYS use CLI commands for file writes. NEVER use:**

- Shell/PowerShell commands (`Out-File`, `Add-Content`, `echo >`, `cat <<`)
- AI Write tools directly to the analysis folder
- Any method that bypasses the CLI artifact tracking

**Why:** CLI commands track artifacts in state.json for workflow continuity.
Any file written outside the CLI will NOT be tracked and may cause issues.

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

## [!] MANDATORY MULTI-PART WRITING

[STOP] **STOP - READ THIS FIRST BEFORE GENERATING ANYTHING**

**DO NOT generate the entire technical spec in one operation.**

**DO NOT create all sections at once.**

**DO NOT skip the writing strategy below.**

**YOU MUST generate the spec in 5 separate parts as specified below.**

Attempting to generate the full spec in one operation WILL result in:

- Incomplete sections due to token limits
- Missing file:line references
- Missing or broken Mermaid diagrams
- Placeholder content (TODO, TBD)
- Verification failures
- Wasted time and compute resources

**If you are about to say "I'll create it in one operation" -> STOP and read the writing strategy below.**

---

## Multi-Part Writing Strategy

**CRITICAL**: The technical-spec-legacy.md size will vary based on project complexity:

- **Small projects** (< 5,000 LOC): **800-2,000 lines**
- **Medium projects** (5,000-50,000 LOC): **2,000-5,000 lines**
- **Large projects** (> 50,000 LOC): **4,000-10,000+ lines**

**[!] COMPLETION-BASED WRITING (NOT size-based)**:

Use **completion-based writing**, NOT size-based writing:

- Generate complete logical sections in each part
- Each part ends with a distinct completion point
- Display progress after each part (MANDATORY)
- NO placeholders allowed (no TODO, TBD, "will be analyzed")

**Why multi-part writing is critical**:

- Technical specs require detailed diagrams that take space
- Large specs may hit token limits without multi-part writing
- Progress tracking improves user experience
- Verification gates ensure quality at each step

---

## Resume Detection (BEFORE Starting)

**BEFORE generating any parts**, check for interrupted generation:

**Step 1: Check for existing spec**:

```bash
# Check if technical-spec-legacy.md already exists
if [ -f "{reports_dir}/technical-spec-legacy.md" ]; then
  # Spec exists - check content to determine resume point
  # Look for section headers to determine last completed part
fi
```

**Step 2: Determine resume point from spec content**:

**IF** technical-spec-legacy.md exists AND is incomplete:

1. Read `{reports_dir}/technical-spec-legacy.md`
2. Identify last completed part by checking which section headers exist
3. Display resume message:

   ```text
   [!] RESUMING INTERRUPTED GENERATION

   Last completed: Part 2 (Technology Stack + Data Architecture)
   Resuming from: Part 3 (API Design + Integration Architecture)

   Continuing generation...
   ```

4. Skip completed parts
5. Start generation from next incomplete part

**IF** technical-spec-legacy.md does NOT exist:

- Start fresh from Part 1

---

## Spec Structure (5 Parts)

Generate spec in `{reports_dir}/technical-spec-legacy.md`

**[!] GENERATION ORDER - STRICTLY ENFORCED**:

1. Generate ONLY Part 1 first
2. Wait for Part 1 completion
3. THEN generate Part 2
4. Continue sequentially through all 5 parts

**DO NOT**:

- [x] Generate multiple parts in one response
- [x] Generate all sections at once
- [x] Skip progress display

**IF** you find yourself generating more than one part at a time -> **STOP IMMEDIATELY**

---

### Part 1: Introduction + Architecture Overview

Generate Sections 1 and 2.

---

[STOP: GENERATE_PART_1]**

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

- [ok] C4 diagrams at all 3 levels
- [ok] Architecture style identified with evidence
- [ok] Characteristics documented
- [ok] NO placeholders

**After Part 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `{reports_dir}/technical-spec-legacy.md`
   - Content: Complete Sections 1-2

2. **Verify:** Read file, confirm diagrams render correctly.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 1/5 complete: Introduction + Architecture
     - C4 Diagrams: 3
     - Architecture style: [STYLE]
     - Lines generated: [COUNT]

   ```

---

### Part 2: Technology Stack + Data Architecture

Generate Sections 3 and 4.

---

[STOP: GENERATE_PART_2]**

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

- [ok] All technologies documented with versions
- [ok] ERD diagram included
- [ok] Every component has file:line reference
- [ok] NO placeholders

**After Part 2 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 3 and 4 to technical-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 2/5 complete: Technology Stack + Data Architecture
     - Technologies documented: [COUNT]
     - Entities documented: [COUNT]
     - ERD diagram: [ok]
     - Lines generated: [COUNT]

   ```

---

### Part 3: API Design + Integration Architecture

Generate Sections 5 and 6.

---

[STOP: GENERATE_PART_3]**

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

- [ok] All API endpoints documented
- [ok] Integration sequence diagrams included
- [ok] Every endpoint has file:line reference
- [ok] NO placeholders

**After Part 3 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 5 and 6 to technical-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 3/5 complete: API Design + Integration Architecture
     - Endpoints documented: [COUNT]
     - Integrations documented: [COUNT]
     - Sequence diagrams: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 4: Security + Deployment

Generate Sections 7 and 8.

---

[STOP: GENERATE_PART_4]**

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

- [ok] Security mechanisms documented with evidence
- [ok] Security issues identified with severity
- [ok] Deployment diagram included
- [ok] Every component has file:line reference
- [ok] NO placeholders

**After Part 4 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 7 and 8 to technical-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 4/5 complete: Security + Deployment
     - Security issues documented: [COUNT]
     - Environments documented: [COUNT]
     - Deployment diagram: [ok]
     - Lines generated: [COUNT]

   ```

---

### Part 5: Testing + Observability + Technical Debt

Generate Sections 9, 10, and 11.

---

[STOP: GENERATE_PART_5]**

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

- [ok] Testing infrastructure documented
- [ok] Observability stack documented
- [ok] Technical debt items categorized
- [ok] All components have file:line references
- [ok] NO placeholders

**After Part 5 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 9, 10, and 11 to technical-spec-legacy.md

2. **Verify:** Read complete file, confirm:
   - All 11 sections present
   - All components have file:line references
   - Diagrams render correctly
   - No placeholders or TODOs

3. **MANDATORY - Display progress and final summary**:

   ```text
   [ok] Part 5/5 complete: Testing + Observability + Technical Debt
     - Test categories documented: [COUNT]
     - Technical debt items: [COUNT]
     - Lines generated: [COUNT]

   [ok] technical-spec-legacy.md GENERATION COMPLETE
      Total sections: 11
      Total diagrams: [COUNT]
      Total lines: [COUNT]
      File path: {reports_dir}/technical-spec-legacy.md

   ```

---

## Verification Gate (HARD STOP)

[!] **VERIFICATION GATE - CANNOT PROCEED WITHOUT PASSING**

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
[x] VERIFICATION FAILED

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
  [!] MULTIPLE CRITICAL ISSUES DETECTED

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

[!] **STOP HERE** - DO NOT CONTINUE TO NEXT STAGE UNTIL VERIFICATION PASSES

---

### Verification Success

**IF ALL checkboxes are checked**:

```text
[ok] VERIFICATION PASSED

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
===========================================================
  ARTIFACT COMPLETE: TECHNICAL-SPEC-LEGACY.md

  Chain ID: {chain_id}
  Sections: 11
  Diagrams: {count}
  Lines: {count}

  This documents the LEGACY system architecture (how it's built today).

  NEXT: Generate technical-spec-target.md (how it will be built)
===========================================================

ARTIFACT_COMPLETE:TECHNICAL_SPEC_LEGACY
```

---

**[GATE-CHECK]** If verification PASSES: auto-continue to next stage.
If verification FAILS: present recovery options and WAIT for user decision.

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.

**DO NOT:**

- Skip to stage-prompts/
- Mark Stage 6 complete
- Include modernization recommendations

**You MUST generate both technical specs before proceeding.**
