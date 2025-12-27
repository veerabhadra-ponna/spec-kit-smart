---
stage: execute
requires: load-context
outputs: tasks_completed
version: 1.0.0
next: 05-complete.md
---

# Stage 4: Execute Tasks

## Purpose

Execute implementation following the task plan.

---

## [!] File Write Best Practices

**For large file generation:**

- Create files in chunks if content exceeds 2000 characters
- Write skeleton first, then fill sections incrementally
- If using shell commands with content, be aware of OS limits (~8000 chars on Windows)

---

## Execution Rules

1. **Phase-by-phase**: Complete each phase before next
2. **Respect dependencies**: Sequential tasks in order
3. **Parallel tasks [P]**: Can run together
4. **File coordination**: Same-file tasks run sequentially
5. **Validation checkpoints**: Verify each phase

---

## Phase Order

### Phase 1: Setup

- Initialize project structure
- Install dependencies
- Create configuration

**Phase 2: Foundational** (BLOCKING)
- Core infrastructure
- Shared utilities
- Must complete before user stories

### Phase 3+: User Stories

- One phase per story (P1, P2, P3...)
- Within each: Tests -> Models -> Services -> Endpoints
- Test each story independently

### Final: Polish

- Cross-cutting concerns
- Documentation
- Compliance verification

---

## Task Completion Tracking

**CRITICAL: EDIT tasks.md to mark [X] immediately after EACH task**

**Required action after completing any task:**

1. **STOP** before moving to next task
2. **EDIT** the tasks.md file directly
3. **CHANGE** `- [ ]` to `- [X]` for the completed task
4. **VERIFY** the edit saved successfully
5. **REPORT** progress to user

```markdown
Before: - [ ] T012 [US1] Create User model
After:  - [X] T012 [US1] Create User model
```

**Rules:**

- Do NOT batch completions - mark each task immediately
- Do NOT just report completion - you MUST edit tasks.md
- Verify previous task is marked [X] before starting next task
- If you cannot edit the file, STOP and report the issue

**After each phase completes:**

1. Verify ALL tasks in that phase show `[X]`
2. Count and report: "Phase N: X/Y tasks complete"
3. Run relevant tests to validate phase
4. Commit changes before proceeding to next phase

---

## Error Handling

- **Sequential task fails**: Halt execution
- **Parallel task fails**: Continue others, report failed
- Provide clear error messages with context
- If stopping mid-phase, report completed [X] vs remaining [ ]

---

## Output

After each task:

```text

[ok] T012 [US1] Create User model - COMPLETE
  - File: src/models/user.py
```

After each phase:

```text

[ok] Phase 3 (US1) Complete
  - Tasks: 8/8
  - Tests: Passing
```

---

## NEXT

```text

speckitadv implement
```
