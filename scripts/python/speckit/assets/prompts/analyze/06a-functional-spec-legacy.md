---
stage: functional_spec_legacy
requires: analyze-project-05-artifacts.json
condition: state.analysis_scope == "A"
outputs: functional_spec_legacy_complete
version: 3.2.0
next: 06b-functional-spec-target.md
---

# Stage 6A: Functional Specification - Legacy System

## Purpose

Generate functional specification documenting WHAT the LEGACY/EXISTING system CURRENTLY does. This is the first of two required functional specs for Full Application Modernization.

---

## [!] IMPORTANT: "Part" vs CLI "--chunk"

This prompt uses **"Part 1-7"** to describe content sections to write incrementally.

**These are NOT CLI `--chunk` parameters!**

- [x] DO NOT run `speckitadv analyze-project --chunk=2` to continue
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
speckitadv write-report <filename> --stage=06a-functional-spec-legacy --append --content '<content>'
```

**For content > 2000 chars, use stdin mode:**

```powershell
@"
<markdown content here>
"@ | speckitadv write-report <filename> --stage=06a-functional-spec-legacy --append --stdin
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
2. Confirm `common_artifacts_complete` = true
3. Confirm `analysis_scope` = "A"

**IF not complete:** STOP - Return to 05a-executive-summary.md

---

## Source of Truth

**Use ONLY these sources:**

- `{reports_dir}/analysis-report.md` Phase 2 (Feature Catalog)
- `{reports_dir}/analysis-report.md` Phase 3 (Positive Findings)

**Template:**

{{include:functional-spec-template.md}}

---

## Content Rules

| Rule | Requirement |
|------|-------------|
| Features | Extract from analysis-report.md exactly as analyzed |
| References | Every feature MUST include `file:line` notation |
| Technology | Describe as-implemented (current state) |
| Tense | Present tense ("The system validates...") |
| Scope | Document what EXISTS, not what's missing |

**Forbidden:** Do NOT include modernization preferences, target stack, or future state.

---

## [!] MANDATORY MULTI-PART WRITING

[STOP] **STOP - READ THIS FIRST BEFORE GENERATING ANYTHING**

**DO NOT generate the entire functional spec in one operation.**

**DO NOT create all sections at once.**

**DO NOT skip the writing strategy below.**

**YOU MUST generate the spec in 5 separate parts as specified below.**

Attempting to generate the full spec in one operation WILL result in:

- Incomplete sections due to token limits
- Missing file:line references
- Placeholder content (TODO, TBD)
- Verification failures
- Wasted time and compute resources

**If you are about to say "I'll create it in one operation" -> STOP and read the writing strategy below.**

---

## Multi-Part Writing Strategy

**CRITICAL**: The functional-spec-legacy.md size will vary based on project complexity:

- **Small projects** (< 5,000 LOC): **500-1,500 lines**
- **Medium projects** (5,000-50,000 LOC): **1,500-3,500 lines**
- **Large projects** (> 50,000 LOC): **3,000-6,000+ lines**

**[!] COMPLETION-BASED WRITING (NOT size-based)**:

Use **completion-based writing**, NOT size-based writing:

- Generate complete logical sections in each part
- Each part ends with a distinct completion point
- Display progress after each part (MANDATORY)
- NO placeholders allowed (no TODO, TBD, "will be analyzed")

**Why multi-part writing is critical**:

- Large specs may hit token limits without multi-part writing
- Progress tracking improves user experience
- Verification gates ensure quality at each step

---

## Resume Detection (BEFORE Starting)

**BEFORE generating any parts**, check for interrupted generation:

**Step 1: Check for existing spec**:

```bash
# Check if functional-spec-legacy.md already exists
if [ -f "{reports_dir}/functional-spec-legacy.md" ]; then
  # Spec exists - check content to determine resume point
  # Look for section headers to determine last completed part
fi
```

**Step 2: Determine resume point from spec content**:

**IF** functional-spec-legacy.md exists AND is incomplete:

1. Read `{reports_dir}/functional-spec-legacy.md`
2. Identify last completed part by checking which section headers exist
3. Display resume message:

   ```text
   [!] RESUMING INTERRUPTED GENERATION

   Last completed: Part 2 (User Stories - CRITICAL)
   Resuming from: Part 3 (User Stories - STANDARD + Business Rules)

   Continuing generation...
   ```

4. Skip completed parts
5. Start generation from next incomplete part

**IF** functional-spec-legacy.md does NOT exist:

