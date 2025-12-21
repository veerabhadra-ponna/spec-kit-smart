---
stage: generate
requires: clarify
outputs: checklist_file
version: 1.0.0
next: null
---

# Stage 3: Generate Checklist

## Purpose

Generate "unit tests for requirements" checklist.

---

## Item Format

**✅ CORRECT (Testing requirements):**
- "Are visual hierarchy requirements defined with measurable criteria? [Clarity]"
- "Are hover state requirements consistent across all elements? [Consistency]"
- "Is fallback behavior defined when images fail to load? [Edge Case, Gap]"

**❌ WRONG (Testing implementation):**
- "Verify button clicks correctly"
- "Test hover states work"
- "Confirm API returns 200"

---

## Quality Dimensions

Organize items by:
- **Completeness**: Are all requirements present?
- **Clarity**: Are requirements unambiguous?
- **Consistency**: Do requirements align?
- **Measurability**: Can requirements be verified?
- **Coverage**: Are all scenarios addressed?
- **Edge Cases**: Are boundaries defined?

---

## Traceability

80%+ items MUST include:
- `[Spec §X.Y]` - Reference to spec section
- `[Gap]` - Missing requirement
- `[Ambiguity]` - Unclear requirement
- `[Conflict]` - Contradicting requirements

---

## File Structure

Create: `{{feature_dir}}/checklists/[domain].md`

```markdown
# [Domain] Requirements Quality Checklist

**Purpose**: Validate [domain] requirement quality
**Created**: {{date}}
**Feature**: {{feature_name}}

## Requirement Completeness
- [ ] CHK001 - Are [X] requirements defined? [Gap]

## Requirement Clarity
- [ ] CHK002 - Is '[term]' quantified? [Ambiguity, Spec §X]

## Scenario Coverage
- [ ] CHK003 - Are [edge cases] addressed? [Coverage]
```

---

## Output

```text

✅ Checklist generated

File: {{feature_dir}}/checklists/[domain].md
Items: [N] total
Traceability: [N]% with references

Focus: [domain]
Audience: [audience]
```

---

## WORKFLOW COMPLETE

Checklist ready for requirements validation.

**Note**: Each `/checklist` run creates a NEW file. Use descriptive domain names.
