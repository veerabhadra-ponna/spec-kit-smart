---
stage: research
requires: setup
outputs: research_md
version: 1.0.0
next: 04-design.md
---

# Stage 3: Research (Phase 0)

## Purpose

Resolve all unknowns and clarifications through research.

---

## Step 1: Extract Unknowns

Review Technical Context from the spec for:
- Items marked "NEEDS CLARIFICATION"
- Dependencies requiring best practices research
- Integrations requiring pattern research

---

## Step 2: Generate Research Tasks

For each unknown:

```text
Task: "Research {unknown} for {feature context}"
```

For each technology choice:

```text
Task: "Find best practices for {tech} in {domain}"
```

---

## Step 3: Execute Research

For each task:
1. Search for authoritative sources
2. Evaluate options and tradeoffs
3. Document findings

---

## Step 4: Consolidate Findings

Create `research.md` in the specs directory:

```markdown
# Research: {{feature_name}}

## Decision: [Topic]
**Chosen**: [what was selected]
**Rationale**: [why selected]
**Alternatives considered**: [what else evaluated]
**Sources**: [links/references]

## Decision: [Topic 2]
...
```

---

## Step 5: Validate

Verify:
- [ ] All NEEDS CLARIFICATION items resolved
- [ ] Each decision has documented rationale
- [ ] Alternatives were evaluated
- [ ] Constitution compliance checked

**IF violations found**: ERROR and revise.

---

## Output

```text

✓ Research complete
  - Decisions: [N] documented
  - Unknowns resolved: [N]
  - File: specs/{{feature}}/research.md
```

---

## NEXT

```text

speckit plan --stage=4 --chain={{chain_id}}
```
