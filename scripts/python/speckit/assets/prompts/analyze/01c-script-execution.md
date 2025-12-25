---
stage: script_execution
requires: 01b-input-collection
outputs: file_manifest_generated
version: 3.4.0
next: 02a-category-scan.md
---

# Stage 1C: Project Enumeration & Data Loading

## Purpose

Generate file manifest and detect technology stack for the project.

---

## State Management

The CLI provides all context via template variables. **Do not read state.json directly.**

**Available template variables:**

- `{project_path}` - Project path to analyze
- `{analysis_dir}` - Analysis folder path (root)
- `{data_dir}` - Data folder for JSON files (`{analysis_dir}/data/`)
- `{reports_dir}` - Reports folder for MD files (`{analysis_dir}/reports/`)
- `{scope}` - Analysis scope (A or B)
- `{context}` - Additional context
- `{concern_type}`, `{current_impl}`, `{target_impl}` - Scope B specific

**CLI Utility Commands (use instead of raw file writes):**

⚠️ **OS command line length limits apply (~8000 chars on Windows).** Break large content into smaller chunks.

```bash
# Write JSON to data/ folder
speckitadv write-data <filename> --stage=<stage-id> --content '<json>'

# Write MD to reports/ folder (put --append EARLY before --content)
speckitadv write-report <filename> --stage=<stage-id> --append --content '<small-md>'

# Get file statistics
speckitadv file-stats <filepath>
```

**For content > 2000 chars, use stdin mode:**

```powershell
@"
<json or markdown content here>
"@ | speckitadv write-data <filename> --stage=<stage-id> --stdin
```

---

## Step 1: Generate File Manifest

Run the enumerate-project CLI command to scan all files:

```bash
speckitadv enumerate-project "{project_path}" --output "{data_dir}/file-manifest.json"
```

This generates a JSON manifest with:

- All file paths (excluding common ignored patterns)
- File sizes and extensions
- File counts by type

---

⏸️ **[STOP: ENUMERATION]**

Execute the command and verify output.

**IF successful:** The manifest will be saved to `{data_dir}/file-manifest.json`
**IF fails:** Check path permissions and retry

---

## Step 2: Detect Technology Stack

Read the file manifest and analyze to detect:

### Languages

Look for file extensions:

- `.cs`, `.csproj` → C# / .NET
- `.java`, `.kt` → Java / Kotlin
- `.py` → Python
- `.js`, `.ts`, `.jsx`, `.tsx` → JavaScript / TypeScript
- `.go` → Go
- `.rb` → Ruby
- `.php` → PHP
- `.rs` → Rust

### Frameworks

Look for indicator files:

- `package.json` with dependencies → Node.js frameworks (Express, React, Vue, etc.)
- `*.csproj` with SDK → .NET (ASP.NET Core, Blazor, etc.)
- `pom.xml` or `build.gradle` → Java (Spring, etc.)
- `requirements.txt` or `pyproject.toml` → Python (Django, Flask, FastAPI, etc.)
- `Gemfile` → Ruby (Rails, Sinatra, etc.)
- `composer.json` → PHP (Laravel, Symfony, etc.)

### Build Tools

Look for:

- `package.json` → npm/yarn/pnpm
- `Makefile` → Make
- `*.csproj` → MSBuild/dotnet
- `pom.xml` → Maven
- `build.gradle` → Gradle
- `Dockerfile` → Docker
- `.github/workflows/` → GitHub Actions
- `azure-pipelines.yml` → Azure DevOps

---

## Step 3: Create Tech Stack File

Write detected stack using CLI command:

```bash
speckitadv write-data tech-stack.json --stage=01c-script-execution --content '<json>' --analysis-dir "{analysis_dir}"
```

This saves to `{data_dir}/tech-stack.json`:

```json
{
  "languages": ["C#", "TypeScript"],
  "frameworks": {
    "backend": ["ASP.NET Core 8"],
    "frontend": ["React"]
  },
  "build_tools": ["dotnet", "npm"],
  "indicators_found": [
    "*.csproj files",
    "package.json",
    "Dockerfile"
  ]
}
```

---

## Step 4: Display Summary

```text
═══════════════════════════════════════════════════════════
  PROJECT ENUMERATION COMPLETE
═══════════════════════════════════════════════════════════

  Project: {project_path}
  Analysis Folder: {analysis_dir}

  ─────────────────────────────────────────────────────────
  TECHNOLOGY STACK DETECTED
  ─────────────────────────────────────────────────────────

  Languages: {comma-separated list}
  Backend: {frameworks or "None detected"}
  Frontend: {frameworks or "None detected"}
  Build Tools: {list}

  ─────────────────────────────────────────────────────────
  FILES ENUMERATED
  ─────────────────────────────────────────────────────────

  Total Files: {count from manifest}

  ─────────────────────────────────────────────────────────
  ANALYSIS CONFIGURATION
  ─────────────────────────────────────────────────────────

  Scope: {scope} ({A=Full Application | B=Cross-Cutting})
  {IF scope=B: Concern: {concern_type}}
  {IF scope=B: Migration: {current_impl} → {target_impl}}

═══════════════════════════════════════════════════════════
  ✓ File manifest generated
  ✓ Tech stack detected
  ✓ Ready for Stage 2: Category Scan
═══════════════════════════════════════════════════════════
```

---

## Generated Files

After this stage, the analysis folder structure should be:

```text
{analysis_dir}/
├── state.json              # Created by CLI (tracks workflow progress)
├── data/
│   ├── file-manifest.json  # Generated by enumerate-project command
│   └── tech-stack.json     # Created by AI based on manifest analysis
└── reports/                # Empty (reports created in later stages)
```

---

## Next Stage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt (02a-category-scan).
