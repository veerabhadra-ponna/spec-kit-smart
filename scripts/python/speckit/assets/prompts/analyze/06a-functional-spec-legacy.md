---
stage: functional_spec_legacy
requires: analyze-project-05-artifacts.json
condition: state.analysis_scope == "A"
outputs: functional_spec_legacy_complete
version: 3.1.0
next: 06b-functional-spec-target.md
---

# Stage 6A: Functional Specification - Legacy System

## Purpose

Generate functional specification documenting WHAT the LEGACY/EXISTING system CURRENTLY does. This is the first of two required functional specs for Full Application Modernization.

---

## Pre-Check

1. Read `.analysis/.state/analyze-project-05-artifacts.json`
2. Confirm `common_artifacts_complete` = true
3. Confirm `analysis_scope` = "A"
4. Load `analysis_dir` path

**IF not complete:** STOP - Return to 05a-executive-summary.md

---

## Source of Truth

**Use ONLY these sources:**
- `{analysis_dir}/analysis-report.md` Phase 2 (Feature Catalog)
- `{analysis_dir}/analysis-report.md` Phase 3 (Positive Findings)

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

## Chunk 1: Introduction + Summary + Scope

Generate Sections 1, 2, and 3.

---
⏸️ **[STOP: GENERATE_CHUNK_1]**

Generate the following sections:

### Section 1: Introduction

- Project name and purpose
- Document scope and audience
- Legacy system overview

### Section 2: Executive Summary

- High-level functionality summary
- Key capabilities
- System boundaries

### Section 3: Scope

- In-scope functionality
- Out-of-scope items
- Assumptions

Write to: `{analysis_dir}/functional-spec-legacy.md`

**Verify:** Read file, confirm no placeholders, all sections complete.

**Output:**

```text
functional-spec-legacy.md Chunk 1/5 complete: Introduction + Summary + Scope
  - Lines: [COUNT]

```

---

## Checkpoint: Chunk 1

Write: `.analysis/.checkpoints/func-legacy-chunk-1.json`

```json
{
  "artifact": "functional-spec-legacy.md",
  "chunk": 1,
  "sections": ["Introduction", "Summary", "Scope"],
  "timestamp": "{ISO-8601}",
  "status": "complete"
}

```

---

## Chunk 2: User Stories - CRITICAL Features

Generate Section 4.1 (CRITICAL priority features).

---
⏸️ **[STOP: GENERATE_CHUNK_2]**

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

Append to: `{analysis_dir}/functional-spec-legacy.md`

**Verify:** Read file, confirm all CRITICAL features documented with file:line references.

**Output:**

```text
functional-spec-legacy.md Chunk 2/5 complete: User Stories (CRITICAL)
  - Features: [COUNT]
  - Lines: [COUNT]

```

---

## Checkpoint: Chunk 2

Write: `.analysis/.checkpoints/func-legacy-chunk-2.json`

```json
{
  "artifact": "functional-spec-legacy.md",
  "chunk": 2,
  "sections": ["User Stories - CRITICAL"],
  "feature_count": {count},
  "timestamp": "{ISO-8601}",
  "status": "complete"
}

```

---

## Chunk 3: User Stories - STANDARD + Business Rules

Generate Sections 4.2 and 5.

---
⏸️ **[STOP: GENERATE_CHUNK_3]**

### Section 4.2: STANDARD Features

- Extract all STANDARD priority features
- Same user story format as CRITICAL
- Include file:line references

### Section 5: Business Rules

```markdown
## 5. Business Rules

### BR-001: {Rule Name}

**Category:** {Validation | Calculation | Authorization | Workflow}
**Source:** {file}:{line}
**Description:** {plain English description}
**Pseudocode:**

```text
IF condition THEN
  action
ELSE
  alternative
END IF
```

Append to: `{analysis_dir}/functional-spec-legacy.md`

**Output:**

```text
functional-spec-legacy.md Chunk 3/5 complete: STANDARD Features + Rules
  - Features: [COUNT]
  - Rules: [COUNT]
  - Lines: [COUNT]

```

---

## Checkpoint: Chunk 3

Write: `.analysis/.checkpoints/func-legacy-chunk-3.json`

---

## Chunk 4: NFRs + Data Requirements

Generate Sections 6 and 7.

---
⏸️ **[STOP: GENERATE_CHUNK_4]**

### Section 6: Non-Functional Requirements

| Category | Current State | Evidence |
|----------|--------------|----------|
| Performance | {metrics} | {file:line} |
| Security | {implementation} | {file:line} |
| Scalability | {approach} | {file:line} |
| Reliability | {mechanisms} | {file:line} |

### Section 7: Data Requirements

```markdown
### Entity: {Name}

**Source:** {file}:{line}

| Field | Type | Constraints |
|-------|------|-------------|
| {field} | {type} | {constraints} |

**Relationships:**
- {relationship description}

```

Append to: `{analysis_dir}/functional-spec-legacy.md`

**Output:**

```text
functional-spec-legacy.md Chunk 4/5 complete: NFRs + Data
  - NFR Categories: [COUNT]
  - Entities: [COUNT]
  - Lines: [COUNT]

```

---

## Checkpoint: Chunk 4

Write: `.analysis/.checkpoints/func-legacy-chunk-4.json`

---

## Chunk 5: Acceptance Criteria + Assumptions + Constraints

Generate Sections 8, 9, and 10.

---
⏸️ **[STOP: GENERATE_CHUNK_5]**

### Section 8: Acceptance Criteria

- System-level acceptance tests
- Integration verification points
- Performance benchmarks

### Section 9: Assumptions

- Technical assumptions
- Business assumptions
- Environmental assumptions

### Section 10: Constraints

- Technical constraints
- Business constraints
- Regulatory constraints

Append to: `{analysis_dir}/functional-spec-legacy.md`

**Verify:** Read complete file, confirm:
- All 10 sections present
- No placeholders or TODOs
- All features have file:line references

**Output:**

```text
functional-spec-legacy.md Chunk 5/5 complete: Acceptance + Assumptions + Constraints
  - Lines: [COUNT]

functional-spec-legacy.md COMPLETE (5/5 chunks)
   Total features: [COUNT]
   Total lines: [COUNT]

```

---

## Final Checkpoint

Write: `.analysis/.checkpoints/func-legacy-complete.json`

```json
{
  "artifact": "functional-spec-legacy.md",
  "chunks_complete": 5,
  "total_features": {count},
  "total_lines": {count},
  "timestamp": "{ISO-8601}",
  "status": "complete"
}

```

---
⏸️ **[STOP: CHECKPOINT_VERIFY]**

1. Read `.analysis/.checkpoints/func-legacy-complete.json`
2. Validate JSON parseable
3. Confirm `status` = "complete"

**IF verified:** Output: `✓ Checkpoint verified: functional-spec-legacy`
**IF failed:** Retry once, then STOP

---

## Completion Marker

```text
═══════════════════════════════════════════════════════════
  ARTIFACT COMPLETE: FUNCTIONAL-SPEC-LEGACY.md

  Chain ID: {chain_id}
  Features Documented: {count}
  Lines: {count}

  This documents the LEGACY system (what exists today).

  NEXT: Generate functional-spec-target.md (what will be built)
═══════════════════════════════════════════════════════════

ARTIFACT_COMPLETE:FUNCTIONAL_SPEC_LEGACY

```

---

## Next Stage

Proceed immediately to: **06b-functional-spec-target.md**

**DO NOT:**
- Skip to technical-spec.md
- Skip to stage-prompts/
- Mark Stage 6 complete

**You MUST generate both functional specs before proceeding.**
