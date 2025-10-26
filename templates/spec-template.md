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

# Problem Statement

Describe the user problem and desired outcome in business language. Reference the personas and pain points driving this request.

## Assumptions

- List explicit assumptions that guided this specification. Remove any that are invalidated.

## Scope

### In Scope
- Capabilities or journeys delivered in this feature release.

### Out of Scope
- Adjacent ideas intentionally deferred or owned by other workstreams.

## Prioritized User Journeys

Each journey must be independently testable and map back to a measurable outcome.

### US-01 – [Journey title] _(Priority: P1)_
- **Narrative:** Describe the user flow end to end in plain language.
- **Value:** Explain why this journey matters most right now.
- **Independent Verification:** How to demonstrate this journey works in isolation.
- **Acceptance Criteria:**
  1. Given … When … Then …
  2. Given … When … Then …

### US-02 – [Journey title] _(Priority: P2)_
- Repeat the structure above. Add or remove journeys as needed; keep priorities unique.

## Functional Requirements

| ID | Description | Fit Criterion / Test Oracle |
|----|-------------|------------------------------|
| FR-001 | [Requirement statement] | [How to verify objectively] |
| FR-002 | [Requirement statement] | [How to verify objectively] |

Document any uncertainties inline using `[NEEDS CLARIFICATION: question]`.

## Non-Functional Requirements

| Category | Requirement | Fit Criterion |
|----------|-------------|---------------|
| Performance | [e.g., 95th percentile response ≤ 400 ms] | [Measurement approach] |
| Reliability | [e.g., Error budget ≤ 0.1%] | [Monitoring source] |
| Security | [Policy or compliance expectation] | [Verification] |

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation / Owner |
|------|--------|------------|---------------------|
| [Describe risk] | High/Med/Low | High/Med/Low | [Action plan and owner] |

## Open Questions

List outstanding items that require clarification. Use the format `[NEEDS CLARIFICATION: question]` and keep to the three highest-impact gaps.

## Glossary & Domain Invariants

Define important terminology, business rules, and invariants to keep future artifacts consistent.

## Traceability Matrix

| User Journey | Functional Requirement(s) | NFR(s) | Planned Tests |
|--------------|---------------------------|--------|---------------|
| US-01 | FR-001 | Performance | [Link to task/test placeholder] |
| US-02 | FR-00X | Security | [Link to task/test placeholder] |

## Clarifications Log

Record resolved questions with date and outcome.

| Date | Question | Decision | Impacted Sections |
|------|----------|----------|--------------------|
| 2024-01-01 | [What was asked] | [Resolution] | [Sections updated] |
