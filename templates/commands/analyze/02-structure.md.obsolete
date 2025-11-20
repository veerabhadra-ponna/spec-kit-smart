---
stage: structure_analysis
requires: 01-setup-and-scope.json
outputs: structure_state
version: 1.0.0
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

# Stage 3: Project Structure Analysis

## Purpose

Run setup scripts to generate file manifest, detect technology stack, identify project type, and map entry points. This stage creates the foundation for deep file analysis.

---

## Previous State

Load state from: `.analysis/.state/02-scope.json`

You should have:
- `chain_id` - Analysis chain identifier
- `project_path` - Path to project being analyzed
- `analysis_scope` - Type of analysis (A or B)
- `estimation` - File count and categories
- `concern_details` - If scope = B, the concern details

---

## Task

1. Load previous state (analysis_dir, manifest_path already created)
2. Detect technology stack from project files
3. Determine project type (monolith, microservices, etc.)
4. Identify entry points and key architectural elements
5. Load applicable corporate guidelines based on detected stack

---

## Step 1: Load Previous State

**CRITICAL**: The enumeration script was ALREADY run in Stage 1. Do NOT run it again.

**Why**: The setup script (analyze-project.sh/ps1) was executed in Stage 1 and already:
- Created the analysis workspace directory
- Generated the file-manifest.json
- Saved all paths to state

Running it again would create a SECOND directory with a different timestamp, causing artifacts to be split across two locations.

### 1.1: Load Previous State

Load state from: `.analysis/.state/01-setup-and-scope.json`

**Previous state contains**:
- `chain_id` - Analysis chain identifier
- `analysis_dir` - Analysis workspace directory (already created)
- `manifest_path` - Path to file-manifest.json (already generated)
- `project_path` - Project being analyzed
- `analysis_scope` - Type of analysis (A or B)
- `additional_context` - User-provided context (may be null)
- Plus: agents_md, config, guidelines, estimation

**Example state from Stage 1**:

```json
{
  "chain_id": "a3f7c8d1",
  "start_time": "2025-11-15T06:35:36Z",
  "timestamp": "2025-11-15T06:35:36Z",
  "stage": "bootstrap",
  "stages_complete": [],
  "project_path": "/home/user/my-app",
  "project_name": "my-app",
  "analysis_dir": "/home/user/my-app/.analysis/my-app-2025-11-15-143536/",
  "manifest_path": "/home/user/my-app/.analysis/my-app-2025-11-15-143536/file-manifest.json"
}
```text

### 1.2: Extract Values for Current State

Extract these values from previous state and merge into current state:

- `analysis_dir` - Use as-is
- `manifest_path` - Use as-is
- `project_name` - Use as-is
- `analysis_timestamp` - Extract from analysis_dir (the timestamp portion)

**Merge into state**:

```json
{
  ...previous_state_from_02-scope,
  "analysis_dir": ".analysis/my-app-2025-11-15-143536/",
  "manifest_path": ".analysis/my-app-2025-11-15-143536/file-manifest.json",
  "project_name": "my-app",
  "analysis_timestamp": "2025-11-15-143536",
  "manifest_generated": true
}
```text

---

## Step 2: Read and Analyze File Manifest

Read the generated `file-manifest.json`.

**Expected structure**:

```json
{
  "project_path": "/home/user/legacy-app",
  "total_files": 245,
  "categories": {
    "controllers": [...],
    "services": [...],
    "models": [...],
    "repositories": [...],
    "configs": [...],
    "tests": [...],
    "docs": [...],
    "dependencies": [...]
  },
  "files": [
    {
      "path": "src/main/java/com/app/Application.java",
      "category": "entry_point",
      "size": 1234,
      "extension": ".java"
    },
    ...
  ]
}
```text

---

## Step 3: Detect Technology Stack

Scan file manifest and project files to detect technology stack.

### 3.1: Detection Heuristics

**ReactJS**:
- `package.json` with `"react"` dependency
- `.jsx` or `.tsx` files
- React-specific patterns in code

**Java**:
- `pom.xml` (Maven)
- `build.gradle` or `settings.gradle` (Gradle)
- `*.java` files
- Spring Boot: `@SpringBootApplication`, `application.yml/properties`

