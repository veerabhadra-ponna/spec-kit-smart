---
stage: file_analysis_phase3
requires: 02b-deep-dive checkpoint
outputs: config_analysis
version: 3.1.0
next: 02d-test-audit.md
time_allocation: 15%
---

# Stage 2C: Configuration Analysis (Phase 3)

## Purpose

Analyze ALL configuration files completely. Configuration contains crucial information about database connections, external services, security settings, and environment-specific behavior.

**Time Allocation:** 15% of file analysis effort
**Coverage Target:** 100% of configuration files

---

## Pre-Check: Verify Previous Substage

1. Read `.analysis/.checkpoints/02b-deep-dive-complete.json`
2. Confirm `status` = "complete"
3. Load deep dive patterns

**IF not complete:** STOP - Return to 02b-deep-dive.md

---

## Step 1: Identify All Configuration Files

Locate configuration files by pattern:

**File Patterns:**
```
*.properties         # Java properties
*.yml, *.yaml        # YAML configs
*.json               # JSON configs
*.xml                # XML configs (Spring, Maven, etc.)
*.env, .env*         # Environment files
*.toml               # TOML configs (Rust, Python)
*.ini                # INI files
*.conf               # General config files
config/*             # Config directories
settings/*           # Settings directories
application*         # Spring application files
appsettings*         # .NET config files
```

---

## Step 2: Application Configuration

---
⏸️ **[STOP: ANALYZE_APP_CONFIG]**

Analyze all application configuration files (100% coverage):

**For each application config file, extract:**

1. **Database Settings:**
   - Connection URL/host/port
   - Database name
   - Credentials handling (referenced env var)
   - Connection pool settings
   - Timeout settings

2. **External Services:**
   - API endpoints
   - Service URLs
   - Timeout configurations
   - Retry settings

3. **Security Settings:**
   - JWT secrets/keys (note if hardcoded - SECURITY ISSUE)
   - Token expiration
   - CORS configuration
   - SSL/TLS settings

4. **Performance Settings:**
   - Thread pool sizes
   - Cache TTLs
   - Request timeouts
   - Rate limits

5. **Feature Flags:**
   - Toggle names
   - Default values
   - Environment overrides

**Output Format:**
```
Application Configuration Analysis:

Profiles/Environments Detected: {list}

Database:
  Type: {PostgreSQL/MySQL/MongoDB/etc}
  Host: {env var reference or value}
  Connection Pool: min={n}, max={m}
  Timeout: {seconds}

External Services:
  {Service1}: {url} (timeout: {ms})
  {Service2}: {url} (timeout: {ms})

Security:
  JWT Secret: {env var | ⚠️ HARDCODED}
  Token Expiry: {duration}
  CORS Origins: {list or pattern}

Performance:
  Thread Pool: {size}
  Cache TTL: {duration}
  Request Timeout: {duration}
```

---

## Step 3: Build Configuration

---
⏸️ **[STOP: ANALYZE_BUILD_CONFIG]**

Analyze all build configuration files:

**Files to Check:**
- `pom.xml` (Maven)
- `build.gradle`, `build.gradle.kts` (Gradle)
- `package.json` (npm/yarn)
- `pyproject.toml`, `setup.py` (Python)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `*.csproj`, `*.sln` (.NET)

**Extract:**

1. **Project Metadata:**
   - Name, version, description
   - Group/organization
   - Authors/maintainers

2. **Dependencies:**
   - Direct dependencies with versions
   - Dev dependencies
   - Plugin/extension dependencies

3. **Build Settings:**
   - Source/target version
   - Compiler options
   - Build profiles

4. **Scripts/Tasks:**
   - Build commands
   - Test commands
   - Deployment scripts

**Output Format:**
```
Build Configuration Analysis:

Build Tool: {Maven/Gradle/npm/etc}
Project: {name} v{version}

Dependencies: {total_count}
  Runtime: {count}
  Dev/Test: {count}
  Plugins: {count}

Compilation Target: {Java 17 / Node 20 / etc}
Build Profiles: {list}

Scripts/Tasks:
  build: {command}
  test: {command}
  deploy: {command if exists}
```

---

## Step 4: Infrastructure Configuration

---
⏸️ **[STOP: ANALYZE_INFRA_CONFIG]**

Analyze all infrastructure/deployment configuration:

