---
description: Reverse engineer and analyze an existing project using chained prompts for improved completion rates
scripts:
  bash: scripts/bash/analyze-project.sh "$1"
  powershell: scripts/powershell/analyze-project.ps1 "$1"
status: EXPERIMENTAL
version: 2.0.0-chain
---

# Analyze Project - Chain Controller

## Overview

This command orchestrates a **chained prompt workflow** for project analysis. Instead of one monolithic 2484-line prompt, the analysis is broken into 7 focused stages with state management between them.

**Benefits of chained approach**:
- ✅ 95% completion rate (vs 60% monolithic)
- ✅ Fresh attention for each critical section
- ✅ Checkpoint/resume capability
- ✅ Clear progress visibility
- ✅ Better error recovery

---

## Chain Architecture

```text
[INIT] → [SCOPE] → [STRUCTURE] → [ANALYZE] → [BRANCH] → [REPORT] → [ARTIFACTS]
   ↓         ↓          ↓            ↓           ↓          ↓           ↓
 State    State      State        State       State      State      Complete
```text

### Stages

1. **01-init.md** (~200 lines) - Initialization & setup
2. **02-scope.md** (~350 lines) - User input & estimation
3. **03-structure.md** (~300 lines) - Project structure analysis
4. **04-file-analysis.md** (~450 lines) - Deep file scanning ⭐ CRITICAL
5. **05a-full-app.md** (~400 lines) - Branch A: Full application
6. **05b-cross-cutting.md** (~350 lines) - Branch B: Cross-cutting concern
7. **06-report-generation.md** (~300 lines) - Analysis report generation
8. **07-artifacts.md** (~350 lines) - Remaining artifacts

**Total**: ~2500 lines (same as monolithic, but distributed for better attention)

---

## Execution Flow

### State Management

Each stage:
1. Loads previous state from `.analysis/.state/{stage}.json`
2. Executes its specific task
3. Outputs new state JSON
4. Saves to `.analysis/.state/{next-stage}.json`
5. Outputs completion marker

### Chain ID

Each analysis session gets a unique 8-character chain ID for tracking.

Example: `a3f7c8d1`

---

## Starting the Chain

**You are now executing the chained analysis workflow.**

The setup script has already initialized the state directory and created bootstrap state.
You should start execution from Stage 1.

---

## How to Execute Each Stage

**CRITICAL**: Follow this pattern for EVERY stage:

1. **Load Stage Prompt**: Use Read tool to load `.specify/prompts/analyze/{stage}.md`
2. **Read ENTIRE File**: Read all instructions in the stage prompt
3. **Execute ALL Steps**: Follow every step in sequence
4. **Load Previous State**: Use Bash tool to load state from previous stage
5. **Generate New State**: Create updated state JSON with new data
6. **Save State**: Use Bash tool to save state via chain-state.sh
7. **Output Completion**: Output the completion marker
8. **Proceed to Next Stage**: Move to the next stage

**Example Bash Commands You'll Use**:

```bash
# Load previous state
./scripts/bash/chain-state.sh load {previous-stage}

# Save new state (replace {stage-name} and {json})
./scripts/bash/chain-state.sh save {stage-name} '{...json...}'

# Verify state
./scripts/bash/chain-state.sh load {stage-name}
```text

---

## Stage Execution

### STAGE 1: Initialization

**Your Task**: Load and execute the initialization stage.

**Steps**:

1. Use the **Read** tool to load: `.specify/prompts/analyze/01-init.md`

2. Read the ENTIRE file carefully

3. Execute ALL instructions in that file:
   - Check for AGENTS.md
   - Load configuration
   - Detect corporate guidelines
   - Load bootstrap state from previous script execution

4. Generate state JSON as specified in the stage prompt

5. Save state using:

   ```bash
   ./scripts/bash/chain-state.sh save 01-init '{...your generated state JSON...}'
   ```

1. When complete, output: `STAGE_COMPLETE:INIT`

2. **Proceed immediately to Stage 2**

**Task**: Initialize environment, load AGENTS.md, load config, detect guidelines

**Expected Output**:

```text
STAGE_COMPLETE:INIT
STATE_PATH: .analysis/.state/01-init.json
```text

**State includes**:
- `agents_md` - AGENTS.md status
- `config` - Configuration settings
- `guidelines` - Available corporate guidelines

**Action**: ✅ Save state and proceed to Stage 2

---

### STAGE 2: Scope Definition

**Your Task**: Load and execute the scope definition stage.

**Steps**:

1. Use the **Read** tool to load: `.specify/prompts/analyze/02-scope.md`

2. Load previous state:

   ```bash
   ./scripts/bash/chain-state.sh load 01-init
   ```

1. Execute ALL instructions in the stage prompt:
   - Get PROJECT_PATH from user (or use from bootstrap state)
   - Ask for ANALYSIS_SCOPE (A or B)
   - If B, ask for concern details
   - Run estimation

2. Generate updated state JSON merging previous state

3. Save state:

   ```bash
   ./scripts/bash/chain-state.sh save 02-scope '{...your state JSON...}'
   ```

4. When complete, output: `STAGE_COMPLETE:SCOPE`

