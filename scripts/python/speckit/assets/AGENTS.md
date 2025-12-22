# AI Agent Guidelines

**Version:** 3.0

---

## ⚠️ CRITICAL OPERATIONAL RULES (Read First)

### CLI Commands

**RULE 1**: Use the `speckitadv` Python CLI for all workflow operations
- The CLI embeds all prompts and templates
- CLI outputs progressive prompts (50-80 lines per stage)
- Follow CLI instructions exactly

**RULE 2**: Chain ID persistence
- Save the chain ID returned by stage commands
- Pass chain ID to subsequent stages: `speckitadv <command> --stage=N --chain=<id>`

### File Operations

**RULE 3**: If inline edit fails → Use fallback strategy:
1. Recreate with full content using creation tool (preserve original filename)
2. **Preserve comments** - Keep ALL existing comments exactly as they were
3. **Precise edits only** - Make ONLY the required changes, do not modify unrelated sections

**Example**:

```text
❌ BAD: Recreate file and "clean up" unrelated code
✅ GOOD: Recreate file with exact original content + only the specific required change
```

**RULE 4**: Chain `mkdir` with semicolon: `mkdir folderA; mkdir folderB`

### Documentation Updates

**RULE 5**: After documentation changes:
1. Increment version number
2. Add entry to CHANGELOG.md (if `__init__.py` or `pyproject.toml` changed)

### Large File Generation

**RULE 6**: Files >1500 lines → Use chunked generation (300-800 lines per chunk)
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
| Follow Constitution at all times | Modify `memory/` during implementation |
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

**Available Capabilities:** The toolkit provides the `speckitadv` Python CLI for all workflow operations. The CLI embeds all prompts, templates, and logic.

**CLI Commands:**

| Command | Stages | Description |
| ------- | ------ | ----------- |
| `speckitadv analyze-project` | 9+ | Analyze existing project for modernization |
| `speckitadv constitution` | 3 | Create project constitution |
| `speckitadv specify` | 6 | Create baseline specification |
| `speckitadv plan` | 4 | Create implementation plan |
| `speckitadv tasks` | 4 | Generate actionable tasks |
| `speckitadv implement` | 5 | Execute implementation |
| `speckitadv clarify` | 3 | Ask structured questions |
| `speckitadv checklist` | 3 | Generate quality checklist |

**Progressive Prompt Injection:**

Each command runs in stages. The CLI outputs focused prompts (50-80 lines) per stage:

```bash
# Example: constitution workflow
speckitadv constitution --stage=1
speckitadv constitution --stage=2 --defaults  # or --principles="..."
speckitadv constitution --stage=3

# Example: analyze-project workflow (uses --chain for state)
speckitadv analyze-project --stage=1 --path=/project --scope=A
speckitadv analyze-project --stage=2 --chain=abc12345
```

**Command Options:** Each command has different options. Use `--help` to see valid options:

```bash
speckitadv constitution --help   # Shows: --stage, --principles, --defaults
speckitadv analyze-project --help # Shows: --stage, --chain, --path, --scope, etc.
```

**Debug Commands:**

| Command | Description |
| ------- | ----------- |
| `speckitadv list-fragments <command>` | List available stages for a command |
| `speckitadv show-fragment <command> <stage>` | Show stage prompt content |

**Pre-commit Hooks:** Check for:

- `.pre-commit-config.yaml` (pre-commit framework)
- `.git/hooks/pre-commit` (manual hooks)
- `package.json` → `husky`, `lint-staged`
- `Makefile` → `pre-commit` or `lint` targets

**Command Failure:** REPORT error → CHECK prerequisites → RETRY 1× (transient) → ESCALATE (persistent)

---

## 3. Document Structure & Priority

**Project Structure:** `memory/` (config.json, constitution.md), `.guidelines/`, `specs/[###-feature-name]/` (spec.md, plan.md, data-model.md, contracts/, research.md, quickstart.md, tasks.md)

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

**Inline Documentation:**

| MUST Document | MUST NOT Document |
| ------------- | ----------------- |
| Classes (purpose, responsibilities) | Entities/DTOs/POCOs (self-documenting) |
| Important methods (non-obvious behavior, business logic) | Trivial getters/setters |
| Complex logic (WHY, not WHAT) | Obvious implementations (CRUD, standard patterns) |
| Business rules (spec references) | Clear implementation details |

**Style:** Explain intent (WHY), not mechanics (WHAT). Example: `// Cache invalidation per GDPR policy (spec.md L45)` NOT `// clears cache`

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

**LTS Examples:** Node.js 20/22, Python 3.11/3.12, Java 17/21, .NET 6/8 - always prefer latest LTS.

### 4.6 Read-Only Defaults & Guardrails

**Allowed:** `src/`, `tests/`, dev configs (`/config/{dev,test,local,development,staging}.*`), build files (package.json, Cargo.toml, pyproject.toml, go.mod, pom.xml, build.gradle, Makefile)

**Prohibited:** `memory/*`, `specs/[###-name]/*.md`, production configs (`/config/*.{production,prod}.*`), dependencies (node_modules, .venv, target, build), `.git`, system files

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
| **Constitution** | Immutable project principles (`memory/constitution.md`) |
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

*AI agents MUST internalize and follow these guidelines for quality, consistency, and specification alignment in Spec-Driven Development projects using Spec Kit.*
