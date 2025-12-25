# Functional Specification - Legacy System Analysis

**Project**: <<PROJECT_NAME>>
**Legacy System Version**: <<LEGACY_VERSION>>
**Analysis Date**: <<ANALYSIS_DATE>>
**Analyst**: AI Agent
**Status**: Draft (For Modernization)

---

## Instructions for AI

This template is based on **Section A (Business Analysis)** from the Universal Meta-Prompt.
It is adapted for **legacy code analysis** to extract WHAT the system does (not HOW).

**Key Adaptations for Legacy Analysis**:

- Extract information from **actual code**, not imagination
- Every finding must include **Evidence** (file:line references)
- Focus on WHAT (business functionality), not HOW (implementation details)
- Identify **Known Quirks** and **Legacy Behaviors** that may need preservation
- Categorize features by criticality: CRITICAL, STANDARD, LEGACY QUIRKS

**Placeholders to Fill** (based on deep analysis of legacy code):

- `<<PROJECT_NAME>>` - Extract from package.json, pom.xml, README, etc.
- `<<LEGACY_VERSION>>` - Current version from codebase
- `<<ANALYSIS_DATE>>` - Current date (ISO 8601)
- `<<EXTRACT_FEATURES>>` - Scan controllers, routes, services for features
- `<<EXTRACT_PERSONAS>>` - Identify from auth/RBAC/user roles in code
- `<<EXTRACT_JOURNEYS>>` - Map workflows from code paths
- `<<EXTRACT_DATA_MODELS>>` - Parse from DB schemas, migrations, ORMs
- `<<EXTRACT_CONFIG>>` - List all config files and their purposes
- `<<EXTRACT_QUIRKS>>` - Find hardcoded values, workarounds, edge cases

---

## 1. Executive Summary

**WHAT**: <<1-2 sentences describing what the legacy system does>>

**WHO**: <<Primary user types/personas extracted from code>>

**WHY**: <<Business purpose derived from functionality analysis>>

**TOP 3 CAPABILITIES**:

1. <<Most important feature from code analysis>>
2. <<Second most important feature>>
3. <<Third most important feature>>

**Evidence**: Analysis of <<N>> files across <<M>> directories

---

## 2. Current State - Problem & Goals

### Current Business Objectives

Based on analysis of the legacy codebase, the system serves these objectives:

- <<Objective 1>> (Evidence: <<file:line>>)
- <<Objective 2>> (Evidence: <<file:line>>)
- <<Objective 3>> (Evidence: <<file:line>>)

### KPIs/Metrics (Extracted from Code)

| Metric | Current Implementation | Evidence |
| -------- | ---------------------- | ---------- |
| <<Metric name>> | <<How it's tracked>> | <<file:line>> |
| <<Response time>> | <<Hardcoded timeout/config>> | <<file:line>> |
| <<Throughput>> | <<Rate limit/throttle config>> | <<file:line>> |

---

## 3. Personas & User Journeys

### Personas (Extracted from Code)

<<Extract from authentication, authorization, RBAC, user roles>>

| Persona | Evidence | Permissions/Capabilities |
| --------- | ---------- | ------------------------- |
| <<Admin>> | <<auth.js:45-67>> | <<Full access, user management, etc.>> |
| <<User>> | <<auth.js:89-102>> | <<Read/write own data, limited access>> |
| <<Guest>> | <<auth.js:115-120>> | <<Read-only public data>> |

### Top User Journeys (From Code Paths)

```mermaid
journey
  title Key User Journeys (Extracted from Legacy Code)
  section <<Journey 1 Name>>
    <<Step 1>>: 3: <<Persona>>
    <<Step 2>>: 3: <<Persona>>
    <<Step 3>>: 3: <<Persona>>
  section <<Journey 2 Name>>
    <<Step 1>>: 3: <<Persona>>
    <<Step 2>>: 3: <<Persona>>
```

**Evidence**:

- Journey 1: <<controller paths, workflow files>>
- Journey 2: <<service methods, state machines>>

---

## 4. Use Cases (Extracted from Code)

### UC-001: <<Use Case Name>>

| Attribute | Value |
|-----------|-------|
| **ID** | UC-001 |
| **Name** | <<Use Case Name>> |
| **Actor(s)** | <<Primary Actor>>, <<Secondary Actor>> |
| **Priority** | CRITICAL / STANDARD |
| **Evidence** | <<file:line>> |

