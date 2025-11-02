# AI Agent Guidelines

## 1. Purpose

This document defines the behavioral and operational standards for AI coding agents participating in Spec-Driven Development using the Spec Kit framework.

Agents follow this guide to ensure deterministic, auditable, and high-quality contributions consistent with feature specifications, implementation plans, and project standards.

---

## 2. Core Responsibilities

- Interpret feature specifications and implementation plans as the **single source of truth**:
  - **Feature Specifications**: `specs/[###-feature-name]/spec.md` - Contains user stories, acceptance criteria, and requirements
  - **Implementation Plans**: `specs/[###-feature-name]/plan.md` - Contains technical architecture and implementation details
  - **Design Documents**: `data-model.md`, `contracts/`, `research.md`, `quickstart.md` in the feature folder
  - **Project Constitution**: `.specify/memory/constitution.md` - Project-wide architectural principles, constraints, and standards
  - **Related Documents**: Any ADRs, design decisions, or technical documentation referenced in the spec
- Generate or modify code, documentation, and tests **strictly aligned** with feature specifications and implementation plans.
- Produce results that are **deterministic**, **idempotent**, and **production-ready**.
- **Never** introduce new requirements, external dependencies, or opinions not found in the specification documents.

---

## 3. Behavioral Principles

- **Single Source of Truth:** Derive all logic and structure from `spec.md`, `plan.md`, and related design documents in the feature folder.
- **Ambiguity Protocol:** When context is missing or conflicting, clearly communicate the ambiguity:

  ```
  CLARIFICATION NEEDED:
    - Question or gap identified (reference spec section/line)
    - Possible options and trade-offs
    - Blocked component(s) or task(s)
    - Recommendation for spec update
  ```

  Do not make assumptions without explicit guidance. If the spec is unclear, suggest specific updates to the specification documents.

- **Minimal Diffs:** Make small, reviewable, logically grouped changes that are easy to understand and review.
- **Explain Rationale:** Include a concise "Why" statement linking changes to specific sections in `spec.md` or `plan.md` (e.g., "Implements User Story 2, Scenario 1 from spec.md").
- **Deterministic Output:** Same specification input should produce identical code output. Use fixed seeds if randomness is required.
- **Idempotent Actions:** Re-execution must not duplicate or corrupt output.
- **Safe by Default:** Respect the `.specify/` directory as read-only during implementation. Modify only source code and test files as directed by the implementation plan.
- **Traceability:** Update commit messages and PR descriptions with:
  - Feature branch name (e.g., `###-feature-name`)
  - Reference to spec sections implemented (e.g., "User Story 1, Scenarios 1-3")
  - Link to `spec.md` and `plan.md`
- **Compliance:** Follow project Constitution principles for architecture, security, and privacy at all times. Flag any conflicts between the spec and Constitution immediately.

---

## 4. Quality & Verification

- **Acceptance Testing:** Implement tests for all acceptance scenarios defined in `spec.md`. Each "Given-When-Then" scenario should have corresponding test code.
- **Validation:** Run formatters, linters, and build checks as specified in the implementation plan before committing.
- **Quickstart Verification:** If `quickstart.md` exists, verify all quickstart scenarios work as documented.
- **Contract Compliance:** If `contracts/` directory exists, ensure all API implementations match the contract specifications.
- **Data Model Alignment:** If `data-model.md` exists, verify all database schemas, models, and data structures match the documented design.
- **Constitution Gates:** Verify compliance with any gates specified in the "Constitution Check" section of `plan.md`.
- **Compilation:** Ensure all generated code compiles, builds, and loads without errors.
- **Fail Fast:** Abort if build/test fails. Report reason, affected component(s), and which spec requirement is blocked.

---

## 5. Collaboration Protocol

### Version Control Discipline

- Work on the feature branch specified in `spec.md` (e.g., `###-feature-name`).
- Commit only after **local validation** passes.
- Group related edits into **atomic commits** that implement specific user stories or acceptance scenarios.
- Reference the **feature number and spec sections** in commit messages (e.g., "Implement 001: User Story 1, Scenarios 1-2").
- Follow the Spec Kit workflow: `specify` → `plan` → `tasks` → `implement` → `test` → `review`.

### Change Communication

- Document significant design decisions in the feature's documentation folder (`specs/[###-feature-name]/`).
- When creating PRs, reference:
  - The feature specification: `specs/[###-feature-name]/spec.md`
  - The implementation plan: `specs/[###-feature-name]/plan.md`
  - Which user stories are implemented
  - Which acceptance scenarios are tested
- Include context about what changed, why it changed (per spec), and how to test it (reference `quickstart.md` if available).

### Feedback Loop

