# AI Agent Guidelines

**Version:** 3.5

---

## Critical Rules

| Rule | Description |
|------|-------------|
| **CLI First** | Use `speckitadv` Python CLI for all workflow operations - it embeds prompts/templates |
| **State Auto-Detection** | After stage 2, CLI auto-detects stage and folder from `specs/{feature}/.state/state.json` |
| **File Edit Fallback** | If inline edit fails: recreate with full content, preserve ALL comments, make ONLY required changes |
| **Chain mkdir** | Use semicolon: `mkdir folderA; mkdir folderB` |
| **Doc Updates** | Increment version, add CHANGELOG entry if `__init__.py` or `pyproject.toml` changed |
| **Large Files** | >1500 lines -> chunked generation (300-800 lines/chunk) |
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
| Run formatters -> linters -> tests before commit | Add requirements not in specs |
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

### Rerunning Specific Stages (analyze-project)

To rerun a specific stage (e.g., after fixing issues or with updated code):

```bash
# Force a specific stage number
speckitadv analyze-project --stage=<number> --analysis-dir=<path>
```

**Stage Reference:**

| Stage | ID | Description | Rerun Command |
|-------|-----|-------------|---------------|
| 1 | 01a-initialization | Setup | `--stage=1` |
| 2 | 01b-input-collection | Input collection | `--stage=2` |
| 3 | 01c-script-execution | Script execution | `--stage=3` |
| 4 | 02a-category-scan | Category scan | `--stage=4` |
| 5 | 02b-deep-dive | Deep dive analysis | `--stage=5` |
| 6 | 02c-config-analysis | Config analysis | `--stage=6` |
| 7 | 02d-test-audit | Test audit | `--stage=7` |
| 8 | 02e-quality-gates | Quality gates | `--stage=8` |
| 9 | 03a-full-app | Full app analysis (Scope A) | `--stage=9 --chunk=1..4` |
| 10 | 03b-cross-cutting | Cross-cutting (Scope B) | `--stage=10 --chunk=1..3` |
| 11 | 04a-report-chunks-1-3 | Report chunks 1-3 | `--stage=11` |
| 12 | 04b-report-chunks-4-6 | Report chunks 4-6 | `--stage=12` |
| 13 | 04c-report-chunks-7-9 | Report chunks 7-9 | `--stage=13` |
| 14 | 04d-report-verification | Report verification | `--stage=14` |
| 15 | 05a-executive-summary | Scoped artifacts | `--stage=15` |
| 16 | 06a-06e | Specs generation | `--stage=16 --chunk=1..5` |

**Chunked Stages (Stage 16 - Scope A):**

```bash
# Functional Spec - Legacy
speckitadv analyze-project --stage=16 --chunk=1

# Functional Spec - Target
speckitadv analyze-project --stage=16 --chunk=2

# Technical Spec - Legacy
speckitadv analyze-project --stage=16 --chunk=3

# Technical Spec - Target
speckitadv analyze-project --stage=16 --chunk=4

# Stage Prompts
speckitadv analyze-project --stage=16 --chunk=5
```

**Chunked Stages (Stage 16 - Scope B):**

```bash
# Cross-cutting Artifacts
speckitadv analyze-project --stage=16 --chunk=1
```

**Example - Rerun Scoped Artifacts Stage:**

```bash
speckitadv analyze-project --stage=15 --analysis-dir=.analysis/myproject-20251226-123456
```

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
| `list-files` | Find files by pattern or category | `speckitadv list-files --pattern "**/*.cs" --limit 50` |

**Note:** `list-files` also accepts shell-expanded paths as positional arguments when the shell
pre-expands glob patterns (e.g., PowerShell may expand `*.cs` before passing to CLI).

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

### CRITICAL: File Write Policy

**ALWAYS use CLI commands for file writes. NEVER use:**

- Shell/PowerShell commands (`Out-File`, `Add-Content`, `echo >`, `cat <<`)
- AI Write tools directly to the analysis folder
- Any method that bypasses the CLI artifact tracking

**Why:** CLI commands track artifacts in state.json for workflow continuity.

### CLI Command Best Practices

**Note:** OS command line length limits apply (~8000 chars on Windows). Break large content into smaller chunks.