- Start fresh from Part 1

---

## Spec Structure (7 Parts)

Generate spec in `{reports_dir}/functional-spec-legacy.md`

**[!] GENERATION ORDER - STRICTLY ENFORCED**:

1. Generate ONLY Part 1 first
2. Wait for Part 1 completion
3. THEN generate Part 2
4. Continue sequentially through all 7 parts

**DO NOT**:

- [x] Generate multiple parts in one response
- [x] Generate all sections at once
- [x] Skip progress display

**IF** you find yourself generating more than one part at a time -> **STOP IMMEDIATELY**

---

### Part 1: Executive Summary + Current State + Personas

Generate Sections 1, 2, and 3.

---

[STOP: GENERATE_PART_1]**

Generate the following sections:

#### Section 1: Executive Summary

- High-level functionality summary
- Key capabilities
- System boundaries

#### Section 2: Current State - Problem & Goals

- Current system overview
- Problems being addressed
- Goals and objectives

#### Section 3: Personas & User Journeys

- User personas
- User journey maps
- Key user interactions

**Completion Criteria**:

- [ok] Project context established
- [ok] System boundaries defined
- [ok] User personas documented
- [ok] NO placeholders

**After Part 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `{reports_dir}/functional-spec-legacy.md`
   - Content: Complete Sections 1-3

2. **Verify:** Read file, confirm no placeholders, all sections complete.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 1/7 complete: Executive Summary + Current State + Personas
     - Sections completed: 3
     - Lines generated: [COUNT]

   ```

---

### Part 2: Use Cases + User Stories

Generate Sections 4 and 5.

---

[STOP: GENERATE_PART_2]**

#### Section 4: Use Cases (Extracted from Code)

Extract use cases from analysis-report.md. For each use case:

```markdown
### UC-{id}: {Use Case Name}

**Priority:** {CRITICAL | STANDARD}
**Source:** {file}:{line}

**Actors:** {Primary actor(s)}
**Preconditions:** {Required state before}
**Main Flow:**
1. {Step 1}
2. {Step 2}

**Alternate Flows:**
- {Alternative path}

**Postconditions:** {State after completion}
```

#### Section 5: User Stories (Given-When-Then Format)

Extract all user stories. For each story:

```markdown
### US-{CRIT|STD}-{id}: {Story Name}

**Priority:** {CRITICAL | STANDARD}
**Source:** {file}:{line}

**As a** {actor}
**I want to** {action}
**So that** {benefit}

**Given** {precondition}
**When** {action}
**Then** {expected result}

**Acceptance Criteria:**
- [ ] {criterion 1}
- [ ] {criterion 2}
```

**Completion Criteria**:

- [ok] ALL use cases from analysis-report.md documented
- [ok] ALL user stories with file:line references
- [ok] Acceptance criteria for each story
- [ok] NO placeholders

**After Part 2 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 4-5 content to functional-spec-legacy.md

2. **Verify:** Read file, confirm all use cases and stories documented with file:line references.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 2/7 complete: Use Cases + User Stories
     - Use cases documented: [COUNT]
     - User stories documented: [COUNT]
     - File:line references: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 3: Business Logic + State Machines + Config Behaviors

Generate Sections 6, 7, and 8.

---

[STOP: GENERATE_PART_3]**

#### Section 6: Business Logic (Algorithms, Rules & Calculations)

Document all business logic using structured formats:

```markdown
### 6.1 Core Processing Algorithms

ALGORITHM: {AlgorithmName}
PURPOSE: {What it does}
INPUT: {Input parameters}
OUTPUT: {Return value/side effects}
STEPS:
  1. {Step description}
  2. {Step description}
ERROR HANDLING: {Error conditions and responses}
RETURN: {Return value}

### 6.2 Decision Trees

DECISION: {Decision Name}
IF: {condition}
THEN: {action}
BECAUSE: {business reason}

### 6.3 Calculation Formulas

FORMULA: {FormulaName}
EXPRESSION: {mathematical expression}
PRECISION: {decimal places, rounding rules}
CONSTRAINTS: {min/max values, edge cases}

### 6.4 Business Constants

| Constant | Value | Source | Purpose |
|----------|-------|--------|---------|
| {NAME} | {value} | {file:line} | {why} |

### 6.5 Validation Rules

