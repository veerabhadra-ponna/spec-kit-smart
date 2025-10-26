---
description: Run the end-to-end specification workflow (specify → clarify → plan → tasks → analyze) and produce consolidated status.
scripts:
  sh: scripts/bash/orchestrate-feature.sh --json
  ps: scripts/powershell/orchestrate-feature.ps1 -Json
---

## Strict Contract

- **Inputs:**
  - Natural language feature description (`$ARGUMENTS`).
  - JSON from `{SCRIPT}` containing feature paths and status file locations.
  - Templates in `templates/*.md` and existing artifacts for incremental updates.
- **Tools:** Shell commands, file reads, file writes. No network access.
- **Outputs:** Overwrite or create the following files atomically:
  1. `${FEATURE_DIR}/spec.md`
  2. `${FEATURE_DIR}/plan.md`
  3. `${FEATURE_DIR}/research.md`
  4. `${FEATURE_DIR}/data-model.md`
  5. `${FEATURE_DIR}/quickstart.md`
  6. `${FEATURE_DIR}/tasks.md`
  7. `${FEATURE_DIR}/status/specify.md`
  8. `${FEATURE_DIR}/status/plan.md`
  9. `${FEATURE_DIR}/status/tasks.md`
 10. `${FEATURE_DIR}/status/feature.md` (aggregated run report)
- **Schema requirements:**
  - Each Markdown artifact must follow its corresponding template (front matter + sections).
  - Status files must include timestamp, branch, validation tables, and follow the examples in the individual commands.
- **Idempotency:** If no changes are required across all artifacts, make no edits and print `No changes`.
- **Failure handling:**
  - If prerequisites are missing, emit `## Error` with remediation steps and stop.
  - If any constitution gate fails, record the failure in `status/feature.md` and exit non-zero.

## Shell Guidance

- **PowerShell:** Base64-encode multi-line descriptions when invoking `create-new-feature.ps1` via `-EncodedArgs`. Use doubled single quotes for literal apostrophes.
- **Bash:** Use `--encoded "$(printf %s "$text" | base64)`"` for the feature description and prefer double quotes for other arguments.

## Execution Sequence

1. **Bootstrap:**
   - Validate the feature brief is present; if absent, produce `## Error` and stop.
   - Call `scripts/powershell/create-new-feature.ps1`/`scripts/bash/create-new-feature.sh` with JSON mode to set up the feature directory.
   - Parse returned paths and ensure `status/` directory exists (as reported by `{SCRIPT}`).
2. **Specification Phase:**
   - Populate `spec.md` using `templates/spec-template.md`.
   - Limit to ≤3 `[NEEDS CLARIFICATION]` markers.
   - Record decisions and clarifications in `status/specify.md`.
3. **Clarification Phase:**
   - List outstanding questions (≤3) in `status/specify.md` under `Clarification Requests`.
   - Apply any known answers to `spec.md` and update the Clarifications Log.
4. **Planning Phase:**
   - Invoke `scripts/powershell/setup-plan.ps1 -Json` (or bash equivalent) to scaffold `plan.md`.
   - Produce `plan.md`, `research.md`, `data-model.md`, and `quickstart.md` per templates.
   - Evaluate gates G1–G3 and write results to `status/plan.md`.
   - If any gate fails, mark the failure in `status/feature.md` and exit.
5. **Tasking Phase:**
   - Use `scripts/powershell/check-prerequisites.ps1 -Json -IncludeTasks` (or bash) to confirm required docs.
   - Draft `tasks.md` with machine-parseable task lines and a Mermaid dependency graph.
   - Capture validation details in `status/tasks.md` (coverage, dependency cycles, risk mitigation).
6. **Analysis Phase:**
   - Cross-check consistency between spec, plan, and tasks (traceability, risk coverage, story alignment).
   - Record results in `status/feature.md` with sections:
     - Metadata (timestamp, branch, feature title)
     - Gate Summary (spec, plan, tasks)
     - Outstanding Clarifications
     - Action Items before implementation
7. **Agent Context Refresh:**
   - After plan updates, run `scripts/powershell/update-agent-context.ps1 -Json` (or bash) and note updated files in `status/feature.md`.

## Aggregated Status Template (`status/feature.md`)

```markdown
# /speckit.feature – End-to-End Report
- **Timestamp:** 2024-01-01T00:00:00Z
- **Branch:** 000-example-feature

## Phase Summary
| Phase | Status | Notes |
|-------|--------|-------|
| Specification | PASS | Clarification queued for pricing tier rules |
| Planning | PASS | All gates satisfied |
| Tasking | PASS | No dependency cycles |
| Analysis | PASS | Traceability complete |

## Outstanding Clarifications
1. [Section] – question

## Action Items
- Refresh agent context files (completed)
- Schedule stakeholder review of plan.md
```

Produce all artifacts in a single run so a fresh AI session can continue implementation without additional setup.
