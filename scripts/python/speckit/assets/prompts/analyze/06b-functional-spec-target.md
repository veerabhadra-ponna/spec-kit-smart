---
stage: functional_spec_target
requires: functional-spec-legacy complete
condition: state.analysis_scope == "A"
outputs: functional_spec_target_complete
version: 3.2.0
next: 06c1-technical-spec-legacy.md
---

# Stage 6B: Functional Specification - Target System

## Purpose

Generate functional specification documenting WHAT the MODERNIZED system WILL do. This is the second of two required functional specs for Full Application Modernization.

---

## [!] IMPORTANT: "Part" vs CLI "--chunk"

This prompt uses **"Part 1-7"** to describe content sections to write incrementally.

**These are NOT CLI `--chunk` parameters!**

- [x] DO NOT run `speckitadv analyze-project --chunk=3` to continue
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
speckitadv write-report <filename> --stage=06b-functional-spec-target --append --content '<content>'
```

**For content > 2000 chars, use stdin mode:**

```powershell
@"
<markdown content here>
"@ | speckitadv write-report <filename> --stage=06b-functional-spec-target --append --stdin
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
2. Confirm `status` = "complete"
3. Load user's modernization preferences from state.json (in `modernization_preferences` field)

**IF not complete:** STOP - Return to 06a-functional-spec-legacy.md

---

## Source of Truth

**Primary Sources:**

- `{reports_dir}/analysis-report.md` (feature catalog)
- `{analysis_dir}/state.json` (`modernization_preferences` field - 10 questions)
- User's scope validation answers

**Template:**

{{include:functional-spec-template.md}}

---

## Content Rules

| Rule | Requirement |
|------|-------------|
| Base | Legacy features enhanced with modernization improvements |
| Technology | Use user's chosen target stack (from 10 questions) |
| Tense | Future tense ("The system will...", "Users will be able to...") |
| Enhancements | Include new capabilities enabled by modernization |
| Scope Boundaries | Respect IN SCOPE vs OUT OF SCOPE from user answers |
| Diagrams | Use Mermaid syntax for all diagrams (flowcharts, state machines, journeys) |

---

## Scope Boundary Rules

Review user's answers from Stage 3A:

| User Answer | Scope Status | Action |
|-------------|--------------|--------|
| Explicit target (e.g., "PostgreSQL 15") | IN SCOPE | Document migration |
| Skipped/Enter pressed | OUT OF SCOPE | Document "Use existing as-is" |
| "Keep current" | OUT OF SCOPE | Document no change |

**DO NOT assume migration for unmentioned components.**

---

## [!] MANDATORY MULTI-PART WRITING

[STOP] **STOP - READ THIS FIRST BEFORE GENERATING ANYTHING**

**DO NOT generate the entire functional spec in one operation.**

**DO NOT create all sections at once.**

**DO NOT skip the writing strategy below.**

**YOU MUST generate the spec in 7 separate parts as specified below.**

Attempting to generate the full spec in one operation WILL result in:

- Incomplete sections due to token limits
- Missing modernization mappings
- Placeholder content (TODO, TBD)
- Verification failures
- Wasted time and compute resources

**If you are about to say "I'll create it in one operation" -> STOP and read the writing strategy below.**

---

## Multi-Part Writing Strategy

**CRITICAL**: The functional-spec-target.md size will vary based on project complexity:

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
# Check if functional-spec-target.md already exists
if [ -f "{reports_dir}/functional-spec-target.md" ]; then
  # Spec exists - check content to determine resume point
  # Look for section headers to determine last completed part
