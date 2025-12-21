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

- **Branch**: `feature/{{number}}-{{jira}}-{{short_name}}`
- **Spec file**: `specs/{{number}}-{{jira}}-{{short_name}}/spec.md`
- **Checklist**: `specs/{{number}}-{{jira}}-{{short_name}}/checklists/requirements.md`

---

## Step 2: Report Completion

Output final summary:

```text

✅ Specification created successfully

Branch: feature/{{number}}-{{jira}}-{{short_name}}
Spec: specs/{{number}}-{{jira}}-{{short_name}}/spec.md

Quality Checklist: [All passed / N items pending]

Next steps:
  1. Review spec.md for accuracy
  2. Run /clarify if clarifications remain
  3. Run /plan to create implementation plan

Suggested commit:
  git add . && git commit -m "docs: create spec for {{feature_name}}"
```

---

## Step 3: Error Recovery Notes

**If branch created but spec incomplete:**
- Fix validation issues
- Re-run validation without re-creating branch

**If script execution failed:**
- Check if branch exists: `git branch | grep {{short_name}}`
- Check if spec dir exists: `ls specs/`
- Checkout existing branch if found

**If clarifications abandoned:**
- Run `/clarify` to resume
- Or proceed to `/plan` if critical items resolved

---

## WORKFLOW COMPLETE

The specification has been created. No further stages.

**Recommended next command:**

```text

speckit clarify --chain={{chain_id}}
```

or

```text

speckit plan --chain={{chain_id}}
```
