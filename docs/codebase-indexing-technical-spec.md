# Codebase Indexing - Technical Specification

**Version:** 1.0.0
**Status:** Draft
**Last Updated:** 2025-01-15
**Author:** Spec Kit Smart Team

---

## Executive Summary

This document provides technical implementation details for the codebase indexing system, including architecture, data structures, algorithms, prerequisite checks, and integration specifications.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Command Specifications](#2-command-specifications)
3. [Prerequisite Check System](#3-prerequisite-check-system)
4. [Data Extraction Algorithms](#4-data-extraction-algorithms)
5. [Index Storage Format](#5-index-storage-format)
6. [Script Implementation](#6-script-implementation)
7. [AGENTS.md Integration](#7-agentsmd-integration)
8. [Testing Strategy](#8-testing-strategy)
9. [Performance Optimization](#9-performance-optimization)
10. [Security Considerations](#10-security-considerations)

---

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Command Layer                          │
│  /speckitsmart.index | .wiki | .ask | .analyze-project  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Prerequisite Check Layer                    │
│  - check-index-prerequisite.sh (hard requirement)       │
│  - check-index-optional.sh (soft warning)               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                Script Execution Layer                    │
│  - build-codebase-index.sh (index builder)             │
│  - generate-deepwiki.sh (documentation)                 │
│  - search-knowledge-base.sh (query engine)              │
│  - load-index-for-analysis.sh (data loader)             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Index Processing Layer                      │
│  - File Scanner (find + filter)                        │
│  - Code Parser (tree-sitter / regex)                   │
│  - Data Extractor (structure, models, APIs)            │
│  - Dependency Analyzer (import graphs)                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Storage Layer                           │
│  .analysis/index/                                       │
│  ├─ structure.json (code structure)                    │
│  ├─ data-models.json (schemas, entities)               │
│  ├─ api-endpoints.json (REST, GraphQL)                 │
│  ├─ external-apis.json (3rd party)                     │
│  ├─ dependencies.json (import graph)                   │
│  └─ metadata.json (statistics, freshness)              │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow

```
Source Code Files
        ↓
    Scanner (find all files)
        ↓
    Filter (by language/pattern)
        ↓
    Parser (extract AST/structure)
        ↓
    Extractor (classes, functions, models, APIs)
        ↓
    Analyzer (dependencies, relationships)
        ↓
    Aggregator (merge, deduplicate)
        ↓
    Writer (JSON files)
        ↓
    Index Files (.analysis/index/)
```

---

## 2. Command Specifications

### 2.1 `/speckitsmart.index` Implementation

#### 2.1.1 Command Template

**File:** `templates/commands/index.md`

**Frontmatter:**
```yaml
---
description: Build codebase index (PREREQUISITE for analyze-project)
scripts:
  bash: scripts/bash/build-codebase-index.sh
  powershell: scripts/powershell/Build-CodebaseIndex.ps1
---
```

**Key Sections:**
1. Overview and purpose
2. Argument parsing from `$ARGUMENTS`
3. OS detection and script execution
4. Output parsing and display
5. Error handling
6. Next steps suggestion

#### 2.1.2 Execution Flow

```bash
# 1. Parse arguments from $ARGUMENTS environment variable
args="${ARGUMENTS:-}"

# 2. Detect OS
if [[ "$SPEC_KIT_PLATFORM" == "unix" ]]; then
    use_bash=true
elif [[ "$SPEC_KIT_PLATFORM" == "windows" ]]; then
    use_bash=false
else
    # Auto-detect
    if command -v uname &>/dev/null; then
        use_bash=true
    elif [[ "$OS" == "Windows_NT" ]]; then
        use_bash=false
    fi
fi

# 3. Execute appropriate script
if $use_bash; then
    ARGUMENTS="$args" .specify/scripts/bash/build-codebase-index.sh
else
    $env:ARGUMENTS="$args"; .specify\scripts\powershell\Build-CodebaseIndex.ps1
fi

# 4. Parse JSON output
output=$(cat /tmp/index-output.json)
success=$(echo "$output" | jq -r '.success')

# 5. Display results to user
if [[ "$success" == "true" ]]; then
    echo "✓ Index built successfully!"
    # ... format and display statistics
else
    echo "❌ Index build failed"
    # ... display error
fi
```

---

### 2.2 `/speckitsmart.wiki` Implementation

**File:** `templates/commands/wiki.md`

**Frontmatter:**
```yaml
---
description: Generate DeepWiki documentation from index
scripts:
  bash: scripts/bash/generate-deepwiki.sh
  powershell: scripts/powershell/Generate-DeepWiki.ps1
prerequisite_check:
  bash: scripts/bash/check-index-prerequisite.sh
  powershell: scripts/powershell/Check-IndexPrerequisite.ps1
---
```

**Prerequisite Check (MANDATORY):**

```markdown
## ⚠️ PREREQUISITE: Codebase Index Required

**CRITICAL: This command REQUIRES a codebase index.**

### Step 1: Check for Index

**For Unix/Linux/macOS (bash):**
```bash
.specify/scripts/bash/check-index-prerequisite.sh
```

**For Windows (PowerShell):**
```powershell
.specify/scripts/powershell/Check-IndexPrerequisite.ps1
```

**Expected output:**
```json
{
  "index_exists": true,
  "index_path": ".analysis/index",
  "files_indexed": 189
}
```

**If `index_exists: false`:**

**STOP EXECUTION** and display:

```
❌ ERROR: Codebase index not found

DeepWiki generation requires a codebase index.

🔧 Solution:
Run this command first:
  /speckitsmart.index

Estimated time: 30-60 seconds

Then re-run:
  /speckitsmart.wiki
```

**EXIT immediately. DO NOT proceed.**

**If `index_exists: true`:**

Proceed with DeepWiki generation.
```

---

### 2.3 `/speckitsmart.ask` Implementation

**File:** `templates/commands/ask.md`

**Frontmatter:**
```yaml
---
description: Query codebase knowledge base
scripts:
  bash: scripts/bash/search-knowledge-base.sh "$ARGUMENTS"
  powershell: scripts/powershell/Search-KnowledgeBase.ps1 -Query "$ARGUMENTS"
prerequisite_check:
  bash: scripts/bash/check-index-prerequisite.sh
  powershell: scripts/powershell/Check-IndexPrerequisite.ps1
---
```

**Prerequisite Check (MANDATORY):**

```markdown
## Knowledge Base Availability Check

**Step 1: Verify Index Exists**

Run prerequisite check:

**For Unix/Linux/macOS:**
```bash
.specify/scripts/bash/check-index-prerequisite.sh
```

**For Windows:**
```powershell
.specify/scripts/powershell/Check-IndexPrerequisite.ps1
```

**If `index_exists: false`:**

```
❌ ERROR: Index required

The ask command requires a codebase index to answer questions.

🔧 Solution:
1. Build index: /speckitsmart.index
2. (Optional) Generate docs: /speckitsmart.wiki
3. Then ask: /speckitsmart.ask "your question"

EXIT - Do not proceed
```

**If `index_exists: true` but DeepWiki missing:**

```
⚠️ WARNING: DeepWiki not generated

Answers will be based on code index only (lower quality).

💡 For better answers, run:
  /speckitsmart.wiki

Continue anyway? [Y/n]
```

Wait for user input. If 'n' or 'N', exit. Otherwise continue.
```

---

### 2.4 `/speckitsmart.analyze-project` Integration

**File:** `templates/commands/analyze-project.md`

**Insert BEFORE existing execution:**

```markdown
## ⚠️ MANDATORY PREREQUISITE: Codebase Index

**This command REQUIRES a codebase index. It will NOT work without it.**

### Step 1: Check for Index (MANDATORY)

**For Unix/Linux/macOS (bash):**
```bash
.specify/scripts/bash/check-index-prerequisite.sh
```

**For Windows (PowerShell):**
```powershell
.specify/scripts/powershell/Check-IndexPrerequisite.ps1
```

**Expected output:**
```json
{
  "index_exists": true,
  "index_path": ".analysis/index",
  "freshness": "2025-01-15T10:30:00Z",
  "is_stale": false,
  "files_indexed": 189
}
```

---

### Step 2: Handle Check Results

**Case 1: Index Missing (`index_exists: false`)**

**STOP EXECUTION IMMEDIATELY** and display:

```
❌ ERROR: Codebase index not found

This command requires a codebase index for efficient reverse engineering.

🔧 Solution:
Run this command first to build the index:

  /speckitsmart.index

Why indexing is required:
  - 10x faster analysis (uses index instead of reading every file)
  - 80% token reduction (pre-extracted structure)
  - Better accuracy (AST-based vs regex patterns)

Estimated time to build index: 30-60 seconds (one-time cost)

After indexing completes, re-run:

  /speckitsmart.analyze-project
```

**EXIT with code 1. DO NOT PROCEED with analysis.**

---

**Case 2: Index Stale (`is_stale: true`, >7 days old)**

Display warning but ALLOW continuation:

```
⚠️ WARNING: Index is stale

Last updated: {age_days} days ago

Analysis will continue, but results may not reflect recent code changes.

Recommendation: Update index first (takes ~5-10 seconds):

  /speckitsmart.index --incremental

Continue with stale index? (Press Enter to continue, Ctrl+C to abort)
```

Wait for user confirmation (Enter key). Then proceed with analysis.

---

**Case 3: Index Fresh (`is_stale: false`)**

Display confirmation:

```
✓ Index found and fresh
✓ Last updated: 2 hours ago
✓ Files indexed: 189

Proceeding with reverse engineering analysis...
```

Proceed immediately to Step 3.

---

### Step 3: Load Index Data for Analysis

**For Unix/Linux/macOS:**
```bash
.specify/scripts/bash/load-index-for-analysis.sh
```

**For Windows:**
```powershell
.specify/scripts/powershell/Load-IndexForAnalysis.ps1
```

**Script returns comprehensive pre-extracted data:**

```json
{
  "code_structure": {
    "total_classes": 45,
    "total_functions": 312,
    "entry_points": ["src/index.ts", "src/cli.ts"]
  },
  "data_models": {
    "total_entities": 23,
    "entities": [
      {"name": "User", "table": "users", "fields": 8},
      {"name": "Order", "table": "orders", "fields": 12}
    ],
    "schemas": [...]
  },
  "api_surface": {
    "total_rest_endpoints": 45,
    "total_graphql_resolvers": 12,
    "rest_endpoints": [...],
    "authentication": "JWT"
  },
  "external_integrations": {
    "total_services": 5,
    "services": ["Stripe", "AWS S3", "SendGrid", "Auth0", "Twilio"],
    "required_env_vars": [
      {"name": "STRIPE_SECRET_KEY", "required": true},
      {"name": "DATABASE_URL", "required": true}
    ]
  },
  "architecture_patterns": {
    "detected": ["Repository Pattern", "Service Layer", "MVC"],
    "frameworks": ["Express.js", "TypeORM", "React"]
  }
}
```

**Use this pre-extracted data for analysis instead of reading files manually.**

This provides:
- ✅ Complete architecture overview
- ✅ All data models and schemas
- ✅ All API endpoints
- ✅ All external integrations
- ✅ Detected patterns and frameworks

**Then proceed with existing analyze-project workflow...**
```

---

### 2.5 `/speckitsmart.implement` Integration

**File:** `templates/commands/implement.md`

**Insert AFTER Corporate Guidelines section:**

```markdown
## 🔍 Code Reusability Check (Optional but Recommended)

**Index availability: OPTIONAL (soft recommendation)**

### Step 1: Check if Index Available

**For Unix/Linux/macOS:**
```bash
.specify/scripts/bash/check-index-optional.sh
```

**For Windows:**
```powershell
.specify/scripts/powershell/Check-IndexOptional.ps1
```

**Output:**
```json
{
  "index_available": true,
  "files_indexed": 189,
  "last_updated": "2 hours ago"
}
```

---

### Step 2: Handle Results

**If `index_available: false`:**

Display warning but CONTINUE:

```
⚠️ Codebase index not available

You can continue implementation, but you'll miss these benefits:

  ✗ 40-60% code reuse (avoid duplicate implementations)
  ✗ Automatic detection of existing utilities
  ✗ Consistent architecture patterns
  ✗ 80% token reduction in AI queries

💡 To enable code reusability features:
   1. Pause implementation
   2. Run: /speckitsmart.index (takes ~30-60 seconds)
   3. Re-run: /speckitsmart.implement

⏭️ Proceeding without index (standard implementation mode)...
```

**Then SKIP to "Begin Implementation" section (no reusability checks).**

---

**If `index_available: true`:**

Display confirmation:

```
✓ Index available (189 files indexed, updated 2 hours ago)
✓ Code reusability checks ENABLED

For each task, I'll check for:
  - Existing implementations to reuse
  - Utilities and helpers
  - Architecture patterns to follow
  - Test examples

This will help you:
  - Write less code (40-60% reuse)
  - Maintain consistency
  - Follow best practices
```

**Then proceed with reusability checks for each task.**

---

### Step 3: Reusability Check Per Task (Only if Index Available)

**BEFORE implementing each task from tasks.md:**

**For Unix/Linux/macOS:**
```bash
.specify/scripts/bash/find-reusable-code.sh "TASK_DESCRIPTION"
```

**For Windows:**
```powershell
.specify/scripts/powershell/Find-ReusableCode.ps1 -TaskDescription "TASK_DESCRIPTION"
```

**Example Task:** "Implement JWT token validation"

**Script returns:**
```json
{
  "existing_implementations": [
    {
      "file": "src/auth/jwt.ts",
      "function": "validateJWT",
      "line": 45,
      "similarity": 0.92,
      "code_preview": "export async function validateJWT(token: string) {...}",
      "recommendation": "⚠️ HIGH MATCH - Reuse this instead of reimplementing"
    }
  ],
  "reusable_utilities": [
    {
      "file": "src/utils/crypto.ts",
      "exports": ["hashPassword", "verifyPassword", "generateToken"],
      "relevance": 0.78,
      "recommendation": "Use these crypto utilities"
    }
  ],
  "architecture_patterns": [
    {
      "pattern": "Middleware Pattern",
      "examples": ["src/middleware/authenticate.ts", "src/middleware/authorize.ts"],
      "recommendation": "Follow this pattern for auth middleware"
    }
  ],
  "test_examples": [
    {
      "file": "tests/auth/jwt.test.ts",
      "relevance": 0.85,
      "recommendation": "Use this as test template"
    }
  ]
}
```

**Display suggestions to developer:**

```
📋 Task: Implement JWT token validation

🔍 Reusability Check Results:

⚠️ EXISTING IMPLEMENTATION FOUND (92% match)
   File: src/auth/jwt.ts:45
   Function: validateJWT
   Recommendation: REUSE THIS - Don't reimplement

✓ Reusable Utilities:
   - src/utils/crypto.ts (hashPassword, verifyPassword, generateToken)
   Recommendation: Use these for crypto operations

✓ Pattern to Follow:
   - Middleware Pattern (see: src/middleware/authenticate.ts)
   Recommendation: Implement as middleware, not inline

✓ Test Example:
   - tests/auth/jwt.test.ts (85% relevant)
   Recommendation: Use as template for tests

💡 Implementation Guidance:
   1. Import existing validateJWT from src/auth/jwt.ts
   2. Use crypto utilities from src/utils/crypto.ts
   3. Follow middleware pattern
   4. Write tests following example pattern
```

**Then implement using suggestions:**

```typescript
// ✅ GOOD: Following index suggestions
import { validateJWT } from '@/auth/jwt';  // Reusing existing
import { generateToken } from '@/utils/crypto';  // Reusing utility

// Following middleware pattern (from index suggestion)
export const authMiddleware = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  const payload = await validateJWT(token);  // Reusing!
  req.user = payload;
  next();
};

// ❌ BAD: Ignoring index suggestions
import jwt from 'jsonwebtoken';

export const authMiddleware = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  // Reimplementing instead of reusing! Duplicate code!
  const payload = jwt.verify(token, process.env.JWT_SECRET);
  req.user = payload;
  next();
};
```

**Then proceed with next task...**
```

---

## 3. Prerequisite Check System

### 3.1 Check Types

#### 3.1.1 Hard Prerequisite (REQUIRED)

**Used by:** analyze-project, wiki, ask

**Behavior:** STOP execution if index missing

**Script:** `scripts/bash/check-index-prerequisite.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INDEX_DIR="$REPO_ROOT/.analysis/index"

check_index() {
    # Check if index directory exists
    if [[ ! -d "$INDEX_DIR" ]]; then
        cat <<EOF
{
  "index_exists": false,
  "error": "Index directory not found at $INDEX_DIR"
}
EOF
        exit 1
    fi

    # Check if metadata file exists
    if [[ ! -f "$INDEX_DIR/metadata.json" ]]; then
        cat <<EOF
{
  "index_exists": false,
  "error": "Index metadata missing. Index may be corrupted."
}
EOF
        exit 1
    fi

    # Load metadata
    local metadata_file="$INDEX_DIR/metadata.json"
    local freshness=$(jq -r '.freshness' "$metadata_file")
    local files_indexed=$(jq -r '.statistics.indexed_files' "$metadata_file")

    # Calculate age
    local freshness_epoch=$(date -d "$freshness" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$freshness" +%s)
    local now_epoch=$(date +%s)
    local age_seconds=$((now_epoch - freshness_epoch))
    local age_days=$((age_seconds / 86400))

    # Determine staleness (>7 days = stale)
    local is_stale=false
    if [[ $age_days -gt 7 ]]; then
        is_stale=true
    fi

    # Output result
    cat <<EOF
{
  "index_exists": true,
  "index_path": "$INDEX_DIR",
  "freshness": "$freshness",
  "age_days": $age_days,
  "is_stale": $is_stale,
  "files_indexed": $files_indexed
}
EOF
}

check_index
```

**PowerShell equivalent:** `scripts/powershell/Check-IndexPrerequisite.ps1`

```powershell
#!/usr/bin/env pwsh
param()

$RepoRoot = git rev-parse --show-toplevel 2>$null
if (-not $RepoRoot) { $RepoRoot = $PWD }

$IndexDir = Join-Path $RepoRoot ".analysis\index"

# Check if index exists
if (-not (Test-Path $IndexDir)) {
    @{
        index_exists = $false
        error = "Index directory not found at $IndexDir"
    } | ConvertTo-Json -Compress
    exit 1
}

# Check metadata
$metadataPath = Join-Path $IndexDir "metadata.json"
if (-not (Test-Path $metadataPath)) {
    @{
        index_exists = $false
        error = "Index metadata missing. Index may be corrupted."
    } | ConvertTo-Json -Compress
    exit 1
}

# Load metadata
$metadata = Get-Content $metadataPath | ConvertFrom-Json
$freshness = [DateTime]::Parse($metadata.freshness)
$age = (Get-Date) - $freshness
$ageDays = [Math]::Floor($age.TotalDays)
$isStale = $ageDays -gt 7

# Output result
@{
    index_exists = $true
    index_path = $IndexDir
    freshness = $metadata.freshness
    age_days = $ageDays
    is_stale = $isStale
    files_indexed = $metadata.statistics.indexed_files
} | ConvertTo-Json
```

#### 3.1.2 Soft Prerequisite (OPTIONAL)

**Used by:** implement

**Behavior:** WARN if index missing, but CONTINUE

**Script:** `scripts/bash/check-index-optional.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INDEX_DIR="$REPO_ROOT/.analysis/index"

check_index() {
    # Check if index exists
    if [[ ! -d "$INDEX_DIR" ]] || [[ ! -f "$INDEX_DIR/metadata.json" ]]; then
        cat <<EOF
{
  "index_available": false,
  "message": "Index not found. Code reusability checks disabled."
}
EOF
        exit 0  # Not an error, just not available
    fi

    # Get metadata
    local metadata_file="$INDEX_DIR/metadata.json"
    local files_indexed=$(jq -r '.statistics.indexed_files' "$metadata_file")
    local freshness=$(jq -r '.freshness' "$metadata_file")

    # Calculate age for user-friendly display
    local freshness_epoch=$(date -d "$freshness" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$freshness" +%s)
    local now_epoch=$(date +%s)
    local age_seconds=$((now_epoch - freshness_epoch))

    local last_updated
    if [[ $age_seconds -lt 3600 ]]; then
        last_updated="$((age_seconds / 60)) minutes ago"
    elif [[ $age_seconds -lt 86400 ]]; then
        last_updated="$((age_seconds / 3600)) hours ago"
    else
        last_updated="$((age_seconds / 86400)) days ago"
    fi

    # Output success
    cat <<EOF
{
  "index_available": true,
  "files_indexed": $files_indexed,
  "last_updated": "$last_updated",
  "freshness": "$freshness"
}
EOF
}

check_index
```

---

## 4. Data Extraction Algorithms

### 4.1 Code Structure Extraction

**Algorithm:** AST-based parsing with tree-sitter (Phase 1: regex fallback)

**For TypeScript/JavaScript:**

```bash
extract_typescript_structure() {
    local file="$1"
    local classes=()
    local functions=()
    local interfaces=()

    # Extract classes: class ClassName or export class ClassName
    while IFS= read -r line; do
        if [[ "$line" =~ (export[[:space:]]+)?class[[:space:]]+([A-Za-z0-9_]+) ]]; then
            local class_name="${BASH_REMATCH[2]}"
            classes+=("$class_name")

            # Extract methods (simplified - Phase 2 will use tree-sitter)
            # Look for method patterns within class
        fi
    done < "$file"

    # Extract functions
    while IFS= read -r line; do
        if [[ "$line" =~ (export[[:space:]]+)?function[[:space:]]+([A-Za-z0-9_]+) ]]; then
            functions+=("${BASH_REMATCH[2]}")
        elif [[ "$line" =~ (export[[:space:]]+)?const[[:space:]]+([A-Za-z0-9_]+)[[:space:]]*=[[:space:]]*(\(.*\)|async) ]]; then
            functions+=("${BASH_REMATCH[2]}")
        fi
    done < "$file"

    # Extract interfaces
    while IFS= read -r line; do
        if [[ "$line" =~ (export[[:space:]]+)?interface[[:space:]]+([A-Za-z0-9_]+) ]]; then
            interfaces+=("${BASH_REMATCH[2]}")
        fi
    done < "$file"

    # Output JSON
    local relative_path="${file#$REPO_ROOT/}"
    jq -n \
        --arg file "$relative_path" \
        --argjson classes "$(printf '%s\n' "${classes[@]}" | jq -R . | jq -s .)" \
        --argjson functions "$(printf '%s\n' "${functions[@]}" | jq -R . | jq -s .)" \
        --argjson interfaces "$(printf '%s\n' "${interfaces[@]}" | jq -R . | jq -s .)" \
        '{
            file: $file,
            classes: $classes,
            functions: $functions,
            interfaces: $interfaces
        }'
}
```

### 4.2 Data Model Extraction

#### 4.2.1 Prisma Schema Extraction

```bash
extract_prisma_models() {
    local schema_file="$1"
    local models=()

    # Parse Prisma schema
    local in_model=false
    local current_model=""
    local current_fields=()

    while IFS= read -r line; do
        # Detect model start
        if [[ "$line" =~ ^model[[:space:]]+([A-Za-z0-9_]+) ]]; then
            in_model=true
            current_model="${BASH_REMATCH[1]}"
            current_fields=()
        elif [[ "$in_model" == true ]] && [[ "$line" == "}" ]]; then
            # Model end - save it
            models+=("{\"model\": \"$current_model\", \"fields\": [${current_fields[*]}]}")
            in_model=false
        elif [[ "$in_model" == true ]] && [[ "$line" =~ ^[[:space:]]+([A-Za-z0-9_]+)[[:space:]]+([A-Za-z0-9_?]+) ]]; then
            # Field definition
            local field_name="${BASH_REMATCH[1]}"
            local field_type="${BASH_REMATCH[2]}"
            current_fields+=("{\"name\": \"$field_name\", \"type\": \"$field_type\"}")
        fi
    done < "$schema_file"

    echo "$models"
}
```

#### 4.2.2 TypeORM Entity Extraction

```bash
extract_typeorm_entities() {
    local file="$1"
    local entity_name=""
    local table_name=""
    local fields=()

    # Check if file has @Entity decorator
    if ! grep -q "@Entity" "$file"; then
        return
    fi

    # Extract entity name from class
    entity_name=$(grep -oP "class\s+\K[A-Za-z0-9_]+" "$file" | head -1)

    # Extract table name from @Entity decorator (if specified)
    table_name=$(grep -oP '@Entity\("\K[^"]+' "$file" || echo "${entity_name,,}s")

    # Extract fields with @Column decorator
    while IFS= read -r line; do
        if [[ "$line" =~ @Column ]]; then
            # Next line should be field definition
            read -r next_line
            if [[ "$next_line" =~ ([A-Za-z0-9_]+):[[:space:]]*([A-Za-z0-9_]+) ]]; then
                local field_name="${BASH_REMATCH[1]}"
                local field_type="${BASH_REMATCH[2]}"
                fields+=("{\"name\": \"$field_name\", \"type\": \"$field_type\"}")
            fi
        fi
    done < "$file"

    jq -n \
        --arg entity "$entity_name" \
        --arg table "$table_name" \
        --arg file "${file#$REPO_ROOT/}" \
        --argjson fields "[$(IFS=,; echo "${fields[*]}")]" \
        '{
            entity: $entity,
            table: $table,
            file: $file,
            fields: $fields
        }'
}
```

### 4.3 API Endpoint Extraction

#### 4.3.1 Express/Fastify Route Extraction

```bash
extract_rest_routes() {
    local file="$1"
    local routes=()

    # Look for router.get, router.post, app.get, etc.
    while IFS= read -r line; do
        if [[ "$line" =~ (router|app)\.(get|post|put|delete|patch)\([[:space:]]*[\'\"](/[^\'\"]+)[\'\"] ]]; then
            local method="${BASH_REMATCH[2]}"
            local path="${BASH_REMATCH[3]}"

            # Extract handler name (next parameter or inline function)
            local handler="anonymous"
            if [[ "$line" =~ ,([[:space:]]*)([A-Za-z0-9_]+)[[:space:]]*\) ]]; then
                handler="${BASH_REMATCH[2]}"
            fi

            routes+=("{\"method\": \"${method^^}\", \"path\": \"$path\", \"handler\": \"$handler\", \"file\": \"${file#$REPO_ROOT/}\"}")
        fi
    done < "$file"

    echo "[$(IFS=,; echo "${routes[*]}")]"
}
```

#### 4.3.2 GraphQL Resolver Extraction

```bash
extract_graphql_resolvers() {
    local file="$1"
    local resolvers=()

    # Look for Query: { ... } or Mutation: { ... }
    local in_query=false
    local in_mutation=false
    local resolver_type=""

    while IFS= read -r line; do
        if [[ "$line" =~ ^[[:space:]]*Query:[[:space:]]*\{ ]]; then
            in_query=true
            resolver_type="Query"
        elif [[ "$line" =~ ^[[:space:]]*Mutation:[[:space:]]*\{ ]]; then
            in_mutation=true
            resolver_type="Mutation"
        elif [[ "$line" =~ ^[[:space:]]*\} ]]; then
            in_query=false
            in_mutation=false
        elif [[ "$in_query" == true ]] || [[ "$in_mutation" == true ]]; then
            # Extract resolver field
            if [[ "$line" =~ ^[[:space:]]*([A-Za-z0-9_]+):[[:space:]]* ]]; then
                local field_name="${BASH_REMATCH[1]}"
                resolvers+=("{\"type\": \"$resolver_type\", \"field\": \"$field_name\", \"file\": \"${file#$REPO_ROOT/}\"}")
            fi
        fi
    done < "$file"

    echo "[$(IFS=,; echo "${resolvers[*]}")]"
}
```

### 4.4 External API Detection

```bash
extract_third_party_services() {
    local package_json="$1"
    local services=()

    # Check for known SDKs in dependencies
    if jq -e '.dependencies.stripe' "$package_json" &>/dev/null; then
        services+=("Stripe")
    fi

    if jq -e '.dependencies."@aws-sdk/client-s3"' "$package_json" &>/dev/null; then
        services+=("AWS")
    fi

    if jq -e '.dependencies."@sendgrid/mail"' "$package_json" &>/dev/null; then
        services+=("SendGrid")
    fi

    echo "$services"
}

extract_stripe_usage() {
    # Find all Stripe API calls
    local stripe_calls=()

    while IFS= read -r file; do
        while IFS= read -r line_num; do
            local line=$(sed "${line_num}q;d" "$file")
            if [[ "$line" =~ stripe\.([A-Za-z0-9_]+)\.([A-Za-z0-9_]+) ]]; then
                local resource="${BASH_REMATCH[1]}"
                local method="${BASH_REMATCH[2]}"
                stripe_calls+=("{\"file\": \"${file#$REPO_ROOT/}\", \"line\": $line_num, \"method\": \"stripe.$resource.$method\"}")
            fi
        done < <(grep -n "stripe\." "$file" | cut -d: -f1)
    done < <(find "$REPO_ROOT" -name "*.ts" -o -name "*.js" | grep -v node_modules)

    echo "[$(IFS=,; echo "${stripe_calls[*]}")]"
}
```

---

## 5. Index Storage Format

### 5.1 Directory Structure

```
.analysis/index/
├── structure.json           # Code structure
├── data-models.json         # Database schemas, entities
├── api-endpoints.json       # REST, GraphQL endpoints
├── external-apis.json       # Third-party integrations
├── dependencies.json        # Import/export graph
├── metadata.json           # Statistics, freshness
└── cache/                  # Incremental update cache
    ├── file-hashes.json    # MD5 hashes for change detection
    └── last-run.json       # Last execution timestamp
```

### 5.2 Schema Definitions

#### 5.2.1 metadata.json

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "version": {"type": "string", "const": "1.0"},
    "generated_at": {"type": "string", "format": "date-time"},
    "freshness": {"type": "string", "format": "date-time"},
    "index_type": {"type": "string", "enum": ["full", "incremental"]},
    "duration_seconds": {"type": "number"},
    "statistics": {
      "type": "object",
      "properties": {
        "total_files": {"type": "integer"},
        "indexed_files": {"type": "integer"},
        "skipped_files": {"type": "integer"},
        "total_classes": {"type": "integer"},
        "total_functions": {"type": "integer"},
        "total_interfaces": {"type": "integer"}
      }
    },
    "languages": {
      "type": "object",
      "additionalProperties": {"type": "integer"}
    }
  },
  "required": ["version", "generated_at", "freshness", "statistics"]
}
```

#### 5.2.2 structure.json

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "version": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"},
    "classes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "file": {"type": "string"},
          "line": {"type": "integer"},
          "methods": {"type": "array", "items": {"type": "string"}},
          "extends": {"type": "string"},
          "implements": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["name", "file"]
      }
    },
    "functions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "file": {"type": "string"},
          "line": {"type": "integer"},
          "parameters": {"type": "array"},
          "return_type": {"type": "string"}
        },
        "required": ["name", "file"]
      }
    }
  }
}
```

#### 5.2.3 data-models.json

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "database_schemas": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "table": {"type": "string"},
          "file": {"type": "string"},
          "columns": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {"type": "string"},
                "type": {"type": "string"},
                "nullable": {"type": "boolean"},
                "unique": {"type": "boolean"},
                "primary_key": {"type": "boolean"},
                "default": {"type": ["string", "number", "null"]}
              },
              "required": ["name", "type"]
            }
          },
          "relationships": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {"type": "string", "enum": ["hasMany", "belongsTo", "hasOne", "manyToMany"]},
                "target": {"type": "string"},
                "foreign_key": {"type": "string"}
              }
            }
          }
        },
        "required": ["table", "columns"]
      }
    },
    "orm_entities": {"type": "array"},
    "type_definitions": {"type": "array"}
  }
}
```

---

## 6. Script Implementation

### 6.1 Main Index Builder

**File:** `scripts/bash/build-codebase-index.sh`

**Key Functions:**

```bash
main() {
    # 1. Parse arguments
    parse_arguments "$@"

    # 2. Check prerequisites
    check_prerequisites

    # 3. Determine index type (auto/full/incremental)
    determine_index_type

    # 4. Create output directory
    mkdir -p "$REPO_ROOT/.analysis/index"

    # 5. Build file list
    local file_list=$(build_file_list)

    # 6. Extract data
    extract_code_structure "$file_list"
    extract_data_models
    extract_api_endpoints
    extract_external_apis
    build_dependency_graph

    # 7. Generate metadata
    generate_metadata

    # 8. Output success JSON
    output_success_json
}
```

### 6.2 Load Index for Analysis

**File:** `scripts/bash/load-index-for-analysis.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INDEX_DIR="$REPO_ROOT/.analysis/index"

