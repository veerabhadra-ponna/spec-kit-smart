---
stage: input_collection
requires: 01a-initialization
outputs: user_inputs
version: 3.3.0
next: 01c-script-execution.md
---

# Stage 1B: Input Collection

## Purpose

Collect all required inputs from the user through explicit prompts.
Each input requires user response before proceeding.

---

## Pre-Check: CLI-Provided Values

Check if inputs were already collected via CLI interactive mode:

**Context variables to check:**

- `{project_path}` - Project path (required)
- `{scope}` - Analysis scope A or B (required)
- `{context}` - Additional context (optional, may be empty)
- `{concern_type}` - Concern type for scope B (conditional)
- `{current_impl}` - Current implementation for scope B (conditional)
- `{target_impl}` - Target implementation for scope B (conditional)

**IF** `{project_path}` is a valid path (not empty) **AND** `{scope}` is "A" or "B":

- Skip all interactive input prompts below
- Use CLI-provided values directly
- Proceed directly to "Output Summary" section

**ELSE:** Continue with interactive prompts below.

---

## Input 1: Project Path

---

⏸️ **[STOP: USER_INPUT_REQUIRED - PROJECT_PATH]**

Present this prompt to user EXACTLY as written:

```text
════════════════════════════════════════════════════════════
PROJECT PATH

Please provide the absolute path to the existing project
you want to analyze.

Examples:
  Linux/Mac: /home/user/my-legacy-app
  Windows:   C:\Users\user\my-legacy-app

Your path: ___
════════════════════════════════════════════════════════════
```

**WAIT for user response. DO NOT proceed until answered.**

---

### Validate Project Path

When user provides path:

1. Check path exists
2. Check path is readable
3. Check path is a directory (not a file)

**IF validation fails:**

```text
❌ Error: Invalid project path
   Reason: {path does not exist | not readable | not a directory}

Please provide a valid path: ___
```

Re-prompt until valid path provided.

---

## Input 2: Additional Context

---

⏸️ **[STOP: USER_INPUT_REQUIRED - ADDITIONAL_CONTEXT]**

Present this prompt to user EXACTLY as written:

```text
════════════════════════════════════════════════════════════
ADDITIONAL CONTEXT (Optional)

Do you want to provide any additional context to help
with the analysis?

This could include:
  • Known pain points or issues
  • Business requirements or constraints
  • Deployment environment details
  • Team preferences or standards
  • Timeline or budget constraints
  • Any other relevant information

Type your context below, or type "none" to skip:
___
════════════════════════════════════════════════════════════
```

**WAIT for user response. DO NOT proceed until answered.**

---

### Process Additional Context

- **IF** user types "none" (case-insensitive): Set context to empty
- **ELSE**: Store user's text as additional context

---

## Input 3: Analysis Scope

---

⏸️ **[STOP: USER_INPUT_REQUIRED - ANALYSIS_SCOPE]**

Present this prompt to user EXACTLY as written:

```text
════════════════════════════════════════════════════════════
ANALYSIS SCOPE

What type of analysis do you need?

[A] Full Application Modernization
    → Analyze entire codebase comprehensively
    → Generate complete functional/technical specs
    → Suitable for legacy app migration
    → Outputs: analysis-report, functional-spec,
               technical-spec, stage-prompts

[B] Cross-Cutting Concern Migration
    → Analyze entire application context FIRST
    → THEN deep-dive into specific concern
    → Assess abstraction quality for migration
    → Suitable for: auth migration, database swap,
                    caching layer, observability, etc.
    → Outputs: analysis-report, abstraction-assessment,
               concern-migration-plan, rollback-procedure

Your choice [A/B]: ___
════════════════════════════════════════════════════════════
```

**WAIT for user response. DO NOT proceed until answered.**

---

### Validate Analysis Scope

**IF** user response is NOT "A" or "B" (case-insensitive):

```text
❌ Invalid selection. Please choose [A] or [B].

Your choice [A/B]: ___
```

Re-prompt until valid choice received.

---

## Input 4: Concern Details (Conditional)

**ONLY IF** scope is "B":

---

⏸️ **[STOP: USER_INPUT_REQUIRED - CONCERN_DETAILS]**

Present these prompts to user EXACTLY as written:

```text
════════════════════════════════════════════════════════════
CONCERN DETAILS

You selected Cross-Cutting Concern Migration.
Please provide details about the concern:

1. CONCERN TYPE
   Which cross-cutting concern do you want to migrate?

   Examples:
     • Authentication/Authorization
     • Database/ORM Layer
     • Caching Layer
     • Message Bus/Queue
     • Resilience/Fault Tolerance
     • Logging/Observability
     • API Gateway/Routing
     • File Storage/CDN
     • Deployment/Infrastructure

   Your concern type: ___

2. CURRENT IMPLEMENTATION
   What is currently used?
   (Will be detected from code, but specify if known)

   Examples: "Custom JWT with bcrypt", "Oracle 11g", "Memcached 1.4"

   Current implementation: ___

3. TARGET IMPLEMENTATION
   What do you want to migrate to?

   Examples: "Okta", "PostgreSQL 15 with Prisma", "Redis 7.x", "AWS"

   Target implementation: ___
════════════════════════════════════════════════════════════
```

**WAIT for ALL THREE responses. DO NOT proceed until all answered.**

---

## Output Summary

```text
═══════════════════════════════════════════════════════════
  SUBSTAGE COMPLETE: 01b-input-collection

  Collected Inputs:
    Project Path: {project_path}
    Analysis Scope: {scope} ({A=Full Application | B=Cross-Cutting})
    Additional Context: {context or "none"}
    Analysis Folder: {analysis_dir}

  Next: Run speckitadv analyze-project
═══════════════════════════════════════════════════════════
```

## Next Substage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
