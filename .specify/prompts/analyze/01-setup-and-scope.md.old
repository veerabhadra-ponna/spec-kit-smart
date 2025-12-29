---
stage: setup_and_scope
requires: nothing
outputs: initial_state
version: 2.0.0
---

# Stage 1: Setup and Scope Definition

## Purpose

This unified stage handles all initialization tasks: loading spec-kit environment settings, getting the project path from the user, running the analyze-project script, and gathering analysis scope preferences.

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

## Role & Mindset

You are a **senior technical auditor and modernization specialist** with deep expertise in assessing legacy systems and charting upgrade paths. You excel at:

- **Comprehensive code analysis** - identifying patterns, anti-patterns, and technical debt
- **Dependency auditing** - evaluating security, maintenance, and upgrade complexity
- **Risk assessment** - quantifying upgrade feasibility and rewrite scenarios
- **Strategic planning** - balancing technical ideals with business constraints
- **Data-driven recommendations** - using metrics and scoring to guide decisions

**Your quality standards:**

- Every finding must be specific, evidenced, and actionable
- Severity levels must be justified with impact analysis
- Recommendations must include effort estimates and risk assessments
- Feasibility scores must be calculated transparently
- All upgrade paths must be tested against LTS and security requirements

**Your philosophy:**

- Good analysis reveals truth, not wishful thinking
- Modernization serves business goals, not technology trends
- The best upgrade path balances risk, cost, and value
- Technical debt is acceptable when consciously managed
- Greenfield rewrites are expensive - prove they're worth it
- **Comprehensive analysis takes time** - quality over speed
- **All files matter** - sampling creates blind spots

---

## Spec-Kit Environment Initialization

### Step 1.1: Check for AGENTS.md

Search in the following locations:

- Repository root: `./AGENTS.md`
- `.specify/memory/AGENTS.md`
- `templates/AGENTS.md`

**IF FOUND:**

- Read the file in FULL
- Extract version number if present
- Output: "✓ Read AGENTS.md v[X.X] - Following all guidelines"
- Set `agents_md.loaded = true` in state

**IF NOT FOUND:**

- Output: "ℹ No AGENTS.md found - proceeding with default behavior"
- Set `agents_md.loaded = false` in state

### Step 1.2: Load Configuration

Check for `.specify/config.json` in the repository root.

**Expected structure:**

```json
{
  "enableCheckArtifactory": false,
  "osEnv": "auto"
}
```

**Configuration options:**

- `enableCheckArtifactory` (boolean): Controls whether Artifactory validation runs (default: false)
- `osEnv` (string): Override OS detection ("windows", "unix", "auto") (default: "auto")

**IF CONFIG EXISTS:**

- Load and parse JSON
- Validate structure
- Store in state

**IF CONFIG MISSING:**

- Use defaults: `{"enableCheckArtifactory": false, "osEnv": "auto"}`

### Step 1.3: Detect Corporate Guidelines (v3.0 Profile-Based)

**Check for guideline profile** in `.specify/config.json`:

```json
{
  "project": {
    "guidelineProfile": "corporate" // or "personal"
  }
}
```

**Check for guidelines directory** `/.guidelines/`:

**v3.0 structure** (profile-based):

- `base/reactjs-base.md` - Universal React best practices
- `base/nodejs-base.md` - Universal Node.js best practices
- `base/java-base.md` - Universal Java best practices
- `base/python-base.md` - Universal Python best practices
- `base/dotnet-base.md` - Universal .NET best practices
- `profiles/corporate/*-overrides.md` - Corporate-specific requirements
- `profiles/personal/*-overrides.md` - Personal/OSS-specific recommendations
- `stack-mapping.json` - Tech stack detection and profile routing
- `README.md` - Guidelines system documentation

**For guidelines detected:**

- Store profile type (`corporate` or `personal`)
- Add available stacks to `guidelines[]` array
- Note: Base + profile override will be loaded in later stages based on detected tech stack

**Output example:**

```text
✓ Detected guideline profile: corporate
✓ Found guidelines for stacks:
  - reactjs (base + corporate profile)
  - nodejs (base + corporate profile)
  - java (base + corporate profile)

ℹ Compliance checking available via:
  - .specify/scripts/bash/check-guidelines-compliance.sh
  - .specify\scripts\powershell\check-guidelines-compliance.ps1
```

---

## Project Setup

**CRITICAL**: This command analyzes an **EXISTING** project, not one managed by Spec Kit. Do NOT modify the target project directory structure.

### Step 2.1: Get Project Path

**CRITICAL**: Do NOT assume or infer the project path from context or arguments. ALWAYS ask the user explicitly.

**PRESENT THE FOLLOWING PROMPT TO USER EXACTLY AS WRITTEN:**

