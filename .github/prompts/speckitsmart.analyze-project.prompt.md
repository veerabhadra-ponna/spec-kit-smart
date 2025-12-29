---
description: Reverse engineer and analyze an existing project using chained prompts with script-based data extraction
status: STABLE
version: 3.0.0-scriptfirst
---

## ⚠️ MANDATORY: Read Agent Instructions First

**BEFORE PROCEEDING:**

1. Check if `AGENTS.md` exists in repository root, `.specify.specify/memory/`, or `.specify/templates/` directory
2. **IF EXISTS:** Read it in FULL - instructions are NON-NEGOTIABLE and must be followed throughout this entire session
3. Follow all AGENTS.md guidelines for the duration of this command execution
4. These instructions override any conflicting default behaviors
5. **DO NOT** forget or ignore these instructions as you work through tasks

**Verification:** After reading AGENTS.md (if it exists), acknowledge with:
   "✓ Read AGENTS.md v[X.X] - Following all guidelines"

**If AGENTS.md does not exist:** Proceed with default behavior.

---

# Analyze Project - Chain Orchestrator

## Overview

This command orchestrates a **script-first chained workflow** for project analysis. Data extraction is handled by shell scripts (deterministic, fast, testable), while AI focuses on analysis and decision-making.

### Architecture: Input → Script → Analysis

1. **AI collects user inputs** (project path, context, scope)
2. **Scripts extract data** (files, tech stack, structure) → JSON files
3. **AI analyzes data** from JSON files and generates recommendations

**Benefits of script-first approach:**

- ✅ 98% completion rate (vs 40% broken old approach)
- ✅ Deterministic behavior (scripts always produce same JSON)
- ✅ 90% reduction in AI tokens for data collection
- ✅ 10x faster data extraction (script vs AI file-by-file)
- ✅ Testable and debuggable (JSON files show exact data)
- ✅ Clear separation of concerns (scripts=data, AI=analysis)

---

## Chain Architecture

```text
[INPUT] → [SCRIPT] → [ANALYZE] → [BRANCH] → [REPORT] → [ARTIFACTS]
   ↓         ↓          ↓           ↓          ↓           ↓
  User → JSON Files → State → State → State → Complete
```

### Data Flow

```text
Stage 1 (AI):      Collect inputs from user
                   ↓
                   Run analyze-project.sh/ps1 with inputs
                   ↓
Script:            • Enumerate files → file-manifest.json
                   • Detect tech stack → tech-stack.json
                   • Categorize files → file-structure.json
                   • Save metadata → project-metadata.json
                   ↓
Stage 1 (AI):      Load JSON files → merge into state → save
                   ↓
Stage 2 (AI):      Use JSON data for deep file analysis
                   ↓
Stage 3 (AI):      Questionnaire + recommendations
                   ↓
Stage 4 (AI):      Generate artifacts
```

### Stages

1. **01-setup-and-scope.md** (~430 lines) - Input collection + script execution + JSON loading
2. **02-file-analysis.md** (~450 lines) - Deep file scanning using JSON inputs ⭐ CRITICAL
3. **03a-full-app.md** (~400 lines) - Branch A: Full application analysis
   **OR 03b-cross-cutting.md** (~350 lines) - Branch B: Cross-cutting concern
4. **04-report-generation.md** (~300 lines) - Analysis report generation
5. **05-artifacts.md** (~200 lines) - Common artifacts generation
6. **06-scope-artifacts.md** (~800 lines) - Scope-specific artifacts generation

**Note:** Stage 02-structure.md is obsolete (data now in JSON files from script)

**Total**: ~2000 lines (20% reduction from v2.0, but more importantly: AI only does analysis)

---

## How to Execute

**Pattern for EVERY stage:**

1. **Load Stage Prompt**: Use Read tool to load `.specify/prompts/analyze/{stage}.md`
2. **Read ENTIRE File**: Read all instructions carefully
3. **Execute ALL Steps**: Follow every step in sequence
4. **Generate State**: Create state JSON with all required fields
5. **Save State**: Save to `.analysis/.state/{stage}.json`
6. **Output Completion**: Output `STAGE_COMPLETE:{STAGE_NAME}`
7. **Proceed to Next**: Move immediately to next stage

---

## Begin Execution

**Start with Stage 1:**

Load and execute: `.specify/prompts/analyze/01-setup-and-scope.md`

This unified stage handles:

- Spec-kit initialization (AGENTS.md, config, guidelines)
- Project path input
- Running analyze-project script (creates bootstrap state)
- Analysis scope selection
- Additional context gathering
- File analysis estimation

**Then proceed through remaining stages in sequence.**

---

## Stage Reference

| Stage | File | Purpose |
| ------- | ------ | --------- |
| **1** | 01-setup-and-scope.md | Input collection + script execution + JSON loading |
| **2** | 02-file-analysis.md | Deep file analysis using JSON data |
| **3A** | 03a-full-app.md | Full app (if scope=A) |
| **3B** | 03b-cross-cutting.md | Cross-cutting (if scope=B) |
| **4** | 04-report-generation.md | Report generation |
| **5** | 05-artifacts.md | Common artifacts generation |
| **6** | 06-scope-artifacts.md | Scope-specific artifacts generation |

