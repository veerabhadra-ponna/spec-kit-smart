---
stage: report_generation
requires: 05-*.json
outputs: report_generated
version: 1.0.0
---

# Stage 6: Analysis Report Generation

## Purpose

Generate the comprehensive `analysis-report.md` file using completion-based chunking strategy. This is the primary deliverable that documents all findings.

---

## Previous State

Load state from either:
- `.analysis/.state/05a-full-app.json` (if scope = A)
- `.analysis/.state/05b-cross-cutting.json` (if scope = B)

---

## Chunking Strategy

**CRITICAL**: Use **completion-based chunking**, NOT size-based chunking.

- Generate complete logical sections in each chunk
- Each chunk ends with a distinct completion point
- Display progress after each chunk
- Create checkpoint markers
- NO placeholders allowed

---

## Report Structure (9 Phases)

Generate report in `.analysis/{project}-{timestamp}/analysis-report.md`

### Chunk 1: Phase 1 - Project Discovery

Complete sections:
- **1.1 Technology Stack** (from structure analysis)
- **1.2 System Architecture** (from project type)
- **1.3 Project Statistics** (LOC, file counts)
- **1.4 Configuration Analysis** (all config files)
- **1.5 Build & Deployment** (build tools, scripts)

**Completion Criteria**:
- ✓ All configuration files analyzed
- ✓ Tech stack fully identified
- ✓ Architecture documented with evidence
- ✓ Project statistics calculated
- ✓ NO placeholders

**Progress Display**:

```
✓ Chunk 1/9 complete: Phase 1 (Project Discovery)
  - Analyzed: {count} configuration files
  - Identified: {tech stack summary}
  - Lines generated: {count}
```

### Chunk 2: Phase 2.1 - Controllers & API Endpoints

Complete **Section 2.1: Controllers Analysis**:
- EVERY controller file analyzed
- EVERY API endpoint documented (method, path, purpose)
- File:line references for all findings
- Auth requirements for each endpoint
- NO placeholders

**Progress Display**:

```
✓ Chunk 2/9 complete: Phase 2.1 (Controllers)
  - Analyzed: {count} controller files
  - Documented: {count} API endpoints
  - Lines generated: {count}
```

### Chunk 3: Phase 2.2 - Services & Business Logic

Complete **Section 2.2: Services Analysis**:
- EVERY service file analyzed
- Business workflows documented with evidence
- External integrations identified
- Transaction patterns clear
- NO placeholders

**Progress Display**:

```
✓ Chunk 3/9 complete: Phase 2.2 (Services)
  - Analyzed: {count} service files
  - Documented: {count} business workflows
  - Lines generated: {count}
```

### Chunk 4: Phase 2.3 - Data Layer

Complete **Section 2.3: Data Models & Repositories**:
- EVERY model/entity file analyzed
- Relationships documented (with cardinality)
- Validation rules extracted
- Database operations categorized
- NO placeholders

**Progress Display**:

```
✓ Chunk 4/9 complete: Phase 2.3 (Data Layer)
  - Analyzed: {count} model files, {count} repositories
  - Documented: {count} entities, {count} relationships
  - Lines generated: {count}
```

### Chunk 5: Phase 3 - Positive Findings

Complete **Section 3: What's Working Well**:
- 10-30 positive findings with file:line references
- Evidence-based (not generic praise)
- Specific examples of good practices
- NO placeholders

**Progress Display**:

```
✓ Chunk 5/9 complete: Phase 3 (Positive Findings)
  - Documented: {count} positive findings
  - Lines generated: {count}
```

### Chunk 6: Phase 4 - Technical Debt & Issues

Complete **Section 4: Technical Debt**:
- **4.1** Technical Debt (HIGH/MEDIUM/LOW severity)
- **4.2** Security Vulnerabilities (with CVE references)
- **4.3** Code Quality Issues (smells, duplication)
- **4.4** Architecture Issues (coupling, abstractions)
- 20-50 technical debt items categorized
- 10-30 security findings with risk scores
- NO placeholders

**Progress Display**:

```
✓ Chunk 6/9 complete: Phase 4 (Technical Debt)
  - Tech debt items: {count}
  - Security findings: {count}
  - Lines generated: {count}
```

