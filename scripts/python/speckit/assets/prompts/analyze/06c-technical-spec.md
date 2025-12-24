---
stage: technical_spec
requires: functional-spec-target complete
condition: state.analysis_scope == "A"
outputs: technical_spec_complete
version: 3.1.0
next: 06d-stage-prompts.md
---

# Stage 6C: Technical Specification

## Purpose

Generate technical specification documenting HOW to build the modernized system. This includes architecture, implementation design, deployment, and operational concerns.

---

## Pre-Check

1. Read `{analysis_dir}/state.json`
2. Confirm `status` = "complete"
3. Load user's modernization preferences from `.analysis/.state/analyze-project-03a-full-app.json`

**IF not complete:** STOP - Return to 06b-functional-spec-target.md

---

## Source of Truth

**Sources:**
- `{analysis_dir}/analysis-report.md`
- `.analysis/.state/analyze-project-03a-full-app.json` (10 modernization preferences)
- Both functional specs for feature reference

**Template:**

{{include:technical-spec-template.md}}

---

## Chunk 1: Architecture Overview + Legacy vs Target

Generate Sections 1, 2, and 3.

---
⏸️ **[STOP: GENERATE_CHUNK_1]**

### Section 1: Introduction

- Document purpose
- Technical audience
- Scope of implementation

### Section 2: Architecture Overview

```markdown
## 2. Architecture Overview

### 2.1 System Context (C4 Level 1)

{Mermaid diagram showing system in context}

### 2.2 Container View (C4 Level 2)

{Mermaid diagram showing containers/services}

### 2.3 Architecture Style

- Pattern: {Monolith | Microservices | Modular Monolith}
- Justification: {based on user preferences}

```

### Section 3: Legacy vs Target Comparison

| Aspect | Legacy | Target | Migration Impact |
|--------|--------|--------|------------------|
| Language | {current} | Q1: {answer} | {impact} |
| Database | {current} | Q2: {answer} | {impact} |
| Deployment | {current} | Q5: {answer} | {impact} |

Write to: `{analysis_dir}/technical-spec.md`

**Output:**

```text
technical-spec.md Chunk 1/5 complete: Architecture + Comparison
  - Diagrams: [COUNT]
  - Lines: [COUNT]

```

---

## Chunk 2: Target Tech Stack + Data Architecture

Generate Sections 4 and 5 using user's Q1-Q4 answers.

---
⏸️ **[STOP: GENERATE_CHUNK_2]**

### Section 4: Target Technology Stack

Based on user's 10 questions:

```markdown
## 4. Target Technology Stack

### 4.1 Runtime & Language

- **Target:** {Q1 answer}
- **Version:** {specific version}
- **Migration from:** {legacy language/version}

### 4.2 Database

- **Target:** {Q2 answer}
- **Migration Strategy:** {approach}
- **Schema Changes:** {summary}

### 4.3 Message Bus

- **Target:** {Q3 answer}
- **Use Cases:** {async patterns}

### 4.4 Package Management

- **Target:** {Q4 answer}
- **Dependency Strategy:** {approach}

```

### Section 5: Data Architecture

```markdown
## 5. Data Architecture

### 5.1 Database Design

{ERD diagram in Mermaid}

### 5.2 Data Flow

{Data flow diagram showing system data paths}

### 5.3 Migration Plan

| Table | Legacy Schema | Target Schema | Migration |
|-------|--------------|---------------|-----------|
| {table} | {columns} | {columns} | {approach} |

```

Append to: `{analysis_dir}/technical-spec.md`

**Output:**

```text
technical-spec.md Chunk 2/5 complete: Tech Stack + Data
  - Target Language: {Q1}
  - Target Database: {Q2}
  - Lines: [COUNT]

```

---

## Chunk 3: API Design + Integration Architecture

Generate Sections 6 and 7.

---
⏸️ **[STOP: GENERATE_CHUNK_3]**

### Section 6: API Design

```markdown
## 6. API Design

### 6.1 API Style

- Style: {REST | GraphQL | gRPC}
- Versioning: {strategy}

### 6.2 Endpoint Catalog

| Endpoint | Method | Purpose | Legacy Equiv |
|----------|--------|---------|--------------|
| {path} | {method} | {purpose} | {legacy ref} |

### 6.3 API Contract Examples

{OpenAPI/GraphQL schema snippets}

```

### Section 7: Integration Architecture

```markdown
## 7. Integration Architecture

### 7.1 External Systems

{Sequence diagram showing integrations}

### 7.2 Integration Points

| System | Protocol | Auth | Data Format |
|--------|----------|------|-------------|
| {system} | {protocol} | {auth} | {format} |

### 7.3 Message Queue Patterns

- Pattern: {Pub/Sub | Request/Reply | Event Sourcing}
- Queue: {Q3 answer}

```

Append to: `{analysis_dir}/technical-spec.md`