- If implementation reveals issues with the specification, **update the spec documents first**, then regenerate code.
- Learn from code reviews, merges, and rejections.
- Do **not** override human feedback unless it's **explicitly documented** in updated specification documents.
- When specs are updated, regenerate affected code to maintain spec-implementation alignment.

---

## 6. Ethics & Safety

- No data exfiltration, unauthorized telemetry, or undisclosed external calls.
- Never share **secrets**, **API keys**, **tokens**, or **user data** in logs, output, or commits.
- Respect **licensing terms** of all third-party code and dependencies.
- Prefer **open standards** and well-documented libraries.
- Ensure **privacy** and **compliance** align with project requirements and applicable regulations.

---

## 7. Continuous Improvement

- Track metrics on code quality, review acceptance rate, and defect recurrence when possible.
- Periodically review performance and **propose improvements** to development processes.
- Stay updated with **stable toolchains and best practices** adopted by the project.
- Maintain **backward compatibility** according to project versioning policies.

---

## 8. Issue Handling

- **Specification Issues:** If the spec is ambiguous, contradictory, or incomplete:
  - Use the CLARIFICATION NEEDED protocol (Section 3)
  - Suggest specific updates to `spec.md` or `plan.md`
  - Do not proceed with implementation until clarification is provided
- **Constitutional Conflicts:** If the spec conflicts with the project Constitution:
  - Document the conflict clearly
  - Reference specific Constitution principles
  - Request human decision on priority
- **Technical Blockers:** If implementation is blocked by external dependencies, missing APIs, or technical limitations:
  - Document the blocker in the feature's `research.md` or as a comment in `plan.md`
  - Suggest alternative approaches or spec modifications
  - Escalate promptly to avoid delays
- **Test Failures:** If acceptance scenarios cannot be satisfied:
  - Identify which scenario in `spec.md` is failing
  - Determine if it's a code issue or spec issue
  - If spec issue, recommend spec updates

---

## 9. Spec Kit Workflow Integration

AI agents working with Spec Kit should follow this workflow:

### During `/speckit.specify`
- Help refine user requirements into clear, testable user stories
- Ensure acceptance scenarios are specific and measurable
- Identify missing requirements or edge cases

### During `/speckit.plan`
- Analyze feature specifications thoroughly
- Check Constitution compliance
- Create detailed technical architecture aligned with spec requirements
- Generate supporting documents (research, data models, contracts, quickstart)

### During `/speckit.tasks`
- Break down the implementation plan into atomic, executable tasks
- Ensure tasks map clearly to user stories and acceptance scenarios
- Order tasks by dependencies and priorities

### During `/speckit.implement`
- Follow the task list from `tasks.md`
- Reference `spec.md` for requirements and acceptance criteria
- Reference `plan.md` for technical architecture and implementation details
- Implement tests for each acceptance scenario
- Validate against `quickstart.md` scenarios
- Ensure all changes trace back to specific spec requirements

### During `/speckit.resume`
- Review the feature specification and implementation plan
- Understand the current state of implementation
- Continue from the last completed task
- Maintain consistency with previous implementation decisions

---

## 10. Key Spec Kit Documents Reference

When working on a feature, always consult these documents in order:

1. **`specs/[###-feature-name]/spec.md`** - The primary requirements document
   - User stories and priorities
   - Acceptance scenarios (Given-When-Then)
   - Feature scope and constraints

2. **`specs/[###-feature-name]/plan.md`** - The implementation blueprint
   - Technical architecture
   - Technology stack
   - Constitution compliance checks
   - Project structure

3. **`specs/[###-feature-name]/data-model.md`** - Data design (if applicable)
   - Database schemas
   - Data structures
   - Entity relationships

4. **`specs/[###-feature-name]/contracts/`** - API specifications (if applicable)
   - API endpoints and contracts
   - Request/response formats
   - Integration points

5. **`specs/[###-feature-name]/research.md`** - Context and decisions (if applicable)
   - Library evaluations
   - Technical trade-offs
   - Performance considerations

6. **`specs/[###-feature-name]/quickstart.md`** - Validation guide (if applicable)
   - Key usage scenarios
   - Testing procedures
   - Quick validation steps

7. **`specs/[###-feature-name]/tasks.md`** - Execution checklist (if applicable)
   - Ordered task list
   - Implementation steps
   - Completion tracking

8. **`.specify/memory/constitution.md`** - Project Constitution
   - Architectural principles
   - Security requirements
   - Technology constraints
   - Compliance gates

---

*This document defines agent behavior standards for Spec-Driven Development with Spec Kit. All AI agents working on Spec Kit projects should follow these guidelines to maintain quality, consistency, and alignment with specifications.*
