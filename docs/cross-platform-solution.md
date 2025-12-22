# Cross-Platform Solution

> **⚠️ SUPERSEDED**: This document describes the original bash/PowerShell unified package approach. As of v3.0, Spec Kit Smart uses the `speckitadv` Python CLI which eliminates the need for platform-specific scripts entirely.

## Current Architecture (v3.0+)

The `speckitadv` CLI is a **single Python executable** that works on all platforms:

- ✅ **Windows** - Works natively with Python
- ✅ **macOS** - Works natively with Python
- ✅ **Linux** - Works natively with Python
- ✅ **WSL** - Works natively with Python
- ✅ **Docker containers** - Works in any Python environment

### No OS Detection Required

The Python CLI handles cross-platform compatibility automatically:

- File path handling uses `pathlib.Path` (cross-platform)
- No bash or PowerShell scripts to select between
- No environment variables needed for platform selection

### Installation

```bash
# Works on all platforms
pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git

# Or run directly
pipx run --spec git+https://github.com/veerabhadra-ponna/spec-kit-smart.git speckitadv --help
```

### Usage

```bash
# Same commands on all platforms
speckitadv init my-project --ai claude
speckitadv check
speckitadv analyze-project --path /my/project --scope A
```

## Historical Context

Prior to v3.0, Spec Kit Smart used separate bash and PowerShell scripts, requiring:

- OS detection logic in prompts
- `SPEC_KIT_PLATFORM` environment variable for overrides
- Separate package variants for Windows vs Unix

This complexity was eliminated by migrating to a unified Python CLI.

## Related Documentation

- [Python Migration Assessment](./PYTHON-MIGRATION-ASSESSMENT.md) - Details on the Python CLI architecture
- [CLI Reference](./reference/cli-reference.md) - Full CLI documentation
- [Local Development](./local-development.md) - Development setup guide
