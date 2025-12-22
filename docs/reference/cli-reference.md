# Specify CLI Reference

The `speckitadv` CLI provides tools for initializing projects and checking prerequisites for Spec-Driven Development.

## Commands

| Command     | Description                                                    |
| ------------- | ---------------------------------------------------------------- |
| `init`      | Initialize a new Specify project from the latest template      |
| `check`     | Check for installed tools (`git`, all supported AI agents, `code`, `code-insiders`) |

## `speckitadv init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
| ------------------------ | ---------- | ------------------------------------------------------------------------------ |
| `<project-name>`       | Argument | Name for your new project directory (optional if using `--here`, or use `.` for current directory) |
| `--ai`                 | Option   | AI assistant to use: `claude`, `gemini`, `copilot`, `cursor-agent`, `qwen`, `opencode`, `codex`, `windsurf`, `kilocode`, `auggie`, `roo`, `codebuddy`, `amp`, or `q` |
| `--no-git`             | Flag     | Skip git repository initialization                                          |
| `--here`               | Flag     | Initialize project in the current directory instead of creating a new one   |
| `--force`              | Flag     | Force merge/overwrite when initializing in current directory (skip confirmation) |

## Examples

```bash
# Basic project initialization
speckitadv init my-project

# Initialize with specific AI assistant
speckitadv init my-project --ai claude

# Initialize with Cursor support
speckitadv init my-project --ai cursor-agent

# Initialize with Windsurf support
speckitadv init my-project --ai windsurf

# Initialize with Amp support
speckitadv init my-project --ai amp

# Initialize in current directory
speckitadv init . --ai copilot
# or use the --here flag
speckitadv init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
speckitadv init . --force --ai copilot
# or
speckitadv init --here --force --ai copilot

# Skip git initialization
speckitadv init my-project --ai gemini --no-git

# Check system requirements
speckitadv check
```

## Available Slash Commands

After running `speckitadv init`, your AI coding agent will have access to these slash commands for structured development:

### Orchestration Commands

**NEW**: Simplified workflow management and context restoration:

| Command                  | Description                                                           |
| -------------------------- | ----------------------------------------------------------------------- |
| `/speckitadv.orchestrate`  | **Orchestrate the complete workflow** from feature description to implementation in a single command. Manages state, phase transitions, and provides interactive or automatic execution modes. |
| `/speckitadv.resume`       | **Restore context and resume work** after chat limit or interruption. Loads all artifacts and continues from exact stopping point with zero context loss. |

**Quick Start with Orchestrator:**

```bash
# Run entire workflow in one command
/speckitadv.orchestrate Build a user authentication system with OAuth2 and JWT

# Or resume after chat limit/interruption
/speckitadv.resume
```

See [Orchestrator Workflow Guide](../workflows/orchestrator.md) for detailed usage.

### Core Commands

Essential commands for the Spec-Driven Development workflow (can be used individually or via orchestrator):

| Command                  | Description                                                           |
| -------------------------- | ----------------------------------------------------------------------- |
| `/speckitadv.constitution`  | Create or update project governing principles and development guidelines |
| `/speckitadv.specify`       | Define what you want to build (requirements and user stories)        |
| `/speckitadv.plan`          | Create technical implementation plans with your chosen tech stack     |
| `/speckitadv.tasks`         | Generate actionable task lists for implementation                     |
| `/speckitadv.implement`     | Execute all tasks to build the feature according to the plan         |

### Optional Commands

Additional commands for enhanced quality and validation:

| Command                      | Description                                                           |
| ------------------------------ | ----------------------------------------------------------------------- |
| `/speckitadv.clarify`           | Clarify underspecified areas (recommended before `/speckitadv.plan`; formerly `/quizme`) |
| `/speckitadv.analyze`           | Cross-artifact consistency & coverage analysis (run after `/speckitadv.tasks`, before `/speckitadv.implement`) |
| `/speckitadv.checklist`         | Generate custom quality checklists that validate requirements completeness, clarity, and consistency (like "unit tests for English") |
| `/speckitadv.generate-guidelines` | **NEW**: Generate or update corporate coding guidelines by analyzing corporate documents and reference codebases (EXPERIMENTAL v1.0.0-alpha) |

## Environment Variables

| Variable         | Description                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| `SPECIFY_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific feature when not using Git branches. **Must be set in the context of the agent you're working with prior to using `/speckitadv.plan` or follow-up commands.** |
| `SPEC_KIT_PLATFORM` | Force platform detection: `windows`, `unix`, or `auto` (default). Use to override automatic script selection. |
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub personal access token for API requests. Required when rate limits are reached or for private repositories. |

## Related Documentation

- [Getting Started Guide](../getting-started.md)
- [Supported AI Agents](../README.md#-supported-ai-agents)
- [Installation Options](../README.md#-get-started)
- [Troubleshooting](troubleshooting.md)
