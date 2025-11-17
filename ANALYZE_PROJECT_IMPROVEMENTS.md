# Analyze Project Command Improvements - Deterministic Behavior

## Executive Summary

**Problem**: The "analyze project" workflow commands exhibit inconsistent behavior with Claude Sonnet 4 via GitHub Copilot:

- Assuming answers to questionnaires instead of asking users
- Making decisions autonomously without user confirmation
- Not honoring AGENTS.md instructions
- Changing questionnaire wording instead of asking as-is
- Inconsistent artifact generation (functional spec for legacy vs target app)
- Assuming migration for unmentioned components instead of treating them as out-of-scope

**Root Cause**: Commands lack the explicit control structures, waiting patterns, and validation gates that make constitution, specify, and plan commands work consistently.

**Solution**: Apply proven patterns from working commands + implement dual functional spec generation + add explicit scope validation.

---

## Critical Changes Required (High Priority)

### 1. Add Mandatory AGENTS.md Enforcement (All Stages)

**Current Problem**: AGENTS.md check exists but is not strongly enforced.

**Working Pattern** (from constitution.md, specify.md, plan.md):

```markdown
## ⚠️ MANDATORY: Read Agent Instructions First

**BEFORE PROCEEDING:**

1. Check if `AGENTS.md` exists in repository root, `.specify/memory/`, or `templates/` directory
2. **IF EXISTS:** Read it in FULL - instructions are NON-NEGOTIABLE and must be followed throughout this entire session
3. Follow all AGENTS.md guidelines for the duration of this command execution
4. These instructions override any conflicting default behaviors
5. **DO NOT** forget or ignore these instructions as you work through tasks

**Verification:** After reading AGENTS.md (if it exists), acknowledge with:
   "✓ Read AGENTS.md v[X.X] - Following all guidelines"

**If AGENTS.md does not exist:** Proceed with default behavior.

---
```

**Required Action**: Add this EXACT section to the TOP of ALL workflow stage files:

- `templates/commands/analyze-project.md` (line 1)
- `templates/commands/analyze/01-init.md` (line 1)
- `templates/commands/analyze/02-scope.md` (line 1)
- `templates/commands/analyze/03-structure.md` (line 1)
- `templates/commands/analyze/04-file-analysis.md` (line 1)
- `templates/commands/analyze/05a-full-app.md` (line 1)
- `templates/commands/analyze/05b-cross-cutting.md` (line 1)
- `templates/commands/analyze/06-report-generation.md` (line 1)
- `templates/commands/analyze/07-artifacts.md` (line 1)

---

### 2. Enforce "Ask Questionnaires AS-IS" (02-scope.md, 05a-full-app.md)

**Current Problem**: AI changes questionnaire wording or skips questions.

**Solution**: Add explicit instruction blocks BEFORE each questionnaire.

**Pattern to Add** (02-scope.md lines 68-97):

```markdown
---

## ⚠️ CRITICAL: Questionnaire Presentation Rules

**YOU MUST FOLLOW THESE RULES WHEN ASKING QUESTIONS:**

1. **Ask questions EXACTLY as written** - Do NOT rephrase, simplify, or modify wording
2. **Present ALL options** - Do NOT remove or combine choices
3. **Wait for user response** - Do NOT assume or guess answers
4. **One question at a time** - Complete each question before moving to next
5. **Validate input** - If user provides invalid choice, re-prompt with error message
6. **No shortcuts** - Do NOT skip questions even if answer seems obvious

**IF you modify questions or assume answers, this is a CRITICAL ERROR and workflow must restart.**

---

## Step 2: Get Analysis Scope

**PRESENT THE FOLLOWING PROMPT TO USER EXACTLY AS WRITTEN:**

```text
ANALYSIS_SCOPE:
What type of analysis do you need?

- [A] Full Application Modernization (entire codebase)
      → Analyze entire application for comprehensive modernization
      → Generate complete functional/technical specs
      → Suitable for legacy app migration

- [B] Cross-Cutting Concern Migration (specific area)
      → Analyze entire application context FIRST (for informed decisions)
      → THEN deep-dive into specific cross-cutting concern
      → Assess abstraction quality for migration
      → Recommend migration strategy without rewriting entire app
      → Suitable for: auth migration, database swap, caching layer, etc.

Your choice: ___
```

**WAIT FOR USER RESPONSE. Do NOT proceed until user provides [A] or [B].**
```