**Preconditions**:
1. <<Precondition 1>>
2. <<Precondition 2>>

**Main Flow (Happy Path)**:
1. Actor <<action 1>>
2. System <<response 1>>
3. Actor <<action 2>>
4. System <<response 2>>
5. System <<final outcome>>

**Alternative Flows**:

| ID | Trigger | Steps | Outcome |
|----|---------|-------|---------|
| AF-1 | <<condition>> | <<steps>> | <<outcome>> |
| AF-2 | <<condition>> | <<steps>> | <<outcome>> |

**Exception Flows**:

| ID | Trigger | Steps | Outcome |
|----|---------|-------|---------|
| EF-1 | <<error condition>> | <<error handling>> | <<recovery/error state>> |
| EF-2 | <<error condition>> | <<error handling>> | <<recovery/error state>> |

**Postconditions**:
1. <<State after successful completion>>
2. <<Data changes made>>

**Business Rules Applied**:
- BR-<<id>>: <<rule reference>>

---

### UC-002: <<Next Use Case>>

<<Repeat structure>>

---

## 5. User Stories (Given-When-Then Format)

### CRITICAL Stories

#### US-CRIT-001: <<Story Title>>

**Evidence**: <<file:line>>
**Priority**: CRITICAL
**Actor**: <<Persona>>

**Story**:
> As a **<<persona>>**,
> I want to **<<action/capability>>**,
> So that **<<business value>>**.

**Acceptance Criteria (Given-When-Then)**:

```gherkin
Scenario: <<Scenario Name>>
  Given <<initial context/state>>
    And <<additional context>>
  When <<action performed>>
    And <<additional action>>
  Then <<expected outcome>>
    And <<additional outcome>>

Scenario: <<Edge Case Scenario>>
  Given <<edge case context>>
  When <<action>>
  Then <<expected behavior>>
```

**Current Implementation**:
- Code location: <<file:line-range>>
- Key logic: <<summary of implementation>>

---

#### US-CRIT-002: <<Next Critical Story>>

<<Repeat structure>>

---

### STANDARD Stories

#### US-STD-001: <<Story Title>>

**Evidence**: <<file:line>>
**Priority**: STANDARD
**Actor**: <<Persona>>

**Story**:
> As a **<<persona>>**,
> I want to **<<action/capability>>**,
> So that **<<business value>>**.

**Acceptance Criteria (Given-When-Then)**:

```gherkin
Scenario: <<Scenario Name>>
  Given <<context>>
  When <<action>>
  Then <<outcome>>
```

**Modernization Opportunity**: <<How this could be improved>>

---

## 6. Business Logic (Pseudocode & Flowcharts)

### BL-001: <<Business Logic Name>>

**Evidence**: <<file:line-range>>
**Category**: <<Validation | Calculation | Authorization | Workflow | Data Processing>>
**Criticality**: <<CRITICAL | STANDARD>>

**Plain English Description**:
<<Natural language explanation of what this logic does and why>>

**Pseudocode**:

```plaintext
FUNCTION <<function_name>>(<<parameters>>):
    // Validation
    IF <<condition>> THEN
        RAISE Error("<<message>>")
    END IF

    // Core Logic
    SET <<variable>> = <<initial_value>>

    FOR EACH <<item>> IN <<collection>>:
        IF <<condition>> THEN
            <<action>>
        ELSE IF <<other_condition>> THEN
            <<alternative_action>>
        ELSE
            <<default_action>>
        END IF
    END FOR

    // Calculation
    SET <<result>> = <<formula>>

    // Persist
    SAVE <<entity>> TO <<storage>>

    RETURN <<result>>
END FUNCTION
```

**Flowchart**:

```mermaid
flowchart TD
    A[Start: <<trigger>>] --> B{<<condition check>>}
    B -->|Yes| C[<<action 1>>]
    B -->|No| D[<<action 2>>]
    C --> E{<<validation>>}
    E -->|Valid| F[<<process>>]
    E -->|Invalid| G[<<error handling>>]
    F --> H[<<persist/output>>]
    G --> I[End: Error]
    H --> J[End: Success]
    D --> J
```

**Edge Cases**:

| Case | Handling | Evidence |
|------|----------|----------|
| <<edge case 1>> | <<how handled>> | <<file:line>> |
| <<edge case 2>> | <<how handled>> | <<file:line>> |

---

### BL-002: <<Next Business Logic>>

<<Repeat structure>>

---

## 7. State Machines