# Load all index files
STRUCTURE="$INDEX_DIR/structure.json"
DATA_MODELS="$INDEX_DIR/data-models.json"
API_ENDPOINTS="$INDEX_DIR/api-endpoints.json"
EXTERNAL_APIS="$INDEX_DIR/external-apis.json"

# Combine into comprehensive analysis object
jq -n \
  --slurpfile structure "$STRUCTURE" \
  --slurpfile data_models "$DATA_MODELS" \
  --slurpfile api_endpoints "$API_ENDPOINTS" \
  --slurpfile external_apis "$EXTERNAL_APIS" \
  '{
    code_structure: {
      total_classes: ($structure[0].classes | length),
      total_functions: ($structure[0].functions | length),
      entry_points: [$structure[0].functions[] | select(.name == "main" or .name == "start") | .file]
    },
    data_models: {
      total_entities: ($data_models[0].orm_entities | length),
      total_tables: ($data_models[0].database_schemas | length),
      entities: $data_models[0].orm_entities,
      schemas: $data_models[0].database_schemas
    },
    api_surface: {
      total_rest_endpoints: ($api_endpoints[0].rest_endpoints | length),
      total_graphql_resolvers: ($api_endpoints[0].graphql_resolvers | length),
      rest_endpoints: $api_endpoints[0].rest_endpoints,
      graphql_resolvers: $api_endpoints[0].graphql_resolvers
    },
    external_integrations: {
      total_services: ($external_apis[0].third_party_services | length),
      services: [$external_apis[0].third_party_services[].service],
      required_env_vars: $external_apis[0].environment_variables
    }
  }'