**Required Action**: Add this pattern to:

- `templates/commands/analyze/02-scope.md` (before Step 2, around line 68)
- `templates/commands/analyze/05a-full-app.md` (before Step 1, around line 29)

---

### 3. Add "Do NOT Assume - Ask First" Pattern (05a-full-app.md)

**Current Problem**: AI assumes modernization preferences instead of asking all 10 questions.

**Solution**: Add explicit "no assumptions" instruction block.

**Pattern to Add** (05a-full-app.md after line 28):

```markdown
---

## ⚠️ MANDATORY: No Assumptions Policy

**YOU MUST ASK ALL 10 QUESTIONS - DO NOT ASSUME ANY ANSWERS.**

**Even if:**

- The answer seems obvious from existing code
- Industry best practices suggest a choice
- User mentioned preferences earlier in conversation
- You think you know what the user wants

**YOU MUST STILL ASK THE QUESTION EXPLICITLY.**

**Failure to ask all 10 questions is a CRITICAL ERROR.**

**IF in doubt about ANY aspect of the questions or user's answer:**

1. **STOP** immediately
2. **ASK** the user for clarification
3. **WAIT** for user response
4. **DO NOT** proceed with assumptions

**Example clarification format:**

```text
⚠️ CLARIFICATION NEEDED

I need clarification on your answer to Question [N]:

You said: "[user's answer]"

I'm unsure about: "[specific ambiguity]"

Options:
- [A] [Interpretation 1]
- [B] [Interpretation 2]
- [C] Other (please specify)

Your choice: ___
```

**REMEMBER**: It's better to ask 5 clarification questions than to make 1 wrong assumption.

---
```

**Required Action**: Add this section to `templates/commands/analyze/05a-full-app.md` at line 29.

---

### 4. Generate BOTH Legacy and Target Functional Specs (07-artifacts.md)

**Current Problem**: Functional spec generation is inconsistent - sometimes describes legacy app (wrong), sometimes target app (right).

**User's Solution**: Generate BOTH specs so there's no confusion and user can use whichever they need.

**Current Artifact 4A** (lines 193-381):

```markdown
### Artifact 4A (Scope = A): functional-spec.md

**Purpose**: Functional specification for modernized application (WHAT system does)
```

**NEW Approach** - Replace with TWO artifacts:

**Artifact 4A-Legacy** (new):

