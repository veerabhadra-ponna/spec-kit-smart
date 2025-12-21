---
stage: setup
requires: initialization
outputs: feature_spec, impl_plan, specs_dir
version: 1.0.0
next: 03-research.md
---

# Stage 2: Setup

## Purpose

Run setup scripts and load context for planning.

---

## Step 1: Collect Constraints (if interactive)

**IF no arguments provided**, prompt user:

```text
Please provide any planning constraints:

CONSTRAINTS:
- Must use PostgreSQL for database
- Performance requirement: < 200ms response time

Format: Each constraint on its own line with dash (-).
Type "none" to proceed without constraints.

Valid constraint types:
- Technology: "Must use PostgreSQL", "Prefer Redis"
- Architecture: "Prefer microservices", "Event-driven"
- Performance: "< 200ms response", "10,000 users"
- Integration: "Use existing auth system"
- Compliance: "GDPR compliant", "Encrypt PII"
```

**WAIT FOR USER RESPONSE.**

---

## Step 2: Run Setup Script

Execute from repo root (cross-platform):

```bash
speckitadv setup-plan --json
```

Parse JSON output for:
- `FEATURE_SPEC` - path to spec.md
- `IMPL_PLAN` - path to plan.md template
- `SPECS_DIR` - feature specs directory
- `BRANCH` - current feature branch

**NOTE**: SPECS_DIR already exists from /specify - do NOT create.

---

## Step 3: Load Context

1. Read `FEATURE_SPEC` (the specification)
2. Read `/memory/constitution.md` (principles)
3. Read `IMPL_PLAN` template

---

## Output

```text

✓ Setup complete
  - Spec: {{feature_spec}}
  - Plan template: {{impl_plan}}
  - Constraints: [N] loaded
```

---

## NEXT

```text

speckit plan --stage=3 --chain={{chain_id}}
```
