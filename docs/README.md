# Documentation

This folder contains the documentation source files for Spec Kit Smart.

## Structure

| File | Description |
|------|-------------|
| `index.md` | Documentation homepage |
| `getting-started.md` | Installation, setup, and first feature guide |
| `branching-strategy.md` | Git workflow patterns |
| `multi-stack-example.md` | Multi-technology stack example |
| `reverse-engineering.md` | Analyze and modernize existing codebases |
| `reference/cli-reference.md` | CLI command documentation |
| `reference/troubleshooting.md` | Common issues and solutions |
| `workflows/orchestrator.md` | Automated workflow execution |
| `spec-driven.md` | Core methodology overview (in repo root) |

## Building Locally

Documentation is built using [DocFX](https://dotnet.github.io/docfx/):

```bash
dotnet tool install -g docfx
cd docs
docfx docfx.json --serve
```

Open `http://localhost:8080` to view.

## Deployment

Documentation is automatically deployed to GitHub Pages on push to `main`.

## Historical context (formerly `docs/archived/`)

Historical planning notes previously stored in `docs/archived/` have been consolidated into the primary documentation:

- **Python CLI migration**: The Bash/PowerShell scripts were superseded by the cross-platform `speckitadv` CLI. Rationale and rollout details are summarized in [README.md](../README.md) and [docs/reference/cli-reference.md](reference/cli-reference.md).
- **State simplification**: Folder-based state (`specs/{feature}/.state/state.json` and `.analysis/{project}/state.json`) is now part of the workflow guides, replacing the earlier chain-based approach.
- **Reverse engineering review**: Findings from the pre-Python engineering review are reflected in the updated [Reverse Engineering Guide](reverse-engineering.md) and orchestrator documentation.

No historical documents remain; current guides contain the supported workflows and design choices.
