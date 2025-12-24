---
stage: file_analysis_verification
requires: 02d-test-audit checkpoint
outputs: file_analysis_complete
version: 3.1.0
next: 03a-questions-part1.md OR 03b1-abstraction-assessment.md
---

# Stage 2E: Quality Gates & Completion

## Purpose

Verify file analysis meets quality standards before proceeding. This is a mandatory verification stage - the workflow cannot continue until all quality gates pass.

---

## Pre-Check: Verify Previous Substage

1. Read `{analysis_dir}/state.json`
2. Confirm `status` = "complete"
3. Load all Phase 1-4 results

**IF not complete:** STOP - Return to 02d-test-audit.md

---

## Step 1: Load All Phase Results

Aggregate results from all previous phases:

```bash
# Load all checkpoint files

cat {analysis_dir}/state.json
cat {analysis_dir}/state.json
cat {analysis_dir}/state.json
cat {analysis_dir}/state.json

```

---

## Step 2: Quality Gate Verification

---
⏸️ **[STOP: QUALITY_GATE_CHECK]**

Verify each quality gate. All gates MUST pass before proceeding.

### Gate 1: Minimum File Coverage

**Requirement:** At least 70% of important files analyzed

**Calculation:**

```text
Important Files = Controllers + Services + Models + Repositories + Security + Configs
Coverage = (Files Analyzed / Important Files) × 100

```

**Check:**
- [ ] Coverage ≥ 70%

**IF FAILED:**

```text
❌ Quality Gate Failed: Minimum File Coverage

Current: {percentage}% (required: 70%)
Missing categories: {list of under-covered areas}

Action Required:
  Return to Phase 2 (02b-deep-dive.md) and complete analysis
  of the following areas:
  - {area1}: {current}% → need {target}%
  - {area2}: {current}% → need {target}%

```

STOP - Do not proceed until gate passes.

---

### Gate 2: Configuration Analysis Complete

**Requirement:** ALL configuration files analyzed (100%)

**Check:**
- [ ] All application configs analyzed
- [ ] All build configs analyzed
- [ ] Infrastructure configs analyzed (if present)

**IF FAILED:**

```text
❌ Quality Gate Failed: Configuration Analysis

Missing config files:
  - {file1}
  - {file2}

Action Required:
  Return to Phase 3 (02c-config-analysis.md) and analyze
  missing configuration files.

```

STOP - Do not proceed until gate passes.

---

### Gate 3: Minimum Feature Descriptions

**Requirement:** At least 50 feature descriptions with file:line references

**Calculation:**

```text
Features = Endpoints + Workflows + Business Rules + Integrations
Each feature must have at least one file:line reference

```

**Check:**
- [ ] Feature count ≥ 50
- [ ] All features have file:line references

**IF FAILED:**

```text
❌ Quality Gate Failed: Feature Descriptions

Current: {count} features (required: 50)
Features without references: {count}

Action Required:
  Return to Phase 2 and extract more features from:
  - Controllers/API endpoints
  - Service methods
  - Business rules

```

STOP - Do not proceed until gate passes.

---

### Gate 4: Technical Debt Items

**Requirement:** At least 20 technical debt items identified

**Categories:**
- Code quality issues
- Security vulnerabilities
- Performance problems
- Architecture issues
- Deprecated patterns

**Check:**
- [ ] Tech debt items ≥ 20
- [ ] Categorized by severity (HIGH/MEDIUM/LOW)

**IF FAILED:**

```text
❌ Quality Gate Failed: Technical Debt Analysis

Current: {count} items (required: 20)

Action Required:
  Review analyzed files for:
  - Missing error handling
  - Hardcoded values
  - Code duplication
  - Missing validations
  - Security anti-patterns

```

STOP - Do not proceed until gate passes.

---

### Gate 5: Security Findings

**Requirement:** At least 10 security-related findings (positive or negative)

**Includes:**
- Security vulnerabilities
- Secure coding practices (positive)
- Auth/authz patterns
- Encryption usage
- Input validation

**Check:**
- [ ] Security findings ≥ 10

**IF FAILED:**

```text
❌ Quality Gate Failed: Security Analysis

Current: {count} findings (required: 10)

Action Required:
  Review security-related code for:
  - Authentication implementation
  - Authorization checks
  - Input validation
  - Output encoding
  - Encryption usage
  - Sensitive data handling

```

STOP - Do not proceed until gate passes.

---

### Gate 6: Dependency Audit Complete

**Requirement:** Dependency audit performed with vulnerability check

**Check:**
- [ ] Dependencies enumerated
- [ ] Vulnerability scan performed
- [ ] Outdated packages identified

**IF FAILED:**

```text
❌ Quality Gate Failed: Dependency Audit

Missing:
  - {missing audit component}

Action Required:
  Return to Phase 4 (02d-test-audit.md) and complete
  dependency analysis.

```

STOP - Do not proceed until gate passes.

---

## Step 3: Compile Final Stage 2 State

Merge all phase results into comprehensive state:

```json
{
  "schema_version": "3.1.0",
  "chain_id": "{chain_id}",
  "stage": "file_analysis",
  "timestamp": "{ISO-8601}",
  "stages_complete": ["setup_and_scope", "file_analysis"],
  "analysis_scope": "{A or B}",

  "patterns_found": {
    "auth": {
      "type": "{mechanism}",
      "storage": "{user storage}",
      "password_hashing": "{algorithm}",
      "token": "{type with config}",
      "authorization": "{model}"
    },
    "database": {
      "engine": "{database}",
      "orm": "{framework}",
      "entities": {count},
      "relationships": {count},
      "native_queries": {count}
    },
    "api": {
      "style": "{REST/GraphQL}",
      "endpoints": {count},
      "versioning": "{strategy}",
      "documentation": "{type}"
    },
    "caching": {
      "present": true,
      "type": "{Redis/Memcached/etc}",
      "strategy": "{pattern}"
    },
    "observability": {
      "logging": "{framework}",
      "metrics": "{present/absent}",
      "tracing": "{present/absent}"
    }
  },

  "files_analyzed": {
    "total_scanned": {count},
    "total_project": {count},
    "coverage_percentage": "{percentage}%",
    "by_category": {
      "controllers": {count},
      "services": {count},
      "models": {count},
      "repositories": {count},
      "configs": {count},
      "security": {count},
      "tests": {count}
    }
  },

  "features_extracted": {
    "total": {count},
    "with_references": {count},
    "by_type": {
      "endpoints": {count},
      "workflows": {count},
      "business_rules": {count},
      "integrations": {count}
    }
  },

  "technical_debt": {
    "total": {count},
    "by_severity": {
      "high": {count},
      "medium": {count},
      "low": {count}
    },
    "items": [
      {
        "id": "TD-001",
        "severity": "HIGH",
        "category": "{category}",
        "description": "{description}",
        "location": "{file:line}",
        "impact": "{impact}",
        "recommendation": "{fix}"
      }
    ]
  },

  "security_findings": {
    "total": {count},
    "vulnerabilities": {count},
    "good_practices": {count},
    "items": [
      {
        "id": "SEC-001",
        "severity": "HIGH",
        "type": "vulnerability",
        "description": "{description}",
        "location": "{file:line}",
        "recommendation": "{fix}"
      }
    ]
  },

  "dependencies": {
    "total": {count},
    "direct": {count},
    "transitive": {count},
    "vulnerabilities": {
      "critical": {count},
      "high": {count},
      "medium": {count},
      "low": {count}
    },
    "outdated": {
      "major": {count},
      "minor": {count},
      "patch": {count}
    }
  },

  "test_coverage": {
    "framework": "{framework}",
    "test_files": {count},
    "estimated_coverage": "{percentage}%",
    "gaps": ["{critical untested areas}"]
  },

  "quality_gates": {
    "file_coverage": "PASS",
    "config_complete": "PASS",
    "feature_count": "PASS",
    "tech_debt_count": "PASS",
    "security_findings": "PASS",
    "dependency_audit": "PASS",
    "all_passed": true
  }
}

```

### Save State

Write to: `.analysis/.state/analyze-project-02-file-analysis.json`

---

## Step 4: Verify State Saved

---
⏸️ **[STOP: VERIFY_STATE_SAVED]**

1. Read `.analysis/.state/analyze-project-02-file-analysis.json`
2. Validate JSON is parseable
3. Confirm all required fields present
4. Confirm `quality_gates.all_passed` = true

**IF verification fails:**

```text
❌ State verification failed

Issues:
  - {issue1}
  - {issue2}

Action Required:
  Regenerate state file with complete data.

```

---

## Create Final Checkpoint

Write checkpoint file: `{analysis_dir}/state.json`

```json
{
  "stage": "02-file-analysis",
  "timestamp": "{ISO-8601}",
  "phases_completed": ["02a", "02b", "02c", "02d", "02e"],
  "quality_gates": {
    "file_coverage": "PASS",
    "config_complete": "PASS",
    "feature_count": "PASS",
    "tech_debt_count": "PASS",
    "security_findings": "PASS",
    "dependency_audit": "PASS"
  },
  "metrics": {
    "files_analyzed": {count},
    "features_extracted": {count},
    "tech_debt_items": {count},
    "security_findings": {count},
    "vulnerabilities": {count}
  },
  "state_saved": ".analysis/.state/analyze-project-02-file-analysis.json",
  "status": "complete"
}

```

### Verify Checkpoint

1. Read `{analysis_dir}/state.json`
2. Confirm all quality gates show "PASS"
3. Confirm status = "complete"

---

## Completion Summary

```text
═══════════════════════════════════════════════════════════
  STAGE COMPLETE: FILE_ANALYSIS

  Chain ID: {chain_id}
  Analysis Scope: {A - Full Application | B - Cross-Cutting}

  ─────────────────────────────────────────────────────────
  ANALYSIS SUMMARY
  ─────────────────────────────────────────────────────────

  Files Analyzed: {count}/{total} ({percentage}%)
  Features Extracted: {count}
  Technical Debt Items: {count} ({high} HIGH)
  Security Findings: {count} ({vulns} vulnerabilities)
  Dependency Vulnerabilities: {count} ({critical} critical)
  Test Coverage: ~{percentage}%

  ─────────────────────────────────────────────────────────
  QUALITY GATES
  ─────────────────────────────────────────────────────────

  ✓ File Coverage: PASS ({percentage}% ≥ 70%)
  ✓ Config Complete: PASS (100%)
  ✓ Features: PASS ({count} ≥ 50)
  ✓ Tech Debt: PASS ({count} ≥ 20)
  ✓ Security: PASS ({count} ≥ 10)
  ✓ Dependencies: PASS (audit complete)

  State: .analysis/.state/analyze-project-02-file-analysis.json

═══════════════════════════════════════════════════════════

STAGE_COMPLETE:FILE_ANALYSIS

```

---

## Next Stage (Conditional)

**IF** `analysis_scope = "A"`:
  Proceed to: **03a-questions-part1.md** (Full Application Modernization)

**IF** `analysis_scope = "B"`:
  Proceed to: **03b1-abstraction-assessment.md** (Cross-Cutting Concern Analysis)