```markdown
### Artifact 4A-Legacy (Scope = A): functional-spec-legacy.md

**Purpose**: Functional specification for LEGACY/EXISTING application (WHAT system currently does)

**CRITICAL - SOURCE OF TRUTH:**

- **Source**: ONLY use analysis-report.md Phase 2 (Feature Catalog) and Phase 3 (Positive Findings)
- **Scope**: Document EXISTING functionality as currently implemented in legacy code
- **Target Audience**: Developers/analysts who need to understand what the legacy app does today
- **Forbidden**: Do NOT include modernization preferences, target tech stack, or future state

**Content Rules:**

1. **Features**: Extract from analysis-report.md Phase 2 exactly as analyzed from legacy code
2. **File References**: Every feature MUST reference legacy code with file:line notation
3. **Technology**: Describe as-implemented (e.g., "Uses custom JWT authentication with bcrypt hashing" not "Should use OAuth2")
4. **State Description**: Present tense (e.g., "The system validates..." not "The system should validate...")
5. **Completeness**: Document what exists, not what's missing (gaps go in technical debt, not functional spec)

**Chunking Strategy** (Generate in 5 chunks):

#### Chunk 1: Introduction + Summary + Current Scope (Legacy)

- Sections: 1 (Introduction), 2 (Executive Summary), 3 (Current Scope)
- Content:
  - What the legacy system does today
  - Current business capabilities
  - Current user base and usage patterns
  - What is IN scope (implemented features)
  - What is OUT of scope (features NOT in legacy system)
- Completion: All 3 sections complete, all present tense, no future-state language

**After Chunk 1 Generation**:

1. **Write to file** using Write tool:
   - File path: `.analysis/{project}-{timestamp}/functional-spec-legacy.md`
   - Content: Complete sections 1-3

2. **Create checkpoint marker**:
   - Create directory: `.analysis/.checkpoints/` (if not exists)
   - Write JSON file: `.analysis/.checkpoints/functional-spec-legacy-chunk-1-complete.json`
   - Content:
     ```json
     {
       "artifact": "functional-spec-legacy.md",
       "chunk": 1,
       "total_chunks": 5,
       "sections": "Introduction + Summary + Current Scope (Legacy)",
       "timestamp": "2025-11-15T10:30:00Z",
       "status": "complete"
     }
     ```

3. **MANDATORY - Display progress**:
   ```text
   ✓ functional-spec-legacy.md Chunk 1/5 complete: Introduction + Summary + Current Scope
     - Lines: [COUNT]
   ```

#### Chunk 2: User Stories (Part 1) - CRITICAL Features (Legacy)

- Section: 4.1 (User Stories - CRITICAL features from legacy system)
- Content: All CRITICAL features CURRENTLY IMPLEMENTED in legacy code
- Every feature MUST have file:line reference to legacy code
- Use present tense: "User can authenticate using..." not "User should be able to..."
- Completion: All CRITICAL features documented with evidence from legacy code

**After Chunk 2 Generation**: [Same checkpoint pattern as above]

#### Chunk 3: User Stories (Part 2) - STANDARD Features + Business Rules (Legacy)

- Sections: 4.2 (STANDARD features), 5 (Business Rules AS IMPLEMENTED)
- Content:
  - STANDARD features from legacy system
  - Business rules and validation logic as currently implemented
  - Edge cases and error handling as they exist today
- Completion: All STANDARD features + current business rules documented

**After Chunk 3 Generation**: [Same checkpoint pattern]

#### Chunk 4: NFRs + Data Requirements (Legacy)

- Sections: 6 (Non-Functional Requirements AS OBSERVED), 7 (Data Requirements CURRENT STATE)
- Content:
  - Performance characteristics observed in legacy system
  - Security measures currently implemented
  - Scalability limits of current system
  - Data entities and relationships as they exist
  - Current database schema (if analyzed)
- Completion: NFRs documented as observed, data models documented as-is

**After Chunk 4 Generation**: [Same checkpoint pattern]

#### Chunk 5: Acceptance Criteria + Assumptions + Constraints (Legacy)

- Sections: 8 (Acceptance Criteria FOR LEGACY BEHAVIOR), 9 (Assumptions ABOUT LEGACY), 10 (Current Constraints)
- Content:
  - How to verify legacy behavior is preserved
  - Assumptions about how legacy system works
  - Constraints in current system
- Completion: All sections complete, no future-state references

**After Chunk 5 Generation**: [Final checkpoint]

**Progress**: `✓ Generated: functional-spec-legacy.md ({lines} lines, {chunks} chunks)`

---

### Artifact 4A-Target (Scope = A): functional-spec-target.md

**Purpose**: Functional specification for TARGET/MODERNIZED application (WHAT system should do)

**CRITICAL - FUTURE STATE:**

- **Source**: Use analysis-report.md + user's 10 modernization preferences from Stage 5A
- **Scope**: Document DESIRED functionality for modernized application
- **Target Audience**: Developers/PMs who will implement the modernized system
- **Requirements**: Include user's chosen tech stack, new capabilities, improvements

**Content Rules:**

1. **Features**: Base on legacy features BUT enhanced with modernization improvements
2. **Technology References**: Use user's chosen target stack (from 10 questions)
3. **Future Tense**: "The system will..." or "Users will be able to..."
4. **Enhancements**: Include new capabilities enabled by modernization (from recommendations)
5. **Out of Scope**: Explicitly document what is NOT being migrated (based on user answers)

**NEW SECTION - Scope Validation** (add after section 3):

### 3.1 Modernization Scope Clarification

**CRITICAL**: Review user's answers to 10 modernization questions from Stage 5A.

**For each component category (Database, Message Bus, Observability), apply this logic:**

```text
IF user explicitly mentioned a target implementation:
  → Component is IN SCOPE for modernization
  → Document target implementation in specs
  → Include migration in technical-spec.md

IF user did NOT mention target implementation:
  → Component is OUT OF SCOPE for modernization
  → Use legacy implementation AS-IS
  → Document as "Out of Scope - Use existing [component] as-is"
  → Do NOT assume migration needed
```

**Example**:

```markdown
## Database

**User Response to Q2**: "PostgreSQL 15" ✅ EXPLICIT TARGET
**Scope**: IN SCOPE - Migrate to PostgreSQL 15
**Action**: Full database migration planning required

