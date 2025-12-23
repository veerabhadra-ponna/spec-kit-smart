---
stage: script_execution
requires: 01b-input-collection checkpoint
outputs: json_data_loaded
version: 3.1.0
next: 02a-category-scan.md
---

# Stage 1C: Script Execution & Data Loading

## Purpose

Execute the analyze-project script with collected inputs, then load and merge the generated JSON files into the analysis state.

---

## Pre-Check: Verify Previous Substage

1. Read `.analysis/.checkpoints/01b-inputs-complete.json`
2. Confirm `status` = "complete"
3. Load all input values into memory

**IF not complete:** STOP - Return to 01b-input-collection.md

---

## Step 1: Execute Analyze-Project Script

Run the cross-platform CLI command with collected inputs:

```bash
speckitadv analyze-project --path "$PROJECT_PATH" \
  --context "$ADDITIONAL_CONTEXT" \
  --scope "$ANALYSIS_SCOPE" \
  --concern-type "$CONCERN_TYPE" \
  --current-impl "$CURRENT_IMPL" \
  --target-impl "$TARGET_IMPL"
```

---
⏸️ **[STOP: SCRIPT_EXECUTION]**

Execute the script and capture output.

**Expected Script Output:**

```text
[analyze-project] Starting analysis...
[analyze-project] Project: {project_name}
[analyze-project] Creating workspace: .analysis/{project}-{timestamp}/
[analyze-project] Enumerating files...
[analyze-project] Detecting technology stack...
[analyze-project] Categorizing files...
[analyze-project] Generated: file-manifest.json
[analyze-project] Generated: tech-stack.json
[analyze-project] Generated: file-structure.json
[analyze-project] Generated: project-metadata.json
[analyze-project] Bootstrap state: .analysis/.state/analyze-project-00-bootstrap.json
[analyze-project] Chain ID: {8-char-hex}
[analyze-project] Complete!

```

**IF script fails:**

```text
❌ Error: Analysis script failed

Error details:
{script error output}

Possible causes:
  • Invalid project path
  • Missing dependencies (jq required for bash)
  • Permission issues

Please resolve the issue and retry.

```

STOP workflow until issue resolved.

---

### Parse Script Output

Extract from script output:
- `$CHAIN_ID` = 8-character hex identifier
- `$ANALYSIS_DIR` = Path to analysis workspace
- `$PROJECT_NAME` = Detected project name

---

## Step 2: Load Generated JSON Files

### Load Bootstrap State

```bash
cat .analysis/.state/analyze-project-00-bootstrap.json

```

Extract:
- `chain_id`
- `workspace_path`
- `created_at`

### Load Project Metadata

```bash
cat {$ANALYSIS_DIR}/project-metadata.json

```

Extract:
- `schema_version`
- `project_path`
- `project_name`
- `timestamp`
- `user_inputs`
- `workspace`

### Load Tech Stack

```bash
cat {$ANALYSIS_DIR}/tech-stack.json

```

Extract:
- `languages`
- `frameworks.backend`
- `frameworks.frontend`
- `build_tools`
- `indicators_found`

### Load File Structure

```bash
cat {$ANALYSIS_DIR}/file-structure.json

```

Extract:
- `total_files`
- `categories` (controllers, services, models, etc.)
- `entry_points`
- `analysis_priority`

---
⏸️ **[STOP: JSON_LOADING]**

Load all four JSON files and validate they are parseable.

**IF any JSON file missing or invalid:**

```text
❌ Error: Failed to load JSON files

Missing/Invalid files:
  {list of problematic files}

The script may have failed silently. Please check:
  1. {$ANALYSIS_DIR}/ directory exists
  2. All 4 JSON files were created
  3. JSON files are valid (try: jq . {file})

```

STOP workflow until resolved.

---

## Step 3: Display Summary to User

