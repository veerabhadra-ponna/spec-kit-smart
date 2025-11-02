# AI Agent Guidelines for Spec-Driven Development

## Purpose

This document defines behavioral and operational standards for AI coding agents working with the Spec Kit framework. Agents must follow these guidelines to ensure deterministic, auditable, and specification-aligned contributions.

**Core Principle**: Specifications are the primary artifact. Code is generated output that serves the specification.

---

## 1. Document Hierarchy (Source of Truth)

All implementation decisions derive from these documents **in priority order**:

### Tier 1: Project Constitution
- **`.specify/memory/constitution.md`** - Immutable architectural principles, constraints, and quality gates
- Violations require explicit justification in `plan.md`

### Tier 2: Feature Specification
- **`specs/[###-feature-name]/spec.md`** - Requirements, user stories, acceptance criteria
- Contains WHAT users need and WHY (not HOW to build it)
- User stories must be independently testable and prioritized (P1, P2, P3...)

### Tier 3: Implementation Plan & Design
- **`specs/[###-feature-name]/plan.md`** - Technical architecture and implementation approach
- **`specs/[###-feature-name]/data-model.md`** - Database schemas, entities, relationships
- **`specs/[###-feature-name]/contracts/`** - API specifications (OpenAPI/GraphQL)
- **`specs/[###-feature-name]/research.md`** - Technical decisions with rationale (Decision → Why → Alternatives Rejected)
- **`specs/[###-feature-name]/quickstart.md`** - Validation scenarios and smoke tests

### Tier 4: Execution Plan
- **`specs/[###-feature-name]/tasks.md`** - Ordered, atomic implementation tasks
- Format: `- [ ] [T###] [P?] [US#] Task description (file: path/to/file.ext)`
- Mark `[x]` **immediately** after each task completion (critical for resumption)

---

## 2. Workflow Commands

AI agents participate in these commands (invoke via `/speckit.<command>`):

| Command | Purpose | Input | Output | Agent Role |
|---------|---------|-------|--------|------------|
| **specify** | Create feature spec | User description | `spec.md` + checklist | Requirements analyst |
| **clarify** | Resolve ambiguities | `spec.md` | Updated `spec.md` | Business analyst |
| **plan** | Design architecture | `spec.md` + constitution | `plan.md` + design docs | Senior architect |
| **analyze** | Quality audit | spec/plan/tasks | Analysis report (read-only) | Technical auditor |
| **tasks** | Generate task list | `plan.md` + `spec.md` | `tasks.md` | Tech lead |
| **implement** | Execute tasks | `tasks.md` + all docs | Working code + tests | Senior engineer |
| **resume** | Restore context | `.speckit-state.json` or feature ID | Full context reload | Context specialist |
| **checklist** | Validate requirements | `spec.md` + context | Quality checklist | QA engineer |
| **constitution** | Update principles | Current constitution | Updated constitution | Governance architect |
| **orchestrate** | Manage workflow | Feature description | Coordinated execution + state | Engineering manager |

---

## 3. Critical Implementation Rules

### Task Execution Protocol

**RULE #1**: Mark `[x]` **immediately** after completing each task in `tasks.md`
- Not after batch completion
- Required for `/speckit.resume` to work correctly
- Update the file, don't just report completion

**RULE #2**: Follow phase order strictly
```
Phase 1: Setup (project initialization)
  ↓
Phase 2: Foundational (BLOCKS all user stories - complete FIRST)
  ↓
Phase 3+: User Story Phases (can be parallelized)
  ↓
Final: Polish & Cross-cutting Concerns
```
- **NEVER** implement user stories before completing Phase 2 (Foundational)
- Phase 2 tasks are dependencies for all feature work

**RULE #3**: Independent User Story Implementation
- Each user story (P1, P2, P3...) must be independently testable
- Implementing just P1 should yield a working MVP
- P2 should add value without breaking P1
- This enables incremental delivery and parallel development

### Parallel Execution Rules

Tasks marked `[P]` can run in parallel **only if**:
- They modify different files
- They have no dependencies on incomplete tasks
- They belong to different user stories

Within a user story, dependencies typically flow:
```
Models/Entities → Services/Logic → Controllers/Endpoints → Tests
```

### Acceptance Testing Requirements

For every acceptance scenario in `spec.md`:
```
Given [context]
When [action]
Then [outcome]
```

There **must be** corresponding test code that:
- Sets up the Given context
- Executes the When action
- Asserts the Then outcome

Tests are NOT extras - they are **implementations of acceptance scenarios**.

### Constitution Compliance

If the specification or plan violates Constitution principles:

1. **Identify the violation** (reference specific Constitution article)
2. **Document in `plan.md`'s "Complexity Tracking" table**:
   ```
   | Violation | Why Needed | Simpler Alternative Rejected |
   |-----------|------------|------------------------------|
   | Anti-Abstraction: Using ORM | Complex queries needed | Raw SQL rejected: maintenance burden |
   ```
3. **Request explicit human approval** before proceeding

### Template Adherence

**ALWAYS** load document structures from `.specify/templates/`:
- `spec-template.md`
- `plan-template.md`
- `tasks-template.md`
- `checklist-template.md`

**NEVER** hallucinate document structure. Templates enforce quality and consistency.

---

## 4. Quality Verification Checklist

Before marking implementation complete:

- [ ] All `[ ]` tasks in `tasks.md` marked `[x]`
- [ ] All acceptance scenarios have passing tests
- [ ] Code matches `data-model.md` schemas (if applicable)
- [ ] APIs match `contracts/` specifications (if applicable)
- [ ] All `quickstart.md` scenarios work as documented (if applicable)
- [ ] Constitution gates passed (see `plan.md` "Constitution Check" section)
- [ ] Formatters, linters, and build checks pass
- [ ] No secrets, tokens, or credentials in code or logs
- [ ] All changes traced to specific `spec.md` requirements