## Caching

**User Response to Q3**: [No answer provided or skipped] ❌ NO TARGET
**Scope**: OUT OF SCOPE - Use existing caching as-is (Memcached 1.4)
**Action**: No migration needed, document existing caching in as-is state

## Message Queue

**User Response to Q3**: [Pressed Enter to skip] ❌ SKIPPED
**Scope**: OUT OF SCOPE - No messaging queue in modernization
**Action**: Keep system synchronous, no async messaging
```

**Validation Checklist**:

- [ ] Reviewed all 10 modernization preference answers
- [ ] Identified EXPLICIT targets (user provided specific answer)
- [ ] Identified SKIPPED components (user pressed Enter / provided no answer)
- [ ] Documented OUT OF SCOPE components clearly
- [ ] Confirmed no assumptions made about unmentioned components
- [ ] All IN SCOPE components have target implementations from user answers

---

**Chunking Strategy** (Generate in 5 chunks - similar to legacy but future-tense):

#### Chunk 1: Introduction + Summary + Target Scope

- Content: Modernization goals, target business capabilities, NEW scope boundaries
- Future tense: "The modernized system will provide..."

#### Chunk 2: User Stories (CRITICAL) - Target System

- Content: Critical features in modernized system (may include enhancements)
- Future tense: "User will be able to..."
- Include improvements over legacy (faster, more secure, better UX)

#### Chunk 3: User Stories (STANDARD) + Business Rules - Target System

- Content: Standard features + NEW/ENHANCED business rules
- Document simplified/improved validation logic
- Include new capabilities enabled by target stack

#### Chunk 4: NFRs + Data Requirements - Target System

- Content:
  - IMPROVED performance targets (based on user's choices)
  - ENHANCED security (e.g., OAuth2 if user chose it)
  - SCALABILITY improvements (cloud, containers if user chose them)
  - TARGET data models (may include schema improvements)

#### Chunk 5: Acceptance Criteria + Assumptions + Constraints - Target System

- Content:
  - How to verify modernized behavior meets requirements
  - Assumptions about target environment
  - Constraints for modernized system

**Progress**: `✓ Generated: functional-spec-target.md ({lines} lines, {chunks} chunks)`

---
```

**Required Action**:

1. Replace `Artifact 4A` in `templates/commands/analyze/07-artifacts.md` (lines 193-381) with the TWO artifacts above
2. Update the final summary section (lines 809-839) to include both files:

```markdown
Full Application:
  ✓ functional-spec-legacy.md (WHAT legacy system does today)
  ✓ functional-spec-target.md (WHAT modernized system will do)
  ✓ technical-spec.md (HOW to build modernized system)
  ✓ stage-prompts/
    - constitution-prompt.md
    - clarify-prompt.md
    - tasks-prompt.md
    - implement-prompt.md
```

---

### 5. Add Explicit Scope Validation (05a-full-app.md)

**Current Problem**: For unmentioned components (database, cache, message queue), AI assumes migration is needed. Should treat as out-of-scope.

**Solution**: Add validation logic after collecting all 10 answers.

**Pattern to Add** (05a-full-app.md after line 267):

```markdown
---

## Step 1.1: Modernization Scope Validation

**CRITICAL**: Before proceeding to scoring, validate scope boundaries.

**Purpose**: Ensure we only modernize components the user explicitly wants to change.

### Validation Logic

For each of the 10 modernization questions, apply this logic:

```text
IF user provided EXPLICIT answer (selected option A/B/C/etc. with specific technology):
  → Component is IN SCOPE for modernization
  → Store as explicit target in state
  → Include in complexity scoring
  → Include in migration planning

IF user pressed Enter / skipped / provided NO answer:
  → Component is OUT OF SCOPE
  → Store as "Use existing as-is" in state
  → EXCLUDE from complexity scoring (no migration cost)
  → Document as "Out of Scope" in recommendations

IF answer is ambiguous or unclear:
  → STOP and ask clarifying question
  → Wait for explicit confirmation
  → Do NOT assume or guess
