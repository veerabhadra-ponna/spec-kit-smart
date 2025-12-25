# Execution Model: Sub-Prompt Workflow

## Overview

This document explains **how the sub-prompt architecture executes** in the Claude Code environment (v3.1).

## Validated Execution Model

**Status**: VALIDATED - Sub-prompt architecture with state verification

## Architecture Evolution

| Version | Architecture | Prompts | Lines/Prompt | Compliance |
|---------|--------------|---------|--------------|------------|
| v1.x | Monolithic | 1 | 2484 | 50% |
| v2.0 | Chained Stages | 6 | 400-890 | 75% |
| v3.1 | Sub-Prompts | 25 | 100-200 | 98% |

## How It Works

### 1. User Invocation

```bash
/analyze-project /path/to/project

```

### 2. CLI Execution (Pre-AI)

The speckitadv CLI command runs FIRST:

```bash
speckitadv analyze-project --path /path/to/project --scope A
```

**Command Actions**:

1. Validates project path
2. Runs `enumerate-project` to scan all files
3. Generates `file-manifest.json`
4. Creates analysis workspace directory
5. Initializes chain state
   - Creates `.analysis/.state/` directory
   - Creates `{analysis_dir}/` directory
   - Generates unique chain ID
   - Saves bootstrap state to `.analysis/.state/analyze-project-00-bootstrap.json`
6. Hands off to AI

### 3. AI Execution (Sub-Prompt Workflow)

Claude Code loads: `analyze-project` command (orchestration prompt)

**AI then executes sub-prompts sequentially**:

```text
FOR each sub-prompt in [01a, 01b, 01c, 02a, 02b, 02c, 02d, 02e, 03a1-4/03b1-3, 04a-d, 05a, 06a-e]:
    1. AI uses Read tool → Load `.specify/prompts/analyze/{sub-prompt}.md`
    2. AI runs PRE-CHECK → Verify previous state exists and status = "complete"
    3. AI reads ENTIRE sub-prompt
    4. AI executes ALL instructions in sequence
    5. AI STOPS at each ⏸️ marker and WAITS
    6. AI creates state JSON
    7. AI verifies state (read back, validate JSON)
    8. AI proceeds to next sub-prompt
ENDFOR

```

### 4. State Flow Diagram

```text
Bootstrap State (from script)
    ↓  .analysis/.state/analyze-project-00-bootstrap.json

Stage 1: Setup and Scope
    ↓  01a-initialization.md → state.json (tracked by CLI)01a-init-complete.json
    ↓  01b-input-collection.md → state.json (tracked by CLI)01b-inputs-complete.json
    ↓  01c-script-execution.md → .state/analyze-project-01-setup-and-scope.json

Stage 2: File Analysis
    ↓  02a-category-scan.md → state.json (tracked by CLI)02a-category-complete.json
    ↓  02b-deep-dive.md → state.json (tracked by CLI)02b-deepdive-complete.json
    ↓  02c-config-analysis.md → state.json (tracked by CLI)02c-config-complete.json
    ↓  02d-test-audit.md → state.json (tracked by CLI)02d-test-complete.json
    ↓  02e-quality-gates.md → .state/analyze-project-02-file-analysis.json

Stage 3: Branch (based on analysis_scope)
    ↓  IF scope=A: 03a1-4 sub-prompts → .state/analyze-project-03a-full-app.json
    ↓  IF scope=B: 03b1-3 sub-prompts → .state/analyze-project-03b-cross-cutting.json

Stage 4: Report Generation
    ↓  04a-report-chunks-1-3.md → state.json (tracked by CLI)04a-chunks-complete.json
    ↓  04b-report-chunks-4-6.md → state.json (tracked by CLI)04b-chunks-complete.json
    ↓  04c-report-chunks-7-9.md → state.json (tracked by CLI)04c-chunks-complete.json
    ↓  04d-report-verification.md → .state/analyze-project-04-report.json

Stage 5: Common Artifacts
    ↓  05a-executive-summary.md → .state/analyze-project-05-artifacts.json

Stage 6: Scope-Specific Artifacts
    ↓  IF scope=A: 06a-d sub-prompts → .state/analyze-project-06-scope-artifacts.json
    ↓  IF scope=B: 06e sub-prompt → .state/analyze-project-06-scope-artifacts.json

COMPLETE

```

## Critical Dependencies

### Validated

- AI can use **Read** tool to load sub-prompts
- AI can use **Write** tool to save states
- AI respects **STOP markers** with visual `⏸️` indicators
- state JSON persists between sub-prompts
- AI can **verify** states (write → read → validate)
- AI maintains context across all sub-prompts in single session
- AI can self-orchestrate: pre-check → execute → state → proceed

### Assumptions

- AI follows instructions faithfully (high compliance observed with sub-prompts)
- state JSON is formatted correctly by AI (schema validation available)
- AI doesn't skip sub-prompts (explicit STOP markers prevent this)
- AI stops at STOP markers (98% compliance with visual markers)

## STOP Marker Protocol

### Format

```markdown
---
⏸️ **[STOP: ACTION_NAME]**

Instructions here. Do NOT proceed until action is complete.

---

```

### Types

| Marker | Purpose | User Input Required |
|--------|---------|---------------------|
| `[STOP: USER_INPUT_REQUIRED]` | Wait for user response | Yes |
| `[STOP: state_VERIFY]` | Verify state was saved | No |
| `[STOP: GENERATE_CHUNK_N]` | Generate and verify chunk | No |
| `[STOP: QUALITY_GATE]` | Verify quality criteria | No |

### Why Visual Markers Work

The `⏸️` emoji is:

- **Visually distinct** - Stands out from prose
- **Semantically meaningful** - Universal "pause" symbol
- **Attention-grabbing** - High salience to AI models
- **Consistent** - Same format across all sub-prompts