fi
```

**Step 2: Determine resume point from spec content**:

**IF** functional-spec-target.md exists AND is incomplete:

1. Read `{reports_dir}/functional-spec-target.md`
2. Identify last completed part by checking which section headers exist
3. Display resume message:

   ```text
   [!] RESUMING INTERRUPTED GENERATION

   Last completed: Part 2 (User Stories - CRITICAL Modernized)
   Resuming from: Part 3 (User Stories - STANDARD + Business Rules)

   Continuing generation...
   ```

4. Skip completed parts
5. Start generation from next incomplete part

**IF** functional-spec-target.md does NOT exist:

- Start fresh from Part 1

---

## Spec Structure (7 Parts)

Generate spec in `{reports_dir}/functional-spec-target.md`

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

### Part 1: Executive Summary + Current State + Personas (Target)

Generate Sections 1, 2, and 3 for TARGET system.

---

[STOP: GENERATE_PART_1]**

#### Section 1: Executive Summary (Target)

- Project name: {name} (Modernized)
- Target system overview
- Modernization goals from user preferences

#### Section 2: Current State - Problem & Goals (Target)

- Current problems being addressed
- Modernization goals
- Success criteria

#### Section 3: Personas & User Journeys (Target)

- User personas (preserved from legacy + enhanced)
- Modernized user journeys
- New user experience improvements

**Completion Criteria**:

- [ok] Modernization goals documented
- [ok] User personas mapped from legacy
- [ok] Target improvements clear
- [ok] NO placeholders

**After Part 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `{reports_dir}/functional-spec-target.md`
   - Content: Complete Sections 1-3

2. **Verify:** Read file, confirm modernization goals match user's answers.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 1/7 complete: Executive Summary + Current State + Personas (Target)
     - Sections completed: 3
     - Lines generated: [COUNT]

   ```

---

### Part 2: Use Cases + User Stories (Target)

Generate Sections 4 and 5 with modernization enhancements.

---

[STOP: GENERATE_PART_2]**

#### Section 4: Use Cases (Target)

For each use case from legacy spec:

```markdown
### UC-{id}: {Use Case Name} (Modernized)

**Priority:** {CRITICAL | STANDARD}
**Legacy Reference:** {legacy-file}:{line}
**Target Implementation:** {user's chosen stack}

**Actors:** {Primary actor(s)}
**Preconditions:** {Updated for target system}
**Main Flow:** (Modernized)
1. {Modernized step 1}
2. {Modernized step 2}

**Modernization Changes:**
- Legacy: {how it works today}
- Target: {how it will work with new stack}

**New Capabilities:**
- {capability enabled by modernization}
```

#### Section 5: User Stories (Target)

For each user story, document with Given-When-Then format:

```markdown
### US-{CRIT|STD}-{id}: {Story Name} (Modernized)

**Priority:** {CRITICAL | STANDARD}
**Preservation:** {EXACT | ENHANCED | REPLACED}
**Legacy Reference:** {file}:{line}

**As a** {actor}
**I want to** {enhanced action}
**So that** {improved benefit}

**Given** {modernized precondition}
**When** {modernized action}
**Then** {modernized result}

**Acceptance Criteria:**
- [ ] {criterion with target tech}
- [ ] {performance improvement}
```

**Completion Criteria**:

- [ok] ALL use cases from legacy spec mapped
- [ok] ALL user stories with modernization status
- [ok] User preferences correctly applied
- [ok] NO placeholders

**After Part 2 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 4-5 to functional-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 2/7 complete: Use Cases + User Stories (Target)
     - Use cases modernized: [COUNT]
     - User stories modernized: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 3: Business Logic + State Machines + Config (Target)

Generate Sections 6, 7, and 8 with target stack considerations.

---

[STOP: GENERATE_PART_3]**

#### Section 6: Business Logic (Target)

Document with EXACT/ENHANCED/REPLACED status:

```markdown
### 6.1 Core Processing Algorithms (Target)

ALGORITHM: {AlgorithmName}
PRESERVATION: {EXACT | ENHANCED | REPLACED}
LEGACY SOURCE: {file}:{line}

TARGET IMPLEMENTATION:
  PURPOSE: {What it does - same or enhanced}
  INPUT: {Updated input types for target stack}
  OUTPUT: {Updated output types}
  STEPS: (Modernized if ENHANCED/REPLACED)
    1. {Step description}
  RATIONALE: {Why preserved/enhanced/replaced}

### 6.2 Decision Trees (Target)

DECISION: {Decision Name}
PRESERVATION: {EXACT | ENHANCED}
IF: {condition}
THEN: {action}
BECAUSE: {business reason - preserved from legacy}

### 6.3 Calculation Formulas (Target)

FORMULA: {FormulaName}
PRESERVATION: {EXACT}
NOTE: Business formulas typically preserved exactly
```

