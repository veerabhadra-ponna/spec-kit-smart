# Token Optimization Analysis

Analysis of token optimization opportunities across prompt files. This document tracks findings for future optimization work.

---

## Optimized Files (Completed)

| File | Before | After | Savings | Approach |
|------|--------|-------|---------|----------|
| `generate-guidelines.md` | 906 | 803 | -103 lines | Consolidated 3 persona descriptions into table format |
| `orchestrate.md` | 1008 | 996 | -12 lines | Removed inline notation notes (already optimized with Mermaid) |
| `resume.md` | 1092 | 1078 | -14 lines | Removed inline notation notes (scenarios already tabled) |

---

## Pending Optimization Candidates

### analyze/06a-functional-spec-legacy.md (949 lines)

**Current State:** Contains verbose example JSON structures and conditional flows.

**Optimization Opportunities:**
- Consolidate example JSON into single reference format
- Convert verbose "If X then Y" conditionals to table format
- Reduce inline documentation that duplicates AGENTS.md content

**Estimated Savings:** ~50-75 lines

**Confidence:** 75% - Core requirements must remain for AI to generate correct output.

**Risk:** Reducing examples may impact AI's understanding of expected output format.

---

### analyze/06b-functional-spec-target.md (884 lines)

**Current State:** Similar structure to 06a with target-specific content.

**Optimization Opportunities:**
- Apply same table-based optimization as 06a
- Consider shared template reference for common sections

**Estimated Savings:** ~40-60 lines

**Confidence:** 75%

---

### analyze/06c1-technical-spec-legacy.md (942 lines)

**Current State:** Contains extensive technical specification templates and examples.

**Optimization Opportunities:**
- Consolidate repeated section structures
- Reference templates instead of inline examples

**Estimated Savings:** ~50-75 lines

**Confidence:** 75%

---

### analyze/06c2-technical-spec-target.md (860 lines)

**Current State:** Similar to 06c1 for target architecture.

**Optimization Opportunities:**
- Same approach as 06c1
- Potential for shared base template

**Estimated Savings:** ~40-60 lines

**Confidence:** 75%

---

### analyze/02a-category-scan.md (387 lines)

**Current State:** Contains file scanning patterns and categorization rules.

**Optimization Opportunities:**
- Pattern lists could be consolidated into tables
- Reduce verbose explanations

**Estimated Savings:** ~20-30 lines

**Confidence:** 85%

---

### analyze/02b-deep-dive.md (500 lines)

**Current State:** Deep analysis instructions with multiple conditional flows.

**Optimization Opportunities:**
- Decision trees could use Mermaid diagrams
- Consolidate repeated instruction patterns

**Estimated Savings:** ~30-50 lines

**Confidence:** 80%

---

## Not Recommended for Optimization

### analyze/03a-full-app.md, analyze/03b-cross-cutting.md

**Reason:** These are parent orchestration prompts that delegate to sub-chunks. Content is already minimal and serves as routing logic.

### analyze/EXECUTION-MODEL.md, analyze/README.md

**Reason:** Documentation files for developers, not for AI consumption. Token optimization not applicable.

---

## Optimization Principles

1. **Tables over Prose:** Convert bulleted lists to markdown tables when possible
2. **Mermaid over ASCII:** Use Mermaid diagrams for workflows (per AGENTS.md)
3. **Reference over Inline:** Reference templates instead of embedding full examples
4. **Core Rules Preserved:** Never remove MUST/SHOULD/NEVER requirements
5. **Test After Changes:** Run full test suite to verify no regressions

---

## Version History

| Date | Change |
|------|--------|
| 2024-12-27 | Initial analysis created |
