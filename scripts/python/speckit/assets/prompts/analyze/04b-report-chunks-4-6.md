---
stage: report_generation_2
requires: 04a-report-chunks-1-3 complete
outputs: report_chunks_4_6
version: 3.1.0
next: 04c-report-chunks-7-9.md
---

# Stage 4B: Report Generation (Chunks 4-6)

## Purpose

Generate chunks 4-6: Data Layer, Positive Findings, and Technical Debt & Issues.

---

## State Management

**Available template variables:**

- `{analysis_dir}` - Analysis folder path (root)
- `{data_dir}` - Data folder for JSON files (`{analysis_dir}/data/`)
- `{reports_dir}` - Reports folder for MD files (`{analysis_dir}/reports/`)

**CLI Utility Commands:**

- `speckitadv write-report analysis-report.md --content '<md>' --append` - Append to report

---

## Pre-Check

1. Read `{analysis_dir}/state.json`
2. Confirm chunks 1-3 complete
3. Read current report at `{reports_dir}/analysis-report.md`

---

## Chunk 4: Phase 2.3 - Data Layer

---
⏸️ **[STOP: GENERATE_CHUNK_4]**

**Append to report:**

```markdown
### 2.3 Data Layer (Models & Repositories)

**Total Entities:** {count}
**Total Repositories:** {count}

#### Entity: {EntityName}

**File:** `{path}:{lines}`
**Table:** `{table_name}`

| Field | Type | Constraints | PII | Evidence |
|-------|------|-------------|-----|----------|
| {field} | {type} | {constraints} | {Y/N} | `{line}` |

**Relationships:**
- {relationship with evidence}

#### Repository: {RepositoryName}

**File:** `{path}:{lines}`

**Query Methods:**

| Method | Type | Complexity | Evidence |
|--------|------|------------|----------|
| {method} | {ORM/Native SQL} | {L/M/H} | `{line}` |

**Data Layer Issues:**
- {N+1 queries, missing indexes, etc. with evidence}

---

```

---
⏸️ **[STOP: VERIFY_CHUNK_4]**

Output: `✓ Chunk 4/9: Data Layer ({entities} entities, {lines} lines)`

---

## Chunk 5: Phase 3 - Positive Findings

---
⏸️ **[STOP: GENERATE_CHUNK_5]**

**Append to report:**

```markdown
## Phase 3: What's Working Well

**Total Positive Findings:** {count}

### 3.1 Architecture & Design

| Finding | Evidence | Impact |
|---------|----------|--------|
| {good practice} | `{file}:{line}` | {positive impact} |

### 3.2 Code Quality

| Finding | Evidence | Impact |
|---------|----------|--------|
| {good practice} | `{file}:{line}` | {positive impact} |

### 3.3 Security Practices

| Finding | Evidence | Impact |
|---------|----------|--------|
| {secure pattern} | `{file}:{line}` | {benefit} |

### 3.4 Testing & Quality Assurance

| Finding | Evidence | Impact |
|---------|----------|--------|
| {good testing} | `{file}:{line}` | {benefit} |

### 3.5 Documentation & Maintainability

| Finding | Evidence | Impact |
|---------|----------|--------|
| {documentation} | `{file}:{line}` | {benefit} |

---

```

---
⏸️ **[STOP: VERIFY_CHUNK_5]**

Output: `✓ Chunk 5/9: Positive Findings ({count} findings, {lines} lines)`

---

## Chunk 6: Phase 4 - Technical Debt & Issues

---
⏸️ **[STOP: GENERATE_CHUNK_6]**

**Append to report:**

```markdown
## Phase 4: Technical Debt & Issues

### 4.1 Technical Debt

**Total Items:** {count}

#### HIGH Severity

| ID | Issue | Location | Impact | Recommendation |
|----|-------|----------|--------|----------------|
| TD-001 | {issue} | `{file}:{line}` | {impact} | {fix} |

#### MEDIUM Severity

| ID | Issue | Location | Impact | Recommendation |
|----|-------|----------|--------|----------------|
| TD-002 | {issue} | `{file}:{line}` | {impact} | {fix} |

#### LOW Severity

| ID | Issue | Location | Impact | Recommendation |
|----|-------|----------|--------|----------------|
| TD-003 | {issue} | `{file}:{line}` | {impact} | {fix} |

### 4.2 Security Vulnerabilities

**Total Vulnerabilities:** {count}

| ID | Severity | Issue | Location | CVE | Remediation |
|----|----------|-------|----------|-----|-------------|
| SEC-001 | {sev} | {issue} | `{file}:{line}` | {CVE if any} | {fix} |

### 4.3 Code Quality Issues

| Category | Count | Examples |
|----------|-------|----------|
| Code Duplication | {n} | `{file}:{line}` |
| Long Methods | {n} | `{file}:{line}` |
| Complex Conditionals | {n} | `{file}:{line}` |
| Missing Error Handling | {n} | `{file}:{line}` |

### 4.4 Architecture Issues

| Issue | Severity | Impact | Location | Recommendation |
|-------|----------|--------|----------|----------------|
| {issue} | {sev} | {impact} | `{files}` | {fix} |

---

```

---
⏸️ **[STOP: VERIFY_CHUNK_6]**

Output: `✓ Chunk 6/9: Tech Debt ({debt_count} debt, {sec_count} security, {lines} lines)`

---

## Output Summary

```text
═══════════════════════════════════════════════════════════
  SUBSTAGE COMPLETE: 04b-report-chunks-4-6

  Chunks Generated: 6/9
  Cumulative Lines: {count}

  Content:
    Phase 2.3: Data Layer ({entities} entities) ✓
    Phase 3: Positive Findings ({count}) ✓
    Phase 4: Tech Debt & Issues ({count}) ✓

  Proceeding to Chunks 7-9...
═══════════════════════════════════════════════════════════

```

---

## Next Substage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
