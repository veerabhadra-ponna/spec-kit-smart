---
stage: artifact_generation
requires: 06-report.json
outputs: all_artifacts_complete
version: 1.0.0
---

# Stage 7: Remaining Artifacts Generation

## Purpose

Generate all remaining artifacts based on analysis scope. These complement the main analysis-report.md.

---

## Previous State

Load state from: `.analysis/.state/06-report.json`

Required:
- `report_generated` must be `true`
- `verification_passed` must be `true`
- `analysis_scope` determines which artifacts to generate

---

## Artifacts to Generate

### Common Artifacts (Both A and B)

1. **EXECUTIVE-SUMMARY.md** (1 chunk)
2. **dependency-audit.md** (1 chunk)
3. **metrics-summary.md** (1 chunk)
4. **analysis-report.md** (from Stage 6)

### Full Application Artifacts (Scope = A)

1. **functional-spec.md** (2-3 chunks)
2. **technical-spec.md** (2-3 chunks)
3. **stage-prompts/** (4 files)
   - constitution-prompt.md
   - clarify-prompt.md
   - tasks-prompt.md
   - implement-prompt.md

### Cross-Cutting Concern Artifacts (Scope = B)

1. **abstraction-assessment.md** (1 chunk)
2. **concern-migration-plan.md** (2-3 chunks)
3. **rollback-procedure.md** (1 chunk)

---

## Artifact Generation (Parallel-Capable Chunks)

### Artifact 1: EXECUTIVE-SUMMARY.md

**Purpose**: C-level summary for stakeholders

**Content**:

```markdown
# Executive Summary: {Project Name}

## Overview
- Project: {name}
- Analysis Date: {date}
- Analysis Scope: {Full Application | Cross-Cutting Concern}

## Key Findings

### Current State
- Technology Stack: {primary stack}
- Project Size: {LOC}, {files} files
- Test Coverage: {percentage}%
- Technical Debt: {HIGH/MEDIUM/LOW}

### Recommendations
- Primary Approach: {Inline Upgrade | Greenfield Rewrite | Hybrid | Migration}
- Confidence: {percentage}%
- Estimated Timeline: {months}
- Estimated Effort: {person-weeks}

### Business Impact
- Risk Level: {LOW/MEDIUM/HIGH/CRITICAL}
- Downtime Required: {Yes/No - details}
- Training Required: {Yes/No - details}
- Cost Estimate: {range}

### Next Steps
1. {immediate action 1}
2. {immediate action 2}
3. {immediate action 3}
```

**Progress**: `✓ Generated: EXECUTIVE-SUMMARY.md`

---

### Artifact 2: dependency-audit.md

**Purpose**: Machine-readable dependency audit results

**Content**:

```json
{
  "audit_date": "2025-11-14T11:30:00Z",
  "project": "{project_name}",
  "total_dependencies": {total},
  "direct_dependencies": {direct},
  "transitive_dependencies": {transitive},
  "outdated": [
    {
      "name": "{package}",
      "current": "{version}",
      "latest": "{version}",
      "type": "major | minor | patch"
    }
  ],
  "vulnerable": [
    {
      "name": "{package}",
      "version": "{version}",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "cve": "{CVE-YYYY-XXXXX}",
      "description": "{description}",
      "remediation": "{fix version or mitigation}"
    }
  ],
  "deprecated": [
    {
      "name": "{package}",
      "replacement": "{suggested alternative}"
    }
  ],
  "license_issues": []
}
```

**Progress**: `✓ Generated: dependency-audit.md`

---

### Artifact 3: metrics-summary.md

**Purpose**: Key metrics for tracking and reporting

**Content**:

```json
{
  "project": "{project_name}",
  "analysis_date": "2025-11-14T11:30:00Z",
  "metrics": {
    "code": {
      "total_lines": {count},
      "total_files": {count},
      "languages": {
        "java": {lines},
        "javascript": {lines}
      }
    },
    "quality": {
      "test_coverage": {percentage},
      "tech_debt_score": {score},
      "security_score": {score},
      "maintainability_score": {score}
    },
    "dependencies": {
      "total": {count},
      "outdated": {count},
      "vulnerable": {count},
      "critical_vulns": {count}
    },
    "complexity": {
      "score": {0-100},
      "rating": "LOW | MEDIUM | HIGH | VERY HIGH"
    },
    "feasibility": {
      "inline_upgrade": {percentage},
      "greenfield_rewrite": {percentage},
      "hybrid_approach": {percentage}
    }
  }
}
```

**Progress**: `✓ Generated: metrics-summary.md`

---

### Artifact 4A (Scope = A): functional-spec.md

**Purpose**: Functional specification for modernized application (WHAT system does)

**Source**: Extract features from analysis-report.md

**Template**: Read `.specify/templates/analyze/functional-spec-template.md` for structure

**Chunking Strategy** (Generate in 5 chunks):

#### Chunk 1: Introduction + Summary + Scope

- Sections: 1 (Introduction), 2 (Executive Summary), 3 (Scope)
- Content: Project overview, high-level purpose, what's in/out of scope
- Completion: All 3 sections complete, no placeholders

**After Chunk 1**: Display progress:

```text
✓ functional-spec.md Chunk 1/5 complete: Introduction + Summary + Scope
  - Lines: [COUNT]
```

#### Chunk 2: User Stories (Part 1) - CRITICAL Features

- Section: 4.1 (User Stories - CRITICAL)
- Content: All CRITICAL features from analysis-report.md
- Every feature MUST have file:line reference
- Completion: All CRITICAL features documented with evidence

**After Chunk 2**: Append using `str_replace`, display progress:

```text
✓ functional-spec.md Chunk 2/5 complete: User Stories (CRITICAL)
  - Features: [COUNT]
  - Lines: [COUNT]
```

#### Chunk 3: User Stories (Part 2) - STANDARD Features + Business Rules

- Sections: 4.2 (User Stories - STANDARD), 5 (Business Rules)
- Content: STANDARD features + validation rules
- Completion: All STANDARD features + rules documented

**After Chunk 3**: Append using `str_replace`, display progress:

```text
✓ functional-spec.md Chunk 3/5 complete: STANDARD Features + Rules
  - Features: [COUNT]
  - Lines: [COUNT]
```

#### Chunk 4: NFRs + Data Requirements

- Sections: 6 (Non-Functional Requirements), 7 (Data Requirements)
- Content: Performance, security, scalability, data entities
- Completion: NFRs defined, data models documented

**After Chunk 4**: Append using `str_replace`, display progress:

```text
✓ functional-spec.md Chunk 4/5 complete: NFRs + Data
  - Lines: [COUNT]
```

#### Chunk 5: Acceptance Criteria + Assumptions + Constraints

- Sections: 8 (Acceptance Criteria), 9 (Assumptions), 10 (Constraints)
- Content: Testing criteria, assumptions, limitations
- Completion: All sections complete, no placeholders

**After Chunk 5**: Append using `str_replace`, display progress:

```text
✅ functional-spec.md COMPLETE (5/5 chunks)
   - Total features: [COUNT]
   - Total lines: [COUNT]
```

**Progress**: `✓ Generated: functional-spec.md ({lines} lines, {chunks} chunks)`

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

**After Chunk 1**: Display progress:

```text
✓ technical-spec.md Chunk 1/5 complete: Architecture + Comparison
  - Diagrams: [COUNT]
  - Lines: [COUNT]
```

#### Chunk 2: Target Tech Stack + Data Architecture

- Sections: 4 (Target Tech Stack), 5 (Data Architecture)
- Content: User's chosen stack (from 10 questions), database design, ORM
- Completion: All tech choices documented, data layer designed

**After Chunk 2**: Append using `str_replace`, display progress:

```text
✓ technical-spec.md Chunk 2/5 complete: Tech Stack + Data
  - Lines: [COUNT]
```

#### Chunk 3: API Design + Integration Points

- Sections: 6 (API Design), 7 (Integration Architecture)
- Content: REST/GraphQL design, external APIs, message queues
- Completion: API contracts defined, integrations documented

**After Chunk 3**: Append using `str_replace`, display progress:

```text
✓ technical-spec.md Chunk 3/5 complete: API + Integrations
  - Endpoints: [COUNT]
  - Lines: [COUNT]
```

#### Chunk 4: Security + Authentication + Deployment

- Sections: 8 (Security), 9 (Deployment Strategy)
- Content: User's chosen auth (Q9), deployment target (Q5), IaC (Q6), containers (Q7)
- Completion: Security measures defined, deployment plan complete

**After Chunk 4**: Append using `str_replace`, display progress:

```text
✓ technical-spec.md Chunk 4/5 complete: Security + Deployment
  - Lines: [COUNT]
```

#### Chunk 5: Testing Strategy + Observability + Migration Risks

- Sections: 10 (Testing), 11 (Observability), 12 (Migration Risks)
- Content: User's testing choice (Q10), observability stack (Q8), risk mitigation
- Completion: All sections complete, no placeholders

**After Chunk 5**: Append using `str_replace`, display progress:

```text
✅ technical-spec.md COMPLETE (5/5 chunks)
   - Total lines: [COUNT]
```

**Progress**: `✓ Generated: technical-spec.md ({lines} lines, {chunks} chunks)`

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

**Progress**: `✓ Generated: stage-prompts/ (4 files)`

---

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
2. Fill in all sections using data from Stage 5B
3. Provide detailed analysis with code references

**Progress**: `✓ Generated: abstraction-assessment.md`

---

### Artifact 5B (Scope = B): concern-migration-plan.md

**Purpose**: Step-by-step migration strategy for the specific concern

**Source**: Recommended strategy from Stage 5B + TARGET_IMPLEMENTATION

**Template**: Read `.specify/templates/analyze/concern-migration-plan-template.md` for structure

**Chunking Strategy** (Generate in 3 chunks):

#### Chunk 1: Migration Strategy + Phasing

- Sections: 1 (Executive Summary), 2 (Migration Strategy), 3 (Phased Plan)
- Content: Chosen approach, justification, 50/30/15/5 phasing, timeline
- Completion: Strategy documented, phases defined with milestones

**After Chunk 1**: Display progress:

```text
✓ concern-migration-plan.md Chunk 1/3 complete: Strategy + Phasing
  - Approach: [APPROACH]
  - Phases: [COUNT]
  - Lines: [COUNT]
```

#### Chunk 2: Technical Implementation + Testing

- Sections: 4 (Setup Steps), 5 (Code Changes), 6 (Testing Strategy)
- Content: Environment setup, required code changes, test plan, rollback procedures
- Completion: Implementation steps detailed, testing strategy complete

**After Chunk 2**: Append using `str_replace`, display progress:

```text
✓ concern-migration-plan.md Chunk 2/3 complete: Implementation + Testing
  - Setup steps: [COUNT]
  - Code changes: [COUNT]
  - Lines: [COUNT]
```

#### Chunk 3: Deployment + Operations + Success Criteria

- Sections: 7 (Deployment Strategy), 8 (Monitoring), 9 (Success Criteria), 10 (Post-Migration)
- Content: Deployment approach, monitoring/alerting, success metrics, post-migration tasks
- Completion: All sections complete, operational plan ready

**After Chunk 3**: Append using `str_replace`, display progress:

```text
✅ concern-migration-plan.md COMPLETE (3/3 chunks)
   - Total lines: [COUNT]
```

**Progress**: `✓ Generated: concern-migration-plan.md ({lines} lines, {chunks} chunks)`

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

**Progress**: `✓ Generated: rollback-procedure.md`

---

## Final Summary

Display completion summary with all file paths:

```text
=== Analysis Complete ===

Generated Artifacts:

Common:
  ✓ EXECUTIVE-SUMMARY.md
  ✓ dependency-audit.md
  ✓ metrics-summary.md
  ✓ analysis-report.md (from Stage 6)

{IF scope = A}
Full Application:
  ✓ functional-spec.md
  ✓ technical-spec.md
  ✓ stage-prompts/
    - constitution-prompt.md
    - clarify-prompt.md
    - tasks-prompt.md
    - implement-prompt.md

{IF scope = B}
Cross-Cutting Concern:
  ✓ abstraction-assessment.md
  ✓ concern-migration-plan.md
  ✓ rollback-procedure.md

All files saved to: {analysis_dir}

Total Artifacts: {count}
Analysis Duration: {duration}
```

---

## Output State

```json
{
  ...previous_state,
  "stage": "artifact_generation",
  "timestamp": "2025-11-14T12:00:00Z",
  "stages_complete": [..., "artifact_generation"],
  "artifacts_generated": [
    "EXECUTIVE-SUMMARY.md",
    "dependency-audit.md",
    "metrics-summary.md",
    "analysis-report.md",
    "functional-spec.md",
    "technical-spec.md",
    "stage-prompts/constitution-prompt.md",
    "stage-prompts/clarify-prompt.md",
    "stage-prompts/tasks-prompt.md",
    "stage-prompts/implement-prompt.md"
  ],
  "total_artifacts": 10,
  "analysis_complete": true
}
```

---

## Completion Marker

```text
STAGE_COMPLETE:ARTIFACTS
STATE_PATH: .analysis/.state/07-artifacts.json

=== ANALYSIS CHAIN COMPLETE ===
Chain ID: {chain_id}
All stages successfully completed.
```

---

## End of Chain

This is the final stage. Analysis is complete!
