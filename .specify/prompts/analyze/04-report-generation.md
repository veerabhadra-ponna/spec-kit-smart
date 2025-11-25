---
stage: report_generation
requires: 03*-*.json
outputs: report_generated
version: 1.0.0
---

## ⚠️ MANDATORY: Read Agent Instructions First

**BEFORE PROCEEDING:**

1. Check if `AGENTS.md` exists in repository root, `.specify/memory/`, or `templates/` directory
2. **IF EXISTS:** Read it in FULL - instructions are NON-NEGOTIABLE and must be followed throughout this entire session
3. Follow all AGENTS.md guidelines for the duration of this command execution
4. These instructions override any conflicting default behaviors
5. **DO NOT** forget or ignore these instructions as you work through tasks

**Verification:** After reading AGENTS.md (if it exists), acknowledge with:
   "✓ Read AGENTS.md v[X.X] - Following all guidelines"

**If AGENTS.md does not exist:** Proceed with default behavior.

---

# Stage 4: Analysis Report Generation

## Purpose

Generate the comprehensive `analysis-report.md` file using completion-based chunking strategy. This is the primary deliverable that documents all findings.

---

## Previous State

Load state from either:
- `.analysis/.state/03a-full-app.json` (if scope = A)
- `.analysis/.state/03b-cross-cutting.json` (if scope = B)

---

## ⚠️ MANDATORY CHUNKING REQUIREMENT

🛑 **STOP - READ THIS FIRST BEFORE GENERATING ANYTHING**

**DO NOT generate the entire report in one operation.**

**DO NOT create all sections at once.**

**DO NOT skip the chunking strategy below.**

**YOU MUST generate the report in 9 separate chunks as specified below.**

Attempting to generate the full report in one operation WILL result in:

- Incomplete sections due to token limits
- Missing file:line references
- Placeholder content (TODO, TBD)
- Verification failures
- Wasted time and compute resources

**If you are about to say "I'll create it in one operation" → STOP and read the chunking strategy below.**

---

## Chunking Strategy

**CRITICAL**: The analysis-report.md size will vary based on project complexity:

- **Small projects** (< 5,000 LOC): **1,000-2,500 lines**
- **Medium projects** (5,000-50,000 LOC): **3,000-8,000 lines**
- **Large projects** (> 50,000 LOC): **5,000-15,000 lines**

**⚠️ COMPLETION-BASED CHUNKING (NOT size-based)**:

Use **completion-based chunking**, NOT size-based chunking:

- Generate complete logical sections in each chunk
- Each chunk ends with a distinct completion point
- Display progress after each chunk (MANDATORY)
- Create checkpoint markers for resume capability
- NO placeholders allowed (no TODO, TBD, "will be analyzed")

**Why chunking is critical**:

- Large reports may hit token limits without chunking
- Checkpoints enable resume if interrupted
- Progress tracking improves user experience
- Verification gates ensure quality at each step

---

## Resume Detection (BEFORE Starting)

**BEFORE generating any chunks**, check for interrupted analysis:

**Step 1: Check for existing report**:

```bash
# Check if analysis-report.md already exists
if [ -f ".analysis/{project}-{timestamp}/analysis-report.md" ]; then
  # Report exists - check if complete
fi
```

**Step 2: Check checkpoints directory**:

```bash
# Check for checkpoint markers
ls .analysis/.checkpoints/
```

**Step 3: Determine resume point**:

**IF** analysis-report.md exists AND is incomplete:

1. Read `.analysis/.checkpoints/` directory
2. Identify last completed checkpoint (e.g., `phase-4-complete.json`)
3. Display resume message:

   ```text
   ⚠️ RESUMING INTERRUPTED ANALYSIS

   Last completed: Chunk 4 (Phase 2.3 - Data Layer)
   Resuming from: Chunk 5 (Phase 3 - Positive Findings)

   Continuing analysis...
   ```

