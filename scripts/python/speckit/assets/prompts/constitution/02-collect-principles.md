---
stage: collect-principles
requires: initialization
outputs: principles_collected
version: 1.0.0
next: 03-generate-constitution.md
---

# Stage 2: Collect Principles

## Purpose

Gather project principles from user input or apply defaults.

---

## Check for User Input

**IF arguments were provided** (JIRA number, principles, or metadata):
- Parse the provided principles
- Extract project metadata (name, team, ratification date)
- Continue to Step 2

**IF no arguments provided** (interactive mode):

Prompt user with this format:

```text
Please provide your constitution principles, or press Enter for defaults.

Option 1: Provide custom principles (copy and fill in):

PRINCIPLES (one per line, format: "Name: Description"):
Library-First: MUST use existing libraries over custom code
Test-First: MUST write tests before implementation
Keep It Simple: MUST minimize abstraction layers

PROJECT METADATA:
Project name: MyApp
Team: Engineering Team
Ratification date: 2025-01-15

Option 2: Use defaults
Simply provide empty input or type "use defaults".
```

**WAIT FOR USER RESPONSE before proceeding.**

---

## Step 2: Apply Defaults (if needed)

**Detection criteria for "no input":**
- User provides empty/whitespace-only input
- User explicitly says "use defaults", "skip", or similar
- User provides project metadata but zero principles

**Default Principles:**
- Good Engineering: MUST follow SOLID, DRY, separation of concerns
- Lean & Simple: MUST avoid over-engineering and unnecessary abstractions
- Readability First: MUST prioritize code clarity over cleverness
- Self-Documenting: MUST write code that explains itself through naming
- Intent Documentation: MUST document WHY, not WHAT
- Test Behavior: MUST write tests that verify behavior, not implementation
- Explicit Errors: MUST handle errors explicitly, no silent failures

**When defaults applied, show user:**

```text

ℹ️ Applied default constitution principles. Run again with custom principles to override.
```

---

## Output

Confirm principles collected:

```text

✓ Principles collected: [N] principles
  - Source: [User input / Defaults]
  - Project: [Name or TBD]
```

---

## NEXT

Run the next stage to generate the constitution:

```text

speckit constitution --stage=3 --chain={{chain_id}}
```
