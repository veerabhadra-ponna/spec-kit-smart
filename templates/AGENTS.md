# AI Agent Guidelines

## 1. Purpose

This document defines behavioral and operational standards for AI coding agents participating in Spec-Driven Development using the Spec Kit framework.

Agents MUST follow these guidelines to ensure deterministic, auditable, and high-quality contributions aligned with project specifications and the Constitution.

**Keywords:** This document uses RFC 2119 terminology:

* **MUST** / **MUST NOT** = Mandatory requirement
* **SHOULD** / **SHOULD NOT** = Recommended best practice
* **MAY** = Optional capability

---

## 2. Quick Reference

### Critical DO Rules

✅ **MUST** Stop and emit `CLARIFICATION NEEDED` when spec is ambiguous  
✅ **MUST** Follow Constitution principles at all times  
✅ **MUST** Mark tasks `[x]` in `tasks.md` immediately after completion  
✅ **MUST** Run formatters, linters, and tests before committing  
✅ **MUST** Update spec documents first if implementation reveals issues

### Critical DON'T Rules

❌ **MUST NOT** commit secrets, API keys, tokens, or credentials  
❌ **MUST NOT** modify `.specify/` directory during implementation  
❌ **MUST NOT** introduce requirements not in specifications  
❌ **MUST NOT** proceed with implementation when spec is unclear  
❌ **MUST NOT** override human feedback without updated spec

### When Stuck

1. **Ambiguous Spec** → Emit `CLARIFICATION NEEDED` (see Section 5.1)
2. **Test Failure** → Report which acceptance scenario failed (see Section 7.3)
3. **Constitutional Conflict** → Flag immediately, request human decision (see Section 7.2)
4. **Technical Blocker** → Document in `research.md`, suggest alternatives (see Section 7.4)

---

## 3. Document Structure & Priority

### Project Structure

Projects using Spec-Driven Development have this structure:

```text
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

### Document Priority & Conflict Resolution

When documents conflict, apply this priority order (highest to lowest):

1. **Constitution** (`.specify/memory/constitution.md`) - Immutable project principles
   * *Example:* Constitution says "no ORMs" but spec suggests using one → Constitution wins
2. **Feature Specification** (`specs/[###-feature-name]/spec.md`) - WHAT and WHY
   * *Example:* Spec says "CSV export" but plan says "JSON only" → Spec wins
3. **Implementation Plan** (`specs/[###-feature-name]/plan.md`) - HOW
   * *Example:* Plan specifies library X but you prefer Y → Plan wins
4. **Supporting Documents** - Data models, contracts, research, quickstart, tasks
   * *Example:* Task says "file A" but data-model references "file B" → Clarify with human

**Conflict Resolution Protocol:**

If documents conflict at the same priority level:

1. **STOP** implementation immediately
2. Emit `CLARIFICATION NEEDED` with references to conflicting sections
3. **DO NOT** make assumptions or "best guesses"
4. Wait for human clarification and spec update

### Workflow Commands

Agents interact with Spec Kit through these commands:

| Command | Creates | Description |
|---------|---------|-------------|
| `/speckit.specify` | `spec.md` | Create feature specification from description |
| `/speckit.clarify` | Updated `spec.md` | Resolve ambiguities in specification |
| `/speckit.plan` | `plan.md` + design docs | Generate implementation architecture |
| `/speckit.tasks` | `tasks.md` | Generate ordered task list from plan |
| `/speckit.implement` | Source code + tests | Execute tasks and write code |
| `/speckit.resume` | Restored context | Resume from saved state or tasks.md |

*For detailed workflow information, see `spec-driven.md` in project root.*

---

## 4. Core Responsibilities

Agents MUST interpret specifications as the **single source of truth** and produce deterministic, production-ready results.

### 4.1 Specification Interpretation

* **MUST** read all documents in priority order (Section 3.2) before starting implementation
* **MUST** derive all logic and structure from specifications only
* **MUST NOT** introduce requirements, dependencies, or opinions not found in specs
* **SHOULD** cross-reference between spec.md, plan.md, and supporting documents for consistency

### 4.2 Code Generation Standards

* **MUST** generate code that is:
  * **Deterministic** - Same spec input → identical code output (use fixed seeds if randomness needed)
  * **Idempotent** - Re-execution does not duplicate or corrupt output
  * **Production-ready** - Compiles, passes tests, follows project conventions
* **MUST** align all code with specifications strictly

### 4.3 Output Requirements

* **MUST** produce all artifacts specified in implementation plan
* **MUST** include tests for every acceptance scenario
* **SHOULD** follow project coding standards and style guides

---

## 5. Behavioral Principles

### 5.1 Ambiguity Protocol

**When context is missing or conflicting, agents MUST emit a clarification request:**

```text
CLARIFICATION NEEDED:
  Document: specs/[###-feature-name]/spec.md (line 45)
  Question: User Story 2 mentions "real-time updates" but doesn't specify latency requirement
  Options:
    A) <100ms (WebSocket) - Higher complexity, better UX
    B) <5s (polling) - Lower complexity, acceptable UX
  Recommendation: Option B (aligns with Constitution Article VII: Simplicity)
  Blocked Tasks: T015, T016, T017 (notification system implementation)
```

**Good Example:**

```text
✅ Agent encounters "fast response time" → Emits CLARIFICATION with options
✅ Waits for human to update spec.md with specific SLA
✅ Resumes after spec updated with "<200ms p95 latency"
```

**Bad Example:**

```text
❌ Agent assumes "fast = 100ms" without asking
❌ Implements complex caching system not in spec
❌ Violates Constitution simplicity principle
```

### 5.2 Minimal Changes

**MUST** make small, reviewable, logically grouped changes.

**Definition of "Small":**

* Single user story or acceptance scenario per commit
* Modify 1-5 files per commit (exception: refactoring)
* <300 lines changed per commit (exception: generated code, data migrations)

**Good Example:**

```text
✅ Commit 1: Implement User Story 1, Scenario 1 (3 files, 87 lines)
✅ Commit 2: Implement User Story 1, Scenario 2 (2 files, 45 lines)
```

**Bad Example:**

```text
❌ Commit 1: Implement all 5 user stories (47 files, 3,421 lines)
```

### 5.3 Rationale Documentation

**MUST** include "Why" statements linking to specification sections.

**Commit Message Format:**

```text
Implement [###-feature-name]: User Story 2, Scenario 1

- Adds CSV export endpoint per spec.md lines 67-72
- Implements validation per plan.md Section 4.2
- Tests cover acceptance scenario: "Given valid data..."

Refs: specs/[###-feature-name]/spec.md (User Story 2)
```

**Code Comment Format:**

```python
# Implements spec.md User Story 2, Scenario 1: CSV export
# Uses streaming to handle large datasets (plan.md Section 3.4)
def export_to_csv(data):
    ...
```

### 5.4 Read-Only Defaults

**MUST** treat `.specify/` directory as read-only during implementation.

**Allowed Modifications:**

* Source code directories
* Test directories
* Build/config files (if specified in plan)

**Prohibited Modifications:**

* `.specify/memory/constitution.md`
* `.specify/templates/*`
* `.specify/scripts/*`
* `specs/[###-feature-name]/*.md` (except under human direction)

### 5.5 Guardrails

**MUST** respect protected paths and project structure.

**Protected Paths (MUST NOT modify):**

* `/data/` - Production data
* `/config/*.production.*` - Production configs
* `/vendor/` or `/node_modules/` - Dependencies
* `.git/` - Version control
* System files (e.g., `/etc/`, registry on Windows)

**Exception:** Changes explicitly directed by implementation plan with justification.

### 5.6 Traceability

**MUST** update commit messages and PR descriptions with specification references.

**PR Description Template:**

```markdown
## Feature

[###-feature-name] - [brief title]

## Specification

- Spec: specs/[###-feature-name]/spec.md
- Plan: specs/[###-feature-name]/plan.md

## Implementation Status

- ✅ User Story 1 (P1) - Scenarios 1-3 complete, all tests passing
- ✅ User Story 2 (P1) - Scenarios 1-2 complete, all tests passing
- ⏳ User Story 2 (P1) - Scenario 3 blocked: awaiting API key (see blocker comment)

## Constitution Compliance

- ✅ Library-First: Implemented as standalone library
- ✅ CLI Interface: Added CLI with text I/O
- ✅ Test-First: 47 tests, 94% coverage
- ⚠️  Simplicity: Using 4 projects (violates Article VII limit of 3)
      Justification: See plan.md "Complexity Tracking" table

## Acceptance Testing

All Given-When-Then scenarios have corresponding passing tests.
See: tests/acceptance/user_story_1_test.py

## How to Test

See specs/[###-feature-name]/quickstart.md for validation steps.
```

### 5.7 Compliance

**MUST** follow Constitution principles for architecture, security, and privacy at all times.

If Constitution conflicts with feature requirements:

1. **STOP** implementation
2. **FLAG** the conflict (see Section 7.2)
3. **DO NOT** proceed without explicit human decision

---

## 6. Quality & Verification

### 6.1 Pre-Commit Validation

**MUST** run before every commit:

* Code formatters (e.g., black, prettier, rustfmt)
* Linters (e.g., pylint, eslint, clippy)
* Type checkers (e.g., mypy, TypeScript, Flow)
* Build verification (code compiles without errors)

**WHERE:** Run locally in agent environment  
**WHEN:** Before `git commit`  
**HOW:** Execute via project-defined pre-commit hooks or CI scripts

### 6.2 Acceptance Testing

**MUST** verify all acceptance scenarios have corresponding passing tests.

**For each scenario in spec.md:**

```text
Given [context]
When [action]
Then [outcome]
```

**There MUST be test code that:**

1. Sets up the Given context
2. Executes the When action
3. Asserts the Then outcome

**Example Mapping:**

```text
spec.md Line 45: "Given valid CSV data, When export requested, Then file downloads"
         ↓
test_export.py:test_valid_csv_export()
  - setUp: creates valid CSV test data
  - action: calls export_to_csv()
  - assert: verifies file content and headers
```

### 6.3 Contract Compliance

**MUST** ensure implementations match API specifications (if `contracts/` exists).

**Verification Steps:**

1. Compare implemented endpoints to contract definitions
2. Validate request/response schemas match exactly
3. Test error responses match contract specifications
4. Verify authentication/authorization as specified

**Tool Recommendations:** OpenAPI validators, GraphQL schema validators

### 6.4 Data Model Alignment

**MUST** verify code matches schemas in `data-model.md` (if applicable).

**Verification:**

* Database migrations match documented schemas
* Model classes match entity definitions
* Validation rules match constraints
* Relationships match documented cardinalities

### 6.5 Quickstart Verification

**MUST** validate documented scenarios work (if `quickstart.md` exists).

**Process:**

1. Follow quickstart steps exactly as documented
2. Verify all examples produce expected output
3. Test edge cases mentioned in quickstart
4. Ensure setup instructions are complete

### 6.6 Constitution Gates

**MUST** verify compliance with gates in "Constitution Check" section of `plan.md`.

**Common Gates:**

* **Library-First Gate** - Feature implemented as standalone library
* **CLI Interface Gate** - Library exposes CLI with text I/O
* **Test-First Gate** - Tests written before implementation
* **Simplicity Gate** - Maximum 3 projects/modules
* **Anti-Abstraction Gate** - Uses framework directly, no wrapper layers
* **Integration-First Gate** - Real databases (not mocks), contract tests mandatory

**Gate Failure = BLOCKER**: Implementation MUST NOT proceed if any gate fails without explicit justification in plan.md "Complexity Tracking" table.

### 6.7 Fail Fast

**MUST** abort if build/test fails.

**Abort Procedure:**

1. **STOP** all implementation work immediately
2. **REPORT** to console/log with:
   * Which test/build failed
   * Error message and stack trace
   * Which acceptance scenario or spec requirement is blocked
   * Which tasks in tasks.md are affected
3. **UPDATE** tasks.md: Mark failed task with `[F]` (Failed) instead of `[x]`
4. **EMIT** issue report (see Section 7.3)
5. **WAIT** for human intervention

**WHERE to Report:**

* Console output (for interactive sessions)
* CI log (for automated runs)
* tasks.md comments (for async workflows)

**Example Report:**

```text
❌ BUILD FAILED

Test: tests/acceptance/test_user_story_2.py::test_csv_export
Error: AssertionError: Expected 3 columns, got 2
Blocked Spec: specs/[###-feature-name]/spec.md User Story 2, Scenario 1
Blocked Tasks: T015 [F], T016, T017

Root Cause: data-model.md specifies 3 fields but implementation only exports 2

Action Required: Review data-model.md vs spec.md for field list discrepancy
```

---

## 7. Violation Handling & Recovery

### 7.1 Specification Violations

**Trigger:** Spec is ambiguous, contradictory, or incomplete

**Response:**

1. **STOP** implementation immediately
2. **EMIT** `CLARIFICATION NEEDED` (see Section 5.1 format)
3. **DO NOT** make assumptions or proceed with "best guess"
4. **WAIT** for human response

**Recovery Process:**

1. Human updates `specs/[###-feature-name]/spec.md` with clarification
2. Human responds with "CLARIFICATION PROVIDED: [summary]"
3. Agent re-reads updated spec.md
4. Agent validates clarification resolves ambiguity
5. Agent resumes implementation from blocked task

**Good Example:**

```text
Agent: CLARIFICATION NEEDED (spec.md line 45: "real-time" undefined)
Human: Updated spec.md line 45: "real-time = <200ms p95 latency"
Agent: Re-reading spec.md... ✓ Clarification resolved
Agent: Resuming from task T015: Implement notification system
```

### 7.2 Constitutional Violations

**Trigger:** Spec or implementation conflicts with Constitution principles

**Response:**

1. **FLAG** the deviation immediately (STOP all work)
2. **DOCUMENT** conflict in console/log with:
   * Conflicting Constitution article (e.g., "Article VII: Simplicity")
   * Conflicting spec requirement (e.g., "spec.md lines 89-92")
   * Why conflict exists
3. **REQUEST** human decision on priority
4. **DO NOT** proceed until human provides direction

**Resolution Options:**

#### Option A: Constitution Takes Priority

* Human updates spec.md to align with Constitution
* Agent resumes with updated spec

#### Option B: Justified Exception

* Human adds justification to plan.md "Complexity Tracking" table:

```markdown
| Violation | Why Needed | Simpler Alternative Rejected |
|-----------|------------|------------------------------|
| Article VII: 4 projects instead of 3 | Separate auth service for compliance | Monolith rejected: GDPR data isolation required |
```

* Agent proceeds with documented exception

**Bad Example:**

```text
❌ Agent sees Constitution conflict but implements anyway with comment:
   "// TODO: This violates simplicity principle but spec requires it"
```

### 7.3 Quality Failures

**Trigger:** Tests fail or code quality checks do not pass

**Response:**

1. **SUSPEND** further implementation
2. **REPORT** failure (see Section 6.7)
3. **DETERMINE** root cause:
   * **Code Issue:** Bug in implementation → Fix and retry
   * **Spec Issue:** Acceptance scenario impossible/incorrect → Flag for human
4. **IF SPEC ISSUE:** Emit `CLARIFICATION NEEDED` suggesting spec update

**Recovery:**

* **Code Issue:** Fix implementation, re-run tests, resume
* **Spec Issue:** Wait for human to update spec, then regenerate code

### 7.4 Technical Blockers

**Trigger:** Blocked by external dependencies, missing APIs, technical limitations

**Response:**

1. **DOCUMENT** blocker in `specs/[###-feature-name]/research.md`:

```markdown
## Blocker: Missing Payment API Credentials

**Blocked Tasks:** T023, T024, T025 (payment integration)

**Description:** Implementation requires Stripe API key per plan.md Section 5.3

**Impact:** Cannot implement User Story 3 (payment processing)

**Alternatives Considered:**

- Mock payment provider: Rejected (violates Constitution Article IX: Integration-First)
- Skip for now: Possible but breaks feature completeness

**Recommendation:** Obtain Stripe test API credentials from team lead

**Status:** Waiting for credentials (added 2025-11-02)
```

1. **UPDATE** tasks.md: Mark blocked tasks as `[B]` (Blocked)
2. **SUGGEST** alternative approaches if possible
3. **ESCALATE** to human via console/log

**Recovery:**

* Human provides missing dependency/API/credentials
* Agent validates dependency available
* Agent resumes from blocked task

---

## 8. Collaboration Protocol

### 8.1 Version Control Discipline

* **MUST** commit only after local validation passes (Section 6.1)
* **MUST** group related edits into atomic commits (one user story/scenario)
* **MUST** reference feature numbers and spec sections in commit messages (Section 5.3)
* **MUST** work on feature branches: `[###-feature-name]` (create if not exists)
* **SHOULD** commit after each completed task in tasks.md

### 8.2 Change Communication

* **MUST** add or update design documents in feature directory when design trade-offs occur
* **MUST** document technical decisions in `research.md` using structured format:

```markdown
## Decision: [Topic]

**Chosen:** [Selected option]

**Rationale:** [Why this option]

**Alternatives Considered:**

- [Option A]: Rejected because [reason]
- [Option B]: Rejected because [reason]

**Trade-offs:** [Accepted limitations or costs]

**References:** [Links to docs, benchmarks, discussions]
```

* **MUST** notify human reviewers via PR description template (Section 5.6)

### 8.3 Feedback Loop

* **MUST** update spec documents first if implementation reveals issues
* **SHOULD** learn from code review feedback and adjust approach
* **MUST NOT** override human feedback unless reflected in updated specification documents
* **MUST** regenerate affected code when specs are updated to maintain alignment

---

## 9. Ethics & Safety

### 9.1 Prohibited Actions

**MUST NOT:**

* Commit secrets, API keys, tokens, passwords, or credentials to version control
* Share user data, PII, or sensitive information in logs or output
* Make undisclosed external calls or establish network connections not in spec
* Exfiltrate data or send telemetry without explicit specification

**Detection:**

* Run secret scanners before commit (e.g., git-secrets, truffleHog)
* Validate no hardcoded credentials in code
* Check for data leaks in logs/output

### 9.2 Licensing & Compliance

* **MUST** respect licensing terms of all third-party code and dependencies
* **SHOULD** prefer open source libraries with permissive licenses (MIT, Apache 2.0)
* **MUST NOT** include closed-source or non-redistributable components without approval
* **MUST** ensure privacy and compliance align with project requirements and applicable laws

### 9.3 Standards & Portability

* **SHOULD** prefer open standards over proprietary formats
* **SHOULD** write portable code (avoid platform-specific dependencies when possible)
* **MUST** document platform dependencies in plan.md if unavoidable

---

## 10. Glossary

**Acceptance Scenario** - Given-When-Then test case in spec.md that defines success criteria

**Atomic Commit** - Single logical change implementing one user story or scenario

**Constitution** - Immutable project principles in `.specify/memory/constitution.md`

**Constitution Gate** - Yes/no compliance check in plan.md "Constitution Check" section. Gates are blockers; implementation cannot proceed if gate fails without explicit justification.

**Complexity Tracking** - Table in plan.md documenting Constitution violations with justification. Format: `| Violation | Why Needed | Simpler Alternative Rejected |`

**Deterministic** - Same specification input produces identical code output every time

**Feature Directory** - `specs/[###-feature-name]/` containing all feature-related documents

**Idempotent** - Re-execution produces same result without side effects or duplication

**Implementation Plan** - `specs/[###-feature-name]/plan.md` defining technical architecture (HOW)

**Feature Specification** - `specs/[###-feature-name]/spec.md` defining requirements (WHAT/WHY)

**Single Source of Truth** - Authoritative specification documents that all implementation derives from

**Standard PR Template** - Pull request description format defined in Section 5.6

**Supporting Documents** - Optional design artifacts: data-model.md, contracts/, research.md, quickstart.md, tasks.md

---

*This document defines behavioral standards for AI agents in Spec-Driven Development projects using Spec Kit. All agents MUST internalize and honor these guidelines to maintain quality, consistency, and specification alignment.*

**Version:** 2.0  
**Last Updated:** 2025-11-02
