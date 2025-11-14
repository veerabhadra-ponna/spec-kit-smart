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
2. **dependency-audit.json** (1 chunk)
3. **metrics-summary.json** (1 chunk)

### Full Application Artifacts (Scope = A)

1. **functional-spec.md** (2-3 chunks)
2. **technical-spec.md** (2-3 chunks)
3. **stage-prompts/** (4 files)
   - stage-1-dependencies.md
   - stage-2-framework.md
   - stage-3-database.md
   - stage-4-deployment.md

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
```text

**Progress**: `✓ Generated: EXECUTIVE-SUMMARY.md`

---

### Artifact 2: dependency-audit.json

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
      "type": "major|minor|patch"
    }
  ],
  "vulnerable": [
    {
      "name": "{package}",
      "version": "{version}",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
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
```text

**Progress**: `✓ Generated: dependency-audit.json`

---

### Artifact 3: metrics-summary.json

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
      "rating": "LOW|MEDIUM|HIGH|VERY HIGH"
    },
    "feasibility": {
      "inline_upgrade": {percentage},
      "greenfield_rewrite": {percentage},
      "hybrid_approach": {percentage}
    }
  }
}
```text

**Progress**: `✓ Generated: metrics-summary.json`

---

### Artifact 4A (Scope = A): functional-spec.md

**Purpose**: Functional specification for modernized application

**Content Structure** (2-3 chunks):
- Chunk 1: User Stories & Features
  - All identified features as user stories
  - Acceptance criteria
  - Priority levels

- Chunk 2: Business Rules & Workflows
  - Business logic documentation
  - Workflow diagrams
  - Data flows

- Chunk 3: Non-Functional Requirements
  - Performance requirements
  - Security requirements
  - Compliance requirements

**Progress**: `✓ Generated: functional-spec.md ({lines} lines, {chunks} chunks)`

---

### Artifact 5A (Scope = A): technical-spec.md

**Purpose**: Technical specification for modernized implementation

**Content Structure** (2-3 chunks):
- Chunk 1: Architecture & Design
  - Target architecture
  - Component diagrams
  - Technology stack decisions

- Chunk 2: API Specifications
  - All API endpoints
  - Request/response schemas
  - Authentication/authorization

- Chunk 3: Data Models & Infrastructure
  - Database schema
  - Entity relationships
  - Infrastructure requirements

**Progress**: `✓ Generated: technical-spec.md ({lines} lines, {chunks} chunks)`

---

### Artifact 6A (Scope = A): stage-prompts/

**Purpose**: Staged implementation prompts for AI-assisted migration

Generate 4 stage prompt files:

**stage-1-dependencies.md**: Update dependencies to latest LTS
**stage-2-framework.md**: Migrate to target framework
**stage-3-database.md**: Migrate database if applicable
**stage-4-deployment.md**: Update deployment configuration

**Progress**: `✓ Generated: stage-prompts/ (4 files)`

---

### Artifact 4B (Scope = B): abstraction-assessment.md

**Purpose**: Detailed abstraction analysis for the concern

**Content**:

```markdown
# Abstraction Assessment: {Concern Type}

## Current Implementation
- Type: {current_implementation}
- Abstraction Level: {LOW|MEDIUM|HIGH}
- Abstraction Score: {score}/10

## Touch Points Analysis
{detailed touch points with file:line references}

## Coupling Analysis
{coupling details, dependencies, tightness}

## Refactoring Recommendations
{specific refactoring steps to improve abstraction}

## Migration Readiness
{assessment of readiness for migration}
```text

**Progress**: `✓ Generated: abstraction-assessment.md`

---

### Artifact 5B (Scope = B): concern-migration-plan.md

**Purpose**: Detailed migration plan for the specific concern

**Content Structure** (2-3 chunks):
- Chunk 1: Migration Strategy
  - Chosen approach and justification
  - Phased plan (50/30/15/5)
  - Timeline and milestones

- Chunk 2: Technical Implementation
  - Setup steps
  - Code changes required
  - Testing strategy
  - Rollback procedures

- Chunk 3: Operational Plan
  - Deployment strategy
  - Monitoring and alerting
  - Success criteria
  - Post-migration tasks

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
```text

**Progress**: `✓ Generated: rollback-procedure.md`

---

## Final Summary

Display completion summary with all file paths:

```text
=== Analysis Complete ===

Generated Artifacts:

Common:
  ✓ EXECUTIVE-SUMMARY.md
  ✓ dependency-audit.json
  ✓ metrics-summary.json
  ✓ analysis-report.md (from Stage 6)

{IF scope = A}
Full Application:
  ✓ functional-spec.md
  ✓ technical-spec.md
  ✓ stage-prompts/
    - stage-1-dependencies.md
    - stage-2-framework.md
    - stage-3-database.md
    - stage-4-deployment.md

{IF scope = B}
Cross-Cutting Concern:
  ✓ abstraction-assessment.md
  ✓ concern-migration-plan.md
  ✓ rollback-procedure.md

All files saved to: {analysis_dir}

Total Artifacts: {count}
Analysis Duration: {duration}
```text

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
    "dependency-audit.json",
    "metrics-summary.json",
    "functional-spec.md",
    "technical-spec.md",
    "stage-prompts/stage-1-dependencies.md",
    "stage-prompts/stage-2-framework.md",
    "stage-prompts/stage-3-database.md",
    "stage-prompts/stage-4-deployment.md"
  ],
  "total_artifacts": 9,
  "analysis_complete": true
}
```text

---

## Completion Marker

```text
STAGE_COMPLETE:ARTIFACTS
STATE_PATH: .analysis/.state/07-artifacts.json

=== ANALYSIS CHAIN COMPLETE ===
Chain ID: {chain_id}
All stages successfully completed.
```text

---

## End of Chain

This is the final stage. Analysis is complete!
