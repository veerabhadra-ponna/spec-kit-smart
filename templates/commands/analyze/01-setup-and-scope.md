---
stage: setup_and_scope
requires: nothing
outputs: project_metadata
version: 3.0.0
---

# Stage 1: Setup and Input Collection

## Purpose

This stage collects all necessary inputs from the user and runs the analyze-project script to generate structured JSON data for AI analysis.

**Key Change from v2.0:** The script now does all data extraction (file enumeration, tech stack detection, file categorization). The AI only collects inputs and loads the resulting JSON files.

---

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

## Step 1: Get Project Path

**CRITICAL**: Do NOT assume or infer the project path from context or arguments. ALWAYS ask the user explicitly.

**PRESENT THE FOLLOWING PROMPT TO USER EXACTLY AS WRITTEN:**

```text
PROJECT_PATH:
Please provide the absolute path to the existing project you want to analyze.

Example: /home/user/my-legacy-app
OR: C:\Users\user\my-legacy-app

Your path: ___
```

**WAIT FOR USER RESPONSE - DO NOT PROCEED UNTIL USER PROVIDES ANSWER.**

**Validation:**

- Path must exist
- Path must be readable
- Path must be a directory

**IF** path validation fails:

- Display error: "❌ Error: Invalid project path. Path must exist and be readable."
- Re-prompt for PROJECT_PATH
- DO NOT proceed until valid path provided

**Store** the validated path in a variable: `PROJECT_PATH`

---

## Step 2: Get Additional Context

**CRITICAL**: Do NOT assume or infer additional context. ALWAYS ask explicitly.

**PRESENT THE FOLLOWING PROMPT TO USER EXACTLY AS WRITTEN:**

```text
ADDITIONAL_CONTEXT:
Do you want to provide any additional context to help with the analysis?

This could include:
- Known pain points or issues
- Business requirements or constraints
- Deployment environment details
- Team preferences or standards
- Timeline or budget constraints
- Any other relevant information

Type "none" if you don't have additional context, or provide your information below:
___
```

**WAIT FOR USER RESPONSE - DO NOT PROCEED UNTIL USER PROVIDES ANSWER.**

**Store** the user's response:

- **IF** user types "none" (case-insensitive): Set `ADDITIONAL_CONTEXT=""` (empty string)
- **ELSE**: Store the user's text in `ADDITIONAL_CONTEXT`

---

## Step 3: Get Analysis Scope

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

**WAIT FOR USER RESPONSE - DO NOT PROCEED UNTIL USER PROVIDES ANSWER.**

**Validation:**

- **IF** user choice is **not** [A] or [B]:
  - Display error: "❌ Invalid selection. Please choose [A] for Full Application or [B] for Cross-Cutting Concern."
  - Re-prompt for ANALYSIS_SCOPE
  - DO NOT proceed until valid choice received

**Store** the analysis scope choice (A or B) in variable: `ANALYSIS_SCOPE`

---

## Step 4: Get Concern Details (Conditional)

**IF ANALYSIS_SCOPE = [B]** (Cross-Cutting Concern Migration):

**PRESENT THE FOLLOWING PROMPTS:**

```text
CONCERN_TYPE:
Which cross-cutting concern do you want to migrate?

Examples:
- Authentication/Authorization
- Database/ORM Layer
- Caching Layer
- Message Bus/Queue
- Resilience/Fault Tolerance
- Logging/Observability
- API Gateway/Routing
- File Storage/CDN
- Deployment/Infrastructure
- Other

Your concern type: ___

CURRENT_IMPLEMENTATION:
What is the current implementation?
(Will be detected from code, but you can specify if known)

Examples: "Custom JWT with bcrypt", "Oracle 11g with raw SQL", "Memcached 1.4"

Your answer: ___

TARGET_IMPLEMENTATION:
What do you want to migrate to?

Examples: "Okta", "PostgreSQL 15 with Prisma ORM", "Redis 7.x", "AWS", "OpenShift"

Your answer: ___
```

**WAIT FOR ALL THREE RESPONSES.**

**Store responses** in variables:

- `CONCERN_TYPE` - The concern type name
- `CURRENT_IMPL` - Current implementation
- `TARGET_IMPL` - Target implementation

**IF ANALYSIS_SCOPE = [A]** (Full Application):

- Skip this step
- Set all concern variables to empty strings

---

## Step 5: Run analyze-project Script

**Detect OS and run correct script with collected inputs:**

**For Unix/Linux/macOS (bash)**:

```bash
.specify/scripts/bash/analyze-project.sh "$PROJECT_PATH" \
  ${ADDITIONAL_CONTEXT:+--context "$ADDITIONAL_CONTEXT"} \
  ${ANALYSIS_SCOPE:+--scope "$ANALYSIS_SCOPE"} \
  ${CONCERN_TYPE:+--concern-type "$CONCERN_TYPE"} \
  ${CURRENT_IMPL:+--current-impl "$CURRENT_IMPL"} \
  ${TARGET_IMPL:+--target-impl "$TARGET_IMPL"}
```

**For Windows (PowerShell)**:

```powershell
$params = @{
    Project = "$PROJECT_PATH"
}
if ($ADDITIONAL_CONTEXT) { $params.Context = $ADDITIONAL_CONTEXT }
if ($ANALYSIS_SCOPE) { $params.Scope = $ANALYSIS_SCOPE }
if ($CONCERN_TYPE) { $params.ConcernType = $CONCERN_TYPE }
if ($CURRENT_IMPL) { $params.CurrentImpl = $CURRENT_IMPL }
if ($TARGET_IMPL) { $params.TargetImpl = $TARGET_IMPL }

.specify\scripts\powershell\analyze-project.ps1 @params
```

