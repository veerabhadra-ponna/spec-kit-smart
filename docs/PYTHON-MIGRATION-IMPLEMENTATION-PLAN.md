# Python Migration Implementation Plan

**Version:** 1.0.0
**Created:** 2025-12-21
**Status:** 🟡 IN PROGRESS
**Based On:** [PYTHON-MIGRATION-ASSESSMENT.md](./PYTHON-MIGRATION-ASSESSMENT.md)

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | Not Started |
| 🟡 | In Progress |
| ✅ | Completed |
| ⏸️ | Blocked |
| ❌ | Cancelled |

---

## Executive Summary

This plan implements the **Zero-Prompt Architecture** with:
- Single Python EXE containing all prompts, templates, and logic
- Progressive prompt injection for model consistency
- Enforced chunking for large document generation
- 3-line launcher files for each AI agent

**Estimated Total Effort:** 4-6 weeks
**Phases:** 6

---

## Phase 1: Project Foundation

**Status:** ⬜ Not Started
**Duration:** 2-3 days
**Dependencies:** None

### 1.1 Create Python Package Structure

**Status:** ⬜

```text
Task 1.1.1: Create package directory structure
Status: ⬜
Dependencies: None
```

Create the following structure:

```text
scripts/python/
├── speckit/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── commands/
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   └── assets/
│       ├── prompts/
│       └── templates/
├── pyproject.toml
├── tests/
│   └── __init__.py
└── README.md
```

```text
Task 1.1.2: Create pyproject.toml with dependencies
Status: ⬜
Dependencies: 1.1.1
```

Dependencies to include:
- typer (CLI framework)
- rich (terminal UI)
- pydantic (data validation)
- pytest (testing)

```text
Task 1.1.3: Create __main__.py entry point
Status: ⬜
Dependencies: 1.1.1
```

```text
Task 1.1.4: Verify package installs correctly
Status: ⬜
Dependencies: 1.1.2, 1.1.3
```

### 1.2 Setup Development Environment

**Status:** ⬜

```text
Task 1.2.1: Create virtual environment setup script
Status: ⬜
Dependencies: 1.1.4
```

```text
Task 1.2.2: Create Makefile/justfile for common tasks
Status: ⬜
Dependencies: 1.1.4
```

Commands needed:
- `make install` - Install package in dev mode
- `make test` - Run tests
- `make build` - Build EXE
- `make clean` - Clean build artifacts

```text
Task 1.2.3: Setup pytest configuration
Status: ⬜
Dependencies: 1.1.4
```

---

## Phase 2: Core Infrastructure

**Status:** ⬜ Not Started
**Duration:** 5-7 days
**Dependencies:** Phase 1 Complete

### 2.1 Stage Emission System

**Status:** ⬜

```text
Task 2.1.1: Create emit.py module with core functions
Status: ⬜
Dependencies: Phase 1
```

Functions to implement:
- `emit_stage(stage_num, total_stages, title, content, next_cmd, alt_cmd=None)`
- `emit_chunk(chunk_num, total_chunks, title, content, file_path, mode, line_range, next_cmd)`
- `emit_complete(message, next_steps)`
- `emit_error(error_type, message, recovery_cmd=None)`

```text
Task 2.1.2: Create output formatter for consistent stage output
Status: ⬜
Dependencies: 2.1.1
```

Output format:

```text
┌────────────────────────────────────────────────────────────────┐
│ STAGE: X/Y - Title                                             │
│                                                                │
│ [content]                                                      │
│                                                                │
│ NEXT: [command]                                                │
└────────────────────────────────────────────────────────────────┘
```

```text
Task 2.1.3: Write tests for emit module
Status: ⬜
Dependencies: 2.1.1, 2.1.2
```

### 2.2 State Management (Chain State)

**Status:** ⬜

```text
Task 2.2.1: Create state.py module
Status: ⬜
Dependencies: Phase 1
```

Migrate from chain-state.sh/ps1:
- `ChainState` class with load/save
- JSON schema validation
- Chain ID generation