```

### 6.3 Find Reusable Code

**File:** `scripts/bash/find-reusable-code.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TASK_DESCRIPTION="$1"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INDEX_DIR="$REPO_ROOT/.analysis/index"

# Search for similar implementations
search_implementations() {
    local query="$1"
    local structure_file="$INDEX_DIR/structure.json"

    # Simple keyword matching (Phase 2: use embeddings for semantic search)
    jq --arg q "$query" '[
        .classes[] | select(.name | ascii_downcase | contains($q | ascii_downcase)) | {
            type: "class",
            name: .name,
            file: .file,
            line: .line,
            similarity: 0.85,
            recommendation: "Reuse this class instead of creating new one"
        },
        .functions[] | select(.name | ascii_downcase | contains($q | ascii_downcase)) | {
            type: "function",
            name: .name,
            file: .file,
            line: .line,
            similarity: 0.80,
            recommendation: "Reuse this function"
        }
    ]' "$structure_file"
}

# Search for utilities
search_utilities() {
    local query="$1"
    local structure_file="$INDEX_DIR/structure.json"

    jq --arg q "$query" '[
        .files[] |
        select(.path | contains("util") or contains("helper") or contains("lib")) |
        select(.functions | length > 0) |
        {
            file: .path,
            exports: [.functions[].name],
            relevance: 0.70,
            recommendation: "Use these utility functions"
        }
    ]' "$structure_file" 2>/dev/null || echo "[]"
}

