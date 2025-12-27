---
stage: complete
requires: validate-spec
outputs: completion_report
version: 1.0.0
next: null
---

# Stage 6: Complete

## Purpose

Finalize the specification workflow and report results.

---

## Step 1: Generate Summary

Compile the workflow results:

- **Branch**: Current git branch name
- **Spec file**: `{{feature_dir}}/spec.md`
- **Checklist**: `{{feature_dir}}/checklists/requirements.md`

---

## Step 2: Report Completion

Output final summary:

```text
[ok] Specification created successfully

Branch: <current git branch>
Spec: {{feature_dir}}/spec.md

Quality Checklist: [All passed / N items pending]

Next steps:
  1. Review spec.md for accuracy
  2. Run /speckitadv.clarify if clarifications remain
  3. Run /speckitadv.plan to create implementation plan

Suggested commit:
  git add . && git commit -m "docs: create spec for <feature name>"
```

---

## Step 3: Error Recovery Notes

**If branch created but spec incomplete:**

- Fix validation issues
- Re-run validation without re-creating branch

**If script execution failed:**

- Check if branch exists: `git branch`
- Check if spec dir exists: `ls specs/`
- Checkout existing branch if found

**If clarifications abandoned:**

- Run /speckitadv.clarify to resume
- Or proceed to /speckitadv.plan if critical items resolved

---

## WORKFLOW COMPLETE

The specification has been created. No further stages.