```text
Task 2.2.2: Implement state persistence
Status: ⬜
Dependencies: 2.2.1
```

Methods:
- `ChainState.initialize(project_path)` - Create new chain
- `ChainState.load(chain_id)` - Load existing chain
- `ChainState.save(stage_name, data)` - Save stage state
- `ChainState.get_last_stage()` - Get last completed stage
- `ChainState.is_complete(stage_name)` - Check stage completion

```text
Task 2.2.3: Implement state schema validation
Status: ⬜
Dependencies: 2.2.1
```

Use pydantic for validation against 00-state-schema.json

```text
Task 2.2.4: Write tests for state module
Status: ⬜
Dependencies: 2.2.1, 2.2.2, 2.2.3
```

### 2.3 Configuration Management

**Status:** ⬜

```text
Task 2.3.1: Create config.py module
Status: ⬜
Dependencies: Phase 1
```

Migrate from common.sh/ps1:
- Load .specify/config.json
- Environment variable handling
- OS detection

```text
Task 2.3.2: Implement config loading with defaults
Status: ⬜
Dependencies: 2.3.1
```

```text
Task 2.3.3: Write tests for config module
Status: ⬜
Dependencies: 2.3.1, 2.3.2
```

### 2.4 Utility Functions

**Status:** ⬜

```text
Task 2.4.1: Create utils.py module
Status: ⬜
Dependencies: Phase 1
```

Functions:
- `get_repo_root()` - Find git repository root
- `detect_os()` - Detect operating system
- `safe_json_loads()` - Parse JSON safely
- `generate_chain_id()` - Generate unique chain ID

```text
Task 2.4.2: Write tests for utils module
Status: ⬜
Dependencies: 2.4.1
```

### 2.5 Template System

**Status:** ⬜

```text
Task 2.5.1: Create templates.py module
Status: ⬜
Dependencies: Phase 1
```

Functions:
- `get_embedded_template(name)` - Load from embedded assets
- `extract_template(name, dest_dir)` - Extract to filesystem
- `emit_with_template(stage_info, template_name, context, inline_threshold)`

```text
Task 2.5.2: Implement frozen asset detection (sys._MEIPASS)
Status: ⬜
Dependencies: 2.5.1
```

```text
Task 2.5.3: Copy all templates to assets/templates/
Status: ⬜
Dependencies: 2.5.1
```

Templates to copy:
- constitution-template.md
- spec-template.md
- plan-template.md
- tasks-template.md
- analysis-report-template.md
- functional-spec-template.md
- technical-spec-template.md
- All templates from templates/analyze/

```text
Task 2.5.4: Write tests for templates module
Status: ⬜
Dependencies: 2.5.1, 2.5.2, 2.5.3
```

### 2.6 Prompt Fragment System

**Status:** ⬜

```text
Task 2.6.1: Create prompts.py module
Status: ⬜
Dependencies: Phase 1
```

Functions:
- `get_prompt_fragment(command, stage)` - Load fragment
- `render_prompt(fragment, context)` - Render with context

```text
Task 2.6.2: Create prompt fragment directory structure
Status: ⬜
Dependencies: 2.6.1
```

Structure:

```text
assets/prompts/
├── constitution/
│   ├── stage1-collect.md
│   ├── stage2-generate.md
│   └── stage3-complete.md
├── specify/
│   ├── stage1-gather.md
│   ├── stage2-structure.md
│   ├── stage3-write.md
│   └── stage4-validate.md
├── plan/
│   └── ...
├── analyze-project/
│   ├── stage1-inputs.md
│   ├── stage2-enumerate.md
│   ├── stage3-auth.md
│   ├── stage4-db.md
│   ├── stage5-api.md
│   ├── stage6-config.md
│   ├── stage7-tests.md
│   ├── stage8-chunk1-summary.md
│   ├── stage8-chunk2-techstack.md
│   ├── ... (all 9 chunks)
│   └── stage9-artifacts.md
└── ... (other commands)
```

