---
stage: report_generation_3
requires: 04b-complete checkpoint
outputs: report_complete
version: 3.1.0
next: 04d-report-verification.md
---

# Stage 4C: Report Generation (Chunks 7-9)

## Purpose

Generate final chunks 7-9: Upgrade Paths, Modernization & Feasibility, and Final Recommendations.

---

## Pre-Check

1. Read `.analysis/.checkpoints/04b-complete.json`
2. Confirm chunks 1-6 complete
3. Load Stage 3 state for recommendations data

---

## Chunk 7: Phase 5 - Upgrade Path Analysis

---
⏸️ **[STOP: GENERATE_CHUNK_7]**

**Append to report:**

```markdown
## Phase 5: Upgrade Path Analysis

### 5.1 Runtime/Language Upgrades

| Current | Target | Breaking Changes | Effort | Evidence |
|---------|--------|------------------|--------|----------|
| {current} | {target} | {changes} | {effort} | {file} |

**Migration Notes:**
{Detailed notes on language/runtime upgrade}

### 5.2 Framework Upgrades

| Framework | Current | Target | Status | Effort |
|-----------|---------|--------|--------|--------|
| {name} | {current} | {LTS} | {EOL/Active} | {effort} |

**Breaking Changes:**
- {change 1 with migration path}
- {change 2 with migration path}

### 5.3 Database Migration Paths

| Current | Options | Recommended | Effort | Risk |
|---------|---------|-------------|--------|------|
| {current} | {options} | {recommended} | {effort} | {risk} |

**Data Migration Considerations:**
- {consideration 1}
- {consideration 2}

### 5.4 Dependency Upgrades

| Package | Current | Latest | Priority | CVEs |
|---------|---------|--------|----------|------|
| {pkg} | {current} | {latest} | {H/M/L} | {count} |

---

```

**Checkpoint:** `.analysis/.checkpoints/report-chunk-7.json`

---
⏸️ **[STOP: VERIFY_CHUNK_7]**

Output: `✓ Chunk 7/9: Upgrade Paths ({lines} lines)`

---

## Chunk 8: Phases 6-7 - Modernization & Feasibility

---
⏸️ **[STOP: GENERATE_CHUNK_8]**

**Append to report:**

```markdown
## Phase 6: Modernization Recommendations

### 6.1 Quick Wins (Low Effort, High Value)

| Action | Effort | Impact | Components | Timeline |
|--------|--------|--------|------------|----------|
| {action} | LOW | HIGH | {list} | {time} |

### 6.2 Strategic Improvements

| Action | Effort | Impact | Components | Timeline |
|--------|--------|--------|------------|----------|
| {action} | MEDIUM | HIGH | {list} | {time} |

### 6.3 Long-term Goals

| Action | Effort | Impact | Components | Timeline |
|--------|--------|--------|------------|----------|
| {action} | HIGH | HIGH | {list} | {time} |

---

## Phase 7: Feasibility Scoring

### 7.1 Inline Upgrade Feasibility

**Score:** {score}%

**Formula:**

```text
Score = 100 - (Complexity × 10) + Abstraction Bonus

Components:
  Complexity Factor: {score}/10
  Abstraction Level: {level}
  Abstraction Bonus: {bonus}
```

**Factors:**

| Factor | Score | Weight | Contribution |
|--------|-------|--------|--------------|
| Tech Stack Gap | {score} | 25% | {value} |
| Abstraction Level | {score} | 30% | {value} |
| Test Coverage | {score} | 15% | {value} |
| Dependencies | {score} | 15% | {value} |
| Team Familiarity | {score} | 15% | {value} |

### 7.2 Greenfield Rewrite Feasibility

**Score:** {score}%

**Formula:**

```text
Score = 50 + Abstraction Penalty - (Feature Count / 10)
```

**Factors:**

| Factor | Assessment | Impact |
|--------|------------|--------|
| Feature Complexity | {level} | {impact} |
| Data Migration | {level} | {impact} |
| Integration Count | {count} | {impact} |
| Timeline Pressure | {level} | {impact} |

### 7.3 Hybrid Approach Feasibility

**Score:** {score}% ⭐

**Formula:**

```text
Score = (Inline + Greenfield) / 2 + 10 (flexibility bonus)
```

**Rationale:**
{Why hybrid might be suitable}

---

<!-- markdownlint-disable-next-line MD040 -->
```

