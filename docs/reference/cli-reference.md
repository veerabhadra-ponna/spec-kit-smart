# Specify CLI Reference

The `specify` command (`speckitsmart`) provides tools for initializing projects and checking prerequisites for Spec-Driven Development.

## Commands

| Command     | Description                                                    |
| ------------- | ---------------------------------------------------------------- |
| `init`      | Initialize a new Specify project from the latest template      |
| `check`     | Check for installed tools (`git`, `claude`, `gemini`, `code`/`code-insiders`, `cursor-agent`, `windsurf`, `qwen`, `opencode`, `codex`) |

## `speckitsmart init` Arguments & Options

| Argument/Option        | Type     | Description                                                                  |
| ------------------------ | ---------- | ------------------------------------------------------------------------------ |
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

## Examples

```bash
# Basic project initialization
speckitsmart init my-project

# Initialize with specific AI assistant
speckitsmart init my-project --ai claude

# Initialize with Cursor support
speckitsmart init my-project --ai cursor-agent

# Initialize with Windsurf support
speckitsmart init my-project --ai windsurf

# Initialize with Amp support
speckitsmart init my-project --ai amp

# Initialize with PowerShell scripts (Windows/cross-platform)
speckitsmart init my-project --ai copilot --script ps

# Initialize in current directory
speckitsmart init . --ai copilot
# or use the --here flag
speckitsmart init --here --ai copilot

# Force merge into current (non-empty) directory without confirmation
speckitsmart init . --force --ai copilot
# or
speckitsmart init --here --force --ai copilot

# Skip git initialization
speckitsmart init my-project --ai gemini --no-git

# Enable debug output for troubleshooting
speckitsmart init my-project --ai claude --debug

# Use GitHub token for API requests (helpful for corporate environments)
speckitsmart init my-project --ai claude --github-token ghp_your_token_here

# Check system requirements
speckitsmart check
```

## Available Slash Commands

After running `speckitsmart init`, your AI coding agent will have access to these slash commands for structured development:

### Orchestration Commands

**NEW**: Simplified workflow management and context restoration:

| Command                  | Description                                                           |
| -------------------------- | ----------------------------------------------------------------------- |
| `/speckitsmart.orchestrate`  | **Orchestrate the complete workflow** from feature description to implementation in a single command. Manages state, phase transitions, and provides interactive or automatic execution modes. |
| `/speckitsmart.resume`       | **Restore context and resume work** after chat limit or interruption. Loads all artifacts and continues from exact stopping point with zero context loss. |

**Quick Start with Orchestrator:**

```bash
# Run entire workflow in one command
/speckitsmart.orchestrate Build a user authentication system with OAuth2 and JWT

# Or resume after chat limit/interruption
/speckitsmart.resume
```

See [Orchestrator Workflow Guide](../workflows/orchestrator.md) for detailed usage.

### Core Commands

Essential commands for the Spec-Driven Development workflow (can be used individually or via orchestrator):

| Command                  | Description                                                           |
| -------------------------- | ----------------------------------------------------------------------- |
| `/speckitsmart.constitution`  | Create or update project governing principles and development guidelines |
| `/speckitsmart.specify`       | Define what you want to build (requirements and user stories)        |
| `/speckitsmart.plan`          | Create technical implementation plans with your chosen tech stack     |
| `/speckitsmart.tasks`         | Generate actionable task lists for implementation                     |
| `/speckitsmart.implement`     | Execute all tasks to build the feature according to the plan         |

### Optional Commands

Additional commands for enhanced quality and validation:

| Command                      | Description                                                           |
| ------------------------------ | ----------------------------------------------------------------------- |
| `/speckitsmart.clarify`           | Clarify underspecified areas (recommended before `/speckitsmart.plan`; formerly `/quizme`) |
| `/speckitsmart.analyze`           | Cross-artifact consistency & coverage analysis (run after `/speckitsmart.tasks`, before `/speckitsmart.implement`) |
| `/speckitsmart.checklist`         | Generate custom quality checklists that validate requirements completeness, clarity, and consistency (like "unit tests for English") |
| `/speckitsmart.generate-guidelines` | **NEW**: Generate or update corporate coding guidelines by analyzing corporate documents and reference codebases (EXPERIMENTAL v1.0.0-alpha) |

## Environment Variables

| Variable         | Description                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| `SPECIFY_FEATURE` | Override feature detection for non-Git repositories. Set to the feature directory name (e.g., `001-photo-albums`) to work on a specific feature when not using Git branches. **Must be set in the context of the agent you're working with prior to using `/speckitsmart.plan` or follow-up commands.** |
| `SPEC_KIT_PLATFORM` | Force platform detection: `windows`, `unix`, or `auto` (default). Use to override automatic script selection. |
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub personal access token for API requests. Required when rate limits are reached or for private repositories. |

## Related Documentation

- [Getting Started Guide](../getting-started.md)
- [Supported AI Agents](../README.md#-supported-ai-agents)
- [Installation Options](../README.md#-get-started)
- [Troubleshooting](troubleshooting.md)