```text
Task 2.6.3: Write tests for prompts module
Status: ⬜
Dependencies: 2.6.1, 2.6.2
```

---

## Phase 3: Command Implementation

**Status:** ⬜ Not Started
**Duration:** 10-14 days
**Dependencies:** Phase 2 Complete

### 3.1 CLI Framework Setup

**Status:** ⬜

```text
Task 3.1.1: Create cli.py with Typer app
Status: ⬜
Dependencies: Phase 2
```

```text
Task 3.1.2: Implement global options (--version, --help, --debug)
Status: ⬜
Dependencies: 3.1.1
```

```text
Task 3.1.3: Implement subcommand routing
Status: ⬜
Dependencies: 3.1.1
```

### 3.2 Analyze-Project Command (Priority: P0)

**Status:** ⬜

This is the most complex command - implement first as reference.

```text
Task 3.2.1: Create commands/analyze.py
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.2.2: Implement Stage 1 - Input Collection
Status: ⬜
Dependencies: 3.2.1
```

- Prompt for PROJECT_PATH
- Prompt for ADDITIONAL_CONTEXT
- Prompt for ANALYSIS_SCOPE (A/B)
- If B: Prompt for concern details

```text
Task 3.2.3: Implement Stage 2 - File Enumeration
Status: ⬜
Dependencies: 3.2.2
```

Migrate from enumerate-project.sh:
- Recursive file listing
- Metadata extraction (size, modified date)
- Generate file-manifest.json

```text
Task 3.2.4: Implement Tech Stack Detection
Status: ⬜
Dependencies: 3.2.3
```

Migrate from analyze-project.sh:
- Detect languages from file extensions
- Detect frameworks from config files
- Generate tech-stack.json

```text
Task 3.2.5: Implement File Structure Categorization
Status: ⬜
Dependencies: 3.2.3
```

Categories:
- controllers, services, models, repositories
- configs, security, middleware, utils
- tests, docs, ci-cd

```text
Task 3.2.6: Implement Stage 3-7 - File Analysis (Progressive)
Status: ⬜
Dependencies: 3.2.5
```

Each stage outputs focused fragment:
- Stage 3: Auth analysis
- Stage 4: Database analysis
- Stage 5: API analysis
- Stage 6: Configuration analysis
- Stage 7: Test coverage analysis

```text
Task 3.2.7: Implement Stage 8 - Report Generation (Chunked)
Status: ⬜
Dependencies: 3.2.6
```

9 chunks with enforced chunking:
- Chunk 1: Executive Summary (CREATE)
- Chunk 2: Technology Stack (APPEND)
- Chunk 3: Architecture Patterns (APPEND)
- Chunk 4: File Analysis Results (APPEND)
- Chunk 5: Technical Debt (APPEND)
- Chunk 6: Security Findings (APPEND)
- Chunk 7: Dependency Audit (APPEND)
- Chunk 8: Test Coverage (APPEND)
- Chunk 9: Recommendations (APPEND)

```text
Task 3.2.8: Implement Report Verification
Status: ⬜
Dependencies: 3.2.7
```

Migrate from verify-analysis-report.sh:
- Check all sections present
- Verify minimum line counts
- Check for file:line references
- Validate no TODO/TBD placeholders

```text
Task 3.2.9: Implement Stage 9 - Artifact Generation
Status: ⬜
Dependencies: 3.2.8
```

Generate based on scope:
- Scope A: functional-spec-legacy.md, functional-spec-target.md, technical-spec.md
- Scope B: concern-analysis.md, migration-plan.md

```text
Task 3.2.10: Write integration tests for analyze command
Status: ⬜
Dependencies: 3.2.1-3.2.9
```

### 3.3 Constitution Command

**Status:** ⬜

```text
Task 3.3.1: Create commands/constitution.py
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.3.2: Implement Stage 1 - Collect Principles
Status: ⬜
Dependencies: 3.3.1
```

