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

Use the **Write tool** to create `{{spec_file}}` with **complete content**.

**IMPORTANT:** Replace ALL placeholders with actual feature-specific content. Do NOT include placeholder text like `[Brief Title]` or `[initial state]` in the final output.

**Template structure** (fill in all sections):

```markdown
# Feature Specification: [FEATURE NAME]

**Feature Branch**: `{{branch_name}}`
**Created**: {{date}}
**Status**: Draft
**Input**: User description: "{{feature}}"

## User Scenarios & Testing

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [How this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Repeat structure for additional stories - typically 3-5 total]

---

### Edge Cases

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements

### Functional Requirements

- **FR-001**: System MUST [specific capability]
- **FR-002**: System MUST [specific capability]
- **FR-003**: Users MUST be able to [key interaction]

### Key Entities (if feature involves data)

- **[Entity 1]**: [What it represents, key attributes]
- **[Entity 2]**: [Relationships to other entities]

## Success Criteria

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete task in under 2 minutes"]
- **SC-002**: [Performance metric, e.g., "System handles 1000 concurrent users"]
- **SC-003**: [User satisfaction metric, e.g., "90% success rate on first attempt"]
```

**Writing guidelines:**

- Write complete user stories with priorities (P1, P2, P3)
- Include acceptance scenarios in Given/When/Then format
- Add functional requirements with FR-XXX numbering
- Define measurable, technology-agnostic success criteria
- Mark unclear items with [NEEDS CLARIFICATION] (max 3)

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
