<div align="center">
    <img src="./media/logo_small.webp" alt="Spec Kit Logo"/>
    <h1>🌱 Spec Kit</h1>
    <h3><em>Build high-quality software faster.</em></h3>
</div>

<p align="center">
    <strong>An open source toolkit that allows you to focus on product scenarios and predictable outcomes instead of vibe coding every piece from scratch.</strong>
</p>

<p align="center">
    <a href="https://github.com/veerabhadra-ponna/spec-kit-smart/actions/workflows/release.yml"><img src="https://github.com/veerabhadra-ponna/spec-kit-smart/actions/workflows/release.yml/badge.svg" alt="Release"/></a>
    <a href="https://github.com/veerabhadra-ponna/spec-kit-smart/stargazers"><img src="https://img.shields.io/github/stars/veerabhadra-ponna/spec-kit-smart?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/veerabhadra-ponna/spec-kit-smart/blob/main/LICENSE"><img src="https://img.shields.io/github/license/veerabhadra-ponna/spec-kit-smart" alt="License"/></a>
    <a href="https://veerabhadra-ponna.github.io/spec-kit-smart/"><img src="https://img.shields.io/badge/docs-GitHub_Pages-blue" alt="Documentation"/></a>
</p>

---

## Table of Contents

- [🤔 What is Spec-Driven Development?](#-what-is-spec-driven-development)
- [⚡ Get Started](#-get-started)
- [🔄 Reverse Engineering & Modernization](#-reverse-engineering--modernization)
- [📽️ Video Overview](#️-video-overview)
- [🤖 Supported AI Agents](#-supported-ai-agents)
- [🔧 Specify CLI Reference](#-specify-cli-reference)
- [🎭 Orchestrator Workflow](#-orchestrator-workflow)
- [🏢 Corporate Guidelines System](#-corporate-guidelines-system)
- [📚 Core Philosophy](#-core-philosophy)
- [🌟 Development Phases](#-development-phases)
- [🎯 Experimental Goals](#-experimental-goals)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn More](#-learn-more)
- [📋 Detailed Process](#-detailed-process)
- [🔍 Troubleshooting](#-troubleshooting)
- [👥 Maintainers](#-maintainers)
- [💬 Support](#-support)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)

## 🤔 What is Spec-Driven Development?

Spec-Driven Development **flips the script** on traditional software development. For decades, code has been king — specifications were just scaffolding we built and discarded once the "real work" of coding began. Spec-Driven Development changes this: **specifications become executable**, directly generating working implementations rather than just guiding them.

## ⚡ Get Started

### 1. Install Specify CLI

Choose your preferred installation method:

#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install specify-cli --from git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
```

Then use the tool directly:

```bash
specify init <PROJECT_NAME>
specify check
```

To upgrade specify run:

```bash
uv tool install specify-cli --force --from git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
uvx --from git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME>
```

**Benefits of persistent installation:**

- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
- Cleaner shell configuration

### 2. Establish project principles

Launch your AI assistant in the project directory. The `/speckit.*` commands are available in the assistant.

Use the **`/speckit.constitution`** command to create your project's governing principles and development guidelines that will guide all subsequent development.

```bash
/speckit.constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements
```

### 3. Create the spec

Use the **`/speckit.specify`** command to describe what you want to build. Focus on the **what** and **why**, not the tech stack.

```bash
/speckit.specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums are never in other nested albums. Within each album, photos are previewed in a tile-like interface.
```

### 4. Create a technical implementation plan

Use the **`/speckit.plan`** command to provide your tech stack and architecture choices.

```bash
/speckit.plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

### 5. Break down into tasks

Use **`/speckit.tasks`** to create an actionable task list from your implementation plan.

```bash
/speckit.tasks
```

### 6. Execute implementation

Use **`/speckit.implement`** to execute all tasks and build your feature according to the plan.

```bash
/speckit.implement
```

For detailed step-by-step instructions, see our [comprehensive guide](./spec-driven.md).

### Workflow Diagram

```mermaid
flowchart TD
    Start([Start New Feature]) --> Constitution
    Constitution[🏛️ Constitution - REQUIRED] --> Specify
    Specify[📝 Specify - REQUIRED] --> Clarify
    Clarify[❓ Clarify - OPTIONAL] -->|Recommended| Plan
    Clarify -.->|Skip if clear| Plan
    Plan[🏗️ Plan - REQUIRED] --> Tasks
    Tasks[📋 Tasks - REQUIRED] --> Analyze
    Analyze[🔍 Analyze - OPTIONAL] -->|Recommended| Implement
    Analyze -.->|Skip if confident| Implement
    Implement[⚙️ Implement - REQUIRED] --> Checklist
    Checklist[✅ Checklist - OPTIONAL] --> Done
    Done([✅ Feature Complete])

    style Constitution fill:#ffcccc,stroke:#333,stroke-width:2px
    style Specify fill:#ffcccc,stroke:#333,stroke-width:2px
    style Plan fill:#ffcccc,stroke:#333,stroke-width:2px
    style Tasks fill:#ffcccc,stroke:#333,stroke-width:2px
    style Implement fill:#ffcccc,stroke:#333,stroke-width:2px
    style Clarify fill:#ffffcc,stroke:#333,stroke-width:2px
    style Analyze fill:#ffffcc,stroke:#333,stroke-width:2px
    style Checklist fill:#ffffcc,stroke:#333,stroke-width:2px
    style Start fill:#ccffcc,stroke:#333,stroke-width:2px
    style Done fill:#ccffcc,stroke:#333,stroke-width:2px
```

**Required Commands** (Red):

- `/speckit.constitution` - Establish project principles
- `/speckit.specify` - Define what to build
- `/speckit.plan` - Create technical design
- `/speckit.tasks` - Generate actionable tasks
- `/speckit.implement` - Execute implementation

**Optional Commands** (Yellow):

- `/speckit.clarify` - Resolve ambiguities (recommended before planning)
- `/speckit.analyze` - Validate consistency (recommended before implementation)
- `/speckit.checklist` - Quality validation (recommended after implementation)

**Alternative: Use Orchestrator** - Run the entire workflow with a single command:

```bash
/speckit.orchestrate <feature-description>
```

Then use `/speckit.resume` to continue after chat limits or interruptions.

## 🔄 Reverse Engineering & Modernization

**NEW**: Analyze existing projects, assess technical debt, and plan modernization strategies!

Spec Kit now supports **reverse engineering existing codebases** to help you:

- 📊 **Assess current state** - Technology stack, architecture, dependencies, code quality
- ✅ **Identify strengths** - What's working well and should be preserved
- ❌ **Find weaknesses** - Technical debt, security vulnerabilities, anti-patterns
- 🔄 **Plan upgrades** - LTS versions, security patches, framework migrations
- 🎯 **Make decisions** - Inline upgrade vs greenfield rewrite vs hybrid approach
- 📈 **Score feasibility** - Data-driven confidence scores for recommendations

### Quick Start

```bash
# In your AI coding agent (Claude Code, GitHub Copilot, etc.)
/speckit.analyze-project
```

When prompted, provide:

```text
PROJECT_PATH: /path/to/your/existing/project
ANALYSIS_DEPTH: STANDARD
FOCUS_AREAS: ALL
```

### What You Get

Analysis generates comprehensive reports in `.analysis/[PROJECT]-[TIMESTAMP]/`:

- **`analysis-report.md`** - Complete assessment with good/bad aspects, upgrade paths, and recommendations
- **`upgrade-plan.md`** - Step-by-step upgrade instructions (if inline upgrade recommended)
- **`recommended-constitution.md`** - Suggested project principles derived from codebase analysis
- **`decision-matrix.md`** - Stakeholder-friendly comparison table
- **`dependency-audit.json`** - Machine-readable dependency data
- **`metrics-summary.json`** - Codebase metrics

### Analysis Depths

- **QUICK** (30 min) - Basic health check, dependency scan, critical issues
- **STANDARD** (2-4 hours) - Full analysis, architecture review, upgrade roadmaps - **Recommended**
- **COMPREHENSIVE** (1-2 days) - Deep dive with performance profiling, security audit, detailed planning

### Focus Areas

- **ALL** - Complete analysis (recommended for first-time analysis)
- **SECURITY** - Vulnerability scanning, dependency audits, security patterns
- **PERFORMANCE** - Bottleneck identification, optimization opportunities
- **ARCHITECTURE** - Design patterns, technical debt, modularity assessment
- **DEPENDENCIES** - Package analysis, upgrade paths, LTS compliance

### Feasibility Scoring

**Inline Upgrade Feasibility** (0-100):

Calculated from:
- Code Quality (20%)
- Test Coverage (15%)
- Dependency Health (20%)
- Architecture Quality (15%)
- Team Familiarity (10%)
- Documentation (10%)
- Breaking Changes (10%)

**Interpretation**:
- **80-100**: ✅ Highly feasible - proceed with inline upgrade
- **60-79**: ⚠️ Feasible with caution - assess risks carefully
- **40-59**: 🟡 Moderately risky - consider hybrid approach
- **0-39**: 🔴 High risk - consider greenfield rewrite

**Greenfield Rewrite Feasibility** (0-100):

Calculated from:
- Requirements Clarity (20%)
- Technical Debt Level (20%)
- Business Continuity (15%)
- Team Capacity (15%)
- Time Available (15%)
- Budget (15%)

### Example Output

```
✅ Analysis Complete: MyLegacyApp

📊 Analysis Summary:
   - Project Type: Monolithic Web Application
   - Primary Stack: Node.js 14.x + React 16.8
   - Lines of Code: 45,320
   - Dependencies: 237 (42 outdated, 7 vulnerable)
   - Test Coverage: 43%

🎯 Recommendation: INLINE UPGRADE (Feasibility: 68/100, Confidence: 85%)

🚨 Immediate Actions (Critical):
   1. Upgrade lodash (CVE-2021-23337, CVSS 9.8) - 15 mins
   2. Patch Node.js 14.x → 18.x (EOL passed) - 2-3 hours
   3. Fix authentication bypass in /api/login - 4 hours

📁 Generated Reports:
   - .analysis/MyLegacyApp-2025-11-06/analysis-report.md
   - .analysis/MyLegacyApp-2025-11-06/upgrade-plan.md
   - .analysis/MyLegacyApp-2025-11-06/decision-matrix.md
```

### Use Cases

**When to use reverse engineering**:

1. **Inherited Codebase** - Understand state, assess technical debt
2. **Modernization Planning** - Runtime/framework versions approaching EOL
3. **Migration Decision** - Deciding between upgrade-in-place vs rewrite
4. **Compliance & Security** - Security audit, identify vulnerabilities
5. **Team Onboarding** - Architecture overview, establish coding standards

### Workflow Examples

**Inline Upgrade Workflow**:
1. Run `/speckit.analyze-project`
2. Review `analysis-report.md`
3. Fix critical security issues immediately
4. Follow `upgrade-plan.md` phase-by-phase
5. Validate at each checkpoint
6. Deploy to production

**Greenfield Rewrite Workflow**:
1. Run `/speckit.analyze-project`
2. Review recommendation (greenfield rewrite)
3. Use `recommended-constitution.md` to establish principles:
   ```bash
   /speckit.constitution [use recommended principles from analysis]
   ```
4. Create spec based on reverse-engineered requirements:
   ```bash
   /speckit.specify [describe features from analysis]
   ```
5. Plan with modern tech stack:
   ```bash
   /speckit.plan [modern technologies]
   ```
6. Implement using `/speckit.orchestrate`

**Hybrid Approach (Strangler Fig)**:
1. Extract and modernize components incrementally
2. Maintain parallel systems during migration
3. Gradually decommission legacy system

### Documentation

For comprehensive guide with examples, scoring details, and prompt suggestions:

- **Full Guide**: [docs/reverse-engineering.md](docs/reverse-engineering.md)
- **Examples & Prompts**: [docs/reverse-engineering-examples.md](docs/reverse-engineering-examples.md)

---

## 📽️ Video Overview

Want to see Spec Kit in action? Watch our [video overview](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)!

[![Spec Kit video header](/media/spec-kit-video-header.jpg)](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)

## 🤖 Supported AI Agents

| Agent                                                     | Support | Notes                                             |
|-----------------------------------------------------------|---------|---------------------------------------------------|
| [Claude Code](https://www.anthropic.com/claude-code)      | ✅ |                                                   |
| [GitHub Copilot](https://code.visualstudio.com/)          | ✅ |                                                   |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ |                                                   |
| [Cursor](https://cursor.sh/)                              | ✅ |                                                   |
| [Qwen Code](https://github.com/QwenLM/qwen-code)          | ✅ |                                                   |
| [opencode](https://opencode.ai/)                          | ✅ |                                                   |
| [Windsurf](https://windsurf.com/)                         | ✅ |                                                   |
| [Kilo Code](https://github.com/Kilo-Org/kilocode)         | ✅ |                                                   |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview)   | ✅ |                                                   |
| [CodeBuddy CLI](https://www.codebuddy.ai/cli)             | ✅ |                                                   |
| [Roo Code](https://roocode.com/)                          | ✅ |                                                   |
| [Codex CLI](https://github.com/openai/codex)              | ✅ |                                                   |
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ | Amazon Q Developer CLI [does not support](https://github.com/aws/amazon-q-developer-cli/issues/3064) custom arguments for slash commands. |
| [Amp](https://ampcode.com/) | ✅ | |

## 🔧 Specify CLI Reference

The `specify` command supports the following options:

### Commands

| Command     | Description                                                    |
|-------------|----------------------------------------------------------------|
| `init`      | Initialize a new Specify project from the latest template      |
| `check`     | Check for installed tools (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`) |

### `specify init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
|------------------------|----------|------------------------------------------------------------------------------|
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory) |
| `--ai`                 | Option   | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor-agent`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, `codebuddy`, `amp`, or `q` |
| `--script`             | Option   | Script variant to use: `sh` (bash/zsh) or `ps` (PowerShell)                 |
| `--ignore-agent-tools` | Flag     | Skip checks for AI agent tools like Claude Code                             |
| `--no-git`             | Flag     | Skip git repository initialization                                          |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one   |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation) |
| `--skip-tls`           | Flag     | Skip SSL/TLS verification (not recommended)                                 |
| `--debug`              | Flag     | Enable detailed debug output for troubleshooting                            |
| `--github-token`       | Option   | GitHub token for API requests (or set GH_TOKEN/GITHUB_TOKEN env variable)  |

### Examples

```bash
# Basic project initialization
specify init my-project

# Initialize with specific AI assistant
specify init my-project --ai claude

# Initialize with Cursor support
specify init my-project --ai cursor-agent

# Initialize with Windsurf support
specify init my-project --ai windsurf

# Initialize with Amp support
specify init my-project --ai amp

# Initialize with PowerShell scripts (Windows/cross-platform)
specify init my-project --ai copilot --script ps

# Initialize in current directory
specify init . --ai copilot
# or use the --here flag
specify init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
specify init . --force --ai copilot
# or 
specify init --here --force --ai copilot

# Skip git initialization
specify init my-project --ai gemini --no-git

# Enable debug output for troubleshooting
specify init my-project --ai claude --debug

# Use GitHub token for API requests (helpful for corporate environments)
specify init my-project --ai claude --github-token ghp_your_token_here

# Check system requirements
specify check
```

### Available Slash Commands

After running `specify init`, your AI coding agent will have access to these slash commands for structured development:

#### Orchestration Commands

**NEW**: Simplified workflow management and context restoration:

| Command                  | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/speckit.orchestrate`  | **Orchestrate the complete workflow** from feature description to implementation in a single command. Manages state, phase transitions, and provides interactive or automatic execution modes. |
| `/speckit.resume`       | **Restore context and resume work** after chat limit or interruption. Loads all artifacts and continues from exact stopping point with zero context loss. |

**Quick Start with Orchestrator:**

```bash
# Run entire workflow in one command
/speckit.orchestrate Build a user authentication system with OAuth2 and JWT

# Or resume after chat limit/interruption
/speckit.resume
```

See [Orchestrator Workflow Guide](#-orchestrator-workflow) for detailed usage.

#### Core Commands

Essential commands for the Spec-Driven Development workflow (can be used individually or via orchestrator):

| Command                  | Description                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/speckit.constitution`  | Create or update project governing principles and development guidelines |
| `/speckit.specify`       | Define what you want to build (requirements and user stories)        |
| `/speckit.plan`          | Create technical implementation plans with your chosen tech stack     |
| `/speckit.tasks`         | Generate actionable task lists for implementation                     |
| `/speckit.implement`     | Execute all tasks to build the feature according to the plan         |

#### Optional Commands

Additional commands for enhanced quality and validation:

| Command              | Description                                                           |
|----------------------|-----------------------------------------------------------------------|
| `/speckit.clarify`   | Clarify underspecified areas (recommended before `/speckit.plan`; formerly `/quizme`) |
| `/speckit.analyze`   | Cross-artifact consistency & coverage analysis (run after `/speckit.tasks`, before `/speckit.implement`) |
| `/speckit.checklist` | Generate custom quality checklists that validate requirements completeness, clarity, and consistency (like "unit tests for English") |

### Environment Variables

| Variable         | Description                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| `SPECIFY_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific feature when not using Git branches.<br/>**Must be set in the context of the agent you're working with prior to using `/speckit.plan` or follow-up commands. |

## 🎭 Orchestrator Workflow

### Overview

The **Orchestrator** workflow simplifies the entire spec-driven development process by managing all phases automatically. Instead of manually invoking each command (constitution → specify → clarify → plan → tasks → analyze → implement), you can run the entire workflow with a single command.

### Why Use the Orchestrator?

**Manual Workflow:** 7 separate commands, manual state tracking, context loss at chat limits.

**Orchestrator Workflow:** `/speckit.orchestrate <feature-description>` - 1 command, automatic state management, seamless resumption.

### Key Features

#### 1. **Single Entry Point**

Run the entire workflow from feature description to implementation with one command.

#### 2. **State Persistence**

The orchestrator saves progress to `.speckit-state.json`, enabling:

- Resumption after chat token limits
- Cross-session continuity
- Progress tracking

#### 3. **Flexible Execution Modes**

```mermaid
graph LR
    subgraph Interactive["Interactive Mode"]
        I1[Constitution] -->|Ask| I2[Specify]
        I2 -->|Ask| I3[Clarify]
        I3 -->|Ask| I4[Plan]
        I4 -->|Ask| I5[Tasks]
        I5 -->|Ask| I6[Analyze]
        I6 -->|Ask| I7[Implement]
    end

    subgraph AutoSpec["Auto-Spec Mode"]
        A1[Constitution] --> A2[Specify]
        A2 --> A3[Plan]
        A3 --> A4[Tasks]
        A4 -->|PAUSE| A5[Implement]
    end

    subgraph FullAuto["Full Auto Mode"]
        F1[Constitution] --> F2[Specify]
        F2 --> F3[Plan]
        F3 --> F4[Tasks]
        F4 --> F5[Implement]
        F5 --> F6[Done]
    end

    style Interactive fill:#e3f2fd,stroke:#333,stroke-width:2px
    style AutoSpec fill:#fff9c4,stroke:#333,stroke-width:2px
    style FullAuto fill:#e8f5e9,stroke:#333,stroke-width:2px
```

**Interactive Mode** (recommended):

- Asks permission before each major phase
- Allows review and adjustment between phases
- User maintains full control

**Auto-Spec Mode**:

- Runs constitution → specify → plan → tasks automatically
- Pauses before implementation for review

**Full Auto Mode**:

- Runs entire workflow to completion
- Minimal user interaction required

#### 4. **Context Restoration with `/speckit.resume`**

Restores context after chat limit: loads all artifacts, identifies stopping point, and continues with zero duplicate work.

### Usage Examples

**Interactive Mode:**

```bash
/speckit.orchestrate Build a user authentication system with OAuth2 and JWT
```

Prompts at each phase for user confirmation and review.

**Auto-Spec Mode:**

```bash
/speckit.orchestrate --mode=auto-spec Create an analytics dashboard
```

Runs constitution → specify → plan → tasks automatically, pauses before implementation for review.

**Resume After Chat Limit:**

```bash
/speckit.resume
```

```mermaid
flowchart TD
    NewChat[New Chat Session] --> Resume[/speckit.resume]
    Resume --> LoadState[Load State]
    LoadState --> LoadArtifacts[Load All Artifacts]
    LoadArtifacts --> Constitution[Constitution]
    LoadArtifacts --> Spec[Specification]
    LoadArtifacts --> Plan[Plan & Research]
    LoadArtifacts --> Tasks[Tasks 28/47]
    Constitution --> Identify
    Spec --> Identify
    Plan --> Identify
    Tasks --> Identify[Identify Resume Point]
    Identify --> Summary[Show Summary]
    Summary --> Confirm{Resume?}
    Confirm -->|Yes| Continue[Continue Implementation]
    Confirm -->|No| Cancel[Cancel]
    Continue --> Done[Complete Tasks]

    style NewChat fill:#e8eaf6,stroke:#333,stroke-width:2px
    style Resume fill:#e1f5e1,stroke:#333,stroke-width:2px
    style LoadState fill:#fff9c4,stroke:#333,stroke-width:2px
    style LoadArtifacts fill:#e3f2fd,stroke:#333,stroke-width:2px
    style Identify fill:#fff4e6,stroke:#333,stroke-width:2px
    style Summary fill:#e8f5e9,stroke:#333,stroke-width:2px
    style Continue fill:#c8e6c9,stroke:#333,stroke-width:2px
    style Done fill:#a5d6a7,stroke:#333,stroke-width:2px
```

Loads state, shows progress (e.g., 28/47 tasks), identifies next task, and continues from exact stopping point.

### State Management

The orchestrator creates `.speckit-state.json` in your repository root:

```json
{
  "version": "1.0",
  "feature_number": "001",
  "feature_name": "user-auth",
  "feature_dir": "specs/001-user-auth",
  "current_phase": "implement",
  "completed_phases": ["constitution", "specify", "plan", "tasks"],
  "workflow_mode": "interactive",
  "started_at": "2025-11-02T10:30:00Z",
  "last_updated": "2025-11-02T11:15:00Z",
  "checkpoints": {
    "implement": {
      "status": "in_progress",
      "tasks_completed": 28,
      "tasks_total": 47,
      "current_task": "[T029] Implement webhook verification"
    }
  }
}
```

**Should you commit `.speckit-state.json`?**

- ✅ **Yes** if you want cross-machine resumption or team collaboration
- ❌ **Add to .gitignore** if you prefer local-only state

### When to Use Orchestrator vs Individual Commands

- **New features:** Use `/speckit.orchestrate`
- **Multi-day workflows:** Use orchestrator + `/speckit.resume`
- **Learning:** Use individual commands
- **Re-running phases:** Use individual commands (e.g., `/speckit.plan`)
- **Token limits:** Use `/speckit.resume`

### Best Practices

- **Commit frequently** during long workflows
- **Review before implementation** using interactive or auto-spec mode
- **Commit `.speckit-state.json`** for cross-machine work
- **Use `/speckit.resume`** after token limits or errors

### Progress Visualization

**Task-Level Progress:**

```mermaid
graph TD
    subgraph US3["User Story 3: In Progress"]
        T015["T015: Auth middleware ✓"]
        T016["T016: JWT validation ⚙"]
        T017["T017: Token refresh ⏳"]
        T018["T018: Logout handler ⏳"]
        T019["T019: Rate limiting ⏳"]
        T020["T020: Tests ⏳"]

        T015 --> T016
        T016 -.-> T017
        T017 -.-> T018
        T018 -.-> T019
        T019 -.-> T020
    end

    style T015 fill:#c8e6c9,stroke:#4caf50,stroke-width:2px
    style T016 fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style T017 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px
    style T018 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px
    style T019 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px
    style T020 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px
```

**Legend:**

- ✓ = Completed
- ⚙ = In Progress (current task)
- ⏳ = Pending
- ⏭ = Skipped

### Error Handling

If any phase fails:

```text
❌ Error in phase: implement

Error details: Module 'stripe' not found

Your progress has been saved.

To resume after fixing the issue:
  /speckit.resume

To start over:
  rm .speckit-state.json
  /speckit.orchestrate <feature-description>
```

Simply fix the issue (e.g., `npm install stripe`) and run `/speckit.resume` to continue.

### Workflow Diagram

```mermaid
flowchart TD
    Start([/speckit.orchestrate]) --> Constitution
    Constitution[Constitution] -->|State saved| Specify
    Constitution -.->|If missing| CreateConst[Create constitution]
    CreateConst --> Specify
    Specify[Specify] -->|State saved| Clarify
    Clarify[Clarify] -->|State saved| Plan
    Clarify -.->|Optional| Plan
    Plan[Plan] -->|State saved| Tasks
    Tasks[Tasks] -->|State saved| Analyze
    Analyze[Analyze] -->|State saved| Implement
    Analyze -.->|Optional| Implement
    Implement[Implement] -->|State saved| Done
    Done([Done])

    State[.speckit-state.json]
    Constitution -.-> State
    Specify -.-> State
    Clarify -.-> State
    Plan -.-> State
    Tasks -.-> State
    Analyze -.-> State
    Implement -.-> State

    State -.-> Resume
    Resume[/speckit.resume]
    Resume -.-> Constitution
    Resume -.-> Specify
    Resume -.-> Clarify
    Resume -.-> Plan
    Resume -.-> Tasks
    Resume -.-> Analyze
    Resume -.-> Implement

    style Start fill:#e1f5e1,stroke:#333,stroke-width:2px
    style Done fill:#e1f5e1,stroke:#333,stroke-width:2px
    style Constitution fill:#fff4e6,stroke:#333,stroke-width:2px
    style Specify fill:#e3f2fd,stroke:#333,stroke-width:2px
    style Clarify fill:#f3e5f5,stroke:#333,stroke-width:2px
    style Plan fill:#e8f5e9,stroke:#333,stroke-width:2px
    style Tasks fill:#fff9c4,stroke:#333,stroke-width:2px
    style Analyze fill:#fce4ec,stroke:#333,stroke-width:2px
    style Implement fill:#e0f2f1,stroke:#333,stroke-width:2px
    style State fill:#fff3e0,stroke:#333,stroke-width:2px
    style Resume fill:#e8eaf6,stroke:#333,stroke-width:2px
```

### Summary

One-command execution, automatic state management, zero context loss, flexible modes, cross-session continuity, error recovery, and progress transparency.

```bash
/speckit.orchestrate <your-feature-description>
```

## 🏢 Corporate Guidelines System

Spec Kit includes a comprehensive Corporate Guidelines system that allows organizations to customize and enforce their development standards, tooling requirements, and compliance policies.

### What are Corporate Guidelines?

Corporate Guidelines enable you to specify:

- **Corporate infrastructure** - Internal scaffolding commands, package registries (Artifactory, Nexus), corporate SDKs
- **Mandatory libraries** - Required corporate packages for authentication, UI components, APIs
- **Banned libraries** - Public packages that must not be used due to security/licensing concerns
- **Security & compliance** - Authentication requirements, data classification, audit logging
- **Architecture patterns** - Folder structure, design patterns, coding standards
- **Branch naming** - Configurable branch naming conventions and Jira integration

### Implementation Phases

The Corporate Guidelines system was implemented in four phases:

#### Phase 1: Foundation ✅

**Completed Features:**

- 7 tech stack guideline templates (React, Java, .NET, Node.js, Python, Go, branching)
- Automatic tech stack detection from project files
- Multi-stack project support (e.g., React frontend + Java backend)
- Priority system: Constitution > Corporate Guidelines > Spec Kit Defaults
- Integration into all core prompts (plan, implement, analyze, tasks)
- Non-compliance handling with TODO generation

**Files Created:**

```text
.guidelines/
├── README.md                    # Guidelines documentation
├── branching-guidelines.md      # Branch naming conventions
├── reactjs-guidelines.md        # React/frontend standards
├── java-guidelines.md           # Java/Spring Boot standards
├── dotnet-guidelines.md         # .NET/C# standards
├── nodejs-guidelines.md         # Node.js/Express standards
└── python-guidelines.md         # Python/Django/Flask standards
```

#### Phase 2: Configurable Branch Naming ✅

**Completed Features:**

- JSON-based branch configuration (`branch-config.json`)
- Customizable branch patterns and prefixes
- Configurable Jira format with regex validation
- Optional Jira support for teams without ticket systems
- Backward compatibility with existing projects

**Configuration Example:**

```json
{
  "version": "1.0",
  "branch_pattern": "feature/<num>-<jira>-<shortname>",
  "branch_prefix": "feature/",
  "jira": {
    "required": true,
    "format": "C12345-7890",
    "regex": "^C[0-9]{5}-[0-9]{4}$"
  }
}
```

#### Phase 3: Multi-Stack Coordination ✅

**Completed Features:**

- Multiple tech stack detection and loading
- Stack-to-file path mapping via `stack-mapping.json`
- Contextual guideline application (frontend vs backend)
- Precedence rules for overlapping guidelines
- Token usage optimization

**Path Mapping Example:**

```json
{
  "stacks": [
    {
      "name": "reactjs",
      "paths": ["frontend/**", "client/**"],
      "extensions": [".tsx", ".jsx"]
    },
    {
      "name": "java",
      "paths": ["backend/**", "server/**"],
      "extensions": [".java"]
    }
  ]
}
```

#### Phase 4: Advanced Features ✅

**New Tools:**

| Tool | Script | Purpose |
|------|--------|---------|
| **Compliance Checker** | `check-guidelines-compliance.sh` | Validate project against guidelines with severity levels (CRITICAL/HIGH/MEDIUM/LOW) |
| **Diff Tool** | `diff-guidelines.sh` | Compare project guidelines vs templates, identify outdated sections |
| **Auto-Fix Tool** | `autofix-guidelines.sh` | Automatically fix common violations (security, structure, config) |
| **Analytics Dashboard** | `guidelines-analytics.sh` | Track compliance metrics, generate trends, visualize scores |
| **CI/CD Integration** | `.guidelines/examples/ci-cd/` | GitHub Actions, GitLab CI, Jenkins pipeline examples |

### Using Guidelines Tools

**Check Compliance:**

```bash
./scripts/bash/check-guidelines-compliance.sh [--strict] [--output=json]
```

**Compare Guidelines:**

```bash
./scripts/bash/diff-guidelines.sh [--stack=reactjs] [--all]
```

**Auto-Fix Violations:**

```bash
./scripts/bash/autofix-guidelines.sh [--dry-run] [--fixes=security|structure|config]
```

Fixes: `.env` in `.gitignore`, `.env.example`, `.npmrc`, architecture folders, docs.

**Analytics Dashboard:**

```bash
./scripts/bash/guidelines-analytics.sh [--save-history] [--output=json|csv]
```

Shows compliance score (0-100), violations, historical trends, and recommendations.

**CI/CD Integration:**

```bash
# Copy templates to your project
cp .guidelines/examples/ci-cd/github-actions.yml .github/workflows/
cp .guidelines/examples/ci-cd/gitlab-ci.yml .gitlab-ci.yml
cp .guidelines/examples/ci-cd/Jenkinsfile Jenkinsfile
```

Features: automated checks, merge blocking, auto-fix, trending, notifications.

### Guidelines Hierarchy

When making decisions, AI prompts follow this priority order:

```mermaid
graph TD
    A[Constitution] -->|HIGHEST| B{Guidelines?}
    B -->|Yes| C[Corporate Guidelines]
    B -->|No| D[Spec Kit Defaults]
    C -->|MEDIUM| E[Final Decision]
    D -->|LOWEST| E

    style A fill:#ff9999,stroke:#333,stroke-width:2px
    style C fill:#ffff99,stroke:#333,stroke-width:2px
    style D fill:#99ff99,stroke:#333,stroke-width:2px
    style E fill:#99ccff,stroke:#333,stroke-width:2px
```

**Example:** If constitution says "MUST use PostgreSQL" but guidelines suggest MySQL, constitution wins.

### Quick Start

1. Customize guidelines: Edit `.guidelines/*.md` files
2. Configure branch naming: Edit `.guidelines/branch-config.json` (optional)
3. Check compliance: `./scripts/bash/check-guidelines-compliance.sh`
4. Auto-fix issues: `./scripts/bash/autofix-guidelines.sh`
5. Set up CI/CD: Copy templates from `.guidelines/examples/ci-cd/`

### Documentation

See `.guidelines/README.md`, `GUIDELINES-IMPLEMENTATION-PLAN.md`, `IMPROVEMENTS.md`, and `.guidelines/examples/ci-cd/` for details.

---

## 📚 Core Philosophy

Spec-Driven Development is a structured process that emphasizes:

- **Intent-driven development** where specifications define the "*what*" before the "*how*"
- **Rich specification creation** using guardrails and organizational principles
- **Multi-step refinement** rather than one-shot code generation from prompts
- **Heavy reliance** on advanced AI model capabilities for specification interpretation

## 🌟 Development Phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **0-to-1 Development** ("Greenfield") | Generate from scratch | <ul><li>Start with high-level requirements</li><li>Generate specifications</li><li>Plan implementation steps</li><li>Build production-ready applications</li></ul> |
| **Creative Exploration** | Parallel implementations | <ul><li>Explore diverse solutions</li><li>Support multiple technology stacks & architectures</li><li>Experiment with UX patterns</li></ul> |
| **Iterative Enhancement** ("Brownfield") | Brownfield modernization | <ul><li>Add features iteratively</li><li>Modernize legacy systems</li><li>Adapt processes</li></ul> |

## 🎯 Experimental Goals

Our research and experimentation focus on:

### Technology independence

- Create applications using diverse technology stacks
- Validate the hypothesis that Spec-Driven Development is a process not tied to specific technologies, programming languages, or frameworks

### Enterprise constraints

- Demonstrate mission-critical application development
- Incorporate organizational constraints (cloud providers, tech stacks, engineering practices)
- Support enterprise design systems and compliance requirements

### User-centric development

- Build applications for different user cohorts and preferences
- Support various development approaches (from vibe-coding to AI-native development)

### Creative & iterative processes

- Validate the concept of parallel implementation exploration
- Provide robust iterative feature development workflows
- Extend processes to handle upgrades and modernization tasks

## 🔧 Prerequisites

- **Linux/macOS/Windows**
- [Supported](#-supported-ai-agents) AI coding agent.
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

If you encounter issues with an agent, please open an issue so we can refine the integration.

## 📖 Learn More

- **[Complete Spec-Driven Development Methodology](./spec-driven.md)** - Deep dive into the full process
- **[Detailed Walkthrough](#-detailed-process)** - Step-by-step implementation guide

---

## 📋 Detailed Process

<details>
<summary>Click to expand the detailed step-by-step walkthrough</summary>

You can use the Specify CLI to bootstrap your project, which will bring in the required artifacts in your environment. Run:

```bash
specify init <project_name>
```

Or initialize in the current directory:

```bash
specify init .
# or use the --here flag
specify init --here
# Skip confirmation when the directory already has files
specify init . --force
# or
specify init --here --force
```

![Specify CLI bootstrapping a new project in the terminal](./media/specify_cli.gif)

You will be prompted to select the AI agent you are using. You can also proactively specify it directly in the terminal:

```bash
specify init <project_name> --ai claude
specify init <project_name> --ai gemini
specify init <project_name> --ai copilot

# Or in current directory:
specify init . --ai claude
specify init . --ai codex

# or use --here flag
specify init --here --ai claude
specify init --here --ai codex

# Force merge into a non-empty current directory
specify init . --force --ai claude

# or
specify init --here --force --ai claude
```

The CLI will check if you have Claude Code, Gemini CLI, Cursor CLI, Qwen CLI, opencode, Codex CLI, or Amazon Q Developer CLI installed. If you do not, or you prefer to get the templates without checking for the right tools, use `--ignore-agent-tools` with your command:

```bash
specify init <project_name> --ai claude --ignore-agent-tools
```

### **STEP 1:** Establish project principles

Go to the project folder and run your AI agent. In our example, we're using `claude`.

![Bootstrapping Claude Code environment](./media/bootstrap-claude-code.gif)

You will know that things are configured correctly if you see the `/speckit.constitution`, `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement` commands available.

The first step should be establishing your project's governing principles using the `/speckit.constitution` command. This helps ensure consistent decision-making throughout all subsequent development phases:

```text
/speckit.constitution Create principles focused on code quality, testing standards, user experience consistency, and performance requirements. Include governance for how these principles should guide technical decisions and implementation choices.
```

This step creates or updates the `.specify/memory/constitution.md` file with your project's foundational guidelines that the AI agent will reference during specification, planning, and implementation phases.

### **STEP 2:** Create project specifications

With your project principles established, you can now create the functional specifications. Use the `/speckit.specify` command and then provide the concrete requirements for the project you want to develop.

>[!IMPORTANT]
>Be as explicit as possible about *what* you are trying to build and *why*. **Do not focus on the tech stack at this point**.

An example prompt:

```text
Develop Taskify, a team productivity platform. It should allow users to create projects, add team members,
assign tasks, comment and move tasks between boards in Kanban style. In this initial phase for this feature,
let's call it "Create Taskify," let's have multiple users but the users will be declared ahead of time, predefined.
I want five users in two different categories, one product manager and four engineers. Let's create three
different sample projects. Let's have the standard Kanban columns for the status of each task, such as "To Do,"
"In Progress," "In Review," and "Done." There will be no login for this application as this is just the very
first testing thing to ensure that our basic features are set up. For each task in the UI for a task card,
you should be able to change the current status of the task between the different columns in the Kanban work board.
You should be able to leave an unlimited number of comments for a particular card. You should be able to, from that task
card, assign one of the valid users. When you first launch Taskify, it's going to give you a list of the five users to pick
from. There will be no password required. When you click on a user, you go into the main view, which displays the list of
projects. When you click on a project, you open the Kanban board for that project. You're going to see the columns.
You'll be able to drag and drop cards back and forth between different columns. You will see any cards that are
assigned to you, the currently logged in user, in a different color from all the other ones, so you can quickly
see yours. You can edit any comments that you make, but you can't edit comments that other people made. You can
delete any comments that you made, but you can't delete comments anybody else made.
```

After this prompt is entered, you should see Claude Code kick off the planning and spec drafting process. Claude Code will also trigger some of the built-in scripts to set up the repository.

Once this step is completed, you should have a new branch created (e.g., `001-create-taskify`), as well as a new specification in the `specs/001-create-taskify` directory.

The produced specification should contain a set of user stories and functional requirements, as defined in the template.

At this stage, your project folder contents should resemble the following:

```text
└── .specify
    ├── memory
    │  └── constitution.md
    ├── scripts
    │  ├── check-prerequisites.sh
    │  ├── common.sh
    │  ├── create-new-feature.sh
    │  ├── setup-plan.sh
    │  └── update-claude-md.sh
    ├── specs
    │  └── 001-create-taskify
    │      └── spec.md
    └── templates
        ├── plan-template.md
        ├── spec-template.md
        └── tasks-template.md
```

### **STEP 3:** Functional specification clarification (required before planning)

With the baseline specification created, you can go ahead and clarify any of the requirements that were not captured properly within the first shot attempt.

You should run the structured clarification workflow **before** creating a technical plan to reduce rework downstream.

Preferred order:

1. Use `/speckit.clarify` (structured) – sequential, coverage-based questioning that records answers in a Clarifications section.
2. Optionally follow up with ad-hoc free-form refinement if something still feels vague.

If you intentionally want to skip clarification (e.g., spike or exploratory prototype), explicitly state that so the agent doesn't block on missing clarifications.

Example free-form refinement prompt (after `/speckit.clarify` if still needed):

```text
For each sample project or project that you create there should be a variable number of tasks between 5 and 15
tasks for each one randomly distributed into different states of completion. Make sure that there's at least
one task in each stage of completion.
```

You should also ask Claude Code to validate the **Review & Acceptance Checklist**, checking off the things that are validated/pass the requirements, and leave the ones that are not unchecked. The following prompt can be used:

```text
Read the review and acceptance checklist, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not.
```

It's important to use the interaction with Claude Code as an opportunity to clarify and ask questions around the specification - **do not treat its first attempt as final**.

### **STEP 4:** Generate a plan

You can now be specific about the tech stack and other technical requirements. You can use the `/speckit.plan` command that is built into the project template with a prompt like this:

```text
We are going to generate this using .NET Aspire, using Postgres as the database. The frontend should use
Blazor server with drag-and-drop task boards, real-time updates. There should be a REST API created with a projects API,
tasks API, and a notifications API.
```

The output of this step will include a number of implementation detail documents, with your directory tree resembling this:

```text
.
├── CLAUDE.md
├── memory
│  └── constitution.md
├── scripts
│  ├── check-prerequisites.sh
│  ├── common.sh
│  ├── create-new-feature.sh
│  ├── setup-plan.sh
│  └── update-claude-md.sh
├── specs
│  └── 001-create-taskify
│      ├── contracts
│      │  ├── api-spec.json
│      │  └── signalr-spec.md
│      ├── data-model.md
│      ├── plan.md
│      ├── quickstart.md
│      ├── research.md
│      └── spec.md
└── templates
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

Check the `research.md` document to ensure that the right tech stack is used, based on your instructions. You can ask Claude Code to refine it if any of the components stand out, or even have it check the locally-installed version of the platform/framework you want to use (e.g., .NET).

Additionally, you might want to ask Claude Code to research details about the chosen tech stack if it's something that is rapidly changing (e.g., .NET Aspire, JS frameworks), with a prompt like this:

```text
I want you to go through the implementation plan and implementation details, looking for areas that could
benefit from additional research as .NET Aspire is a rapidly changing library. For those areas that you identify that
require further research, I want you to update the research document with additional details about the specific
versions that we are going to be using in this Taskify application and spawn parallel research tasks to clarify
any details using research from the web.
```

During this process, you might find that Claude Code gets stuck researching the wrong thing - you can help nudge it in the right direction with a prompt like this:

```text
I think we need to break this down into a series of steps. First, identify a list of tasks
that you would need to do during implementation that you're not sure of or would benefit
from further research. Write down a list of those tasks. And then for each one of these tasks,
I want you to spin up a separate research task so that the net results is we are researching
all of those very specific tasks in parallel. What I saw you doing was it looks like you were
researching .NET Aspire in general and I don't think that's gonna do much for us in this case.
That's way too untargeted research. The research needs to help you solve a specific targeted question.
```

>[!NOTE]
>Claude Code might be over-eager and add components that you did not ask for. Ask it to clarify the rationale and the source of the change.

### **STEP 5:** Have Claude Code validate the plan

With the plan in place, you should have Claude Code run through it to make sure that there are no missing pieces. You can use a prompt like this:

```text
Now I want you to go and audit the implementation plan and the implementation detail files.
Read through it with an eye on determining whether or not there is a sequence of tasks that you need
to be doing that are obvious from reading this. Because I don't know if there's enough here. For example,
when I look at the core implementation, it would be useful to reference the appropriate places in the implementation
details where it can find the information as it walks through each step in the core implementation or in the refinement.
```

This helps refine the implementation plan and helps you avoid potential blind spots that Claude Code missed in its planning cycle. Once the initial refinement pass is complete, ask Claude Code to go through the checklist once more before you can get to the implementation.

You can also ask Claude Code (if you have the [GitHub CLI](https://docs.github.com/en/github-cli/github-cli) installed) to go ahead and create a pull request from your current branch to `main` with a detailed description, to make sure that the effort is properly tracked.

>[!NOTE]
>Before you have the agent implement it, it's also worth prompting Claude Code to cross-check the details to see if there are any over-engineered pieces (remember - it can be over-eager). If over-engineered components or decisions exist, you can ask Claude Code to resolve them. Ensure that Claude Code follows the [constitution](base/memory/constitution.md) as the foundational piece that it must adhere to when establishing the plan.

### **STEP 6:** Generate task breakdown with /speckit.tasks

With the implementation plan validated, you can now break down the plan into specific, actionable tasks that can be executed in the correct order. Use the `/speckit.tasks` command to automatically generate a detailed task breakdown from your implementation plan:

```text
/speckit.tasks
```

This step creates a `tasks.md` file in your feature specification directory that contains:

- **Task breakdown organized by user story** - Each user story becomes a separate implementation phase with its own set of tasks
- **Dependency management** - Tasks are ordered to respect dependencies between components (e.g., models before services, services before endpoints)
- **Parallel execution markers** - Tasks that can run in parallel are marked with `[P]` to optimize development workflow
- **File path specifications** - Each task includes the exact file paths where implementation should occur
- **Test-driven development structure** - If tests are requested, test tasks are included and ordered to be written before implementation
- **Checkpoint validation** - Each user story phase includes checkpoints to validate independent functionality

The generated tasks.md provides a clear roadmap for the `/speckit.implement` command, ensuring systematic implementation that maintains code quality and allows for incremental delivery of user stories.

### **STEP 7:** Implementation

Once ready, use the `/speckit.implement` command to execute your implementation plan:

```text
/speckit.implement
```

The `/speckit.implement` command will:

- Validate that all prerequisites are in place (constitution, spec, plan, and tasks)
- Parse the task breakdown from `tasks.md`
- Execute tasks in the correct order, respecting dependencies and parallel execution markers
- Follow the TDD approach defined in your task plan
- Provide progress updates and handle errors appropriately

>[!IMPORTANT]
>The AI agent will execute local CLI commands (such as `dotnet`, `npm`, etc.) - make sure you have the required tools installed on your machine.

Once the implementation is complete, test the application and resolve any runtime errors that may not be visible in CLI logs (e.g., browser console errors). You can copy and paste such errors back to your AI agent for resolution.

</details>

---

## 🔍 Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```

## 👥 Maintainers

- Den Delimarsky ([@localden](https://github.com/localden))
- John Lam ([@jflam](https://github.com/jflam))

## 💬 Support

For support, please open a [GitHub issue](https://github.com/veerabhadra-ponna/spec-kit-smart/issues/new). We welcome bug reports, feature requests, and questions about using Spec-Driven Development.

## 🙏 Acknowledgements

This project is heavily influenced by and based on the work and research of [John Lam](https://github.com/jflam).

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.