```text
Task 3.3.3: Implement Stage 2 - Generate Constitution
Status: ⬜
Dependencies: 3.3.2
```

```text
Task 3.3.4: Implement Stage 3 - Verify & Complete
Status: ⬜
Dependencies: 3.3.3
```

```text
Task 3.3.5: Write tests for constitution command
Status: ⬜
Dependencies: 3.3.1-3.3.4
```

### 3.4 Specify Command

**Status:** ⬜

```text
Task 3.4.1: Create commands/specify.py
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.4.2: Implement Stage 1 - Gather Requirements
Status: ⬜
Dependencies: 3.4.1
```

```text
Task 3.4.3: Implement Stage 2 - Structure Spec
Status: ⬜
Dependencies: 3.4.2
```

```text
Task 3.4.4: Implement Stage 3 - Write Sections
Status: ⬜
Dependencies: 3.4.3
```

```text
Task 3.4.5: Implement Stage 4 - Validate
Status: ⬜
Dependencies: 3.4.4
```

```text
Task 3.4.6: Write tests for specify command
Status: ⬜
Dependencies: 3.4.1-3.4.5
```

### 3.5 Plan Command

**Status:** ⬜

```text
Task 3.5.1: Create commands/plan.py
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.5.2: Implement Stage 1 - Load Spec Context
Status: ⬜
Dependencies: 3.5.1
```

```text
Task 3.5.3: Implement Stage 2 - Design Approach
Status: ⬜
Dependencies: 3.5.2
```

```text
Task 3.5.4: Implement Stage 3 - Generate Plan
Status: ⬜
Dependencies: 3.5.3
```

```text
Task 3.5.5: Implement Stage 4 - Review
Status: ⬜
Dependencies: 3.5.4
```

```text
Task 3.5.6: Write tests for plan command
Status: ⬜
Dependencies: 3.5.1-3.5.5
```

### 3.6 Remaining Commands

**Status:** ⬜

```text
Task 3.6.1: Implement clarify command
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.6.2: Implement tasks command
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.6.3: Implement implement command
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.6.4: Implement checklist command
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.6.5: Implement analyze (cross-artifact) command
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.6.6: Implement init command (project initialization)
Status: ⬜
Dependencies: 3.1.3
```

```text
Task 3.6.7: Write tests for all remaining commands
Status: ⬜
Dependencies: 3.6.1-3.6.6
```

---

## Phase 4: Prompt Fragment Creation

**Status:** ⬜ Not Started
**Duration:** 3-5 days
**Dependencies:** Phase 3 (can run in parallel with 3.3-3.6)

### 4.1 Extract and Fragment Existing Prompts

**Status:** ⬜

```text
Task 4.1.1: Fragment constitution.md into 3 stages
Status: ⬜
Dependencies: None
```

- stage1-collect.md (~40 lines)
- stage2-generate.md (~50 lines)
- stage3-complete.md (~30 lines)

```text
Task 4.1.2: Fragment specify.md into 4 stages
Status: ⬜
Dependencies: None
```

```text
Task 4.1.3: Fragment plan.md into 4 stages
Status: ⬜
Dependencies: None
```

```text
Task 4.1.4: Fragment clarify.md into 3 stages
Status: ⬜
Dependencies: None
```

```text
Task 4.1.5: Fragment tasks.md into 3 stages
Status: ⬜
Dependencies: None
```

```text
Task 4.1.6: Fragment implement.md into 4 stages
Status: ⬜
Dependencies: None
```

```text
Task 4.1.7: Fragment analyze-project into 9+ stages with chunks
Status: ⬜
Dependencies: None
```

This is the most complex:
- Stage 1: Input collection (1 fragment)
- Stage 2: Enumeration (1 fragment)
- Stages 3-7: Analysis phases (5 fragments)
- Stage 8: Report chunks (9 fragments)
- Stage 9: Artifacts (2 fragments - scope A/B)

Total: ~18 fragments

