---
stage: stage_prompts
requires: technical-spec-target complete
condition: state.analysis_scope == "A"
outputs: stage_prompts_complete
version: 3.1.0
next: (final)
---

# Stage 6D: Stage Prompts Generation

## Purpose

Generate staged implementation prompts for Spec Kit workflow integration. These prompts enable the user to use the analysis results with Spec Kit's constitution, clarify, tasks, and implement commands.

---

## Pre-Check

1. Read `{analysis_dir}/state.json`
2. Confirm `status` = "complete"
3. Load analysis data from state files

**IF not complete:** STOP - Return to 06c2-technical-spec-target.md

---

## Templates

{{include:stage-prompt-templates/constitution-prompt-template.md}}

{{include:stage-prompt-templates/clarify-prompt-template.md}}

{{include:stage-prompt-templates/tasks-prompt-template.md}}

{{include:stage-prompt-templates/implement-prompt-template.md}}

---

## Create Output Directory

Create: `{analysis_dir}/stage-prompts/`

---

## Prompt 1: Constitution Prompt

---
⏸️ **[STOP: GENERATE_CONSTITUTION_PROMPT]**

**Purpose:** Extract project principles from legacy code for `/speckitadv.constitution` command

**Template:** Use constitution-prompt template above

**Content to extract:**

```markdown
# Project Constitution: {Project Name}

## Core Values

{Extract from legacy code patterns and documentation}

## Coding Standards

- Naming conventions observed in legacy
- Code organization patterns
- Documentation style

## Architecture Decisions

| Decision | Context | Rationale |
|----------|---------|-----------|
| {ADR from legacy} | {why} | {justification} |

## Quality Standards

- Test coverage expectations
- Performance benchmarks
- Security requirements

## Legacy Preservation

{Critical behaviors that MUST be preserved exactly}
- {behavior 1} (Source: {file}:{line})
- {behavior 2} (Source: {file}:{line})

```

Write to: `{analysis_dir}/stage-prompts/constitution-prompt.md`

**Output:** `✓ Generated: constitution-prompt.md`

---

## Prompt 2: Clarify Prompt

---
⏸️ **[STOP: GENERATE_CLARIFY_PROMPT]**

**Purpose:** Use legacy code as source of truth for clarifications with `/speckitadv.clarify` command

**Template:** Use clarify-prompt template above

**Content to extract:**

```markdown
# Clarification Guide: {Project Name}

## Legacy Code References

When clarifying ambiguous requirements, reference these legacy implementations:

### Authentication & Authorization

- Source: {auth files with line numbers}
- Key behaviors: {list}

### Business Logic

- Source: {business logic files with line numbers}
- Critical rules: {list}

### Data Validation

- Source: {validation files with line numbers}
- Validation patterns: {list}

## Ambiguity Resolution Patterns

| Ambiguous Spec | Legacy Behavior | Resolution |
|----------------|-----------------|------------|
| "{ambiguous text}" | {what legacy does} | {clarification} |

## Edge Cases Discovered

- {edge case 1}: Handled by {file}:{line}
- {edge case 2}: Handled by {file}:{line}

## Questions for Stakeholders

{List of unresolved ambiguities requiring business decision}

```

Write to: `{analysis_dir}/stage-prompts/clarify-prompt.md`

**Output:** `✓ Generated: clarify-prompt.md`

---

## Prompt 3: Tasks Prompt

---
⏸️ **[STOP: GENERATE_TASKS_PROMPT]**

**Purpose:** Break down implementation with legacy complexity awareness for `/speckitadv.tasks` command

**Template:** Use tasks-prompt template above

**Content to extract:**

```markdown
# Task Breakdown: {Project Name}

## Migration Phases

### Phase 1: Foundation (50% value)

| Task | Legacy Source | Complexity | Effort |
|------|--------------|------------|--------|
| {task} | {file}:{line} | {H/M/L} | {days} |

### Phase 2: Core Migration (30% value)

| Task | Legacy Source | Complexity | Effort |
|------|--------------|------------|--------|
| {task} | {file}:{line} | {H/M/L} | {days} |

### Phase 3: Complete Migration (15% value)

| Task | Legacy Source | Complexity | Effort |
|------|--------------|------------|--------|
| {task} | {file}:{line} | {H/M/L} | {days} |

### Phase 4: Optimization (5% value)

| Task | Legacy Source | Complexity | Effort |
|------|--------------|------------|--------|
| {task} | {file}:{line} | {H/M/L} | {days} |

## Complexity Hotspots

{Files/components with highest complexity scores}
- {file}: Complexity {score}, Effort: {estimate}

## Dependencies

{Task dependencies and ordering constraints}

## Risk Mitigation Tasks

{Additional tasks to reduce migration risk}

```