# Search for patterns
search_patterns() {
    # Check data models for similar entities
    local data_models_file="$INDEX_DIR/data-models.json"

    jq --arg q "$1" '[
        .orm_entities[] |
        select(.entity | ascii_downcase | contains($q | ascii_downcase)) |
        {
            type: "entity",
            name: .entity,
            file: .file,
            table: .table,
            recommendation: "Reuse this entity - already defined"
        }
    ]' "$data_models_file" 2>/dev/null || echo "[]"
}

# Combine results
main() {
    local implementations=$(search_implementations "$TASK_DESCRIPTION")
    local utilities=$(search_utilities "$TASK_DESCRIPTION")
    local patterns=$(search_patterns "$TASK_DESCRIPTION")

    jq -n \
        --argjson impl "$implementations" \
        --argjson utils "$utilities" \
        --argjson patterns "$patterns" \
        '{
            existing_implementations: $impl,
            reusable_utilities: $utils,
            architecture_patterns: $patterns
        }'
}

main
```

---

## 7. AGENTS.md Integration

### 7.1 New Section for Indexing Features

**Add to:** `templates/AGENTS.md` (goes to release package)

```markdown
## Codebase Indexing Features

**New in v1.0.0**: Spec Kit now includes powerful codebase indexing capabilities that dramatically improve code analysis, reverse engineering, and implementation quality.