```text
Task 4.1.8: Fragment checklist.md into 2 stages
Status: ⬜
Dependencies: None
```

```text
Task 4.1.9: Fragment analyze.md (cross-artifact) into 3 stages
Status: ⬜
Dependencies: None
```

### 4.2 Validate Fragment Quality

**Status:** ⬜

```text
Task 4.2.1: Verify each fragment is < 100 lines
Status: ⬜
Dependencies: 4.1.1-4.1.9
```

```text
Task 4.2.2: Verify context placeholders are correct
Status: ⬜
Dependencies: 4.1.1-4.1.9
```

```text
Task 4.2.3: Verify NEXT command format is consistent
Status: ⬜
Dependencies: 4.1.1-4.1.9
```

```text
Task 4.2.4: Test fragment rendering with sample context
Status: ⬜
Dependencies: 4.2.1-4.2.3
```

---

## Phase 5: Packaging and Distribution

**Status:** ⬜ Not Started
**Duration:** 3-5 days
**Dependencies:** Phase 3 and 4 Complete

### 5.1 PyInstaller Configuration

**Status:** ⬜

```text
Task 5.1.1: Create speckit.spec file
Status: ⬜
Dependencies: Phase 3, Phase 4
```

Configuration:
- One-file mode
- Include assets/prompts and assets/templates
- Set appropriate icon

```text
Task 5.1.2: Test local build on development machine
Status: ⬜
Dependencies: 5.1.1
```

```text
Task 5.1.3: Verify embedded assets accessible via sys._MEIPASS
Status: ⬜
Dependencies: 5.1.2
```

```text
Task 5.1.4: Test EXE execution end-to-end
Status: ⬜
Dependencies: 5.1.3
```

### 5.2 Launcher File Generation

**Status:** ⬜

```text
Task 5.2.1: Create scripts/generate-launchers.py
Status: ⬜
Dependencies: None
```

```text
Task 5.2.2: Generate launchers for all agents
Status: ⬜
Dependencies: 5.2.1
```

Agents:
- claude (.claude/commands/)
- copilot (.github/copilot/commands/)
- gemini (.gemini/commands/)
- cursor-agent (.cursor/commands/)
- windsurf (.windsurf/commands/)
- kilocode (.kilocode/commands/)
- auggie (.augment/commands/)
- codebuddy (.codebuddy/commands/)
- roo (.roo/commands/)
- q (.amazonq/commands/)
- amp (.agents/commands/)

```text
Task 5.2.3: Verify launcher format (3 lines each)
Status: ⬜
Dependencies: 5.2.2
```

### 5.3 CI/CD Pipeline

**Status:** ⬜

```text
Task 5.3.1: Create .github/workflows/build-binaries.yml
Status: ⬜
Dependencies: 5.1.4
```

Matrix build:
- ubuntu-latest → speckit-linux-x86_64
- ubuntu-latest (cross) → speckit-linux-arm64
- macos-latest → speckit-darwin-universal
- windows-latest → speckit-windows-x86_64.exe

```text
Task 5.3.2: Create .github/workflows/test.yml
Status: ⬜
Dependencies: Phase 3
```

Run tests on all PRs.

```text
Task 5.3.3: Create release automation
Status: ⬜
Dependencies: 5.3.1, 5.2.2
```

On tag push:
- Build all binaries
- Generate launchers
- Create GitHub release
- Upload all artifacts

```text
Task 5.3.4: Test full release pipeline
Status: ⬜
Dependencies: 5.3.3
```

### 5.4 Update Init Command

**Status:** ⬜

```text
Task 5.4.1: Modify init to download launchers only
Status: ⬜
Dependencies: 5.2.3, 5.3.3
```

Current: Downloads full ZIP with scripts + prompts
New: Downloads only 3-line launcher files

```text
Task 5.4.2: Add binary auto-detection and installation option
Status: ⬜
Dependencies: 5.4.1
```

```text
Task 5.4.3: Test init command end-to-end
Status: ⬜
Dependencies: 5.4.2
```