**.NET**:
- `*.csproj` (C# project files)
- `*.sln` (Solution files)
- `*.cs` files
- `web.config`, `appsettings.json`

**Node.js**:
- `package.json` with backend dependencies (express, fastify, koa, hapi, nest)
- `index.js`, `server.js`, `app.js` entry points
- No React dependency (distinguish from React)

**Python**:
- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `*.py` files
- Framework detection: Django (`manage.py`), Flask (`app.py` with Flask imports)

**Go**:
- `go.mod`, `go.sum`
- `*.go` files

**Ruby**:
- `Gemfile`
- `*.rb` files
- Rails: `config/application.rb`

### 3.2: Extract Version Information

Scan configuration files for versions:

**Java/Spring Boot**:
- `pom.xml`: `<java.version>`, Spring Boot version
- `build.gradle`: Java version, dependency versions

**Node.js**:
- `package.json`: `"node"` in engines, dependency versions

**.NET**:
- `*.csproj`: `<TargetFramework>`, NuGet package versions

**Python**:
- `requirements.txt`: Package versions
- `runtime.txt`: Python version

### 3.3: Detect Additional Technologies

**Database**:
- Scan configs for JDBC URLs, connection strings
- Check dependencies: postgresql, mysql, mongodb, oracle, mssql
- Look for ORM frameworks: Hibernate, JPA, Sequelize, TypeORM, SQLAlchemy, Entity Framework

**Caching**:
- Redis: `redis` dependency, Redis config
- Memcached: `memcached` dependency
- In-memory: Caffeine, Guava Cache

**Message Bus**:
- Kafka: `kafka` dependency, kafka configs
- RabbitMQ: `rabbitmq` dependency
- Azure Service Bus, AWS SQS: Cloud SDK dependencies

**Frontend** (if full-stack):
- React, Vue, Angular detection
- Build tools: Webpack, Vite, Parcel

### 3.4: Build Tech Stack Object

```json
{
  "tech_stack": {
    "primary": "java",
    "secondary": ["react", "postgresql"],
    "versions": {
      "java": "11",
      "spring-boot": "2.3.4",
      "react": "16.13.1",
      "postgresql": "12.5"
    },
    "frameworks": {
      "backend": ["Spring Boot", "Hibernate"],
      "frontend": ["React", "Redux"],
      "testing": ["JUnit", "Mockito", "Jest"]
    },
    "build_tools": {
      "backend": "Maven",
      "frontend": "npm + Webpack"
    },
    "database": {
      "type": "PostgreSQL",
      "version": "12.5",
      "orm": "Hibernate/JPA"
    },
    "caching": {
      "detected": true,
      "type": "Redis",
      "version": "6.2"
    },
    "message_bus": {
      "detected": false
    },
    "observability": {
      "logging": ["SLF4J", "Logback"],
      "monitoring": []
    }
  }
}
```text

---

## Step 4: Determine Project Type

Analyze project structure to classify:

**Monolith**:
- Single deployable unit
- One main entry point
- Shared database
- All code in one repository

**Microservices**:
- Multiple independent services
- Separate deployable units
- Each service has its own entry point
- May have separate databases per service
- Indicators: Multiple `Application.java` files, service-specific configs, API gateway

**Modular Monolith**:
- Single deployment but modular structure
- Clear module boundaries
- Shared database but isolated modules
- Indicators: Modules/packages with clear separation

**Library**:
- Reusable component
- No main entry point
- Published to package registry
- Indicators: `pom.xml` with `<packaging>jar</packaging>`, `package.json` with `"main"` or `"exports"`

**Example classification**:

```json
{
  "project_type": "microservices",
  "structure": {
    "services": ["auth-service", "api-gateway", "user-service", "order-service"],
    "shared_libs": ["common-utils", "dto"],
    "service_count": 4
  }
}
```text

---

## Step 5: Identify Entry Points

Find main entry points and key architectural elements:

**Java/Spring Boot**:
- `@SpringBootApplication` annotated classes
- `public static void main` methods
- Example: `src/main/java/com/app/Application.java`

**Node.js**:
- `index.js`, `server.js`, `app.js`
- `package.json`: `"main"` field

**.NET**:
- `Program.cs`, `Startup.cs`
- ASP.NET Core entry points

**Python**:
- `manage.py` (Django)
- `app.py`, `wsgi.py`, `main.py`

**Map entry points**:

```json
{
  "entry_points": {
    "auth-service": "src/main/java/com/app/auth/AuthApplication.java",
    "api-gateway": "src/main/java/com/app/gateway/GatewayApplication.java",
    "user-service": "src/main/java/com/app/user/UserApplication.java"
  }
}
```text

---

## Step 6: Load Corporate Guidelines

Based on detected tech stack, load applicable guidelines from state.guidelines.

**From state** (loaded in Stage 1):

```json
{
  "guidelines": [
    "java-guidelines.md",
    "reactjs-guidelines.md",
    "nodejs-guidelines.md"
  ]
}
```text

**Match to detected stack**:
- If `tech_stack.primary = "java"` → Load `java-guidelines.md`
- If `tech_stack.secondary` includes "react" → Load `reactjs-guidelines.md`
- If `tech_stack.primary = "nodejs"` → Load `nodejs-guidelines.md`

**For each matched guideline**:
1. Read the guideline file in FULL
2. Extract key requirements:
   - Approved libraries
   - Banned libraries
   - Architecture patterns
   - Security requirements
   - Compliance rules

**Store guideline summaries**:

```json
{
  "guidelines_loaded": {
    "java-guidelines": {
      "loaded": true,
      "approved_libraries": ["Spring Boot", "Hibernate"],
      "banned_libraries": ["Log4j 1.x"],
      "architecture": ["Layered architecture", "DDD patterns"]
    },
    "reactjs-guidelines": {
      "loaded": true,
      "approved_libraries": ["@acmecorp/ui-components"],
      "banned_libraries": ["moment.js"],
      "architecture": ["Component-based", "Hooks-based"]
    }
  }
}
```text

**If no guidelines match**:

```json
{
  "guidelines_loaded": {},
  "guidelines_note": "No corporate guidelines found for detected tech stack. Using industry best practices."
}
```text

---

## Output State

Merge with previous state and add structure analysis data:

```json
{
  ...previous_state,
  "stage": "structure_analysis",
  "timestamp": "2025-11-14T10:20:00Z",
  "stages_complete": ["initialization", "scope_definition", "structure_analysis"],
  "analysis_dir": ".analysis/legacy-app-20251114-102045/",
  "manifest_path": ".analysis/legacy-app-20251114-102045/file-manifest.json",
  "manifest_generated": true,
  "project_name": "legacy-app",
  "analysis_timestamp": "20251114-102045",
  "tech_stack": {
    "primary": "java",
    "secondary": ["react"],
    "versions": {
      "java": "11",
      "spring-boot": "2.3.4",
      "react": "16.13.1"
    },
    "frameworks": {
      "backend": ["Spring Boot", "Hibernate"],
      "frontend": ["React", "Redux"]
    },
    "database": {
      "type": "PostgreSQL",
      "version": "12.5",
      "orm": "Hibernate/JPA"
    },
    "caching": {
      "detected": true,
      "type": "Redis"
    },
    "message_bus": {
      "detected": false
    }
  },
  "project_type": "microservices",
  "structure": {
    "services": ["auth-service", "api-gateway", "user-service"],
    "shared_libs": ["common-utils", "dto"],
    "service_count": 3,
    "entry_points": {
      "auth-service": "src/main/java/com/app/auth/AuthApplication.java",
      "api-gateway": "src/main/java/com/app/gateway/GatewayApplication.java",
      "user-service": "src/main/java/com/app/user/UserApplication.java"
    }
  },
  "guidelines_loaded": {
    "java-guidelines": {
      "loaded": true,
      "approved_libraries": ["Spring Boot", "Hibernate"],
      "banned_libraries": ["Log4j 1.x"]
    },
    "reactjs-guidelines": {
      "loaded": true,
      "approved_libraries": ["@acmecorp/ui-components"]
    }
  }
}
```text

---

## Completion Marker

When structure analysis is complete, output:

```text
STAGE_COMPLETE:STRUCTURE
STATE_PATH: .analysis/.state/02-structure.json
```text

Save the state JSON to `.analysis/.state/02-structure.json`.

---

## Error Handling

**If previous state not found**:
- Output: "❌ Error: Previous state not found at .analysis/.state/01-setup-and-scope.json"
- This means setup script was not run properly
- Abort and instruct user to run analyze-project.sh/ps1 first

**If file-manifest.json not found at bootstrap path**:
- Output: "❌ File manifest not found at {manifest_path from bootstrap}"
- This means enumeration failed during bootstrap
- Fallback to manual directory scanning
- Generate minimal manifest

**If tech stack cannot be detected**:
- Output: "⚠️ Warning: Unable to detect tech stack"
- Set `tech_stack.primary = "unknown"`
- Continue with generic analysis

**If project path not accessible**:
- Output: "❌ Error: Cannot access project: {project_path}"
- Abort and return to Stage 2

---

## Example Execution

```text
=== Stage 3: Structure Analysis ===

Previous state loaded from: .analysis/.state/02-scope.json
Chain ID: a3f7c8d1
Project: /home/user/legacy-app

Loading previous state...
✓ Previous state: .analysis/.state/01-setup-and-scope.json

Extracting paths from bootstrap...
✓ Analysis workspace: .analysis/legacy-app-2025-11-14-102045/
✓ File manifest: .analysis/legacy-app-2025-11-14-102045/file-manifest.json
✓ Project name: legacy-app

Reading file manifest...
✓ Loaded 245 files

Detecting technology stack...
✓ Primary: Java 11
✓ Framework: Spring Boot 2.3.4
✓ Frontend: React 16.13.1
✓ Database: PostgreSQL 12.5 (Hibernate/JPA)
✓ Caching: Redis detected
✓ Message Bus: None detected

Determining project type...
✓ Type: Microservices (3 services)
  - auth-service
  - api-gateway
  - user-service

Identifying entry points...
✓ Mapped 3 entry points

Loading corporate guidelines...
✓ Loaded: java-guidelines.md
✓ Loaded: reactjs-guidelines.md

STAGE_COMPLETE:STRUCTURE
STATE_PATH: .analysis/.state/02-structure.json

Next stage: 03-file-analysis.md
```text

---

## State Schema Reference

This stage must produce a state object conforming to `00-state-schema.json`.

Required new fields:
- `analysis_dir` (string)
- `manifest_path` (string)
- `manifest_generated` (boolean)
- `tech_stack` (object)
- `project_type` (string)
- `structure` (object)

---

## Next Stage

After successful completion, proceed to:
**Stage 4: 03-file-analysis.md** (Deep File Analysis)

This is the most critical stage where comprehensive file scanning occurs.
