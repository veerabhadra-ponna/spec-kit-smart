---
stage: collect-principles
requires: initialization
outputs: principles_collected
version: 1.0.0
next: 03-generate-constitution.md
---

# Stage 2: Collect Principles

## Purpose

Structure the collected principles for constitution generation.

---

## Collected Principles

The following principles have been collected (via CLI or interactive prompt):

{principles}

Source: {used_defaults:User input}

---

## Task

Review and validate the principles above:

1. **Check completeness** - Are all key areas covered?
   - Code quality and standards
   - Testing requirements
   - Documentation standards
   - Security practices
   - Architecture constraints

2. **Check clarity** - Is each principle:
   - Specific and measurable?
   - Using normative language (MUST, SHOULD, MAY)?
   - Actionable in code reviews?

3. **Identify gaps** - Suggest additional principles if critical areas are missing

---

## Output

Confirm principles are ready for constitution generation:

```text
✓ Principles validated: [N] principles
  - Quality coverage: [Complete/Needs additions]
  - Ready for constitution generation
```

---

## NEXT

Run the next stage to generate the constitution:

```text
speckitadv constitution --stage=3 --chain={chain_id}
```
