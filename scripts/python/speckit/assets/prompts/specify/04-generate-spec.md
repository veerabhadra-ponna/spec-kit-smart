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

**Template structure:**

{{include:spec-template.md}}

**Writing guidelines:**

- Replace ALL `[placeholder]` text with actual content
- Remove all HTML comments (`<!-- ... -->`) from output
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
