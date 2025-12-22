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

**IF FEATURE is NOT "$NONE":**

- Use provided FEATURE value
- Use JIRA if provided (empty string means no JIRA)
- Skip to "Validate Input" section below

**IF FEATURE shows "$NONE"** (interactive mode):

Prompt user with this format:

```text
Please provide the following information:

JIRA: C12345-7890 (optional - press Enter to skip)
FEATURE: Add user authentication with email/password and OAuth2

Format rules:
- Line 1: JIRA: C12345-7890 (optional, or leave blank)
- Line 2: FEATURE: <your description> (required)

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

---

## Validate Input

Check the provided input:

1. **JIRA format** (optional): If provided, must match `C[0-9]{5}-[0-9]{4}` pattern
   - Valid: C12345-7890, or empty/blank (no JIRA)
   - Invalid: JIRA-123, 12345 (wrong format)

2. **Feature description** (required): Must be specific and actionable
   - Contains action verb (add, create, implement, build, fix)
   - Describes a concrete outcome
   - Not vague or abstract

**IF invalid**: Show error and re-prompt.

---

## Output

Confirm input collected:

```text

✓ Input collected
  - JIRA: [number or "none"]
  - Feature: [short summary]
```

---

## NEXT

```text
speckitadv specify --stage=3 --chain={{chain_id}}
```

**Note:** JIRA and feature info collected here will be used by subsequent stages via AI context.