```

### Specific Component Validation

**Run through each question systematically:**

#### Q1: Target Language/Framework
```text
User answer: [record exact answer]
Scope: [IN SCOPE - explicit target: X] OR [OUT OF SCOPE - no target provided]
Action: [Full migration] OR [Keep existing language/framework as-is]
```

#### Q2: Target Database
```text
User answer: [record exact answer]
Scope: [IN SCOPE - explicit target: X] OR [OUT OF SCOPE - no target provided]
Action: [Database migration] OR [Keep existing database as-is]
```

#### Q3: Message Bus/Queue
```text
User answer: [record exact answer]
Was marked OPTIONAL: [Yes/No]
Scope: [IN SCOPE - explicit target: X] OR [OUT OF SCOPE - user skipped/no answer]
Action: [Add/migrate messaging] OR [No messaging changes, keep existing if any]
```

#### Q4: Package Manager
```text
User answer: [record exact answer]
Scope: [IN SCOPE - explicit target: X] OR [OUT OF SCOPE - keep existing]
Action: [Migrate to new package manager] OR [Keep existing package manager]
```

#### Q5: Deployment Target
```text
User answer: [record exact answer]
Scope: [IN SCOPE - explicit target: X] OR [OUT OF SCOPE - keep existing]
Action: [Migrate deployment] OR [Keep existing deployment as-is]
Note: This determines if Q6 and Q7 are asked
```

#### Q6: Infrastructure as Code (Conditional)
```text
Asked: [Yes/No - based on Q5]
User answer: [record exact answer if asked]
Scope: [IN SCOPE - explicit target: X] OR [SKIPPED - not applicable] OR [OUT OF SCOPE - no answer]
Action: [Add IaC] OR [Not applicable] OR [No IaC, manual deployment]
```

#### Q7: Containerization Strategy (Conditional)
```text
Asked: [Yes/No - based on Q5]
User answer: [record exact answer if asked]
Scope: [IN SCOPE - explicit target: X] OR [SKIPPED - not applicable] OR [OUT OF SCOPE - no answer]
Action: [Containerize] OR [Not applicable] OR [No containers, traditional deployment]
```

#### Q8: Observability Stack (Optional)
```text
User answer: [record exact answer]
Was marked OPTIONAL: [Yes/No]
Scope: [IN SCOPE - explicit target: X] OR [OUT OF SCOPE - user skipped/no answer]
Action: [Add/migrate observability] OR [Keep existing observability or none]
```

#### Q9: Security & Authentication
```text
User answer: [record exact answer]
Scope: [IN SCOPE - explicit target: X] OR [OUT OF SCOPE - keep existing]
Action: [Migrate auth] OR [Keep existing auth as-is]
```

#### Q10: Testing Strategy
```text
User answer: [record exact answer]
Scope: [IN SCOPE - explicit target: X] OR [OUT OF SCOPE - keep existing]
Action: [Enhance testing] OR [Keep existing test approach]
```

### Output Scope Summary

After validation, display summary:

```text
=== MODERNIZATION SCOPE VALIDATION ===

Components IN SCOPE (explicit targets provided):
  ✓ Language/Framework: [target]
  ✓ Database: [target]
  ✓ Deployment: [target]

Components OUT OF SCOPE (no targets, use existing as-is):
  • Message Bus: Keep existing [current implementation] as-is
  • Observability: Keep existing logging/monitoring as-is
  • IaC: Not applicable (traditional deployment)

Validation Status: ✓ PASSED
Ready to proceed with complexity scoring for IN SCOPE components only.
```

### Store in State

```json
{
  "modernization_scope": {
    "in_scope": [
      {"component": "language", "current": "...", "target": "...", "explicit": true},
      {"component": "database", "current": "...", "target": "...", "explicit": true}
    ],
    "out_of_scope": [
      {"component": "message_bus", "current": "None", "reason": "User skipped question (optional)", "action": "No changes"},
      {"component": "observability", "current": "Basic logging", "reason": "User provided no answer", "action": "Keep as-is"}
    ],
    "validation_passed": true
  }
}
```

---
```

**Required Action**: Add this section to `templates/commands/analyze/05a-full-app.md` at line 268 (right after Step 1 questions complete, before Step 2 scoring).

---

## Medium Priority Changes

### 6. Add "Wait Explicitly" Pattern (All Interactive Stages)

**Current Problem**: AI doesn't always wait for user responses.

**Solution**: Add explicit wait markers after each user prompt.

**Pattern**:

```markdown
**WAIT FOR USER RESPONSE - DO NOT PROCEED**

[Use 3-second pause if possible, or display clear prompt]

Expected response format: [describe format]
Validation: [describe how to validate]
If invalid: [describe error handling]
```

