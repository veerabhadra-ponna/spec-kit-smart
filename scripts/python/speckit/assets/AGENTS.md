# AI Agent Guidelines

**Version:** 3.4

---

## Critical Rules

| Rule | Description |
|------|-------------|
| **CLI First** | Use `speckitadv` Python CLI for all workflow operations - it embeds prompts/templates |
| **State Auto-Detection** | After stage 2, CLI auto-detects stage and folder from `specs/{feature}/.state/state.json` |
| **File Edit Fallback** | If inline edit fails: recreate with full content, preserve ALL comments, make ONLY required changes |
| **Chain mkdir** | Use semicolon: `mkdir folderA; mkdir folderB` |
| **Doc Updates** | Increment version, add CHANGELOG entry if `__init__.py` or `pyproject.toml` changed |
| **Large Files** | >1500 lines → chunked generation (300-800 lines/chunk) |
| **No Backward Compatibility** | System is pre-release; breaking changes are allowed. Do not add legacy mappings or compatibility shims. |

---

## Quick Reference

**Core Principle:** Specifications are the **single source of truth**. Never guess, always clarify.

**Priority:** Constitution > Spec > Plan > Supporting Docs

**Task States:** `[ ]` pending, `[x]` complete, `[F]` failed, `[B]` blocked, `[W]` waiting

| DO | DON'T |
|----|-------|
| Stop & emit `CLARIFICATION NEEDED` when unclear | Commit secrets/API keys/credentials |
| Follow Constitution at all times | Modify `memory/` during implementation |
| Run formatters → linters → tests before commit | Add requirements not in specs |
| Update spec first if issues found | Proceed when spec is unclear |

**RFC 2119:** MUST/MUST NOT (mandatory), SHOULD/SHOULD NOT (recommended), MAY (optional)

**Decision Tree:**

| Problem | Action |
|---------|--------|
| Spec unclear? | CLARIFICATION NEEDED, mark [B], WAIT |
| Test failed (syntax)? | Auto-fix max 2× |
| Test failed (logic)? | Mark [F], REPORT, WAIT |
| Constitution conflict? | STOP, FLAG, WAIT |
| Missing dependency? | research.md, [B], ESCALATE |

---

## CLI Commands

| Command | Stages | Description |
|---------|--------|-------------|
| `analyze-project` | 9+ | Analyze existing project for modernization |
| `constitution` | 3 | Create project constitution |
| `specify` | 6 | Create baseline specification |
| `plan` | 4 | Create implementation plan |
| `tasks` | 4 | Generate actionable tasks |
| `implement` | 5 | Execute implementation |
| `clarify` | 3 | Ask structured questions |
| `checklist` | 3 | Generate quality checklist |

**State Locations:**

| Command | State Location |
|---------|----------------|
| `analyze-project` | `.analysis/{project}-{timestamp}/state.json` |
| `constitution` | `memory/constitution.md` (file existence) |
| `specify`, `plan`, `tasks`, `implement` | `specs/{feature}/.state/state.json` |

**Usage:** After state created (stage 3+), just run `speckitadv <command>` - auto-detects stage/folder.

---

## CLI Utility Commands (for analyze-project)

These deterministic commands allow AI agents to write artifacts and query context without ad-hoc file operations.

### Artifact Writing

| Command | Purpose | Example |
|---------|---------|---------|
| `write-data` | Write JSON to `data/` folder | `speckitadv write-data category-patterns.json --content '{"patterns": [...]}'` |
| `write-report` | Write/append Markdown to `reports/` | `speckitadv write-report analysis-report.md --content '# Report...'` |
| `update-stage` | Update stage status in state.json | `speckitadv update-stage 02a-category-scan --status completed --artifacts file.json` |
| `update-preferences` | Store Q1-Q10 modernization preferences | `speckitadv update-preferences '{"q1_language": {"value": "Java 21"}, ...}'` |

### Context Queries

| Command | Purpose | Example |
|---------|---------|---------|
| `get-context` | Get render context for prompts | `speckitadv get-context --field scope` |
| `file-stats` | Get file info (lines, size, patterns) | `speckitadv file-stats reports/analysis-report.md --pattern "^##"` |
| `list-files` | Find files by pattern or category | `speckitadv list-files --pattern "**/*Service*.cs" --limit 50` |