### Chunk 7: Phase 5 - Upgrade Path Analysis

Complete **Section 5: Upgrade Paths**:
- **5.1** Runtime/Framework Upgrades
- **5.2** Dependency Upgrades
- **5.3** Database Migration Paths
- All upgrade paths evaluated
- Breaking changes identified
- Effort estimates provided
- Risk assessment for each path
- NO placeholders

**Progress Display**:

```
✓ Chunk 7/9 complete: Phase 5 (Upgrade Paths)
  - Upgrade paths documented: {count}
  - Lines generated: {count}
```

### Chunk 8: Phases 6-7 - Modernization & Feasibility

Complete **Sections 6 & 7**:
- **Section 6**: Modernization Recommendations
  - Quick wins (low effort, high value)
  - Strategic improvements
  - Long-term goals
- **Section 7**: Feasibility Scoring
  - Inline upgrade feasibility (formula shown)
  - Greenfield rewrite feasibility (formula shown)
  - Hybrid approach feasibility
- Recommendations prioritized
- Feasibility scores calculated with formulas
- NO placeholders

**Progress Display**:

```
✓ Chunk 8/9 complete: Phases 6-7 (Modernization & Feasibility)
  - Recommendations: {count}
  - Feasibility scores calculated
  - Lines generated: {count}
```

### Chunk 9: Phases 8-9 - Decision Matrix & Final Recommendations

Complete **Sections 8 & 9**:
- **Section 8**: Decision Matrix
  - Comparison table: Time, Cost, Risk, Business Disruption
  - Scoring for each approach
- **Section 9**: Final Recommendations
  - Primary recommendation with confidence score (0-100%)
  - Immediate actions (next steps)
  - Short-term roadmap (0-6 months)
  - Long-term roadmap (6-18 months)
- Decision matrix complete
- Primary recommendation stated
- Roadmaps provided with milestones
- NO placeholders

**Progress Display**:

```
✓ Chunk 9/9 complete: Phases 8-9 (Decision Matrix & Recommendations)
  - Decision matrix complete
  - Primary recommendation: {approach}
  - Lines generated: {count}
```

---

## Verification Gate (HARD STOP)

**BEFORE** proceeding to Stage 7, verify report quality:

### Checklist

- [ ] File exists at expected path
- [ ] All 9 phase headers present (Phase 1-9)
- [ ] Quality checks:
      - [ ] 50+ file:line references present
      - [ ] Technical debt items have severity ratings (HIGH/MEDIUM/LOW)
      - [ ] Security vulnerabilities documented with risk scores
      - [ ] Feasibility scores calculated with formulas shown
      - [ ] Primary recommendation stated with confidence score (0-100%)
      - [ ] No placeholders (TODO, TBD, "will be analyzed")
      - [ ] All tables properly formatted
      - [ ] All code blocks have syntax highlighting
- [ ] Completeness:
      - [ ] Total lines: 3,000+ (minimum)
      - [ ] Feature descriptions: 50-200 with evidence
      - [ ] Technical debt items: 20-50 categorized
      - [ ] Security findings: 10-30 with risk scores

**If ANY checkbox fails**:
- Identify incomplete sections
- Regenerate ONLY missing phases using checkpoint system
- Enhance quality issues in problematic sections
- Re-run verification

**Only after PASSING verification**: Proceed to Stage 7

---

## Output State

```json
{
  ...previous_state,
  "stage": "report_generation",
  "timestamp": "2025-11-14T11:30:00Z",
  "stages_complete": [..., "report_generation"],
  "report_generated": true,
  "report_path": ".analysis/{project}-{timestamp}/analysis-report.md",
  "report_stats": {
    "total_lines": 3450,
    "chunks_generated": 9,
    "file_references": 127,
    "tech_debt_items": 34,
    "security_findings": 18
  },
  "verification_passed": true
}
```

---

## Completion Marker

```
STAGE_COMPLETE:REPORT
STATE_PATH: .analysis/.state/06-report.json
```

---

## Next Stage

Proceed to: **Stage 7: 07-artifacts.md** (Generate remaining artifacts)