### Overview

The indexing system creates a searchable, structured representation of your codebase that enables:

- **10x faster reverse engineering** - Pre-extracted architecture instead of reading every file
- **40-60% code reuse** - Automatic detection of duplicate implementations
- **80% token reduction** - Grounded context instead of full file reads
- **Better accuracy** - AST-based understanding vs regex patterns

### New Commands

#### `/speckitsmart.index` - Build Codebase Index

**Purpose:** Create searchable index of code structure, data models, and APIs

**When to use:**
- **FIRST STEP**: Run before `/speckitsmart.analyze-project` (required prerequisite)
- After major code changes (new modules, refactoring)
- Weekly for active projects

**Basic usage:**
```bash
# First time - full index
/speckitsmart.index

# Update after changes - incremental (fast)
/speckitsmart.index --incremental

# Index specific directory
/speckitsmart.index --path src/

# Verbose output
/speckitsmart.index --verbose
```

**What gets indexed:**
- ✅ Code structure (classes, functions, interfaces)
- ✅ Data models (database schemas, ORM entities, TypeScript types)
- ✅ API endpoints (REST, GraphQL, WebSocket)
- ✅ External APIs (Stripe, AWS, third-party services)
- ✅ Dependencies (imports, exports, call graphs)

**Output location:** `.analysis/index/`