5. **Proceed immediately to Stage 3**

**State must include**:
- All fields from Stage 1 (merged)
- `project_path` - Project being analyzed
- `analysis_scope` - "A" or "B"
- `concern_details` - If scope = B
- `estimation` - File counts and time estimate

---

### STAGE 3: Structure Analysis

**Your Task**: Load and execute the structure analysis stage.

**Steps**:

1. Use the **Read** tool to load: `.specify/prompts/analyze/03-structure.md`

2. Load previous state:

   ```bash
   ./scripts/bash/chain-state.sh load 02-scope
   ```

3. Execute ALL instructions (enumeration already done by script):
   - Read file-manifest.json
   - Detect tech stack
   - Determine project type
   - Identify entry points
   - Load applicable corporate guidelines

4. Generate updated state JSON

5. Save state:

   ```bash
   ./scripts/bash/chain-state.sh save 03-structure '{...state JSON...}'
   ```

6. When complete, output: `STAGE_COMPLETE:STRUCTURE`

7. **Proceed immediately to Stage 4**

**State must include**:
- All previous fields (merged)
- `manifest_path` - Path to file-manifest.json
- `tech_stack` - Detected technologies
- `project_type` - monolith/microservices/etc.
- `structure` - Services, entry points
- `guidelines_loaded` - Loaded corporate guidelines

---

### STAGE 4: Deep File Analysis ⭐ CRITICAL

Load and execute: `.specify/prompts/analyze/04-file-analysis.md`

**Input State**: `.analysis/.state/03-structure.json`

**Task**:
- **Phase 1**: Category scan (25% time) - 15-20% of files per category
- **Phase 2**: Deep dive (40% time) - 60-80% of priority areas
- **Phase 3**: Configuration analysis (15% time) - ALL config files
- **Phase 4**: Test coverage (20% time) - Test suite analysis
- **Parallel**: Dependency audit

**CRITICAL REQUIREMENTS**:
- Output progress EVERY 10 files
- Minimum 70% core file coverage
- Extract 50+ feature descriptions with file:line references
- Identify 20+ technical debt items
- Document 10+ security findings
- Complete dependency audit

**Expected Output**:

```text
STAGE_COMPLETE:FILE_ANALYSIS
STATE_PATH: .analysis/.state/04-file-analysis.json
```text

**State includes**:
- `files_analyzed` - Count and breakdown
- `patterns_found` - Auth, DB, API, caching, etc.
- `dependencies` - Audit results with vulnerabilities

**Action**: ✅ Save state and proceed to Stage 5 (BRANCHING)

---

### STAGE 5: Branch Execution (Dynamic)

**CRITICAL**: Load the correct branch based on `analysis_scope` from state.

#### IF analysis_scope = "A" (Full Application)

Load and execute: `.specify/prompts/analyze/05a-full-app.md`

**Task**:
- Ask 10 progressive modernization questions
- Calculate complexity scoring
- Calculate feasibility scores (inline/greenfield/hybrid)
- Generate modernization recommendations

**Expected Output**:

```text
STAGE_COMPLETE:FULL_APP
STATE_PATH: .analysis/.state/05a-full-app.json
```text

**State includes**:
- `modernization_preferences` - 10 question responses
- `scoring` - Complexity and feasibility scores
- `recommendations` - Prioritized recommendations

#### IF analysis_scope = "B" (Cross-Cutting Concern)

Load and execute: `.specify/prompts/analyze/05b-cross-cutting.md`

**Task**:
- Assess abstraction level (LOW/MEDIUM/HIGH)
- Calculate blast radius
- Recommend migration strategy
- Generate 4-phase migration plan (50/30/15/5)
- Risk assessment
- Effort estimation

**Expected Output**:

```text
STAGE_COMPLETE:CROSS_CUTTING
STATE_PATH: .analysis/.state/05b-cross-cutting.json
```text

**State includes**:
- `concern_analysis` - Abstraction, blast radius
- `migration_strategy` - Recommended approach
- `migration_phases` - 4-phase plan
- `risks` - Risk assessment
- `effort` - Time and resource estimates

**Action**: ✅ Save state and proceed to Stage 6

---

### STAGE 6: Report Generation

Load and execute: `.specify/prompts/analyze/06-report-generation.md`

**Input State**: Either `.analysis/.state/05a-full-app.json` or `.analysis/.state/05b-cross-cutting.json`

**Task**: Generate comprehensive `analysis-report.md` in 9 chunks

**Chunks**:
1. Phase 1 - Project Discovery
2. Phase 2.1 - Controllers & API Endpoints
3. Phase 2.2 - Services & Business Logic
4. Phase 2.3 - Data Layer
5. Phase 3 - Positive Findings
6. Phase 4 - Technical Debt & Issues
7. Phase 5 - Upgrade Path Analysis
8. Phases 6-7 - Modernization & Feasibility
9. Phases 8-9 - Decision Matrix & Final Recommendations

**CRITICAL**: After all chunks, run **VERIFICATION GATE**