### SM-001: <<Entity/Process Name>> States

**Evidence**: <<file:line-range>> or <<state management files>>
**Applies To**: <<Entity or Process>>

**State Diagram**:

```mermaid
stateDiagram-v2
    [*] --> Draft

    Draft --> Pending: submit()
    Draft --> Cancelled: cancel()

    Pending --> Approved: approve()
    Pending --> Rejected: reject()
    Pending --> Draft: requestChanges()

    Approved --> Active: activate()
    Approved --> Cancelled: cancel()

    Active --> Suspended: suspend()
    Active --> Completed: complete()

    Suspended --> Active: resume()
    Suspended --> Cancelled: cancel()

    Rejected --> Draft: revise()
    Rejected --> Cancelled: abandon()

    Completed --> [*]
    Cancelled --> [*]
```

**State Definitions**:

| State | Description | Entry Conditions | Exit Conditions |
|-------|-------------|------------------|-----------------|
| <<Draft>> | <<Initial state, editable>> | <<Created>> | <<submit, cancel>> |
| <<Pending>> | <<Awaiting approval>> | <<Submitted>> | <<approve, reject, requestChanges>> |
| <<Approved>> | <<Approved, ready for activation>> | <<Approval granted>> | <<activate, cancel>> |
| <<Active>> | <<In use/operation>> | <<Activated>> | <<suspend, complete>> |
| <<Suspended>> | <<Temporarily inactive>> | <<Suspended by admin>> | <<resume, cancel>> |
| <<Completed>> | <<Final successful state>> | <<Process finished>> | <<terminal>> |
| <<Rejected>> | <<Denied, needs revision>> | <<Rejection>> | <<revise, abandon>> |
| <<Cancelled>> | <<Terminated>> | <<Cancellation>> | <<terminal>> |

**Transitions**:

| From | To | Trigger | Guard Condition | Action | Evidence |
|------|-----|---------|-----------------|--------|----------|
| Draft | Pending | submit() | <<validation passes>> | <<notify reviewers>> | <<file:line>> |
| Pending | Approved | approve() | <<has approval authority>> | <<log approval>> | <<file:line>> |
| Pending | Rejected | reject() | <<has rejection authority>> | <<notify owner, log reason>> | <<file:line>> |

**Business Rules for Transitions**:
- BR-<<id>>: <<rule that governs transitions>>

---

### SM-002: <<Next State Machine>>

<<Repeat structure>>

---

## 8. Configuration-Driven Behaviors

### Config Category: <<Category Name>>

**Evidence**: <<config file path>>
**Impact**: <<What behavior is controlled>>

#### CFG-001: <<Configuration Name>>

| Attribute | Value |
|-----------|-------|
| **Config Key** | <<key name>> |
| **Location** | <<file path>> |
| **Type** | <<string/number/boolean/object>> |
| **Default** | <<default value>> |
| **Environment Override** | <<ENV_VAR_NAME>> |

**Behavior Impact**:

| Config Value | Resulting Behavior |
|--------------|-------------------|
| `<<value 1>>` | <<behavior when this value>> |
| `<<value 2>>` | <<behavior when this value>> |
| `<<value 3>>` | <<behavior when this value>> |

**Code Reference**:

```javascript
// Evidence: <<file:line>>
if (config.<<key>> === '<<value>>') {
    // <<resulting behavior>>
}
```

**Dependencies**:
- Depends on: <<other config keys>>
- Affects: <<features/modules>>

---

#### CFG-002: <<Next Configuration>>

<<Repeat structure>>

---

### Feature Flags

| Flag | Purpose | Default | Evidence |
|------|---------|---------|----------|
| <<FLAG_NAME>> | <<what it enables/disables>> | <<on/off>> | <<file:line>> |
| <<FLAG_NAME>> | <<what it enables/disables>> | <<on/off>> | <<file:line>> |

**Flag Behavior Matrix**:

| Flag | ON Behavior | OFF Behavior |
|------|-------------|--------------|
| <<flag>> | <<behavior when enabled>> | <<behavior when disabled>> |

---

## 9. Scope / Out-of-Scope

### In Scope (Features Found in Legacy Code)

| Feature/Capability | Evidence (file:line) | Criticality |
| ------------------- | --------------------- | ------------- |
| <<Feature 1>> | <<path/to/file:123>> | CRITICAL |
| <<Feature 2>> | <<path/to/file:456>> | STANDARD |
| <<Feature 3>> | <<path/to/file:789>> | STANDARD |