**Performance:** 30-60 seconds for typical projects

---

#### `/speckitsmart.wiki` - Generate Documentation

**Purpose:** Auto-generate comprehensive documentation (DeepWiki) from index

**Prerequisite:** Requires index (run `/speckitsmart.index` first)

**Basic usage:**
```bash
# Generate all documentation
/speckitsmart.wiki

# Generate specific tiers
/speckitsmart.wiki --tiers 1,2
```

**Output:** `.deepwiki/` directory containing:
- `overview.md` - What is this repo?
- `functional-summary.md` - Problems it solves
- `architecture/` - Architecture diagrams and details
- `modules/` - Per-module documentation
- `api-reference/` - API endpoint documentation

**Use cases:**
- Onboarding new team members
- Architecture documentation
- API documentation
- Understanding legacy code

---

#### `/speckitsmart.ask` - Query Codebase

**Purpose:** Ask questions about codebase using natural language

**Prerequisites:** Requires index, optionally DeepWiki for better answers

**Basic usage:**
```bash
# Ask about functionality
/speckitsmart.ask "How does authentication work?"

# Ask about data
/speckitsmart.ask "What database tables exist?"

# Ask about APIs
/speckitsmart.ask "Show me all user management endpoints"

# Ask about integrations
/speckitsmart.ask "What third-party services does this use?"
```

