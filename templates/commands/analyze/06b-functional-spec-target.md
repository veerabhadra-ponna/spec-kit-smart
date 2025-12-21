---
stage: functional_spec_target
requires: func-legacy-complete checkpoint
condition: state.analysis_scope == "A"
outputs: functional_spec_target_complete
version: 3.1.0
next: 06c-technical-spec.md
---

# Stage 6B: Functional Specification - Target System

## Purpose

Generate functional specification documenting WHAT the MODERNIZED system WILL do. This is the second of two required functional specs for Full Application Modernization.

---

## Pre-Check

1. Read `.analysis/.checkpoints/func-legacy-complete.json`
2. Confirm `status` = "complete"
3. Load user's modernization preferences from `.analysis/.state/03a-full-app.json`

**IF not complete:** STOP - Return to 06a-functional-spec-legacy.md

---

## Source of Truth

**Primary Sources:**
- `.analysis/{dir}/analysis-report.md` (feature catalog)
- `.analysis/.state/03a-full-app.json` (10 modernization preferences)
- User's scope validation answers

**Template:** Read `.specify/templates/analyze/functional-spec-template.md`

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

## Chunk 1: Introduction + Summary + Scope

Generate Sections 1, 2, and 3 for TARGET system.

---
⏸️ **[STOP: GENERATE_CHUNK_1]**

### Section 1: Introduction

- Project name: {name} (Modernized)
- Target system overview
- Modernization goals from user preferences

### Section 2: Executive Summary

- High-level target functionality
- Key improvements over legacy
- New capabilities

### Section 3: Scope

- IN SCOPE: Components with explicit target preferences
- OUT OF SCOPE: Components to keep as-is
- Migration boundaries

Write to: `.analysis/{dir}/functional-spec-target.md`

**Verify:** Read file, confirm scope boundaries match user's answers.

**Output:**

```text
functional-spec-target.md Chunk 1/5 complete: Introduction + Summary + Scope
  - In Scope Components: [COUNT]
  - Out of Scope Components: [COUNT]
  - Lines: [COUNT]

```

---

## Checkpoint: Chunk 1

Write: `.analysis/.checkpoints/func-target-chunk-1.json`

```json
{
  "artifact": "functional-spec-target.md",
  "chunk": 1,
  "sections": ["Introduction", "Summary", "Scope"],
  "in_scope_count": {count},
  "out_of_scope_count": {count},
  "timestamp": "{ISO-8601}",
  "status": "complete"
}

```

---

## Chunk 2: User Stories - CRITICAL Features (Modernized)

Generate Section 4.1 with modernization enhancements.

---
⏸️ **[STOP: GENERATE_CHUNK_2]**

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

Append to: `.analysis/{dir}/functional-spec-target.md`

**Output:**

```text
functional-spec-target.md Chunk 2/5 complete: User Stories (CRITICAL)
  - Features: [COUNT]
  - Enhancements: [COUNT]
  - Lines: [COUNT]

```

---

## Checkpoint: Chunk 2

Write: `.analysis/.checkpoints/func-target-chunk-2.json`

---

## Chunk 3: User Stories - STANDARD + Business Rules (Modernized)

Generate Sections 4.2 and 5 with target stack considerations.

---
⏸️ **[STOP: GENERATE_CHUNK_3]**

### Section 4.2: STANDARD Features (Modernized)

- Same format as CRITICAL
- Include modernization changes where applicable
- Note OUT OF SCOPE items explicitly

### Section 5: Business Rules (Preserved + Enhanced)

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

Append to: `.analysis/{dir}/functional-spec-target.md`

**Output:**

```text
functional-spec-target.md Chunk 3/5 complete: STANDARD Features + Rules
  - Features: [COUNT]
  - Rules Preserved: [COUNT]
  - Rules Enhanced: [COUNT]
  - Lines: [COUNT]

```

---

## Checkpoint: Chunk 3

Write: `.analysis/.checkpoints/func-target-chunk-3.json`

---

## Chunk 4: NFRs + Data Requirements (Target)

Generate Sections 6 and 7 using user's target preferences.

---
⏸️ **[STOP: GENERATE_CHUNK_4]**

### Section 6: Non-Functional Requirements (Target)

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

### Section 7: Data Requirements (Target)

Use user's answer from Q2 (Database):

```markdown
### Entity: {Name} (Migrated)

**Target Database:** {Q2 answer}
**Migration Notes:** {considerations}

| Field | Type | Target Type | Migration |
|-------|------|-------------|-----------|
| {field} | {legacy} | {target} | {notes} |

```

Append to: `.analysis/{dir}/functional-spec-target.md`

**Output:**

```text
functional-spec-target.md Chunk 4/5 complete: NFRs + Data
  - Target Database: {Q2 answer}
  - Target Deployment: {Q5 answer}
  - Lines: [COUNT]

```

---

## Checkpoint: Chunk 4

Write: `.analysis/.checkpoints/func-target-chunk-4.json`

---

## Chunk 5: Acceptance Criteria + Assumptions + Constraints (Target)

Generate Sections 8, 9, and 10.

---
⏸️ **[STOP: GENERATE_CHUNK_5]**

### Section 8: Acceptance Criteria (Target)

- Migration success criteria
- Feature parity verification
- Performance benchmarks vs legacy

### Section 9: Assumptions (Target)

- Target environment assumptions
- Migration path assumptions
- Team capability assumptions

### Section 10: Constraints (Target)

- Timeline constraints
- Budget constraints
- Technology constraints from user preferences

Append to: `.analysis/{dir}/functional-spec-target.md`

**Verify:** Read complete file, confirm:
- All 10 sections present
- Scope boundaries respected
- User preferences correctly applied
- No placeholders or TODOs

**Output:**

```text
functional-spec-target.md Chunk 5/5 complete: Acceptance + Assumptions + Constraints
  - Lines: [COUNT]

functional-spec-target.md COMPLETE (5/5 chunks)
   Total features: [COUNT]
   Total lines: [COUNT]

```

---

## Final Checkpoint

Write: `.analysis/.checkpoints/func-target-complete.json`

```json
{
  "artifact": "functional-spec-target.md",
  "chunks_complete": 5,
  "total_features": {count},
  "in_scope_components": {count},
  "out_of_scope_components": {count},
  "timestamp": "{ISO-8601}",
  "status": "complete"
}

```

---
⏸️ **[STOP: CHECKPOINT_VERIFY]**

1. Read `.analysis/.checkpoints/func-target-complete.json`
2. Validate JSON parseable
3. Confirm `status` = "complete"

**IF verified:** Output: `✓ Checkpoint verified: functional-spec-target`
**IF failed:** Retry once, then STOP

---

## Both Functional Specs Complete

```text
═══════════════════════════════════════════════════════════
  BOTH FUNCTIONAL SPECS COMPLETE

  1. functional-spec-legacy.md - LEGACY system (what exists today)
  2. functional-spec-target.md - TARGET system (what will be built)

  Chain ID: {chain_id}

  Now proceeding to technical-spec.md...
═══════════════════════════════════════════════════════════

ARTIFACT_COMPLETE:FUNCTIONAL_SPEC_TARGET

```

---

## Next Stage

Proceed immediately to: **06c-technical-spec.md**
