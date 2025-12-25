# Spec Kit Smart

*Build high-quality software faster with Spec-Driven Development.*

[![Release](https://github.com/veerabhadra-ponna/spec-kit-smart/actions/workflows/release.yml/badge.svg)](https://github.com/veerabhadra-ponna/spec-kit-smart/actions/workflows/release.yml)
[![License](https://img.shields.io/github/license/veerabhadra-ponna/spec-kit-smart)](https://github.com/veerabhadra-ponna/spec-kit-smart/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub_Pages-blue)](https://veerabhadra-ponna.github.io/spec-kit-smart/)

**[Get Started](#get-started)** | **[Reverse Engineering](#reverse-engineering)** | **[Orchestrator](#orchestrator)** | **[CLI Reference](docs/reference/cli-reference.md)** | **[Troubleshooting](docs/reference/troubleshooting.md)**

## Documentation map

- **Product overview**: This README, plus the methodology primer in [spec-driven.md](spec-driven.md)
- **Step-by-step guides**: [Getting Started](docs/getting-started.md), [Orchestrator Workflow](docs/workflows/orchestrator.md)
- **Reference**: [CLI Reference](docs/reference/cli-reference.md), [Troubleshooting](docs/reference/troubleshooting.md)
- **Design background**: Reverse engineering and state design details in [Reverse Engineering Guide](docs/reverse-engineering.md)

Historical planning notes previously kept under `docs/archived/` have been folded into the guides above so readers only need the main documentation set.

---

## Why This Fork?

Enterprise extensions to [original Spec Kit](https://github.com/github/spec-kit) for corporate teams:

| Feature | Original | This Fork |
|---------|----------|-----------|
| Platform | Bash (Unix only) | Python CLI (all platforms) |
| Workflow | Manual commands | Orchestrator + auto-resume |
| Legacy Code | Greenfield only | Reverse engineering & modernization |
| Standards | Generic | Corporate guidelines + compliance |
| Branching | Fixed | Configurable + Jira integration |

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **Reverse Engineering** | Analyze legacy codebases, extract requirements, assess tech debt, generate modernization plans with feasibility scores (0-100) |
| **Orchestrator** | `/speckitadv.orchestrate` runs entire workflow; `/speckitadv.resume` restores context after interruptions |
| **Corporate Guidelines** | `/speckitadv.generate-guidelines` extracts standards from PDFs and reference projects |
| **Cross-Cutting Concerns** | Migrate auth, database, caching, deployment without full rewrites |
| **Cross-Platform** | Single `speckitadv` binary works on Linux, macOS, Windows |

---

## Get Started

```bash
# Install
pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git

# Initialize project
speckitadv init my-project --ai claude

# Build a feature
/speckitadv.constitution Create quality-focused principles
/speckitadv.specify Build a photo album application...
/speckitadv.plan Use Vite, vanilla JS, SQLite
/speckitadv.tasks
/speckitadv.implement
```

**For complete installation options and step-by-step tutorial: [Getting Started Guide](docs/getting-started.md)**

### Workflow Commands

| Command | Purpose |
|---------|---------|
| `/speckitadv.orchestrate` | Run entire workflow in one command |
| `/speckitadv.resume` | Resume after interruption |
| `/speckitadv.constitution` | Establish project principles |
| `/speckitadv.specify` | Define requirements |
| `/speckitadv.plan` | Create technical design |
| `/speckitadv.tasks` | Generate task list |
| `/speckitadv.implement` | Execute implementation |
| `/speckitadv.clarify` | Resolve ambiguities (optional) |
| `/speckitadv.analyze` | Validate consistency (optional) |

### Choosing Your Workflow

| Scenario | Approach |
|----------|----------|
| New feature | `/speckitadv.orchestrate <description>` |
| Complex/multi-day | Orchestrator + `/speckitadv.resume` |
| Legacy modernization | `/speckitadv.analyze-project` |
| Company standards | `/speckitadv.generate-guidelines` |
| Learning | Individual commands step-by-step |

---

## Reverse Engineering

**Status**: EXPERIMENTAL (v1.0.0-alpha) - ~4,564 LOC Python + orchestration + templates

Analyze existing projects, assess technical debt, and plan modernization strategies.

```bash
/speckitadv.analyze-project
# Provide PROJECT_PATH when prompted
```

**Analysis Scopes:**

| Scope | Use Case | Output |
|-------|----------|--------|
| **[A] Full Application** | Complete modernization | analysis-report.md, functional-spec.md, technical-spec.md, stage-prompts/ |
| **[B] Cross-Cutting Concern** | Targeted migration (auth, DB, caching, deployment) | concern-analysis.md, concern-migration-plan.md |

**Full Analysis Includes:**
- Tech stack detection & EOL tracking
- Security vulnerability scanning (CVEs)
- Dependency health analysis
- Architecture assessment
- Feasibility scores (0-100) for inline/greenfield/hybrid
- Interactive 10-question modernization planning

**Cross-Cutting Concerns (9 types):**
Auth, Database, Caching, Messaging, Observability, API Gateway, Storage, Deployment, Other

**Migration Strategies:** STRANGLER_FIG, ADAPTER_PATTERN, REFACTOR_FIRST, BIG_BANG_WITH_FEATURE_FLAGS

**Complete guide: [Reverse Engineering Guide](docs/reverse-engineering.md)**

---

## Orchestrator

Single-command workflow with automatic state management and resumption.

```bash
# Run entire workflow
/speckitadv.orchestrate Build user authentication with OAuth2 and JWT

# Resume after interruption
/speckitadv.resume
```

**Features:**
- Runs constitution → specify → clarify → plan → tasks → analyze → implement
- Progress tracked in `specs/{feature}/.state/state.json`
- Zero context loss after chat token limits
- Modes: Interactive (default), Auto-Spec, Full Auto

**Complete guide: [Orchestrator Guide](docs/workflows/orchestrator.md)**

---

## Corporate Guidelines

Customize and enforce development standards, compliance policies, and tooling requirements.

```bash
/speckitadv.generate-guidelines /path/to/corporate-resources
```

**Three-Persona Analysis:**
1. **Standards Architect** - Extract principles from PDFs, policies
2. **Code Archeologist** - Reverse-engineer patterns from reference projects
3. **Technical Writer** - Synthesize into RFC 2119 guidelines (MUST/SHOULD/MAY)

**Generated:** `.guidelines/{stack}-guidelines.md` with mandatory/banned libraries, architecture patterns, security requirements

**Priority:** Constitution > Corporate Guidelines > Spec Kit Defaults

---

## Supported AI Agents

| Agent | Status |
|-------|--------|
| [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Cursor](https://cursor.sh/), [Qwen Code](https://github.com/QwenLM/qwen-code) | ✅ |
| [opencode](https://opencode.ai/), [Windsurf](https://windsurf.com/), [Kilo Code](https://github.com/Kilo-Org/kilocode), [Auggie CLI](https://docs.augmentcode.com/cli/overview), [CodeBuddy CLI](https://www.codebuddy.ai/cli) | ✅ |
| [Roo Code](https://roocode.com/), [Codex CLI](https://github.com/openai/codex), [Amp](https://ampcode.com/) | ✅ |
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ No custom args |

**CLI options:** `claude`, `gemini`, `copilot`, `cursor-agent`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, `codebuddy`, `amp`, `q`

---

## Prerequisites

- Linux/macOS/Windows
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Git ([Download](https://git-scm.com/downloads))
- [Supported AI agent](#supported-ai-agents)

---

## Video Overview

[![Spec Kit video](./media/spec-kit-video-header.jpg)](https://www.youtube.com/watch?v=a9eR1xsfvHg)

---

## Glossary

| Term | Definition |
|------|------------|
| **Constitution** | Project principles governing AI decisions (highest priority) |
| **Orchestrator** | Single-command workflow manager with auto-resume |
| **Cross-Cutting Concern** | Architectural aspect affecting multiple modules (auth, logging, caching) |
| **Blast Radius** | % of codebase affected by concern migration |
| **Strangler Fig** | Incremental migration with parallel systems |
| **Feasibility Score** | 0-100 rating for upgrade vs rewrite viability |
| **Stage Prompts** | Pre-generated prompts for workflow phases |
| **Artifact-Based State** | Progress detection from spec/plan/tasks files |

---

## Links

- [Getting Started](docs/getting-started.md)
- [CLI Reference](docs/reference/cli-reference.md)
- [Reverse Engineering](docs/reverse-engineering.md)
- [Orchestrator](docs/workflows/orchestrator.md)
- [Troubleshooting](docs/reference/troubleshooting.md)
- [Spec-Driven Methodology](./spec-driven.md)

## Maintainers

Veerabhadra Rao Ponna ([@veerabhadra-ponna](https://github.com/veerabhadra-ponna))

## License

MIT - see [LICENSE](./LICENSE)