| Rule ID | Field | Validation | Error Message | Source |
|---------|-------|------------|---------------|--------|
| VR-001 | {field} | {rule} | {message} | {file:line} |
```

#### Section 7: State Machines

Document all state-based behaviors.

#### Section 8: Configuration-Driven Behaviors

Document all config-dependent logic.

**Completion Criteria**:

- [ok] ALL algorithms documented with STEPS format
- [ok] Decision trees with business reasoning (BECAUSE)
- [ok] Calculation formulas with PRECISION
- [ok] Business constants with sources
- [ok] State machines with transitions
- [ok] Config behaviors documented
- [ok] NO placeholders

**After Part 3 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 6-8 to functional-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 3/7 complete: Business Logic + State Machines + Config
     - Algorithms documented: [COUNT]
     - Decision trees: [COUNT]
     - Calculation formulas: [COUNT]
     - State machines: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 4: Scope + Requirements + NFRs + Error Handling

Generate Sections 9, 10, 11, 12, and 13.

---

[STOP: GENERATE_PART_4]**

#### Section 9: Scope / Out-of-Scope

Document what is included and excluded.

#### Section 10: Functional Requirements (Extracted from Legacy Code)

Extract all functional requirements with priorities.

#### Section 11: Non-Negotiables (Extracted from Code Analysis)

Document constraints that cannot be changed.

#### Section 12: Non-Functional Requirements (Legacy System)

| Category | Current State | Evidence |
|----------|--------------|----------|
| Performance | {metrics} | {file:line} |
| Security | {implementation} | {file:line} |
| Scalability | {approach} | {file:line} |
| Reliability | {mechanisms} | {file:line} |

[CONDITIONAL] Include Audit Trail subsection if compliance requirements detected.

#### Section 13: Error Handling & Recovery

Document all error handling patterns:

```markdown
### 13.1 Exception Handling Patterns

EXCEPTION: {ExceptionName}
TRIGGER: {What causes this exception}
HANDLER: {How it is handled}
RECOVERY: {Recovery action}
USER_MESSAGE: {What user sees}
LOGGING: {What is logged}
SOURCE: {file:line}

### 13.2 Error Recovery Algorithms

RECOVERY: {RecoveryName}
TRIGGER: {Error condition}
STEPS:
  1. {Recovery step}
  2. {Recovery step}
FALLBACK: {If recovery fails}
SOURCE: {file:line}

### 13.3 Error Codes Catalog

| Code | Category | Description | User Action | Source |
|------|----------|-------------|-------------|--------|
| E001 | {category} | {description} | {action} | {file:line} |
```

**Completion Criteria**:

- [ok] Scope clearly defined
- [ok] All functional requirements documented
- [ok] Non-negotiables identified
- [ok] All NFR categories documented with evidence
- [ok] Error handling patterns extracted
- [ok] Recovery algorithms documented
- [ok] NO placeholders

**After Part 4 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 9-13 to functional-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 4/7 complete: Scope + Requirements + NFRs + Error Handling
     - Functional requirements: [COUNT]
     - Non-negotiables: [COUNT]
     - NFR categories: [COUNT]
     - Error patterns: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 5: Data Models + Config Mapping + API + Integration

Generate Sections 14, 15, 16, and 17.

---

[STOP: GENERATE_PART_5]**

#### Section 14: Data Models (Extracted from DB Schemas)

Document all data entities with field mappings:

```markdown
### Entity: {Name}

**Source:** {file}:{line}

| Field | Type | Constraints |
|-------|------|-------------|
| {field} | {type} | {constraints} |

**Relationships:**
- {relationship description}

### 14.2 Field Mappings

| Source Field | Target Field | Transformation | Validation |
|--------------|--------------|----------------|------------|
| {source} | {target} | {transform} | {validation} |

### 14.3 Data Validation Rules

