---
stage: setup
requires: initialization
outputs: feature_dir, design_docs
version: 1.0.0
next: 03-generate.md
---

# Stage 2: Setup

## Purpose

Run setup scripts and load design documents.

---

## Step 1: Collect Preferences (if interactive)

**IF no arguments**, prompt user:

```text
Provide task generation preferences:

PREFERENCES:
- Break into smaller tasks (< 2 hours each)
- Prioritize backend before frontend

Format: Each preference on its own line with dash.
Type "none" for standard breakdown.

Examples:
- Task size: "< 2 hours", "half-day chunks"
- Grouping: "by feature area", "by user story"
- Priority: "backend first", "P1 and P2 only"
- Detail: "include sub-tasks", "high-level only"
```

**WAIT FOR USER RESPONSE.**

---

## Step 2: Run Setup Script

Execute from repo root:

**Unix:**
```bash
scripts/bash/check-prerequisites.sh --json
```

**Windows:**
```powershell
scripts/powershell/check-prerequisites.ps1 -Json
```

Parse: `FEATURE_DIR`, `AVAILABLE_DOCS`

---

## Step 3: Load Design Documents

From FEATURE_DIR:
- **Required**: `plan.md` (tech stack, libraries), `spec.md` (user stories)
- **Optional**: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`

Note: Not all projects have all documents. Generate tasks from available docs.

---

## Output

```
✓ Setup complete
  - Feature dir: {{feature_dir}}
  - Docs available: [list]
  - Preferences: [N] loaded
```

---

## NEXT

```
speckit tasks --stage=3 --chain={{chain_id}}
```
