---
stage: initialization
requires: nothing
outputs: agents_verified
version: 3.1.0
next: 01b-input-collection.md
---

# Stage 1A: Initialization

## Purpose

Initialize the analysis chain by verifying AGENTS.md guidelines and preparing the workspace.

---

## Step 1: Verify Agent Instructions

Check if `AGENTS.md` exists in any of these locations (in order):

1. Repository root: `./AGENTS.md`
2. Memory directory: `memory/AGENTS.md`

---
⏸️ **[STOP: AGENTS_CHECK]**

Search for AGENTS.md in the locations listed above.

**IF AGENTS.md EXISTS:**
1. Read the ENTIRE file
2. Note the version number (line 3-4)
3. Internalize all guidelines
4. Output confirmation:

   ```text
   ✓ Read AGENTS.md v[X.X] - Following all guidelines

   ```

**IF AGENTS.md DOES NOT EXIST:**
1. Output: `✓ No AGENTS.md found - Proceeding with default behavior`

**Capture result in:** `$AGENTS_STATUS`

---

## Step 2: Verify Toolkit Availability

Check that the speckitadv CLI is available:

```bash
speckitadv --version
```

This provides the cross-platform commands for project analysis and enumeration.

---
⏸️ **[STOP: TOOLKIT_CHECK]**

Execute the appropriate check for the detected OS.

**IF scripts exist:** Output: `✓ Toolkit scripts verified`
**IF scripts missing:** Output: `❌ Error: Required scripts not found` → STOP workflow

**Capture result in:** `$TOOLKIT_STATUS`

---

## Step 3: Prepare Analysis Directory

Verify or create the analysis directory structure:

```bash
mkdir -p .analysis/.state
mkdir -p .analysis/.checkpoints

```

---

## Checkpoint: Initialization Complete

### Create Checkpoint

Write checkpoint file: `.analysis/.checkpoints/01a-init-complete.json`

```json
{
  "substage": "01a-initialization",
  "timestamp": "{ISO-8601}",
  "agents_verified": true,
  "agents_version": "{version or null}",
  "toolkit_verified": true,
  "status": "complete"
}

```

### Verify Checkpoint

1. Read `.analysis/.checkpoints/01a-init-complete.json`
2. Validate JSON is parseable
3. Confirm `status` = "complete"

---
⏸️ **[STOP: CHECKPOINT_VERIFY]**

**IF checkpoint verified:** Output: `✓ Checkpoint verified: 01a-initialization`
**IF checkpoint failed:** Retry checkpoint creation once, then STOP if still failing

---

## Output

```text
═══════════════════════════════════════════════════════════
  SUBSTAGE COMPLETE: 01a-initialization
  AGENTS.md: {verified v[X.X] | not found}
  Toolkit: verified
  Next: 01b-input-collection.md
═══════════════════════════════════════════════════════════

```

## Next Substage

Proceed immediately to: **01b-input-collection.md**
