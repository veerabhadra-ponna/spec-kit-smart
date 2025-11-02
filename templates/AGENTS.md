# AI Agent Guidelines

**Version:** 2.2
**Last Updated:** 2025-11-02

---

## TL;DR - Quick Start for AI Agents

**Core Principle:** Specifications are the **single source of truth**. Never guess, always clarify.

**Document Priority (Highest to Lowest):**

1. Constitution (.specify/memory/constitution.md) - Immutable principles
2. Spec (specs/[###-feature-name]/spec.md) - WHAT and WHY
3. Plan (specs/[###-feature-name]/plan.md) - HOW
4. Supporting docs (data-model, contracts, research, quickstart, tasks)

**Golden Rules:**

- ✅ When unclear: STOP → emit `CLARIFICATION NEEDED` → wait for human
- ✅ Task states: `[ ]` pending, `[x]` complete, `[F]` failed, `[B]` blocked, `[W]` waiting
- ✅ Before commit: Run formatters → linters → tests
- ✅ Commits: Small (1 scenario/story), atomic, with spec references
- ❌ NEVER commit secrets, modify .specify/, or introduce unspecified requirements

**When Stuck:** See Section 2 "When Stuck" (8 common scenarios with solutions)

**Full Details Below** ↓

---

## 1. Purpose

This document defines behavioral and operational standards for AI coding agents participating in Spec-Driven Development using the Spec Kit framework.

Agents MUST follow these guidelines to ensure deterministic, auditable, and high-quality contributions aligned with project specifications and the Constitution.

**Keywords:** This document uses RFC 2119 terminology:

- **MUST** / **MUST NOT** = Mandatory requirement
- **SHOULD** / **SHOULD NOT** = Recommended best practice
- **MAY** = Optional capability

---

## 2. Quick Reference

### Critical DO Rules

✅ **MUST** Stop and emit `CLARIFICATION NEEDED` when spec is ambiguous
✅ **MUST** Follow Constitution principles at all times
✅ **MUST** Update task states in `tasks.md`: `[ ]` pending, `[x]` complete, `[F]` failed, `[B]` blocked, `[W]` waiting
✅ **MUST** Run formatters, linters, and tests before committing
✅ **MUST** Update spec documents first if implementation reveals issues

### Critical DON'T Rules

❌ **MUST NOT** commit secrets, API keys, tokens, or credentials  
❌ **MUST NOT** modify `.specify/` directory during implementation  
❌ **MUST NOT** introduce requirements not in specifications  
❌ **MUST NOT** proceed with implementation when spec is unclear  
❌ **MUST NOT** override human feedback without updated spec

### When Stuck

**Decision Flowchart:**

```text
┌─── Problem Occurred ───┐
│                        │
├─ Spec unclear/ambiguous?
│  └─ YES → EMIT "CLARIFICATION NEEDED" (5.1)
│           Mark affected tasks [B], WAIT for human
│
├─ Test failed?
│  ├─ Syntax error/typo? → Auto-fix (max 2 attempts) (7.3)
│  ├─ Logic/assertion error? → Mark [F], REPORT, WAIT (7.3)
│  └─ Flaky (passes sometimes)? → Document, ESCALATE (7.3)
│
├─ Constitution conflict?
│  └─ YES → STOP all work, FLAG conflict (7.2)
│           Request human decision, WAIT
│
├─ Missing dependency/API/file?
│  └─ YES → Document in research.md (7.4)
│           Mark tasks [B], ESCALATE, WAIT
│
├─ Dependency version conflict?
│  └─ YES → EMIT "CLARIFICATION NEEDED" (5.4)
│           Show current vs required, WAIT
│
├─ License incompatible?
│  └─ YES → Document in research.md (9.2)
│           Suggest alternatives, WAIT
│
├─ Workflow command failed?
│  └─ YES → Check prerequisites, retry once (3)
│           If still fails → ESCALATE
│
├─ Constitution Gate failed?
│  └─ YES → STOP, check plan.md for justification (6.6)
│           If no justification → REQUEST human decision
│
└─ Git merge conflict?
   └─ YES → git merge --abort (8.1)
            REPORT conflicts, WAIT for human resolution
```

**Quick Lookup by Symptom:**

1. **Ambiguous Spec** → Emit `CLARIFICATION NEEDED` (see Section 5.1)
2. **Test Failure** → Report which acceptance scenario failed (see Section 7.3)
3. **Constitutional Conflict** → Flag immediately, request human decision (see Section 7.2)
4. **Technical Blocker** → Document in `research.md`, suggest alternatives (see Section 7.4)
5. **Licensing Conflict** → Document in `research.md`, suggest compatible alternatives (see Section 9.2)
6. **Workflow Command Fails** → Check prerequisites, retry once, escalate if retry fails (see Section 3)
7. **Gate Failure** → Stop implementation, check plan.md for justification (see Section 6.6)
8. **Git Merge Conflict** → Abort merge, notify human, wait for resolution (see Section 8.1)

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
   - *Example:* Constitution says "no ORMs" but spec suggests using one → Constitution wins
2. **Feature Specification** (`specs/[###-feature-name]/spec.md`) - WHAT and WHY
   - *Example:* Spec says "CSV export" but plan says "JSON only" → Spec wins
3. **Implementation Plan** (`specs/[###-feature-name]/plan.md`) - HOW
   - *Example:* Plan specifies library X but you prefer Y → Plan wins
4. **Supporting Documents** - Data models, contracts, research, quickstart, tasks
   - *Example:* Task says "file A" but data-model references "file B" → Clarify with human
   - **Sub-priority within Supporting Docs:** data-model.md > contracts/ > research.md > quickstart.md > tasks.md

**Conflict Resolution Protocol:**

If documents conflict at the same priority level:

1. **STOP** implementation immediately
2. Emit `CLARIFICATION NEEDED` with references to conflicting sections
3. **DO NOT** make assumptions or "best guesses"
4. Wait for human clarification and spec update

**Examples of Same-Level Conflicts:**

- **Supporting docs conflict:** data-model.md says 3 fields but contracts/api.yaml says 4 fields → STOP, emit `CLARIFICATION NEEDED` citing both sources. Sub-priority (data-model > contracts) is a *suggestion* for human resolution, NOT agent authority to proceed.
- **Multiple specs:** If multiple spec.md files exist for different features → Treat as separate contexts (no conflict unless features interact)
- **Plan contradicts itself:** Section 3.2 says "use library X" but Section 4.5 says "use library Y" → STOP, emit `CLARIFICATION NEEDED`

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

**Workflow Command Failure Handling:**

If a workflow command fails (e.g., `/speckit.plan` errors, `/speckit.implement` crashes):

1. **REPORT** error message and stack trace
2. **CHECK** prerequisites: Does spec.md exist for `/speckit.plan`? Does plan.md exist for `/speckit.tasks`?
3. **RETRY** once if transient error (network timeout, file lock)
4. **ESCALATE** to human if retry fails, providing error details and blocked workflow step

*For detailed workflow information, see `spec-driven.md` in project root.*

---

## 4. Core Responsibilities

Agents MUST interpret specifications as the **single source of truth** and produce deterministic, production-ready results.

### 4.1 Specification Interpretation

- **MUST** read all documents in priority order (Section 3.1) before starting implementation
- **MUST** derive all logic and structure from specifications only
- **MUST NOT** introduce requirements, dependencies, or opinions not found in specs
- **SHOULD** cross-reference between spec.md, plan.md, and supporting documents for consistency

**Context Window Management:**

If total document size exceeds agent context window:

1. **ALWAYS read completely:** Constitution, Spec, Plan (these are mandatory)
2. **Read selectively:** Supporting documents (load sections on-demand as needed)
3. **EMIT WARNING:** "Documents exceed context window. Read Constitution + Spec + Plan fully. Supporting docs loaded on-demand."
4. **Strategy:** Read executive summaries first, load detailed sections when implementing specific features

**Binary Files and Non-Text References:**

If spec/plan references binary files (images, PDFs, diagrams, videos):

1. **EMIT WARNING:** "Cannot read binary file: [filename]. Agent requires text description."
2. **REQUEST** human to provide text description in spec.md or plan.md:
   - Image/diagram: Describe what the diagram shows, key components, relationships
   - PDF: Extract relevant text sections and add to spec/plan
   - Video: Provide transcript or written summary
3. **EXAMPLES:**

```text
❌ BAD: "See architecture diagram in docs/architecture.png"
✅ GOOD: "Architecture follows 3-tier design:
         - Frontend (React) communicates with Backend (FastAPI) via REST
         - Backend connects to Database (PostgreSQL)
         - See docs/architecture.png for visual representation"
```

1. **DO NOT:**
   - Proceed with assumptions about binary file content
   - Skip implementation because binary reference exists
   - Attempt to parse binary files directly

**Context Budget Guidelines:**

- Reserve 30% of context for documents
- Reserve 40% for code generation/editing
- Reserve 30% for conversation history/planning

**If Unable to Read Mandatory Documents (Constitution + Spec + Plan):**

- **STOP** implementation
- **EMIT:** "CONTEXT OVERFLOW: Cannot fit Constitution + Spec + Plan in context window"
- **SUGGEST:** "Split spec into smaller feature specs or use chunked reading approach"
- **WAIT** for human guidance

### 4.2 Code Generation Standards

- **MUST** generate code that is:
  - **Functionally Deterministic** - Same spec input → functionally equivalent code (same behavior, may differ in non-functional metadata)
  - **Idempotent** - Re-execution does not duplicate or corrupt output
  - **Production-ready** - Compiles, passes tests, follows project conventions
- **MUST** align all code with specifications strictly

**Functional Determinism Explained:**

- **REQUIRED:** Identical logic, control flow, algorithms, data structures, test assertions
- **ALLOWED TO VARY:** Timestamps in comments, UUIDs in metadata, code formatter version differences, file path separators (Windows vs Linux)
- **RANDOMNESS:** If randomness needed (test data, IDs), use fixed seeds from sources below

**Deterministic Seed Sources (in priority order):**

1. Explicit seed in spec.md or plan.md (e.g., "use seed 42 for test data generation")
2. Hash of feature directory name (e.g., `hash("[###-feature-name]") mod 2^32`)
3. Fixed constant (e.g., `0` for consistent test fixtures)

**Example of Acceptable Variance:**

```python
# Run 1 (functionally identical to Run 2):
# Generated on 2025-11-02 at 14:23:15
def export_csv(data):
    return data.to_csv()

# Run 2 (functionally identical to Run 1):
# Generated on 2025-11-03 at 09:17:42
def export_csv(data):
    return data.to_csv()
```

### 4.3 Output Requirements

- **MUST** produce all artifacts specified in implementation plan
- **MUST** include tests for every acceptance scenario
- **SHOULD** follow project coding standards and style guides

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

**Multiple Ambiguities:**

If multiple ambiguities found during spec review (before implementation):

- **BATCH** all clarifications into single `CLARIFICATION NEEDED` message with numbered questions
- **EXAMPLE:** "Found 3 ambiguities in spec.md: (1) Line 45: 'real-time' undefined, (2) Line 67: CSV column order not specified, (3) Line 89: Error handling strategy missing"

If ambiguities discovered during implementation (blocking different tasks):

- **EMIT** `CLARIFICATION NEEDED` immediately when first ambiguity blocks progress
- **CONTINUE** with non-blocked tasks while waiting for clarification
- **EMIT** additional `CLARIFICATION NEEDED` if second ambiguity blocks different task

### 5.2 Minimal Changes

**MUST** make small, reviewable, logically grouped changes.

**Definition of "Small":**

- Single user story or acceptance scenario per commit
- Modify 1-5 files per commit (exception: refactoring, adding new modules)
- <300 lines changed per commit

**Exceptions to <300 lines limit:**

- Generated code (protobuf, OpenAPI schemas, database ORM models)
- Data migrations (SQL schema changes, seed data)
- Large test fixtures (JSON/XML test data files)
- Initial project scaffolding (first commit only)
- Dependency lockfiles (package-lock.json, Cargo.lock, poetry.lock)

**Good Example:**

```text
✅ Commit 1: Implement User Story 1, Scenario 1 (3 files, 87 lines)
✅ Commit 2: Implement User Story 1, Scenario 2 (2 files, 45 lines)
```

**Bad Example:**

```text
❌ Commit 1: Implement all 5 user stories (47 files, 3,421 lines)
```

**Partial Implementation Policy:**

- **MAY** ship user stories incrementally (e.g., User Story 1 complete, User Story 2 pending)
- **MUST NOT** ship half-implemented user stories or scenarios
- **MUST** mark incomplete user stories as "⏳ In Progress" in PR description
- **SHOULD** prioritize P1 user stories before P2/P3

**Definitions:**

- **Half-implemented:** Code is written but broken/incomplete (tests failing, logic incomplete)
- **Blocked:** Code not yet written due to external dependency (API key, infrastructure, human approval)

**Shipping Rules:**

- ✅ **CAN ship** scenarios marked `[B]` blocked with clear blocker documentation in research.md
- ❌ **CANNOT ship** scenarios marked `[F]` failed or partially coded but not working
- ✅ **CAN ship** PR with mix of `[x]` complete and `[B]` blocked scenarios
- ❌ **CANNOT ship** PR with any `[F]` failed scenarios

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

- Source code directories
- Test directories
- Development/test config files: `/config/dev.*`, `/config/test.*`, `/config/local.*`, `/config/development.*`, `/config/staging.*` (only if specified in plan)
- Build/dependency manifest files: `Makefile`, `package.json`, `Cargo.toml`, `build.gradle`, `build.gradle.kts`, `pom.xml`, `pyproject.toml`, `go.mod`, `Gemfile`, `composer.json`, `CMakeLists.txt`, `meson.build`, etc.

**Build File Modification Rules:**

- **IF** plan explicitly mentions modifying build files → Follow plan instructions
- **IF** spec requires dependency not in plan → **MAY** add dependency to build files **AND** document decision in research.md with rationale
- **IF** neither spec nor plan mentions dependency → **MUST** emit `CLARIFICATION NEEDED` before adding

**Example Exception (Allowed):**

```text
Spec says: "Use requests library for HTTP calls"
Plan says: (nothing about requirements.txt)
Agent may: Add "requests==2.31.0" to requirements.txt
Agent must: Document in research.md:
  "Added requests dependency per spec.md line 45 requirement.
   Plan didn't explicitly mention requirements.txt modification,
   but dependency is required for implementation."
```

**Dependency Version Conflicts:**

Before adding or modifying dependencies, agent MUST check for version conflicts:

1. **CHECK** existing dependencies in build files (requirements.txt, package.json, Cargo.toml, etc.)
2. **DETECT** conflicts:
   - **Direct conflict:** Spec requires `requests==2.28.0` but project already uses `requests==2.31.0`
   - **Incompatible versions:** Spec requires `django==4.0` but another dependency requires `django>=3.0,<4.0`
   - **Breaking changes:** Upgrading from v1 to v2 with breaking API changes
3. **IF conflict detected:** Emit `CLARIFICATION NEEDED`:

```text
CLARIFICATION NEEDED:
  Document: spec.md line 78
  Issue: Dependency version conflict detected

  Required by spec: requests==2.28.0
  Currently installed: requests==2.31.0 (used by feature [001-user-auth])

  Options:
    A) Downgrade to 2.28.0 (may break existing feature [001-user-auth])
    B) Upgrade spec requirement to 2.31.0 (update spec.md)
    C) Test if 2.31.0 is compatible with spec requirements (preferred if backward compatible)

  Recommendation: Option C - Test with 2.31.0 first, as it's likely backward compatible
  Blocked Tasks: T056, T057
```

1. **DO NOT:**
   - Install conflicting versions without approval
   - Downgrade dependencies that break other features
   - Modify dependencies used by other features without checking impact
1. **PREFER:** Using existing dependency version if compatible with spec requirements

**Prohibited Modifications:**

- `.specify/memory/constitution.md`
- `.specify/templates/*`
- `.specify/scripts/*`
- `specs/[###-feature-name]/*.md` (except under human direction)
- Production config files (see Section 5.5)

### 5.5 Guardrails

**MUST** respect protected paths and project structure.

**Protected Paths (MUST NOT modify):**

- `/data/` - Production data
- `/config/*.production.*`, `/config/*.prod.*` - Production configs
- Dependency directories: `/vendor/`, `/node_modules/`, `/.venv/`, `/venv/`, `/target/` (Rust), `/build/` (compiled artifacts)
- `.git/` - Version control metadata
- System files (e.g., `/etc/`, `/usr/`, Windows registry)

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
- ✅ Test-First: 47 tests, 94% coverage (target: ≥80% line coverage, 100% acceptance scenario coverage)
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

- Code formatters (e.g., black, prettier, rustfmt)
- Linters (e.g., pylint, eslint, clippy)
- Type checkers (e.g., mypy, TypeScript, Flow)
- Build verification (code compiles without errors)

**WHERE:** Run locally in agent environment
**WHEN:** Before `git commit`
**HOW:** Execute via project-defined pre-commit hooks or CI scripts

**Fallback if No Pre-Commit Hooks:**

1. Check for common config files: `.pre-commit-config.yaml`, `package.json` (scripts), `Makefile` (lint/test targets)
2. If config exists but hooks not installed: Run tools manually based on config
3. If no config exists: Run language-standard tools (e.g., `black .`, `eslint .`, `cargo clippy`)
4. Document missing automation in research.md and suggest adding hooks to plan

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

**Scenario Failure Policy:**

- **MUST** fix all scenarios for a user story before marking that user story complete
- **MAY** proceed to next user story if current user story scenarios all pass (even if later user stories have failing scenarios)
- **MUST NOT** ship PR with any failing scenarios (all scenarios in PR must pass)
- **Priority order:** Fix P1 user story scenarios before P2/P3 scenarios

**Time-Dependent Requirements:**

If spec includes time-based requirements (timeouts, delays, expiration, scheduling):

1. **MUST** use time mocking/stubbing (do not wait for real time to pass)
2. **Recommended libraries by language:**
   - Python: `freezegun`, `time-machine`, `pytest-freezegun`
   - JavaScript: `Sinon.useFakeTimers()`, `jest.useFakeTimers()`
   - Ruby: `timecop`, `ActiveSupport::Testing::TimeHelpers`
   - Java: `java.time.Clock` with fixed clock
   - Go: `clockwork`, dependency injection for time.Now()
3. **MUST** document time mocking approach in plan.md "Testing Strategy" section
4. **EXAMPLES:**

```python
# BAD: Real time wait (slow, flaky)
def test_cache_expiration():
    cache.set("key", "value", ttl=3600)  # 1 hour
    time.sleep(3600)  # Wait 1 hour
    assert cache.get("key") is None

# GOOD: Time mocking (fast, deterministic)
@freeze_time("2025-01-01 12:00:00")
def test_cache_expiration():
    cache.set("key", "value", ttl=3600)  # 1 hour
    with freeze_time("2025-01-01 13:00:00"):  # Jump 1 hour
        assert cache.get("key") is None
```

1. **IF** time mocking library not available: Document in research.md and request approval for adding dependency

### 6.3 Contract Compliance

**MUST** ensure implementations match API specifications (if `contracts/` exists).

**Verification Steps:**

1. Compare implemented endpoints to contract definitions
2. Validate request/response schemas match exactly
3. Test error responses match contract specifications
4. Verify authentication/authorization as specified

**Tool Recommendations (SHOULD use if available):**

- OpenAPI contracts: OpenAPI validators (e.g., Spectral, Redocly)
- GraphQL contracts: GraphQL schema validators (e.g., graphql-inspector)
- REST contracts: Contract testing tools (e.g., Pact, Spring Cloud Contract)

### 6.4 Data Model Alignment

**MUST** verify code matches schemas in `data-model.md` (if applicable).

**Verification:**

- Database migrations match documented schemas
- Model classes match entity definitions
- Validation rules match constraints
- Relationships match documented cardinalities

### 6.5 Quickstart Verification

**MUST** validate documented scenarios work (if `quickstart.md` exists).

**Process:**

1. Follow quickstart steps exactly as documented
2. Verify all examples produce expected output
3. Test edge cases mentioned in quickstart
4. Ensure setup instructions are complete

### 6.6 Constitution Gates

**MUST** verify compliance with gates in "Constitution Check" section of `plan.md`.

**Common Constitution-Based Gates:**

- **Library-First Gate** - Feature implemented as standalone library
- **CLI Interface Gate** - Library exposes CLI with text I/O
- **Test-First Gate** - Tests written before implementation
- **Simplicity Gate** - Maximum 3 projects/modules
- **Anti-Abstraction Gate** - Uses framework directly, no wrapper layers
- **Integration-First Gate** - Real databases (not mocks), contract tests mandatory

**Gate Failure = BLOCKER**: Implementation MUST NOT proceed if any gate fails without explicit justification in plan.md "Complexity Tracking" table.

**Custom Gates (Non-Constitution):**

If plan.md defines additional gates beyond Constitution (e.g., "Performance Gate: <100ms p95 latency"):

- **MUST** verify custom gates same as Constitution gates
- **MUST** treat custom gate failure as blocker unless plan.md explicitly marks it as "SHOULD" or "aspirational"
- **SHOULD** report custom gate compliance in PR description

### 6.7 Fail Fast

**MUST** abort if build/test fails.

**Abort Procedure:**

1. **STOP** all implementation work immediately
2. **REPORT** to console/log with:
   - Which test/build failed
   - Error message and stack trace
   - Which acceptance scenario or spec requirement is blocked
   - Which tasks in tasks.md are affected
3. **UPDATE** tasks.md: Mark failed task with `[F]` (Failed) instead of `[x]`
4. **EMIT** issue report (see Section 7.3)
5. **WAIT** for human intervention

**WHERE to Report:**

- Console output (for interactive sessions)
- CI log (for automated runs)
- tasks.md comments (for async workflows)

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

1. **DETERMINE SCOPE:** Does ambiguity block ALL work or SOME work?
2. **IF ambiguity blocks ALL work:** STOP all implementation completely
3. **IF ambiguity blocks SOME work:** STOP blocked work, CONTINUE with non-blocked tasks
4. **EMIT** `CLARIFICATION NEEDED` (see Section 5.1 format)
5. **DO NOT** make assumptions or proceed with "best guess" on blocked work
6. **WAIT** for human response on blocked work

**Decision Rule:**

| Ambiguity Type | Action | Example |
|----------------|--------|---------|
| **Fundamental** (affects all user stories) | **STOP ALL WORK** | "Real-time updates" undefined - affects entire architecture |
| **Isolated** (affects specific user story/scenario) | **STOP blocked, CONTINUE others** | User Story 2 unclear - but User Stories 1 & 3 are clear |
| **Detail** (affects specific function/feature) | **CONTINUE main work, EMIT clarification** | CSV column order unspecified - implement other features while waiting |

**Recovery Process:**

1. Human updates `specs/[###-feature-name]/spec.md` with clarification
2. Human responds with "CLARIFICATION PROVIDED: [summary]" OR agent detects file modification timestamp change on spec.md
3. Agent re-reads updated spec.md
4. Agent validates clarification resolves ambiguity (checks that previously ambiguous section now has concrete values/requirements)
5. Agent resumes implementation from blocked task

**Human Response Detection Methods (in priority order):**

1. **Interactive sessions:** Wait for explicit "CLARIFICATION PROVIDED" message (no timeout - session-based)
2. **Git-based workflows (PREFERRED):** Check for spec.md changes via git:
   - Command: `git log -1 --format=%cd specs/[###-feature-name]/spec.md`
   - Check every 5 minutes (not CPU-intensive, uses git metadata)
   - Look for commits with message containing "clarification", "update", or "fix"
   - Max 24h timeout, then report timeout and suspend
3. **File-based workflows (FALLBACK):** If not using git:
   - Check spec.md file modification timestamp
   - Check every 5 minutes (reduced from 30s to minimize I/O)
   - Max 24h timeout
   - **Warning:** May not work reliably on network file systems (NFS, SMB)
4. **CI/CD workflows:** Fail build after timeout specified in plan.md (default: 30 minutes)
   - **Note:** CI/CD cannot wait indefinitely
   - Agent must emit `CLARIFICATION NEEDED` early in CI build (before 30min timeout)

**Why Git-Based is Preferred:**

- Uses git metadata (fast, no file I/O)
- Works reliably in containers and network filesystems
- Provides commit message context
- Less resource-intensive than file polling

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
   - Conflicting Constitution article (e.g., "Article VII: Simplicity")
   - Conflicting spec requirement (e.g., "spec.md lines 89-92")
   - Why conflict exists
3. **REQUEST** human decision on priority
4. **DO NOT** proceed until human provides direction

**Resolution Options:**

#### Option A: Constitution Takes Priority

- Human updates spec.md to align with Constitution
- Agent resumes with updated spec

#### Option B: Justified Exception

- Human adds justification to plan.md "Complexity Tracking" table:

```markdown
| Violation | Why Needed | Simpler Alternative Rejected |
|-----------|------------|------------------------------|
| Article VII: 4 projects instead of 3 | Separate auth service for compliance | Monolith rejected: GDPR data isolation required |
```

- Agent proceeds with documented exception

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
   - **Obvious Code Issue:** Auto-fix and retry (max 2 attempts)
     - Examples: Syntax errors, typos in variable names, missing imports, incorrect indentation, missing semicolons, unclosed brackets
   - **Ambiguous Failure:** Mark `[F]`, wait for human
     - Examples: Logic bugs, assertion errors, unexpected test output, wrong algorithm, incorrect business logic
   - **Spec Issue:** Acceptance scenario impossible/incorrect → Flag for human
4. **IF SPEC ISSUE:** Emit `CLARIFICATION NEEDED` suggesting spec update

**Recovery:**

- **Obvious Code Issue:** Fix implementation, re-run tests, resume (if fix successful after ≤2 attempts)
- **Ambiguous Failure:** Wait for human diagnosis, apply directed fix, re-run tests, resume
- **Spec Issue:** Wait for human to update spec, then regenerate code

**Flaky Test Detection:**

If test exhibits non-deterministic behavior (passes sometimes, fails other times):

1. **IDENTIFY** flaky test:
   - Different error messages across retry attempts
   - Timeouts or race conditions
   - Network/filesystem dependencies
   - Random data without fixed seeds
2. **DOCUMENT** in research.md:

```markdown
## Flaky Test Detected

**Test:** tests/integration/test_api_endpoint.py::test_response_time

**Flakiness Evidence:**
- Attempt 1: PASS
- Attempt 2: FAIL (timeout after 5s)
- Attempt 3: PASS
- Attempt 4: FAIL (connection refused)

**Root Cause:** Test depends on external service availability

**Impact:** Cannot reliably verify acceptance scenario

**Recommendation:**
1. Add retry logic to test
2. Use service mocking/stubbing
3. Increase timeout threshold
4. Fix race condition in implementation
```

1. **EMIT** warning: "FLAKY TEST DETECTED: [test name]"
1. **MARK** task as `[F]` (not `[x]`)
1. **ESCALATE** to human for investigation

**DO NOT:**

- Continue retrying indefinitely (max 2 attempts)
- Mark flaky test as passed
- Ignore flaky test

**Note:** Flaky tests indicate quality issues (race conditions, improper mocking, non-deterministic logic).

### 7.4 Technical Blockers

**Trigger:** Blocked by external dependencies, missing APIs, technical limitations, missing files

**Common Blocker Types:**

1. **Missing external dependencies:** API keys, credentials, infrastructure
2. **Missing files/resources:** Files referenced in spec/plan that don't exist
3. **Technical limitations:** Platform incompatibility, library unavailable

**Response:**

1. **DOCUMENT** blocker in `specs/[###-feature-name]/research.md`
1. **UPDATE** tasks.md: Mark blocked tasks as `[B]` (Blocked) with inline comment
1. **SUGGEST** alternative approaches if possible
1. **ESCALATE** to human via console/log

#### Special Case: Missing or Renamed Files

If spec/plan references file that doesn't exist:

1. **SEARCH** for similar filenames (fuzzy match):
   - `src/utils/helper.py` missing → Search for `src/utils/help*.py`, `src/**/helper*.py`
   - Use file tree, grep, or find commands
2. **IF similar file found:** Emit `CLARIFICATION NEEDED`:

```text
CLARIFICATION NEEDED:
  Document: plan.md line 67
  Issue: Referenced file "src/utils/helper.py" does not exist
  Similar files found:
    - src/utils/helpers.py (plural)
    - src/lib/helper_functions.py
  Question: Which file should be modified?
  Blocked Tasks: T042, T043
```

1. **IF no similar files found:** Emit `CLARIFICATION NEEDED`:

```text
CLARIFICATION NEEDED:
  Document: plan.md line 67
  Issue: Referenced file "src/utils/helper.py" does not exist
  No similar files found
  Question: Should this file be created, or is the path incorrect?
  Blocked Tasks: T042, T043
```

1. **DO NOT:**
   - Create new file without confirmation (may duplicate existing file)
   - Proceed with "best guess" filename
   - Silently skip the file modification

**Example: Documenting Blocker in research.md:**

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

**Example: Blocker Format in tasks.md:**

```markdown
- [B] T023: Implement payment gateway integration <!-- BLOCKED: Missing Stripe API credentials (see research.md "Blocker: Missing Payment API Credentials") -->
- [B] T024: Test payment flow <!-- BLOCKED: Depends on T023 -->
- [B] T025: Add payment error handling <!-- BLOCKED: Depends on T023 -->
```

**Recovery:**

- Human provides missing dependency/API/credentials
- Agent validates dependency available
- Agent resumes from blocked task

### 7.5 Constitution Ambiguity

**Trigger:** Constitution article is vague, open to multiple interpretations

**Problem:** Constitution is "immutable" but articles may be ambiguous (e.g., "Keep it simple" - how simple?)

**Common Ambiguous Constitution Phrases:**

- "Keep it simple" - How many files/modules/lines?
- "Prefer libraries over custom code" - Even if library is 10x larger?
- "Test-first" - Unit tests? Integration tests? Both? Coverage threshold?
- "Avoid premature optimization" - What's premature vs necessary?

**Response:**

1. **STOP** implementation immediately
2. **DOCUMENT** ambiguity in console/log:
   - Conflicting Constitution article (e.g., "Article VII: Simplicity")
   - Multiple valid interpretations
   - Why clarification needed
3. **EMIT** `CONSTITUTION AMBIGUITY`:

```text
CONSTITUTION AMBIGUITY:
  Article: Article VII "Keep it simple - maximum 3 projects"
  Question: Does "3 projects" mean 3 source code projects or 3 total dependencies?
  Current situation: Spec requires 2 source projects + 5 library dependencies = 7 total
  Interpretations:
    A) 3 source projects (allows many dependencies) → Implementation is valid
    B) 3 total projects including dependencies → Implementation violates Constitution
  Blocked: Cannot proceed without clarifying Constitution intent
```

1. **DO NOT** proceed until human clarifies Constitution interpretation
1. **WAIT** for human to either:
   - Add clarification note to constitution.md (e.g., "Note: '3 projects' means source code projects, not dependencies")
   - Update spec.md to align with Constitution
   - Add justified exception to plan.md Complexity Tracking table

**Recovery:**

- Human clarifies Constitution intent (via note in constitution.md or response message)
- Agent re-reads Constitution and validates understanding
- Agent proceeds with clarified interpretation

**Key Insight:** Constitution may be "immutable" in principle, but *interpretation* requires human input when ambiguous.

---

## 8. Collaboration Protocol

### 8.1 Version Control Discipline

- **MUST** commit only after local validation passes (Section 6.1)
- **MUST** group related edits into atomic commits (one user story/scenario)
- **MUST** reference feature numbers and spec sections in commit messages (Section 5.3)
- **MUST** work on feature branches: `[###-feature-name]` (create if not exists)
- **SHOULD** commit after each completed task group: Multiple related tasks implementing a single scenario or user story SHOULD be grouped into one atomic commit. Individual unrelated tasks MAY be committed separately.

**Commit Timing Workflow:**

1. Complete implementation for scenario/user story
2. Mark tasks as `[x]` in tasks.md
3. Run pre-commit validation (formatters, linters, type checkers, tests)
4. If validation passes → Create commit with atomic change
5. If validation fails → Fix issues, repeat from step 3
6. Push commits to feature branch after each logical unit (scenario/user story) is complete

**Parallelization Policy:**

- **SHOULD** work on one task at a time for deterministic, traceable execution
- **MAY** work on multiple independent tasks in parallel if:
  - Tasks have no shared dependencies (different files, different modules)
  - Tasks implement different user stories
  - Agent has capability for parallel execution (multi-threaded, multi-agent)
- **MUST NOT** parallelize tasks that:
  - Modify the same files
  - Share data models or contracts
  - Have sequential dependencies (Task B depends on Task A output)

**Git Merge Conflict Handling:**

If `git pull` or `git merge` results in conflicts:

1. **ABORT** merge immediately (`git merge --abort` or `git rebase --abort`)
2. **REPORT** conflict details to human:
   - Conflicting files
   - Local changes summary
   - Remote changes summary
3. **DO NOT** attempt to resolve conflicts automatically
4. **WAIT** for human to resolve conflicts manually
5. **RESUME** implementation after human completes merge

**Rollback Procedure:**

If PR is rejected or human requests rollback:

1. **DO NOT** delete feature branch (preserve history)
2. **REVERT** commits if already merged to main: `git revert <commit-range>`
3. **RESET** branch if not yet merged: `git reset --hard <last-good-commit>` (only if human explicitly requests destructive reset)
4. **PREFER** creating fix commits over rewriting history
5. **WAIT** for human direction before force-pushing or deleting branches

### 8.2 Change Communication

- **MUST** add or update design documents in feature directory when design trade-offs occur
- **MUST** document technical decisions in `research.md` using structured format:

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

- **MUST** notify human reviewers via PR description template (Section 5.6)

### 8.3 Feedback Loop

- **MUST** update spec documents first if implementation reveals issues
- **SHOULD** learn from code review feedback and adjust approach
- **MUST NOT** override human feedback unless reflected in updated specification documents
- **MUST** regenerate affected code when specs are updated to maintain alignment

**Regeneration Strategy Decision Criteria:**

| Spec Change Type | Strategy | Action |
|------------------|----------|--------|
| **Requirements added** (e.g., "also support JSON export") | **Incremental** | Add new code, keep existing code unchanged |
| **Requirements modified** (e.g., "CSV export" → "CSV with headers export") | **Selective** | Regenerate only affected functions/classes |
| **Architecture changed** (e.g., "REST API" → "GraphQL API") | **Full** | Regenerate entire affected modules from scratch |
| **Data model changed** (e.g., new field in schema) | **Full** | Regenerate models, migrations, and dependent code |
| **Acceptance criteria changed** (e.g., new test scenarios) | **Test-first** | Regenerate tests first, then update implementation to pass |

**Regeneration Workflow:**

1. **Identify scope:** Determine which strategy applies (see table above)
2. **Backup existing:** Preserve current implementation (via git commit before regenerating)
3. **Regenerate tests first:** Update tests to reflect new acceptance criteria
4. **Regenerate implementation:** Apply strategy (incremental/selective/full)
5. **Validate:** Run all tests to ensure regenerated code works
6. **If tests fail:** Fix or repeat regeneration

**When in Doubt:**

- **PREFER** incremental/selective over full (preserve working code)
- **ALWAYS** regenerate tests before implementation
- **NEVER** delete working code without git backup

---

## 9. Ethics & Safety

### 9.1 Prohibited Actions

**MUST NOT:**

- Commit secrets, API keys, tokens, passwords, or credentials to version control
- Share user data, PII, or sensitive information in logs or output
- Make undisclosed external calls or establish network connections not in spec
- Exfiltrate data or send telemetry without explicit specification

**Detection:**

- **MUST** run secret scanners before commit (tools: git-secrets, truffleHog, gitleaks, detect-secrets, GitHub Secret Scanning)
- **MUST** validate no hardcoded credentials in code (search for patterns: password=, api_key=, token=, secret=)
- **MUST** check for data leaks in logs/output (PII, email addresses, IP addresses)
- **SHOULD** use .gitignore to prevent accidental commit of sensitive files (`.env`, `credentials.json`, `*.pem`, `*.key`)

### 9.2 Licensing & Compliance

- **MUST** respect licensing terms of all third-party code and dependencies
- **SHOULD** prefer open source libraries with permissive licenses (MIT, Apache 2.0, BSD)
- **MUST NOT** include closed-source or non-redistributable components without approval
- **MUST** ensure privacy and compliance align with project requirements and applicable laws

**Licensing Conflicts:**

If spec requires a library but its license conflicts with Constitution or project license:

1. **STOP** implementation immediately
2. **DOCUMENT** conflict in research.md:
   - Required library and its license (e.g., "Library X under GPL-3.0")
   - Constitution/project license requirement (e.g., "Article XII: MIT-only dependencies")
   - Why library is needed (e.g., "Only implementation of Protocol Y")
3. **SUGGEST** alternatives with compatible licenses
4. **ESCALATE** to human for decision (accept GPL, find alternative, or update spec)
5. **WAIT** for human direction before proceeding

### 9.3 Standards & Portability

- **SHOULD** prefer open standards over proprietary formats (JSON over binary, REST over proprietary RPC)
- **SHOULD** write portable code (avoid platform-specific dependencies when possible)
- **MUST** document platform dependencies in plan.md if unavoidable

**Platform Dependency Documentation:**

If implementation requires platform-specific code (e.g., Windows-only API, Linux-only system call):

- **WHERE:** Document in plan.md "Platform Requirements" section
- **WHAT:** Specify OS, version, architecture, required system libraries
- **WHY:** Explain why platform-specific approach is necessary
- **ALTERNATIVES:** Document rejected cross-platform alternatives

**Example:**

```markdown
## Platform Requirements

**Target:** Linux x86_64 only (Ubuntu 20.04+)

**Platform-Specific Dependencies:**
- inotify API for file watching (Linux kernel 2.6.13+)
- Rejected alternative: Polling (violates Constitution Article VII: Simplicity - adds polling complexity)
```

---

## 10. Meta-Guidelines

### 10.1 Reporting Errors in This Document

If agent discovers error in AGENTS.md itself (wrong section reference, contradiction, typo):

1. **EMIT** `DOCUMENT ERROR`:

```text
DOCUMENT ERROR in AGENTS.md:
  Location: Section 4.2, line 156
  Issue: Reference says "See Section 3.2" but correct section is "Section 3.1"
  Impact: May cause confusion about document priority
  Severity: LOW/MEDIUM/HIGH
```

1. **CONTINUE** implementation (don't block on documentation errors)
1. **LOG** error for human review

**DO NOT:**

- Stop work due to minor documentation errors
- Attempt to fix AGENTS.md (it's read-only for agents)
- Ignore severe contradictions that affect behavior

### 10.2 AGENTS.md Version Management

**Version Consistency Rule:**

- Agent **MUST** use version of AGENTS.md present at **start of feature implementation**
- **DO NOT** switch AGENTS.md versions mid-feature (causes inconsistent behavior)
- **IF** new AGENTS.md version released during implementation:
  - Complete current feature with original version
  - Adopt new version for **next** feature

**Version Detection:**

- Check version at top of document (line 3-4)
- Document version used in PR description: "Implemented per AGENTS.md v2.2"

**Version Upgrade Trigger:**

- New feature starts (new feature directory)
- Human explicitly requests: "Use AGENTS.md v2.3 for this feature"
- Critical bug fix in AGENTS.md requires immediate adoption (human will notify)

**Example:**

```text
Feature [001-user-auth] implementation started 2025-11-01 (AGENTS.md v2.2)
AGENTS.md v2.3 released 2025-11-05 (mid-feature)
Agent continues with v2.2 for feature [001-user-auth]
Feature [002-csv-export] implementation started 2025-11-10
Agent adopts v2.3 for feature [002-csv-export]
```

---

## 11. Glossary

**Acceptance Criteria** - Measurable conditions that must be met for a user story to be considered complete (defined in spec.md)

**Acceptance Scenario** - Given-When-Then test case in spec.md that defines success criteria

**Acceptance Testing** - Verification that all Given-When-Then scenarios in spec.md have corresponding passing tests (Section 6.2)

**Atomic Commit** - Single logical change implementing one user story or scenario

**Constitution** - Immutable project principles in `.specify/memory/constitution.md`

**Constitution Gate** - Yes/no compliance check in plan.md "Constitution Check" section. Gates are blockers; implementation cannot proceed if gate fails without explicit justification.

**Complexity Tracking** - Table in plan.md documenting Constitution violations with justification. Format: `| Violation | Why Needed | Simpler Alternative Rejected |`

**Deterministic** - Same specification input produces identical code output every time

**Feature Branch** - Git branch for implementing a specific feature, named `[###-feature-name]` matching the feature directory

**Feature Directory** - `specs/[###-feature-name]/` containing all feature-related documents

**Feature Directory Name** - Identifier format `[###-feature-name]` where `###` is a numeric ID and `feature-name` is descriptive (e.g., `001-user-auth`, `042-csv-export`)

**Given-When-Then** - Format for acceptance scenarios: "Given [context] When [action] Then [outcome]". Provides clear, testable specification of expected behavior.

**Idempotent** - Re-execution produces same result without side effects or duplication

**Implementation Plan** - `specs/[###-feature-name]/plan.md` defining technical architecture (HOW)

**Feature Specification** - `specs/[###-feature-name]/spec.md` defining requirements (WHAT/WHY)

**P1/P2/P3** - Priority levels for user stories in spec.md (P1 = highest priority, must-have; P2 = should-have; P3 = nice-to-have)

**Pre-Commit Validation** - Running formatters, linters, type checkers, and build verification before `git commit` (Section 6.1)

**Single Source of Truth** - Authoritative specification documents that all implementation derives from

**Standard PR Template** - Pull request description format defined in Section 5.6

**Supporting Documents** - Optional design artifacts: data-model.md, contracts/, research.md, quickstart.md, tasks.md

**Task States** - Status markers in tasks.md:

- `[ ]` **Pending:** Not yet started
- `[x]` **Complete:** Successfully implemented and tested
- `[F]` **Failed:** Implementation attempted but test failures or errors occurred
- `[B]` **Blocked:** Cannot start due to external dependency (API key, infrastructure, missing library)
- `[W]` **Waiting:** Implemented but awaiting human review/approval/feedback (different from blocked - code is ready, just needs sign-off)

**User Story** - High-level requirement in spec.md describing what user wants to accomplish and why. Format: "As a [user type], I want [goal] so that [benefit]". Contains acceptance scenarios that define success criteria.

---

*This document defines behavioral standards for AI agents in Spec-Driven Development projects using Spec Kit. All agents MUST internalize and honor these guidelines to maintain quality, consistency, and specification alignment.*