#### Section 7: State Machines (Target)

Document modernized state transitions.

#### Section 8: Configuration-Driven Behaviors (Target)

Document target configuration approach.

**Completion Criteria**:

- [ok] ALL business logic marked EXACT/ENHANCED/REPLACED
- [ok] Rationale for each decision
- [ok] State machines preserved or enhanced
- [ok] NO placeholders

**After Part 3 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 6-8 to functional-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 3/7 complete: Business Logic + State Machines + Config (Target)
     - Logic Preserved (EXACT): [COUNT]
     - Logic Enhanced: [COUNT]
     - Logic Replaced: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 4: Scope + Requirements + NFRs + Error Handling (Target)

Generate Sections 9, 10, 11, 12, and 13 using user's preferences.

---

[STOP: GENERATE_PART_4]**

#### Section 9: Scope / Out-of-Scope (Target)

- IN SCOPE: Components with explicit target preferences
- OUT OF SCOPE: Components to keep as-is
- Migration boundaries

#### Section 10: Functional Requirements (Target)

Map from legacy with modernization status.

#### Section 11: Non-Negotiables (Target)

Preserve critical constraints from legacy.

#### Section 12: Non-Functional Requirements (Target)

Use user's answers from 10 questions:

| Category | Target State | User Preference |
|----------|-------------|-----------------|
| Performance | {target metrics} | {Q answer} |
| Security | {target approach} | Q9: {answer} |
| Scalability | {target approach} | Q5: {answer} |
| Observability | {target stack} | Q8: {answer} |

#### Section 13: Error Handling & Recovery (Target)

Document target error handling strategy:
- Which legacy patterns to preserve
- Which to modernize (circuit breakers, retry with backoff)
- New observability for errors

**Completion Criteria**:

- [ok] Scope boundaries match user's answers
- [ok] NFRs reflect user's Q5-Q10 preferences
- [ok] Error handling strategy defined
- [ok] NO placeholders

**After Part 4 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 9-13 to functional-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 4/7 complete: Scope + Requirements + NFRs + Error Handling (Target)
     - In Scope Components: [COUNT]
     - Out of Scope Components: [COUNT]
     - Target NFR categories: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 5: Data Models + Config Mapping + API + Integration (Target)

Generate Sections 14, 15, 16, and 17.

---

[STOP: GENERATE_PART_5]**

#### Section 14: Data Models (Target)

Use user's answer from Q2 (Database):

```markdown
### Entity: {Name} (Migrated)

**Target Database:** {Q2 answer}
**Migration Notes:** {considerations}

| Field | Legacy Type | Target Type | Migration |
|-------|-------------|-------------|-----------|
| {field} | {legacy} | {target} | {notes} |

### 14.2 Field Mappings (Target)

| Source Field | Target Field | Transformation | Validation |
|--------------|--------------|----------------|------------|
| {legacy} | {target} | {transform} | {validation} |
```

#### Section 15: Configuration Mapping (Target)

Document target configuration approach.

#### Section 16: API Contracts (Target)

Document modernized API contracts.

#### Section 17: Integration Points (Target)

Document target integrations.

**Completion Criteria**:

- [ok] Data migration approach documented
- [ok] Target database from Q2 applied
- [ok] API modernization documented
- [ok] NO placeholders

**After Part 5 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 14-17 to functional-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 5/7 complete: Data Models + Config + API + Integration (Target)
     - Target Database: {Q2 answer}
     - Entities with migration plan: [COUNT]
     - API endpoints modernized: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 6: Quirks + RAD + Value + Traceability + Next Steps (Target)

Generate Sections 18, 19, 20, 21, and 22.

---

[STOP: GENERATE_PART_6]**

#### Section 18: Known Quirks & Legacy Behaviors (Target)

Document which quirks to:
- PRESERVE (critical business behavior)
- FIX (known bugs)
- REMOVE (obsolete workarounds)

#### Section 19: Risks, Assumptions, Decisions (Target)

Document modernization-specific RAD.

#### Section 20: Value / Business Case (Target)

Document expected benefits of modernization.

#### Section 21: Traceability Matrix (Target)

