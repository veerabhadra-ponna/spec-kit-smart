---
stage: technical_spec_target
requires: technical-spec-legacy complete
condition: state.analysis_scope == "A"
outputs: technical_spec_target_complete
version: 3.2.0
next: 06d-stage-prompts.md
---

# Stage 6C2: Technical Specification - Target System

## Purpose

Generate technical specification documenting HOW to build the MODERNIZED system. This is the second of two required technical specs for Full Application Modernization.

---

## [!] IMPORTANT: "Part" vs CLI "--chunk"

This prompt uses **"Part 1-5"** to describe content sections to write incrementally.

**These are NOT CLI `--chunk` parameters!**

- [x] DO NOT run `speckitadv analyze-project --chunk=5` to continue
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
speckitadv write-report <filename> --stage=06c2-technical-spec-target --append --content '<content>'
```

**For content > 2000 chars, use stdin mode:**

```powershell
@"
<markdown content here>
"@ | speckitadv write-report <filename> --stage=06c2-technical-spec-target --append --stdin
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
2. Confirm `technical_spec_legacy_complete` = true
3. Load user's modernization preferences from state.json (in `modernization_preferences` field)

**IF not complete:** STOP - Return to 06c1-technical-spec-legacy.md

---

## Source of Truth

**Sources:**

- `{reports_dir}/analysis-report.md`
- `{reports_dir}/technical-spec-legacy.md` (current architecture reference)
- `{analysis_dir}/state.json` (`modernization_preferences` field - 10 questions)
- Both functional specs for feature reference

**Template:**

{{include:technical-spec-template.md}}

**Note on Template vs Prompt Sections**: This prompt uses a condensed 12-section structure that
maps to the full 23-section template as follows:

| Prompt Section | Template Sections | Content |
|----------------|-------------------|---------|
| 1. Introduction | Header + Intro | Purpose, scope, audience |
| 2. Architecture Overview | 1, 2, 8 | Principles, C4 diagrams, patterns |
| 3. Legacy vs Target | 3 | Comparison table, migration impact |
| 4. Target Tech Stack | 13 | Q1-Q4 preferences, versions |
| 5. Data Architecture | 12 | Schema, migration plan, ERD |
| 6. API Design | 4, 11 | Endpoints, contracts, versioning |
| 7. Integration Architecture | 6 | External systems, Q3 message bus |
| 8. Security Architecture | 16 | Q9 approach, auth, data protection |
| 9. Deployment Architecture | 5, 15, 20-22 | Q5-Q7, ADR, IaC, CI/CD |
| 10. Testing Strategy | 19 | Q10 approach, test pyramid |
| 11. Observability | 14, 15 | Q8 stack, metrics, dashboards |
| 12. Migration Risks | 17, 18 | Risk matrix, rollback, success criteria |

**[TARGET ONLY] Sections**: Include ADR (20), IaC (21), CI/CD (22) for target spec.

---

## [!] MANDATORY MULTI-PART WRITING

[STOP] **STOP - READ THIS FIRST BEFORE GENERATING ANYTHING**

**DO NOT generate the entire technical spec in one operation.**

**DO NOT create all sections at once.**

**DO NOT skip the writing strategy below.**

**YOU MUST generate the spec in 5 separate parts as specified below.**

Attempting to generate the full spec in one operation WILL result in:

- Incomplete sections due to token limits
- Missing user preference mappings
- Missing or broken Mermaid diagrams
- Placeholder content (TODO, TBD)
- Verification failures
- Wasted time and compute resources

**If you are about to say "I'll create it in one operation" -> STOP and read the writing strategy below.**

---

## Multi-Part Writing Strategy

**CRITICAL**: The technical-spec-target.md size will vary based on project complexity:

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
# Check if technical-spec-target.md already exists
if [ -f "{reports_dir}/technical-spec-target.md" ]; then
  # Spec exists - check content to determine resume point
  # Look for section headers to determine last completed part
fi
```

**Step 2: Determine resume point from spec content**:

**IF** technical-spec-target.md exists AND is incomplete:

1. Read `{reports_dir}/technical-spec-target.md`
2. Identify last completed part by checking which section headers exist
3. Display resume message:

   ```text
   [!] RESUMING INTERRUPTED GENERATION

   Last completed: Part 2 (Target Tech Stack + Data Architecture)
   Resuming from: Part 3 (API Design + Integration Architecture)

   Continuing generation...
   ```

4. Skip completed parts
5. Start generation from next incomplete part

**IF** technical-spec-target.md does NOT exist:

- Start fresh from Part 1

---

## Spec Structure (5 Parts)

Generate spec in `{reports_dir}/technical-spec-target.md`

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

### Part 1: Architecture Overview + Legacy vs Target

Generate Sections 1, 2, and 3.

---

[STOP: GENERATE_PART_1]**

#### Section 1: Introduction

- Document purpose
- Technical audience
- Scope of implementation

#### Section 2: Architecture Overview

```markdown
## 2. Architecture Overview