```text
═══════════════════════════════════════════════════════════
  ANALYSIS SETUP COMPLETE
═══════════════════════════════════════════════════════════

  Project: {project_name}
  Path: {project_path}
  Chain ID: {chain_id}

  ─────────────────────────────────────────────────────────
  TECHNOLOGY STACK DETECTED
  ─────────────────────────────────────────────────────────

  Languages: {comma-separated list}
  Backend Frameworks: {list or "None detected"}
  Frontend Frameworks: {list or "None detected"}
  Build Tools: {list}

  ─────────────────────────────────────────────────────────
  FILE ANALYSIS SUMMARY
  ─────────────────────────────────────────────────────────

  Total Files: {total_files}

  By Category:
    Controllers/Routes: {count}
    Services/Business Logic: {count}
    Models/Entities: {count}
    Repositories/DAOs: {count}
    Configurations: {count}
    Security/Auth: {count}
    Tests: {count}
    Other: {count}

  ─────────────────────────────────────────────────────────
  ANALYSIS CONFIGURATION
  ─────────────────────────────────────────────────────────

  Scope: {Full Application Modernization | Cross-Cutting Concern Migration}
  {IF scope=B: Concern: {concern_type}}
  {IF scope=B: Migration: {current_impl} → {target_impl}}
  {IF context: Additional Context: Provided}

  Workspace: {analysis_dir}

═══════════════════════════════════════════════════════════
  ✓ All data generated successfully
  ✓ Ready for Stage 2: Deep File Analysis
═══════════════════════════════════════════════════════════

```

---

## Step 4: Create Stage 1 State

### Generate State JSON

Create the complete Stage 1 state object:

```json
{
  "schema_version": "3.1.0",
  "chain_id": "{chain_id}",
  "stage": "setup_and_scope",
  "timestamp": "{ISO-8601}",
  "stages_complete": ["setup_and_scope"],
  "project_path": "{project_path}",
  "project_name": "{project_name}",
  "analysis_dir": "{analysis_dir}",
  "user_inputs": {
    "analysis_scope": "{A or B}",
    "additional_context": "{context or empty}",
    "concern_details": {
      "type": "{concern_type or null}",
      "current": "{current_impl or null}",
      "target": "{target_impl or null}"
    }
  },
  "tech_stack": {
    "languages": ["{list}"],
    "frameworks": {
      "backend": ["{list}"],
      "frontend": ["{list}"]
    },
    "build_tools": ["{list}"],
    "indicators_found": ["{list}"]
  },
  "file_structure": {
    "total_files": {count},
    "categories": {
      "controllers": {count},
      "services": {count},
      "models": {count},
      "repositories": {count},
      "configs": {count},
      "security": {count},
      "middleware": {count},
      "utils": {count},
      "tests": {count},
      "docs": {count}
    },
    "entry_points": ["{list}"],
    "analysis_priority": {
      "critical": ["configs", "security", "entry_points"],
      "high": ["controllers", "services", "models", "repositories"],
      "medium": ["middleware", "utils"],
      "low": ["tests", "docs"]
    }
  },
  "workspace_files": {
    "manifest_path": "{analysis_dir}/file-manifest.json",
    "tech_stack_path": "{analysis_dir}/tech-stack.json",
    "file_structure_path": "{analysis_dir}/file-structure.json",
    "metadata_path": "{analysis_dir}/project-metadata.json"
  }
}

```

### Save State

Write to: `.analysis/.state/analyze-project-01-setup-and-scope.json`

---

## Checkpoint: Script Execution Complete

### Create Checkpoint

Write checkpoint file: `.analysis/.checkpoints/01c-script-complete.json`

```json
{
  "substage": "01c-script-execution",
  "timestamp": "{ISO-8601}",
  "chain_id": "{chain_id}",
  "analysis_dir": "{analysis_dir}",
  "json_files_loaded": [
    "00-bootstrap.json",
    "project-metadata.json",
    "tech-stack.json",
    "file-structure.json"
  ],
  "state_saved": ".analysis/.state/analyze-project-01-setup-and-scope.json",
  "status": "complete"
}

```

### Verify Checkpoint

1. Read `.analysis/.checkpoints/01c-script-complete.json`
2. Validate JSON is parseable
3. Read `.analysis/.state/analyze-project-01-setup-and-scope.json`
4. Validate state file exists and is valid JSON

---
⏸️ **[STOP: CHECKPOINT_VERIFY]**

**IF both checkpoints verified:**
  Output: `✓ Checkpoint verified: 01c-script-execution`
  Output: `✓ State saved: 01-setup-and-scope.json`
**IF checkpoint failed:** Retry checkpoint creation once, then STOP if still failing

---

## Completion Marker

```text
═══════════════════════════════════════════════════════════
  STAGE COMPLETE: SETUP_AND_SCOPE

  Chain ID: {chain_id}
  State: .analysis/.state/analyze-project-01-setup-and-scope.json

  Proceeding to Stage 2: Deep File Analysis
═══════════════════════════════════════════════════════════

STAGE_COMPLETE:SETUP_AND_SCOPE

```

---

## Next Stage

Proceed immediately to: **02a-category-scan.md**
