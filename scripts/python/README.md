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

# Stage 2: Collect inputs (interactive if no args)
speckitadv specify --stage=2

# Or provide arguments directly:
speckitadv specify --stage=2 --jira=C12345-7890 --feature="Add user auth"

# Stage 3: Create feature branch (requires --feature from stage 2)
speckitadv specify --stage=3 --feature="Add user auth" --jira=C12345-7890

# Stage 4+: Chain auto-resumes from state (--chain optional)
speckitadv specify --stage=4 --feature-dir=specs/001-user-auth
# ... until complete
```

**Notes:**

- Stages 1-2 are stateless. Pass `--feature` and `--jira` from stage 2 to stage 3.
- Stage 3 creates the feature folder and persists state.
- Stage 4+ auto-detects chain from state. Use `--chain` or `--feature-dir` to
  disambiguate when multiple features exist.

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
│   ├── prompts.py      # Prompt fragment loading + template injection
│   ├── stages.py       # Generic stage handler
│   └── ...
└── assets/             # (Embedded in EXE)
    ├── prompts/        # Stage prompts for each workflow
    └── templates/      # Reusable templates (spec, plan, tasks, etc.)
```

### Template Injection

Prompts can include templates using `{{include:template.md}}` syntax:

```markdown
**Template:**

{{include:spec-template.md}}
```

The CLI injects template content at runtime via `render_prompt()` in `core/prompts.py`.
Templates are loaded from `assets/templates/` and support:

- Nested includes (templates can include other templates)
- Variable substitution (`{variable}` or `{variable:default}`)
- Recursive rendering

### Template Copying

For deterministic file creation, prompts can use `{{copy-template:...}}` to copy
template files to the feature directory:

```markdown
{{copy-template:spec-template.md:spec.md}}
```

This copies `assets/templates/spec-template.md` to `{feature_dir}/spec.md`.
The destination filename is optional - if omitted, `-template` is stripped from
the source name (e.g., `plan-template.md` becomes `plan.md`).

This approach ensures:

- Deterministic file creation (CLI copies, not AI agent)
- Template content is not embedded in prompts (reduces prompt size)
- AI agent fills the copied template in subsequent steps

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