Write to: `{analysis_dir}/stage-prompts/tasks-prompt.md`

**Output:** `✓ Generated: tasks-prompt.md`

---

## Prompt 4: Implement Prompt

---
⏸️ **[STOP: GENERATE_IMPLEMENT_PROMPT]**

**Purpose:** Reference legacy code during implementation for `/speckitadv.implement` command

**Template:** Use implement-prompt template above

**Content to extract:**

```markdown
# Implementation Guide: {Project Name}

## Must-Preserve Behaviors

### CRITICAL - Exact Preservation Required

These behaviors must be implemented EXACTLY as in legacy:

| Behavior | Legacy Source | Why Critical |
|----------|--------------|--------------|
| {behavior} | {file}:{line} | {reason} |

### Code Patterns to Follow

{Legacy patterns that should be replicated}

```text
// Legacy Pattern: {name}
// Source: {file}:{line}
{code snippet}
```

## Edge Cases Catalog

| Scenario | Legacy Handling | Test Case |
|----------|-----------------|-----------|
| {edge case} | {behavior} | {test ref} |

## API Contract Preservation

{Endpoints/interfaces that must maintain backwards compatibility}

## Data Migration Notes

{Critical data handling from legacy that affects implementation}

## Testing Checkpoints

| Checkpoint | Validation | Legacy Reference |
|------------|------------|------------------|
| {checkpoint} | {how to verify} | {file}:{line} |

<!-- markdownlint-disable-next-line MD040 -->
```

Write to: `{analysis_dir}/stage-prompts/implement-prompt.md`

**Output:** `✓ Generated: implement-prompt.md`

---

## Generate Stage 6 State (Scope A)

```json
{
  "schema_version": "3.1.0",
  "chain_id": "{chain_id}",
  "stage": "scope_artifact_generation",
  "timestamp": "{ISO-8601}",
  "stages_complete": [..., "scope_artifact_generation"],
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

The CLI automatically updates `{analysis_dir}/state.json` when stages complete.

---

## Completion Marker

```text
═══════════════════════════════════════════════════════════
  STAGE COMPLETE: SCOPE_ARTIFACTS (Full Application)

  Chain ID: {chain_id}

  Artifacts Generated (7 total):
    ✓ functional-spec-legacy.md
    ✓ functional-spec-target.md
    ✓ technical-spec.md
    ✓ stage-prompts/constitution-prompt.md
    ✓ stage-prompts/clarify-prompt.md
    ✓ stage-prompts/tasks-prompt.md
    ✓ stage-prompts/implement-prompt.md
═══════════════════════════════════════════════════════════

STAGE_COMPLETE:SCOPE_ARTIFACTS

```

---

## Analysis Chain Complete

```text
═══════════════════════════════════════════════════════════
           ANALYSIS CHAIN COMPLETE
═══════════════════════════════════════════════════════════

Chain ID: {chain_id}

All Stages Completed:
  ✓ Stage 1: Setup and Scope
  ✓ Stage 2: File Analysis
  ✓ Stage 3A: Full Application Analysis
  ✓ Stage 4: Report Generation
  ✓ Stage 5: Common Artifacts
  ✓ Stage 6: Scope-Specific Artifacts

Analysis Directory: {analysis_dir}

Generated Artifacts:
  Common:
    • EXECUTIVE-SUMMARY.md
    • dependency-audit.json
    • metrics-summary.json
    • analysis-report.md

  Scope-Specific:
    • functional-spec-legacy.md
    • functional-spec-target.md
    • technical-spec.md
    • stage-prompts/ (4 files)

Next Steps:
  1. Review generated artifacts in {analysis_dir}
  2. Use stage-prompts/ with Spec Kit commands
  3. Begin implementation using /speckitadv.implement

═══════════════════════════════════════════════════════════

```
