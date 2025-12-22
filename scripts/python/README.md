# Spec Kit Smart - Python CLI

Zero-prompt architecture CLI for AI-powered development workflows.

## Features

- **Progressive Prompt Injection**: Small, focused prompts (50-80 lines) at each stage
- **Embedded Assets**: All prompts and templates bundled in single executable
- **Chain State Management**: Persist workflow state between sessions
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Installation

### From Source (Development)

```bash
cd scripts/python
pip install -e .
speckitadv --version
```

### Build Executable

```bash
cd scripts/python
pip install pyinstaller
pyinstaller speckit.spec
./dist/speckitadv --version
```

## Usage

### List Available Commands

```bash
speckitadv --help
```

### Available Commands

| Command | Description | Stages |
|---------|-------------|--------|
| `constitution` | Create project constitution | 3 |
| `specify` | Create baseline specification | 6 |
| `plan` | Create implementation plan | 4 |
| `tasks` | Generate actionable tasks | 4 |
| `implement` | Execute implementation | 5 |
| `clarify` | Ask structured questions | 3 |
| `checklist` | Generate quality checklist | 3 |
| `analyze-project` | Analyze existing project | 9+ |

### Basic Workflow

```bash
# Start constitution workflow
speckitadv constitution --stage=1

# AI agent follows instructions, then runs:
speckitadv constitution --stage=2 --chain=<chain_id>

# Continue through stages...
speckitadv constitution --stage=3 --chain=<chain_id>
```

### Example: Specify Workflow

```bash
# Stage 1: Initialize and understand role
speckitadv specify --stage=1 --path=/path/to/project

# AI reads instructions, runs stage 2 (interactive if no args)
speckitadv specify --stage=2 --chain=abc123

# Or provide arguments directly:
speckitadv specify --stage=2 --chain=abc123 --jira=C12345-7890 --feature="Add user auth"

# Continue through all 6 stages
speckitadv specify --stage=3 --chain=abc123
# ... until complete
```

### Interactive Mode Options

Commands support optional arguments that enable interactive prompts when not provided:

| Command | Option | Description |
|---------|--------|-------------|
| `specify` | `--jira`, `--feature` | JIRA number and feature description |
| `plan` | `--constraints` | Planning constraints (tech, architecture, etc.) |
| `tasks` | `--preferences` | Task generation preferences |
| `implement` | `--notes` | Implementation notes and priorities |
| `constitution` | `--defaults`, `--principles` | Use default or custom principles |
| `analyze-project` | `--path`, `--scope`, `--context` | Project path and analysis scope |

When these options are omitted at the appropriate stage, the CLI prompts interactively:

```bash
# Interactive mode - prompts for JIRA and feature
speckitadv specify --stage=2 --chain=abc123

# Non-interactive - uses provided values
speckitadv specify --stage=2 --chain=abc123 --jira=C12345-7890 --feature="OAuth2"
```

### Debug Commands

```bash
# List fragments for a command
speckitadv list-fragments constitution

# Show fragment content
speckitadv show-fragment constitution 01-initialization
```

## How It Works

1. **CLI emits stage prompt** (50-80 lines)
2. **AI agent follows instructions** in the prompt
3. **CLI provides next command** at end of each stage
4. **Chain ID persists state** between invocations
5. **Repeat until workflow complete**

## Architecture

```text

speckit/
├── cli.py              # Typer CLI entry point
├── commands/           # Command implementations
│   ├── analyze.py      # analyze-project command
│   └── constitution.py # constitution command
├── core/
│   ├── emit.py         # Stage emission system
│   ├── state.py        # Chain state management
│   ├── prompts.py      # Prompt fragment loading
│   ├── stages.py       # Generic stage handler
│   └── ...
└── assets/             # (Embedded in EXE)
```

## Building for Distribution

```bash
# Build single-file executable
pyinstaller speckit.spec

# Output: dist/speckitadv (15MB)
```

The executable includes all prompts and templates embedded via PyInstaller.

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
pytest

# Test a command
python -m speckit specify --stage=1
```
