---
stage: common_artifact_generation
requires: 04-report.json
outputs: common_artifacts_complete
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

# Stage 5: Common Artifacts Generation

## Purpose

Generate common artifacts that are required for both analysis scopes. Scope-specific artifacts are generated in Stage 6.

---

## Previous State

Load state from: `.analysis/.state/04-report.json`

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

**Note:** analysis-report.md was generated in Stage 4.

**Scope-specific artifacts** (functional-spec, technical-spec, etc.) are generated in **Stage 6**.

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
      "rating": "LOW | MEDIUM | HIGH | VERY HIGH"
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

---

## Final Verification Checklist

Before proceeding to Stage 6, verify:

- [ ] EXECUTIVE-SUMMARY.md generated
- [ ] dependency-audit.json generated
- [ ] metrics-summary.json generated
- [ ] No placeholders or TODOs in generated files
- [ ] All JSON files are valid

**IF any checkbox is unchecked, STOP and fix the issue before proceeding.**

---

## Output State

```json
{
  "common_artifacts_complete": true,
  "artifacts_generated": [
    "EXECUTIVE-SUMMARY.md",
    "dependency-audit.json",
    "metrics-summary.json"
  ],
  "timestamp": "{ISO-8601}",
  "ready_for_scope_artifacts": true
}
```

---

## Completion Marker

```text
STAGE_COMPLETE:COMMON_ARTIFACTS
STATE_PATH: .analysis/.state/05-artifacts.json
```

---

## Next Stage

Proceed to: **Stage 6: 06-scope-artifacts.md** (Generate scope-specific artifacts)