### Out of Scope (Not Found in Legacy Code)

| Capability | Rationale |
| ----------- | ----------- |
| <<Feature X>> | No evidence in codebase; may be external/deprecated |
| <<Feature Y>> | Only mentioned in comments, no implementation |

---

## 10. Functional Requirements (Extracted from Legacy Code)

### CRITICAL Features (Must Preserve Exactly)

#### FR-CRIT-001: <<Feature Name>>

- **As a** <<persona from code>>, **the system provides** <<capability extracted from code>>,
  **so that** <<business value inferred from usage>>.
- **Evidence**: <<controller/service/file:line-range>>
- **Current Implementation**:
  - <<Key code logic summary>>
  - <<Important config/constants>>
- **Related Use Case**: UC-<<id>>
- **Related User Story**: US-CRIT-<<id>>
- **Business Logic**: BL-<<id>>
- **State Machine**: SM-<<id>> (if applicable)
- **Configuration**: CFG-<<id>> (if applicable)
- **Acceptance Criteria** (derived from code/tests):
  - AC-1: <<Measurable condition from test or code logic>>
  - AC-2: <<Second condition>>
- **CRITICAL**: This behavior MUST be preserved exactly in modernized system.

#### FR-CRIT-002: <<Next Critical Feature>>

<<Repeat structure>>

### STANDARD Features (Can Modernize Implementation)

#### FR-STD-001: <<Feature Name>>

- **As a** <<persona>>, **the system provides** <<capability>>, **so that** <<value>>.
- **Evidence**: <<file:line>>
- **Current Implementation**: <<Summary>>
- **Related Use Case**: UC-<<id>>
- **Related User Story**: US-STD-<<id>>
- **Modernization Opportunity**: <<How this could be improved in new system>>
- **Acceptance Criteria**:
  - AC-1: <<Condition>>
  - AC-2: <<Condition>>

#### FR-STD-002: <<Next Standard Feature>>

<<Repeat structure>>

### LEGACY QUIRKS (Decide: Preserve or Fix)

#### FR-QUIRK-001: <<Quirk Name>>

- **Current Behavior**: <<Description of unexpected/undocumented behavior>>
- **Evidence**: <<file:line>>
- **Issue**: <<Why this is a quirk (hardcoded, workaround, anti-pattern)>>
- **Decision Needed**:
  - **Option A**: Preserve (for backward compatibility)
  - **Option B**: Fix/modernize (with migration plan)
- **Impact Analysis**: <<What breaks if changed>>

#### FR-QUIRK-002: <<Next Quirk>>

<<Repeat structure>>

---

## 11. Non-Negotiables (Extracted from Code Analysis)

These constraints are derived from code evidence and must be preserved:

1. **<<Non-Negotiable 1>>**
   **Rationale**: <<Why mandatory>>
   **Evidence**: <<file:line>>
   **Example**: <<Actual code snippet or config value>>

2. **<<Non-Negotiable 2>>** (e.g., PII Encryption)
   **Rationale**: All PII must be encrypted at rest
   **Evidence**: <<encryption-middleware.js:45-78>>
   **Example**: Uses AES-256-CBC with custom key derivation

3. **<<Non-Negotiable 3>>** (e.g., Audit Logging)
   **Rationale**: Regulatory compliance (GDPR, SOX)
   **Evidence**: <<audit-logger.js:12-34>>
   **Example**: All transactions logged to immutable audit table

---

## 12. Non-Functional Requirements (Legacy System)

### Performance (Extracted from Config/Code)

| Metric | Current Target | Evidence | Notes |
| -------- | --------------- | ---------- | ------- |
| Response time | p95 < <<X>>ms | <<config.js:23>> | Hardcoded timeout |
| Throughput | <<Y>> req/min | <<rate-limiter.js:45>> | Per-user limit |
| Batch size | <<Z>> records | <<batch-processor.js:67>> | Max batch |

### Availability & Reliability

| Metric | Current Implementation | Evidence |
| -------- | ---------------------- | ---------- |
| Uptime | <<SLA/config>> | <<deploy/config.yaml:12>> |
| Retry logic | <<3 attempts, exp backoff>> | <<http-client.js:89-102>> |
| Circuit breaker | <<Threshold: 5 failures>> | <<circuit-breaker.js:34>> |

### Security (Current Implementation)