**Required Action**: Add after every user prompt in:

- `templates/commands/analyze/02-scope.md` (after lines 51, 88, 151)
- `templates/commands/analyze/05a-full-app.md` (after each of the 10 questions)

---

### 7. Add Validation Checklists (End of Each Stage)

**Current Problem**: No verification that all steps were followed correctly.

**Solution**: Add verification checklist at end of each stage.

**Pattern**:

```markdown
---

## Stage Completion Validation

**Before proceeding to next stage, verify:**

- [ ] All questions asked exactly as written (no modifications)
- [ ] All user responses recorded in state
- [ ] No assumptions made (all answers from user)
- [ ] State saved successfully
- [ ] Completion marker output

**IF any checkbox is unchecked, STOP and fix the issue before proceeding.**

---
```

**Required Action**: Add to end of:

- `templates/commands/analyze/02-scope.md` (before completion marker, line 360)
- `templates/commands/analyze/05a-full-app.md` (before completion marker, line 458)
- `templates/commands/analyze/07-artifacts.md` (before completion marker, line 870)

---

### 8. Add "Consistency Markers" for Expected Behavior

**Current Problem**: No clear indicators of expected consistent behavior.

**Solution**: Add consistency markers at key decision points.

**Pattern**:

```markdown
---

## 🎯 CONSISTENCY CHECKPOINT

**Expected Behavior (MUST be identical across all runs):**

1. Present [X] options to user
2. Wait for user selection
3. Record answer in state field: `[field_name]`
4. Validate answer matches expected format: `[format]`
5. If invalid, re-prompt with error message
6. If valid, proceed to next question

**This behavior MUST be consistent regardless of:**

- AI model being used (GPT-4, Claude Sonnet 4, Gemini, etc.)
- Time of day
- Previous conversation context
- Inferred user preferences

**Deviation from this behavior is a CRITICAL ERROR.**

---
```

**Required Action**: Add to:

- `templates/commands/analyze/02-scope.md` (before Step 2, line 68)
- `templates/commands/analyze/05a-full-app.md` (before Step 1, line 29)

---

## Low Priority (Nice-to-Have) Changes

### 9. Add "Debug Mode" Markers

**Pattern**:

```markdown
---

## 🐛 DEBUG CHECKPOINT (for troubleshooting)

**If behavior is inconsistent, check:**

1. Was AGENTS.md read? Expected: `agents_md.loaded = true` in state
2. Were all questions asked? Expected: 10 responses in state
3. Was user response recorded? Expected: `modernization_preferences` object in state
4. Was scope validated? Expected: `in_scope` and `out_of_scope` arrays in state

**To reproduce issue:**

1. Run command with `--debug` flag (if supported)
2. Check state files in `.analysis/.state/` directory
3. Review completion markers in output

---
```

**Required Action**: Add to problematic stages for easier troubleshooting.

---

### 10. Add Examples of Correct vs Incorrect Behavior

**Pattern**:

```markdown
---

## ✅ Correct Behavior Example

**User runs analyze-project command**

```text
AI: ANALYSIS_SCOPE:
    What type of analysis do you need?

    - [A] Full Application Modernization
    - [B] Cross-Cutting Concern Migration

    Your choice: ___

User: A

AI: ✓ Scope recorded: Full Application Modernization

    Now I'll ask 10 questions about your modernization preferences.

    Question 1: Target Language/Framework:
    Current: Java 8
    Options:
    - [A] Java 17 LTS
    - [B] Java 21 LTS
    - [C] Kotlin
    - [D] Other (specify)

    Your choice: ___

User: A

AI: ✓ Target language recorded: Java 17 LTS

    Question 2: Target Database:
    Current: Oracle 11g
    Options:
    ...
```

## ❌ Incorrect Behavior Example

**User runs analyze-project command**

```text
AI: I'll analyze your project for modernization. Based on your codebase,
    I can see you're using Java 8 and Oracle. I'll assume you want to
    upgrade to Java 17 and PostgreSQL since those are common choices.

    [This is WRONG - AI assumed answers without asking]
```

**Another Incorrect Example**:

```text
AI: What do you want to modernize? (Full app or specific concern): ___

User: Full app