```bash
# Write report (put --append EARLY before --content)
speckitadv write-report <filename> --stage=<stage-id> --content '<small-md>'
speckitadv write-report <filename> --stage=<stage-id> --append --content '<small-md>'

# Write JSON data
speckitadv write-data <filename> --stage=<stage-id> --content '<small-json>'
```

**For content > 2000 chars, use stdin mode:**

```powershell
# For reports
@"
<markdown content here>
"@ | speckitadv write-report <filename> --stage=<stage-id> --append --stdin

# For JSON data
@"
<json content here>
"@ | speckitadv write-data <filename> --stage=<stage-id> --stdin
```

**Key Rules:**

1. Place `--append` EARLY in the command (before `--content`) to prevent truncation
2. Keep `--content` value under 2000 characters
3. Use stdin mode for large content blocks (JSON or markdown)
4. Never use shell file write commands for analysis artifacts

### Shell Quote Escaping

**CRITICAL:** JSON content with quotes causes shell parsing errors like `unexpected EOF while looking for matching '"'`.

#### JSON in write-data Commands

**WRONG - causes shell quote errors:**

```bash
# Single quotes around JSON with internal quotes breaks bash
speckitadv write-data file.json --content '{"key": "value"}'
# Error: unexpected EOF while looking for matching `"'
```

**CORRECT - use stdin mode for JSON (recommended):**

```bash
# Bash - heredoc with stdin
cat << 'EOF' | speckitadv write-data file.json --stage=02e --stdin
{"quality_gates": {"file_coverage": true, "execution": "complete"}}
EOF

# PowerShell - here-string with stdin
@"
{"quality_gates": {"file_coverage": true, "execution": "complete"}}
"@ | speckitadv write-data file.json --stage=02e --stdin
```

**CORRECT - escape quotes for simple JSON:**

```bash
# Use backslash escapes for short, simple JSON
speckitadv write-data file.json --stage=02e --content "{\"key\": \"value\"}"
```

#### General Quote Rules

| Problem | Solution |
|---------|----------|
| JSON with quotes | Use stdin mode (heredoc/here-string) |
| Python: `open('file.json')` | Use double quotes: `open("file.json")` |
| Complex nested quotes | Always use stdin mode |
| Content > 2000 chars | Always use stdin mode |

**Example Python heredoc error:**

```bash
# WRONG - single quotes in Python break bash
python3 << 'PYEOF'
with open('file.json', 'w') as f:  # <-- These quotes break bash
PYEOF
```

**Fix:**

```bash
# CORRECT - use double quotes in Python
python3 << 'PYEOF'
with open("file.json", "w") as f:  # <-- Works
PYEOF
```

### Temporary File Fallback

If stdin mode fails due to parsing issues (special characters, encoding, etc.) and you **absolutely must** create a temp file:

```powershell
# Windows - use system temp folder
$tempFile = "$env:TEMP\speckit-chunk-$(Get-Random).md"
@"
<content>
"@ | Out-File -FilePath $tempFile -Encoding utf8
Get-Content $tempFile | speckitadv write-report analysis-report.md --stage=X --append --stdin
# No cleanup needed - OS handles temp folder

