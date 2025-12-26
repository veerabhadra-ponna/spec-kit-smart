---
stage: file_analysis_phase3
requires: 02b-deep-dive complete
outputs: config_analysis
version: 3.4.0
next: 02d-test-audit.md
time_allocation: 15%
---

# Stage 2C: Configuration Analysis (Phase 3)

## Purpose

Analyze ALL configuration files completely. Configuration contains crucial information about database connections, external services, security settings, and environment-specific behavior.

**Time Allocation:** 15% of file analysis effort
**Coverage Target:** 100% of configuration files

---

## How Context Is Provided

The CLI manages state and provides all context. **Do not read state.json directly.**

Values available in this prompt (already substituted by CLI):
- Project path, analysis directory, scope, context
- Concern type, current/target implementation (Scope B only)

---

## Pre-Check: Verify Previous Substage

1. Verify `{data_dir}/deep-dive-patterns.json` exists
2. Load deep dive patterns

**IF not complete:** STOP - Return to 02b-deep-dive

---

## Step 1: Identify All Configuration Files

Locate configuration files by pattern:

**File Patterns:**

```text
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
[STOP: ANALYZE_APP_CONFIG]**

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

```text
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
  JWT Secret: {env var | [!] HARDCODED}
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
[STOP: ANALYZE_BUILD_CONFIG]**

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

```text
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
[STOP: ANALYZE_INFRA_CONFIG]**

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

```text
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

Save configuration analysis to `{data_dir}/config-analysis.json`:

```powershell
@"
<full config_analysis json here>
"@ | speckitadv write-data config-analysis.json --stage=02c-config-analysis --stdin
```

---

## Output Summary

```text
===========================================================
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
===========================================================

```

---

**[AUTO-CONTINUE]** Immediately proceed to next substage. Do NOT wait for user input.

## Next Substage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
