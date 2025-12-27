---
stage: research
requires: setup
outputs: research_md
version: 1.1.0
next: 04-design.md
---

# Stage 3: Research & Initial Plan Sections

## Purpose

1. Create research.md with technical decisions
2. Fill initial plan.md sections (Summary, Technical Context, Constitution Check)

---

## Step 1: Extract Unknowns

Review the specification for:

- Items marked "NEEDS CLARIFICATION"
- Dependencies requiring best practices research
- Integrations requiring pattern research
- Technology choices not specified

---

## Step 2: Execute Research

For each unknown or technology choice:

1. Search for authoritative sources
2. Evaluate options and tradeoffs
3. Document findings

---

## Step 3: Create research.md

Use the **Write tool** to create `{{feature_dir}}/research.md`:

```markdown
# Research: <feature name>

## Decision: [Topic 1]

**Chosen**: [what was selected]
**Rationale**: [why selected]
**Alternatives considered**: [what else evaluated]
**Sources**: [links/references]

## Decision: [Topic 2]

...
```

---

## Step 4: Fill Plan Sections (Chunk 1 of 3)

Edit `{{feature_dir}}/plan.md` to fill these sections:

### 4.1 Summary Section

Replace the `[Extract from feature spec...]` placeholder with:

- Primary requirement from spec
- Technical approach from research

### 4.2 Technical Context Section

Fill ALL fields, replacing `[...]` and `NEEDS CLARIFICATION`:

- Language/Version
- Primary Dependencies
- Storage
- Testing
- Target Platform
- Project Type
- Performance Goals
- Constraints
- Scale/Scope

### 4.3 Constitution Check Section

Validate spec against constitution principles. Fill the section with:

- Each principle from constitution.md
- Pass/fail status for each
- Notes on any violations

**IMPORTANT**: Do NOT leave any `[...]` placeholders in these sections.

---

## Step 5: Validate Chunk 1

Verify all sections are filled:

- [ ] research.md created with all decisions
- [ ] Summary section filled (no placeholders)
- [ ] Technical Context filled (no placeholders)
- [ ] Constitution Check completed

**IF violations found in Constitution Check**: Document in Complexity Tracking section.

---

## Output

```text
[ok] Research complete
  - Decisions: [N] documented
  - File: {{feature_dir}}/research.md
  - Plan sections filled: Summary, Technical Context, Constitution Check
```

Then run the next command shown below.
