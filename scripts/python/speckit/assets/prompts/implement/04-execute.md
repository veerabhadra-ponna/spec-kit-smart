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
- Within each: Tests → Models → Services → Endpoints
- Test each story independently

### Final: Polish

- Cross-cutting concerns
- Documentation
- Compliance verification

---

## Task Completion Tracking

**CRITICAL: Mark [X] immediately after EACH task**

```markdown
Before: - [ ] T012 [US1] Create User model
After:  - [X] T012 [US1] Create User model
```

- Do NOT batch completions
- Report progress: "Completed T012 - Created User model"
- Update tasks.md after EVERY task
- Verify previous task marked before moving on

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

✓ T012 [US1] Create User model - COMPLETE
  - File: src/models/user.py
```

After each phase:

```text

✓ Phase 3 (US1) Complete
  - Tasks: 8/8
  - Tests: Passing
```

---

## NEXT

```text

speckitadv implement --stage=5 --feature-dir={{feature_dir}}
```