### 2.1 System Context (C4 Level 1)

{Mermaid diagram showing system in context}

### 2.2 Container View (C4 Level 2)

{Mermaid diagram showing containers/services}

### 2.3 Architecture Style

- Pattern: {Monolith | Microservices | Modular Monolith}
- Justification: {based on user preferences}
```

#### Section 3: Legacy vs Target Comparison

| Aspect | Legacy | Target | Migration Impact |
|--------|--------|--------|------------------|
| Language | {current} | Q1: {answer} | {impact} |
| Database | {current} | Q2: {answer} | {impact} |
| Deployment | {current} | Q5: {answer} | {impact} |

**Completion Criteria**:

- [ok] C4 diagrams for target architecture
- [ok] Legacy vs Target comparison table
- [ok] User preferences (Q1, Q2, Q5) applied
- [ok] NO placeholders

**After Part 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `{reports_dir}/technical-spec-target.md`
   - Content: Complete Sections 1-3

2. **Verify:** Read file, confirm diagrams render correctly.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 1/5 complete: Architecture + Legacy vs Target Comparison
     - C4 Diagrams: 2
     - Target Language: {Q1 answer}
     - Target Database: {Q2 answer}
     - Lines generated: [COUNT]

   ```

---

### Part 2: Target Tech Stack + Data Architecture

Generate Sections 4 and 5 using user's Q1-Q4 answers.

---

[STOP: GENERATE_PART_2]**

#### Section 4: Target Technology Stack

Based on user's 10 questions:

```markdown
## 4. Target Technology Stack

### 4.1 Runtime & Language

- **Target:** {Q1 answer}
- **Version:** {specific version}
- **Migration from:** {legacy language/version}

### 4.2 Database

- **Target:** {Q2 answer}
- **Migration Strategy:** {approach}
- **Schema Changes:** {summary}

### 4.3 Message Bus

- **Target:** {Q3 answer}
- **Use Cases:** {async patterns}

### 4.4 Package Management

- **Target:** {Q4 answer}
- **Dependency Strategy:** {approach}
```

#### Section 5: Data Architecture

```markdown
## 5. Data Architecture

### 5.1 Database Design

{ERD diagram in Mermaid}

### 5.2 Data Flow

{Data flow diagram showing system data paths}

### 5.3 Migration Plan

| Table | Legacy Schema | Target Schema | Migration |
|-------|--------------|---------------|-----------|
| {table} | {columns} | {columns} | {approach} |
```

**Completion Criteria**:

- [ok] User preferences Q1-Q4 applied correctly
- [ok] ERD diagram for target data model
- [ok] Migration plan for each entity
- [ok] NO placeholders

**After Part 2 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 4 and 5 to technical-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 2/5 complete: Target Tech Stack + Data Architecture
     - Target Language: {Q1}
     - Target Database: {Q2}
     - Target Message Bus: {Q3}
     - Entities with migration plan: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 3: API Design + Integration Architecture

Generate Sections 6 and 7.

---

[STOP: GENERATE_PART_3]**

#### Section 6: API Design

```markdown
## 6. API Design

### 6.1 API Style

- Style: {REST | GraphQL | gRPC}
- Versioning: {strategy}

### 6.2 Endpoint Catalog

| Endpoint | Method | Purpose | Legacy Equiv |
|----------|--------|---------|--------------|
| {path} | {method} | {purpose} | {legacy ref} |

### 6.3 API Contract Examples

{OpenAPI/GraphQL schema snippets}
```

#### Section 7: Integration Architecture

```markdown
## 7. Integration Architecture

### 7.1 External Systems

{Sequence diagram showing integrations}

### 7.2 Integration Points

| System | Protocol | Auth | Data Format |
|--------|----------|------|-------------|
| {system} | {protocol} | {auth} | {format} |

### 7.3 Message Queue Patterns

- Pattern: {Pub/Sub | Request/Reply | Event Sourcing}
- Queue: {Q3 answer}
```

**Completion Criteria**:

- [ok] All API endpoints mapped from legacy
- [ok] Integration sequence diagrams included
- [ok] Message queue patterns from Q3 applied
- [ok] NO placeholders

**After Part 3 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 6 and 7 to technical-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 3/5 complete: API Design + Integration Architecture
     - Endpoints mapped: [COUNT]
     - Integrations documented: [COUNT]
     - Message Queue: {Q3 answer}
     - Lines generated: [COUNT]

   ```

---

### Part 4: Security + Deployment

Generate Sections 8 and 9 using Q5, Q6, Q7, Q9 answers.

---

[STOP: GENERATE_PART_4]**

#### Section 8: Security Architecture

Based on Q9 (Security approach):

```markdown
## 8. Security Architecture

