# AI Agent Guidelines

**Version:** 2.4
**Last Updated:** 2025-11-13

---

## ⚠️ CRITICAL OPERATIONAL RULES (Read First)

### PowerShell Commands

**RULE 1**: Use semicolon (`;`) NOT double-ampersand (`&&`)
- ✅ `Get-Service 'ServiceA'; Stop-Service 'ServiceA'`
- ❌ `Get-Service 'ServiceA' && Stop-Service 'ServiceA'`

**RULE 2**: On execution policy errors, run TWO separate commands:
1. `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force`
2. Rerun original script

**WHY**: VSCode auto-approves individual commands. Chaining (`;` or `&&`) triggers approval prompts.

### Bash/Sh Commands

**RULE 3**: On permission errors, run TWO separate commands:
1. `chmod +x <script>`
2. Rerun original script

**WHY**: Same as PowerShell - individual commands auto-approved, chaining triggers prompts.

### File Operations

**RULE 4**: If inline edit fails → Use fallback strategy:
1. Recreate with full content using creation tool (preserve original filename)
2. **Preserve comments** - Keep ALL existing comments exactly as they were
3. **Precise edits only** - Make ONLY the required changes, do not modify unrelated sections

**Example**:

```text
❌ BAD: Recreate file and "clean up" unrelated code
✅ GOOD: Recreate file with exact original content + only the specific required change
```

**RULE 5**: Chain `mkdir` with semicolon: `mkdir folderA; mkdir folderB`

### Documentation Updates

**RULE 6**: After documentation changes:
1. Increment version number
2. Add entry to CHANGELOG.md (if `__init__.py` or `pyproject.toml` changed)

### Large File Generation

**RULE 7**: Files >1500 lines → Use chunked generation (300-800 lines per chunk)
- First chunk: Use Write tool
- Subsequent chunks: Use Edit tool (append mode)

---

## 1. Quick Reference

**Core Principle:** Specifications are the **single source of truth**. Never guess, always clarify.

**Document Priority:** Constitution > Spec > Plan > Supporting Docs

**Task States:** `[ ]` pending, `[x]` complete, `[F]` failed, `[B]` blocked, `[W]` waiting for approval

**Critical Rules:**

| DO | DON'T |
| ---- | ------- |
| Stop & emit `CLARIFICATION NEEDED` when unclear | Commit secrets/API keys/credentials |
| Follow Constitution at all times | Modify `.specify/` during implementation |
| Run formatters → linters → tests before commit | Add requirements not in specs |
| Update spec first if issues found | Proceed when spec is unclear |
| Mark tasks immediately after completion | Override human feedback without updated spec |

**RFC 2119 Keywords:** MUST/MUST NOT (mandatory), SHOULD/SHOULD NOT (recommended), MAY (optional)

**When Stuck - Decision Tree:**

```text
Problem → Action
├─ Spec unclear? → CLARIFICATION NEEDED (4.1), mark tasks [B], WAIT
├─ Test failed?
│  ├─ Syntax/typo? → Auto-fix max 2× (6.3)
│  ├─ Logic error? → Mark [F], REPORT, WAIT (6.3)
│  └─ Flaky? → Document, ESCALATE (6.3)
├─ Constitution conflict? → STOP, FLAG, WAIT (6.2)
├─ Missing dependency/file? → research.md, [B], ESCALATE (6.4)
├─ Version conflict? → CLARIFICATION NEEDED (4.4)
├─ License conflict? → research.md, suggest alternatives (8.2)
├─ Workflow command fails? → Check, retry 1×, escalate (2)
├─ Gate fails? → STOP, check plan.md justification (5.6)
└─ Git conflict? → abort, REPORT, WAIT (7.1)
```

---

## 2. Toolkit Intelligence

**Available Capabilities:** The toolkit provides cross-platform scripts (bash + PowerShell) for common operations. Agents SHOULD leverage these instead of implementing from scratch.

**Script Locations:**

- Bash: `.specify/scripts/bash/`
- PowerShell: `.specify/scripts/powershell/`

**Core Functions Available:**

| Function | Description | Bash | PowerShell |
| ---------- | ------------- | ------ | ------------ |
| Repository root detection | Gets project root (git or fallback) | `get_repo_root()` | `Get-RepoRoot` |
| Git detection | Checks if git is available | `has_git()` | `Test-HasGit` |
| Branch detection | Gets current branch or feature | `get_current_branch()` | `Get-CurrentBranch` |
| Feature paths | Gets all spec file paths | `get_feature_paths()` | `Get-FeaturePathsEnv` |
| File validation | Checks file existence | `check_file()` | `Test-FileExists` |