AI: Great! For databases, most teams migrate to PostgreSQL. I'll plan
    for that. For deployment, I'll assume Kubernetes since it's industry
    standard.

    [This is WRONG - AI assumed database and deployment without asking]
```

---
```

**Required Action**: Add to:

- `templates/commands/analyze/02-scope.md` (end of file)
- `templates/commands/analyze/05a-full-app.md` (end of file)

---

## Implementation Priority

### Phase 1 (Critical - Fix Now)

1. Add AGENTS.md enforcement to all 9 files
2. Add "Ask Questionnaires AS-IS" pattern to 02-scope.md and 05a-full-app.md
3. Add "No Assumptions" policy to 05a-full-app.md
4. Generate BOTH functional specs in 07-artifacts.md
5. Add scope validation to 05a-full-app.md

### Phase 2 (High Priority - Fix This Week)

1. Add "Wait Explicitly" pattern to interactive stages
2. Add validation checklists to stage endings
3. Add consistency markers to decision points

### Phase 3 (Medium Priority - Nice to Have)

1. Add debug mode markers
2. Add correct vs incorrect examples
3. Add troubleshooting guide

---

## Testing Checklist

After implementing changes, test with:

```markdown
- [ ] Run analyze-project with Claude Sonnet 4 via GitHub Copilot
- [ ] Verify AGENTS.md is read and acknowledged
- [ ] Verify all questionnaires are asked exactly as written
- [ ] Verify AI waits for user response at each prompt
- [ ] Verify NO assumptions are made for skipped questions
- [ ] Verify BOTH functional specs are generated (legacy and target)
- [ ] Verify unmentioned components are marked "out of scope"
- [ ] Run same test 3 times and verify identical behavior
- [ ] Test with different models (GPT-4, Claude, Gemini) to verify consistency
```

---

## Expected Outcome

After implementing these changes:

1. **Consistent questionnaire presentation** - Questions asked exactly as written, every time
2. **No autonomous decisions** - AI waits for explicit user input
3. **AGENTS.md honored** - Instructions followed throughout session
4. **Clear artifact separation** - Legacy spec (what exists) and Target spec (what to build)
5. **Explicit scope boundaries** - Unmentioned components stay as-is, not assumed for migration
6. **Model-agnostic behavior** - Same behavior regardless of Claude Sonnet 4, GPT-4, or other models

---

## Comparison: Why Other Commands Work

### Constitution, Specify, Plan Commands - Success Pattern

These commands work consistently because they:

1. **AGENTS.md at top** - Non-negotiable, read first
2. **Explicit role definition** - Sets clear expectations
3. **Argument validation** - Checks for `$ARGUMENTS` literally
4. **Wait markers** - Explicit "WAIT FOR USER RESPONSE"
5. **Format rules** - Clear input format specifications
6. **Validation gates** - Checklists before proceeding
7. **Error recovery** - Documented failure modes

### Analyze Project Commands - Current Issues

These commands have:

1. ❌ AGENTS.md check exists but not enforced strongly enough
2. ❌ No explicit wait markers
3. ❌ No "ask as-is" policy
4. ❌ No "no assumptions" policy
5. ❌ Ambiguous artifact generation (one functional spec, unclear which app)
6. ❌ No scope validation for unmentioned components
7. ❌ No consistency markers

**Solution**: Copy proven patterns from working commands to analyze-project commands.

---

## Key Insight from User

**User's suggestion**: Generate functional spec for BOTH legacy and target apps.

**Why this is brilliant**:

- Removes all ambiguity (no chance of confusion)
- Provides complete picture (what exists + what to build)
- Gives user flexibility (use whichever they need)
- Makes behavior deterministic (always generate both)
- Mirrors industry practice (current state + future state documentation)

This single change may have the biggest impact on consistency.

---

## Conclusion

The analyze-project commands need to adopt the explicit control structures, validation gates, and user interaction patterns that make constitution, specify, and plan commands work consistently.

The root cause is not command complexity - it's lack of explicit control flow and validation.

By adding:

1. Strong AGENTS.md enforcement
2. "Ask as-is" policies
3. "No assumptions" policies
4. Dual functional spec generation
5. Explicit scope validation

We can achieve the same deterministic, consistent behavior across all models and runs.

---

**Document Version**: 1.0
**Created**: 2025-11-17
**Author**: Senior Dev + Architect + AI Prompt Engineer Analysis
**Status**: Ready for Implementation
