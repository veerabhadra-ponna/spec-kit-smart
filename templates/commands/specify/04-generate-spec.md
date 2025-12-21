---
stage: generate-spec
requires: branch-setup
outputs: spec_file
version: 1.0.0
next: 05-validate-spec.md
---

# Stage 4: Generate Specification

## Purpose

Parse the feature description and generate a complete specification.

---

## Step 1: Load Template

Load `templates/spec-template.md` to understand required sections.

---

## Step 2: Parse Feature Description

Extract from the feature description:
- **Actors**: Who uses this feature?
- **Actions**: What can they do?
- **Data**: What information is involved?
- **Constraints**: What limitations exist?

---

## Step 3: Fill Sections

**User Scenarios & Testing:**
- Define primary user flows
- Include happy path and error cases
- Each scenario must be testable

**Functional Requirements:**
- Each requirement independently testable
- Use reasonable defaults for unspecified details
- Document assumptions in Assumptions section

**Success Criteria:**
- Measurable outcomes (time, percentage, count)
- Technology-agnostic (no frameworks, APIs)
- User-focused (business perspective)

**Examples of good criteria:**
- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"

**Bad criteria (too technical):**
- "API response time is under 200ms"
- "Redis cache hit rate above 80%"

---

## Step 4: Handle Ambiguities

**Only mark with [NEEDS CLARIFICATION] if:**
- Choice significantly impacts scope or UX
- Multiple reasonable interpretations exist
- No reasonable default applies

**LIMIT: Maximum 3 clarification markers.**

Prioritize: scope > security > user experience > technical

**Make informed guesses for:**
- Data retention (industry standard)
- Performance (standard web expectations)
- Error handling (user-friendly messages)
- Authentication (standard OAuth2/sessions)

---

## Output

Write spec to `{{spec_file}}`.

```
✓ Specification generated
  - Sections: [N] completed
  - Clarifications needed: [0-3]
```

---

## NEXT

```
speckit specify --stage=5 --chain={{chain_id}}
```
