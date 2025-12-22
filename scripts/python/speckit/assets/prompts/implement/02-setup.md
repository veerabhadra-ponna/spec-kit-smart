---
stage: setup
requires: initialization
outputs: feature_dir, checklist_status
version: 1.0.0
next: 03-load-context.md
---

# Stage 2: Setup

## Purpose

Run setup scripts and check checklist status.

---

## Step 1: Collect Notes (if interactive)

**IF no arguments**, prompt user:

```text
Provide implementation notes:

NOTES:
- Start with database migration first
- Focus on P1 user stories only

Format: Each note on its own line with dash.
Type "none" for standard implementation.

Examples:
- Execution: "database first", "backend before frontend"
- Scope: "P1 only", "skip optional features"
- Testing: "write tests first", "skip tests (spike)"
```

**WAIT FOR RESPONSE.**

---

## Step 2: Run Setup Script

Execute (cross-platform):

```bash
speckitadv check --json --require-tasks --include-tasks
```

Parse: `FEATURE_DIR`, `AVAILABLE_DOCS`

---

## Step 3: Check Checklists

Scan `{{feature_dir}}/checklists/`:

```text

| Checklist | Total | Complete | Incomplete | Status |
|-----------|-------|----------|------------|--------|
| ux.md     | 12    | 12       | 0          | ✓ PASS |
| test.md   | 8     | 5        | 3          | ✗ FAIL |
```

**If any incomplete:**
- Display table
- **STOP** and ask: "Some checklists incomplete. Proceed anyway? (yes/no)"
- Wait for response

**If all complete:**
- Display table
- Proceed automatically

---

## Output

```text

✓ Setup complete
  - Feature: {{feature_dir}}
  - Checklists: [PASS / user approved]
```

---

## NEXT

```text

speckitadv implement --stage=3 --chain={{chain_id}}
```
