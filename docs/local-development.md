# Local Development Guide

This guide shows how to iterate on the `speckitadv` CLI locally without publishing a release or committing to `main` first.

> The toolkit uses the `speckitadv` Python CLI for all workflow operations. No bash or PowerShell scripts required.

## 1. Clone and Switch Branches

```bash
git clone https://github.com/veerabhadra-ponna/spec-kit-smart.git
cd spec-kit-smart
# Work on a feature branch
git checkout -b your-feature-branch
```

## 2. Run the CLI Directly (Fastest Feedback)

You can execute the CLI directly without installing, using either method:

Both methods require PYTHONPATH to resolve imports:

```bash
# From repo root - set PYTHONPATH first
PYTHONPATH=scripts/python python scripts/python/speckit/cli.py --help
PYTHONPATH=scripts/python python scripts/python/speckit/cli.py init demo-project --ai claude --ignore-agent-tools
```

Or use module style:

```bash
# From repo root - set PYTHONPATH first
PYTHONPATH=scripts/python python -m speckit.cli --help
PYTHONPATH=scripts/python python -m speckit.cli init demo-project --ai claude --ignore-agent-tools
```

## 3. Use Editable Install (Isolated Environment)

Create an isolated environment using `venv` so dependencies resolve exactly like end users get them:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac/Git Bash
# or .venv\Scripts\activate  # Windows PowerShell
# or .venv\Scripts\activate.bat  # Windows CMD

# Install project in editable mode
pip install -e .

# Now 'speckitadv' entrypoint is available
speckitadv --help
```

Re-running after code edits requires no reinstall because of editable mode.

## 4. Invoke with pipx Directly From Git (Current Branch)

`pipx run` can run from a local path (or a Git ref) to simulate user flows:

```bash
# Run from local repository
pipx run --spec /path/to/spec-kit-smart speckitadv init test-project

# Run from specific Git branch
pipx run --spec git+https://github.com/veerabhadra-ponna/spec-kit-smart.git@feature-branch speckitadv init test-project
```

### 4a. Absolute Path pipx (Run From Anywhere)

If you're in another directory, use an absolute path:

```bash
pipx run --spec /mnt/c/GitHub/spec-kit-smart speckitadv --help
pipx run --spec /mnt/c/GitHub/spec-kit-smart speckitadv init demo-anywhere --ai copilot --ignore-agent-tools
```

Set an environment variable for convenience:

```bash
export SPEC_KIT_SRC=/mnt/c/GitHub/spec-kit-smart
pipx run --spec "$SPEC_KIT_SRC" speckitadv init demo-env --ai copilot --ignore-agent-tools
```

(Optional) Define a shell function:

```bash
speckitadv-dev() { pipx run --spec /mnt/c/GitHub/spec-kit-smart speckitadv "$@"; }
# Then
speckitadv-dev --help
```

## 5. Testing Python CLI

After running an `init`, verify the launcher files are in place:

```bash
ls -la .specify/commands/
# Or check agent-specific directory (e.g., .claude/commands/)
```

The `speckitadv` CLI handles all operations cross-platform - no shell scripts needed.

## 6. Run Lint / Basic Checks (Add Your Own)

Currently no enforced lint config is bundled, but you can quickly sanity check importability:

```bash
# After editable install (pip install -e .)
python -c "import speckit; print('Import OK')"

# Or without install
PYTHONPATH=scripts/python python -c "import speckit; print('Import OK')"
```

## 7. Build a Wheel Locally (Optional)

Validate packaging before publishing:

```bash
pip install build
python -m build
ls dist/
```

Install the built artifact into a fresh throwaway environment if needed.

## 8. Using a Temporary Workspace

When testing `init --here` in a dirty directory, create a temp workspace:

```bash
mkdir /tmp/spec-test && cd /tmp/spec-test

# Option 1: Use absolute path to script (requires PYTHONPATH)
PYTHONPATH=/path/to/spec-kit-smart/scripts/python python /path/to/spec-kit-smart/scripts/python/speckit/cli.py init --here --ai claude --ignore-agent-tools

# Option 2: Use PYTHONPATH for module style
PYTHONPATH=/path/to/spec-kit-smart/scripts/python python -m speckit.cli init --here --ai claude --ignore-agent-tools
```

Or use pipx for a cleaner isolated test.

## 9. Debug Network / TLS Skips

If you need to bypass TLS validation while experimenting:

```bash
speckitadv check --skip-tls
speckitadv init demo --skip-tls --ai gemini --ignore-agent-tools
```

(Use only for local experimentation.)

## 10. Rapid Edit Loop Summary

| Action | Command |
| -------- | --------- |
| Run CLI directly | `PYTHONPATH=scripts/python python scripts/python/speckit/cli.py --help` |
| Editable install | `pip install -e .` then `speckitadv ...` |
| Local pipx run | `pipx run --spec /path/to/repo speckitadv ...` |
| Git branch pipx | `pipx run --spec git+URL@branch speckitadv ...` |
| Build wheel | `python -m build` |

## 11. Cleaning Up

Remove build artifacts / virtual env quickly:

```bash
rm -rf .venv dist build *.egg-info
```

## 12. Common Issues

| Symptom | Fix |
| --------- | ----- |
| `ModuleNotFoundError: typer` | Run `pip install -e .` after activating venv |
| Launcher files missing | Re-run init or check agent command directory |
| Git step skipped | You passed `--no-git` or Git not installed |
| TLS errors on corporate network | Try `--skip-tls` (not for production) |
| Chain ID mismatch error | Only the latest chain is retained. Start a new workflow or use the current chain ID shown in the error |

## 13. Next Steps

- Update docs and run through Quick Start using your modified CLI
- Open a PR when satisfied
- (Optional) Tag a release once changes land in `main`