### Valid Preference Keys (Q1-Q10)

```text
q1_language, q2_database, q3_message_bus, q4_package_manager,
q5_deployment, q6_iac, q7_containerization, q8_observability,
q9_security, q10_testing
```

### File Categories for list-files

```text
controllers, services, models, repositories, handlers, middleware,
config, tests, views, utilities, migrations
```

---

## Document Structure

**Priority (Highest→Lowest):**
1. Constitution - Immutable project principles
2. Spec - Requirements (WHAT/WHY)
3. Plan - Architecture (HOW)
4. Supporting Docs - data-model > contracts > research > quickstart > tasks

**Conflict:** STOP → `CLARIFICATION NEEDED` (cite sections) → WAIT

---

## Core Responsibilities

### Ambiguity Protocol

| Type | Action |
|------|--------|
| Fundamental (architecture) | STOP ALL, WAIT |
| Isolated (one module) | STOP blocked, CONTINUE others |
| Detail (one function) | CONTINUE, emit clarification later |

### Code Generation

**MUST generate code that is:**
- Functionally deterministic
- Idempotent
- Production-ready (compiles, passes tests)
- Traceable (links to spec via comments)

**Code Reuse:** MUST search existing methods before creating new. Extract common patterns.

**Documentation:**

| MUST Document | MUST NOT Document |
|---------------|-------------------|
| Classes (purpose) | Entities/DTOs |
| Important methods (business logic) | Trivial getters/setters |
| Complex logic (WHY) | Obvious implementations |

### Commits

**Small Commits:** 1 scenario/story, 1-5 files, <300 lines

**Exceptions:** Generated code, migrations, fixtures, scaffolding, lockfiles

### Dependencies

**Version Selection:** Default to latest LTS. State version + reasoning in plan.md.

**LTS Examples:** Node.js 20/22, Python 3.11/3.12, Java 17/21, .NET 6/8

### File Access

| Allowed | Prohibited |
|---------|------------|
| `src/`, `tests/`, dev configs, build files | `memory/*`, `specs/*.md`, prod configs, `.git` |

---

## Quality & Verification

### Pre-Commit (MUST run)

Formatters → Linters → Type checkers → Build verification

### Testing

- Test each Given-When-Then scenario
- Fix all scenarios before marking complete
- Use mocking for time-dependent tests (NO real sleeps)

### Constitution Gates

Gate fail = BLOCKER. Requires plan.md "Complexity Tracking" justification.

---

## Violation Handling

| Trigger | Response | Recovery |
|---------|----------|----------|
| Spec ambiguous | STOP, CLARIFICATION NEEDED, WAIT | Human updates spec → resume |
| Constitution conflict | STOP, FLAG, WAIT | Human updates spec OR adds justification |
| Test fail (obvious) | Auto-fix max 2× | Fix + retest |
| Test fail (logic) | Mark [F], WAIT | Human diagnosis |
| Missing file | SEARCH similar → CLARIFICATION NEEDED | Human confirms |

---

## Collaboration

### Version Control

- Atomic commits (1 story/scenario)
- Commit after validation passes
- Work on feature branch `[###-feature-name]`
- Merge conflicts: git abort → REPORT → WAIT

### Change Communication

- Update design docs when trade-offs occur
- Document decisions in research.md
- Update spec first if issues found

---

## Ethics & Safety

**MUST NOT:** Commit secrets/keys/tokens, share PII, make undisclosed network calls

**Detection:** Run scanners (git-secrets, truffleHog, gitleaks)

**Licensing:** Prefer permissive (MIT, Apache, BSD). STOP for license conflicts.

---

## Glossary

| Term | Definition |
|------|------------|
| Constitution | Immutable project principles (`memory/constitution.md`) |
| Constitution Gate | Compliance check - failure = blocker |
| Complexity Tracking | plan.md table: Violation, Why Needed, Alternative Rejected |
| Feature Directory | `specs/[###-feature-name]/` |
| Given-When-Then | Scenario: "Given [context] When [action] Then [outcome]" |
| Task States | `[ ]` pending, `[x]` complete, `[F]` failed, `[B]` blocked |

---

*AI agents MUST follow these guidelines for spec-driven development.*