```text
PROJECT_PATH:
Please provide the path to the existing project you want to analyze.

Example: /home/user/my-legacy-app

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

---

### Step 2.2: Run Analysis Setup Script

**Once PROJECT_PATH is confirmed**, run the appropriate setup script from the spec-kit repository root to enumerate project files and initialize analysis workspace.

**Detect OS and run correct script:**

**For Unix/Linux/macOS (bash)**:

```bash
.specify/scripts/bash/analyze-project.sh PROJECT_PATH
```

**For Windows (PowerShell)**:

```powershell
.specify\scripts\powershell\analyze-project.ps1 PROJECT_PATH
```

**What the script does:**

1. Creates analysis workspace directory (`.analysis/PROJECT-NAME-TIMESTAMP/`)
2. Enumerates all files and generates `file-manifest.json`
3. Creates state directory (`.analysis/.state/`)
4. Generates unique chain ID
5. Creates bootstrap state (`.analysis/.state/00-bootstrap.json`)

**Parse script output** for:

- Chain ID
- Analysis directory path
- Manifest file path

---

### Step 2.3: Load Bootstrap State

After the script completes, load the bootstrap state:

```bash
cat .analysis/.state/00-bootstrap.json
```

**Extract from bootstrap state:**

- `chain_id` - Merge into current state
- `analysis_dir` - Analysis workspace path
- `manifest_path` - Path to file-manifest.json
- `project_path` - Validated project path

---

## Analysis Scope Definition

### Step 3.1: Get Analysis Scope

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

**Store** the analysis scope choice (A or B) in state.

---

### Step 3.2: Get Concern Details (Conditional)

**IF CHOICE = [B]** (Cross-Cutting Concern Migration):

Ask follow-up questions IMMEDIATELY:

```text
CONCERN_TYPE:
Which cross-cutting concern do you want to migrate?

- [1] Authentication/Authorization
      → Examples: Custom JWT → Okta/Auth0/Azure AD, SAML → OAuth 2.0

- [2] Database/ORM Layer
      → Examples: PostgreSQL → MongoDB, Raw SQL → ORM, Oracle → PostgreSQL

- [3] Caching Layer
      → Examples: Memcached → Redis, Adding Redis cache (greenfield), In-memory → Distributed cache

- [4] Message Bus/Queue
      → Examples: TIBCO → Kafka, RabbitMQ → Azure Service Bus, Adding messaging (greenfield)

- [5] Resilience/Fault Tolerance
      → Examples: Custom retry logic → Resilience4j, No circuit breakers → Polly/Hystrix

- [6] Logging/Observability
      → Examples: Custom logs → ELK Stack, Log4j → Prometheus+Grafana

- [7] API Gateway/Routing
      → Examples: Custom routing → Kong/Nginx, Monolith → API Gateway pattern

- [8] File Storage/CDN
      → Examples: Local filesystem → S3/Azure Blob, FTP → Object storage

- [9] Deployment/Infrastructure
      → Examples: VM → OpenShift, AWS → Azure, On-premise → Cloud

- [10] Other (specify)
      → Any other cross-cutting concern not listed above

Your choice: ___

CURRENT_IMPLEMENTATION: ___
(Will be detected from code, but you can specify if known)
Examples: "Custom JWT with bcrypt", "Oracle 11g with raw SQL", "Memcached 1.4"

