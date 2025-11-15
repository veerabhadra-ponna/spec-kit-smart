---
stage: scope_definition
requires: 01-init.json
outputs: scope_state
version: 1.0.0
---

# Stage 2: Analysis Scope Definition

## Purpose

Gather project path and analysis scope from user, run estimation, and prepare for the main analysis workflow.

---

## Previous State

Load state from: `.analysis/.state/01-init.json`

You should have:
- `chain_id` - Unique analysis chain identifier
- `agents_md` - AGENTS.md loading status
- `config` - Configuration settings
- `guidelines` - Available corporate guidelines

---

## Task

Interactively gather:
1. PROJECT_PATH - Path to existing project to analyze
2. ANALYSIS_SCOPE - Type of analysis (Full App or Cross-Cutting Concern)
3. Additional details if Cross-Cutting Concern selected
4. Run estimation to warn user about analysis time

---

## Step 1: Get Project Path

**IF** arguments were provided to the command:
- Parse PROJECT_PATH from arguments
- Validate path exists and is readable
- Continue to Step 2

**ELSE** (interactive mode):

Display prompt:

```text
PROJECT_PATH: /path/to/existing/project
```text

**Example**:

```text
PROJECT_PATH: /home/user/my-legacy-app
```text

**Validation**:
- Path must exist
- Path must be readable
- Path must be a directory
- If invalid, re-prompt with error message

---

## Step 2: Get Analysis Scope

Display the following prompt:

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
```text

**Validation**:

- **IF** user choice is **not** [A] or [B]:
  - Display error: "❌ Invalid selection. Please choose [A] for Full Application or [B] for Cross-Cutting Concern."
  - Re-prompt for ANALYSIS_SCOPE
  - DO NOT proceed until valid choice received

**Store** the analysis scope choice (A or B) in state.

---

## Step 3: Get Concern Details (Conditional)

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

- [5] Logging/Observability
      → Examples: Custom logs → ELK Stack, Log4j → Prometheus+Grafana, Adding observability (greenfield)

- [6] API Gateway/Routing
      → Examples: Custom routing → Kong/Nginx, Monolith → API Gateway pattern

- [7] File Storage/CDN
      → Examples: Local filesystem → S3/Azure Blob, FTP → Object storage

- [8] Deployment/Infrastructure
      → Examples: VM → OpenShift, AWS → Azure, On-premise → Cloud, Dedicated server → Kubernetes

- [9] Other (specify)
      → Any other cross-cutting concern not listed above

Your choice: ___

CURRENT_IMPLEMENTATION: ___
(Will be detected from code, but you can specify if known)
Examples: "Custom JWT with bcrypt", "Oracle 11g with raw SQL", "Memcached 1.4"

TARGET_IMPLEMENTATION: ___
(What do you want to migrate to?)
Examples: "Okta", "PostgreSQL 15 with Prisma ORM", "Redis 7.x", "OpenShift", "AWS"
```text

**Store responses** in state as `concern_details`:
- `type` - The concern type name (map number to name)
- `current` - Current implementation
- `target` - Target implementation

**Concern type mapping**:

```text
1 → "Authentication/Authorization"
2 → "Database/ORM Layer"
3 → "Caching Layer"
4 → "Message Bus/Queue"
5 → "Logging/Observability"
6 → "API Gateway/Routing"
7 → "File Storage/CDN"
8 → "Deployment/Infrastructure"
9 → "Other" (use user-provided text)
```text

**IF CHOICE = [A]** (Full Application):
- Skip this step
- Set `concern_details = null` in state

---

## Step 4: Load File Counts and Calculate Estimation

**CRITICAL**: File enumeration was already done during bootstrap. Do NOT run enumerate scripts again.

### 4.1: Load Bootstrap State

Load the bootstrap state that was created by the setup script:

```bash
# Load from: .analysis/.state/00-bootstrap.json
```

**Bootstrap state contains**:
- `analysis_dir` - Analysis workspace path
- `manifest_path` - Path to file-manifest.json (already generated)

### 4.2: Read File Manifest and Count Categories

Read the file-manifest.json from the bootstrap `manifest_path`.

**Count files by category**:
- Core application files (controllers, services, models, repositories, configs, security, middleware, utils)
- Tests
- Configuration files
- Documentation
- CI/CD files
- Dependencies/vendor

**Parse file-manifest.json structure**:

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

### 4.3: Calculate Time Estimate

Use this formula:

```text
Important files = controllers + services + models + repositories + configs + security + middleware + utils

Estimated minutes = ceiling(important_files / 10) + 10
```text

**Time ranges**:
- **Small** (<50 files): 5-10 minutes
- **Medium** (50-150 files): 15-25 minutes
- **Large** (150-300 files): 30-50 minutes
- **Very Large** (300-500 files): 60-90 minutes
- **Extremely Large** (>500 files): 90+ minutes

### 4.4: Display Estimation to User

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
```text

### 4.5: Warning for Large Projects

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
```text

**IF** user chooses [N]:
- Output: "Analysis cancelled by user"
- Exit gracefully

---

## Output State

Generate JSON state object merging previous state with new data:

```json
{
  ...previous_state,
  "stage": "scope_definition",
  "timestamp": "2025-11-14T10:15:00Z",
  "stages_complete": ["initialization", "scope_definition"],
  "project_path": "/home/user/legacy-app",
  "analysis_scope": "B",
  "concern_details": {
    "type": "Authentication/Authorization",
    "current": "Custom JWT with bcrypt",
    "target": "Okta"
  },
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
```text

**OR for Full Application (scope = A)**:

```json
{
  ...previous_state,
  "stage": "scope_definition",
  "timestamp": "2025-11-14T10:15:00Z",
  "stages_complete": ["initialization", "scope_definition"],
  "project_path": "/home/user/legacy-app",
  "analysis_scope": "A",
  "concern_details": null,
  "estimation": {
    "total_files": 180,
    "categories": {
      "core_application": 85,
      "tests": 35,
      "configs": 12,
      "docs": 18,
      "ci_cd": 8,
      "dependencies": 22
    },
    "important_files": 85,
    "estimated_minutes": 25,
    "size_category": "medium"
  }
}
```text

---

## Completion Marker

When scope definition is complete, output:

```text
STAGE_COMPLETE:SCOPE
STATE_PATH: .analysis/.state/02-scope.json
```text

Save the state JSON to `.analysis/.state/02-scope.json`.

---

## Error Handling

**If project path doesn't exist**:
- Output: "❌ Error: Project path does not exist: {path}"
- Re-prompt for PROJECT_PATH
- Do not proceed until valid path provided

**If project path is not readable**:
- Output: "❌ Error: Cannot read project directory: {path}"
- Check permissions
- Re-prompt or exit

**If enumeration script fails**:
- Output: "❌ Error running enumeration script"
- Display script error output
- Offer to continue with manual file scanning

**If user cancels large project analysis**:
- Output: "ℹ Analysis cancelled by user"
- Clean up any created directories
- Exit gracefully

---

## Example Execution

```text
=== Stage 2: Scope Definition ===

Previous state loaded from: .analysis/.state/01-init.json
Chain ID: a3f7c8d1

PROJECT_PATH: /home/user/legacy-spring-app

Validating path...
✓ Path exists and is readable

ANALYSIS_SCOPE:
What type of analysis do you need?

- [A] Full Application Modernization (entire codebase)
- [B] Cross-Cutting Concern Migration (specific area)

Your choice: B

CONCERN_TYPE:
Which cross-cutting concern do you want to migrate?

[1] Authentication/Authorization
[2] Database/ORM Layer
... (full list)

Your choice: 1

CURRENT_IMPLEMENTATION: Custom JWT with bcrypt and custom user store

TARGET_IMPLEMENTATION: Okta with OAuth 2.0

Running project estimation...
✓ Enumerated 245 files

=== Analysis Scope Estimation ===

Total Files: 245

File Categories:
- Core Application: 120 files
- Tests: 45 files
- Configuration: 15 files
- Documentation: 20 files
- CI/CD: 10 files
- Dependencies: 35 files

Estimated Analysis Time: 45 minutes (large)

⚠️ WARNING: Large Project Detected
... (warning message)

Do you want to proceed? Y

✓ Proceeding with analysis

STAGE_COMPLETE:SCOPE
STATE_PATH: .analysis/.state/02-scope.json

Next stage: 03-structure.md
```text

---

## State Schema Reference

This stage must produce a state object conforming to `00-state-schema.json`.

Required new fields:
- `project_path` (string)
- `analysis_scope` (string: "A" or "B")
- `estimation` (object with total_files, categories, etc.)

Optional fields:
- `concern_details` (object, only if scope = "B")

---

## Next Stage

After successful completion, proceed to:
**Stage 3: 03-structure.md** (Project Structure Analysis)