**Environment Variables:**

- `SPECIFY_FEATURE`: Override feature detection (useful for CI/CD)
- Standard git env vars (GIT_DIR, etc.) work as expected

**OS Detection:** Agents CAN detect OS from:

1. Bash presence → Unix-like (Linux/macOS)
2. PowerShell presence → Windows (or cross-platform)
3. Script file extensions in project (.sh → bash, .ps1 → PowerShell)

**Pre-commit Hooks:** Check for:

- `.pre-commit-config.yaml` (pre-commit framework)
- `.git/hooks/pre-commit` (manual hooks)
- `package.json` → `husky`, `lint-staged`
- `Makefile` → `pre-commit` or `lint` targets

**Workflow Commands:**

| Command | Output | Description |
| --------- | -------- | ------------- |
| `/speckitsmart.specify` | spec.md | Create spec from description |
| `/speckitsmart.clarify` | Updated spec.md | Resolve ambiguities |
| `/speckitsmart.plan` | plan.md + design docs | Generate architecture |
| `/speckitsmart.tasks` | tasks.md | Generate task list |
| `/speckitsmart.implement` | Code + tests | Execute tasks |
| `/speckitsmart.resume` | Restored context | Resume from state/tasks |

**Command Failure:** REPORT error → CHECK prerequisites → RETRY 1× (transient) → ESCALATE (persistent)

---

## 3. Document Structure & Priority

**Project Structure:**

```text
project-root/
├── .specify/memory/constitution.md    # Immutable principles
├── .specify/templates/                 # Templates
├── .specify/scripts/{bash,powershell}/ # Cross-platform scripts
└── specs/[###-feature-name]/
    ├── spec.md                         # WHAT/WHY (requirements)
    ├── plan.md                         # HOW (architecture)
    └── data-model.md, contracts/, research.md, quickstart.md, tasks.md
```

**Priority (Highest→Lowest):**

1. **Constitution** - Immutable project principles
2. **Spec** - Requirements (WHAT/WHY)
3. **Plan** - Architecture (HOW)
4. **Supporting Docs** - Sub-priority: data-model > contracts > research > quickstart > tasks

**Conflict Resolution:** STOP → emit `CLARIFICATION NEEDED` (cite conflicting sections) → DO NOT guess → WAIT for human + spec update

---

## 4. Core Responsibilities & Behavioral Principles

### 4.1 Ambiguity Protocol

**When unclear:** emit `CLARIFICATION NEEDED` with: Document+line, Question, Options (if any), Recommendation (if Constitution-aligned), Blocked tasks

**Scope Decision:**

| Ambiguity Type | Action |
| ---------------- | -------- |
| Fundamental (affects architecture) | STOP ALL WORK, WAIT |
| Isolated (affects one module) | STOP blocked tasks, CONTINUE others |
| Detail (affects one function) | CONTINUE, emit clarification for later |

**Multiple Ambiguities:** BATCH if found upfront. EMIT immediately + CONTINUE non-blocked if found during implementation.

### 4.2 Specification Interpretation

- **MUST** read in priority order (§3) before implementation
- **MUST** derive all logic from specs only - no assumptions, opinions, or undocumented requirements
- **SHOULD** cross-reference spec/plan/supporting docs for consistency
- **MUST NOT** add dependencies, libraries, or features not in specs

**Context Window Management:** If docs exceed capacity: (1) read Constitution+Spec+Plan fully, (2) load supporting docs on-demand, (3) emit warning, (4) reserve 30%/40%/30% for docs/code/history. **If mandatory docs don't fit:** STOP, emit `CONTEXT OVERFLOW`, suggest splitting, WAIT.

**Binary Files:** If spec references images/PDFs: emit warning, REQUEST text description in spec/plan, DO NOT proceed with assumptions.

### 4.3 Code Generation Standards

**MUST** generate code that is:

- **Functionally Deterministic:** Same spec → same behavior (timestamps/UUIDs in metadata may vary)
- **Idempotent:** Re-execution doesn't duplicate or corrupt state
- **Production-ready:** Compiles, passes all tests, follows project conventions
- **Traceable:** Links to spec sections via comments and commit messages