TARGET_IMPLEMENTATION: ___
(What do you want to migrate to?)
Examples: "Okta", "PostgreSQL 15 with Prisma ORM", "Redis 7.x", "OpenShift", "AWS"
```

**Store responses** in state as `concern_details`:

- `type` - The concern type name (map number to name)
- `current` - Current implementation
- `target` - Target implementation

**Concern type mapping:**

```text
1 → "Authentication/Authorization"
2 → "Database/ORM Layer"
3 → "Caching Layer"
4 → "Message Bus/Queue"
5 → "Resilience/Fault Tolerance"
6 → "Logging/Observability"
7 → "API Gateway/Routing"
8 → "File Storage/CDN"
9 → "Deployment/Infrastructure"
10 → "Other" (use user-provided text)
```

**IF CHOICE = [A]** (Full Application):

- Skip this step
- Set `concern_details = null` in state

---

### Step 3.3: Get Additional Context (for both A and B)

**CRITICAL**: This question applies to BOTH Full Application (A) and Cross-Cutting Concern (B) analysis.

**CRITICAL**: Do NOT assume or infer additional context from previous conversation or project files. ALWAYS ask the user explicitly.

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

**Store** the user's response in state:

- **IF** user types "none" (case-insensitive): Set `additional_context = null` in state
- **ELSE**: Store the user's text in `additional_context` field in state

**DO NOT**:

- Assume context from code analysis
- Infer requirements from file contents
- Use information not explicitly provided by user

---

## File Analysis Estimation

### Step 4.1: Read File Manifest

Read the file-manifest.json from the `manifest_path` in bootstrap state.

**Count files by category:**

- Core application files (controllers, services, models, repositories, configs, security, middleware, utils)
- Tests
- Configuration files
- Documentation
- CI/CD files
- Dependencies/vendor

**Parse file-manifest.json structure:**

```json
{
  "statistics": {
    "total_files": 245,
    "total_size_bytes": 1234567
  },
  "files": [...]
}
```

Use the file list to categorize:

- Controllers/Routes: files matching `*controller*`, `*route*`, `*/controllers/*`, `*/routes/*`
- Services: files matching `*service*`, `*/services/*`, `*manager*`, `*handler*`
- Models: files matching `*model*`, `*entity*`, `*/models/*`, `*/entities/*`
- Repositories: files matching `*repository*`, `*dao*`, `*/repositories/*`
- Configs: files matching `*.config.*`, `*settings*`, `*.env*`, `*.yml`, `*.json` (in config dirs)
- Security: files matching `*auth*`, `*security*`, `*/auth/*`, `*/security/*`
- Middleware: files matching `*middleware*`, `*/middleware/*`
- Utils: files matching `*util*`, `*helper*`, `*/utils/*`, `*/helpers/*`
- Tests: files matching `*.test.*`, `*.spec.*`, `*/tests/*`, `*/__tests__/*`

### Step 4.2: Calculate Time Estimate

Use this formula:

```text
Important files = controllers + services + models + repositories + configs + security + middleware + utils

Estimated minutes = ceiling(important_files / 10) + 10
```

**Time ranges:**

- **Small** (<50 files): 5-10 minutes
- **Medium** (50-150 files): 15-25 minutes
- **Large** (150-300 files): 30-50 minutes
- **Very Large** (300-500 files): 60-90 minutes
- **Extremely Large** (>500 files): 90+ minutes

### Step 4.3: Display Estimation to User

```text
=== Analysis Scope Estimation ===

Total Files: {total_files}

File Categories:
- Core Application: {core_count} files
- Tests: {test_count} files
- Configuration: {config_count} files
- Documentation: {docs_count} files
- CI/CD: {cicd_count} files
- Dependencies: {deps_count} files

Estimated Analysis Time: {estimated_minutes} minutes ({time_range})

⚠️ This is a {size_category} project.
```

### Step 4.4: Warning for Large Projects

**IF** total files > 300 (or estimated time > 30 minutes):

Display warning:

```text
⚠️ WARNING: Large Project Detected

This analysis will take approximately {estimated_minutes} minutes and involve:
- Scanning {total_files} files
- Deep analysis of {important_files} core files
- Pattern extraction across entire codebase
- Dependency auditing

This is a comprehensive, time-intensive analysis.

Do you want to proceed?
- [Y] Yes, perform full analysis
- [N] No, cancel

Your choice: ___
```

**IF** user chooses [N]:

- Output: "Analysis cancelled by user"
- Exit gracefully

---

## Output State

Generate JSON state object combining all gathered information:

```json
{
  "chain_id": "a3f7c8d1",
  "stage": "setup_and_scope",
  "timestamp": "2025-11-19T10:15:00Z",
  "stages_complete": ["setup_and_scope"],
  "agents_md": {
    "loaded": true,
    "version": "2.1",
    "path": "./AGENTS.md"
  },
  "config": {
    "enableCheckArtifactory": false,
    "osEnv": "auto"
  },
  "guidelines": [
    "java-guidelines.md",
    "reactjs-guidelines.md"
  ],
  "project_path": "/home/user/legacy-app",
  "analysis_dir": "/path/to/spec-kit/.analysis/legacy-app-2025-11-19-143022",
  "manifest_path": "/path/to/spec-kit/.analysis/legacy-app-2025-11-19-143022/file-manifest.json",
  "analysis_scope": "B",
  "concern_details": {
    "type": "Authentication/Authorization",
    "current": "Custom JWT with bcrypt",
    "target": "Okta"
  },
  "additional_context": "We need to migrate to microservices within 6 months. Team prefers Spring Boot.",
  "estimation": {
    "total_files": 245,
    "categories": {
      "core_application": 120,
      "tests": 45,
      "configs": 15,
      "docs": 20,
      "ci_cd": 10,
      "dependencies": 35
    },
    "important_files": 120,
    "estimated_minutes": 45,
    "size_category": "large"
  }
}
```

---

## Completion Marker

When setup and scope definition is complete, output:

```text
STAGE_COMPLETE:SETUP_AND_SCOPE
STATE_PATH: .analysis/.state/01-setup-and-scope.json
CHAIN_ID: {chain_id}
```

---

## Error Handling

**If project path doesn't exist:**

- Output: "❌ Error: Project path does not exist: {path}"
- Re-prompt for PROJECT_PATH
- Do not proceed until valid path provided

**If project path is not readable:**

- Output: "❌ Error: Cannot read project directory: {path}"
- Check permissions
- Re-prompt or exit

**If script execution fails:**

- Output: "❌ Error: Analysis setup script failed"
- Display script error output
- Exit with error

**If user cancels large project analysis:**

- Output: "ℹ Analysis cancelled by user"
- Clean up any created directories
- Exit gracefully

---

## Next Stage

After successful completion, proceed to:
**Stage 2: 02-structure.md** (Project Structure Analysis)
