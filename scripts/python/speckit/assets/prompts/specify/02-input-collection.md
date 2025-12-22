---
stage: input-collection
requires: initialization
outputs: jira_number, feature_description
version: 1.0.0
next: 03-branch-setup.md
---

# Stage 2: Input Collection

## Purpose

Collect the JIRA number and feature description from user.

---

## Check for Arguments

**Arguments provided:**

```text
JIRA: {jira:$NONE}
FEATURE: {feature:$NONE}
```

**IF both values above are NOT "$NONE":**
- Use provided JIRA and FEATURE values
- Skip to "Validate Input" section below

**IF either shows "$NONE"** (interactive mode):

Prompt user with this format:

```text
Please provide the following information:

JIRA: C12345-7890
FEATURE: Add user authentication with email/password and OAuth2

Format rules:
- Line 1: JIRA: C12345-7890 (exactly 5 digits, dash, 4 digits)
- Line 2: FEATURE: <your description>

Good examples:
✅ "Add user authentication with email/password and OAuth2"
✅ "Create analytics dashboard showing signups and revenue"
✅ "Implement CSV export for transaction history"

Bad examples (too vague):
❌ "Make it better"
❌ "Add security"
❌ "Improve UI"
```

**WAIT FOR USER RESPONSE.**

**IF values were provided above** (not "$NONE"), use them directly.

---

## Validate Input

Check the provided input:

1. **JIRA format**: Must match `C[0-9]{5}-[0-9]{4}` pattern
   - Valid: C12345-7890
   - Invalid: JIRA-123, 12345

2. **Feature description**: Must be specific and actionable
   - Contains action verb (add, create, implement, build, fix)
   - Describes a concrete outcome
   - Not vague or abstract

**IF invalid**: Show error and re-prompt.

---

## Output

Confirm input collected:

```text

✓ Input collected
  - JIRA: [number]
  - Feature: [short summary]
```

---

## NEXT

```text

speckitadv specify --stage=3 --chain={{chain_id}} --jira={{jira}} --feature="{{feature}}"
```