**Randomness Seeds (priority order):** (1) Explicit in spec/plan, (2) Hash of feature dir name, (3) Fixed constant (e.g., 0)

**Output:** All artifacts specified in plan + tests for every acceptance scenario

**Code Reuse (MUST):**

- **MUST** search for existing methods/functions before creating new ones
- **MUST** refactor to enable reuse when duplicate logic is detected
- **MUST** extract common patterns into shared utilities
- **SHOULD** document reusable components for discoverability

**Inline Documentation (MUST/MUST NOT):**

**MUST document:**

- Classes: Purpose and responsibilities
- Important methods: Non-obvious behavior, business logic, complex algorithms
- Complex logic: WHY (intent/rationale), not WHAT (implementation)
- Business rules: References to spec sections or business requirements

**MUST NOT document:**

- Entities, DTOs, POCOs, data models (self-documenting via naming)
- Trivial getters/setters or simple property accessors
- Obvious implementations (simple CRUD operations, standard patterns)
- Implementation details that are clear from reading the code

**Documentation Style:** Explain intent and rationale (WHY), not mechanics (WHAT). Example: `// Cache invalidation required per GDPR data retention policy (spec.md L45)` NOT `// This function clears the cache`

### 4.4 Minimal Changes

**Small Commits:** 1 scenario/story per commit, 1-5 files, <300 lines

**Exceptions (>300 lines OK):** Generated code, migrations, test fixtures, initial scaffolding, lockfiles

**Partial Implementation:** MAY ship incremental user stories. MUST NOT ship half-implemented (broken) code. CAN ship `[B]` blocked with research.md documentation. CANNOT ship `[F]` failed.

### 4.5 Dependency Management

**Build Files:** IF plan mentions → follow. IF spec requires dependency → MAY add + document in research.md. IF neither → CLARIFICATION NEEDED.

**Conflict Detection:** CHECK existing versions → DETECT conflicts → emit `CLARIFICATION NEEDED` (current vs required, compatibility, options) → PREFER existing if compatible.