**Response includes:**
- Clear explanation with code examples
- File paths and line numbers
- Related information
- Source citations

**Benefits:**
- Get answers in seconds vs reading code for hours
- Grounded in actual codebase (no hallucinations)
- Links to source code for verification

---

### Updated Workflow

**Old workflow:**
```
1. /speckitsmart.analyze-project  ← Slow, read every file
2. /speckitsmart.specify
3. /speckitsmart.implement
```

**New workflow (recommended):**
```
1. /speckitsmart.index              ← NEW: Build index first (30-60s)
2. /speckitsmart.analyze-project    ← 10x faster with index
3. /speckitsmart.wiki               ← NEW: Generate docs (optional)
4. /speckitsmart.ask                ← NEW: Q&A during development (optional)
5. /speckitsmart.specify
6. /speckitsmart.implement          ← Enhanced with code reuse checks
```

### Prerequisite Requirements

#### Commands that REQUIRE index (will fail without):

- `/speckitsmart.analyze-project` - Reverse engineering needs index
- `/speckitsmart.wiki` - Documentation generation needs index
- `/speckitsmart.ask` - Q&A needs index to answer questions

**If index missing, you'll see:**
```
❌ ERROR: Codebase index not found

Run this command first:
  /speckitsmart.index

Then re-run this command.
```

#### Commands with OPTIONAL index (warns but continues):

- `/speckitsmart.implement` - Works without index, but with reduced benefits

**If index missing during implement:**
```
⚠️ Index not available

Proceeding without code reusability checks.
Missing: 40-60% code reuse, pattern detection, etc.

Run /speckitsmart.index to enable these features.
```

### Index Maintenance

**Freshness:**
- Fresh: <24 hours old
- Valid: <7 days old
- Stale: >7 days old (commands will warn)

**Update index:**
```bash
# Quick incremental update (5-10 seconds)
/speckitsmart.index --incremental

# Full rebuild (30-60 seconds)
/speckitsmart.index --full
```

**Automatic updates:**
- `/speckitsmart.analyze-project` checks freshness (warns if stale)
- `/speckitsmart.implement` can trigger incremental updates

### Best Practices

1. **Always index first** - Run `/speckitsmart.index` before analysis
2. **Keep index fresh** - Update weekly or after major changes
3. **Generate docs** - Run `/speckitsmart.wiki` for team onboarding
4. **Use ask command** - Query codebase instead of reading files
5. **Enable reusability** - Keep index updated during implementation

### Troubleshooting

**Q: How much disk space does index use?**
A: ~1-10MB for most projects (<1% of codebase size)

**Q: How long does indexing take?**
A: 30-60 seconds for typical projects, 2-5 minutes for large codebases

**Q: Does index work with all languages?**
A: Phase 1 supports TypeScript, JavaScript, Python, Java, C#, Go

**Q: Is index committed to git?**
A: No, `.analysis/index/` is gitignored. Each developer builds locally.

**Q: What if indexing fails?**
A: Run with `--verbose` to see details. Common issues:
   - Syntax errors in code (skip with `--skip-invalid`)
   - Large files (increase `--max-file-size`)
   - Permission issues (check `.analysis/` write access)

### Performance Expectations

