---
description: Reverse engineer and analyze an existing project using chained prompts with script-based data extraction
status: STABLE
version: 3.1.0
---

## MANDATORY: Read Agent Instructions First

**BEFORE PROCEEDING:**

1. Check if `AGENTS.md` exists in repository root, `.specify/memory/`, or `templates/` directory
2. **IF EXISTS:** Read it in FULL - instructions are NON-NEGOTIABLE
3. Follow all AGENTS.md guidelines for the duration of this command execution

**Verification:** After reading AGENTS.md (if it exists), acknowledge with:
   "✓ Read AGENTS.md v[X.X] - Following all guidelines"

**If AGENTS.md does not exist:** Proceed with default behavior.

---

# Analyze Project - Chain Orchestrator v3.1

## Overview

This command orchestrates a **script-first chained workflow** for project analysis. Data extraction is handled by shell scripts (deterministic, fast, testable), while AI focuses on analysis and decision-making.

### Architecture: Input → Script → Analysis

1. **AI collects user inputs** (project path, context, scope)
2. **Scripts extract data** (files, tech stack, structure) → JSON files
3. **AI analyzes data** from JSON files and generates recommendations

---

## Chain Architecture

```text
[INPUT] → [SCRIPT] → [ANALYZE] → [BRANCH] → [REPORT] → [ARTIFACTS]
   ↓         ↓          ↓           ↓          ↓           ↓
  User → JSON Files → State → State → State → Complete
```

---

## Stage Sub-Prompt Reference

Each stage is split into focused sub-prompts (~100-200 lines each) for better AI comprehension and execution.

### Stage 1: Setup and Scope
| Sub-Prompt | Purpose |
|------------|---------|
| **01a-initialization.md** | AGENTS.md check, toolkit verification, project path input |
| **01b-input-collection.md** | Scope selection, concern details (if B), additional context |
| **01c-script-execution.md** | Script execution, JSON loading, state creation |

### Stage 2: File Analysis
| Sub-Prompt | Purpose |
|------------|---------|
| **02a-category-scan.md** | Phase 1 (25%): Quick category scan by priority |
| **02b-deep-dive.md** | Phase 2 (40%): Deep analysis of critical/high priority |
| **02c-config-analysis.md** | Phase 3 (15%): Configuration file analysis |
| **02d-test-audit.md** | Phase 4 (20%): Test coverage + dependency audit |
| **02e-quality-gates.md** | Quality gate verification before proceeding |

### Stage 3A: Full Application (Scope = A)
| Sub-Prompt | Purpose |
|------------|---------|
| **03a1-questions-part1.md** | Questions 1-5: Language, Database, Message Bus, Packages, Deployment |
| **03a2-questions-part2.md** | Questions 6-10: IaC, Containers, Observability, Security, Testing |
| **03a3-validation-scoring.md** | Scope validation, complexity & feasibility scoring |
| **03a4-recommendations.md** | Recommendations, phased plan, state output |

### Stage 3B: Cross-Cutting Concern (Scope = B)
| Sub-Prompt | Purpose |
|------------|---------|
| **03b1-abstraction-assessment.md** | Abstraction level + blast radius analysis |
| **03b2-migration-strategy.md** | Strategy selection + risk assessment |
| **03b3-effort-success.md** | Effort estimation + success criteria |

### Stage 4: Report Generation
| Sub-Prompt | Purpose |
|------------|---------|
| **04a-report-chunks-1-3.md** | Chunks 1-3: Header, TOC, Tech Stack, File Analysis |
| **04b-report-chunks-4-6.md** | Chunks 4-6: Quality, Dependencies, Security |
| **04c-report-chunks-7-9.md** | Chunks 7-9: Recommendations, Appendix, Conclusions |
| **04d-report-verification.md** | Report verification + state output |

### Stage 5: Common Artifacts
| Sub-Prompt | Purpose |
|------------|---------|
| **05a-executive-summary.md** | EXECUTIVE-SUMMARY.md, dependency-audit.json, metrics-summary.json |

### Stage 6: Scope-Specific Artifacts
| Sub-Prompt | Condition | Purpose |
|------------|-----------|---------|
| **06a-functional-spec-legacy.md** | Scope = A | Legacy system functional spec (5 chunks) |
| **06b-functional-spec-target.md** | Scope = A | Target system functional spec (5 chunks) |
| **06c-technical-spec.md** | Scope = A | Technical specification (5 chunks) |
| **06d-stage-prompts.md** | Scope = A | Spec Kit stage prompts (4 files) |
| **06e-cross-cutting-artifacts.md** | Scope = B | Abstraction assessment + migration plan + rollback |

---

## Execution Pattern

**For EVERY sub-prompt:**

```text
1. LOAD    → Read .specify/prompts/analyze/{sub-prompt}.md
2. PRE-CHECK → Verify previous checkpoint exists and status = "complete"
3. EXECUTE → Follow ALL steps in sequence
4. STOP    → WAIT at each ⏸️ [STOP] marker
5. VERIFY  → Confirm output before proceeding
6. SAVE    → Create checkpoint file
7. PROCEED → Move to next sub-prompt
```

### STOP Marker Protocol

When you encounter:
```
---
⏸️ **[STOP: ACTION_NAME]**
---
```

**YOU MUST:**
1. Complete the action described
2. Wait for user input if required
3. Verify output before proceeding
4. DO NOT skip or rush past STOP markers

---

## Inter-Stage Validation

**Before loading any sub-prompt, verify:**

```
1. Previous checkpoint exists
2. Previous checkpoint status = "complete"
3. Required state data is available
```