| Rule | Field(s) | Validation | Error |
|------|----------|------------|-------|
| DVR-001 | {field} | {validation} | {error} |
```

#### Section 15: Configuration Mapping (All Config Files)

Document all configuration sources.

#### Section 16: API Contracts (Extracted from Code)

Document all API endpoints and contracts.

#### Section 17: Integration Points (External Systems)

Document all external integrations.

[CONDITIONAL] Include Message Formats subsection if event-driven architecture detected.

**Completion Criteria**:

- [ok] All data entities documented with fields
- [ok] Field mappings with transformations
- [ok] Data validation rules extracted
- [ok] Configuration sources mapped
- [ok] API contracts documented
- [ok] Integration points identified
- [ok] NO placeholders

**After Part 5 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 14-17 to functional-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 5/7 complete: Data Models + Config + API + Integration
     - Data entities: [COUNT]
     - Field mappings: [COUNT]
     - API endpoints: [COUNT]
     - Integration points: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 6: Quirks + RAD + Value + Traceability + Next Steps

Generate Sections 18, 19, 20, 21, and 22.

---

[STOP: GENERATE_PART_6]**

#### Section 18: Known Quirks & Legacy Behaviors

Document undocumented behaviors and edge cases.

#### Section 19: Risks, Assumptions, Decisions (RAD)

Document project risks, assumptions made, and decisions needed.

#### Section 20: Value / Business Case (Legacy System)

Document business value and modernization drivers.

#### Section 21: Traceability Matrix

Cross-reference all requirements to evidence.

#### Section 22: Next Steps

Define actions for stakeholder review.

**Completion Criteria**:

- [ok] All quirks and edge cases documented
- [ok] Risks and assumptions identified
- [ok] Business value articulated
- [ok] Traceability matrix complete
- [ok] Next steps defined
- [ok] NO placeholders

**After Part 6 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 18-22 to functional-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 6/7 complete: Quirks + RAD + Value + Traceability + Next Steps
     - Quirks documented: [COUNT]
     - Risks identified: [COUNT]
     - Assumptions made: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 7: Preservation Checklists + Appendices

Generate Sections 23, 24, and Appendices A-C.

---

[STOP: GENERATE_PART_7]**

#### Section 23: Business Logic Preservation Checklist

Complete the extraction verification checklist:

- Verify all validation rules extracted
- Verify all calculation formulas with precision
- Verify all decision trees mapped
- Verify all state transitions documented
- Verify all error handling captured

#### Section 24: Output Validation Checklist

Complete the output quality checklist:

- Verify document quality (no placeholders)
- Verify content completeness (all sections)
- Verify traceability (requirements to evidence)
- Verify stakeholder readiness

#### Appendix A: Analysis Metadata

Document analysis statistics.

#### Appendix B: Glossary

Define domain terms.

#### Appendix C: Reference Diagrams

Include system context diagram.

**Completion Criteria**:

- [ok] Preservation checklist completed
- [ok] Validation checklist completed
- [ok] Metadata documented
- [ok] Glossary populated
- [ok] Diagrams included
- [ok] NO placeholders

**After Part 7 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 23-24 and Appendices to functional-spec-legacy.md

2. **MANDATORY - Display progress and final summary**:

   ```text
   [ok] Part 7/7 complete: Checklists + Appendices
     - Preservation items verified: [COUNT]
     - Validation items verified: [COUNT]
     - Glossary terms: [COUNT]
     - Lines generated: [COUNT]

   [ok] functional-spec-legacy.md GENERATION COMPLETE
      Total sections: 24 + 3 appendices
      Total features: [COUNT]
      Total lines: [COUNT]
      File path: {reports_dir}/functional-spec-legacy.md

   ```

---

## Verification Gate (HARD STOP)

[!] **VERIFICATION GATE - CANNOT PROCEED WITHOUT PASSING**

**BEFORE** proceeding to 06b-functional-spec-target.md, verify spec quality:

### Verification Checklist

Read functional-spec-legacy.md and verify:

- [ ] File exists at expected path: `{reports_dir}/functional-spec-legacy.md`
- [ ] All 24 section headers present (core sections):
      - [ ] Section 1: Executive Summary
      - [ ] Section 2: Current State - Problem & Goals
      - [ ] Section 3: Personas & User Journeys
      - [ ] Section 4: Use Cases
      - [ ] Section 5: User Stories
      - [ ] Section 6: Business Logic (with 6.1-6.5 subsections)
      - [ ] Section 7: State Machines
      - [ ] Section 8: Configuration-Driven Behaviors
      - [ ] Section 9: Scope / Out-of-Scope
      - [ ] Section 10: Functional Requirements
      - [ ] Section 11: Non-Negotiables
      - [ ] Section 12: Non-Functional Requirements
      - [ ] Section 13: Error Handling & Recovery
      - [ ] Section 14: Data Models (with Field Mappings)
      - [ ] Section 15: Configuration Mapping
      - [ ] Section 16: API Contracts
      - [ ] Section 17: Integration Points
      - [ ] Section 18: Known Quirks & Legacy Behaviors
      - [ ] Section 19: Risks, Assumptions, Decisions
      - [ ] Section 20: Value / Business Case
      - [ ] Section 21: Traceability Matrix
      - [ ] Section 22: Next Steps
      - [ ] Section 23: Business Logic Preservation Checklist
      - [ ] Section 24: Output Validation Checklist
      - [ ] Appendices A, B, C present
- [ ] Quality checks:
      - [ ] 30+ file:line references present throughout
      - [ ] All use cases have actors and flows
      - [ ] All user stories have acceptance criteria
      - [ ] Business logic has ALGORITHM/DECISION/FORMULA formats
      - [ ] Error handling patterns documented
      - [ ] NFRs have evidence references
      - [ ] Data entities have field definitions and mappings
      - [ ] Preservation checklist items verified
      - [ ] No placeholders (TODO, TBD, "will be analyzed", "coming soon")
      - [ ] All tables properly formatted (Markdown)
- [ ] Completeness (verify based on project size/complexity):
      - [ ] **Small projects (< 5,000 LOC)**:
            - Total lines: 800+ (minimum)
            - Use cases: 5-15
            - User stories: 10-30
            - Business logic items: 5-15
            - Error patterns: 3-10
      - [ ] **Medium projects (5,000-50,000 LOC)**:
            - Total lines: 2,000+ (minimum)
            - Use cases: 15-50
            - User stories: 30-100
            - Business logic items: 15-40
            - Error patterns: 10-30
      - [ ] **Large projects (> 50,000 LOC)**:
            - Total lines: 4,000+ (minimum)
            - Use cases: 50-150
            - User stories: 100-300
            - Business logic items: 40-100
            - Error patterns: 30-80

---

### Recovery Actions (IF ANY CHECKBOX FAILS)

**IF ANY checkbox is unchecked**:

```text
[x] VERIFICATION FAILED