**Files to Check:**
- `Dockerfile`, `docker-compose.yml`
- `kubernetes/*.yaml`, `k8s/*.yaml`
- Helm charts
- Terraform files (`*.tf`)
- CloudFormation templates
- CI/CD configs (`.github/workflows`, `Jenkinsfile`, `.gitlab-ci.yml`)

**Extract:**

1. **Container Configuration:**
   - Base image
   - Exposed ports
   - Environment variables
   - Health checks
   - Resource limits

2. **Orchestration:**
   - Replicas/scaling
   - Load balancing
   - Service discovery
   - Secrets management

3. **CI/CD Pipeline:**
   - Pipeline stages
   - Build steps
   - Test steps
   - Deployment steps

**Output Format:**
```
Infrastructure Configuration Analysis:

Container:
  Runtime: {Docker/Podman}
  Base Image: {image:tag}
  Exposed Ports: {list}
  Health Check: {yes/no}

Orchestration:
  Platform: {K8s/ECS/Docker Compose/None}
  Replicas: {default count}
  Scaling: {HPA/manual/none}

CI/CD:
  Platform: {GitHub Actions/Jenkins/GitLab/etc}
  Stages: {list}
  Deployment: {method}
```

---

## Step 5: Extract All Settings Summary

Create comprehensive settings inventory:

```json
{
  "config_analysis": {
    "application": {
      "profiles": ["{list}"],
      "database": {
        "type": "{engine}",
        "host_source": "{env var name}",
        "pool_size": "{min-max}",
        "timeout_ms": {value}
      },
      "external_services": [
        {"name": "{service}", "url_source": "{env or value}", "timeout_ms": {value}}
      ],
      "security": {
        "jwt_secret_source": "{env var or HARDCODED}",
        "token_expiry_seconds": {value},
        "cors_origins": ["{list}"]
      },
      "performance": {
        "thread_pool_size": {value},
        "cache_ttl_seconds": {value},
        "request_timeout_ms": {value}
      },
      "feature_flags": [
        {"name": "{flag}", "default": "{value}", "description": "{purpose}"}
      ]
    },
    "build": {
      "tool": "{Maven/Gradle/npm/etc}",
      "project_name": "{name}",
      "project_version": "{version}",
      "target_runtime": "{Java 17/Node 20/etc}",
      "dependencies": {
        "runtime": {count},
        "dev": {count},
        "total": {count}
      }
    },
    "infrastructure": {
      "containerization": "{Docker/none}",
      "base_image": "{image:tag}",
      "orchestration": "{K8s/ECS/none}",
      "cicd_platform": "{GitHub Actions/Jenkins/none}"
    },
    "security_issues": [
      {"severity": "HIGH", "issue": "Hardcoded secret in {file}", "line": {n}}
    ],
    "files_analyzed": {count},
    "coverage": "100%"
  }
}
```

---

## Checkpoint: Configuration Analysis Complete

### Create Checkpoint

Write checkpoint file: `.analysis/.checkpoints/02c-config-complete.json`

```json
{
  "substage": "02c-config-analysis",
  "phase": 3,
  "timestamp": "{ISO-8601}",
  "config_files_analyzed": {count},
  "categories_completed": ["application", "build", "infrastructure"],
  "security_issues": {count},
  "coverage": "100%",
  "status": "complete"
}
```

### Verify Checkpoint

1. Read `.analysis/.checkpoints/02c-config-complete.json`
2. Validate all categories completed
3. Confirm 100% coverage achieved

---
⏸️ **[STOP: CHECKPOINT_VERIFY]**

**IF checkpoint verified:** Output: `✓ Checkpoint verified: 02c-config-analysis`
**IF checkpoint failed:** Retry checkpoint creation once, then STOP if still failing

---

## Output Summary

```
═══════════════════════════════════════════════════════════
  SUBSTAGE COMPLETE: 02c-config-analysis (Phase 3)

  Time Used: 15% allocation

  Configuration Files Analyzed: {count}
  Coverage: 100%

  Key Findings:
    Profiles: {list}
    Database: {type}
    External Services: {count}
    CI/CD: {platform}

  Security Issues in Config: {count}

  Proceeding to Phase 4: Test & Dependency Audit
═══════════════════════════════════════════════════════════
```

---

## Next Substage

Proceed immediately to: **02d-test-audit.md**
