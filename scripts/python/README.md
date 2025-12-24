# Spec Kit Smart - Python CLI

Zero-prompt architecture CLI for AI-powered development workflows.

## Features

- **Progressive Prompt Injection**: Small, focused prompts (50-80 lines) at each stage
- **Embedded Assets**: All prompts and templates bundled in single executable
- **Folder-Based State Management**: Simple state persistence using feature folders
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
speckitadv constitution --stage=2

# Continue through stages...
speckitadv constitution --stage=3
```

### Example: Specify Workflow

```bash
# Stage 1: Initialize and understand role
speckitadv specify --stage=1

# Stage 2: Collect inputs (interactive if no args)
speckitadv specify --stage=2

# Or provide arguments directly:
speckitadv specify --stage=2 --jira=C12345-7890 --feature="Add user auth"

# Stage 3: Create feature branch and folder
# AI calls create-feature helper to create specs/001-user-auth/
speckitadv specify --stage=3 --feature="Add user auth" --jira="C12345-7890"

# Stage 4+: CLI auto-detects stage and feature folder from state!
speckitadv specify  # Just run without args
speckitadv specify  # CLI reads state, continues at correct stage
```

**Notes:**

- Stages 1-2 are stateless. Pass `--feature` and `--jira` from stage 2 to stage 3.
- Stage 3 creates the feature folder via `create-feature` command and persists state.
- **Stage 3+ auto-detects** - CLI reads state file to determine stage and feature folder.

### Auto-Resume for Feature Commands

All feature-scoped commands (`specify`, `plan`, `tasks`, `implement`, `clarify`, `checklist`) support
automatic state detection:

- **Stage auto-detection**: CLI reads state file to determine which stage to run next.
- **Feature directory detection**: CLI auto-detects the latest feature folder in `specs/`.
- **Explicit overrides**: Use `--stage` or `--feature-dir` to override auto-detection.
- **Resume command**: Use `speckitadv resume` to see what's next.

```bash
# Example: plan workflow with auto-detection (stage 3+)
speckitadv plan --stage=1     # Early stages need explicit --stage
speckitadv plan --stage=2     # Still no state (created at stage 3)
speckitadv plan               # Stage 3+: auto-detects everything!
speckitadv plan               # Continues at correct stage

# Or specify explicitly to override
speckitadv plan --stage=2 --feature-dir=specs/001-user-auth
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
4. **Feature folder persists state** between invocations
5. **Repeat until workflow complete**

## Architecture

```text

speckit/
├── cli.py              # Typer CLI entry point
├── commands/           # Command implementations
│   ├── analyze.py      # analyze-project command
│   ├── constitution.py # constitution command
│   └── feature.py      # create-feature helper
├── core/
│   ├── emit.py         # Stage emission system
│   ├── state_v2.py     # Folder-based state management
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

**Template Search Order** (project overrides first):

1. `memory/templates/` - Project-level customizations
2. `.specify/templates/` - Project-level customizations
3. `templates/` - Repository-level templates
4. CLI embedded templates - Default fallback

Templates support:

- Nested includes (templates can include other templates)
- Variable substitution (`{variable}` or `{variable:default}`)
- Recursive rendering

### Template Copying

For deterministic file creation, prompts can use `{{copy-template:...}}` to copy
template files to the feature directory:

```markdown
{{copy-template:spec-template.md:spec.md}}
```

This copies the template to `{feature_dir}/spec.md`, searching the same override
locations as template includes. The destination filename is optional - if omitted,
`-template` is stripped from the source name (e.g., `plan-template.md` becomes
`plan.md`).

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
