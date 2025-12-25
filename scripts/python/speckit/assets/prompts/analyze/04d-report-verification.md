---
stage: report_verification
requires: 04c-report-chunks-7-9 complete
outputs: report_verified
version: 3.1.0
next: 05a-executive-summary.md
---

# Stage 4D: Report Verification

## Purpose

Verify the analysis report meets all quality standards before proceeding to artifact generation.

---

## State Management

**Available template variables:**

- `{analysis_dir}` - Analysis folder path (root)
- `{data_dir}` - Data folder for JSON files (`{analysis_dir}/data/`)
- `{reports_dir}` - Reports folder for MD files (`{analysis_dir}/reports/`)

---

## Pre-Check

1. Read `{analysis_dir}/state.json`
2. Confirm all 9 chunks complete
3. Verify report exists at `{reports_dir}/analysis-report.md`

---

## Verification Checklist

---
⏸️ **[STOP: VERIFY_REPORT]**

Read the complete report at `{reports_dir}/analysis-report.md` and verify each item:

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
  "report_path": "{reports_dir}/analysis-report.md",
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

The CLI automatically updates `{analysis_dir}/state.json` with stage completion.

---

## Completion Marker

```text
═══════════════════════════════════════════════════════════
  STAGE COMPLETE: REPORT_GENERATION

  Chain ID: {chain_id}
  Report: {reports_dir}/analysis-report.md
  Lines: {count}
  Verification: PASSED ✓

  Proceeding to Stage 5: Artifact Generation
═══════════════════════════════════════════════════════════

STAGE_COMPLETE:REPORT_GENERATION

```

---

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