### 8.1 Authentication

- Approach: {Q9 answer}
- Implementation: {details}

### 8.2 Authorization

- Model: {RBAC | ABAC | etc.}
- Enforcement: {where/how}

### 8.3 Data Protection

- Encryption at rest: {approach}
- Encryption in transit: {approach}
- Secrets management: {approach}

### 8.4 Security Checklist

- [ ] OWASP Top 10 mitigations
- [ ] Input validation
- [ ] Output encoding
- [ ] Rate limiting
```

#### Section 9: Deployment Architecture

Based on Q5 (Deployment), Q6 (IaC), Q7 (Containers):

```markdown
## 9. Deployment Architecture

### 9.1 Target Environment

- Platform: {Q5 answer}
- Container: {Q7 answer}
- IaC Tool: {Q6 answer}

### 9.2 Deployment Diagram

{Mermaid diagram showing deployment topology}

### 9.3 CI/CD Pipeline

{Pipeline stages and gates}

### 9.4 Environment Strategy

| Environment | Purpose | Config |
|-------------|---------|--------|
| dev | Development | {config} |
| staging | Pre-prod | {config} |
| prod | Production | {config} |
```

**Completion Criteria**:

- [ok] User preferences Q5, Q6, Q7, Q9 applied
- [ok] Deployment diagram included
- [ok] CI/CD pipeline defined
- [ok] NO placeholders

**After Part 4 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 8 and 9 to technical-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 4/5 complete: Security + Deployment
     - Security Approach: {Q9}
     - Deployment Target: {Q5}
     - Container: {Q7}
     - IaC Tool: {Q6}
     - Lines generated: [COUNT]

   ```

---

### Part 5: Testing + Observability + Migration Risks

Generate Sections 10, 11, and 12 using Q8, Q10 answers.

---

[STOP: GENERATE_PART_5]**

#### Section 10: Testing Strategy

Based on Q10 (Testing approach):

```markdown
## 10. Testing Strategy

### 10.1 Testing Approach

- Strategy: {Q10 answer}
- Coverage Target: {percentage}

### 10.2 Test Pyramid

| Level | Tool | Coverage |
|-------|------|----------|
| Unit | {tool} | {target}% |
| Integration | {tool} | {target}% |
| E2E | {tool} | {target}% |

### 10.3 Migration Testing

- Feature parity tests
- Performance regression tests
- Data integrity verification
```

#### Section 11: Observability

Based on Q8 (Observability stack):

```markdown
## 11. Observability

### 11.1 Stack

- Metrics: {Q8 metrics answer}
- Logging: {Q8 logging answer}
- Tracing: {Q8 tracing answer}

### 11.2 Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| {metric} | {target} | {threshold} |

### 11.3 Dashboards

- {dashboard 1 purpose}
- {dashboard 2 purpose}
```

#### Section 12: Migration Risks & Mitigations

```markdown
## 12. Migration Risks

### 12.1 Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {risk} | {H/M/L} | {H/M/L} | {strategy} |

### 12.2 Rollback Strategy

- Trigger conditions
- Rollback procedure
- Data recovery

### 12.3 Success Criteria

- [ ] All features migrated
- [ ] Performance meets targets
- [ ] Zero data loss
- [ ] All tests passing
```

**Completion Criteria**:

- [ok] User preferences Q8, Q10 applied
- [ok] Migration risks documented
- [ok] Rollback strategy defined
- [ok] NO placeholders

**After Part 5 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 10, 11, and 12 to technical-spec-target.md

2. **Verify:** Read complete file, confirm:
   - All 12 sections present
   - User preferences (Q1-Q10) correctly applied
   - Diagrams rendered correctly
   - No placeholders or TODOs

3. **MANDATORY - Display progress and final summary**:

   ```text
   [ok] Part 5/5 complete: Testing + Observability + Migration Risks
     - Testing Strategy: {Q10}
     - Observability Stack: {Q8}
     - Migration risks documented: [COUNT]
     - Lines generated: [COUNT]

   [ok] technical-spec-target.md GENERATION COMPLETE
      Total sections: 12
      Total diagrams: [COUNT]
      Total lines: [COUNT]
      File path: {reports_dir}/technical-spec-target.md

   ```

---

## Verification Gate (HARD STOP)

[!] **VERIFICATION GATE - CANNOT PROCEED WITHOUT PASSING**

**BEFORE** proceeding to 06d-stage-prompts.md, verify spec quality:

### Verification Checklist

Read technical-spec-target.md and verify:

