---
stage: initialization
requires: nothing
outputs: agents_verified
version: 3.2.0
next: 01b-input-collection.md
---

# Stage 1A: Initialization

## Purpose

Initialize the analysis chain by verifying AGENTS.md guidelines and toolkit availability.

Note: The CLI has already created the analysis folder at `{analysis_dir}` with state.json.

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

---

## Step 2: Verify Toolkit Availability

Check that the speckitadv CLI is available:

```bash
speckitadv --version
```

---

⏸️ **[STOP: TOOLKIT_CHECK]**

**IF CLI works:** Output: `✓ Toolkit verified (vX.X.X)`
**IF CLI missing:** Output: `❌ Error: speckitadv CLI not found` → STOP workflow

---

## Output

```text
═══════════════════════════════════════════════════════════
  SUBSTAGE COMPLETE: 01a-initialization
  AGENTS.md: {verified v[X.X] | not found}
  Toolkit: verified
  Analysis folder: {analysis_dir}
  Next: Run speckitadv analyze-project
═══════════════════════════════════════════════════════════
```

## Next Substage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
