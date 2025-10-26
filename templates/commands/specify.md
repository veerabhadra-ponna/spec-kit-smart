---
description: Create or update the feature specification from a natural language brief.
scripts:
  sh: scripts/bash/create-new-feature.sh --json --encoded "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 -Json -EncodedArgs "{ARGS}"
---

## Strict Contract

- **Inputs:**
  - Raw feature description supplied after `/speckit.specify`.
  - JSON emitted by `{SCRIPT}` containing `ok`, `paths.feature_dir`, and `paths.spec`.
  - Existing `spec.md` (if present) to preserve stable IDs.
- **Tools:** Shell commands, file reads, and writes only. No network access.
- **Outputs:** Write _exactly_ these files, overwriting atomically:
  1. `${FEATURE_DIR}/spec.md` — Markdown matching `templates/spec-template.md` (all sections required).
  2. `${FEATURE_DIR}/status/specify.md` — Markdown summary with run metadata and queued clarification questions.
- **Schema expectations:**
  - `spec.md` must include YAML front matter with `feature_id`, `title`, `status`, `branch`, `created_at`, `source_commit`, `generator`, `constitution_version`.
  - `status/specify.md` must contain: heading, timestamp, `Decisions` list (≤5 bullets), `Clarification Requests` (≤3 items), and `Validation` table covering completeness checks.
- **Idempotency:** If `spec.md` already satisfies the desired content and no new clarifications arise, leave both files unchanged and print `No changes` to STDOUT.
- **Failure handling:**
  - If the feature description is empty, emit `## Error\nMissing feature description.` and stop.
  - If `{SCRIPT}` returns `ok=false`, surface the `error` message in the status file and halt without modifying `spec.md`.

## Shell Guidance

- **PowerShell:** `-EncodedArgs ([Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($text)))` and quote arguments as `'I''m Groot'` when needed.
- **Bash:** `--encoded "$(printf %s "$text" | base64)`"` or wrap plain text with double quotes (`"I'm Groot"`).

## Execution Flow

1. **Validate Input:** Ensure the feature brief is non-empty; trim whitespace.
2. **Bootstrap Feature Structure:**
   - Base64-encode the raw brief and invoke `{SCRIPT}` with `--json`/`-Json` to initialize `specs/<feature>`.
   - Parse the JSON payload and capture `feature_dir`, `spec`, `branch`, and `feature_id`.
3. **Analyse the Brief:** Identify personas, core value, constraints, and success signals. Note up to three high-impact uncertainties as `[NEEDS CLARIFICATION: …]` items.
4. **Draft `spec.md`:**
   - Start from `templates/spec-template.md`.
   - Populate all sections with precise, testable language.
   - Generate prioritized user journeys (`US-01…`) with measurable acceptance criteria.
   - Define functional and non-functional requirements with fit criteria.
   - Maintain or create consistent requirement IDs (e.g., FR-001).
   - Limit `[NEEDS CLARIFICATION]` markers to the top three unresolved issues.
5. **Internal Validation:**
   - Confirm every user journey maps to ≥1 functional requirement and success metric.
   - Ensure NFRs contain measurable thresholds.
   - Verify risks include owners and mitigation direction.
   - Record results in the `Validation` table inside the status file.
6. **Surface Clarifications:** List ≤3 questions in the status file’s `Clarification Requests` section, referencing the impacted spec sections.
7. **Write Outputs:** Update `spec.md` and `status/specify.md`. Use atomic writes and preserve newline at EOF.

## Reporting Format (`status/specify.md`)

```markdown
# /speckit.specify – Run Summary
- **Timestamp:** 2024-01-01T00:00:00Z
- **Branch:** 000-example-feature

## Decisions
- Captured key conclusions (≤5 bullets)

## Clarification Requests
1. `[Section]` – question

## Validation
| Check | Status | Notes |
|-------|--------|-------|
| All mandatory sections present | Pass | |
| Requirements testable | Pass | |
| Risks owned | Needs Review | Owner TBD |
```

Keep the command focused: produce the specification and summarise follow-up work; defer user interaction to `/speckit.clarify`.