| Aspect | Implementation | Evidence |
| -------- | --------------- | ---------- |
| Authentication | <<Session-based, 30min timeout>> | <<auth/session.js:45>> |
| Authorization | <<Role-based (admin/user/guest)>> | <<auth/rbac.js:23-67>> |
| Encryption | <<AES-256-CBC for PII>> | <<crypto/encrypt.js:12>> |
| Input validation | <<Schema-based (Joi)>> | <<validators/input.js:34>> |

### Accessibility, Privacy, Localization

| Aspect | Current State | Evidence |
| -------- | -------------- | ---------- |
| A11y | <<WCAG level/none>> | <<frontend analysis>> |
| Privacy | <<PII masking in logs>> | <<logger.js:56>> |
| I18n | <<EN only / multi-lang>> | <<i18n/locales/>> |

---

## 13. Data Models (Extracted from DB Schemas)

### Core Entities

#### Entity: <<EntityName>> (e.g., User)

**Evidence**: <<migrations/001_create_users.sql>> or <<models/User.js>>

| Field | Type | Constraints | PII | Notes |
| ------- | ------ | ------------- | ----- | ------- |
| id | UUID | PRIMARY KEY | No | Auto-generated |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Yes | Encrypted |
| password_hash | VARCHAR(255) | NOT NULL | Yes | bcrypt |
| role | ENUM | admin/user/guest | No | Default: user |
| created_at | TIMESTAMP | NOT NULL | No | Auto |

**Relationships**:

- Has many: <<RelatedEntity>> (<<foreign_key_field>>)
- Belongs to: <<ParentEntity>> (<<foreign_key_field>>)

**Evidence**: <<schema.sql:45-78>> or <<ORM model file>>

#### Entity: <<NextEntityName>>

<<Repeat structure>>

---

## 14. Configuration Mapping (All Config Files)

| Config File | Purpose | Key Settings | Migration Strategy |
| ------------- | --------- | -------------- | ------------------- |
| `.env.example` | Env var template | DB_URL, API_KEY, etc. | Keep, update keys |
| `config/app.js` | App settings | PORT, LOG_LEVEL, TIMEOUT | Migrate to env vars |
| `config/database.yml` | DB connection | host, port, credentials | Use connection string |
| `logging.conf` | Log settings | Format, level, output | Modernize to structured logging |
| `nginx.conf` | Reverse proxy | Routing, SSL | Migrate to K8s Ingress/ALB |

**Evidence**: Analysis of <<N>> config files

---

## 15. API Contracts (Extracted from Code)

### REST Endpoints

| Method | Path | Purpose | Auth Required | Request | Response | Evidence |
| -------- | ------ | --------- | -------------- | --------- | ---------- | ---------- |
| GET | `/api/users` | List users | Yes (admin) | Query params | User[] | <<routes/users.js:23>> |
| POST | `/api/users` | Create user | Yes (admin) | UserInput | User | <<routes/users.js:45>> |
| GET | `/api/users/:id` | Get user | Yes | - | User | <<routes/users.js:67>> |
| PUT | `/api/users/:id` | Update user | Yes (self/admin) | UserInput | User | <<routes/users.js:89>> |
| DELETE | `/api/users/:id` | Delete user | Yes (admin) | - | 204 | <<routes/users.js:112>> |

### Request/Response Schemas (Extract from code validators or examples)

<<Paste actual schemas found in code>>

---

## 16. Integration Points (External Systems)

| External System | Purpose | Protocol | Auth Method | Evidence |
| ---------------- | --------- | ---------- | ------------- | ---------- |
| <<Payment Gateway>> | Process payments | REST API | API Key | <<services/payment.js:34>> |
| <<Email Service>> | Send notifications | SMTP | Username/Password | <<services/email.js:56>> |
| <<Analytics>> | Track events | HTTP POST | Bearer token | <<services/analytics.js:78>> |

**Evidence**: Scan for external HTTP calls, SDK usage, message queue producers/consumers

---

## 17. Known Quirks & Legacy Behaviors

### Quirk 1: <<Name>>

- **Description**: <<What happens>>
- **Evidence**: <<file:line>>
- **Root Cause**: <<Why it exists (workaround, bug, limitation)>>
- **Impact**: <<Who is affected, when>>
- **Related State Machine**: SM-<<id>> (if applicable)
- **Related Config**: CFG-<<id>> (if applicable)
- **Decision Needed**: Preserve or fix in modernization?

### Quirk 2: <<Name>>

<<Repeat>>

