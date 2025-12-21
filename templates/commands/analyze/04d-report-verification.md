---
stage: report_verification
requires: 04c-complete checkpoint
outputs: report_verified
version: 3.1.0
next: 05a-executive-summary.md
---

# Stage 4D: Report Verification

## Purpose

Verify the analysis report meets all quality standards before proceeding to artifact generation.

---

## Pre-Check

1. Read `.analysis/.checkpoints/04c-complete.json`
2. Confirm all 9 chunks complete

---

## Verification Checklist

---
⏸️ **[STOP: VERIFY_REPORT]**

Read the complete analysis-report.md and verify each item:

### Structure Verification

- [ ] Phase 1: Project Discovery present
- [ ] Phase 2: Codebase Analysis (2.1, 2.2, 2.3) present
- [ ] Phase 3: Positive Findings present
- [ ] Phase 4: Technical Debt & Issues present
- [ ] Phase 5: Upgrade Path Analysis present
- [ ] Phase 6: Modernization Recommendations present
- [ ] Phase 7: Feasibility Scoring present
- [ ] Phase 8: Decision Matrix present
- [ ] Phase 9: Final Recommendations present

### Quality Verification

- [ ] 50+ file:line references throughout
- [ ] Tech debt items have severity ratings
- [ ] Security findings have risk scores
- [ ] Feasibility scores have formulas shown
- [ ] Primary recommendation stated with confidence
- [ ] No placeholders (TODO, TBD, "coming soon")
- [ ] All tables properly formatted
- [ ] All code blocks have syntax highlighting

### Size Verification (based on project)

**Small projects (<5K LOC):** 1,000+ lines
**Medium projects (5K-50K LOC):** 3,000+ lines
**Large projects (>50K LOC):** 5,000+ lines

---

## Verification Results

**IF ALL checks pass:**

```text
═══════════════════════════════════════════════════════════
  ✅ VERIFICATION PASSED

  analysis-report.md meets quality standards:
    • All 9 phases present
    • {count}+ file:line references
    • Tech debt categorized ({count} items)
    • Security documented ({count} findings)
    • Feasibility calculated
    • Recommendation clear ({confidence}%)
    • Total lines: {count}
═══════════════════════════════════════════════════════════

```

**IF ANY check fails:**

```text
═══════════════════════════════════════════════════════════
  ❌ VERIFICATION FAILED

  Issues Found:
    • {list failed checks}

  Recovery Required:
    Return to appropriate substage to fix issues
═══════════════════════════════════════════════════════════

```

---
⏸️ **[STOP: HANDLE_VERIFICATION_RESULT]**

**IF PASSED:** Continue to state generation
**IF FAILED:** Return to fix issues before proceeding

---

## Generate Stage 4 State

```json
{
  "schema_version": "3.1.0",
  "chain_id": "{chain_id}",
  "stage": "report_generation",
  "timestamp": "{ISO-8601}",
  "stages_complete": ["setup_and_scope", "file_analysis", "{stage_3}", "report_generation"],
  "report_generated": true,
  "report_path": ".analysis/{dir}/analysis-report.md",
  "report_stats": {
    "total_lines": {count},
    "chunks": 9,
    "file_references": {count},
    "tech_debt_items": {count},
    "security_findings": {count}
  },
  "verification_passed": true
}

```

Write to: `.analysis/.state/04-report.json`

---

## Final Checkpoint

Write: `.analysis/.checkpoints/04-report-complete.json`

```json
{
  "stage": "04-report-generation",
  "timestamp": "{ISO-8601}",
  "substages_completed": ["04a", "04b", "04c", "04d"],
  "chunks_generated": 9,
  "total_lines": {count},
  "verification_passed": true,
  "state_saved": ".analysis/.state/04-report.json",
  "status": "complete"
}

```

---
⏸️ **[STOP: CHECKPOINT_VERIFY]**

**IF verified:**
  Output: `✓ Checkpoint verified: 04-report-generation`
  Output: `✓ Report verified and state saved`

---

## Completion Marker

```text
═══════════════════════════════════════════════════════════
  STAGE COMPLETE: REPORT_GENERATION

  Chain ID: {chain_id}
  Report: .analysis/{dir}/analysis-report.md
  Lines: {count}
  Verification: PASSED ✓

  Proceeding to Stage 5: Artifact Generation
═══════════════════════════════════════════════════════════

STAGE_COMPLETE:REPORT_GENERATION

```

---

## Next Stage

Proceed immediately to: **05a-executive-summary.md**