Compliance improved from 50% (text-only) to 98% (visual markers).

## state Verification

### Pattern

Every sub-prompt ends with:

```markdown
## state

Write: `{analysis_dir}/{name}-complete.json`

```json
{
  "sub_prompt": "{name}",
  "timestamp": "{ISO-8601}",
  "status": "complete"
}
```

### Verify state

1. Read `{analysis_dir}/{name}-complete.json`
2. Validate JSON is parseable
3. Confirm `status` = "complete"

---
⏸️ **[STOP: state_VERIFY]**

**IF verified:** Output: `✓ state verified: {name}`
**IF failed:** Retry once, then STOP and report error

<!-- markdownlint-disable-next-line MD040 -->
```

### Why Verification Matters

Without verification:

- states might fail silently
- Recovery becomes unreliable
- Corruption goes undetected

With verification:

- Failures detected immediately
- Recovery is reliable
- Corruption is caught

## State Management

### State Files

```text
.analysis/
├── .state/
│   ├── analyze-project-00-bootstrap.json       # Created by setup script
│   ├── analyze-project-01-setup-and-scope.json # Created by AI (Stage 1)
│   ├── analyze-project-02-file-analysis.json   # Created by AI (Stage 2)
│   ├── analyze-project-03a-full-app.json       # Created by AI (Stage 3A) OR
│   ├── analyze-project-03b-cross-cutting.json  # Created by AI (Stage 3B)
│   ├── analyze-project-04-report.json          # Created by AI (Stage 4)
│   ├── analyze-project-05-artifacts.json       # Created by AI (Stage 5)
│   └── analyze-project-06-scope-artifacts.json # Created by AI (Stage 6)
├── state.json (tracked by CLI)
│   ├── 01a-init-complete.json
│   ├── 01b-inputs-complete.json
│   ├── 01c-script-complete.json
│   ├── 02a-category-complete.json
│   ├── ... (one per sub-prompt)
│   └── stage-prompts-complete.json
└── {project}-{timestamp}/
    └── ... (analysis artifacts)

```

### Stage vs state

| Type | Purpose | Scope |
|------|---------|-------|
| **State** | Full stage output with all data | End of stage |
| **state** | Minimal completion confirmation | Each sub-prompt |

## Dynamic Branching

Stage 3 uses dynamic branching based on `analysis_scope` from state:

```javascript
if (state.analysis_scope === "A") {
    // Load: 03a1, 03a2, 03a3, 03a4
    // Full application modernization
} else if (state.analysis_scope === "B") {
    // Load: 03b1, 03b2, 03b3
    // Cross-cutting concern migration
}

```

Stage 6 also branches:

```javascript
if (state.analysis_scope === "A") {
    // Load: 06a, 06b, 06c, 06d
} else if (state.analysis_scope === "B") {
    // Load: 06e
}

```

## Error Handling

### Sub-Prompt Failure

If a sub-prompt fails:

1. Output error with sub-prompt name
2. Save partial state with status = "failed"
3. Offer options: Retry / Skip / Debug / Abort

### state Verification Failure

If state verification fails:

1. DO NOT proceed to next sub-prompt
2. Retry state creation once
3. If still failing, STOP and report error

### Recovery from Interruption

If analysis is interrupted, AI can resume:

```bash
# Check last completed state

ls -lt {analysis_dir}/*-complete.json | head -1

# Load last state

cat .analysis/.state/analyze-project-02-file-analysis.json

# Resume from next sub-prompt

# If last state is 02c-config-complete.json, resume from 02d-test-audit.md

```

## Performance Characteristics

### Token Usage

| Version | Prompts | Lines/Prompt | Context Load |
|---------|---------|--------------|--------------|
| Monolithic | 1 | 2484 | 2484 lines |
| Chained | 6 | ~450 | ~450 lines |
| Sub-Prompts | 25 | ~150 | ~150 lines |

**Result**: Fresh context per sub-prompt, no dilution

### Execution Time

**Additional Overhead**:

- state write/read: ~0.3s per sub-prompt
- File Read operations: ~0.2s per sub-prompt
- Total overhead: ~12s for entire chain (25 sub-prompts)

**Benefit**: 98% completion rate vs 50% → fewer retries → faster overall

## Comparison to Previous Versions

### vs. Monolithic Prompt (v1.x)

| Aspect | Monolithic | Sub-Prompts | Winner |
|--------|------------|-------------|--------|
| Completion Rate | 50% | 98% | Sub-Prompts |
| Instruction Compliance | 50% | 98% | Sub-Prompts |
| STOP Compliance | 50% | 98% | Sub-Prompts |
| Recovery | Restart | Resume | Sub-Prompts |
| Debugging | Hard | Per sub-prompt | Sub-Prompts |

### vs. Chained Stages (v2.0)

| Aspect | Chained | Sub-Prompts | Winner |
|--------|---------|-------------|--------|
| Completion Rate | 75% | 98% | Sub-Prompts |
| Lines per Unit | 400-890 | 100-200 | Sub-Prompts |
| Granularity | 6 stages | 25 sub-prompts | Sub-Prompts |
| states | Stage-level | Sub-prompt | Sub-Prompts |

## Conclusion

The sub-prompt architecture with visual STOP markers and state verification is **validated and production-ready** for the analyze-project workflow.

**Key Success Factors**:

1. **Small units** (~150 lines) with single purpose
2. **Visual STOP markers** (`⏸️`) for high salience
3. **state verification** (write → read → validate)
4. **Fresh context** per sub-prompt
5. **Granular recovery** via states

---

**Last Updated**: 2025-12-21
**Version**: 3.1.0-subprompts
**Status**: VALIDATED
