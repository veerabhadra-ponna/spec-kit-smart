# AI Agent Guidelines

**Version:** 3.6

---

## Critical Rules

| Rule | Description |
|------|-------------|
| **CLI First** | Use `speckitadv` CLI for all workflow operations |
| **ASCII-Only** | No Unicode (arrows, checkmarks). Use `->`, `[ok]`, `[x]`, `[!]` |
| **Mermaid Diagrams** | Use Mermaid syntax for all diagrams. No text-based ASCII art |
| **State Auto-Detection** | After stage 2, CLI auto-detects stage from state.json |
| **File Write via CLI** | Use `write-report`/`write-data` commands. Never use shell file writes |
| **Large Content** | >2000 chars: use stdin mode. >1500 lines: chunked generation |
| **No Backward Compat** | Pre-release system. Breaking changes allowed |

---

## Quick Reference

**Priority:** Constitution > Spec > Plan > Supporting Docs

**Task States:** `[ ]` pending, `[x]` complete, `[F]` failed, `[B]` blocked

| DO | DON'T |
|----|-------|
| STOP + `CLARIFICATION NEEDED` when unclear | Commit secrets/credentials |
| Follow Constitution at all times | Modify `memory/` during implementation |
| Run formatters -> linters -> tests before commit | Add requirements not in specs |

**Decision Tree:**

| Problem | Action |
|---------|--------|
| Spec unclear? | STOP, mark [B], WAIT |
| Test failed (syntax)? | Auto-fix max 2x |
| Test failed (logic)? | Mark [F], WAIT |
| Constitution conflict? | STOP, FLAG, WAIT |

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `analyze-project` | Analyze existing project for modernization |
| `constitution` | Create project constitution |
| `specify` | Create baseline specification |
| `plan` | Create implementation plan |
| `tasks` | Generate actionable tasks |
| `implement` | Execute implementation |

**State Locations:**

| Command | State Location |
|---------|----------------|
| `analyze-project` | `.analysis/{project}-{timestamp}/state.json` |
| `constitution` | `memory/constitution.md` |
| Others | `specs/{feature}/.state/state.json` |

---

## Stage Reference (analyze-project)

| Stage | ID | Description | Rerun Command |
|-------|-----|-------------|---------------|
| 1-3 | 01a-01c | Setup, input, scripts | `--stage=1` to `--stage=3` |
| 4-8 | 02a-02e | Analysis phases | `--stage=4` to `--stage=8` |
| 9 | 03a-full-app | Full app (Scope A) | `--stage=9 --chunk=1` (1-4) |
| 10 | 03b-cross-cutting | Cross-cutting (Scope B) | `--stage=10 --chunk=1` (1-3) |
| 11-14 | 04a-04d | Report generation | `--stage=11` to `--stage=14` |
| 15 | 05a-executive-summary | Scoped artifacts | `--stage=15` |
| 16 | 06a-06e | Specs generation | `--stage=16 --chunk=1` (1-5) |

**Stage 16 Chunks (Scope A):** 1=func-legacy, 2=func-target, 3=tech-legacy, 4=tech-target, 5=stage-prompts

**Stage 16 Chunks (Scope B):** 1=cross-cutting-artifacts

---

## CLI Utility Commands

### Writing Artifacts

```bash
# Reports (markdown)
speckitadv write-report <file.md> --stage=<id> --append --content '<content>'

# Data (JSON)
speckitadv write-data <file.json> --stage=<id> --content '<json>'
```

**For content >2000 chars, use stdin:**

```powershell
@"
<content>
"@ | speckitadv write-report <file.md> --stage=<id> --append --stdin
```

### Context Queries

| Command | Purpose |
|---------|---------|
| `get-context --field scope` | Get render context |
| `file-stats <file> --pattern "^##"` | File info and pattern counts |
| `list-files --pattern "**/*.cs"` | Find files by pattern |

### Valid Preference Keys