functional-spec-legacy.md is incomplete. Issues found:
- [List specific missing items from checklist above]
```

**RECOVERY DECISION TREE**:

**1. Identify incomplete sections**:

List which sections or quality checks failed verification.

**2. Determine recovery approach**:

**IF** entire sections missing (e.g., Section 5 not found in file):

- **Action**: Regenerate ONLY the missing sections
- **Method**:
  1. Check functional-spec-legacy.md content to identify last completed section
  2. Resume generation from first missing section
  3. Use Edit tool to append missing sections to existing file
  4. Re-run verification after regeneration

**IF** quality issues in existing sections (e.g., no file:line references in Section 4):

- **Action**: Enhance the problematic section with missing details
- **Method**:
  1. Read the incomplete section from functional-spec-legacy.md
  2. Identify specific missing elements (file:line refs, acceptance criteria, etc.)
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
  [A] Regenerate entire functional-spec-legacy.md from scratch
  [B] Fix individual sections (may take longer)
  [C] Proceed anyway (NOT RECOMMENDED - will cause issues in next stage)

  Your choice: ___
  ```

**3. Execute recovery**:

- Based on failure type, perform specific recovery actions
- Use appropriate tools (Edit for fixes, Write for full regen)
- Re-run verification after recovery
- **DO NOT proceed to 06b until verification passes**

[!] **STOP HERE** - DO NOT CONTINUE TO NEXT STAGE UNTIL VERIFICATION PASSES

---

### Verification Success

**IF ALL checkboxes are checked**:

```text
[ok] VERIFICATION PASSED

functional-spec-legacy.md is complete and meets quality standards:
- All 24 sections + 3 appendices present and complete
- 30+ file:line references found
- All use cases have actors and flows
- All user stories have acceptance criteria
- Business logic documented with ALGORITHM/DECISION/FORMULA formats
- Error handling patterns documented
- NFRs have evidence
- Data models have field mappings
- Preservation checklist verified
- No placeholders or incomplete sections
- Total lines: [COUNT] (comprehensive spec)

Proceeding to 06b-functional-spec-target.md...
```

**Only after passing verification**: Proceed to next stage

---

## Completion Marker

```text
===========================================================
  ARTIFACT COMPLETE: FUNCTIONAL-SPEC-LEGACY.md

  Chain ID: {chain_id}
  Features Documented: {count}
  Lines: {count}

  This documents the LEGACY system (what exists today).

  NEXT: Generate functional-spec-target.md (what will be built)
===========================================================

ARTIFACT_COMPLETE:FUNCTIONAL_SPEC_LEGACY
```

---

**[GATE-CHECK]** If verification PASSES: auto-continue to next stage.
If verification FAILS: present recovery options and WAIT for user decision.

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.

**DO NOT:**

- Skip to technical specs
- Skip to stage-prompts/
- Mark Stage 6 complete

**You MUST generate both functional specs before proceeding.**
