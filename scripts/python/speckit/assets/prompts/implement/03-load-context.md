---
stage: load-context
requires: setup
outputs: tasks_loaded, structure_verified
version: 1.0.0
next: 04-execute.md
---

# Stage 3: Load Context

## Purpose

Load design documents and verify project structure.

---

## Step 1: Load Design Documents

From FEATURE_DIR:
- **REQUIRED**: `tasks.md` - Complete task list
- **REQUIRED**: `plan.md` - Tech stack, architecture
- **IF EXISTS**: `data-model.md` - Entities
- **IF EXISTS**: `contracts/` - API specs
- **IF EXISTS**: `research.md` - Decisions
- **IF EXISTS**: `quickstart.md` - Integration scenarios

---

## Step 2: Verify Project Setup

Create/verify ignore files based on tech stack:

**Detection:**
- `git rev-parse --git-dir` → create .gitignore
- `Dockerfile*` exists → create .dockerignore
- `.eslintrc*` exists → create .eslintignore

**Common Patterns by Stack:**
- **Node.js**: `node_modules/`, `dist/`, `*.log`, `.env*`
- **Python**: `__pycache__/`, `.venv/`, `*.pyc`
- **Java**: `target/`, `*.class`, `build/`
- **.NET**: `bin/`, `obj/`, `*.user`
- **Universal**: `.DS_Store`, `.idea/`, `.vscode/`

**If file exists**: Append missing critical patterns only
**If missing**: Create with full pattern set

---

## Step 3: Parse Task Structure

From tasks.md extract:
- **Phases**: Setup, Tests, Core, Integration, Polish
- **Dependencies**: Sequential vs parallel rules
- **Details**: ID, description, file paths, `[P]` markers
- **Execution flow**: Order and dependency requirements

---

## Output

```text

✓ Context loaded
  - Tasks: [N] across [N] phases
  - Tech stack: [detected]
  - Ignore files: [verified / created]
```

---

## NEXT

```text

speckitadv implement
```
