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
speckit --version
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
speckit --help
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
speckit constitution --stage=1

# AI agent follows instructions, then runs:
speckit constitution --stage=2 --chain=<chain_id>

# Continue through stages...
speckit constitution --stage=3 --chain=<chain_id>
```

### Example: Specify Workflow

```bash
# Stage 1: Initialize and understand role
speckit specify --stage=1 --path=/path/to/project

# AI reads instructions, runs stage 2
speckit specify --stage=2 --chain=abc123

# Continue through all 6 stages
speckit specify --stage=3 --chain=abc123
# ... until complete
```

### Debug Commands

```bash
# List fragments for a command
speckit list-fragments constitution

# Show fragment content
speckit show-fragment constitution 01-initialization
```

## How It Works

1. **CLI emits stage prompt** (50-80 lines)
2. **AI agent follows instructions** in the prompt
3. **CLI provides next command** at end of each stage
4. **Chain ID persists state** between invocations
5. **Repeat until workflow complete**

## Architecture

```
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
