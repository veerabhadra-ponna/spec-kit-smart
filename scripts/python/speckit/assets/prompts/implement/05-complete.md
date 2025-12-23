---
stage: complete
requires: execute
outputs: implementation_complete
version: 1.0.0
next: null
---

# Stage 5: Complete

## Purpose

Validate implementation and report completion.

---

## Step 1: Completion Validation

Verify:
- [ ] All required tasks marked [X]
- [ ] Implementation matches specification
- [ ] Tests pass and coverage meets requirements
- [ ] Implementation follows technical plan
- [ ] Ignore files properly configured

---

## Step 2: Generate Summary

```markdown
# Implementation Summary

**Feature**: {{feature_name}}
**Branch**: {{branch}}

## Task Completion

| Phase | Tasks | Completed |
|-------|-------|-----------|
| Setup | [N] | [N] |
| Foundational | [N] | [N] |
| US1 | [N] | [N] |
| US2 | [N] | [N] |
| Polish | [N] | [N] |
| **Total** | [N] | [N] |

## Artifacts Created

- [list of created files]

## Test Status

- Unit tests: [passing/failing]
- Integration tests: [passing/failing]
- Coverage: [X]%
```

---

## Step 3: Report Completion

```text

✅ Implementation complete

Tasks: [N]/[N] completed
Tests: [status]
Files created: [N]

Next steps:
  1. Review code changes
  2. Run full test suite
  3. Create pull request

Suggested commit:
  git add . && git commit -m "feat: implement {{feature_name}}"
```

---

## Error Recovery Notes

**If stopped mid-phase:**
- Check tasks.md for [X] vs [ ]
- Resume from first unchecked task

**If task failed:**
- Fix error in code
- Keep task [ ] until fixed
- Retry and mark [X] on success

**If tests failing:**
- Do NOT mark [X] if tests fail
- Fix implementation or tests
- Re-run until passing

---

## WORKFLOW COMPLETE

Implementation is done. Ready for code review.