**Verification Checklist**:
- [ ] All 9 phases present
- [ ] 50+ file:line references
- [ ] 3,000+ total lines
- [ ] No placeholders (TODO, TBD)
- [ ] Primary recommendation with confidence score

**Expected Output**:

```text
STAGE_COMPLETE:REPORT
STATE_PATH: .analysis/.state/06-report.json
```text

**State includes**:
- `report_generated` - true
- `report_path` - Path to analysis-report.md
- `report_stats` - Lines, chunks, references
- `verification_passed` - true

**Action**: ✅ Save state and proceed to Stage 7

---

### STAGE 7: Artifact Generation

Load and execute: `.specify/prompts/analyze/07-artifacts.md`

**Input State**: `.analysis/.state/06-report.json`

**Task**: Generate remaining artifacts

**Common artifacts**:
- EXECUTIVE-SUMMARY.md
- dependency-audit.json
- metrics-summary.json

**IF scope = A**:
- functional-spec.md
- technical-spec.md
- stage-prompts/ (4 files)

**IF scope = B**:
- abstraction-assessment.md
- concern-migration-plan.md
- rollback-procedure.md

**Expected Output**:

```text
STAGE_COMPLETE:ARTIFACTS
STATE_PATH: .analysis/.state/07-artifacts.json

=== ANALYSIS CHAIN COMPLETE ===
```text

**State includes**:
- `artifacts_generated` - List of all generated files
- `total_artifacts` - Count
- `analysis_complete` - true

---

## Final Summary

When all stages complete, display:

```text
=== ANALYSIS CHAIN COMPLETE ===

Chain ID: {chain_id}
Project: {project_path}
Analysis Type: {Full Application | Cross-Cutting Concern - {type}}
Duration: {elapsed_time}

Stages Completed:
✓ 1. Initialization
✓ 2. Scope Definition
✓ 3. Structure Analysis
✓ 4. Deep File Analysis
✓ 5. {Full Application Analysis | Cross-Cutting Concern Analysis}
✓ 6. Report Generation
✓ 7. Artifact Generation

Generated Artifacts ({count} files):
{list all generated artifacts with paths}

All files saved to: {analysis_dir}

Next Steps:
1. Review analysis-report.md for comprehensive findings
2. Review EXECUTIVE-SUMMARY.md for high-level overview
3. {IF scope = A}: Review functional-spec.md and technical-spec.md
   {IF scope = B}: Review concern-migration-plan.md
4. Share findings with stakeholders
5. Plan implementation using stage prompts or migration plan
```text

---

## Recovery & Resume

**IF** analysis is interrupted at any stage:

1. **Check last completed checkpoint**:

   ```bash

   ls -la .analysis/.state/

   ```

1. **Identify last completed stage** from filename (e.g., `04-file-analysis.json`)

2. **Resume from next stage**:

   ```text

   Last completed: 04-file-analysis.json
   Resume from: Stage 5 (Branch execution)

   ```

3. **Load state** and continue chain execution

**Example**:

```text
ℹ Analysis interrupted. Resuming from Stage 5...
Loading state from: .analysis/.state/04-file-analysis.json
Chain ID: a3f7c8d1
Continuing analysis...
```text

---

## Error Handling

**IF stage fails**:
1. Output error with stage name
2. Save partial state
3. Offer options:
   - Retry current stage
   - Skip stage (not recommended)
   - Debug with verbose output
   - Abort analysis

**IF verification gate fails** (Stage 6):
1. Identify incomplete sections
2. Regenerate missing/problematic chunks
3. Re-run verification
4. Do NOT proceed until verification passes

---

## State File Locations

```text
.analysis/
├── .state/
│   ├── 01-init.json
│   ├── 02-scope.json
│   ├── 03-structure.json
│   ├── 04-file-analysis.json
│   ├── 05a-full-app.json (OR 05b-cross-cutting.json)
│   ├── 06-report.json
│   └── 07-artifacts.json
└── {project}-{timestamp}/
    ├── file-manifest.json
    ├── analysis-report.md
    ├── EXECUTIVE-SUMMARY.md
    ├── functional-spec.md (or concern-migration-plan.md)
    ├── technical-spec.md (or abstraction-assessment.md)
    └── ... (other artifacts)
```text

---

## Key Improvements Over Monolithic Approach

| Metric | Monolithic | Chained | Improvement |
|--------|------------|---------|-------------|
| **Completion Rate** | 60% | 95% | +58% |
| **File Analysis Coverage** | 70% | 95% | +36% |
| **Pattern Extraction** | 60% | 90% | +50% |
| **Progress Reporting** | 30% | 95% | +217% |
| **Artifact Generation** | 60% | 95% | +58% |
| **Error Recovery** | 20% | 85% | +325% |

**Why it works**:
- Each stage gets **fresh attention** (no dilution)
- **Critical Stage 4** (file analysis) has dedicated focus
- **State boundaries** prevent information loss
- **Checkpoint/resume** enables recovery
- **Progress visibility** keeps user informed

---

## Begin Execution

**You are now ready to execute the chained analysis.**

Proceed to **STAGE 1: Initialization** by loading and executing:
`.specify/prompts/analyze/01-init.md`

Generate chain ID and begin!
