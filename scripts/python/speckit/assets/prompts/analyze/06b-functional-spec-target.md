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

This prompt uses **"Part 1-5"** to describe content sections to write incrementally.

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

**YOU MUST generate the spec in 5 separate parts as specified below.**

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

## Spec Structure (5 Parts)

Generate spec in `{reports_dir}/functional-spec-target.md`

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

Generate Sections 1, 2, and 3 for TARGET system.

---

[STOP: GENERATE_PART_1]**

#### Section 1: Introduction

- Project name: {name} (Modernized)
- Target system overview
- Modernization goals from user preferences

#### Section 2: Executive Summary

- High-level target functionality
- Key improvements over legacy
- New capabilities

#### Section 3: Scope

- IN SCOPE: Components with explicit target preferences
- OUT OF SCOPE: Components to keep as-is
- Migration boundaries

**Completion Criteria**:

- [ok] Modernization goals documented
- [ok] Scope boundaries match user's answers
- [ok] IN/OUT scope clearly defined
- [ok] NO placeholders

**After Part 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `{reports_dir}/functional-spec-target.md`
   - Content: Complete Sections 1-3

2. **Verify:** Read file, confirm scope boundaries match user's answers.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 1/5 complete: Introduction + Summary + Scope
     - In Scope Components: [COUNT]
     - Out of Scope Components: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 2: User Stories - CRITICAL Features (Modernized)

Generate Section 4.1 with modernization enhancements.

---

[STOP: GENERATE_PART_2]**

For each CRITICAL feature from legacy spec:

```markdown
### US-{id}: {Feature Name} (Modernized)

**Priority:** CRITICAL
**Legacy Reference:** {legacy-file}:{line}
**Target Implementation:** {user's chosen stack}

**As a** {actor}
**I want to** {enhanced action}
**So that** {improved benefit}

**Modernization Changes:**
- Legacy: {how it works today}
- Target: {how it will work with new stack}

**New Capabilities:**
- {capability enabled by modernization}

**Acceptance Criteria:**
- [ ] {criterion with target tech}
- [ ] {performance improvement}
```

**Completion Criteria**:

- [ok] ALL CRITICAL features from legacy spec mapped
- [ok] Every feature shows Legacy -> Target mapping
- [ok] User preferences correctly applied
- [ok] NO placeholders

**After Part 2 Generation**:

1. **Append to file** using Edit tool:
   - Append Section 4.1 content to functional-spec-target.md

2. **Verify:** Read file, confirm all CRITICAL features have modernization mappings.

3. **MANDATORY - Display progress**:

   ```text
   [ok] Part 2/5 complete: User Stories (CRITICAL Modernized)
     - CRITICAL features modernized: [COUNT]
     - New capabilities added: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 3: User Stories - STANDARD + Business Rules (Modernized)

Generate Sections 4.2 and 5 with target stack considerations.

---

[STOP: GENERATE_PART_3]**

#### Section 4.2: STANDARD Features (Modernized)

- Same format as CRITICAL
- Include modernization changes where applicable
- Note OUT OF SCOPE items explicitly

#### Section 5: Business Rules (Preserved + Enhanced)

```markdown
## 5. Business Rules

### BR-001: {Rule Name}

**Category:** {category}
**Preservation:** {EXACT | ENHANCED | REPLACED}
**Legacy Source:** {file}:{line}

**Current Logic:**
{legacy pseudocode}

**Target Logic:**
{modernized pseudocode - if ENHANCED/REPLACED}
{or "Preserved exactly as legacy" - if EXACT}

**Rationale:**
{why preserved/enhanced/replaced}
```

**Completion Criteria**:

- [ok] ALL STANDARD features mapped with modernization status
- [ok] Business rules marked as EXACT/ENHANCED/REPLACED
- [ok] Rationale provided for each rule decision
- [ok] NO placeholders

**After Part 3 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 4.2 and 5 to functional-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 3/5 complete: STANDARD Features + Business Rules (Modernized)
     - STANDARD features modernized: [COUNT]
     - Rules Preserved (EXACT): [COUNT]
     - Rules Enhanced: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 4: NFRs + Data Requirements (Target)

Generate Sections 6 and 7 using user's target preferences.

---

[STOP: GENERATE_PART_4]**

#### Section 6: Non-Functional Requirements (Target)

Use user's answers from 10 questions:

- Q5: Deployment target
- Q7: Containerization
- Q8: Observability stack
- Q9: Security approach
- Q10: Testing strategy

| Category | Target State | User Preference |
|----------|-------------|-----------------|
| Performance | {target metrics} | {Q answer} |
| Security | {target approach} | Q9: {answer} |
| Scalability | {target approach} | Q5: {answer} |
| Observability | {target stack} | Q8: {answer} |

#### Section 7: Data Requirements (Target)

Use user's answer from Q2 (Database):

```markdown
### Entity: {Name} (Migrated)

