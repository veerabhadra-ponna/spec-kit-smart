---
stage: complete
requires: analyze
outputs: updated_spec
version: 1.0.0
next: null
---

# Stage 3: Complete

## Purpose

Finalize clarification and report results.

---

## Step 1: Validate Updates

Verify spec updates:
- [ ] Clarifications section has one bullet per answer
- [ ] Total questions <= 5
- [ ] Updated sections have no lingering placeholders
- [ ] No contradictory statements remain
- [ ] Terminology consistent across sections

---

## Step 2: Generate Coverage Report

```markdown
# Clarification Coverage

| Category | Status |
|----------|--------|
| Functional Scope | [Resolved/Clear/Deferred] |
| Domain & Data | [Resolved/Clear/Deferred] |
| Interaction & UX | [Resolved/Clear/Deferred] |
| Non-Functional | [Resolved/Clear/Deferred] |
| Edge Cases | [Resolved/Clear/Deferred] |

**Resolved**: Was Partial/Missing, now addressed
**Clear**: Already sufficient
**Deferred**: Low impact or better for planning phase
```

---

## Step 3: Report Completion

```text

[ok] Clarification complete

Questions asked: [N]
Sections updated: [list]
Spec path: {{feature_spec}}

Outstanding items: [list or "None"]

Next steps:
  - Review updated spec
  - Run /speckitadv.plan to create implementation plan
  - Run /speckitadv.clarify again if new ambiguities emerge
```

---

## Behavior Notes

- **If no ambiguities found**: Report "No critical ambiguities detected" and suggest proceeding
- **If spec missing**: Instruct user to run `/speckitadv.specify` first
- **Multiple sessions supported**: Can run `/speckitadv.clarify` again later

---

## WORKFLOW COMPLETE

Spec is clarified. Proceed to planning.

**Next command:**

```text

speckitadv plan
```
