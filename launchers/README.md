# Spec Kit Smart - Agent Launchers

Minimal 3-line launcher files for AI agent slash commands.

## How It Works

These launchers invoke the `speckitadv` CLI to execute progressive prompt workflows.
The CLI embeds all prompts and templates - agents just receive focused stage instructions.

## Usage

1. Copy the appropriate directory to your project:
   - Claude: Copy `claude/` to `.claude/commands/`
   - Copilot: Copy `copilot/` to `.github/prompts/`
   - Gemini: Copy `gemini/` to `.gemini/commands/`
   - (etc.)

2. Ensure `speckitadv` is in your PATH or use full path in launchers.

3. Use slash commands: `/analyze-project`, `/constitution`, `/specify`, etc.

## Available Commands

| Command | Stages | Description |
|---------|--------|-------------|
| `analyze-project` | 9+ | Analyze existing project for modernization |
| `constitution` | 3 | Create project constitution |
| `specify` | 6 | Create baseline specification |
| `plan` | 4 | Create implementation plan |
| `tasks` | 4 | Generate actionable tasks |
| `implement` | 5 | Execute implementation |
| `clarify` | 3 | Ask structured questions |
| `checklist` | 3 | Generate quality checklist |

## Agent Directories

| Agent | Directory | Format |
|-------|-----------|--------|
| Claude Code | `.claude/commands/` | Markdown |
| GitHub Copilot | `.github/prompts/` | Markdown |
| Gemini CLI | `.gemini/commands/` | TOML |
| Cursor | `.cursor/commands/` | Markdown |
| Qwen Code | `.qwen/commands/` | TOML |
| opencode | `.opencode/command/` | Markdown |
| Codex CLI | `.codex/commands/` | Markdown |
| Windsurf | `.windsurf/workflows/` | Markdown |
| Kilo Code | `.kilocode/rules/` | Markdown |
| Auggie CLI | `.augment/rules/` | Markdown |
| CodeBuddy | `.codebuddy/commands/` | Markdown |
| Roo Code | `.roo/rules/` | Markdown |
| Amazon Q | `.amazonq/prompts/` | Markdown |
| Amp | `.agents/commands/` | Markdown |
