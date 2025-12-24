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
| `development/` | Historical development docs |
| `archived/` | Completed planning documents |

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
