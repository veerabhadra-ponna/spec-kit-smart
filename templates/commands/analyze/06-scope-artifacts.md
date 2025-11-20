---
stage: scope_artifact_generation
requires: 05-artifacts.json
outputs: all_artifacts_complete
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

# Stage 6: Scope-Specific Artifacts Generation

## Purpose

Generate scope-specific artifacts based on analysis scope (A or B). This stage runs after common artifacts (EXECUTIVE-SUMMARY.md, dependency-audit.json, metrics-summary.json) have been generated in Stage 5. The artifacts generated here are tailored to the specific modernization needs identified during the analysis.

---

## Previous State

Load state from: `.analysis/.state/05-artifacts.json`

Required:

- `common_artifacts_complete` must be `true`
- `analysis_scope` determines which artifacts to generate (A = Full Application, B = Cross-Cutting Concern)

---

## CRITICAL: Generate BOTH Functional Specs (Scope = A)

STOP - READ THIS BEFORE GENERATING ANY FUNCTIONAL SPECS

For Full Application Modernization, you MUST generate TWO separate functional specs:

1. **functional-spec-legacy.md** - What the LEGACY system does TODAY
2. **functional-spec-target.md** - What the MODERNIZED system WILL do

**THIS IS MANDATORY - DO NOT GENERATE JUST ONE SPEC. GENERATE BOTH.**

**IF YOU GENERATE ONLY ONE FUNCTIONAL SPEC, THIS IS A CRITICAL ERROR.**

**DO NOT:**

- Generate only functional-spec-legacy.md and stop
- Generate only functional-spec-target.md and stop
- Combine both into a single file
- Skip either spec thinking "the user can infer the other"
- Proceed to stage-prompts/ without generating both specs

**YOU MUST GENERATE BOTH SPECS IN SEQUENCE:**

1. Generate functional-spec-legacy.md (5 chunks) FIRST
2. THEN generate functional-spec-target.md (5 chunks)
3. ONLY AFTER BOTH are complete - proceed to technical-spec.md

**Why Two Specs?**

- Legacy spec: Documents current functionality (source of truth for what exists)
- Target spec: Documents desired functionality (what to build)
- Prevents confusion about which app is being documented
- Gives user complete documentation set
- Enables comparison between before/after states

---

## Full Application Artifacts (Scope = A)

### Artifact 4A-Legacy (Scope = A): functional-spec-legacy.md

**Purpose**: Functional specification for LEGACY/EXISTING application (WHAT system CURRENTLY does)

**CRITICAL - SOURCE OF TRUTH:**

- **Source**: ONLY use analysis-report.md Phase 2 (Feature Catalog) and Phase 3 (Positive Findings)
- **Scope**: Document EXISTING functionality as currently implemented in legacy code
- **Target Audience**: Developers/analysts who need to understand what the legacy app does today
- **Forbidden**: Do NOT include modernization preferences, target tech stack, or future state

**Content Rules:**

1. **Features**: Extract from analysis-report.md Phase 2 exactly as analyzed from legacy code
2. **File References**: Every feature MUST reference legacy code with file:line notation
3. **Technology**: Describe as-implemented (e.g., "Uses custom JWT authentication" not "Should use OAuth2")
4. **Tense**: Present tense (e.g., "The system validates..." not "The system should validate...")
5. **Completeness**: Document what exists, not what's missing

**Source**: Extract features from analysis-report.md

**Template**: Read `.specify/templates/analyze/functional-spec-template.md` for structure

**Chunking Strategy** (Generate in 5 chunks):

#### Chunk 1: Introduction + Summary + Scope

- Sections: 1 (Introduction), 2 (Executive Summary), 3 (Scope)
- Content: Project overview, high-level purpose, what's in/out of scope
- Completion: All 3 sections complete, no placeholders

**After Chunk 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `.analysis/{project}-{timestamp}/functional-spec-legacy.md`
   - Content: Complete sections 1-3

2. **Create checkpoint marker**:
   - Create directory: `.analysis/.checkpoints/` (if not exists)
   - Write JSON file: `.analysis/.checkpoints/functional-spec-chunk-1-complete.json`
   - Content:

     ```json
     {
       "artifact": "functional-spec-legacy.md",
       "chunk": 1,
       "total_chunks": 5,
       "sections": "Introduction + Summary + Scope",
       "timestamp": "2025-11-15T10:30:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   functional-spec-legacy.md Chunk 1/5 complete: Introduction + Summary + Scope
     - Lines: [COUNT]
   ```