4. Skip completed chunks 1-4
5. Start generation from Chunk 5

**IF** analysis-report.md does NOT exist OR checkpoints missing:

- Start fresh from Chunk 1

---

## Report Structure (9 Phases)

Generate report in `.analysis/{project}-{timestamp}/analysis-report.md`

**⚠️ GENERATION ORDER - STRICTLY ENFORCED**:

1. Generate ONLY Chunk 1 first (Phase 1)
2. Wait for Chunk 1 completion
3. THEN generate Chunk 2 (Phase 2.1)
4. Continue sequentially through all 9 chunks

**DO NOT**:

- ❌ Generate multiple chunks in one response
- ❌ Generate all phases at once
- ❌ Skip checkpoint creation
- ❌ Skip progress display

**IF** you find yourself generating more than one chunk at a time → **STOP IMMEDIATELY**

---

### Chunk 1: Phase 1 - Project Discovery

Complete sections:
- **1.1 Technology Stack** (from structure analysis)
- **1.2 System Architecture** (from project type)
- **1.3 Project Statistics** (LOC, file counts)
- **1.4 Configuration Analysis** (all config files)
- **1.5 Build & Deployment** (build tools, scripts)

**Completion Criteria**:

- ✓ All configuration files analyzed
- ✓ Tech stack fully identified
- ✓ Architecture documented with evidence
- ✓ Project statistics calculated
- ✓ NO placeholders

**After Chunk 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `.analysis/{project}-{timestamp}/analysis-report.md`
   - Content: Complete Phase 1 sections (1.1-1.5)

2. **Create checkpoint marker**:
   - Create directory: `.analysis/.checkpoints/` (if not exists)
   - Write JSON file: `.analysis/.checkpoints/phase-1-complete.json`
   - Content:

     ```json
     {
       "chunk": 1,
       "phase": "1",
       "phase_name": "Project Discovery",
       "timestamp": "2025-11-15T10:30:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 1/9 complete: Phase 1 (Project Discovery)
     - Analyzed: [COUNT] configuration files
     - Identified: [TECH STACK SUMMARY]
     - Lines generated: [COUNT]
   ```

### Chunk 2: Phase 2.1 - Controllers & API Endpoints

Complete **Section 2.1: Controllers Analysis**:

- EVERY controller file analyzed
- EVERY API endpoint documented (method, path, purpose)
- File:line references for all findings
- Auth requirements for each endpoint
- NO placeholders

