# AI Agent Guidelines

## 1. Purpose

This document defines the behavioral and operational standards for AI coding agents participating in Spec-Driven Development.

Agents follow this guide to ensure deterministic, auditable, and high-quality contributions consistent with project specifications and the **Constitution** (`.specify/memory/constitution.md`).

---

## 2. Core Responsibilities

* Interpret specifications and design documents as the **single source of truth**:
  - `.specify/memory/constitution.md` - Project principles and constraints
  - `specs/[###-feature-name]/spec.md` - Feature requirements and acceptance criteria
  - `specs/[###-feature-name]/plan.md` - Implementation architecture
  - `specs/[###-feature-name]/` - Supporting design documents (data-model, contracts, research, quickstart, tasks)

* Generate or modify code, documentation, and tests **strictly aligned** with these specifications.
* Produce results that are **deterministic**, **idempotent**, and **production-ready**.
* **Never** introduce new requirements, external dependencies, or opinions not found in the specifications.

---

## 3. Behavioral Principles

* **Ambiguity Protocol:** When context is missing or conflicting, emit a clarification request instead of assuming:

  ```
  CLARIFICATION NEEDED:
    - <question or gap>
    - <options/trade-offs>
    - <blocked component(s)>
  ```

* **Minimal Diffs:** Make small, reviewable, logically grouped changes.

* **Explain Rationale:** Include a concise "Why" statement mapping to spec sections (e.g., `Implements User Story 2, Scenario 1 from spec.md`).

* **Deterministic Output:** Same input → identical output; use fixed seeds if randomness is needed.

* **Idempotent Actions:** Re-execution must not duplicate or corrupt output.

* **Read-Only by Default:** Modify files only as directed by the implementation plan. Respect `.specify/` directory as read-only during implementation.

* **Guardrails:** Respect protected paths and project structure. Do not modify system files, configuration, or vendor dependencies unless explicitly specified.

* **Traceability:** Update commit messages and PR descriptions with summary, rationale, and specification references.

* **Compliance:** Follow Constitution principles for architecture, security, and privacy at all times.

---

## 4. Quality & Verification

* **Validation:** Run formatters, linters, and build checks automatically before committing.

* **Acceptance Testing:** Verify that all acceptance scenarios in the feature spec have corresponding passing tests.

* **Contract Compliance:** Ensure implementations match API specifications (if `contracts/` exists).

* **Data Model Alignment:** Verify all code matches documented schemas and structures (if `data-model.md` exists).

* **Quickstart Verification:** Validate documented scenarios work as expected (if `quickstart.md` exists).

* **Constitution Gates:** Verify compliance with gates specified in the "Constitution Check" section of the implementation plan.

* **Compilation:** Ensure all generated code compiles and loads without errors.

* **Fail Fast:** Abort if build/test fails; report reason, affected component(s), and which spec requirement is blocked.

---

## 5. Collaboration Protocol

### Version Control Discipline

* Commit only after **local validation** passes.
* Group related edits into **atomic commits** that implement specific user stories or acceptance scenarios.
* Reference **feature numbers and spec sections** in commit messages (e.g., `Implement 001: User Story 1, Scenarios 1-2`).
* Work on feature branches as specified in the feature specification.

### Change Communication

* Add or update design documents in the feature directory when design trade-offs occur.
* Document technical decisions with rationale and alternatives considered.
* Notify human reviewers via the **standard PR description template**, including:
  - Links to feature specification and implementation plan
  - Which user stories and acceptance scenarios are implemented
  - Which tests validate the implementation

### Feedback Loop

* If implementation reveals spec issues, **update spec documents first**, then regenerate code.
* Learn from merges and rejections; **adjust approach** accordingly.
* Do **not** override manual feedback unless it's **reflected in updated specification documents**.
* When specs are updated, regenerate affected code to maintain spec-implementation alignment.

---

## 6. Ethics & Safety

* No data exfiltration, unauthorized telemetry, or undisclosed external calls.
* Never share **secrets**, **API keys**, **tokens**, or **user data** in logs, output, or commits.
* Respect **licensing terms** of all third-party code.
* Prefer **open standards**; avoid closed or non-redistributable components.
* Ensure **privacy** and **compliance** align with project requirements and applicable laws.

---

## 7. Continuous Improvement

* Track metrics on code quality, review acceptance rate, and defect recurrence when possible.
* Periodically review performance and **propose improvements** to specifications and development processes.
* Adopt newer **stable toolchains and best practices** once validated by the project team.
* Maintain **backward compatibility** according to project versioning policies.

---

## 8. Violation Handling

* **Specification Violations:** If the spec is ambiguous, contradictory, or incomplete:
  - Use the CLARIFICATION NEEDED protocol (Section 3)
  - Do not proceed with implementation until clarification is provided
  - Suggest specific updates to specification documents

* **Constitutional Violations:** If the spec or implementation conflicts with Constitution principles:
  - **Flag** the deviation immediately
  - Document the conflict clearly with reference to specific Constitution articles
  - If proceeding is necessary, add explicit justification to the "Complexity Tracking" section of the implementation plan
  - Request human decision on priority

* **Quality Failures:** If tests fail or code quality checks do not pass:
  - **Suspend** further implementation
  - Report which acceptance scenario or spec requirement is failing
  - Determine if it's a code issue or spec issue
  - If spec issue, recommend spec updates; otherwise fix the implementation

* **Technical Blockers:** If blocked by external dependencies, missing APIs, or technical limitations:
  - Document the blocker in the research document or as a comment in the implementation plan
  - Suggest alternative approaches or spec modifications
  - Escalate promptly to avoid delays

---

## Document Structure Reference

Projects using Spec-Driven Development have this structure:

```
project-root/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # Project principles and constraints
│   ├── templates/                    # Spec, plan, and checklist templates
│   └── scripts/                      # Project management scripts
│
└── specs/
    └── [###-feature-name]/           # Feature-specific directory
        ├── spec.md                   # Requirements and acceptance criteria
        ├── plan.md                   # Implementation architecture
        ├── data-model.md             # Database schemas (if applicable)
        ├── contracts/                # API specifications (if applicable)
        ├── research.md               # Technical decisions (if applicable)
        ├── quickstart.md             # Validation scenarios (if applicable)
        └── tasks.md                  # Implementation tasks (if applicable)
```

**Consult documents in priority order:**

1. **Constitution** - Project-wide immutable principles
2. **Feature Specification** - Requirements, user stories, acceptance criteria (WHAT and WHY)
3. **Implementation Plan** - Technical architecture and approach (HOW)
4. **Supporting Documents** - Data models, contracts, research, quickstart, tasks (as applicable)

---

*This document defines behavioral standards for AI agents working on Spec-Driven Development projects. All agents must follow these guidelines to maintain quality, consistency, and alignment with specifications.*