---

## 5. Ambiguity & Issue Resolution

### When Specification is Unclear

**DO NOT** make assumptions. Instead:

```
CLARIFICATION NEEDED:
  Section: [spec.md section/line reference]
  Question: [specific gap or contradiction]
  Options:
    A) [option with pros/cons]
    B) [option with pros/cons]
  Recommendation: [preferred option with rationale]
  Blocked: [tasks/components that cannot proceed]
```

**DO NOT** proceed with implementation until clarification is provided.

### When Constitution Conflicts with Spec

1. Document the conflict clearly
2. Reference specific Constitution article
3. Request human decision on priority
4. If proceeding with violation, add justification to `plan.md`

### When Implementation Reveals Spec Issues

1. **Update spec documents FIRST**
2. Then regenerate affected code
3. Maintain spec-implementation alignment at all times

---

## 6. State Management & Resumption

The `/speckit.orchestrate` command creates `.speckit-state.json` to enable multi-session workflows.

**For Resumption**:
- `/speckit.resume` can restore full context with zero chat history
- Depends on accurate task marking in `tasks.md`
- Finds first unchecked `[ ]` task and continues from there

**State Integrity**:
- Mark tasks `[x]` immediately upon completion
- Never batch multiple task completions before marking
- State file enables seamless cross-session continuation

---

## 7. Checklists as "Unit Tests for Requirements"

Quality checklists (in `specs/[###-feature-name]/checklists/`) validate **requirement quality**, not implementation correctness.

**Purpose**: Ensure specifications are clear, complete, measurable, and consistent **before** implementation begins.

**Examples**:
- ✅ "Each user story has at least one acceptance scenario"
- ✅ "Success criteria use measurable metrics (not 'fast' but '<200ms p95')"
- ✅ "API requirements specify error responses (not just happy path)"

**NOT**:
- ❌ "API returns correct status codes" (that's implementation testing)

---

## 8. Version Control & Traceability

### Commit Messages
```
Implement [###-feature-name]: [User Story #], Scenarios [#-#]

- Implements spec.md User Story 2, Acceptance Scenarios 1-3
- Adds [component] per plan.md Section [X]
- Tests validate Given-When-Then scenarios

Refs: specs/[###-feature-name]/spec.md (lines XX-YY)
```

### Pull Request Description
```
## Feature
[###-feature-name] - [brief title]

## Specification
- Spec: specs/[###-feature-name]/spec.md
- Plan: specs/[###-feature-name]/plan.md

## Implemented
- ✅ User Story 1 (P1) - All acceptance scenarios
- ✅ User Story 2 (P1) - Scenarios 1-3
- ⏳ User Story 2 (P1) - Scenario 4 (blocked: awaiting API key)

## Testing
- All acceptance scenarios have passing tests
- Quickstart scenarios verified (see quickstart.md)
- Constitution gates: ✅ Passed

## How to Test
[Reference quickstart.md or provide specific steps]
```

---

## 9. Ethics & Safety

- **NO** data exfiltration, unauthorized telemetry, or undisclosed external calls
- **NEVER** commit secrets, API keys, tokens, credentials, or user data
- Respect licensing terms of all dependencies
- Prefer open standards and well-documented libraries
- Ensure privacy and compliance with project requirements and regulations

---

## 10. Quick Reference

### Execution Order
```
1. /speckit.constitution (optional: set project principles)
2. /speckit.specify <description>
3. /speckit.clarify (optional: if ambiguities exist)
4. /speckit.plan
5. /speckit.analyze (optional: quality gate)
6. /speckit.tasks
7. /speckit.implement
8. /speckit.resume (if interrupted)
```

### Document Reading Order During Implementation
```
1. constitution.md - Non-negotiable principles
2. spec.md - WHAT to build and WHY
3. plan.md - HOW to build (architecture)
4. data-model.md - Data structures
5. contracts/ - API specifications
6. research.md - Technical decisions & rationale
7. quickstart.md - Validation scenarios
8. tasks.md - Execution order
```

### Critical "DO NOT" Rules
- ❌ Implement user stories before Phase 2 (Foundational) tasks
- ❌ Batch task completions (mark `[x]` immediately per task)
- ❌ Make assumptions when spec is unclear (use CLARIFICATION protocol)
- ❌ Violate Constitution without documented justification
- ❌ Hallucinate document structures (load from templates)
- ❌ Commit secrets, credentials, or tokens
- ❌ Proceed with implementation when checklists are incomplete (unless approved)

### Critical "MUST DO" Rules
- ✅ Mark `[x]` in tasks.md immediately after each task completion
- ✅ Complete Phase 2 (Foundational) before any user story work
- ✅ Write tests for every acceptance scenario (Given-When-Then)
- ✅ Update spec documents first if implementation reveals issues
- ✅ Load document structures from `.specify/templates/`
- ✅ Trace all changes to specific spec.md requirements
- ✅ Validate against quickstart.md scenarios if present
- ✅ Check Constitution gates and justify violations explicitly

---

## Appendix: Research Document Structure

When documenting technical decisions in `research.md`, use this format:

```markdown
## Decision: [Topic]

**Chosen**: [Selected option]

**Rationale**: [Why this option]

**Alternatives Considered**:
- [Option A]: Rejected because [reason]
- [Option B]: Rejected because [reason]

**Trade-offs**: [Accepted limitations or costs]

**References**: [Links to docs, benchmarks, discussions]
```

This structured format ensures decisions are auditable and reversible if context changes.

---

*This document is the definitive guide for AI agent behavior in Spec-Driven Development projects using Spec Kit. All agents must internalize and honor these standards to maintain quality, consistency, and specification alignment.*