- [ ] File exists at expected path: `{reports_dir}/technical-spec-target.md`
- [ ] All 12 section headers present:
      - [ ] Section 1: Introduction
      - [ ] Section 2: Architecture Overview (with C4 diagrams)
      - [ ] Section 3: Legacy vs Target Comparison
      - [ ] Section 4: Target Technology Stack
      - [ ] Section 5: Data Architecture (with ERD)
      - [ ] Section 6: API Design
      - [ ] Section 7: Integration Architecture
      - [ ] Section 8: Security Architecture
      - [ ] Section 9: Deployment Architecture
      - [ ] Section 10: Testing Strategy
      - [ ] Section 11: Observability
      - [ ] Section 12: Migration Risks
- [ ] Quality checks:
      - [ ] User preferences (Q1-Q10) correctly applied
      - [ ] C4 diagrams for target architecture
      - [ ] ERD diagram for target data model
      - [ ] Deployment diagram present
      - [ ] Migration risks have severity ratings
      - [ ] Rollback strategy defined
      - [ ] No placeholders (TODO, TBD, "will be analyzed", "coming soon")
      - [ ] All Mermaid diagrams render correctly
- [ ] Completeness (verify based on project size/complexity):
      - [ ] **Small projects (< 5,000 LOC)**:
            - Total lines: 800+ (minimum)
            - Diagrams: 4+ (C4x2, ERD, deployment)
            - Migration risks: 5-10
      - [ ] **Medium projects (5,000-50,000 LOC)**:
            - Total lines: 2,000+ (minimum)
            - Diagrams: 6+ (C4x2, ERD, deployment, sequence, data flow)
            - Migration risks: 10-20
      - [ ] **Large projects (> 50,000 LOC)**:
            - Total lines: 4,000+ (minimum)
            - Diagrams: 8+ (multiple of each type)
            - Migration risks: 20-40

---

### Recovery Actions (IF ANY CHECKBOX FAILS)

**IF ANY checkbox is unchecked**:

```text
[x] VERIFICATION FAILED

technical-spec-target.md is incomplete. Issues found:
- [List specific missing items from checklist above]
```

**RECOVERY DECISION TREE**:

**1. Identify incomplete sections**:

List which sections or quality checks failed verification.

**2. Determine recovery approach**:

**IF** entire sections missing (e.g., Section 8 not found in file):

- **Action**: Regenerate ONLY the missing sections
- **Method**:
  1. Check technical-spec-target.md content to identify last completed section
  2. Resume generation from first missing section
  3. Use Edit tool to append missing sections to existing file
  4. Re-run verification after regeneration

**IF** quality issues in existing sections (e.g., user preferences not applied):

- **Action**: Fix the problematic section with correct preferences
- **Method**:
  1. Read the problematic section from technical-spec-target.md
  2. Identify specific issues (wrong Q values, broken diagrams, etc.)
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
  [A] Regenerate entire technical-spec-target.md from scratch
  [B] Fix individual sections (may take longer)
  [C] Proceed anyway (NOT RECOMMENDED - will cause issues in next stage)

  Your choice: ___
  ```

**3. Execute recovery**:

- Based on failure type, perform specific recovery actions
- Use appropriate tools (Edit for fixes, Write for full regen)
- Re-run verification after recovery
- **DO NOT proceed to 06d until verification passes**

[!] **STOP HERE** - DO NOT CONTINUE TO NEXT STAGE UNTIL VERIFICATION PASSES

---

### Verification Success

**IF ALL checkboxes are checked**:

```text
[ok] VERIFICATION PASSED

technical-spec-target.md is complete and meets quality standards:
- All 12 sections present and complete
- User preferences (Q1-Q10) correctly applied
- C4 diagrams for target architecture
- ERD and deployment diagrams present
- Migration risks documented with mitigations
- Rollback strategy defined
- No placeholders or incomplete sections
- Total lines: [COUNT] (comprehensive spec)

Proceeding to 06d-stage-prompts.md...
```

**Only after passing verification**: Proceed to next stage

---

## Both Technical Specs Complete

```text
===========================================================
  BOTH TECHNICAL SPECS COMPLETE

  1. technical-spec-legacy.md - LEGACY system (how it's built today)
  2. technical-spec-target.md - TARGET system (how it will be built)

  Chain ID: {chain_id}

  User Preferences Applied:
    Q1 Language: {answer}
    Q2 Database: {answer}
    Q3 Message Bus: {answer}
    Q4 Package Manager: {answer}
    Q5 Deployment: {answer}
    Q6 IaC: {answer}
    Q7 Container: {answer}
    Q8 Observability: {answer}
    Q9 Security: {answer}
    Q10 Testing: {answer}

  Now proceeding to stage-prompts...
===========================================================

ARTIFACT_COMPLETE:TECHNICAL_SPEC_TARGET
```

---

**[GATE-CHECK]** If verification PASSES: auto-continue to next stage.
If verification FAILS: present recovery options and WAIT for user decision.

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