---

## Phase 6: Testing and Documentation

**Status:** ⬜ Not Started
**Duration:** 3-5 days
**Dependencies:** Phase 5 Complete

### 6.1 Integration Testing

**Status:** ⬜

```text
Task 6.1.1: Create integration test for full analyze-project workflow
Status: ⬜
Dependencies: Phase 5
```

Test with sample project, verify:
- All stages execute
- State persists correctly
- Chunks generate in order
- Final report passes verification

```text
Task 6.1.2: Create integration test for constitution workflow
Status: ⬜
Dependencies: Phase 5
```

```text
Task 6.1.3: Create integration test for specify → plan → tasks flow
Status: ⬜
Dependencies: Phase 5
```

```text
Task 6.1.4: Test session recovery (interrupt and resume)
Status: ⬜
Dependencies: 6.1.1
```

### 6.2 Cross-Platform Testing

**Status:** ⬜

```text
Task 6.2.1: Test on Linux (Ubuntu)
Status: ⬜
Dependencies: 5.3.4
```

```text
Task 6.2.2: Test on macOS (Intel and Apple Silicon)
Status: ⬜
Dependencies: 5.3.4
```

```text
Task 6.2.3: Test on Windows
Status: ⬜
Dependencies: 5.3.4
```

### 6.3 AI Model Testing

**Status:** ⬜

```text
Task 6.3.1: Test with Claude Opus 4.5
Status: ⬜
Dependencies: Phase 5
```

```text
Task 6.3.2: Test with Claude Sonnet 4
Status: ⬜
Dependencies: Phase 5
```

Verify:
- All stages followed correctly
- Chunking enforced
- No instruction skipping

```text
Task 6.3.3: Test with lower models if available
Status: ⬜
Dependencies: Phase 5
```

### 6.4 Documentation Updates

**Status:** ⬜

```text
Task 6.4.1: Update README.md with new installation instructions
Status: ⬜
Dependencies: Phase 5
```

```text
Task 6.4.2: Create MIGRATION-GUIDE.md for existing users
Status: ⬜
Dependencies: Phase 5
```

```text
Task 6.4.3: Update CHANGELOG.md
Status: ⬜
Dependencies: Phase 5
```

```text
Task 6.4.4: Create developer documentation for adding new commands
Status: ⬜
Dependencies: Phase 5
```

---

## Dependency Graph

```text
Phase 1: Foundation
    │
    ▼
Phase 2: Core Infrastructure
    │
    ├──────────────────┐
    ▼                  ▼
Phase 3: Commands    Phase 4: Fragments
    │                  │
    └────────┬─────────┘
             ▼
      Phase 5: Packaging
             │
             ▼
      Phase 6: Testing
```

---

## Risk Mitigation

### Risk 1: PyInstaller Binary Size Too Large

#### Mitigation

- Use Nuitka as alternative (smaller binaries)
- Exclude unnecessary dependencies
- Use --exclude-module for unused stdlib modules

### Risk 2: Cross-Platform Differences

#### Mitigation

- Use pathlib for all path operations
- Test on all platforms early
- CI/CD runs tests on all platforms

### Risk 3: AI Model Doesn't Follow Stage Instructions

#### Mitigation

- Keep fragments under 80 lines
- Use clear NEXT command format
- Test with multiple models
- Add explicit "DO NOT" instructions

### Risk 4: State Corruption During Multi-Chunk Generation

#### Mitigation

- Atomic file writes
- Backup state before each stage
- Clear recovery instructions

---

## Success Criteria

### Phase 1 Complete When

- [ ] Package installs with `pip install -e .`
- [ ] `speckit --version` works

### Phase 2 Complete When

- [ ] All core modules have >80% test coverage
- [ ] State save/load works correctly
- [ ] Template extraction works

### Phase 3 Complete When

- [ ] All commands implemented
- [ ] Progressive stages work
- [ ] Chunking enforced

### Phase 4 Complete When