**Checkpoint:** `.analysis/.checkpoints/report-chunk-8.json`

---
⏸️ **[STOP: VERIFY_CHUNK_8]**

Output: `✓ Chunk 8/9: Modernization & Feasibility ({lines} lines)`

---

## Chunk 9: Phases 8-9 - Decision Matrix & Final Recommendations

---
⏸️ **[STOP: GENERATE_CHUNK_9]**

**Append to report:**

```markdown
## Phase 8: Decision Matrix

### Approach Comparison

| Criterion | Inline Upgrade | Greenfield | Hybrid |
|-----------|---------------|------------|--------|
| **Time to Value** | {rating} | {rating} | {rating} |
| **Total Cost** | {rating} | {rating} | {rating} |
| **Risk Level** | {rating} | {rating} | {rating} |
| **Business Disruption** | {rating} | {rating} | {rating} |
| **Technical Debt** | {rating} | {rating} | {rating} |
| **Team Learning** | {rating} | {rating} | {rating} |

### Weighted Scores

| Approach | Score | Confidence |
|----------|-------|------------|
| Inline Upgrade | {score}/100 | {conf}% |
| Greenfield Rewrite | {score}/100 | {conf}% |
| Hybrid/Strangler | {score}/100 | {conf}% |

---

## Phase 9: Final Recommendations

### Primary Recommendation

**Approach:** {recommended_approach}
**Confidence:** {confidence}%

**Rationale:**
{Detailed explanation of why this approach is recommended}

### Immediate Actions (Next 2 Weeks)

1. {Action 1}
2. {Action 2}
3. {Action 3}

### Short-Term Roadmap (0-6 Months)

| Month | Milestone | Deliverables |
|-------|-----------|--------------|
| 1-2 | {milestone} | {deliverables} |
| 3-4 | {milestone} | {deliverables} |
| 5-6 | {milestone} | {deliverables} |

### Long-Term Roadmap (6-18 Months)

| Period | Focus | Expected Outcomes |
|--------|-------|-------------------|
| 6-12 months | {focus} | {outcomes} |
| 12-18 months | {focus} | {outcomes} |

### Success Metrics

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| {metric} | {current} | {target} | {when} |

### Risk Mitigation Summary

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {risk} | {prob} | {impact} | {mitigation} |

---

## Appendix

**Analysis Metadata:**
- Chain ID: {chain_id}
- Analysis Date: {date}
- Files Analyzed: {count}
- Time Taken: {duration}
- Tool Version: 3.1.0

**Report Statistics:**
- Total Lines: {count}
- File References: {count}
- Tech Debt Items: {count}
- Security Findings: {count}
- Recommendations: {count}

---

*End of Analysis Report*

```

**Checkpoint:** `.analysis/.checkpoints/report-chunk-9.json`

---
⏸️ **[STOP: VERIFY_CHUNK_9]**

Output: `✓ Chunk 9/9: Recommendations ({lines} lines)`

---

## Substage Checkpoint

Write: `.analysis/.checkpoints/04c-complete.json`

```json
{
  "substage": "04c-report-chunks-7-9",
  "timestamp": "{ISO-8601}",
  "chunks_completed": [7, 8, 9],
  "all_chunks_complete": true,
  "total_lines": {count},
  "primary_recommendation": "{approach}",
  "confidence": {percentage},
  "status": "complete"
}

```

---
⏸️ **[STOP: CHECKPOINT_VERIFY]**

Output: `✓ Checkpoint verified: 04c (Chunks 7-9, Report Generation Complete)`

---

## Output Summary

```text
═══════════════════════════════════════════════════════════
  SUBSTAGE COMPLETE: 04c-report-chunks-7-9

  All 9 Chunks Generated ✓
  Total Report Lines: {count}

  Content:
    Phase 5: Upgrade Paths ✓
    Phase 6: Modernization ✓
    Phase 7: Feasibility Scoring ✓
    Phase 8: Decision Matrix ✓
    Phase 9: Final Recommendations ✓

  Report: {analysis_dir}/analysis-report.md

  Proceeding to Report Verification...
═══════════════════════════════════════════════════════════

```

---

## Next Substage

Proceed immediately to: **04d-report-verification.md**
