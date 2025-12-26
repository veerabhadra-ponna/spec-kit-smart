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

This prompt uses **"Part 1-5"** to describe content sections to write incrementally.

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

## Spec Structure (5 Parts)

Generate spec in `{reports_dir}/functional-spec-legacy.md`

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

### Part 1: Introduction + Summary + Scope

Generate Sections 1, 2, and 3.

---

[STOP: GENERATE_PART_1]**

Generate the following sections:

#### Section 1: Introduction

- Project name and purpose
- Document scope and audience
- Legacy system overview

#### Section 2: Executive Summary

- High-level functionality summary
- Key capabilities
- System boundaries

#### Section 3: Scope

- In-scope functionality
- Out-of-scope items
- Assumptions

**Completion Criteria**:

- [ok] Project context established
- [ok] System boundaries defined
- [ok] Assumptions documented
- [ok] NO placeholders

**After Part 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `{reports_dir}/functional-spec-legacy.md`
   - Content: Complete Sections 1-3

2. **Verify:** Read file, confirm no placeholders, all sections complete.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 1/5 complete: Introduction + Summary + Scope
     - Sections completed: 3
     - Lines generated: [COUNT]

   ```

---

### Part 2: User Stories - CRITICAL Features

Generate Section 4.1 (CRITICAL priority features).

---

[STOP: GENERATE_PART_2]**

Extract all CRITICAL features from analysis-report.md Phase 2.

**For each feature:**

```markdown
### US-{id}: {Feature Name}

**Priority:** CRITICAL
**Source:** {file}:{line}

**As a** {actor}
**I want to** {action}
**So that** {benefit}

**Current Implementation:**
- {how it works today}
- Reference: `{file}:{line}`

**Acceptance Criteria:**
- [ ] {criterion 1}
- [ ] {criterion 2}
```

**Completion Criteria**:

- [ok] ALL CRITICAL features from analysis-report.md documented
- [ok] Every feature has file:line reference
- [ok] Acceptance criteria for each feature
- [ok] NO placeholders

**After Part 2 Generation**:

1. **Append to file** using Edit tool:
   - Append Section 4.1 content to functional-spec-legacy.md

2. **Verify:** Read file, confirm all CRITICAL features documented with file:line references.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 2/5 complete: User Stories (CRITICAL)
     - CRITICAL features documented: [COUNT]
     - File:line references: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 3: User Stories - STANDARD + Business Rules

Generate Sections 4.2 and 5.

---

[STOP: GENERATE_PART_3]**

#### Section 4.2: STANDARD Features

- Extract all STANDARD priority features
- Same user story format as CRITICAL
- Include file:line references

#### Section 5: Business Rules

```markdown
## 5. Business Rules

### BR-001: {Rule Name}

**Category:** {Validation | Calculation | Authorization | Workflow}
**Source:** {file}:{line}
**Description:** {plain English description}
**Pseudocode:**
```

```text
IF condition THEN
  action
ELSE
  alternative
END IF
```

**Completion Criteria**:

- [ok] ALL STANDARD features documented
- [ok] Business rules extracted with pseudocode
- [ok] Every item has file:line reference
- [ok] NO placeholders

**After Part 3 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 4.2 and 5 to functional-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 3/5 complete: STANDARD Features + Business Rules
     - STANDARD features documented: [COUNT]
     - Business rules documented: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 4: NFRs + Data Requirements

Generate Sections 6 and 7.

---

[STOP: GENERATE_PART_4]**

#### Section 6: Non-Functional Requirements

| Category | Current State | Evidence |
|----------|--------------|----------|
| Performance | {metrics} | {file:line} |
| Security | {implementation} | {file:line} |
| Scalability | {approach} | {file:line} |
| Reliability | {mechanisms} | {file:line} |

#### Section 7: Data Requirements

```markdown
### Entity: {Name}

**Source:** {file}:{line}

| Field | Type | Constraints |
|-------|------|-------------|
| {field} | {type} | {constraints} |

**Relationships:**
- {relationship description}
```

**Completion Criteria**:

- [ok] All NFR categories documented with evidence
- [ok] All data entities documented
- [ok] Relationships mapped
- [ok] Every item has file:line reference
- [ok] NO placeholders

**After Part 4 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 6 and 7 to functional-spec-legacy.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 4/5 complete: NFRs + Data Requirements
     - NFR categories documented: [COUNT]
     - Data entities documented: [COUNT]
     - Relationships mapped: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 5: Acceptance Criteria + Assumptions + Constraints

Generate Sections 8, 9, and 10.

---

[STOP: GENERATE_PART_5]**

#### Section 8: Acceptance Criteria

- System-level acceptance tests
- Integration verification points
- Performance benchmarks

#### Section 9: Assumptions

- Technical assumptions
- Business assumptions
- Environmental assumptions

#### Section 10: Constraints

- Technical constraints
- Business constraints
- Regulatory constraints

**Completion Criteria**:

- [ok] Acceptance criteria defined
- [ok] All assumptions documented
- [ok] All constraints identified
- [ok] NO placeholders

**After Part 5 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 8, 9, and 10 to functional-spec-legacy.md

2. **MANDATORY - Display progress and final summary**:

   ```text
   [ok] Part 5/5 complete: Acceptance + Assumptions + Constraints
     - Acceptance criteria: [COUNT]
     - Assumptions: [COUNT]
     - Constraints: [COUNT]
     - Lines generated: [COUNT]

   [ok] functional-spec-legacy.md GENERATION COMPLETE
      Total sections: 10
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
- [ ] All 10 section headers present:
      - [ ] Section 1: Introduction
      - [ ] Section 2: Executive Summary
      - [ ] Section 3: Scope
      - [ ] Section 4: User Stories (4.1 CRITICAL, 4.2 STANDARD)
      - [ ] Section 5: Business Rules
      - [ ] Section 6: Non-Functional Requirements
      - [ ] Section 7: Data Requirements
      - [ ] Section 8: Acceptance Criteria
      - [ ] Section 9: Assumptions
      - [ ] Section 10: Constraints
- [ ] Quality checks:
      - [ ] 20+ file:line references present throughout
      - [ ] All CRITICAL features have acceptance criteria
      - [ ] Business rules have pseudocode
      - [ ] NFRs have evidence references
      - [ ] Data entities have field definitions
      - [ ] No placeholders (TODO, TBD, "will be analyzed", "coming soon")
      - [ ] All tables properly formatted (Markdown)
- [ ] Completeness (verify based on project size/complexity):
      - [ ] **Small projects (< 5,000 LOC)**:
            - Total lines: 500+ (minimum)
            - Features documented: 10-30
            - Business rules: 5-15
      - [ ] **Medium projects (5,000-50,000 LOC)**:
            - Total lines: 1,500+ (minimum)
            - Features documented: 30-100
            - Business rules: 15-40
      - [ ] **Large projects (> 50,000 LOC)**:
            - Total lines: 3,000+ (minimum)
            - Features documented: 100-300
            - Business rules: 40-100

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
- All 10 sections present and complete
- 20+ file:line references found
- All features have acceptance criteria
- Business rules documented with pseudocode
- NFRs have evidence
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

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.

**DO NOT:**

- Skip to technical specs
- Skip to stage-prompts/
- Mark Stage 6 complete

**You MUST generate both functional specs before proceeding.**