- [ ] All fragments created (<100 lines each)
- [ ] Context placeholders work

### Phase 5 Complete When

- [ ] EXE builds on all platforms
- [ ] Launchers generated
- [ ] Release pipeline works

### Phase 6 Complete When

- [ ] Integration tests pass
- [ ] Works on Sonnet 4 consistently
- [ ] Documentation updated

---

## Implementation Progress Log

### Session 2025-12-21 (Current)

#### Completed

**Phase 1: Project Foundation** ✅
- Created package structure: `scripts/python/speckit/`
- Created `pyproject.toml` with dependencies (typer, rich, pydantic)
- Created `__init__.py` and `__main__.py` entry points
- Verified package installs correctly

**Phase 2: Core Infrastructure** ✅
- Created `core/emit.py` - Stage emission system with box-drawing output
- Created `core/state.py` - Chain state management with Pydantic validation
- Created `core/config.py` - Configuration loading with defaults
- Created `core/utils.py` - Utility functions (repo root, run_command, etc.)
- Created `core/templates.py` - Template loading and extraction
- Created `core/prompts.py` - Prompt fragment system

**Phase 3: Commands** 🟡 In Progress
- Created `cli.py` with Typer app - all commands defined
- Created `commands/analyze.py` - Full analyze-project workflow with stages/chunks
- Created `commands/constitution.py` - 3-stage constitution workflow
- Remaining commands using placeholder emit_stage

**Phase 4: Prompt Fragments** ⚠️ Needs Revision
- 34 fragments created externally for analyze-project
- **ISSUE: Fragments do NOT meet design spec** (see below)

---

## Critical Issue: Fragmentation Gap

### Problem

The external fragmentation of `analyze-project` prompts does NOT match the design spec:

| Requirement | Design Target | Actual | Status |
|-------------|---------------|--------|--------|
| Fragment size | 50-100 lines | 138-920 lines | ❌ 2-10x too large |
| Main prompts | Fragmented | NOT fragmented (228-1210 lines) | ❌ Not started |
| Templates | Handled | NOT fragmented (453-1153 lines) | ⚠️ Acceptable (different handling) |

### analyze-project Fragments (Current State)

| Fragment | Lines | Target | Gap |
|----------|-------|--------|-----|
| 01a-initialization | 138 | 50-80 | 1.7x |
| 01b-input-collection | 294 | 50-80 | 3.7x |
| 02b-deep-dive | 472 | 50-80 | 5.9x |
| 06-scope-artifacts | 920 | 50-80 | 11.5x |
| 02-file-analysis | 870 | 50-80 | 10.9x |
| 04-report-generation | 755 | 50-80 | 9.4x |

### Main Prompts (NOT Fragmented)

| File | Lines | Action Needed |
|------|-------|---------------|
| implement.md | 657 | Split into ~8 fragments |
| specify.md | 483 | Split into ~6 fragments |
| plan.md | 350 | Split into ~4 fragments |
| tasks.md | 324 | Split into ~4 fragments |
| constitution.md | 233 | Split into ~3 fragments |
| clarify.md | 228 | Split into ~3 fragments |
| checklist.md | 228 | Split into ~3 fragments |

### Recommendations

1. **Re-fragment analyze-project prompts** - Further subdivide into 50-80 line chunks
2. **Fragment main prompts** - Apply same fragmentation pattern
3. **Templates are OK** - Use inline/extract threshold (100 lines) already implemented

### Impact

Without proper fragmentation:
- Progressive injection won't reduce cognitive load for models
- Lower models (Sonnet 4) may still fail to follow complex instructions
- Chunking enforcement loses effectiveness

---

## Session Recovery Checkpoints

If session is interrupted, resume from the last completed task. Check:

1. `git status` - See uncommitted work
2. `git log --oneline -5` - See recent commits
3. Check this file for last ✅ status

**Current Checkpoint:** Phase 3 In Progress - Commands created, need proper fragmentation

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-21 | Initial plan created | Claude |

---

---End of Implementation Plan---
