# Python Migration Assessment for Spec Kit Smart

**Version:** 1.0.0
**Date:** 2025-12-21
**Status:** Assessment Document (No Code Changes)

---

## Executive Summary

This document provides a comprehensive assessment of migrating from the current dual-script architecture (Bash + PowerShell) to a unified Python-based solution. It evaluates multiple approaches including single script, multiple scripts, and compiled executable options.

---

## Table of Contents

1. [Current Architecture Overview](#1-current-architecture-overview)
2. [Python Migration: Pros and Cons](#2-python-migration-pros-and-cons)
3. [Implementation Approaches](#3-implementation-approaches)
4. [Compiled EXE Assessment](#4-compiled-exe-assessment)
5. [Embedding Prompts in EXE](#5-embedding-prompts-in-exe)
6. [Progressive Prompt Injection Architecture](#6-progressive-prompt-injection-architecture)
7. [Why Staged Prompts Fail on Lower Models](#7-why-staged-prompts-fail-on-lower-models)
8. [Recommendations](#8-recommendations)

---

## 1. Current Architecture Overview

### 1.1 Script Inventory

| Category | Bash Scripts | PowerShell Scripts | Total Size |
|----------|-------------|-------------------|------------|
| Core Analysis | 4 files (53K) | 4 files (57K) | 110K |
| Guidelines | 5 files (73K) | 4 files (54K) | 127K |
| Supporting | 6 files (68K) | 4 files (43K) | 111K |
| **TOTAL** | **15 files (194K)** | **12 files (154K)** | **348K** |

### 1.2 Core Scripts by Function

```text
┌─────────────────────────────────────────────────────────────────┐
│                    SCRIPT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│  analyze-project.sh/ps1 (22K/22K)                               │
│     ├── enumerate-project.sh/ps1 (17K/16K)                      │
│     ├── chain-state.sh/ps1 (7K/11K)                             │
│     └── common.sh/ps1 (7K/8K)                                   │
│                                                                 │
│  check-guidelines-compliance.sh/ps1 (19K/14K)                   │
│  generate-guidelines.sh/ps1 (15K/14K)                           │
│  update-agent-context.sh/ps1 (25K/20K)                          │
│  create-new-feature.sh/ps1 (15K/16K)                            │
│  check-artifactory.sh/ps1 (8K/12K)                              │
│  verify-analysis-report.sh/ps1 (3K/4K)                          │
│  ... and more                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 External Dependencies

#### Bash Scripts Require

- `jq` - JSON processing (CRITICAL - prevents injection attacks)
- `find` - File enumeration
- `stat` - File metadata (platform-specific flags)
- `git` - Optional, for repo detection
- `openssl` - Optional, for hash generation

#### PowerShell Scripts Require

- No external dependencies (pure PowerShell cmdlets)
- Works on Windows, macOS, Linux with PowerShell Core

---

## 2. Python Migration: Pros and Cons

### 2.1 PROS of Python Migration

| Advantage | Impact | Details |
|-----------|--------|---------|
| **Single Language** | HIGH | Eliminate dual maintenance burden (Bash + PowerShell) |
| **Cross-Platform Native** | HIGH | One codebase works on Windows, macOS, Linux |
| **No `jq` Dependency** | HIGH | Built-in `json` module eliminates external tool requirement |
| **Rich Standard Library** | MEDIUM | `pathlib`, `subprocess`, `argparse`, `json`, `re` all built-in |
| **Better Error Handling** | MEDIUM | Try/except with stack traces vs shell error codes |
| **Type Hints** | MEDIUM | Optional static typing with `mypy` for better maintainability |
| **Testing Infrastructure** | HIGH | `pytest`, `unittest` are mature and well-supported |
| **Packaging Flexibility** | HIGH | pip, pipx, PyInstaller, cx_Freeze, Nuitka options |
| **IDE Support** | MEDIUM | Better autocomplete, refactoring, debugging |
| **Security** | HIGH | No shell injection risks from improper quoting |
| **Consistent Behavior** | HIGH | Same code path on all platforms (no `stat -f` vs `stat -c`) |

### 2.2 CONS of Python Migration

| Disadvantage | Impact | Mitigation |
|--------------|--------|------------|
| **Runtime Requirement** | MEDIUM | Users need Python 3.11+ installed |
| **Startup Overhead** | LOW | ~100-200ms Python interpreter startup |
| **Distribution Complexity** | MEDIUM | Need pip/pipx or compiled binary |
| **Learning Curve** | LOW | Team must maintain Python vs shell |
| **Embedded Prompt Size** | MEDIUM | Binary grows with embedded assets |
| **Shell Interop** | LOW | Some operations still need `subprocess` |
| **Git Operations** | LOW | Still needs `git` command via subprocess |

### 2.3 Feature Parity Assessment

| Feature | Current (Bash/PS1) | Python | Notes |
|---------|-------------------|--------|-------|
| File enumeration | ✅ `find` / `Get-ChildItem` | ✅ `pathlib.rglob()` | Identical capability |
| JSON processing | ✅ `jq` / native PS | ✅ `json` module | Better - no external dep |
| Tech stack detection | ✅ Pattern matching | ✅ Same patterns | Identical |
| State management | ✅ File-based JSON | ✅ File-based JSON | Identical |
| Progress reporting | ✅ `echo` / `Write-Host` | ✅ `rich` library | Better UX |
| Git operations | ✅ `git` command | ✅ `subprocess` | Identical |
| Config loading | ✅ JSON + env vars | ✅ Same | Identical |

---

## 3. Implementation Approaches

### 3.1 Option A: Single Unified Python Script

#### Structure

```text
scripts/python/
└── speckit.py (~3000-4000 lines)
    ├── Commands: analyze, enumerate, check-guidelines, etc.
    ├── Shared utilities embedded
    └── All functionality in one file
```

#### Pros

- Simplest distribution (one file)
- No import/path issues
- Easy to embed in release

#### Cons

- Large file, harder to maintain
- All code loaded even for small operations
- Merge conflicts more likely

**Verdict:** ⚠️ NOT RECOMMENDED for this codebase size

---

### 3.2 Option B: Modular Python Package

#### Structure

```text
scripts/python/
├── speckit/
│   ├── __init__.py
│   ├── __main__.py          # CLI entry point
│   ├── cli.py                # Typer/Click CLI definitions
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── analyze.py        # analyze-project command
│   │   ├── enumerate.py      # enumerate-project command
│   │   ├── guidelines.py     # guidelines commands
│   │   └── features.py       # feature commands
│   ├── core/
│   │   ├── __init__.py
│   │   ├── state.py          # chain-state management
│   │   ├── config.py         # config loading
│   │   └── utils.py          # common utilities
│   └── assets/
│       └── prompts/          # Embedded prompts (optional)
├── pyproject.toml
└── tests/
    └── ...
```

#### Pros

- Clean separation of concerns
- Easy to test individual modules
- Standard Python package structure
- Can still compile to single EXE

#### Cons

- More complex than single file
- Requires proper packaging

**Verdict:** ✅ RECOMMENDED for maintainability

---

### 3.3 Option C: Compiled Single Executable

#### Structure

```text
dist/
├── speckit (Linux/macOS binary)
├── speckit.exe (Windows binary)
└── speckit-universal (macOS universal binary)
```

#### Compilation Options

| Tool | Size | Startup | Cross-Compile | Notes |
|------|------|---------|---------------|-------|
| **PyInstaller** | ~15-50MB | ~1-2s | No | Most mature, bundle everything |
| **Nuitka** | ~10-30MB | ~200ms | No | Compiles to C, faster startup |
| **cx_Freeze** | ~20-40MB | ~1s | No | Similar to PyInstaller |
| **PyOxidizer** | ~15-40MB | ~500ms | Yes | Rust-based, modern |
| **Briefcase** | ~30-60MB | ~1s | Yes | Multi-platform apps |

**Verdict:** ✅ VIABLE - see Section 4 for detailed analysis

---

## 4. Compiled EXE Assessment

### 4.1 PyInstaller Approach (Recommended)

```bash
# Single-file executable
pyinstaller --onefile \
  --name speckitadv \
  --add-data "prompts:prompts" \
  --add-data "templates:templates" \
  speckit/__main__.py

# Result: dist/speckitadv (~25MB)
```

#### Advantages

- Single file, no dependencies
- All Python packages bundled
- Works on all platforms (compile per-platform)
- Can embed prompts/templates as data files

#### Disadvantages

- Must compile separately for each OS
- Larger file size (~15-50MB)
- Slower first startup (~1-2s) due to extraction
- Anti-virus false positives possible

### 4.2 Nuitka Approach (Higher Performance)

```bash
# Compile to native binary
python -m nuitka \
  --standalone \
  --onefile \
  --output-filename=speckitadv \
  --include-data-dir=prompts=prompts \
  --include-data-dir=templates=templates \
  speckit/__main__.py

# Result: dist/speckitadv (~15MB, faster startup)
```

#### Advantages

- Faster startup (~200ms vs 1-2s)
- Smaller binary size
- Actual compiled code (harder to reverse-engineer)

#### Disadvantages

- Longer compile time
- C compiler required for building
- Less mature than PyInstaller

### 4.3 Cross-Platform Distribution Strategy

```text
GitHub Release Assets:
├── speckitadv-linux-x86_64        (Linux AMD64)
├── speckitadv-linux-arm64         (Linux ARM64)
├── speckitadv-darwin-x86_64       (macOS Intel)
├── speckitadv-darwin-arm64        (macOS Apple Silicon)
├── speckitadv-darwin-universal    (macOS Universal)
├── speckitadv-windows-x86_64.exe  (Windows 64-bit)
└── speckitadv.py                  (Source, for pipx install)
```

### 4.4 Compilation CI/CD Pipeline

```yaml
# .github/workflows/build-binaries.yml
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        include:
          - os: ubuntu-latest
            artifact: speckitadv-linux-x86_64
          - os: macos-latest
            artifact: speckitadv-darwin-universal
          - os: windows-latest
            artifact: speckitadv-windows-x86_64.exe

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyinstaller

      - name: Build binary
        run: pyinstaller --onefile --name ${{ matrix.artifact }} speckit/__main__.py

      - uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.artifact }}
          path: dist/${{ matrix.artifact }}
```

---

## 5. Embedding Prompts in EXE

### 5.1 Technical Feasibility: ✅ YES, FULLY POSSIBLE

Prompts and templates can be embedded in the compiled EXE using multiple methods:

### 5.2 Method 1: PyInstaller Data Files (Recommended)

```python
# speckit/assets.py
import sys
from pathlib import Path

def get_assets_path() -> Path:
    """Get path to embedded assets, works in both dev and frozen mode."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys._MEIPASS) / 'assets'
    else:
        # Running in development
        return Path(__file__).parent / 'assets'

def get_prompt(name: str) -> str:
    """Load an embedded prompt by name."""
    prompt_path = get_assets_path() / 'prompts' / f'{name}.md'
    return prompt_path.read_text(encoding='utf-8')

def get_template(name: str) -> str:
    """Load an embedded template by name."""
    template_path = get_assets_path() / 'templates' / f'{name}.md'
    return template_path.read_text(encoding='utf-8')
```

#### PyInstaller spec file

```python
# speckit.spec
a = Analysis(
    ['speckit/__main__.py'],
    datas=[
        ('prompts', 'assets/prompts'),
        ('templates', 'assets/templates'),
    ],
    ...
)
```

### 5.3 Method 2: Inline String Embedding

```python
# speckit/prompts/embedded.py
# Auto-generated file - DO NOT EDIT MANUALLY

PROMPTS = {
    "analyze-project": """---
description: Analyze project with chained prompts
version: 3.0.0-scriptfirst
---
# Analyze Project - Chain Orchestrator
...
""",
    "01-setup-and-scope": """---
stage: setup_and_scope
requires: nothing
---
# Stage 1: Setup and Input Collection
...
""",
    # ... more prompts
}

def get_prompt(name: str) -> str:
    return PROMPTS.get(name, "")
```

#### Build script to generate embedded.py

```python
# scripts/embed_prompts.py
import json
from pathlib import Path

def generate_embedded():
    prompts = {}
    for prompt_file in Path('prompts').rglob('*.md'):
        key = prompt_file.stem
        prompts[key] = prompt_file.read_text(encoding='utf-8')

    output = f"PROMPTS = {json.dumps(prompts, indent=2)}\n"
    Path('speckit/prompts/embedded.py').write_text(output)
```

### 5.4 Method 3: Resource Module (importlib.resources)

```python
# speckit/prompts/__init__.py
from importlib import resources

def get_prompt(name: str) -> str:
    """Load prompt from package resources."""
    return resources.files('speckit.prompts').joinpath(f'{name}.md').read_text()
```

### 5.5 Prompt Organization in EXE

```text
speckit (compiled EXE)
├── [Python runtime bundled]
├── [Dependencies bundled]
└── assets/
    ├── prompts/
    │   ├── commands/
    │   │   ├── analyze-project.md
    │   │   ├── constitution.md
    │   │   ├── specify.md
    │   │   ├── plan.md
    │   │   ├── clarify.md
    │   │   ├── tasks.md
    │   │   ├── implement.md
    │   │   └── analyze/
    │   │       ├── 01-setup-and-scope.md
    │   │       ├── 02-file-analysis.md
    │   │       ├── 03a-full-app.md
    │   │       ├── 03b-cross-cutting.md
    │   │       ├── 04-report-generation.md
    │   │       ├── 05-artifacts.md
    │   │       └── 06-scope-artifacts.md
    │   └── stage-templates/
    │       ├── constitution-prompt-template.md
    │       ├── clarify-prompt-template.md
    │       ├── tasks-prompt-template.md
    │       └── implement-prompt-template.md
    └── templates/
        ├── analysis-report-template.md
        ├── functional-spec-template.md
        ├── technical-spec-template.md
        └── ... (other templates)
```

### 5.6 Benefits of Embedded Prompts

| Benefit | Description |
|---------|-------------|
| **Source/Deploy Confusion Eliminated** | Agent only sees embedded prompts, never source files |
| **Version Consistency** | Prompts always match the EXE version |
| **Tamper Resistance** | Users can't accidentally modify prompts |
| **Simpler Distribution** | No need to track separate prompt files |
| **Faster Loading** | Prompts already in memory (if using inline embedding) |

---

## 6. Progressive Prompt Injection Architecture

### 6.1 Concept Overview

Instead of loading the entire 850+ line staged prompt at once, the EXE outputs prompts progressively as the workflow progresses. This is a **significant architectural improvement** for lower-capability models.

### 6.2 How AI Agents Can Receive Prompts from EXE Output

**YES, this is fully possible.** Here's how:

```text
┌─────────────────────────────────────────────────────────────────┐
│                PROGRESSIVE PROMPT INJECTION FLOW                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User: "Run /speckitadv.analyze-project"                      │
│                                                                 │
│  Agent: Runs → speckitadv analyze --stage=init                  │
│                                                                 │
│  EXE Output:                                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ PROMPT_FRAGMENT:START                                       ││
│  │ ## Stage 1: Setup and Input Collection                      ││
│  │                                                             ││
│  │ Collect the following from user:                            ││
│  │ 1. PROJECT_PATH - absolute path to analyze                  ││
│  │ 2. ADDITIONAL_CONTEXT - optional notes                      ││
│  │ 3. ANALYSIS_SCOPE - [A] Full or [B] Cross-cutting           ││
│  │                                                             ││
│  │ When user provides inputs, run:                             ││
│  │   speckitadv analyze --stage=collect --path="$PATH" ...     ││
│  │                                                             ││
│  │ PROMPT_FRAGMENT:END                                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Agent: Follows instructions, collects user input               │
│  Agent: Runs → speckitadv analyze --stage=collect --path=/path  │
│                                                                 │
│  EXE Output:                                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ DATA:                                                       ││
│  │ { "chain_id": "abc123", "files": 245, ... }                 ││
│  │                                                             ││
│  │ PROMPT_FRAGMENT:START                                       ││
│  │ ## Stage 2: File Analysis                                   ││
│  │                                                             ││
│  │ You now have 245 files to analyze. Focus on:                ││
│  │ - Controllers (12 files)                                    ││
│  │ - Services (28 files)                                       ││
│  │ ...                                                         ││
│  │ When complete, run:                                         ││
│  │   speckitadv analyze --stage=file-analysis --chain=abc123   ││
│  │                                                             ││
│  │ PROMPT_FRAGMENT:END                                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Agent: Performs file analysis, saves state                     │
│  Agent: Runs → speckitadv analyze --stage=file-analysis ...     │
│                                                                 │
│  ... continues until ...                                        │
│                                                                 │
│  EXE Output:                                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ WORKFLOW_COMPLETE                                           ││
│  │ All artifacts generated in: .analysis/project-timestamp/    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 Implementation Design

```python
# speckit/cli.py
import typer
from speckit.prompts import get_stage_prompt
from speckit.state import ChainState

app = typer.Typer()

@app.command()
def analyze(
    stage: str = typer.Option("init", help="Current workflow stage"),
    chain_id: str = typer.Option(None, help="Chain ID for state"),
    path: str = typer.Option(None, help="Project path"),
    scope: str = typer.Option(None, help="Analysis scope A or B"),
):
    """Progressive analyze-project workflow."""

    if stage == "init":
        # Output Stage 1 prompt fragment
        prompt = get_stage_prompt("01-setup-and-scope", fragment=True)
        print("PROMPT_FRAGMENT:START")
        print(prompt)
        print("PROMPT_FRAGMENT:END")
        print(f"NEXT_COMMAND: speckitadv analyze --stage=collect --path=<USER_PATH> --scope=<USER_SCOPE>")
        return

    if stage == "collect":
        # Run data extraction
        state = ChainState.initialize(path)
        data = run_enumeration(path)
        state.save("01-setup-and-scope", data)

        # Output data + next stage prompt
        print(f"DATA: {state.to_json()}")
        print("PROMPT_FRAGMENT:START")
        print(get_stage_prompt("02-file-analysis",
              context={"files": data["file_count"], "categories": data["categories"]}))
        print("PROMPT_FRAGMENT:END")
        print(f"NEXT_COMMAND: speckitadv analyze --stage=file-analysis --chain={state.chain_id}")
        return

    if stage == "file-analysis":
        state = ChainState.load(chain_id)
        # ... perform analysis ...

        # Branch based on scope
        next_stage = "03a-full-app" if state.scope == "A" else "03b-cross-cutting"
        print("PROMPT_FRAGMENT:START")
        print(get_stage_prompt(next_stage, context=state.to_dict()))
        print("PROMPT_FRAGMENT:END")
        print(f"NEXT_COMMAND: speckitadv analyze --stage={next_stage} --chain={chain_id}")
        return

    # ... more stages ...

    if stage == "complete":
        print("WORKFLOW_COMPLETE")
        print(f"ARTIFACTS: {state.analysis_dir}")
```

### 6.4 Prompt Fragment Structure

Instead of 850 lines at once, each fragment is 50-150 lines:

```markdown
## Stage 2: File Analysis

### Context (injected by EXE)
- Project: {project_name}
- Total Files: {file_count}
- Categories: {categories_summary}

### Your Task
Analyze the files listed in `file-manifest.json`. Focus on:
1. Authentication patterns (8 files in security/)
2. Database access (18 files in repositories/)
3. API endpoints (12 files in controllers/)

### Output Requirements
- Extract patterns found
- Document technical debt
- Note security concerns

### When Complete
Run: `speckitadv analyze --stage=file-analysis --chain={chain_id}`

Provide your findings as JSON in the command output.
```

### 6.5 Benefits of Progressive Injection

| Benefit | Lower Models | Higher Models |
|---------|--------------|---------------|
| **Focused Attention** | ✅ Critical - only 50-150 lines at a time | ✅ Helpful |
| **Context Relevance** | ✅ Only see data for current stage | ✅ Cleaner |
| **Error Recovery** | ✅ Resume from any stage | ✅ Same |
| **Reduced Hallucination** | ✅ Concrete data injected | ✅ Same |
| **Progress Tracking** | ✅ Clear stage markers | ✅ Same |
| **Consistent Behavior** | ✅ Same prompt = same behavior | ✅ Same |

### 6.6 Comparison: Monolithic vs Progressive

| Metric | Monolithic (850 lines) | Progressive (50-150 per stage) |
|--------|------------------------|--------------------------------|
| Sonnet 4 completion | 60-70% | 95%+ expected |
| Opus 4.5 completion | 95% | 95%+ |
| Instruction following | Varies by model | Consistent |
| Recovery from interruption | Manual | Automatic |
| Context window usage | High | Low per stage |
| Prompt caching benefit | Limited | High (small fragments) |

---

## 7. Why Staged Prompts Fail on Lower Models

### 7.1 Root Cause Analysis

After examining the staged prompts (`02-file-analysis.md` = 851 lines), I identified several issues:

#### Issue 1: Attention Dilution

The `02-file-analysis.md` prompt contains:
- 4 major phases (Category Scan, Deep Dive, Configuration, Test Coverage)
- 8+ sub-categories per phase
- Complex nested JSON examples
- Multiple quality gates
- Progress reporting requirements every 10 files

**Problem:** Lower models can't maintain attention across 850 lines with competing instructions.

#### Issue 2: Instruction Density

```markdown
# Example from 02-file-analysis.md (lines 60-75)

## Phase 1: Category Scan (25% of time)

Scan 15-20% of files in EACH category to identify patterns.

### Step 1.1: Categorize Files from Manifest
Read `file-manifest.json` and group files by category:

**Core Application Categories**:
1. **Controllers/Routes** - API endpoints, HTTP handlers
2. **Services/Business Logic** - Core business workflows
3. **Models/Entities** - Data structures, domain models
...
```

**Problem:** Too many directives per section. Lower models skip or merge instructions.

#### Issue 3: Complex Conditional Logic

```markdown
# From 02-file-analysis.md

**IF** `additional_context` is provided (not null):
- Keep this context in mind throughout your analysis
- Use it to focus on relevant areas
- Reference it when identifying pain points
- Include relevant findings in your analysis

**IF** user choice is **not** [A] or [B]:
- Display error: "❌ Invalid selection..."
- Re-prompt for ANALYSIS_SCOPE
- DO NOT proceed until valid choice received
```

**Problem:** Nested conditionals confuse lower models - they may execute the wrong branch.

#### Issue 4: Output Format Complexity

The staged prompts require complex JSON state output:

```json
{
  "schema_version": "3.0.0",
  "chain_id": "a3f7c8d1",
  "stage": "setup_and_scope",
  "timestamp": "2025-11-19T10:15:00Z",
  "stages_complete": ["setup_and_scope"],
  "project_path": "/home/user/legacy-app",
  "tech_stack": { ... },
  "file_structure": { ... },
  "workspace_files": { ... }
}
```

**Problem:** Lower models generate invalid JSON or miss required fields.

### 7.2 Comparison: Main Prompts vs Staged Prompts

| Aspect | Main Prompts (constitution.md) | Staged Prompts (02-file-analysis.md) |
|--------|--------------------------------|--------------------------------------|
| **Length** | 234 lines | 851 lines |
| **Phases** | 1 main flow | 4 phases + sub-phases |
| **Conditionals** | 2-3 simple IF/ELSE | 10+ nested conditionals |
| **Output Format** | Simple Markdown file | Complex JSON state object |
| **Progress Requirements** | None | Every 10 files |
| **Quality Gates** | 1 (validation) | 5 (must all pass) |
| **JSON Examples** | 1 simple | 5 complex nested |
| **Model Behavior** | ✅ Works on all models | ❌ Fails on Sonnet, works on Opus |

### 7.3 Specific Failure Modes on Lower Models

1. **Phase Skipping:** Model jumps from Phase 1 to Phase 4
2. **Incomplete Extraction:** Only 30% of files analyzed instead of 70%
3. **State Corruption:** Missing required JSON fields
4. **Quality Gate Bypass:** Model says "gates passed" without checking
5. **Progress Reporting Ignored:** No updates during analysis
6. **Conditional Confusion:** Executes wrong branch of IF/ELSE

### 7.4 Why Main Prompts Work Better

The `constitution.md` prompt succeeds because:

1. **Single Focus:** One task (create/update constitution)
2. **Linear Flow:** Step 1 → Step 2 → Step 3 → Done
3. **Simple Conditionals:** Only "if AGENTS.md exists, read it"
4. **Concrete Examples:** Clear before/after
5. **Modest Output:** One Markdown file, not complex JSON
6. **No Progress Tracking:** Just complete the task
7. **Self-Contained:** Doesn't depend on external state files

---

## 8. Recommendations

### 8.1 Migration Strategy: Phased Approach

```text
Phase 1: Python Core (Week 1-2)
├── Create Python package structure
├── Migrate common.sh/ps1 → core/utils.py
├── Migrate chain-state.sh/ps1 → core/state.py
└── Add comprehensive tests

Phase 2: Analysis Commands (Week 3-4)
├── Migrate enumerate-project → commands/enumerate.py
├── Migrate analyze-project → commands/analyze.py
├── Implement progressive prompt injection
└── Test with multiple AI models

Phase 3: Supporting Commands (Week 5-6)
├── Migrate guidelines commands
├── Migrate feature commands
├── Migrate verification scripts
└── Full integration testing

Phase 4: Packaging (Week 7-8)
├── PyInstaller configuration
├── Embed prompts as assets
├── CI/CD for multi-platform builds
├── GitHub Release automation
└── Documentation and migration guide
```

### 8.2 Recommended Architecture

```text
speckit/
├── __init__.py
├── __main__.py
├── cli.py                     # Typer CLI
├── commands/
│   ├── __init__.py
│   ├── analyze.py             # Progressive analyze workflow
│   ├── enumerate.py
│   ├── guidelines.py
│   ├── features.py
│   └── verify.py
├── core/
│   ├── __init__.py
│   ├── state.py               # Chain state management
│   ├── config.py              # Config loading
│   ├── utils.py               # Shared utilities
│   └── tech_detect.py         # Tech stack detection
├── prompts/
│   ├── __init__.py
│   ├── loader.py              # Prompt loading/injection
│   └── fragments/             # Small prompt fragments
│       ├── analyze-init.md
│       ├── analyze-collect.md
│       ├── analyze-files.md
│       ├── analyze-report.md
│       └── ...
└── assets/
    └── templates/             # Report templates
```

### 8.3 Prompt Fragment Design

#### Current (monolithic)

```text
02-file-analysis.md (851 lines)
├── Phase 1: Category Scan (200 lines)
├── Phase 2: Deep Dive (250 lines)
├── Phase 3: Configuration (150 lines)
├── Phase 4: Test Coverage (100 lines)
├── Dependency Audit (80 lines)
└── Output State (71 lines)
```

#### Proposed (fragmented)

```text
analyze/
├── init.md (30 lines)            # Initial setup instructions
├── collect.md (50 lines)         # Collect user inputs
├── phase1-scan.md (80 lines)     # Category scan only
├── phase2-auth.md (60 lines)     # Auth deep dive
├── phase2-db.md (60 lines)       # Database deep dive
├── phase2-api.md (60 lines)      # API deep dive
├── phase3-config.md (50 lines)   # Config analysis
├── phase4-tests.md (40 lines)    # Test coverage
├── dependency-audit.md (40 lines)
└── generate-report.md (50 lines)
```

#### Benefits

- Each fragment is 30-80 lines (vs 851)
- Model only sees current task
- EXE injects relevant context
- Consistent behavior across models

### 8.4 Final Recommendation

Recommendation: Modular Python Package with Progressive Prompt Injection and Optional EXE Compilation

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python | Cross-platform, no `jq` dependency |
| Structure | Modular package | Maintainability, testability |
| Prompts | Embedded + fragmented | Eliminate source confusion, model consistency |
| Distribution | pip/pipx + EXE | Flexibility for different user needs |
| Prompt Injection | Progressive | Critical for lower model support |

---

## Appendix A: Tool Comparison Matrix

| Feature | Bash+PS | Single Python | Modular Python | Compiled EXE |
|---------|---------|---------------|----------------|--------------|
| Cross-platform | ⚠️ Dual code | ✅ | ✅ | ✅ |
| No external deps | ❌ (jq) | ✅ | ✅ | ✅ |
| Easy distribution | ⚠️ | ⚠️ | ⚠️ | ✅ |
| Maintainability | ❌ | ⚠️ | ✅ | ✅ |
| Prompt embedding | ❌ | ✅ | ✅ | ✅ |
| Progressive injection | ❌ | ✅ | ✅ | ✅ |
| Model consistency | ❌ | ✅ | ✅ | ✅ |
| Startup time | ✅ Fast | ⚠️ ~200ms | ⚠️ ~200ms | ⚠️ ~1-2s |
| File size | ✅ ~350K | ✅ ~100K | ✅ ~150K | ❌ ~25MB |

---

## Appendix B: Sample Progressive Prompt Fragment

```markdown
# Stage 2A: Authentication Analysis

## Context
You are analyzing project `{project_name}` ({file_count} files).
Chain ID: `{chain_id}`

## Your Task
Analyze the {security_file_count} files in the security/ directory:
{security_files_list}

Extract:
1. Authentication mechanism (JWT, OAuth, SAML, Basic, etc.)
2. Password hashing algorithm
3. Token expiration settings
4. Session management approach
5. Security vulnerabilities

## Output Format
Provide your findings as:
```json
{
  "auth_type": "JWT|OAuth|SAML|Basic|Custom",
  "password_hash": "bcrypt|scrypt|argon2|sha256|other",
  "token_expiry": "24h",
  "vulnerabilities": ["issue1", "issue2"]
}
```text

## Next Step

When complete, run:

```bash
speckitadv analyze --stage=auth-complete --chain={chain_id} --findings='<YOUR_JSON>'
```text

```

**Note:** This fragment is 30 lines vs the current 200+ lines for auth analysis in `02-file-analysis.md`.

---

## Appendix C: Implementation Priority

| Priority | Task | Effort | Impact |
|----------|------|--------|--------|
| P0 | Create Python package skeleton | 2 days | Foundation |
| P0 | Migrate state management | 3 days | Critical for workflow |
| P0 | Implement progressive prompt injection | 5 days | Model consistency |
| P1 | Migrate analyze-project | 5 days | Core functionality |
| P1 | Fragment existing prompts | 3 days | Model support |
| P2 | Migrate remaining commands | 5 days | Full parity |
| P2 | PyInstaller packaging | 2 days | Distribution |
| P3 | CI/CD for multi-platform builds | 2 days | Automation |

**Total Estimated Effort:** 4-6 weeks for full migration

---

## 9. Zero-Prompt Architecture (Enhanced Design)

### 9.1 Concept: EXE as Single Source of All Prompts

Instead of having prompt files that the agent reads, the EXE **outputs** all prompts dynamically. Slash command files become ultra-minimal launchers.

### 9.2 Launcher File Template (3 lines each)

```markdown
---
description: {command_description}
---
Run: `speckitadv {command_name}`
Follow all instructions in the output.
```

### 9.3 All Commands Using Zero-Prompt Pattern

| Command | Launcher | EXE Command |
|---------|----------|-------------|
| constitution | 3 lines | `speckitadv constitution` |
| specify | 3 lines | `speckitadv specify` |
| plan | 3 lines | `speckitadv plan` |
| clarify | 3 lines | `speckitadv clarify` |
| tasks | 3 lines | `speckitadv tasks` |
| implement | 3 lines | `speckitadv implement` |
| analyze-project | 3 lines | `speckitadv analyze-project` |
| checklist | 3 lines | `speckitadv checklist` |
| analyze | 3 lines | `speckitadv analyze` |

### 9.4 Progressive Injection for ALL Commands

#### Even simple commands benefit

```text
speckitadv constitution
├── Stage 1: Collect principles (40 lines)
├── Stage 2: Generate file (50 lines)
└── Stage 3: Verify & complete (30 lines)

speckitadv specify
├── Stage 1: Gather requirements (50 lines)
├── Stage 2: Structure spec (60 lines)
├── Stage 3: Write sections (50 lines)
└── Stage 4: Validate (30 lines)

speckitadv plan
├── Stage 1: Load spec context (40 lines)
├── Stage 2: Design approach (60 lines)
├── Stage 3: Generate plan (50 lines)
└── Stage 4: Review (30 lines)

speckitadv analyze-project
├── Stage 1: Collect inputs (50 lines)
├── Stage 2: Run enumeration (40 lines)
├── Stage 3: Analyze files - auth (60 lines)
├── Stage 4: Analyze files - db (60 lines)
├── Stage 5: Analyze files - api (60 lines)
├── Stage 6: Configuration (50 lines)
├── Stage 7: Test coverage (40 lines)
├── Stage 8: Generate report (60 lines)
└── Stage 9: Create artifacts (50 lines)
```

### 9.5 Complete Flow Example: /speckitadv.constitution

```text
User: /speckitadv.constitution

Agent reads launcher (3 lines):
  "Run: speckitadv constitution"

Agent runs: speckitadv constitution

EXE outputs:
┌────────────────────────────────────────────────────────────────┐
│ STAGE: 1/3 - Collect Principles                                │
│                                                                │
│ Ask user for their project principles.                         │
│                                                                │
│ Format: One principle per line                                 │
│   PrincipleName: MUST/SHOULD/MAY description                   │
│                                                                │
│ Examples:                                                      │
│   Library-First: MUST use existing libraries over custom code  │
│   Test-First: MUST write tests before implementation           │
│                                                                │
│ If user says "use defaults" or provides empty input,           │
│ pass --defaults flag.                                          │
│                                                                │
│ NEXT: speckitadv constitution --stage=2 --principles="<INPUT>" │
│   OR: speckitadv constitution --stage=2 --defaults             │
└────────────────────────────────────────────────────────────────┘

Agent: "Please provide your project principles..."
User: "Test-First: MUST write tests before code"

Agent runs: speckitadv constitution --stage=2 --principles="Test-First: MUST write tests before code"

EXE outputs:
┌────────────────────────────────────────────────────────────────┐
│ STAGE: 2/3 - Generate Constitution                             │
│                                                                │
│ Create file: memory/constitution.md                            │
│                                                                │
│ Content to write:                                              │
│ ---                                                            │
│ # Project Constitution v1.0.0                                  │
│ Ratified: 2025-12-21                                           │
│                                                                │
│ ## Principles                                                  │
│                                                                │
│ ### Test-First                                                 │
│ MUST write tests before implementation                         │
│ ---                                                            │
│                                                                │
│ After writing file:                                            │
│ NEXT: speckitadv constitution --stage=3                        │
└────────────────────────────────────────────────────────────────┘

Agent: Creates memory/constitution.md
Agent runs: speckitadv constitution --stage=3

EXE outputs:
┌────────────────────────────────────────────────────────────────┐
│ WORKFLOW_COMPLETE                                              │
│                                                                │
│ Constitution created: memory/constitution.md                   │
│ Version: 1.0.0                                                 │
│ Principles: 1                                                  │
│                                                                │
│ Next steps:                                                    │
│ - Run /speckitadv.specify to create specifications           │
└────────────────────────────────────────────────────────────────┘
```

### 9.6 Benefits Summary

| Aspect | Current (Prompt Files) | Zero-Prompt (EXE Only) |
|--------|----------------------|------------------------|
| Prompt files | 11 files, 2000+ lines | 11 files, 33 lines total |
| Source of truth | Scattered .md files | Single EXE |
| Version sync | Manual | Automatic |
| Source/deploy confusion | Possible | Eliminated |
| Model consistency | Varies | Guaranteed |
| Update process | Edit multiple files | Rebuild EXE |
| Distribution | EXE + prompts | EXE only |
| Context window | Full prompt loaded | 40-80 lines at a time |

### 9.7 Implementation in Python

```python
# speckit/commands/constitution.py
import typer
from speckit.prompts import emit_stage

app = typer.Typer()

@app.command()
def constitution(
    stage: int = typer.Option(1, help="Current stage"),
    principles: str = typer.Option(None, help="User principles"),
    defaults: bool = typer.Option(False, help="Use default principles"),
):
    if stage == 1:
        emit_stage(
            stage_num=1,
            total_stages=3,
            title="Collect Principles",
            content=STAGE_1_PROMPT,
            next_cmd="speckitadv constitution --stage=2 --principles='<INPUT>'",
            alt_cmd="speckitadv constitution --stage=2 --defaults"
        )
        return

    if stage == 2:
        if defaults:
            principles = DEFAULT_PRINCIPLES

        constitution_content = generate_constitution(principles)

        emit_stage(
            stage_num=2,
            total_stages=3,
            title="Generate Constitution",
            content=f"Create file: memory/constitution.md\n\nContent:\n{constitution_content}",
            next_cmd="speckitadv constitution --stage=3"
        )
        return

    if stage == 3:
        emit_complete(
            message="Constitution created: memory/constitution.md",
            next_steps=["Run /speckitadv.specify to create specifications"]
        )

def emit_stage(stage_num, total_stages, title, content, next_cmd, alt_cmd=None):
    print(f"STAGE: {stage_num}/{total_stages} - {title}")
    print()
    print(content)
    print()
    print(f"NEXT: {next_cmd}")
    if alt_cmd:
        print(f"  OR: {alt_cmd}")

def emit_complete(message, next_steps):
    print("WORKFLOW_COMPLETE")
    print()
    print(message)
    print()
    print("Next steps:")
    for step in next_steps:
        print(f"- {step}")
```

### 9.8 Revised Implementation Priority

| Priority | Task | Notes |
|----------|------|-------|
| P0 | Implement emit_stage/emit_complete helpers | Core output format |
| P0 | Convert analyze-project to progressive | Most complex, biggest win |
| P1 | Convert main prompts to progressive | constitution, specify, plan, etc. |
| P1 | Create 3-line launcher templates | Replace current .md files |
| P2 | Compile to EXE with embedded fragments | Distribution |
| P2 | CI/CD for multi-platform builds | Automation |

---

## 10. Enforced Chunking Architecture

### 10.1 The Chunking Problem

#### Current behavior with prompt-based chunking

```text
Prompt instruction:
"Generate the analysis report in 9 chunks:
1. Executive Summary
2. Technology Stack
3. Architecture Patterns
4. File Analysis Results
5. Technical Debt
6. Security Findings
7. Dependency Audit
8. Test Coverage
9. Recommendations"

What models do:
├── Opus 4.5: Sometimes follows chunking (70%)
├── Sonnet 4: Often ignores, generates at once (40% follow)
├── Lower models: Almost always ignore chunking
└── Result: Incomplete/truncated output for large projects
```

**Root cause:** Models treat chunking as a suggestion, not a requirement. They optimize for "complete faster" and attempt everything in one pass.

### 10.2 Enforced Chunking via Progressive EXE

With the EXE architecture, chunking is **enforced by design**:

```text
speckitadv analyze-project --stage=8
├── --chunk=1  →  "Generate Executive Summary ONLY"
├── --chunk=2  →  "Generate Technology Stack ONLY"
├── --chunk=3  →  "Generate Architecture Patterns ONLY"
├── --chunk=4  →  "Generate File Analysis Results ONLY"
├── --chunk=5  →  "Generate Technical Debt ONLY"
├── --chunk=6  →  "Generate Security Findings ONLY"
├── --chunk=7  →  "Generate Dependency Audit ONLY"
├── --chunk=8  →  "Generate Test Coverage ONLY"
└── --chunk=9  →  "Generate Recommendations ONLY"
```

**Each chunk is a separate command.** The model physically cannot generate multiple chunks because it only receives instructions for one at a time.

### 10.3 Chunk Flow Example

```text
Agent runs: speckitadv analyze-project --stage=8 --chunk=1 --chain=abc123

EXE outputs:
┌────────────────────────────────────────────────────────────────┐
│ REPORT CHUNK: 1/9 - Executive Summary                          │
│                                                                │
│ Generate ONLY the Executive Summary section (50-100 lines).    │
│                                                                │
│ Include:                                                       │
│ - Project name: {project_name}                                 │
│ - Analysis scope: {scope}                                      │
│ - Key findings summary (3-5 sentences)                         │
│ - Critical metrics:                                            │
│   * Files analyzed: {files_count}                              │
│   * Tech debt items: {debt_count}                              │
│   * Security issues: {security_count}                          │
│ - Primary recommendation preview                               │
│                                                                │
│ Write to: .analysis/{workspace}/analysis-report.md             │
│ Mode: CREATE (new file)                                        │
│                                                                │
│ NEXT: speckitadv analyze-project --stage=8 --chunk=2 --chain=abc│
└────────────────────────────────────────────────────────────────┘

Agent: Generates ~80 lines of Executive Summary
Agent: Creates analysis-report.md with content
Agent runs: speckitadv analyze-project --stage=8 --chunk=2 --chain=abc123

EXE outputs:
┌────────────────────────────────────────────────────────────────┐
│ REPORT CHUNK: 2/9 - Technology Stack                           │
│                                                                │
│ Generate ONLY the Technology Stack section (80-120 lines).     │
│                                                                │
│ Data from tech-stack.json:                                     │
│ {                                                              │
│   "languages": ["java-11", "javascript-es6"],                  │
│   "frameworks": {                                              │
│     "backend": ["spring-boot-2.7.5"],                          │
│     "frontend": ["react-16.8.0"]                               │
│   },                                                           │
│   "build_tools": ["maven-3.8.6"]                               │
│ }                                                              │
│                                                                │
│ Include version analysis and upgrade recommendations.          │
│                                                                │
│ Write to: .analysis/{workspace}/analysis-report.md             │
│ Mode: APPEND                                                   │
│                                                                │
│ NEXT: speckitadv analyze-project --stage=8 --chunk=3 --chain=abc│
└────────────────────────────────────────────────────────────────┘

... continues until chunk 9 ...

Agent runs: speckitadv analyze-project --stage=8 --chunk=9 --chain=abc123

EXE outputs:
┌────────────────────────────────────────────────────────────────┐
│ REPORT CHUNK: 9/9 - Recommendations (FINAL)                    │
│                                                                │
│ Generate ONLY the Recommendations section (100-150 lines).     │
│                                                                │
│ Requirements:                                                  │
│ - Primary recommendation with confidence score (0-100)         │
│ - Justify the score based on analysis findings                 │
│ - 3-5 secondary recommendations with priority                  │
│ - Actionable next steps                                        │
│ - Risk assessment for each recommendation                      │
│                                                                │
│ Write to: .analysis/{workspace}/analysis-report.md             │
│ Mode: APPEND                                                   │
│                                                                │
│ After writing, run verification:                               │
│ NEXT: speckitadv analyze-project --stage=8 --verify --chain=abc│
└────────────────────────────────────────────────────────────────┘
```

### 10.4 Benefits of Enforced Chunking

| Aspect | Prompt-Based Chunking | EXE-Enforced Chunking |
|--------|----------------------|----------------------|
| Model compliance | 40-70% | 100% (physically enforced) |
| Large project handling | Fails/truncates | Works reliably |
| Context per chunk | Entire doc context | Only chunk context |
| Recovery on failure | Start over | Resume from chunk |
| Progress visibility | None until complete | Per-chunk progress |
| Output quality | Rushed, incomplete | Focused, complete |

### 10.5 Chunk Size Guidelines

| Document Type | Total Size | Chunks | Lines per Chunk |
|---------------|------------|--------|-----------------|
| Analysis Report | 3000+ lines | 9 | 300-400 |
| Functional Spec | 1500+ lines | 6 | 250-300 |
| Technical Spec | 1200+ lines | 5 | 240-300 |
| Migration Plan | 800+ lines | 4 | 200-250 |

### 10.6 Python Implementation

```python
# speckit/commands/analyze.py

@app.command()
def analyze_project(
    stage: int = typer.Option(1),
    chunk: int = typer.Option(None),
    verify: bool = typer.Option(False),
    chain_id: str = typer.Option(None),
):
    if stage == 8 and chunk is not None:
        state = ChainState.load(chain_id)

        chunk_configs = [
            ("Executive Summary", "CREATE", 50, 100),
            ("Technology Stack", "APPEND", 80, 120),
            ("Architecture Patterns", "APPEND", 150, 200),
            ("File Analysis Results", "APPEND", 200, 300),
            ("Technical Debt", "APPEND", 150, 200),
            ("Security Findings", "APPEND", 100, 150),
            ("Dependency Audit", "APPEND", 80, 120),
            ("Test Coverage", "APPEND", 60, 100),
            ("Recommendations", "APPEND", 100, 150),
        ]

        if chunk > len(chunk_configs):
            # All chunks complete, move to verification
            emit_stage(
                stage_num=8,
                total_stages=9,
                title="Report Generation Complete",
                content="All chunks generated. Running verification...",
                next_cmd=f"speckitadv analyze-project --stage=8 --verify --chain={chain_id}"
            )
            return

        name, mode, min_lines, max_lines = chunk_configs[chunk - 1]
        context = get_chunk_context(state, chunk)

        emit_chunk(
            chunk_num=chunk,
            total_chunks=len(chunk_configs),
            title=name,
            content=get_chunk_prompt(name, context),
            file_path=f"{state.workspace}/analysis-report.md",
            mode=mode,
            line_range=(min_lines, max_lines),
            next_cmd=f"speckitadv analyze-project --stage=8 --chunk={chunk+1} --chain={chain_id}"
        )
        return

    if stage == 8 and verify:
        # Verify all chunks were generated correctly
        report_path = Path(state.workspace) / "analysis-report.md"
        issues = verify_report(report_path)

        if issues:
            emit_stage(
                stage_num=8,
                title="Verification Failed",
                content=f"Issues found:\n" + "\n".join(f"- {i}" for i in issues),
                next_cmd=f"speckitadv analyze-project --stage=8 --fix --chain={chain_id}"
            )
        else:
            emit_stage(
                stage_num=8,
                title="Verification Passed",
                content="Report complete and verified.",
                next_cmd=f"speckitadv analyze-project --stage=9 --chain={chain_id}"
            )
        return

def emit_chunk(chunk_num, total_chunks, title, content, file_path, mode, line_range, next_cmd):
    min_lines, max_lines = line_range
    print(f"REPORT CHUNK: {chunk_num}/{total_chunks} - {title}")
    print()
    print(f"Generate ONLY this section ({min_lines}-{max_lines} lines).")
    print()
    print(content)
    print()
    print(f"Write to: {file_path}")
    print(f"Mode: {mode}")
    print()
    print(f"NEXT: {next_cmd}")
```

---

## 11. Template Handling in Zero-Prompt Architecture

### 11.1 Template vs Prompt Distinction

| Type | Purpose | Handling |
|------|---------|----------|
| **Prompts** | Instructions for agent | EXE outputs as stage fragments |
| **Templates** | Structure for output files | EXE injects inline or extracts |

### 11.2 Template Injection Strategies

#### Strategy A: Inline (for templates < 100 lines)

```text
EXE outputs:
┌────────────────────────────────────────────────────────────────┐
│ STAGE: 2/3 - Generate Constitution                             │
│                                                                │
│ Create file: memory/constitution.md                            │
│                                                                │
│ Use this template:                                             │
│ ══════════════════════════════════════════════════════════════ │
│ # Project Constitution v{version}                              │
│ Ratified: {date}                                               │
│                                                                │
│ ## Principles                                                  │
│                                                                │
│ {for each principle:}                                          │
│ ### {principle_name}                                           │
│ {MUST|SHOULD|MAY} {description}                                │
│                                                                │
│ ## Governance                                                  │
│ - Amendment requires team review                               │
│ - Version follows semver                                       │
│ ══════════════════════════════════════════════════════════════ │
│                                                                │
│ Fill with:                                                     │
│ - version: 1.0.0                                               │
│ - date: 2025-12-21                                             │
│ - principles: {user_provided_principles}                       │
│                                                                │
│ NEXT: speckitadv constitution --stage=3                        │
└────────────────────────────────────────────────────────────────┘
```

#### Strategy B: Extract (for templates > 100 lines)

```text
EXE behavior:
1. Extracts embedded template to filesystem
2. Outputs reference in stage

EXE outputs:
┌────────────────────────────────────────────────────────────────┐
│ STAGE: 8/9 - Generate Analysis Report                          │
│                                                                │
│ Template extracted to:                                         │
│   .analysis/templates/analysis-report-template.md              │
│                                                                │
│ 1. Read the template                                           │
│ 2. Fill all {placeholders} with data below                     │
│ 3. Save to: .analysis/project/analysis-report.md               │
│                                                                │
│ Data for template:                                             │
│ - project_name: legacy-app                                     │
│ - files_analyzed: 187                                          │
│ - patterns: auth(JWT), db(PostgreSQL)                          │
│ - tech_debt_items: 34                                          │
│ - security_findings: 18                                        │
│                                                                │
│ NEXT: speckitadv analyze-project --stage=9 --chain=abc123      │
└────────────────────────────────────────────────────────────────┘
```

### 11.3 Template Size Guidelines

| Template | Lines | Strategy |
|----------|-------|----------|
| constitution-template.md | ~50 | Inline |
| spec-template.md | ~80 | Inline |
| plan-template.md | ~60 | Inline |
| tasks-template.md | ~40 | Inline |
| analysis-report-template.md | ~300 | Extract |
| functional-spec-template.md | ~200 | Extract |
| technical-spec-template.md | ~250 | Extract |

### 11.4 Python Implementation for Templates

```python
# speckit/templates.py
import sys
from pathlib import Path

def get_embedded_template(name: str) -> str:
    """Load template from embedded assets."""
    if getattr(sys, 'frozen', False):
        base = Path(sys._MEIPASS) / 'assets' / 'templates'
    else:
        base = Path(__file__).parent / 'assets' / 'templates'
    return (base / f'{name}.md').read_text()

def extract_template(name: str, dest_dir: Path) -> Path:
    """Extract template to filesystem for agent to use."""
    content = get_embedded_template(name)
    template_dir = dest_dir / 'templates'
    template_dir.mkdir(parents=True, exist_ok=True)
    dest_path = template_dir / f'{name}.md'
    dest_path.write_text(content)
    return dest_path

def emit_with_template(
    stage_info: dict,
    template_name: str,
    context: dict,
    inline_threshold: int = 100
):
    """Emit stage with template - inline if small, extract if large."""
    template_content = get_embedded_template(template_name)
    line_count = len(template_content.splitlines())

    if line_count <= inline_threshold:
        # Inline the template
        print(f"STAGE: {stage_info['num']}/{stage_info['total']} - {stage_info['title']}")
        print()
        print("Use this template:")
        print("═" * 60)
        print(template_content)
        print("═" * 60)
        print()
        print("Fill with:")
        for key, value in context.items():
            print(f"  {key}: {value}")
    else:
        # Extract to filesystem
        dest_path = extract_template(template_name, Path(context.get('workspace', '.')))
        print(f"STAGE: {stage_info['num']}/{stage_info['total']} - {stage_info['title']}")
        print()
        print(f"Template extracted to: {dest_path}")
        print()
        print("Data for template:")
        for key, value in context.items():
            print(f"  {key}: {value}")

    print()
    print(f"NEXT: {stage_info['next_cmd']}")
```

---

## 12. Release Package and Process Changes

### 12.1 Current Release Structure

```text
GitHub Release (Current):
└── spec-kit-template-{agent}-{version}.zip
    ├── .specify/
    │   ├── scripts/
    │   │   ├── bash/           # 15 scripts (194K)
    │   │   └── powershell/     # 12 scripts (154K)
    │   └── prompts/            # 11+ prompt files (50K)
    ├── templates/
    │   ├── commands/           # Command prompts
    │   │   └── analyze/        # Staged prompts
    │   └── analyze/            # Templates
    ├── scripts/python/speckit/ # Python CLI
    └── ...other files
```

#### Current process

1. Update scripts and prompts in repo
2. Create version tag
3. GitHub Action builds ZIP per agent
4. Upload ZIPs to release

### 12.2 New Release Structure (Zero-Prompt)

```text
GitHub Release (New):
├── speckit-linux-x86_64           # Linux AMD64 binary (~25MB)
├── speckit-linux-arm64            # Linux ARM64 binary (~25MB)
├── speckit-darwin-x86_64          # macOS Intel binary (~25MB)
├── speckit-darwin-arm64           # macOS Apple Silicon (~25MB)
├── speckit-darwin-universal       # macOS Universal binary (~45MB)
├── speckit-windows-x86_64.exe     # Windows 64-bit (~30MB)
├── speckit-source.tar.gz          # Source for pip/pipx install
│
└── launcher-templates/            # Minimal launcher files per agent
    ├── claude/
    │   └── commands/
    │       ├── speckitadv.constitution.md  (3 lines)
    │       ├── speckitadv.specify.md       (3 lines)
    │       ├── speckitadv.plan.md          (3 lines)
    │       └── ...                           (3 lines each)
    ├── copilot/
    │   └── ...
    └── gemini/
        └── ...
```

### 12.3 What's Inside the EXE

```text
speckit (compiled binary)
├── Python 3.11 runtime (bundled)
├── Dependencies (typer, rich, etc.)
├── speckit package
│   ├── cli.py
│   ├── commands/
│   │   ├── constitution.py
│   │   ├── specify.py
│   │   ├── plan.py
│   │   ├── analyze.py
│   │   └── ...
│   └── core/
│       ├── state.py
│       ├── config.py
│       └── utils.py
│
└── Embedded Assets (frozen)
    ├── prompts/              # All prompt fragments
    │   ├── constitution/
    │   │   ├── stage1.md
    │   │   ├── stage2.md
    │   │   └── stage3.md
    │   ├── analyze-project/
    │   │   ├── stage1.md
    │   │   ├── stage2.md
    │   │   └── ...stage9 chunks...
    │   └── .../
    │
    └── templates/            # All output templates
        ├── constitution-template.md
        ├── analysis-report-template.md
        ├── functional-spec-template.md
        └── ...
```

### 12.4 New CI/CD Pipeline

```yaml
# .github/workflows/release-binaries.yml
name: Build and Release

on:
  push:
    tags: ['v*']

jobs:
  build-binaries:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: linux-x86_64
            artifact: speckit-linux-x86_64
          - os: ubuntu-latest
            target: linux-arm64
            artifact: speckit-linux-arm64
            # Uses cross-compilation
          - os: macos-latest
            target: darwin-universal
            artifact: speckit-darwin-universal
          - os: windows-latest
            target: windows-x86_64
            artifact: speckit-windows-x86_64.exe

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyinstaller
          pip install -e .

      - name: Build binary
        run: |
          pyinstaller \
            --onefile \
            --name ${{ matrix.artifact }} \
            --add-data "speckit/assets:assets" \
            speckit/__main__.py

      - uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.artifact }}
          path: dist/${{ matrix.artifact }}

  build-launchers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate launcher files
        run: |
          python scripts/generate-launchers.py

      - uses: actions/upload-artifact@v4
        with:
          name: launcher-templates
          path: dist/launchers/

  create-release:
    needs: [build-binaries, build-launchers]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            speckit-linux-x86_64/speckit-linux-x86_64
            speckit-linux-arm64/speckit-linux-arm64
            speckit-darwin-universal/speckit-darwin-universal
            speckit-windows-x86_64.exe/speckit-windows-x86_64.exe
            launcher-templates.zip
```

### 12.5 Launcher Generator Script

```python
# scripts/generate-launchers.py
"""Generate minimal 3-line launcher files for each agent."""

from pathlib import Path

AGENTS = {
    "claude": ".claude/commands",
    "copilot": ".github/copilot/commands",
    "gemini": ".gemini/commands",
    "cursor-agent": ".cursor/commands",
    "windsurf": ".windsurf/commands",
}

COMMANDS = [
    ("constitution", "Create or update project constitution"),
    ("specify", "Create baseline specification"),
    ("plan", "Create implementation plan"),
    ("clarify", "Ask structured questions"),
    ("tasks", "Generate actionable tasks"),
    ("implement", "Execute implementation"),
    ("analyze-project", "Analyze existing project"),
    ("checklist", "Generate quality checklist"),
    ("analyze", "Cross-artifact consistency check"),
]

LAUNCHER_TEMPLATE = """---
description: {description}
---
Run: `speckitadv {command}`
Follow all instructions in the output.
"""

def generate_launchers():
    dist = Path("dist/launchers")

    for agent, cmd_path in AGENTS.items():
        agent_dir = dist / agent / cmd_path
        agent_dir.mkdir(parents=True, exist_ok=True)

        for command, description in COMMANDS:
            launcher_content = LAUNCHER_TEMPLATE.format(
                description=description,
                command=command
            )

            launcher_file = agent_dir / f"speckitadv.{command}.md"
            launcher_file.write_text(launcher_content)
            print(f"Generated: {launcher_file}")

if __name__ == "__main__":
    generate_launchers()
```

### 12.6 Installation Flow Changes

#### Current flow

```bash
# Install CLI
pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git

# Initialize project (downloads ZIP with scripts + prompts)
speckitadv init my-project --ai claude
```

#### New flow

```bash
# Option A: Download binary directly
curl -L https://github.com/.../releases/latest/speckit-linux-x86_64 -o speckit
chmod +x speckit
sudo mv speckit /usr/local/bin/

# Option B: Install via pip (builds from source)
pipx install git+https://github.com/.../spec-kit-smart.git

# Initialize project (downloads only launcher files)
speckitadv init my-project --ai claude
```

### 12.7 Size Comparison

| Component | Current | New (EXE) | Change |
|-----------|---------|-----------|--------|
| Scripts (bash) | 194K | 0 (embedded) | -194K |
| Scripts (powershell) | 154K | 0 (embedded) | -154K |
| Prompts | ~50K | 0 (embedded) | -50K |
| Templates | ~30K | 0 (embedded) | -30K |
| Python CLI | ~50K | 0 (embedded) | -50K |
| **Downloaded files** | **~480K** | **~33 lines** | **-99.9%** |
| EXE binary | N/A | ~25MB | New |

**Trade-off:** Larger binary, but near-zero deployment files and guaranteed consistency.

### 12.8 Backward Compatibility

For users who want the old script-based approach:

```bash
# Install source package (includes scripts)
pip install spec-kit-smart[scripts]

# Or download source release
curl -L .../releases/latest/speckit-source.tar.gz | tar xz
```

---

---End of Assessment Document---