Cross-reference legacy to target requirements.

#### Section 22: Next Steps (Target)

Define implementation roadmap.

**Completion Criteria**:

- [ok] Quirks categorized (PRESERVE/FIX/REMOVE)
- [ok] Modernization risks documented
- [ok] Traceability matrix complete
- [ok] NO placeholders

**After Part 6 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 18-22 to functional-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 6/7 complete: Quirks + RAD + Value + Traceability + Next Steps (Target)
     - Quirks preserved: [COUNT]
     - Quirks fixed: [COUNT]
     - Risks documented: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 7: Validation Checklist + Appendices (Target)

Generate Section 24 and Appendices A-C.

**Note**: Section 23 (Business Logic Preservation Checklist) is LEGACY ONLY.
For target spec, skip Section 23 or replace with implementation verification.

---

[STOP: GENERATE_PART_7]**

#### Section 24: Output Validation Checklist (Target)

Complete the target spec validation checklist:
- Verify all legacy features mapped to target
- Verify user preferences (Q1-Q10) correctly applied
- Verify preservation status documented for all business logic
- Verify migration strategy for all data models

#### Appendix A: Analysis Metadata

Document analysis statistics.

#### Appendix B: Glossary

Define domain terms (preserved from legacy + new terms).

#### Appendix C: Reference Diagrams

Include target system context diagram.

**Completion Criteria**:

- [ok] Validation checklist completed
- [ok] Metadata documented
- [ok] Glossary populated
- [ok] Diagrams included
- [ok] NO placeholders

**After Part 7 Generation**:

1. **Append to file** using Edit tool:
   - Append Section 24 and Appendices to functional-spec-target.md

2. **MANDATORY - Display progress and final summary**:

   ```text
   [ok] Part 7/7 complete: Validation Checklist + Appendices (Target)
     - Validation items verified: [COUNT]
     - Glossary terms: [COUNT]
     - Lines generated: [COUNT]

   [ok] functional-spec-target.md GENERATION COMPLETE
      Total sections: 23 + 3 appendices (Section 23 skipped for target)
      Total features modernized: [COUNT]
      Total lines: [COUNT]
      File path: {reports_dir}/functional-spec-target.md

   ```

---

## Verification Gate (HARD STOP)

[!] **VERIFICATION GATE - CANNOT PROCEED WITHOUT PASSING**

**BEFORE** proceeding to 06c1-technical-spec-legacy.md, verify spec quality:

### Verification Checklist

Read functional-spec-target.md and verify:

- [ ] File exists at expected path: `{reports_dir}/functional-spec-target.md`
- [ ] All 23 section headers present (Section 23 skipped for target):
      - [ ] Section 1: Executive Summary
      - [ ] Section 2: Current State - Problem & Goals
      - [ ] Section 3: Personas & User Journeys
      - [ ] Section 4: Use Cases (with modernization status)
      - [ ] Section 5: User Stories (with EXACT/ENHANCED/REPLACED status)
      - [ ] Section 6: Business Logic (with preservation status)
      - [ ] Section 7: State Machines (Target)
      - [ ] Section 8: Configuration-Driven Behaviors (Target)
      - [ ] Section 9: Scope / Out-of-Scope
      - [ ] Section 10: Functional Requirements (Target)
      - [ ] Section 11: Non-Negotiables (Target)
      - [ ] Section 12: Non-Functional Requirements (Target)
      - [ ] Section 13: Error Handling & Recovery (Target)
      - [ ] Section 14: Data Models (with migration plan)
      - [ ] Section 15: Configuration Mapping (Target)
      - [ ] Section 16: API Contracts (Target)
      - [ ] Section 17: Integration Points (Target)
      - [ ] Section 18: Known Quirks (PRESERVE/FIX/REMOVE)
      - [ ] Section 19: Risks, Assumptions, Decisions
      - [ ] Section 20: Value / Business Case
      - [ ] Section 21: Traceability Matrix
      - [ ] Section 22: Next Steps
      - [ ] Section 24: Output Validation Checklist
      - [ ] Appendices A, B, C present