**Output:**

```text
technical-spec.md Chunk 3/5 complete: API + Integrations
  - Endpoints: [COUNT]
  - Integrations: [COUNT]
  - Lines: [COUNT]

```

---

## Chunk 4: Security + Deployment

Generate Sections 8 and 9 using Q5, Q6, Q7, Q9 answers.

---
⏸️ **[STOP: GENERATE_CHUNK_4]**

### Section 8: Security Architecture

Based on Q9 (Security approach):

```markdown
## 8. Security Architecture

### 8.1 Authentication

- Approach: {Q9 answer}
- Implementation: {details}

### 8.2 Authorization

- Model: {RBAC | ABAC | etc.}
- Enforcement: {where/how}

### 8.3 Data Protection

- Encryption at rest: {approach}
- Encryption in transit: {approach}
- Secrets management: {approach}

### 8.4 Security Checklist

- [ ] OWASP Top 10 mitigations
- [ ] Input validation
- [ ] Output encoding
- [ ] Rate limiting

```

### Section 9: Deployment Architecture

Based on Q5 (Deployment), Q6 (IaC), Q7 (Containers):

```markdown
## 9. Deployment Architecture

### 9.1 Target Environment

- Platform: {Q5 answer}
- Container: {Q7 answer}
- IaC Tool: {Q6 answer}

### 9.2 Deployment Diagram

{Mermaid diagram showing deployment topology}

### 9.3 CI/CD Pipeline

{Pipeline stages and gates}

### 9.4 Environment Strategy

| Environment | Purpose | Config |
|-------------|---------|--------|
| dev | Development | {config} |
| staging | Pre-prod | {config} |
| prod | Production | {config} |

```

Append to: `{analysis_dir}/technical-spec.md`

**Output:**

```text
technical-spec.md Chunk 4/5 complete: Security + Deployment
  - Security Approach: {Q9}
  - Deployment Target: {Q5}
  - Container: {Q7}
  - Lines: [COUNT]

```

---

## Chunk 5: Testing + Observability + Migration Risks

Generate Sections 10, 11, and 12 using Q8, Q10 answers.

---
⏸️ **[STOP: GENERATE_CHUNK_5]**

### Section 10: Testing Strategy

Based on Q10 (Testing approach):

```markdown
## 10. Testing Strategy

### 10.1 Testing Approach

- Strategy: {Q10 answer}
- Coverage Target: {percentage}

### 10.2 Test Pyramid

| Level | Tool | Coverage |
|-------|------|----------|
| Unit | {tool} | {target}% |
| Integration | {tool} | {target}% |
| E2E | {tool} | {target}% |

### 10.3 Migration Testing

- Feature parity tests
- Performance regression tests
- Data integrity verification

```

### Section 11: Observability

Based on Q8 (Observability stack):

```markdown
## 11. Observability

### 11.1 Stack

- Metrics: {Q8 metrics answer}
- Logging: {Q8 logging answer}
- Tracing: {Q8 tracing answer}

### 11.2 Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| {metric} | {target} | {threshold} |

### 11.3 Dashboards

- {dashboard 1 purpose}
- {dashboard 2 purpose}

```

### Section 12: Migration Risks & Mitigations

```markdown
## 12. Migration Risks

### 12.1 Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {risk} | {H/M/L} | {H/M/L} | {strategy} |

### 12.2 Rollback Strategy

- Trigger conditions
- Rollback procedure
- Data recovery

### 12.3 Success Criteria

- [ ] All features migrated
- [ ] Performance meets targets
- [ ] Zero data loss
- [ ] All tests passing

```

Append to: `{analysis_dir}/technical-spec.md`

**Verify:** Read complete file, confirm:
- All 12 sections present
- User preferences (Q1-Q10) correctly applied
- Diagrams rendered correctly
- No placeholders or TODOs

**Output:**

```text
technical-spec.md Chunk 5/5 complete: Testing + Observability + Risks
  - Lines: [COUNT]

technical-spec.md COMPLETE (5/5 chunks)
   Total diagrams: [COUNT]
   Total lines: [COUNT]

```

---

## Completion Marker

```text
═══════════════════════════════════════════════════════════
  ARTIFACT COMPLETE: TECHNICAL-SPEC.md

  Chain ID: {chain_id}
  Sections: 12
  Diagrams: {count}
  Lines: {count}

  User Preferences Applied:
    Q1 Language: {answer}
    Q2 Database: {answer}
    Q3 Message Bus: {answer}
    Q4 Package Manager: {answer}
    Q5 Deployment: {answer}
    Q6 IaC: {answer}
    Q7 Container: {answer}
    Q8 Observability: {answer}
    Q9 Security: {answer}
    Q10 Testing: {answer}
═══════════════════════════════════════════════════════════

ARTIFACT_COMPLETE:TECHNICAL_SPEC

```

---

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