**What the script does:**

1. Validates project path
2. Creates analysis workspace directory (`.analysis/PROJECT-NAME-TIMESTAMP/`)
3. Enumerates all files and generates `file-manifest.json`
4. Detects technology stack and generates `tech-stack.json`
5. Analyzes file structure and generates `file-structure.json`
6. Consolidates all inputs into `project-metadata.json`
7. Creates bootstrap state (`.analysis/.state/00-bootstrap.json`)

**Parse script output** for:

- Chain ID
- Analysis directory path
- Confirmation of JSON files created

**IF script fails:**

- Display error message
- Exit with error
- DO NOT proceed

---

## Step 6: Load Generated JSON Files

After the script completes successfully, load all generated JSON files:

```bash
# Load project metadata
cat .analysis/{project}-{timestamp}/project-metadata.json

# Load tech stack
cat .analysis/{project}-{timestamp}/tech-stack.json

# Load file structure
cat .analysis/{project}-{timestamp}/file-structure.json

# Load bootstrap state
cat .analysis/.state/00-bootstrap.json
```

**Extract and merge into state:**

From `project-metadata.json`:
- `schema_version`
- `project_path`
- `project_name`
- `timestamp`
- `user_inputs` (analysis_scope, additional_context, concern_details)
- `workspace` (all paths)

From `tech-stack.json`:
- `languages`
- `frameworks`
- `build_tools`
- `indicators_found`

From `file-structure.json`:
- `total_files`
- `categories` (controllers, services, models, etc.)
- `entry_points`
- `analysis_priority`

From `00-bootstrap.json`:
- `chain_id`

---

## Step 7: Display Summary to User

```text
=== Analysis Setup Complete ===

Project: {project_name}
Path: {project_path}
Chain ID: {chain_id}

Technology Stack Detected:
- Languages: {languages}
- Backend Frameworks: {backend_frameworks}
- Frontend Frameworks: {frontend_frameworks}

File Analysis:
- Total Files: {total_files}
- Core Application Files: {core_file_count}
- Configuration Files: {config_count}
- Test Files: {test_count}

Analysis Scope: {scope_description}
{IF scope=B: Concern: {concern_type} ({current_impl} → {target_impl})}
{IF context provided: Additional Context: Provided}

Workspace: {analysis_dir}

✓ All data generated successfully
✓ Ready for Stage 2: Deep File Analysis
```

---

## Output State

Generate JSON state object with all collected and loaded data:

```json
{
  "schema_version": "3.0.0",
  "chain_id": "a3f7c8d1",
  "stage": "setup_and_scope",
  "timestamp": "2025-11-19T10:15:00Z",
  "stages_complete": ["setup_and_scope"],
  "project_path": "/home/user/legacy-app",
  "project_name": "legacy-app",
  "analysis_dir": "/path/to/spec-kit/.analysis/legacy-app-2025-11-19-143022",
  "user_inputs": {
    "analysis_scope": "B",
    "additional_context": "We need to migrate to microservices within 6 months",
    "concern_details": {
      "type": "Authentication/Authorization",
      "current": "Custom JWT with bcrypt",
      "target": "Okta"
    }
  },
  "tech_stack": {
    "languages": ["java", "javascript"],
    "frameworks": {
      "backend": ["spring-boot-2.7.5"],
      "frontend": ["react-16.8.0"]
    },
    "build_tools": ["maven"],
    "indicators_found": [
      {"file": "pom.xml", "type": "java-maven", "confidence": "high"},
      {"file": "package.json", "type": "nodejs", "confidence": "high"}
    ]
  },
  "file_structure": {
    "total_files": 245,
    "categories": {
      "controllers": 12,
      "services": 28,
      "models": 15,
      "repositories": 18,
      "configs": 10,
      "security": 8,
      "middleware": 5,
      "utils": 12,
      "tests": 45,
      "docs": 15
    },
    "entry_points": [
      "src/main/java/com/example/Application.java",
      "src/main/resources/application.yml"
    ],
    "analysis_priority": {
      "critical": ["configs", "security", "entry_points"],
      "high": ["controllers", "services", "models", "repositories"],
      "medium": ["middleware", "utils"],
      "low": ["tests", "docs"]
    }
  },
  "workspace_files": {
    "manifest_path": "/path/to/.analysis/legacy-app-2025-11-19-143022/file-manifest.json",
    "tech_stack_path": "/path/to/.analysis/legacy-app-2025-11-19-143022/tech-stack.json",
    "file_structure_path": "/path/to/.analysis/legacy-app-2025-11-19-143022/file-structure.json",
    "metadata_path": "/path/to/.analysis/legacy-app-2025-11-19-143022/project-metadata.json"
  }
}
```

---

## Save State

Save the complete state to `.analysis/.state/01-setup-and-scope.json`

---

## Completion Marker

When setup and input collection is complete, output:

```text
STAGE_COMPLETE:SETUP_AND_SCOPE
STATE_PATH: .analysis/.state/01-setup-and-scope.json
CHAIN_ID: {chain_id}
NEXT_STAGE: 02-file-analysis.md
```

---

## Error Handling

**If project path doesn't exist:**

- Output: "❌ Error: Project path does not exist: {path}"
- Re-prompt for PROJECT_PATH
- Do not proceed until valid path provided

**If script execution fails:**

- Output: "❌ Error: Analysis setup script failed"
- Display script error output
- Exit with error

---

## Next Stage

After successful completion, proceed to:

**02-file-analysis.md** (Deep File Analysis using JSON inputs)

**Note:** Stage 02-structure.md is obsolete - all structure data is now in JSON files generated by the script.
