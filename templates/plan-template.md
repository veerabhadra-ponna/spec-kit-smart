---
feature_id: 000-example-feature
title: "[Replace with feature title]"
status: Draft
branch: 000-example-feature
semver: 0.1.0
created_at: 2024-01-01
source_commit: HEAD
generator: spec-kit
constitution_version: 1.0.0
---

# Implementation Plan Overview

Summarize the architectural direction and the value delivered in this increment.

## Constitution Gate Summary

| Gate | Description | Status | Notes |
|------|-------------|--------|-------|
| G1 | Constitution compliance | Pending | Reference rule IDs |
| G2 | Clarifications resolved | Pending | Cite unanswered questions |
| G3 | High risks mitigated | Pending | Link to Risk Register |

## Technical Context

| Field | Decision |
|-------|----------|
| Language/Version | [e.g., Python 3.12 or NEEDS CLARIFICATION] |
| Primary Dependencies | [Frameworks/libraries] |
| Storage | [Database/filesystem or N/A] |
| Testing Strategy | [Test frameworks & cadence] |
| Target Platform | [Runtime/OS/devices] |
| Project Type | [Monolith/service/mobile/etc.] |
| Performance Goals | [Quantified targets] |
| Constraints | [Latency, compliance, deployment] |

## Phase Breakdown & Exit Criteria

### Phase 0 – Research & Clarifications
- Objectives
- Exit Criteria: [All clarifications resolved, research captured]
- Artifacts: `research.md`

### Phase 1 – System Design
- Objectives
- Exit Criteria: [Design decisions recorded, risks mitigated]
- Artifacts: `data-model.md`, `contracts/`, `quickstart.md`

### Phase 2 – Implementation Planning
- Objectives
- Exit Criteria: [All blockers addressed, tasks ready]
- Downstream Artifact: `tasks.md`

## Architecture & Structure Decisions

Document key structural choices and rationale. Create ADR stubs if decisions are contentious.

```text
[Proposed repository layout copied from research]
```

## Decision Log (ADR Stubs)

| ADR ID | Title | Status | Summary |
|--------|-------|--------|---------|
| ADR-001 | [Decision] | Proposed | [One-sentence summary] |

## Risk Register

| ID | Risk | Impact | Likelihood | Mitigation | Owner | Due |
|----|------|--------|------------|------------|-------|-----|
| R-01 | [Describe risk] | High | Medium | [Mitigation action] | [Name/Role] | [Date] |

## Dependencies

- External systems or teams required.
- Contracts or approvals needed before build starts.

## Clarification Outcomes

Summarize how open questions from the spec were resolved. Link back to the Clarifications Log.

## Next Steps

List actions required before `/speckit.tasks` (e.g., update agent context, schedule reviews).