**After Chunk 2 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Read existing analysis-report.md
   - Append Section 2.1 content to the end
   - Use str_replace to append (not overwrite)

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/phase-2-1-complete.json`
   - Content:

     ```json
     {
       "chunk": 2,
       "phase": "2.1",
       "phase_name": "Controllers & API Endpoints",
       "timestamp": "2025-11-15T10:45:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 2/9 complete: Phase 2.1 (Controllers)
     - Analyzed: [COUNT] controller files
     - Documented: [COUNT] API endpoints
     - Features extracted: [COUNT]
     - Lines generated: [COUNT]
   ```

### Chunk 3: Phase 2.2 - Services & Business Logic

Complete **Section 2.2: Services Analysis**:

- EVERY service file analyzed
- Business workflows documented with evidence
- External integrations identified
- Transaction patterns clear
- NO placeholders

**After Chunk 3 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Section 2.2 content to analysis-report.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/phase-2-2-complete.json`
   - Content:

     ```json
     {
       "chunk": 3,
       "phase": "2.2",
       "phase_name": "Services & Business Logic",
       "timestamp": "2025-11-15T11:00:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 3/9 complete: Phase 2.2 (Services)
     - Analyzed: [COUNT] service files
     - Documented: [COUNT] business workflows
     - Integrations found: [COUNT]
     - Lines generated: [COUNT]
   ```

### Chunk 4: Phase 2.3 - Data Layer

Complete **Section 2.3: Data Models & Repositories**:

- EVERY model/entity file analyzed
- Relationships documented (with cardinality)
- Validation rules extracted
- Database operations categorized
- NO placeholders

**After Chunk 4 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Section 2.3 content to analysis-report.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/phase-2-3-complete.json`
   - Content:

     ```json
     {
       "chunk": 4,
       "phase": "2.3",
       "phase_name": "Data Layer",
       "timestamp": "2025-11-15T11:15:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 4/9 complete: Phase 2.3 (Data Layer)
     - Analyzed: [COUNT] model files, [COUNT] repositories
     - Documented: [COUNT] entities, [COUNT] relationships
     - Lines generated: [COUNT]
   ```

### Chunk 5: Phase 3 - Positive Findings

Complete **Section 3: What's Working Well**:

- 10-30 positive findings with file:line references
- Evidence-based (not generic praise)
- Specific examples of good practices
- NO placeholders

**After Chunk 5 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Section 3 content to analysis-report.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/phase-3-complete.json`
   - Content:

     ```json
     {
       "chunk": 5,
       "phase": "3",
       "phase_name": "Positive Findings",
       "timestamp": "2025-11-15T11:30:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 5/9 complete: Phase 3 (Positive Findings)
     - Documented: [COUNT] positive findings
     - Good patterns found: [COUNT]
     - Lines generated: [COUNT]
   ```

### Chunk 6: Phase 4 - Technical Debt & Issues

Complete **Section 4: Technical Debt**:

- **4.1** Technical Debt (HIGH/MEDIUM/LOW severity)
- **4.2** Security Vulnerabilities (with CVE references)
- **4.3** Code Quality Issues (smells, duplication)
- **4.4** Architecture Issues (coupling, abstractions)
- 20-50 technical debt items categorized
- 10-30 security findings with risk scores
- NO placeholders

**After Chunk 6 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Section 4 (all subsections 4.1-4.4) to analysis-report.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/phase-4-complete.json`
   - Content:

     ```json
     {
       "chunk": 6,
       "phase": "4",
       "phase_name": "Technical Debt & Issues",
       "timestamp": "2025-11-15T11:45:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 6/9 complete: Phase 4 (Technical Debt)
     - Tech debt items: [COUNT]
     - Security findings: [COUNT]
     - Code quality issues: [COUNT]
     - Lines generated: [COUNT]
   ```

### Chunk 7: Phase 5 - Upgrade Path Analysis

Complete **Section 5: Upgrade Paths**:

- **5.1** Runtime/Framework Upgrades
- **5.2** Dependency Upgrades
- **5.3** Database Migration Paths
- All upgrade paths evaluated
- Breaking changes identified
- Effort estimates provided
- Risk assessment for each path
- NO placeholders

**After Chunk 7 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Section 5 (all subsections 5.1-5.3) to analysis-report.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/phase-5-complete.json`
   - Content:

     ```json
     {
       "chunk": 7,
       "phase": "5",
       "phase_name": "Upgrade Path Analysis",
       "timestamp": "2025-11-15T12:00:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 7/9 complete: Phase 5 (Upgrade Paths)
     - Upgrade paths evaluated: [COUNT]
     - Breaking changes identified: [COUNT]
     - Lines generated: [COUNT]
   ```

### Chunk 8: Phases 6-7 - Modernization & Feasibility

Complete **Sections 6 & 7**:

- **Section 6**: Modernization Recommendations
  - Quick wins (low effort, high value)
  - Strategic improvements
  - Long-term goals
- **Section 7**: Feasibility Scoring
  - Inline upgrade feasibility (formula shown)
  - Greenfield rewrite feasibility (formula shown)
  - Hybrid approach feasibility
- Recommendations prioritized
- Feasibility scores calculated with formulas
- NO placeholders

**After Chunk 8 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 6 & 7 to analysis-report.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/phase-6-7-complete.json`
   - Content:

     ```json
     {
       "chunk": 8,
       "phase": "6-7",
       "phase_name": "Modernization & Feasibility",
       "timestamp": "2025-11-15T12:15:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   ✓ Chunk 8/9 complete: Phases 6-7 (Modernization & Feasibility)
     - Recommendations: [COUNT]
     - Feasibility scores calculated
     - Lines generated: [COUNT]
   ```

### Chunk 9: Phases 8-9 - Decision Matrix & Final Recommendations

Complete **Sections 8 & 9**:

- **Section 8**: Decision Matrix
  - Comparison table: Time, Cost, Risk, Business Disruption
  - Scoring for each approach
- **Section 9**: Final Recommendations
  - Primary recommendation with confidence score (0-100%)
  - Immediate actions (next steps)
  - Short-term roadmap (0-6 months)
  - Long-term roadmap (6-18 months)
- Decision matrix complete
- Primary recommendation stated
- Roadmaps provided with milestones
- NO placeholders

**After Chunk 9 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 8 & 9 to analysis-report.md

2. **Create final checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/all-phases-complete.json`
   - Content:

     ```json
     {
       "chunk": 9,
       "phase": "8-9",
       "phase_name": "Decision Matrix & Final Recommendations",
       "timestamp": "2025-11-15T12:30:00Z",
       "status": "complete",
       "all_phases_complete": true
     }
     ```

3. **MANDATORY - Display progress and final summary**:

   ```text
   ✓ Chunk 9/9 complete: Phases 8-9 (Decision Matrix & Recommendations)
     - Decision matrix complete
     - Primary recommendation: [APPROACH]
     - Lines generated: [COUNT]

   ✅ analysis-report.md GENERATION COMPLETE
      Total lines: [COUNT]
      Total chunks: 9
      File path: .analysis/{project}-{timestamp}/analysis-report.md
      Analysis duration: [DURATION]
   ```

---

## Verification Gate (HARD STOP)

⚠️ **VERIFICATION GATE - CANNOT PROCEED WITHOUT PASSING**

**BEFORE** proceeding to Stage 5, verify report quality:

### Verification Checklist

Read analysis-report.md and verify:

- [ ] File exists at expected path: `.analysis/{project}-{timestamp}/analysis-report.md`
- [ ] All 9 phase headers present:
      - [ ] Phase 1: Project Discovery
      - [ ] Phase 2: Codebase Analysis
      - [ ] Phase 3: Positive Findings
      - [ ] Phase 4: Technical Debt & Issues
      - [ ] Phase 5: Upgrade Path Analysis
      - [ ] Phase 6: Modernization Recommendations
      - [ ] Phase 7: Feasibility Scoring
      - [ ] Phase 8: Decision Matrix
      - [ ] Phase 9: Final Recommendations
- [ ] Quality checks:
      - [ ] 50+ file:line references present throughout
      - [ ] Technical debt items have severity ratings (HIGH/MEDIUM/LOW)
      - [ ] Security vulnerabilities documented with risk scores
      - [ ] Feasibility scores calculated with formulas shown
      - [ ] Primary recommendation stated with confidence score (0-100%)
      - [ ] No placeholders (TODO, TBD, "will be analyzed", "coming soon")
      - [ ] All tables properly formatted (Markdown)
      - [ ] All code blocks have syntax highlighting
- [ ] Completeness (verify based on project size/complexity):
      - [ ] **Small projects (< 5,000 LOC)**:
            - Total lines: 1,000+ (minimum for comprehensive analysis)
            - Feature descriptions: 10-50 with evidence
            - Technical debt items: 5-20 categorized
            - Security findings: 3-10 with risk scores
      - [ ] **Medium projects (5,000-50,000 LOC)**:
            - Total lines: 3,000+ (minimum for comprehensive analysis)
            - Feature descriptions: 50-200 with evidence
            - Technical debt items: 20-50 categorized
            - Security findings: 10-30 with risk scores
      - [ ] **Large projects (> 50,000 LOC)**:
            - Total lines: 5,000+ (minimum for comprehensive analysis)
            - Feature descriptions: 100-500 with evidence
            - Technical debt items: 50-150 categorized
            - Security findings: 30-100 with risk scores

---

### Recovery Actions (IF ANY CHECKBOX FAILS)

**IF ANY checkbox is unchecked**:

```text
❌ VERIFICATION FAILED

analysis-report.md is incomplete. Issues found:
- [List specific missing items from checklist above]
```

**RECOVERY DECISION TREE**:

**1. Identify incomplete sections**:

List which phases or quality checks failed verification.

**2. Determine recovery approach**:

**IF** entire phases missing (e.g., Phase 5 not found in file):

- **Action**: Regenerate ONLY the missing phases
- **Method**:
  1. Check `.analysis/.checkpoints/` to identify last completed phase
  2. Resume generation from first missing phase
  3. Use Edit tool (str_replace) to append missing phases to existing file
  4. Create checkpoint markers for newly generated phases
  5. Re-run verification after regeneration

**IF** quality issues in existing phases (e.g., no file:line references in Phase 3):

- **Action**: Enhance the problematic phase with missing details
- **Method**:
  1. Read the incomplete phase from analysis-report.md
  2. Identify specific missing elements (file:line refs, severity ratings, etc.)
  3. Regenerate that phase section with proper detail
  4. Use Edit tool (str_replace) to replace the incomplete section
  5. Update checkpoint marker for that phase
  6. Re-run verification after enhancement

**IF** multiple critical failures (>3 phases missing OR >5 quality issues):

- **Action**: Recommend full regeneration from scratch
- **Display**:

  ```text
  ⚠️ MULTIPLE CRITICAL ISSUES DETECTED

  Issues found:
  - Missing phases: [COUNT]
  - Quality failures: [COUNT]

  Recommendation: Full regeneration recommended due to extent of issues.
  ```

- **Ask user**:

  ```text
  Recovery options:
  [A] Regenerate entire analysis-report.md from scratch
  [B] Fix individual sections (may take longer)
  [C] Proceed anyway (NOT RECOMMENDED - will cause issues in Stage 5)

  Your choice: ___
  ```

**3. Execute recovery**:

- Based on failure type, perform specific recovery actions
- Use appropriate tools (Edit/str_replace for fixes, Write for full regen)
- Create/update checkpoint markers after fixes
- Re-run verification after recovery
- **DO NOT proceed to Stage 5 until verification passes**

⚠️ **STOP HERE** - DO NOT CONTINUE TO NEXT STEP UNTIL VERIFICATION PASSES

---

### Verification Success

**IF ALL checkboxes are checked**:

```text
✅ VERIFICATION PASSED

analysis-report.md is complete and meets quality standards:
- All 9 phases present and complete
- 50+ file:line references found
- Technical debt properly categorized
- Security issues documented with risk scores
- Feasibility calculations shown
- No placeholders or incomplete sections
- Total lines: [COUNT] (comprehensive analysis)

Proceeding to Stage 5 (Artifact Generation)...
```

**Only after passing verification**: Proceed to Stage 5

---

## Output State

```json
{
  ...previous_state,
  "stage": "report_generation",
  "timestamp": "2025-11-14T11:30:00Z",
  "stages_complete": [..., "report_generation"],
  "report_generated": true,
  "report_path": ".analysis/{project}-{timestamp}/analysis-report.md",
  "report_stats": {
    "total_lines": 3450,
    "chunks_generated": 9,
    "file_references": 127,
    "tech_debt_items": 34,
    "security_findings": 18
  },
  "verification_passed": true
}
```text

---

## Completion Marker

```text
STAGE_COMPLETE:REPORT
STATE_PATH: .analysis/.state/04-report.json
```

---

## Next Stage

Proceed to: **Stage 5: 05-artifacts.md** (Generate remaining artifacts)
