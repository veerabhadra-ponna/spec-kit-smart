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

## NEXT: Collect Principles

Before running Stage 2, determine which principles to use:

### Check: Did User Provide Principles?

**IF user provided principles in their initial request** (e.g., `/speckitadv.constitution "No Tests, focus on simplicity"`):

Skip to running Stage 2 with those principles:

```bash
speckitadv constitution --stage=2 --principles="<user's principles>"
```

### ELSE: Ask User About Principles

---
⏸️ **[STOP: USER_INPUT_REQUIRED - PRINCIPLES_CHOICE]**

Present this prompt to user EXACTLY:

```text
════════════════════════════════════════════════════════════
CONSTITUTION PRINCIPLES

Do you want to use the default engineering principles?
(code quality, testing, documentation, etc.)

[Y] Yes - Use recommended defaults
[N] No - I'll provide custom principles

Your choice [Y/N]: ___
════════════════════════════════════════════════════════════
```

**WAIT FOR USER RESPONSE. DO NOT proceed until answered.**

---

### Process User Response

**IF user chooses Y (defaults):**

```bash
speckitadv constitution --stage=2 --defaults
```

**IF user chooses N (custom):**

---
⏸️ **[STOP: USER_INPUT_REQUIRED - CUSTOM_PRINCIPLES]**

Ask user for their principles:

```text
════════════════════════════════════════════════════════════
CUSTOM PRINCIPLES

Please provide your project principles.
Format: One principle per line, or a comma-separated list.

Examples:
  • "No Tests, No TDD"
  • "Focus on simplicity over abstraction"
  • "Code readability first, performance second"

Your principles: ___
════════════════════════════════════════════════════════════
```

**WAIT FOR USER RESPONSE. DO NOT proceed until answered.**

---

Then run Stage 2 with the collected principles:

```bash
speckitadv constitution --stage=2 --principles="<user's principles>"
```

**IMPORTANT:**
- Always use `--defaults` OR `--principles` flag - never run Stage 2 without one
- Never assume user wants defaults - always ask explicitly
- Capture user's exact wording for custom principles