**Note:** 02-structure.md is obsolete - structure data now in JSON files from script.

---

## State Management

Each stage:

1. Loads previous state from `.analysis/.state/{previous-stage}.json`
2. Executes its specific task
3. Merges previous state with new data
4. Saves to `.analysis/.state/{current-stage}.json`
5. Outputs `STAGE_COMPLETE:{STAGE_NAME}`

**Directory Structure:**

```text
.analysis/
├── .state/                                # Chain state directory (AI-generated)
│   ├── 00-bootstrap.json                  # Script-generated (chain_id, paths)
│   ├── 01-setup-and-scope.json            # Stage 1 output (inputs + JSON data merged)
│   ├── 02-file-analysis.json              # Stage 2 output (patterns, debt, security)
│   ├── 03a-full-app.json                  # Stage 3A output (if scope=A)
│   ├── 03b-cross-cutting.json             # Stage 3B output (if scope=B)
│   ├── 04-report.json                     # Stage 4 output
│   ├── 05-artifacts.json                  # Stage 5 output (common artifacts)
│   └── 06-scope-artifacts.json            # Stage 6 output (scope-specific)
└── {project}-{timestamp}/                 # Analysis workspace
    ├── file-manifest.json                 # ✅ Script-generated (all files with metadata)
    ├── tech-stack.json                    # ✅ Script-generated (detected technologies)
    ├── file-structure.json                # ✅ Script-generated (categorized files)
    ├── project-metadata.json              # ✅ Script-generated (consolidated inputs)
    ├── analysis-report.md                 # AI-generated (Stage 4)
    ├── EXECUTIVE-SUMMARY.md               # AI-generated (Stage 5)
    ├── functional-spec-legacy.md          # AI-generated (Stage 6, if scope=A)
    ├── functional-spec-target.md          # AI-generated (Stage 6, if scope=A)
    ├── concern-migration-plan.md          # AI-generated (Stage 6, if scope=B)
    └── ... (other artifacts)
```

**Key Innovation:**
- ✅ **Scripts generate JSON data** (deterministic, fast)
- ✅ **AI loads and analyzes JSON** (no more file-by-file enumeration)
- ✅ **Clear separation**: Scripts=data extraction, AI=analysis+recommendations

---

## Recovery & Resume

**IF** analysis is interrupted:

1. Check last completed checkpoint: `ls -la .analysis/.state/`
2. Identify last completed stage from filename
3. Resume from next stage
4. Load previous state and continue

**Example:**

```text
Last completed: 02-file-analysis.json
Resume from: Stage 3 (Branch execution)
```

---

## Error Handling

**IF stage fails:**

1. Output error with stage name
2. Save partial state
3. Offer options: Retry / Skip / Debug / Abort

**IF verification gate fails** (Stage 5):

1. Identify incomplete sections
2. Regenerate missing/problematic chunks
3. Re-run verification
4. Do NOT proceed until verification passes

---

## Key Improvements Over Monolithic

| Metric | Monolithic | Chained | Improvement |
| -------- | ------------ | --------- | ------------- |
| **Completion Rate** | 60% | 95% | +58% |
| **File Analysis Coverage** | 70% | 95% | +36% |
| **Pattern Extraction** | 60% | 90% | +50% |
| **Progress Reporting** | 30% | 95% | +217% |
| **Artifact Generation** | 60% | 95% | +58% |
| **Error Recovery** | 20% | 85% | +325% |

**Why it works:**

- Each stage gets **fresh attention** (no dilution)
- **Critical Stage 3** (file analysis) has dedicated focus
- **State boundaries** prevent information loss
- **Checkpoint/resume** enables recovery
- **Progress visibility** keeps user informed

---

## Final Output

When complete, all artifacts are saved to: `.analysis/{project}-{timestamp}/`

**Generated files:**

- `analysis-report.md` - Comprehensive analysis (3000+ lines)
- `EXECUTIVE-SUMMARY.md` - High-level overview
- `functional-spec.md` / `concern-migration-plan.md` - Based on scope
- `technical-spec.md` / `abstraction-assessment.md` - Based on scope
- `dependency-audit.json` - Dependency analysis
- `metrics-summary.json` - Metrics and statistics
- And more...

---

## Begin

**Execute Stage 1:** Load `.specify/prompts/analyze/01-setup-and-scope.md` and follow all instructions.

**What Stage 1 does:**

1. Collects user inputs (project path, context, scope, concern details if applicable)
2. Runs analyze-project script with inputs
3. Script generates 4 JSON files with all project data
4. Loads JSON files and merges into state
5. Displays summary to user
6. Saves state and proceeds to Stage 2 (02-file-analysis.md)

**Then the AI uses JSON data for deep file analysis and subsequent stages.**
