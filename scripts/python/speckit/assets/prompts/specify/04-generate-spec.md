---
stage: generate-spec
requires: branch-setup
outputs: spec_file
version: 1.1.0
next: 05-validate-spec.md
---

# Stage 4: Generate Specification

## Purpose

Parse the feature description and generate a complete specification file.

---

## Step 1: Parse Feature Description

Extract from the feature description:

- **Actors**: Who uses this feature?
- **Actions**: What can they do?
- **Data**: What information is involved?
- **Constraints**: What limitations exist?

---

## Step 2: Generate Content

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

## Step 3: Handle Ambiguities

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

## Step 4: Write Specification File

Use the **Write tool** to create `{{spec_file}}` with complete content.

**Template structure** (fill in all sections based on feature description):

```markdown
# Feature Specification

**Feature**: {{feature}}
**Number**: {{feature_num}}
**Created**: {{date}}
**JIRA**: {{jira}}

---

## Overview

[Write 2-3 sentences describing the feature purpose and value]

---

## User Stories

### US-1: [Descriptive Story Title]

**As a** [specific user type]
**I want** [concrete goal]
**So that** [measurable benefit]

**Acceptance Criteria:**

- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

[Add more user stories as needed - typically 3-5]

---

## Functional Requirements

### FR-1: [Requirement Name]

[Detailed description of the requirement]

**Validation:**

- [How to verify this requirement is met]

[Add more requirements as needed]

---

## Technical Notes

[Technical considerations, constraints, or architecture notes]

---

## Dependencies

- [ ] [Specific dependency with rationale]

---

## Out of Scope

- [Explicitly excluded item]

---

## Assumptions

- [Assumption made during specification]

---

## Success Criteria

- [Measurable outcome 1]
- [Measurable outcome 2]
```

---

## Output

After writing the file:

```text
✓ Specification generated
  - File: {{spec_file}}
  - User stories: [N]
  - Requirements: [N]
  - Clarifications needed: [0-3]
```

---

## NEXT

```text
speckitadv specify --stage=5 --chain={{chain_id}}
```