- [ ] Quality checks:
      - [ ] User preferences (Q1-Q10) correctly applied
      - [ ] All use cases show Legacy -> Target mapping
      - [ ] All user stories with EXACT/ENHANCED/REPLACED status
      - [ ] Business logic preservation rationale documented
      - [ ] Error handling strategy defined
      - [ ] NFRs reference user's technology choices
      - [ ] Data migration approach documented
      - [ ] Quirks categorized (PRESERVE/FIX/REMOVE)
      - [ ] No placeholders (TODO, TBD, "will be analyzed", "coming soon")
      - [ ] All tables properly formatted (Markdown)
- [ ] Completeness (verify based on project size/complexity):
      - [ ] **Small projects (< 5,000 LOC)**:
            - Total lines: 800+ (minimum)
            - Use cases: 5-15
            - User stories: 10-30
            - Business logic items: 5-15
      - [ ] **Medium projects (5,000-50,000 LOC)**:
            - Total lines: 2,000+ (minimum)
            - Use cases: 15-50
            - User stories: 30-100
            - Business logic items: 15-40
      - [ ] **Large projects (> 50,000 LOC)**:
            - Total lines: 4,000+ (minimum)
            - Use cases: 50-150
            - User stories: 100-300
            - Business logic items: 40-100

---

### Recovery Actions (IF ANY CHECKBOX FAILS)

**IF ANY checkbox is unchecked**:

```text
[x] VERIFICATION FAILED

functional-spec-target.md is incomplete. Issues found:
- [List specific missing items from checklist above]
```

**RECOVERY DECISION TREE**:

**1. Identify incomplete sections**:

List which sections or quality checks failed verification.

**2. Determine recovery approach**:

**IF** entire sections missing (e.g., Section 5 not found in file):

- **Action**: Regenerate ONLY the missing sections
- **Method**:
  1. Check functional-spec-target.md content to identify last completed section
  2. Resume generation from first missing section
  3. Use Edit tool to append missing sections to existing file
  4. Re-run verification after regeneration

**IF** quality issues in existing sections (e.g., user preferences not applied):

- **Action**: Enhance the problematic section with missing details
- **Method**:
  1. Read the incomplete section from functional-spec-target.md
  2. Identify specific missing elements (preference mappings, rule status, etc.)
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
  [A] Regenerate entire functional-spec-target.md from scratch
  [B] Fix individual sections (may take longer)
  [C] Proceed anyway (NOT RECOMMENDED - will cause issues in next stage)

  Your choice: ___
  ```

**3. Execute recovery**:

- Based on failure type, perform specific recovery actions
- Use appropriate tools (Edit for fixes, Write for full regen)
- Re-run verification after recovery
- **DO NOT proceed to 06c1 until verification passes**

[!] **STOP HERE** - DO NOT CONTINUE TO NEXT STAGE UNTIL VERIFICATION PASSES

---

### Verification Success

**IF ALL checkboxes are checked**:

```text
[ok] VERIFICATION PASSED

functional-spec-target.md is complete and meets quality standards:
- All 23 sections + 3 appendices present and complete (Section 23 skipped for target)
- User preferences (Q1-Q10) correctly applied
- All use cases show Legacy -> Target mapping
- All user stories have EXACT/ENHANCED/REPLACED status
- Business logic preservation rationale documented
- Error handling strategy defined
- NFRs reflect target technology choices
- Data migration approach documented
- Quirks categorized (PRESERVE/FIX/REMOVE)
- No placeholders or incomplete sections
- Total lines: [COUNT] (comprehensive spec)

Proceeding to 06c1-technical-spec-legacy.md...
```

**Only after passing verification**: Proceed to next stage

---

## Both Functional Specs Complete

```text
===========================================================
  BOTH FUNCTIONAL SPECS COMPLETE

  1. functional-spec-legacy.md - LEGACY system (what exists today)
  2. functional-spec-target.md - TARGET system (what will be built)

  Chain ID: {chain_id}

  Now proceeding to technical specs (legacy + target)...
===========================================================

ARTIFACT_COMPLETE:FUNCTIONAL_SPEC_TARGET
```

---

**[GATE-CHECK]** If verification PASSES: auto-continue to next stage.
If verification FAILS: present recovery options and WAIT for user decision.

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
