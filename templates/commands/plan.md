---
description: Produce the implementation plan, supporting research, and gate report for the active feature.
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
---

## Strict Contract

- **Inputs:**
  - JSON from `{SCRIPT}` with resolved paths.
  - Latest `spec.md` (including clarifications).
  - Existing plan artifacts (`plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`) when present.
- **Tools:** Shell, file I/O, and local parsing only. Do not access external networks.
- **Outputs:** Write _exactly_ these files:
  1. `${FEATURE_DIR}/plan.md` — Markdown matching `templates/plan-template.md`.
  2. `${FEATURE_DIR}/research.md` — Markdown capturing outstanding investigations.
  3. `${FEATURE_DIR}/data-model.md` — Markdown (can be stubbed when not applicable).
  4. `${FEATURE_DIR}/quickstart.md` — Markdown quickstart for developers.
  5. `${FEATURE_DIR}/status/plan.md` — Summary of gate results and next actions.
- **Schema expectations:**
  - `plan.md` must keep YAML front matter and fill every section in the template.
  - `status/plan.md` must include: timestamp, gate table (G1–G3) with PASS/FAIL, unresolved issues, and reminders to run `update-agent-context`.
- **Idempotency:** If the plan and supporting docs already reflect the specification with no changes, leave files untouched and print `No changes`.
- **Failure handling:**
  - If `spec.md` is missing, emit `## Error\nMissing spec.md – run /speckit.specify.` and stop.
  - If any gate fails, record failure reasons in `status/plan.md` and highlight blockers for `/speckit.tasks`.

## Shell Guidance

- **PowerShell:** `-Json` returns compressed JSON only; use doubled single quotes in manual arguments.
- **Bash:** Use double quotes for arguments (`"value"`) and prefer the `--json` flag to suppress human-readable noise.

## Execution Flow

1. **Setup:** Invoke `{SCRIPT}` to ensure `plan.md` exists and capture feature paths.
2. **Load Specification:** Read `spec.md`, extract user journeys, requirements, risks, and open questions.
3. **Assess Clarifications:** If `[NEEDS CLARIFICATION]` markers remain, flag Gate G2 as `FAIL` and summarise the blockers in `status/plan.md`.
4. **Draft Plan:**
   - Populate the Technical Context table with explicit decisions or `NEEDS CLARIFICATION` markers.
   - Outline phases with exit criteria tied to deliverables.
   - Record architecture decisions and ADR placeholders.
   - Update the risk register with owners and due dates.
5. **Supporting Artifacts:**
   - `research.md`: Document assumptions needing validation and assign owners.
   - `data-model.md`: Provide entity definitions, relationships, or note if not required.
   - `quickstart.md`: Summarize setup steps, build/test commands, and environment variables.
6. **Gate Evaluation:**
   - G1 Constitution: confirm rules in `constitution.md` remain satisfied (cite rule IDs).
   - G2 Clarifications: verify zero unresolved `[NEEDS CLARIFICATION]` markers.
   - G3 Risks: ensure each High risk has an owner and mitigation plan.
7. **Status Report:**
   - Write `status/plan.md` with gate results, next actions (including rerunning `scripts/powershell/update-agent-context.ps1`), and references to updated files.

## Status Template (`status/plan.md`)

```markdown
# /speckit.plan – Gate Report
- **Timestamp:** 2024-01-01T00:00:00Z
- **Branch:** 000-example-feature

## Gate Results
| Gate | Status | Notes |
|------|--------|-------|
| G1 – Constitution | PASS | Rule C-SEC-001 satisfied |
| G2 – Clarifications | FAIL | Spec still contains [NEEDS CLARIFICATION: auth provider] |
| G3 – Risk Mitigation | PASS | Owners assigned |

## Next Actions
- Run `scripts/powershell/update-agent-context.ps1 -Json` to refresh agent instructions.
- Prepare `/speckit.tasks` once gates are PASS.
```