#### Chunk 2: User Stories (Part 1) - CRITICAL Features

- Section: 4.1 (User Stories - CRITICAL)
- Content: All CRITICAL features from analysis-report.md
- Every feature MUST have file:line reference
- Completion: All CRITICAL features documented with evidence

**After Chunk 2 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Read existing functional-spec-legacy.md
   - Append Section 4.1 content to the end
   - Use str_replace to append (not overwrite)

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/functional-spec-chunk-2-complete.json`
   - Content:

     ```json
     {
       "artifact": "functional-spec-legacy.md",
       "chunk": 2,
       "total_chunks": 5,
       "sections": "User Stories (CRITICAL)",
       "timestamp": "2025-11-15T10:45:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   functional-spec-legacy.md Chunk 2/5 complete: User Stories (CRITICAL)
     - Features: [COUNT]
     - Lines: [COUNT]
   ```

#### Chunk 3: User Stories (Part 2) - STANDARD Features + Business Rules

- Sections: 4.2 (User Stories - STANDARD), 5 (Business Rules)
- Content: STANDARD features + validation rules
- Completion: All STANDARD features + rules documented

**After Chunk 3 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 4.2 & 5 content to functional-spec-legacy.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/functional-spec-chunk-3-complete.json`
   - Content:

     ```json
     {
       "artifact": "functional-spec-legacy.md",
       "chunk": 3,
       "total_chunks": 5,
       "sections": "STANDARD Features + Rules",
       "timestamp": "2025-11-15T11:00:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   functional-spec-legacy.md Chunk 3/5 complete: STANDARD Features + Rules
     - Features: [COUNT]
     - Lines: [COUNT]
   ```

#### Chunk 4: NFRs + Data Requirements

- Sections: 6 (Non-Functional Requirements), 7 (Data Requirements)
- Content: Performance, security, scalability, data entities
- Completion: NFRs defined, data models documented

**After Chunk 4 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 6 & 7 content to functional-spec-legacy.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/functional-spec-chunk-4-complete.json`
   - Content:

     ```json
     {
       "artifact": "functional-spec-legacy.md",
       "chunk": 4,
       "total_chunks": 5,
       "sections": "NFRs + Data",
       "timestamp": "2025-11-15T11:15:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   functional-spec-legacy.md Chunk 4/5 complete: NFRs + Data
     - Lines: [COUNT]
   ```

#### Chunk 5: Acceptance Criteria + Assumptions + Constraints

- Sections: 8 (Acceptance Criteria), 9 (Assumptions), 10 (Constraints)
- Content: Testing criteria, assumptions, limitations
- Completion: All sections complete, no placeholders

**After Chunk 5 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 8, 9 & 10 content to functional-spec-legacy.md

2. **Create final checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/functional-spec-complete.json`
   - Content:

     ```json
     {
       "artifact": "functional-spec-legacy.md",
       "chunk": 5,
       "total_chunks": 5,
       "sections": "Acceptance Criteria + Assumptions + Constraints",
       "timestamp": "2025-11-15T11:30:00Z",
       "status": "complete",
       "all_chunks_complete": true
     }
     ```

3. **MANDATORY - Display progress and final summary**:

   ```text
   functional-spec-legacy.md Chunk 5/5 complete: Acceptance + Assumptions + Constraints
     - Lines: [COUNT]

   functional-spec-legacy.md COMPLETE (5/5 chunks)
      Total features: [COUNT]
      Total lines: [COUNT]
   ```

**Progress**: `Generated: functional-spec-legacy.md ({lines} lines, {chunks} chunks)`

---

## CHECKPOINT: Legacy Spec Complete - Now Generate Target Spec

MANDATORY CHECKPOINT - DO NOT SKIP

You just completed functional-spec-legacy.md. DO NOT STOP HERE.

### NEXT REQUIRED STEP: Generate functional-spec-target.md

**Verify before proceeding:**

- [ ] functional-spec-legacy.md is complete (all 5 chunks)
- [ ] All sections present (Introduction through Constraints)
- [ ] No placeholders or TODOs
- [ ] Checkpoint file exists: `.analysis/.checkpoints/functional-spec-complete.json`

### NOW IMMEDIATELY PROCEED TO GENERATE functional-spec-target.md

**DO NOT:**

- Skip to technical-spec.md
- Skip to stage-prompts/
- Mark artifact generation as complete
- Proceed to final summary

### ONLY AFTER functional-spec-target.md is ALSO complete can you proceed to technical-spec.md

---

### Artifact 4A-Target (Scope = A): functional-spec-target.md

**Purpose**: Functional specification for TARGET/MODERNIZED application (WHAT system WILL do)

**CRITICAL - FUTURE STATE:**

- **Source**: Use analysis-report.md + user's 10 modernization preferences from Stage 3A
- **Scope**: Document DESIRED functionality for modernized application
- **Target Audience**: Developers/PMs who will implement the modernized system
- **Requirements**: Include user's chosen tech stack, new capabilities, improvements

**Content Rules:**

1. **Features**: Base on legacy features BUT enhanced with modernization improvements
2. **Technology References**: Use user's chosen target stack (from 10 questions)
3. **Tense**: Future tense ("The system will..." or "Users will be able to...")
4. **Enhancements**: Include new capabilities enabled by modernization
5. **Out of Scope**: Explicitly document what is NOT being migrated (based on user's scope validation)

**CRITICAL - Scope Boundaries:**

Review user's answers to 10 modernization questions and scope validation from Stage 3A:

- **IN SCOPE**: Components where user provided explicit target (e.g., "PostgreSQL 15")
- **OUT OF SCOPE**: Components where user skipped/provided no answer (use existing as-is)

**DO NOT assume migration for unmentioned components.**

**Example**:

- Database: User said "PostgreSQL 15" - IN SCOPE, document migration
- Caching: User pressed Enter/skipped - OUT OF SCOPE, document "Use existing Memcached as-is"

**Chunking Strategy** (Generate in 5 chunks, similar to legacy spec but future-tense):

- Use same 5-chunk structure as legacy spec
- Change all tense to future ("will", "will be able to")
- Include modernization enhancements
- Document scope boundaries clearly
- File path: `.analysis/{project}-{timestamp}/functional-spec-target.md`

**IMPORTANT - This is the SECOND of TWO required functional specs:**

1. functional-spec-legacy.md (COMPLETED)
2. functional-spec-target.md (GENERATING NOW - 5 chunks)

Follow the same 5-chunk pattern as legacy spec with proper checkpoint markers.

**After completing ALL 5 chunks of functional-spec-target.md:**

Display final completion message:

```text
BOTH FUNCTIONAL SPECS COMPLETE
   1. functional-spec-legacy.md - LEGACY system (what exists today)
   2. functional-spec-target.md - TARGET system (what will be built)

   Now proceeding to technical-spec.md...
```

**Progress**: `Generated: functional-spec-target.md ({lines} lines, {chunks} chunks)`

---

### Artifact 5A (Scope = A): technical-spec.md

**Purpose**: Technical specification for modernized implementation (HOW to build)

**Source**: analysis-report.md + user's modernization preferences (from 10 questions)

**Template**: Read `.specify/templates/analyze/technical-spec-template.md` for structure

**Chunking Strategy** (Generate in 5 chunks):

#### Chunk 1: Architecture Overview + Legacy vs Target Comparison

- Sections: 1 (Introduction), 2 (Architecture Overview), 3 (Legacy vs Target)
- Content: System architecture, comparison tables, Mermaid diagrams
- Completion: Architecture patterns documented, comparison complete

**After Chunk 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `.analysis/{project}-{timestamp}/technical-spec.md`
   - Content: Complete sections 1-3

2. **Create checkpoint marker**:
   - Create directory: `.analysis/.checkpoints/` (if not exists)
   - Write JSON file: `.analysis/.checkpoints/technical-spec-chunk-1-complete.json`
   - Content:

     ```json
     {
       "artifact": "technical-spec.md",
       "chunk": 1,
       "total_chunks": 5,
       "sections": "Architecture + Comparison",
       "timestamp": "2025-11-15T10:30:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   technical-spec.md Chunk 1/5 complete: Architecture + Comparison
     - Diagrams: [COUNT]
     - Lines: [COUNT]
   ```

#### Chunk 2: Target Tech Stack + Data Architecture

- Sections: 4 (Target Tech Stack), 5 (Data Architecture)
- Content: User's chosen stack (from 10 questions), database design, ORM
- Completion: All tech choices documented, data layer designed

**After Chunk 2 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Read existing technical-spec.md
   - Append Sections 4 & 5 content to the end
   - Use str_replace to append (not overwrite)

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/technical-spec-chunk-2-complete.json`
   - Content:

     ```json
     {
       "artifact": "technical-spec.md",
       "chunk": 2,
       "total_chunks": 5,
       "sections": "Tech Stack + Data",
       "timestamp": "2025-11-15T10:45:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   technical-spec.md Chunk 2/5 complete: Tech Stack + Data
     - Lines: [COUNT]
   ```

#### Chunk 3: API Design + Integration Points

- Sections: 6 (API Design), 7 (Integration Architecture)
- Content: REST/GraphQL design, external APIs, message queues
- Completion: API contracts defined, integrations documented

**After Chunk 3 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 6 & 7 content to technical-spec.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/technical-spec-chunk-3-complete.json`
   - Content:

     ```json
     {
       "artifact": "technical-spec.md",
       "chunk": 3,
       "total_chunks": 5,
       "sections": "API + Integrations",
       "timestamp": "2025-11-15T11:00:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   technical-spec.md Chunk 3/5 complete: API + Integrations
     - Endpoints: [COUNT]
     - Lines: [COUNT]
   ```

#### Chunk 4: Security + Authentication + Deployment

- Sections: 8 (Security), 9 (Deployment Strategy)
- Content: User's chosen auth (Q9), deployment target (Q5), IaC (Q6), containers (Q7)
- Completion: Security measures defined, deployment plan complete

**After Chunk 4 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 8 & 9 content to technical-spec.md

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/technical-spec-chunk-4-complete.json`
   - Content:

     ```json
     {
       "artifact": "technical-spec.md",
       "chunk": 4,
       "total_chunks": 5,
       "sections": "Security + Deployment",
       "timestamp": "2025-11-15T11:15:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   technical-spec.md Chunk 4/5 complete: Security + Deployment
     - Lines: [COUNT]
   ```

#### Chunk 5: Testing Strategy + Observability + Migration Risks

- Sections: 10 (Testing), 11 (Observability), 12 (Migration Risks)
- Content: User's testing choice (Q10), observability stack (Q8), risk mitigation
- Completion: All sections complete, no placeholders

**After Chunk 5 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 10, 11 & 12 content to technical-spec.md

2. **Create final checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/technical-spec-complete.json`
   - Content:

     ```json
     {
       "artifact": "technical-spec.md",
       "chunk": 5,
       "total_chunks": 5,
       "sections": "Testing + Observability + Risks",
       "timestamp": "2025-11-15T11:30:00Z",
       "status": "complete",
       "all_chunks_complete": true
     }
     ```

3. **MANDATORY - Display progress and final summary**:

   ```text
   technical-spec.md Chunk 5/5 complete: Testing + Observability + Risks
     - Lines: [COUNT]

   technical-spec.md COMPLETE (5/5 chunks)
      Total lines: [COUNT]
   ```

**Progress**: `Generated: technical-spec.md ({lines} lines, {chunks} chunks)`

---

### Artifact 6A (Scope = A): stage-prompts/

**Purpose**: Staged implementation prompts for Spec Kit workflow integration

**Templates**: Read from `.specify/templates/analyze/stage-prompt-templates/`

Generate 4 stage prompt files for Spec Kit workflow:

**constitution-prompt.md**: Extract project principles from legacy code

- Template: `.specify/templates/analyze/stage-prompt-templates/constitution-prompt-template.md`
- Fill with: Project values, coding standards, architecture decisions extracted from analysis
- Purpose: Use with `/speckit.constitution` command

**clarify-prompt.md**: Use legacy code as source of truth for clarifications

- Template: `.specify/templates/analyze/stage-prompt-templates/clarify-prompt-template.md`
- Fill with: Legacy code references (file:line), ambiguity resolution patterns, critical behaviors
- Purpose: Use with `/speckit.clarify` command when specs are unclear

**tasks-prompt.md**: Break down implementation with legacy complexity awareness

- Template: `.specify/templates/analyze/stage-prompt-templates/tasks-prompt-template.md`
- Fill with: Legacy feature complexity scores, migration task breakdowns, effort estimates
- Purpose: Use with `/speckit.tasks` command

**implement-prompt.md**: Reference legacy code during implementation

- Template: `.specify/templates/analyze/stage-prompt-templates/implement-prompt-template.md`
- Fill with: Legacy code patterns (with file:line), must-preserve behaviors, edge cases
- Purpose: Use with `/speckit.implement` command

**Instructions**:

1. Read all 4 templates from `.specify/templates/analyze/stage-prompt-templates/`
2. Fill each template with specific data from analysis-report.md
3. Include file:line references for all legacy code examples
4. Mark CRITICAL behaviors that must be preserved exactly

**Progress**: `Generated: stage-prompts/ (4 files)`

---

## Cross-Cutting Concern Artifacts (Scope = B)

### Artifact 4B (Scope = B): abstraction-assessment.md

**Purpose**: Detailed abstraction analysis for the concern

**Template**: Read `.specify/templates/analyze/concern-analysis-template.md` for structure

**Content**:

```markdown
# Abstraction Assessment: {Concern Type}

## Current Implementation

- Type: {current_implementation}
- Abstraction Level: {LOW | MEDIUM | HIGH}
- Abstraction Score: {score}/10

## Touch Points Analysis

{detailed touch points with file:line references}

## Coupling Analysis

{coupling details, dependencies, tightness}

## Refactoring Recommendations

{specific refactoring steps to improve abstraction}

## Migration Readiness

{assessment of readiness for migration}
```

**Instructions**:

1. Read template: `.specify/templates/analyze/concern-analysis-template.md`
2. Fill in all sections using data from Stage 3B
3. Provide detailed analysis with code references

**Progress**: `Generated: abstraction-assessment.md`

---

### Artifact 5B (Scope = B): concern-migration-plan.md

**Purpose**: Step-by-step migration strategy for the specific concern

**Source**: Recommended strategy from Stage 6B + TARGET_IMPLEMENTATION

**Template**: Read `.specify/templates/analyze/concern-migration-plan-template.md` for structure

**Chunking Strategy** (Generate in 3 chunks):

#### Chunk 1: Migration Strategy + Phasing

- Sections: 1 (Executive Summary), 2 (Migration Strategy), 3 (Phased Plan)
- Content: Chosen approach, justification, 50/30/15/5 phasing, timeline
- Completion: Strategy documented, phases defined with milestones

**After Chunk 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `.analysis/{project}-{timestamp}/concern-migration-plan.md`
   - Content: Complete sections 1-3

2. **Create checkpoint marker**:
   - Create directory: `.analysis/.checkpoints/` (if not exists)
   - Write JSON file: `.analysis/.checkpoints/concern-migration-plan-chunk-1-complete.json`
   - Content:

     ```json
     {
       "artifact": "concern-migration-plan.md",
       "chunk": 1,
       "total_chunks": 3,
       "sections": "Strategy + Phasing",
       "timestamp": "2025-11-15T10:30:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   concern-migration-plan.md Chunk 1/3 complete: Strategy + Phasing
     - Approach: [APPROACH]
     - Phases: [COUNT]
     - Lines: [COUNT]
   ```

#### Chunk 2: Technical Implementation + Testing

- Sections: 4 (Setup Steps), 5 (Code Changes), 6 (Testing Strategy)
- Content: Environment setup, required code changes, test plan, rollback procedures
- Completion: Implementation steps detailed, testing strategy complete

**After Chunk 2 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Read existing concern-migration-plan.md
   - Append Sections 4, 5 & 6 content to the end
   - Use str_replace to append (not overwrite)

2. **Create checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/concern-migration-plan-chunk-2-complete.json`
   - Content:

     ```json
     {
       "artifact": "concern-migration-plan.md",
       "chunk": 2,
       "total_chunks": 3,
       "sections": "Implementation + Testing",
       "timestamp": "2025-11-15T10:45:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:

   ```text
   concern-migration-plan.md Chunk 2/3 complete: Implementation + Testing
     - Setup steps: [COUNT]
     - Code changes: [COUNT]
     - Lines: [COUNT]
   ```

#### Chunk 3: Deployment + Operations + Success Criteria

- Sections: 7 (Deployment Strategy), 8 (Monitoring), 9 (Success Criteria), 10 (Post-Migration)
- Content: Deployment approach, monitoring/alerting, success metrics, post-migration tasks
- Completion: All sections complete, operational plan ready

**After Chunk 3 Generation**:

1. **Append to file** using Edit tool (str_replace):
   - Append Sections 7, 8, 9 & 10 content to concern-migration-plan.md

2. **Create final checkpoint marker**:
   - Write JSON file: `.analysis/.checkpoints/concern-migration-plan-complete.json`
   - Content:

     ```json
     {
       "artifact": "concern-migration-plan.md",
       "chunk": 3,
       "total_chunks": 3,
       "sections": "Deployment + Operations + Success",
       "timestamp": "2025-11-15T11:00:00Z",
       "status": "complete",
       "all_chunks_complete": true
     }
     ```

3. **MANDATORY - Display progress and final summary**:

   ```text
   concern-migration-plan.md Chunk 3/3 complete: Deployment + Operations + Success
     - Lines: [COUNT]

   concern-migration-plan.md COMPLETE (3/3 chunks)
      Total lines: [COUNT]
   ```

**Progress**: `Generated: concern-migration-plan.md ({lines} lines, {chunks} chunks)`

---

### Artifact 6B (Scope = B): rollback-procedure.md

**Purpose**: Detailed rollback procedure in case of issues

**Content**:

```markdown
# Rollback Procedure: {Concern Type} Migration

## When to Rollback

{criteria for triggering rollback}

## Rollback Steps

### Step 1: {action}

{detailed instructions}

### Step 2: {action}

{detailed instructions}

## Verification

{how to verify successful rollback}

## Post-Rollback Actions

{cleanup and next steps}
```

**Progress**: `Generated: rollback-procedure.md`

---

## Final Verification Checklist

**Before proceeding to completion, verify all scope-specific artifacts:**

### For Scope = A (Full Application)

- [ ] **BOTH** functional-spec-legacy.md AND functional-spec-target.md generated (2 specs required)
- [ ] functional-spec-legacy.md complete (all 5 chunks)
- [ ] functional-spec-target.md complete (all 5 chunks)
- [ ] technical-spec.md generated (all 5 chunks)
- [ ] stage-prompts/ directory with 4 files:
  - [ ] constitution-prompt.md
  - [ ] clarify-prompt.md
  - [ ] tasks-prompt.md
  - [ ] implement-prompt.md
- [ ] All artifacts validated (no placeholders, no TODOs)
- [ ] All checkpoint files created in `.analysis/.checkpoints/`

### For Scope = B (Cross-Cutting Concern)

- [ ] abstraction-assessment.md generated
- [ ] concern-migration-plan.md complete (all 3 chunks)
- [ ] rollback-procedure.md generated
- [ ] All artifacts validated (no placeholders, no TODOs)
- [ ] All checkpoint files created in `.analysis/.checkpoints/`

**IF any checkbox is unchecked, STOP and fix the issue before proceeding.**

---

## Output State

```json
{
  "...previous_state": "...",
  "stage": "scope_artifact_generation",
  "timestamp": "2025-11-14T12:00:00Z",
  "stages_complete": ["...", "scope_artifact_generation"],
  "scope_artifacts_generated": [
    "functional-spec-legacy.md",
    "functional-spec-target.md",
    "technical-spec.md",
    "stage-prompts/constitution-prompt.md",
    "stage-prompts/clarify-prompt.md",
    "stage-prompts/tasks-prompt.md",
    "stage-prompts/implement-prompt.md"
  ],
  "total_scope_artifacts": 7,
  "all_artifacts_complete": true
}
```

---

## Completion Marker

```text
STAGE_COMPLETE:SCOPE_ARTIFACTS
STATE_PATH: .analysis/.state/06-scope-artifacts.json

=== ANALYSIS CHAIN COMPLETE ===
Chain ID: {chain_id}
All stages successfully completed.
```

---

## End of Chain

This is the final stage. Analysis is complete!