**Version Selection (when spec/plan doesn't specify):**

- **MUST** default to latest LTS (Long-Term Support) versions for languages and frameworks
- **MUST** state version chosen in plan.md and reasoning: "Using Node.js 20 LTS (latest stable LTS as of 2025-01-08)"
- **SHOULD** check project constraints first: existing dependencies, platform requirements, team familiarity
- **SHOULD** prefer even-numbered versions for Node.js (LTS releases: 18, 20, 22, etc.)
- **MAY** use current stable version for libraries without explicit LTS designation
- **MUST NOT** use pre-release, beta, or nightly versions without explicit spec approval

**LTS Examples:**

- Node.js: 20.x (LTS), 22.x (LTS) - prefer latest LTS
- Python: 3.11, 3.12 - prefer latest stable
- Java: 17 (LTS), 21 (LTS) - prefer latest LTS
- .NET: 6.0 (LTS), 8.0 (LTS) - prefer latest LTS
- React: Latest stable major version (no formal LTS)
- PostgreSQL: Latest stable major version

### 4.6 Read-Only Defaults & Guardrails

**Allowed:** `src/`, `tests/`, dev configs (`/config/{dev,test,local,development,staging}.*`), build files (package.json, Cargo.toml, pyproject.toml, go.mod, pom.xml, build.gradle, Makefile)

**Prohibited:** `.specify/*`, `specs/[###-name]/*.md`, production configs (`/config/*.{production,prod}.*`), dependencies (node_modules, .venv, target, build), `.git`, system files

**Exception:** Changes with explicit plan.md justification in "Complexity Tracking" section.

### 4.7 Traceability & Rationale

**MUST** link to spec sections:

- **Commit Message:** `Implement [###-name]: Story 2, Scenario 1\n- Adds X per spec.md L67-72\nRefs: specs/[###-name]/spec.md`
- **Code Comments:** `# Implements spec.md Story 2, Scenario 1: CSV export (plan.md 3.4)`

**PR Template Must Include:** Feature name, Spec/Plan paths, Status (✅/⏳ user stories), Constitution Compliance (gates + coverage ≥80% line, 100% scenario), Acceptance Testing results, How to Test (→quickstart.md)

### 4.8 Constitution Compliance

**MUST** follow all Constitution articles. **If conflict:** STOP → FLAG (article, spec requirement, conflict reason) → DO NOT proceed → WAIT for human decision.

**Resolution:** (A) Human updates spec to align, OR (B) Human adds justification to plan.md Complexity Tracking

---

## 5. Quality & Verification

### 5.1 Pre-Commit Validation

**MUST run before every commit:** Formatters → linters → type checkers → build verification

**No hooks?** Check configs → run manually → document missing automation in research.md → suggest adding hooks in PR comments

### 5.2 Acceptance Testing

**For each Given-When-Then:** Test code that (1) sets up Given, (2) executes When, (3) asserts Then

**Failure Policy:** Fix all scenarios for current story before marking complete. MAY proceed to next story if current passes. MUST NOT ship PR with failing scenarios. **Priority:** P1 before P2/P3.

**Time-Dependent Tests:** MUST use mocking (freezegun, Sinon, timecop, Clock). Document in plan.md. **NO real sleeps or wall-clock dependencies.**

### 5.3 Contract, Data Model & Quickstart Compliance

| Document | Verification Required |
| ---------- | ---------------------- |
| contracts/ | Compare endpoints to definitions, validate schemas exactly, test error responses, verify auth |
| data-model.md | Verify migrations/models/validation/relationships match schemas |
| quickstart.md | Follow steps exactly, verify outputs, test edge cases |

**Tools (SHOULD use if available):** OpenAPI (Spectral, Redocly), GraphQL (graphql-inspector), REST (Pact)

### 5.4 Constitution Gates

**Common Gates:** Library-First, CLI Interface, Test-First, Simplicity, Anti-Abstraction, Integration-First

**Gate fail = BLOCKER.** MUST NOT proceed without plan.md "Complexity Tracking" justification.

**Custom Gates (non-Constitution):** Verify same as Constitution gates. Treat as blocker unless marked "SHOULD"/"aspirational". Report in PR.

### 5.5 Fail Fast

**On any blocker:** STOP → REPORT (test/build failed, error, affected tasks) → UPDATE tasks.md with `[F]` or `[B]` → EMIT issue → WAIT

**Report to:** Console (interactive), CI log (automated), tasks.md comments (async)

---

## 6. Violation Handling & Recovery

**Pattern:** Trigger → Response → Recovery

### 6.1 Specification Violations

| Trigger | Response | Recovery |
| --------- | ---------- | ---------- |
| Spec ambiguous/contradictory | STOP (per §4.1 scope table) → CLARIFICATION NEEDED → WAIT | Human updates spec → re-read → validate → resume |
| Spec incomplete | Same as ambiguous | Same as ambiguous |

**Detection (git):** Poll `git log -1 spec.md` every 5min for updates

### 6.2 Constitutional Violations

| Trigger | Response | Recovery |
| --------- | ---------- | ---------- |
| Spec conflicts Constitution | STOP all → FLAG (article, requirement, conflict) → WAIT | Human updates spec OR adds plan.md justification |
| Constitution article ambiguous | STOP → CONSTITUTION AMBIGUITY (article, question, situation, interpretations) → WAIT | Human clarifies (constitution.md note or message) → proceed |

### 6.3 Quality Failures

**Test/Build Failures:**

| Error Type | Response | Recovery |
| ------------ | ---------- | ---------- |
| Obvious (syntax, imports, typos) | Auto-fix max 2× | Fix + retest + resume (if ≤2 attempts) |
| Ambiguous (logic, assertions) | Mark `[F]`, WAIT | Human diagnosis + fix + retest |
| Spec issue (requirements wrong) | CLARIFICATION NEEDED | Human updates spec + regenerate |
| Flaky (non-deterministic) | DOCUMENT in research.md → mark `[F]` → ESCALATE | Human fixes root cause (races, timeouts, network deps) |

**Flaky Test Documentation:** Test name, evidence (logs), root cause hypothesis, recommendations. **DO NOT:** retry >2×, mark passed, ignore.

### 6.4 Technical Blockers

**Types:** Missing dependencies/credentials, missing/renamed files, platform incompatibility

**Response:** DOCUMENT in research.md (blocker, blocked tasks, description, impact, alternatives, recommendation, status) → UPDATE tasks.md `[B]` → SUGGEST alternatives → ESCALATE

**Missing Files:** SEARCH similar (fuzzy) → IF found: `CLARIFICATION NEEDED` (similar files, question) → IF not: `CLARIFICATION NEEDED` (should create or path wrong?) → DO NOT create without confirmation.

**Recovery:** Human provides dependency/API/credentials → validate available → resume

---

## 7. Collaboration Protocol

### 7.1 Version Control

**Commit Rules:**

- **MUST** atomic commits (1 story/scenario)
- **MUST** commit after validation passes (§5.1)
- **MUST** reference feature + spec sections
- **MUST** work on feature branch `[###-feature-name]`
- **SHOULD** 1 task at a time (MAY parallel if no shared deps/files)

**Timing:** Complete task → mark `[x]` → validate → IF pass: commit, IF fail: fix + repeat

**Merge Conflicts:** git abort → REPORT (files, local/remote changes) → DO NOT resolve → WAIT

**Rollback:** DO NOT delete branch → PREFER fix commits → WAIT for direction before force-push/delete

### 7.2 Change Communication & Feedback Loop

**MUST** update design docs when trade-offs occur. **MUST** document decisions in research.md: Chosen approach, Rationale, Alternatives (rejected + why), Trade-offs, References.

**MUST** update spec first if issues found. **MUST NOT** override human feedback without updated spec.

**Regeneration Strategy:**

| Spec Change | Strategy | Action |
| ------------- | ---------- | -------- |
| Requirements added | Incremental | Add new code, keep existing |
| Requirements modified | Selective | Regen affected functions/classes only |
| Architecture changed | Full | Regen entire modules from scratch |
| Data model changed | Full | Regen models, migrations, dependencies |
| Acceptance criteria changed | Test-first | Regen tests → update impl to pass |

**Workflow:** Identify scope → backup (git commit) → regen tests → regen impl → validate → IF fail: fix or repeat

---

## 8. Ethics & Safety

### 8.1 Prohibited Actions

**MUST NOT:** Commit secrets/keys/tokens/passwords, share PII in logs, make undisclosed network calls, exfiltrate data

**Detection (MUST run):** Scanners (git-secrets, truffleHog, gitleaks, detect-secrets), validate no hardcoded credentials (patterns: `password=`, `api_key=`, `token=`, `secret=`, `private_key=`), check data leaks

**SHOULD:** Use `.gitignore` for sensitive files (`.env`, `credentials.json`, `*.pem`, `*.key`, `secrets.yml`)

### 8.2 Licensing & Standards

**MUST** respect licenses. **SHOULD** prefer permissive (MIT, Apache, BSD). **MUST NOT** include closed-source without approval.

**License Conflicts:** STOP → DOCUMENT in research.md (library+license, Constitution requirement, why needed) → SUGGEST compatible alternatives → ESCALATE → WAIT

**Standards:** SHOULD prefer open standards (JSON > binary), portable code. MUST document platform deps in plan.md if unavoidable.

---

## 9. Meta-Guidelines

### 9.1 Document Errors

**IF** error in AGENTS.md: EMIT `DOCUMENT ERROR` (location, issue, impact, severity) → CONTINUE implementation → LOG for human. **DO NOT:** stop for minor errors, attempt fix, ignore severe contradictions.

### 9.2 Version Management

**MUST** use version at **start of feature** implementation. **DO NOT** switch mid-feature.

**Upgrade triggers:** New feature starts, human requests, critical bug fix (human notifies)

**Detection:** Check lines 3-4 of this file. Document in PR: `Implemented per AGENTS.md v2.4`

---

## 10. Glossary

| Term | Definition |
| ------ | ------------ |
| **Acceptance Criteria** | Measurable conditions for user story completion (spec.md) |
| **Acceptance Scenario** | Given-When-Then test case defining success criteria |
| **Atomic Commit** | Single logical change implementing 1 story/scenario |
| **Constitution** | Immutable project principles (`.specify/memory/constitution.md`) |
| **Constitution Gate** | Yes/no compliance check (plan.md). Failure = blocker without justification |
| **Complexity Tracking** | Table in plan.md: `Violation │ Why Needed │ Simpler Alternative Rejected` |
| **Deterministic** | Same spec → functionally equivalent code (behavior identical) |
| **Feature Branch** | Git branch `[###-feature-name]` for specific feature |
| **Feature Directory** | `specs/[###-feature-name]/` containing all feature docs |
| **Given-When-Then** | Scenario format: "Given [context] When [action] Then [outcome]" |
| **Idempotent** | Re-execution produces same result without side effects |
| **Implementation Plan** | `plan.md` defining HOW (technical architecture) |
| **Feature Specification** | `spec.md` defining WHAT/WHY (requirements) |
| **P1/P2/P3** | Priority levels (P1=must-have, P2=should-have, P3=nice-to-have) |
| **Pre-Commit Validation** | Formatters → linters → type checkers → build before commit |
| **Single Source of Truth** | Authoritative specification documents |
| **Supporting Documents** | Optional artifacts: data-model, contracts, research, quickstart, tasks |
| **Task States** | `[ ]` pending, `[x]` complete, `[F]` failed, `[B]` blocked, `[W]` waiting |
| **User Story** | High-level requirement: "As [user], I want [goal] so that [benefit]" |

---

## 11. Codebase Indexing & Knowledge Base

**New in v1.0.0**: Spec Kit now includes powerful codebase indexing capabilities that dramatically improve code analysis, reverse engineering, and implementation quality.

### 11.1 Overview

The indexing system creates a searchable, structured representation of your codebase that enables:

- **10x faster reverse engineering** - Pre-extracted architecture instead of reading every file
- **40-60% code reuse** - Automatic detection of duplicate implementations
- **80% token reduction** - Grounded context instead of full file reads
- **Better accuracy** - AST-based understanding vs regex patterns

### 11.2 New Commands

#### 11.2.1 `/speckitsmart.index` - Build Codebase Index

**Purpose:** Create searchable index of code structure, data models, and APIs

**When to use:**
- **FIRST STEP**: Run before `/speckitsmart.analyze-project` (required prerequisite)
- After major code changes (new modules, refactoring)
- Weekly for active projects

**Basic usage:**
```bash
# First time - full index
/speckitsmart.index

# Update after changes - incremental (fast)
/speckitsmart.index --incremental

# Index specific directory
/speckitsmart.index --path src/

# Verbose output
/speckitsmart.index --verbose
```

**What gets indexed:**
- ✅ Code structure (classes, functions, interfaces)
- ✅ Data models (database schemas, ORM entities, TypeScript types)
- ✅ API endpoints (REST, GraphQL, WebSocket)
- ✅ External APIs (Stripe, AWS, third-party services)
- ✅ Dependencies (imports, exports, call graphs)

**Output:** `.analysis/index/` directory

**Performance:** 30-60 seconds for typical projects

---

#### 11.2.2 `/speckitsmart.wiki` - Generate Documentation

**Purpose:** Auto-generate comprehensive documentation (DeepWiki) from index

**Prerequisite:** **REQUIRES** index (run `/speckitsmart.index` first)

**Basic usage:**
```bash
# Generate all documentation
/speckitsmart.wiki

# Generate specific tiers
/speckitsmart.wiki --tiers 1,2
```

**Output:** `.deepwiki/` directory containing:
- `overview.md` - What is this repo?
- `functional-summary.md` - Problems it solves
- `architecture/` - Architecture diagrams and details
- `modules/` - Per-module documentation
- `api-reference/` - API endpoint documentation

**Use cases:**
- Onboarding new team members
- Architecture documentation
- API documentation
- Understanding legacy code

---

#### 11.2.3 `/speckitsmart.ask` - Query Codebase

**Purpose:** Ask questions about codebase using natural language

**Prerequisites:** **REQUIRES** index, optionally DeepWiki for better answers

**Basic usage:**
```bash
# Ask about functionality
/speckitsmart.ask "How does authentication work?"

# Ask about data
/speckitsmart.ask "What database tables exist?"

# Ask about APIs
/speckitsmart.ask "Show me all user management endpoints"

# Ask about integrations
/speckitsmart.ask "What third-party services does this use?"
```

**Response includes:**
- Clear explanation with code examples
- File paths and line numbers
- Related information
- Source citations

**Benefits:**
- Get answers in seconds vs reading code for hours
- Grounded in actual codebase (no hallucinations)
- Links to source code for verification

---

### 11.3 Updated Workflow

**Old workflow:**
```
1. /speckitsmart.analyze-project  ← Slow, read every file
2. /speckitsmart.specify
3. /speckitsmart.implement
```

**New workflow (REQUIRED):**
```
1. /speckitsmart.index              ← NEW: Build index first (30-60s)
2. /speckitsmart.analyze-project    ← 10x faster with index
3. /speckitsmart.wiki               ← NEW: Generate docs (optional)
4. /speckitsmart.ask                ← NEW: Q&A during development (optional)
5. /speckitsmart.specify
6. /speckitsmart.implement          ← Enhanced with code reuse checks
```

### 11.4 Prerequisite Requirements

**CRITICAL RULE:** Always check prerequisites before command execution

#### Commands that REQUIRE index (MUST have index, will FAIL without):

**`/speckitsmart.analyze-project`**
- **Behavior:** STOP execution if index missing
- **Check:** Run `check-index-prerequisite.sh` first
- **Error message:** Display clear error with solution
- **Action:** EXIT immediately, do NOT proceed

**`/speckitsmart.wiki`**
- **Behavior:** STOP execution if index missing
- **Check:** Run `check-index-prerequisite.sh` first
- **Error message:** "Index required for documentation generation"
- **Action:** EXIT immediately, do NOT proceed

**`/speckitsmart.ask`**
- **Behavior:** STOP execution if index missing
- **Check:** Run `check-index-prerequisite.sh` first
- **Error message:** "Index required to answer questions"
- **Action:** EXIT immediately, do NOT proceed

**Prerequisite Check Output:**
```json
{
  "index_exists": false,
  "error": "Index not found at .analysis/index"
}
```

**IF `index_exists: false` → MUST display:**
```
❌ ERROR: Codebase index not found

This command requires a codebase index.

🔧 Solution:
Run this command first:
  /speckitsmart.index

Estimated time: 30-60 seconds

Then re-run: /speckitsmart.[command]
```

**STOP EXECUTION. DO NOT PROCEED.**

**IF `index_exists: true` but `is_stale: true` (>7 days old):**
```
⚠️ WARNING: Index is stale (last updated N days ago)

Results may not reflect recent code changes.

Recommendation: Update index (takes 5-10 seconds):
  /speckitsmart.index --incremental

Continue with stale index? (Press Enter to continue, Ctrl+C to abort)
```

**WAIT for user confirmation, then proceed.**

---

#### Commands with OPTIONAL index (SHOULD have, warns but continues):

**`/speckitsmart.implement`**
- **Behavior:** WARN if index missing, but CONTINUE
- **Check:** Run `check-index-optional.sh` first
- **Warning message:** Display benefits but allow continuation
- **Action:** SKIP reusability checks, proceed with standard implementation

**Optional Check Output:**
```json
{
  "index_available": false,
  "message": "Code reusability checks disabled"
}
```

**IF `index_available: false` → SHOULD display:**
```
⚠️ Codebase index not available

Proceeding without code reusability checks.

Missing benefits:
  ✗ 40-60% code reuse (avoid duplicate implementations)
  ✗ Automatic detection of existing utilities
  ✗ Consistent architecture patterns
  ✗ 80% token reduction in AI queries

💡 To enable these features:
   1. Pause (optional)
   2. Run: /speckitsmart.index (30-60 seconds)
   3. Re-run: /speckitsmart.implement

⏭️ Proceeding without index...
```

**CONTINUE with standard implementation (no reusability checks).**

---

### 11.5 Code Reusability with Index

**WHEN index available during `/speckitsmart.implement`:**

**For EACH task in tasks.md, BEFORE implementing:**

1. **Query index** for reusable code:
   ```bash
   find-reusable-code.sh "TASK_DESCRIPTION"
   ```

2. **Review suggestions:**
   ```json
   {
     "existing_implementations": [
       {
         "file": "src/auth/jwt.ts",
         "function": "validateJWT",
         "similarity": 0.92,
         "recommendation": "⚠️ HIGH MATCH - Reuse instead of reimplementing"
       }
     ],
     "reusable_utilities": [
       {
         "file": "src/utils/crypto.ts",
         "exports": ["hashPassword", "verifyPassword"],
         "recommendation": "Use these crypto utilities"
       }
     ],
     "architecture_patterns": [
       {
         "pattern": "Middleware Pattern",
         "examples": ["src/middleware/authenticate.ts"],
         "recommendation": "Follow this pattern"
       }
     ]
   }
   ```

3. **Display to developer:**
   ```
   📋 Task: Implement JWT validation

   🔍 Reusability Check:
   ⚠️ EXISTING IMPLEMENTATION FOUND (92% match)
      File: src/auth/jwt.ts:45
      Function: validateJWT
      Recommendation: REUSE THIS - Don't reimplement

   ✓ Utilities: src/utils/crypto.ts
   ✓ Pattern: Middleware (see: src/middleware/authenticate.ts)
   ```

4. **Follow suggestions in implementation:**
   ```typescript
   // ✅ GOOD: Reusing existing
   import { validateJWT } from '@/auth/jwt';

   export const authMiddleware = async (req, res, next) => {
     const token = req.headers.authorization?.split(' ')[1];
     const payload = await validateJWT(token);  // Reusing!
     req.user = payload;
     next();
   };

   // ❌ BAD: Reimplementing (ignoring index suggestion)
   export const authMiddleware = async (req, res, next) => {
     const token = req.headers.authorization?.split(' ')[1];
     const payload = jwt.verify(token, secret);  // Duplicate!
     req.user = payload;
     next();
   };
   ```

**RULE:** MUST check index before implementing. SHOULD reuse when similarity >80%.

---

### 11.6 Index Maintenance

**Freshness levels:**
- **Fresh:** <24 hours old (optimal)
- **Valid:** <7 days old (good)
- **Stale:** >7 days old (warn user, suggest update)
- **Very stale:** >30 days old (strongly recommend rebuild)

**Update commands:**
```bash
# Quick incremental update (5-10 seconds)
/speckitsmart.index --incremental

# Full rebuild (30-60 seconds)
/speckitsmart.index --full
```

**Automatic update triggers:**
- `/speckitsmart.analyze-project` checks freshness (warns if stale)
- `/speckitsmart.implement` MAY trigger incremental update after major tasks

---

### 11.7 Best Practices

**DO:**
- ✅ **Always** run `/speckitsmart.index` before analysis
- ✅ Keep index fresh (update weekly or after major changes)
- ✅ Use `/speckitsmart.ask` to understand code before modifying
- ✅ Follow reusability suggestions (avoid duplicates)
- ✅ Generate DeepWiki for team onboarding

**DON'T:**
- ❌ Skip indexing and run analyze-project (will fail)
- ❌ Ignore reusability suggestions (causes duplicate code)
- ❌ Let index become very stale (>30 days)
- ❌ Commit `.analysis/index/` to git (auto-gitignored)

---

### 11.8 Troubleshooting

**Q: analyze-project fails with "index not found"**
A: Run `/speckitsmart.index` first. It's a required prerequisite.

**Q: How much disk space does index use?**
A: ~1-10MB for most projects (<1% of codebase size)

**Q: How long does indexing take?**
A: 30-60 seconds for typical projects, 2-5 minutes for large codebases (10K+ files)

**Q: Does index work with all languages?**
A: Phase 1 supports TypeScript, JavaScript, Python, Java, C#, Go

**Q: Is index committed to git?**
A: No. `.analysis/index/` is auto-gitignored. Each developer builds locally.

**Q: What if indexing fails?**
A: Run with `--verbose` to see details. Common issues:
   - Syntax errors in code → Use `--skip-invalid`
   - Large files → Increase `--max-file-size`
   - Permission issues → Check `.analysis/` write access

**Q: Can I skip indexing?**
A: No for analyze-project, wiki, ask (hard requirement). Yes for implement (soft warning).

---

### 11.9 Performance Expectations

| Codebase Size | Index Build | Incremental Update |
|---------------|-------------|-------------------|
| Small (<1K files) | 5-10s | 1-2s |
| Medium (1K-10K) | 30-60s | 3-5s |
| Large (10K-50K) | 2-5min | 10-20s |
| Very Large (>50K) | 10-30min | 30-60s |

---

### 11.10 Security & Privacy

**What gets indexed:**
- ✅ Code structure and patterns
- ✅ API endpoint definitions
- ✅ Data model schemas
- ✅ Environment variable **names** (not values)

**What does NOT get indexed:**
- ❌ Secrets or API keys (redacted if found)
- ❌ Runtime values
- ❌ User data
- ❌ Passwords or credentials

**Security guarantees:**
- Index is **local-only** (never uploaded to external services)
- Automatically **gitignored**
- All processing happens **on your machine**
- No telemetry or analytics
- Safe for proprietary code

**MUST NOT:** Commit index to git, share index externally, include secrets in code

---

*AI agents MUST internalize and follow these guidelines for quality, consistency, and specification alignment in Spec-Driven Development projects using Spec Kit.*
