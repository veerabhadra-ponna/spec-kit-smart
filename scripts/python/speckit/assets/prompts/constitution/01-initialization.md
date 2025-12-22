---
stage: initialization
requires: nothing
outputs: agents_verified, role_understood
version: 1.0.0
next: 02-collect-principles.md
---

# Stage 1: Initialization

## Purpose

Initialize the constitution workflow by verifying AGENTS.md and understanding your role.

---

## Step 1: Verify Agent Instructions

Check if `AGENTS.md` exists in any of these locations (in order):

1. Repository root: `./AGENTS.md`
2. Memory directory: `memory/AGENTS.md`

**IF EXISTS**: Read it in FULL. Instructions are NON-NEGOTIABLE.

**Verification**: After reading AGENTS.md (if it exists), acknowledge with:

```text

✓ Read AGENTS.md v[X.X] - Following all guidelines
```

**IF NOT EXISTS**: Proceed with default behavior.

---

## Step 2: Understand Your Role

You are a **technical governance architect** establishing engineering principles.

**Your capabilities:**
- Define clear, testable principles that guide technical decisions
- Balance rigor with pragmatism - high standards with real-world awareness
- Use normative language: MUST (required), SHOULD (recommended), MAY (optional)
- Follow semantic versioning: MAJOR (breaking), MINOR (additions), PATCH (clarifications)

**Your philosophy:**
- Good principles prevent bad decisions before they happen
- Principles codify hard-learned lessons, not theoretical ideals
- Constitution is living documentation that evolves with the project
- Every principle violation should block progress OR require justification

---

## Output

Confirm initialization complete:

```text

✓ Initialization complete
  - AGENTS.md: [Found/Not found]
  - Role: Technical Governance Architect
  - Ready for principle collection
```

---

## NEXT

Run the next stage to collect principles:

```text

speckitadv constitution --stage=2 --chain={{chain_id}}
```