| Codebase Size | Index Build | Incremental Update |
|---------------|-------------|-------------------|
| Small (<1K files) | 5-10s | 1-2s |
| Medium (1K-10K) | 30-60s | 3-5s |
| Large (10K-50K) | 2-5min | 10-20s |
| Very Large (>50K) | 10-30min | 30-60s |

### Security Notes

**What gets indexed:**
- ✅ Code structure and patterns
- ✅ API endpoint definitions
- ✅ Data model schemas
- ✅ Environment variable names (not values)

**What does NOT get indexed:**
- ❌ Secrets or API keys (redacted if found)
- ❌ Runtime values
- ❌ User data

**Recommendations:**
- Index is local-only (never uploaded)
- Automatically gitignored
- Safe to use with proprietary code
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

**Test coverage required:**
- Prerequisite check scripts (100%)
- Data extraction functions (90%)
- Index building logic (90%)
- Query functions (85%)

**Example test: Prerequisite check**

```bash
# tests/test-prerequisite-check.sh

test_index_exists() {
    # Setup: Create mock index
    mkdir -p .analysis/index
    cat > .analysis/index/metadata.json <<EOF
{
  "freshness": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "statistics": {"indexed_files": 100}
}
EOF

    # Execute
    result=$(./scripts/bash/check-index-prerequisite.sh)

    # Assert
    assert_equals "$(echo "$result" | jq -r '.index_exists')" "true"

    # Cleanup
    rm -rf .analysis/index
}

test_index_missing() {
    # Setup: No index
    rm -rf .analysis/index

    # Execute
    result=$(./scripts/bash/check-index-prerequisite.sh 2>&1)

    # Assert
    assert_equals "$(echo "$result" | jq -r '.index_exists')" "false"
    assert_contains "$result" "Index directory not found"
}
```

### 8.2 Integration Tests

**Scenarios:**

1. **Full workflow test:**
   - Run index → analyze-project → wiki → ask
   - Verify each stage succeeds
   - Verify output files exist

2. **Prerequisite enforcement:**
   - Try analyze-project without index → should fail
   - Try wiki without index → should fail
   - Try implement without index → should warn but continue

3. **Incremental update:**
   - Build full index
   - Modify one file
   - Run incremental update
   - Verify only modified file re-indexed

### 8.3 Cross-Platform Tests

**Test matrix:**

| OS | Shell | Test Coverage |
|----|-------|--------------|
| Ubuntu 22.04 | bash | Full |
| macOS 13+ | bash | Full |
| Windows 11 | PowerShell | Full |

**Automated testing:**
- GitHub Actions workflow for each OS
- Test all commands and scripts
- Verify output JSON format
- Check file creation

---

## 9. Performance Optimization

### 9.1 Indexing Performance

**Optimizations:**

1. **Parallel file processing** (Phase 2)
   - Use `xargs -P` for parallel execution
   - Process batches of files simultaneously
   - Target: 4x speedup on multi-core systems

2. **Incremental updates**
   - Track file MD5 hashes
   - Only re-index changed files
   - Target: <5 seconds for single file changes

3. **Smart parsing**
   - Skip binary files
   - Skip large files (>10MB)
   - Use regex for simple cases, tree-sitter for complex

### 9.2 Query Performance

**Optimizations:**

1. **Index structure**
   - Use flat JSON for fast loading
   - Pre-compute common queries
   - Cache frequently accessed data

2. **Search algorithms**
   - Phase 1: Simple keyword matching (O(n))
   - Phase 2: Vector embeddings for semantic search (O(log n))

---

## 10. Security Considerations

### 10.1 Secret Detection

**Problem:** Code may contain hardcoded secrets

**Solution:** Redact before indexing

```bash
redact_secrets() {
    local content="$1"

    # Redact common patterns
    content=$(echo "$content" | sed -E 's/(API_KEY|SECRET|PASSWORD)[[:space:]]*=[[:space:]]*['\''"]([^'\''"]+)['\''"]/\1=***REDACTED***/g')

    # Redact JWT tokens
    content=$(echo "$content" | sed -E 's/eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/***JWT_REDACTED***/g')

    echo "$content"
}
```

### 10.2 Access Control

**Requirements:**
- Index files readable only by owner
- `.analysis/` directory permissions: 700
- Warn if repository is public and contains secrets

### 10.3 Data Privacy

**Guarantees:**
- Index never uploaded to external services
- All processing happens locally
- No telemetry or analytics
- Respects `.gitignore` patterns

---

## Appendices

### A. File Checklist

**Command Templates:**
- [ ] `templates/commands/index.md`
- [ ] `templates/commands/wiki.md` (with prerequisite check)
- [ ] `templates/commands/ask.md` (with prerequisite check)
- [ ] Update `templates/commands/analyze-project.md` (add prerequisite check)
- [ ] Update `templates/commands/implement.md` (add optional check)

**Bash Scripts:**
- [ ] `scripts/bash/build-codebase-index.sh`
- [ ] `scripts/bash/check-index-prerequisite.sh`
- [ ] `scripts/bash/check-index-optional.sh`
- [ ] `scripts/bash/load-index-for-analysis.sh`
- [ ] `scripts/bash/find-reusable-code.sh`
- [ ] `scripts/bash/generate-deepwiki.sh`
- [ ] `scripts/bash/search-knowledge-base.sh`

**PowerShell Scripts:**
- [ ] `scripts/powershell/Build-CodebaseIndex.ps1`
- [ ] `scripts/powershell/Check-IndexPrerequisite.ps1`
- [ ] `scripts/powershell/Check-IndexOptional.ps1`
- [ ] `scripts/powershell/Load-IndexForAnalysis.ps1`
- [ ] `scripts/powershell/Find-ReusableCode.ps1`
- [ ] `scripts/powershell/Generate-DeepWiki.ps1`
- [ ] `scripts/powershell/Search-KnowledgeBase.ps1`

**Documentation:**
- [ ] `docs/codebase-indexing-functional-spec.md`
- [ ] `docs/codebase-indexing-technical-spec.md`
- [ ] Update `templates/AGENTS.md`

**Tests:**
- [ ] `tests/index/test-prerequisite-checks.sh`
- [ ] `tests/index/test-index-building.sh`
- [ ] `tests/index/test-data-extraction.sh`

---

**End of Technical Specification**
