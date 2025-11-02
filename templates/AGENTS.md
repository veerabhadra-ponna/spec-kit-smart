# AI Agent Guidelines

## 1. Purpose

This document defines the behavioral and operational standards for AI coding agents participating in Spec-Driven Development.

Agents follow this guide to ensure deterministic, auditable, and high-quality contributions consistent with the project **Constitution**.

---

## 2. Core Responsibilities

* Interpret specifications in `specs/[###-feature-name]/spec.md` and related design documents as the **single source of truth**.
* Generate or modify code, documentation, and tests **strictly aligned** with those specs and the implementation plan (`specs/[###-feature-name]/plan.md`).
* Produce results that are **deterministic**, **idempotent**, and **production-ready**.
* **Never** introduce new requirements, external dependencies, or opinions not found in the spec or plan.

---

## 3. Behavioral Principles

* **Single Source of Truth:** Derive all logic and structure from the feature specification (`specs/[###-feature-name]/spec.md`), implementation plan (`specs/[###-feature-name]/plan.md`), and supporting design documents.

* **Ambiguity Protocol:** When context is missing or conflicting, emit a clarification request instead of assuming:

  ```
  CLARIFICATION NEEDED:
    - <question or gap>
    - <options/trade-offs>
    - <blocked component(s)>
  ```

* **Minimal Diffs:** Make small, reviewable, logically grouped changes.

* **Explain Rationale:** Include a concise "Why" statement mapping to spec sections (e.g., `Implements spec.md User Story 2, Scenario 1`).

* **Deterministic Output:** Same input → identical output; use fixed seeds if randomness is needed.

* **Idempotent Actions:** Re-execution must not duplicate or corrupt output.

* **Read-Only by Default:** Modify files only as directed by `specs/[###-feature-name]/tasks.md` or the implementation plan. Respect `.specify/` directory as read-only during implementation.

* **Guardrails:** Respect protected paths and project structure. Do not modify system files, configuration, or vendor dependencies unless explicitly specified.

* **Traceability:** Update commit messages and PR descriptions with summary, rationale, and references to spec sections (e.g., `specs/[###-feature-name]/spec.md lines 45-67`).

* **Compliance:** Follow Constitution principles (`.specify/memory/constitution.md`) for architecture, security, and privacy at all times.

---

## 4. Quality & Verification

* **Validation:** Run formatters, linters, and build checks automatically before committing.

* **Acceptance Testing:** Verify that all acceptance scenarios in `specs/[###-feature-name]/spec.md` have corresponding passing tests.

* **Contract Compliance:** Ensure implementations match API specifications in `specs/[###-feature-name]/contracts/` (if applicable).

* **Data Model Alignment:** Verify all code matches schemas and structures in `specs/[###-feature-name]/data-model.md` (if applicable).

* **Quickstart Verification:** Validate that scenarios in `specs/[###-feature-name]/quickstart.md` work as documented (if applicable).

* **Compilation:** Ensure all generated code compiles and loads without errors.

* **Constitution Gates:** Verify compliance with any gates specified in the "Constitution Check" section of `specs/[###-feature-name]/plan.md`.

* **Fail Fast:** Abort if build/test fails; report reason, affected component(s), and which spec requirement is blocked.

---

## 5. Collaboration Protocol

### Version Control Discipline

* Commit only after **local validation** passes.
* Group related edits into **atomic commits** that implement specific user stories or acceptance scenarios.
* Reference **feature numbers and spec sections** in commit messages (e.g., `Implement 001: User Story 1, Scenarios 1-2`).
* Work on feature branches specified in `specs/[###-feature-name]/spec.md`.

### Change Communication

* Add or update design documents in `specs/[###-feature-name]/` when design trade-offs occur.
* Document technical decisions in `specs/[###-feature-name]/research.md` with rationale and alternatives considered.
* Notify human reviewers via the **standard PR description template**, including:
  - Links to `spec.md` and `plan.md`
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
* Ensure **privacy** and **compliance** align with the project Constitution (`.specify/memory/constitution.md`) and applicable laws.

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

* **Constitutional Violations:** If the spec or implementation conflicts with Constitution principles (`.specify/memory/constitution.md`):
  - **Flag** the deviation immediately
  - Document the conflict clearly with reference to specific Constitution articles
  - If proceeding is necessary, add explicit justification to `specs/[###-feature-name]/plan.md` "Complexity Tracking" section
  - Request human decision on priority

* **Quality Failures:** If tests fail or code quality checks do not pass:
  - **Suspend** further implementation
  - Report which acceptance scenario or spec requirement is failing
  - Determine if it's a code issue or spec issue
  - If spec issue, recommend spec updates; otherwise fix the implementation

* **Technical Blockers:** If blocked by external dependencies, missing APIs, or technical limitations:
  - Document the blocker in `specs/[###-feature-name]/research.md` or as a comment in `specs/[###-feature-name]/plan.md`
  - Suggest alternative approaches or spec modifications
  - Escalate promptly to avoid delays

---

## Key Document Reference

When working on a feature, consult these documents in priority order:

1. **`.specify/memory/constitution.md`** - Project-wide immutable principles, constraints, and quality gates
2. **`specs/[###-feature-name]/spec.md`** - Feature requirements, user stories, and acceptance criteria (WHAT and WHY)
3. **`specs/[###-feature-name]/plan.md`** - Technical architecture and implementation approach (HOW)
4. **`specs/[###-feature-name]/data-model.md`** - Database schemas, entities, relationships (if applicable)
5. **`specs/[###-feature-name]/contracts/`** - API specifications (if applicable)
6. **`specs/[###-feature-name]/research.md`** - Technical decisions with rationale (if applicable)
7. **`specs/[###-feature-name]/quickstart.md`** - Validation scenarios (if applicable)
8. **`specs/[###-feature-name]/tasks.md`** - Ordered implementation tasks (if applicable)

**Templates** are available in `.specify/templates/` for creating consistent specification and design documents.

**Scripts** for project management are available in `.specify/scripts/` (e.g., updating agent context, validation).

---

*This document defines behavioral standards for AI agents working on Spec-Driven Development projects. All agents must follow these guidelines to maintain quality, consistency, and alignment with specifications.*
