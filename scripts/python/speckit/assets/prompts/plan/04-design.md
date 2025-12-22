---
stage: design
requires: research
outputs: data_model, contracts, quickstart
version: 1.0.0
next: null
---

# Stage 4: Design (Phase 1)

## Purpose

Generate design artifacts: data model, API contracts, quickstart.

---

## Prerequisites

Verify `research.md` is complete before proceeding.

---

## Step 1: Generate Data Model

Create `data-model.md`:

```markdown
# Data Model: {{feature_name}}

## Entity: [Name]
**Fields:**
- field1: type (constraints)
- field2: type (constraints)

**Relationships:**
- has_many: [Entity]
- belongs_to: [Entity]

**Validation:**
- [rule from requirements]

**State transitions** (if applicable):
- state1 -> state2 (on event)
```

---

## Step 2: Generate API Contracts

For each user action in spec, create endpoint:

Create files in `/contracts/`:
- OpenAPI spec (for REST)
- GraphQL schema (for GraphQL)

Include for each endpoint:
- Request format
- Response format
- Error responses
- Authentication requirements

---

## Step 3: Create Quickstart

Create `quickstart.md` with:
- Local development setup
- Environment variables
- Database setup
- Running tests
- API examples

---

## Step 4: Update Agent Context

Run agent update command (cross-platform):

```bash
speckitadv update-agent-context {{agent_type}}
```

---

## Output

```text

✅ Planning complete

Artifacts generated:
  - specs/{{feature}}/research.md
  - specs/{{feature}}/data-model.md
  - specs/{{feature}}/contracts/
  - specs/{{feature}}/quickstart.md

Next command:
  speckitadv tasks --chain={{chain_id}}
```

---

## WORKFLOW COMPLETE

Planning is done. Proceed to task generation.