`q1_language`, `q2_database`, `q3_message_bus`, `q4_package_manager`, `q5_deployment`, `q6_iac`, `q7_containerization`, `q8_observability`, `q9_security`, `q10_testing`

---

## File Write Rules

| Rule | Requirement |
|------|-------------|
| **CLI Only** | Always use `write-report`/`write-data`. Never `Out-File`, `echo >`, `cat <<` |
| **--append First** | Place `--append` before `--content` to prevent truncation |
| **Stdin for Large** | Content >2000 chars must use `--stdin` mode |
| **Full Quality** | Chunking = multiple writes, NOT reduced content |
| **Track Artifacts** | CLI tracks in state.json for workflow continuity |

### Shell Quote Escaping

| Problem | Solution |
|---------|----------|
| JSON with quotes | Use stdin mode (heredoc) |
| Content >2000 chars | Use stdin mode |
| Python in heredoc | Use double quotes: `open("file")` not `open('file')` |

**Stdin example (JSON):**

```bash
cat << 'EOF' | speckitadv write-data file.json --stage=02e --stdin
{"key": "value"}
EOF
```

### Temp File Fallback

If stdin fails, use system temp folder (`$env:TEMP` or `/tmp`) with random names. Never create temp files in analysis directory.

---

## Agentic Workflow

| Marker | Meaning | Action |
|--------|---------|--------|
| `[AUTO-CONTINUE]` | No user input needed | Proceed immediately |
| `[WAIT-FOR-INPUT]` | User response required | Stop and wait |
| `[GATE-CHECK]` | Verification gate | Pass: continue. Fail: wait |

**Default:** If no marker, treat as `[AUTO-CONTINUE]`. Do NOT ask "should I continue?" between stages.

---

## Document Structure

**Priority (Highest to Lowest):**

1. Constitution - Immutable principles
2. Spec - Requirements (WHAT/WHY)
3. Plan - Architecture (HOW)
4. Supporting Docs

**Conflict:** STOP -> cite sections -> WAIT for human resolution

---

## Code Generation

**Requirements:**

- Functionally deterministic and idempotent
- Production-ready (compiles, passes tests)
- Traceable (links to spec via comments)
- Search existing methods before creating new

**Documentation:** Document classes and business logic. Skip trivial getters/DTOs.

**Commits:** Small (1 scenario, 1-5 files, <300 lines). Exceptions: generated code, migrations.

**Dependencies:** Default to latest LTS. State version + reasoning in plan.md.

---

## Quality & Verification

**Pre-Commit:** Formatters -> Linters -> Type checkers -> Build

**Testing:** Test each Given-When-Then scenario. Fix all before marking complete.

**Constitution Gates:** Gate fail = BLOCKER. Requires justification in plan.md.

---

## Violation Handling

| Trigger | Response |
|---------|----------|
| Spec ambiguous | STOP, CLARIFICATION NEEDED, WAIT |
| Constitution conflict | STOP, FLAG, WAIT |
| Test fail (obvious) | Auto-fix max 2x |
| Test fail (logic) | Mark [F], WAIT |
| Missing file | SEARCH -> CLARIFICATION NEEDED |

---

## Collaboration

- Atomic commits (1 story/scenario)
- Feature branch `[###-feature-name]`
- Merge conflicts: git abort -> REPORT -> WAIT
- Update design docs for trade-offs

---

## Ethics & Safety

**MUST NOT:** Commit secrets/keys, share PII, make undisclosed network calls

**Licensing:** Prefer permissive (MIT, Apache, BSD). STOP for license conflicts.

---

## Glossary

| Term | Definition |
|------|------------|
| Constitution | Immutable project principles (`memory/constitution.md`) |
| Constitution Gate | Compliance check - failure = blocker |
| Feature Directory | `specs/[###-feature-name]/` |
| Given-When-Then | Scenario format |
| Task States | `[ ]` pending, `[x]` complete, `[F]` failed, `[B]` blocked |

---

*AI agents MUST follow these guidelines for spec-driven development.*