# Linux/Mac
tempFile="/tmp/speckit-chunk-$RANDOM.md"
cat > "$tempFile" << 'EOF'
<content>
EOF
cat "$tempFile" | speckitadv write-report analysis-report.md --stage=X --append --stdin
```

**Rules:**

- NEVER create temp files in the analysis directory
- ALWAYS use system temp folder (`$env:TEMP` or `/tmp`)
- Use unique random names to avoid conflicts
- No explicit cleanup needed - OS handles it

---

## File Write Best Practices (All Workflows)

### CRITICAL: Never Reduce Content Quality

**Chunking means MULTIPLE WRITE OPERATIONS, NOT reduced output.**

- WRONG: "I'll generate a smaller JSON to fit the limit"
- WRONG: "Given the limit, I'll create a reduced version"
- CORRECT: "I'll write the full content using multiple --append operations"
- CORRECT: "I'll use stdin mode for this large content block"

**The content quality and completeness must be IDENTICAL** regardless of how it's written.

### For CLI Commands (analyze-project workflow)

See "CLI Command Best Practices" above for `write-report` and `write-data` commands.

**How to chunk large content - ALWAYS use --append:**

```bash
# --append works for ALL chunks (creates file if not exists, appends if exists)
speckitadv write-report file.md --stage=X --append --content '<section 1>'
speckitadv write-report file.md --stage=X --append --content '<section 2>'
speckitadv write-report file.md --stage=X --append --content '<section 3>'
```

**OR use stdin for single large block:**

```powershell
@"
<full content here - no size limit via stdin>
"@ | speckitadv write-report file.md --stage=X --append --stdin
```

### For AI Write/Edit Tools (feature-scoped workflows)

Feature-scoped workflows (specify, plan, tasks, implement, checklist) use AI Write/Edit tools for files in `specs/{feature}/`.

**Chunking Rules:**

| Content Size | Approach |
|-------------|----------|
| < 2000 chars | Single write operation |
| 2000-5000 chars | Write in 2-3 chunks by section |
| > 5000 chars | Write skeleton first, then fill sections incrementally |

**Best Practices:**

1. **Write skeleton first**: Create file structure with headers, then fill content
2. **Section-by-section**: Complete one section before moving to next
3. **Verify after each chunk**: Read file to confirm content was written correctly
4. **Group logically**: Write related content together (e.g., all user stories, then all requirements)

**Examples by Workflow:**

| Workflow | Chunking Strategy |
|----------|-------------------|
| `specify` | Steps 3-6 are pre-chunked (Overview -> Stories -> Requirements -> Technical) |
| `plan` | Chunks 1-3 (Summary -> Architecture -> Data) |
| `tasks` | By phase (Setup -> Foundational -> User Stories -> Polish) |
| `checklist` | By quality dimension (Completeness -> Clarity -> Coverage) |
| `implement` | Write file skeleton, then fill methods incrementally |

**Shell Command Warning:**

**Note:** If using shell commands with content arguments, OS limits apply (~8000 chars on Windows). Prefer AI tools or stdin piping for large content.

---

## Agentic Workflow (Auto-Continue)

The analyze-project workflow supports fully agentic execution through continuation markers.

### Continuation Markers

| Marker | Meaning | AI Action |
|--------|---------|-----------|
| `[AUTO-CONTINUE]` | No user input needed | Immediately proceed to next stage |
| `[WAIT-FOR-INPUT]` | User response required | Stop and wait for user |
| `[GATE-CHECK]` | Verification gate | If pass: continue. If fail: wait |

### How It Works

1. **Within stages**: `[STOP: USER_INPUT_REQUIRED]` markers pause for user input
2. **At stage end**: The continuation marker determines what happens next
3. **Default**: If no marker, treat as `[AUTO-CONTINUE]`

### Stage Types

| Stage Type | End Behavior | Examples |
|------------|--------------|----------|
| Analysis/Generation | AUTO-CONTINUE | 02a-02d, 04a-04c, 05a |
| Q&A (multi-question) | AUTO-CONTINUE after all answered | 03a1, 03a2 |
| Verification gates | GATE-CHECK (pass/fail) | 02e, 04d, 06a-06c2 |
| User decisions | Wait for explicit input | 01b (if interactive) |

### Best Practice

Do NOT stop and ask "should I continue?" between stages. Follow the continuation markers and proceed automatically unless:
- A `[GATE-CHECK]` fails
- A `[STOP: USER_INPUT_REQUIRED]` marker is encountered

---

## Document Structure

**Priority (Highest->Lowest):**
1. Constitution - Immutable project principles
2. Spec - Requirements (WHAT/WHY)
3. Plan - Architecture (HOW)
4. Supporting Docs - data-model > contracts > research > quickstart > tasks

**Conflict:** STOP -> `CLARIFICATION NEEDED` (cite sections) -> WAIT

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

Formatters -> Linters -> Type checkers -> Build verification

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
| Spec ambiguous | STOP, CLARIFICATION NEEDED, WAIT | Human updates spec -> resume |
| Constitution conflict | STOP, FLAG, WAIT | Human updates spec OR adds justification |
| Test fail (obvious) | Auto-fix max 2× | Fix + retest |
| Test fail (logic) | Mark [F], WAIT | Human diagnosis |
| Missing file | SEARCH similar -> CLARIFICATION NEEDED | Human confirms |

---

## Collaboration

### Version Control

- Atomic commits (1 story/scenario)
- Commit after validation passes
- Work on feature branch `[###-feature-name]`
- Merge conflicts: git abort -> REPORT -> WAIT

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