**IF validation fails:** STOP and return to previous incomplete sub-prompt.

### Checkpoint Verification Pattern

```bash
# Check checkpoint exists
cat .analysis/.checkpoints/{stage}-complete.json

# Verify status
jq '.status' .analysis/.checkpoints/{stage}-complete.json
# Expected: "complete"
```

---

## Begin Execution

**Start with Stage 1, Sub-prompt 1A:**

Load and execute: `.specify/prompts/analyze/01a-initialization.md`

### Execution Flow

```text
01a-initialization.md
        ↓
01b-input-collection.md
        ↓
01c-script-execution.md
        ↓
02a-category-scan.md
        ↓
02b-deep-dive.md
        ↓
02c-config-analysis.md
        ↓
02d-test-audit.md
        ↓
02e-quality-gates.md
        ↓
   ┌────┴────┐
   ↓         ↓
Scope A   Scope B
   ↓         ↓
03a1...   03b1...
03a2...   03b2...
03a3...   03b3...
03a4...      ↓
   ↓         │
   └────┬────┘
        ↓
04a-report-chunks-1-3.md
        ↓
04b-report-chunks-4-6.md
        ↓
04c-report-chunks-7-9.md
        ↓
04d-report-verification.md
        ↓
05a-executive-summary.md
        ↓
   ┌────┴────┐
   ↓         ↓
Scope A   Scope B
   ↓         ↓
06a...    06e...
06b...
06c...
06d...
   ↓         ↓
   └────┬────┘
        ↓
    COMPLETE
```

---

## State Management

### Directory Structure

```text
.analysis/
├── .state/                                # Chain state directory
│   ├── 00-bootstrap.json                  # Script-generated
│   ├── 01-setup-and-scope.json            # Stage 1 output
│   ├── 02-file-analysis.json              # Stage 2 output
│   ├── 03a-full-app.json                  # Stage 3A (if scope=A)
│   ├── 03b-cross-cutting.json             # Stage 3B (if scope=B)
│   ├── 04-report.json                     # Stage 4 output
│   ├── 05-artifacts.json                  # Stage 5 output
│   └── 06-scope-artifacts.json            # Stage 6 output
├── .checkpoints/                          # Sub-prompt checkpoints
│   ├── 01a-init-complete.json
│   ├── 01b-inputs-complete.json
│   ├── 01c-script-complete.json
│   ├── 02a-category-complete.json
│   ├── ... (one per sub-prompt)
│   └── stage-prompts-complete.json
└── {project}-{timestamp}/                 # Analysis workspace
    ├── file-manifest.json                 # Script-generated
    ├── tech-stack.json                    # Script-generated
    ├── file-structure.json                # Script-generated
    ├── project-metadata.json              # Script-generated
    ├── analysis-report.md                 # AI-generated
    ├── EXECUTIVE-SUMMARY.md               # AI-generated
    ├── functional-spec-legacy.md          # AI-generated (scope=A)
    ├── functional-spec-target.md          # AI-generated (scope=A)
    ├── technical-spec.md                  # AI-generated (scope=A)
    ├── stage-prompts/                     # AI-generated (scope=A)
    ├── abstraction-assessment.md          # AI-generated (scope=B)
    ├── concern-migration-plan.md          # AI-generated (scope=B)
    └── rollback-procedure.md              # AI-generated (scope=B)
```

---

## Recovery & Resume

**IF analysis is interrupted:**

1. List checkpoints: `ls -la .analysis/.checkpoints/`
2. Find last complete checkpoint
3. Resume from next sub-prompt
4. Load previous state and continue

**Example:**
```text
Last checkpoint: 02c-config-complete.json
Resume from: 02d-test-audit.md
```

---

## Error Handling

**IF sub-prompt fails:**

1. Output error with sub-prompt name
2. Save partial checkpoint with status = "failed"
3. Offer options: Retry / Skip / Debug / Abort

**IF checkpoint verification fails:**

1. DO NOT proceed to next sub-prompt
2. Retry checkpoint creation once
3. If still failing, STOP and report error

---

## Key Metrics

| Metric | Target |
|--------|--------|
| Sub-prompt completion rate | 98% |
| Checkpoint verification pass | 100% |
| STOP marker compliance | 100% |
| State preservation | 100% |

---

## Final Output

When complete, all artifacts are saved to: `.analysis/{project}-{timestamp}/`

### Scope A Artifacts
- `analysis-report.md` - Comprehensive analysis
- `EXECUTIVE-SUMMARY.md` - High-level overview
- `functional-spec-legacy.md` - Legacy system spec
- `functional-spec-target.md` - Target system spec
- `technical-spec.md` - Implementation design
- `stage-prompts/` - Spec Kit integration prompts
- `dependency-audit.json` - Dependency analysis
- `metrics-summary.json` - Metrics and statistics

### Scope B Artifacts
- `analysis-report.md` - Comprehensive analysis
- `EXECUTIVE-SUMMARY.md` - High-level overview
- `abstraction-assessment.md` - Abstraction analysis
- `concern-migration-plan.md` - Migration strategy
- `rollback-procedure.md` - Rollback instructions
- `dependency-audit.json` - Dependency analysis
- `metrics-summary.json` - Metrics and statistics

---

## Begin

**Execute Stage 1, Sub-prompt 1A:**

Load `.specify/prompts/analyze/01a-initialization.md` and follow all instructions.

**Remember:**
- STOP at every ⏸️ marker
- Verify checkpoints before proceeding
- Save state after every sub-prompt
- Follow inter-stage validation