---

## 18. Risks, Assumptions, Decisions (RAD)

### Risks (Identified from Code Analysis)

| Risk | Evidence | Impact | Mitigation |
| ------ | ---------- | -------- | ------------ |
| <<Missing input validation>> | <<file:line>> | HIGH | Add validation layer |
| <<Hardcoded credentials>> | <<file:line>> | CRITICAL | Move to secrets manager |
| <<Race condition in concurrent writes>> | <<file:line>> | MEDIUM | Add locking mechanism |

### Assumptions (Made During Analysis)

1. <<Assumption 1>>: <<Description>> (Unable to verify from code; needs user confirmation)
2. <<Assumption 2>>: <<Description>>

### Decisions Needed

1. **<<Decision 1>>**: Should we preserve <<legacy quirk X>>?
   **Options**: A) Preserve, B) Fix
   **Owner**: User
   **Deadline**: Before modernization begins

---

## 19. Value / Business Case (Legacy System)

### Current Value Delivered

Based on code analysis, the legacy system delivers:

- <<Value 1>>: <<Quantify if possible (N users, M transactions/day)>>
- <<Value 2>>: <<Business capability>>
- <<Value 3>>: <<Cost savings/revenue>>

### Modernization Drivers

Why modernize (inferred from code analysis):

1. **Technical Debt**: <<Language version EOL, framework outdated, etc.>>
2. **Performance Issues**: <<Identified bottlenecks from code>>
3. **Security Risks**: <<Vulnerabilities found>>
4. **Scalability Limits**: <<Architecture constraints>>

---

## 20. Traceability Matrix

### Requirements to Evidence

| Requirement | Use Case | User Story | Business Logic | State Machine | Config | Evidence |
|-------------|----------|------------|----------------|---------------|--------|----------|
| FR-CRIT-001 | UC-001 | US-CRIT-001 | BL-001 | SM-001 | CFG-001 | <<file:line>> |
| FR-CRIT-002 | UC-002 | US-CRIT-002 | BL-002 | - | - | <<file:line>> |
| FR-STD-001 | UC-003 | US-STD-001 | BL-003 | - | CFG-002 | <<file:line>> |

---

## 21. Next Steps

1. **User Review**: Validate extracted features, use cases, and quirks with stakeholders
2. **Decision Points**: Resolve all "Decision Needed" items in FR-QUIRK sections
3. **Clarifications**: Address assumptions that couldn't be verified from code
4. **State Machine Validation**: Confirm state transitions match expected behavior
5. **Configuration Review**: Verify all config-driven behaviors are documented
6. **Modernization Planning**: Use this spec as input to technical-spec-target.md

---

## Appendix A: Analysis Metadata

- **Files Analyzed**: <<N>> files
- **Lines of Code**: <<M>> LOC
- **Languages Detected**: <<List>>
- **Frameworks Detected**: <<List>>
- **Database**: <<Type, version>>
- **Analysis Tool**: AI Agent with legacy code analysis capability
- **Analysis Duration**: <<X>> hours/minutes
- **Confidence Level**: <<HIGH/MEDIUM/LOW>> based on code completeness

---

## Appendix B: Glossary

| Term | Definition | Context |
|------|------------|---------|
| <<Term 1>> | <<Definition>> | <<Where used>> |
| <<Term 2>> | <<Definition>> | <<Where used>> |

---

## Appendix C: Reference Diagrams

### System Context Diagram

```mermaid
C4Context
    title System Context - <<Project Name>>

    Person(user, "<<User Type>>", "<<Description>>")
    System(system, "<<System Name>>", "<<Description>>")
    System_Ext(ext1, "<<External System 1>>", "<<Description>>")
    System_Ext(ext2, "<<External System 2>>", "<<Description>>")

    Rel(user, system, "<<Uses>>")
    Rel(system, ext1, "<<Integrates with>>")
    Rel(system, ext2, "<<Integrates with>>")
```

---

## END OF FUNCTIONAL SPECIFICATION

This document serves as the "WHAT" for the modernization effort.
<!-- Note: This template is used for BOTH functional-spec-legacy.md and functional-spec-target.md -->
<!-- The corresponding technical spec depends on context: -->
<!--   - functional-spec-legacy.md → technical-spec-legacy.md (current architecture) -->
<!--   - functional-spec-target.md → technical-spec-target.md (target architecture) -->
For "HOW" (architecture, target stack, migration), see the corresponding technical specification.
