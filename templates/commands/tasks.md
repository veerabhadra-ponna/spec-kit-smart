---
description: Generate an implementation task list aligned with the plan and specification.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -IncludeTasks
---

## Strict Contract

- **Inputs:**
  - JSON from `{SCRIPT}` containing feature paths and available documents.
  - `plan.md`, `spec.md`, and supporting artifacts produced by `/speckit.plan`.
- **Tools:** Shell and filesystem access only. No network calls.
- **Outputs:**
  1. `${FEATURE_DIR}/tasks.md` — Markdown conforming to `templates/tasks-template.md`.
  2. `${FEATURE_DIR}/status/tasks.md` — Markdown summary with dependency health, blockers, and completion checklist.
- **Schema expectations:**
  - Every task line must follow `[T-###] [P#] [US-##|Cross] [label1,label2] [DependsOn: …] Description (Definition of Done)`.
  - `tasks.md` must include a `Dependency Graph` Mermaid diagram referencing each task ID exactly once.
  - `status/tasks.md` must document validation results (orphan checks, cycle detection, coverage of user journeys).
- **Idempotency:** If no substantive changes are required, leave both files untouched and print `No changes`.
- **Failure handling:**
  - If prerequisites are missing, emit `## Error\nMissing planning artifacts – run /speckit.plan.` and stop.
  - If dependency cycles are detected, record them in `status/tasks.md` and flag the run as needing manual intervention.

## Shell Guidance

- **PowerShell:** Always include `-Json` to avoid extraneous output; use doubled single quotes when quoting manually.
- **Bash:** Prefer double quotes (`"value"`); base64 encoding is not required for this command.

## Execution Flow

1. **Validate prerequisites:** Confirm `plan.md` passes gates and that all required artifacts are present.
2. **Extract Inputs:** Map user journeys, functional requirements, risks, and non-functional requirements to task categories.
3. **Author Tasks:**
   - Create foundational tasks (`CORE` label) covering shared infrastructure.
  - For each user journey, generate a Definition of Done and the minimal set of tasks to reach it.
   - Attach labels (`api`, `frontend`, `data`, etc.) and `DependsOn` metadata.
   - Ensure every High risk from the plan has at least one mitigation task.
4. **Validate Graph:** Build a dependency graph and check for missing nodes or cycles.
5. **Update Outputs:**
   - Write the curated tasks to `tasks.md` respecting format and ordering (foundation → journeys → cross-cutting).
   - Produce `status/tasks.md` summarising coverage, dependency analysis, and outstanding risks before implementation.

## Status Template (`status/tasks.md`)

```markdown
# /speckit.tasks – Validation Report
- **Timestamp:** 2024-01-01T00:00:00Z
- **Branch:** 000-example-feature

## Coverage
| Item | Status | Notes |
|------|--------|-------|
| Every user journey mapped to tasks | PASS | |
| High risks mitigated | PASS | |
| Dependency cycles detected | FAIL | T-010 ↔ T-020

## Follow-ups
- Investigate cycle between T-010 and T-020 before implementation.
```