**Target Database:** {Q2 answer}
**Migration Notes:** {considerations}

| Field | Type | Target Type | Migration |
|-------|------|-------------|-----------|
| {field} | {legacy} | {target} | {notes} |
```

**Completion Criteria**:

- [ok] NFRs reflect user's Q5-Q10 preferences
- [ok] Data migration approach documented
- [ok] Target database from Q2 applied
- [ok] NO placeholders

**After Part 4 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 6 and 7 to functional-spec-target.md

2. **MANDATORY - Display progress**:

   ```text
   [ok] Part 4/5 complete: NFRs + Data Requirements (Target)
     - Target Database: {Q2 answer}
     - Target Deployment: {Q5 answer}
     - Entities with migration plan: [COUNT]
     - Lines generated: [COUNT]

   ```

---

### Part 5: Acceptance Criteria + Assumptions + Constraints (Target)

Generate Sections 8, 9, and 10.

---

[STOP: GENERATE_PART_5]**

#### Section 8: Acceptance Criteria (Target)

- Migration success criteria
- Feature parity verification
- Performance benchmarks vs legacy

#### Section 9: Assumptions (Target)

- Target environment assumptions
- Migration path assumptions
- Team capability assumptions

#### Section 10: Constraints (Target)

- Timeline constraints
- Budget constraints
- Technology constraints from user preferences

**Completion Criteria**:

- [ok] Migration success criteria defined
- [ok] All assumptions documented
- [ok] Constraints from user preferences captured
- [ok] NO placeholders

**After Part 5 Generation**:

1. **Append to file** using Edit tool:
   - Append Sections 8, 9, and 10 to functional-spec-target.md

2. **Verify:** Read complete file, confirm:
   - All 10 sections present
   - Scope boundaries respected
   - User preferences correctly applied
   - No placeholders or TODOs

3. **MANDATORY - Display progress and final summary**:

   ```text
   [ok] Part 5/5 complete: Acceptance + Assumptions + Constraints (Target)
     - Migration criteria: [COUNT]
     - Assumptions: [COUNT]
     - Constraints: [COUNT]
     - Lines generated: [COUNT]

   [ok] functional-spec-target.md GENERATION COMPLETE
      Total sections: 10
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
- [ ] All 10 section headers present:
      - [ ] Section 1: Introduction
      - [ ] Section 2: Executive Summary
      - [ ] Section 3: Scope (with IN/OUT boundaries)
      - [ ] Section 4: User Stories (4.1 CRITICAL, 4.2 STANDARD)
      - [ ] Section 5: Business Rules (with preservation status)
      - [ ] Section 6: Non-Functional Requirements (Target)
      - [ ] Section 7: Data Requirements (Target)
      - [ ] Section 8: Acceptance Criteria (Target)
      - [ ] Section 9: Assumptions (Target)
      - [ ] Section 10: Constraints (Target)
- [ ] Quality checks:
      - [ ] User preferences (Q1-Q10) correctly applied
      - [ ] All features show Legacy -> Target mapping
      - [ ] Business rules marked EXACT/ENHANCED/REPLACED
      - [ ] NFRs reference user's technology choices
      - [ ] Data migration approach documented
      - [ ] No placeholders (TODO, TBD, "will be analyzed", "coming soon")
      - [ ] All tables properly formatted (Markdown)
- [ ] Completeness (verify based on project size/complexity):
      - [ ] **Small projects (< 5,000 LOC)**:
            - Total lines: 500+ (minimum)
            - Features modernized: 10-30
            - Business rules categorized: 5-15
      - [ ] **Medium projects (5,000-50,000 LOC)**:
            - Total lines: 1,500+ (minimum)
            - Features modernized: 30-100
            - Business rules categorized: 15-40
      - [ ] **Large projects (> 50,000 LOC)**:
            - Total lines: 3,000+ (minimum)
            - Features modernized: 100-300
            - Business rules categorized: 40-100

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
- All 10 sections present and complete
- User preferences (Q1-Q10) correctly applied
- All features show Legacy -> Target mapping
- Business rules have preservation status
- NFRs reflect target technology choices
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
