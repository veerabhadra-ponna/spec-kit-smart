# Spec Kit Smart - Enterprise Migration Guide

**Date:** 2025-11-11
**Purpose:** Document all changes needed to remove UV dependency, customize branding, and simplify user experience for enterprise environments

---

## Overview of Changes

This document outlines all changes needed to:
1. ✅ Replace UV with pip/pipx for enterprise compatibility
2. ✅ Customize ASCII banner for Spec Kit Smart branding
3. ✅ Remove script type selection (auto-detection only)
4. ✅ Ensure all files (.guidelines, scripts/bash, scripts/powershell) are copied to repo root
5. ✅ Fix package download pattern to work with unified packages

---

## 1. Change Installation from UV to pip/pipx

### Files to Modify:

#### A. `README.md`

**Lines 164-194: Installation section**

**Current:**
```markdown
#### Option 1: Persistent Installation (Recommended)
```bash
uv tool install specify-cli --from git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
```

#### Option 2: One-time Usage
```bash
uvx --from git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME>
```

**Benefits of persistent installation:**
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
```

**Change to:**
```markdown
#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
# From public GitHub
pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git

# From GitHub Enterprise (for corporate environments)
pipx install git+https://github.company.com/yourorg/spec-kit-smart.git
```

Then use the tool directly:

```bash
specify init <PROJECT_NAME>
specify check
```

To upgrade specify run:

```bash
pipx install --force git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
# From public GitHub
pipx run --spec git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME>

# From GitHub Enterprise
pipx run --spec git+https://github.company.com/yourorg/spec-kit-smart.git specify init <PROJECT_NAME>
```

#### Option 3: From Corporate Artifactory (Enterprise)

If your company uses Artifactory PyPI mirror:

```bash
# One-time configuration (usually done by IT)
pip config set global.index-url https://artifactory.company.com/artifactory/api/pypi/pypi-virtual/simple

# Install
pip install specify-cli
```

**Benefits of persistent installation:**
- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `pipx list`, `pipx upgrade`, `pipx uninstall`
- Cleaner shell configuration
- Works in corporate environments without UV approval
```

#### B. `CONTRIBUTING.md`

**Lines 34-35: Developer setup**

**Current:**
```bash
uv sync
uv run specify --help
```

**Change to:**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install in editable mode
pip install -e .

# Test the CLI
specify --help
```

**Lines 62-63: Testing template changes locally**

**Current:**
```markdown
Running `uv run specify init` pulls released packages, which won't include your local changes.
```

**Change to:**
```markdown
Running `specify init` after installing with `pip install -e .` pulls released packages, which won't include your local changes.
```

#### C. `docs/local-development.md`

**Lines 34-49: Environment setup**

**Current:**
```bash
# Create & activate virtual env (uv auto-manages .venv)
uv venv
source .venv/bin/activate

# Install project in editable mode
uv pip install -e .

# Now 'specify' entrypoint is available
specify --help
```

**Change to:**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac/Git Bash
# or .venv\Scripts\activate  # Windows PowerShell
# or .venv\Scripts\activate.bat  # Windows CMD

# Install project in editable mode
pip install -e .

# Now 'specify' entrypoint is available
specify --help
```

**Lines 50-53: Direct invocation**

**Current:**
```markdown
## 4. Invoke with uvx Directly From Git (Current Branch)

`uvx` can run from a local path (or a Git ref) to simulate user flows:
```

**Change to:**
```markdown
## 4. Invoke with pipx Directly From Git (Current Branch)

`pipx run` can run from a local path (or a Git ref) to simulate user flows:

```bash
# Run from local repository
pipx run --spec /path/to/spec-kit-smart specify init test-project

# Run from specific Git branch
pipx run --spec git+https://github.com/veerabhadra-ponna/spec-kit-smart.git@feature-branch specify init test-project
```
```

#### D. `docs/quickstart.md`

**Lines 14-22: Quick start commands**

**Current:**
```bash
uvx --from git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME>

# Pick script type explicitly (optional):
uvx --from git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME> --script ps  # Force PowerShell
uvx --from git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME> --script sh  # Force POSIX shell
```

**Change to:**
```bash
pipx run --spec git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME>

# Script type is auto-detected based on OS (Windows → PowerShell, Linux/Mac → Bash)
# Optional: Force specific script type
pipx run --spec git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME> --script ps  # Force PowerShell
pipx run --spec git+https://github.com/veerabhadra-ponna/spec-kit-smart.git specify init <PROJECT_NAME> --script sh  # Force Bash
```

#### E. `.devcontainer/post-create.sh`

**Lines 86-89: Remove UV installation**

**Current:**
```bash
# Installing UV (Python package manager)
echo -e "\n🐍 Installing UV - Python Package Manager..."
run_command "pipx install uv"
echo "✅ Done"
```

**Change to:**
```bash
# UV is not needed - pip/pipx are sufficient and already installed
# Removed to avoid corporate approval issues
```

#### F. `src/specify_cli/__init__.py` (Documentation in docstrings)

**Lines 13-24: Module docstring examples**

**Current:**
```python
"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init .
    specify init --here
"""
```

**Change to:**
```python
"""
Specify CLI - Setup tool for Specify projects

Usage:
    pipx run --spec specify-cli.py specify init <project-name>
    pipx run --spec specify-cli.py specify init .
    pipx run --spec specify-cli.py specify init --here

Or install globally:
    pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
    specify init <project-name>
    specify init .
    specify init --here
"""
```

---

## 2. Customize ASCII Banner

### File: `src/specify_cli/__init__.py`

**Lines 159-168: Banner and tagline**

**Current:**
```python
BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝
███████║██║     ███████╗╚██████╗██║██║        ██║
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝
"""

TAGLINE = "GitHub Spec Kit - Spec-Driven Development Toolkit"
```

**Change to:**
```python
BANNER = """
███████╗██████╗ ███████╗ ██████╗    ██╗  ██╗██╗████████╗
██╔════╝██╔══██╗██╔════╝██╔════╝    ██║ ██╔╝██║╚══██╔══╝
███████╗██████╔╝█████╗  ██║         █████╔╝ ██║   ██║
╚════██║██╔═══╝ ██╔══╝  ██║         ██╔═██╗ ██║   ██║
███████║██║     ███████╗╚██████╗    ██║  ██╗██║   ██║
╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝  ╚═╝╚═╝   ╚═╝
███████╗███╗   ███╗ █████╗ ██████╗ ████████╗
██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
███████╗██╔████╔██║███████║██████╔╝   ██║
╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║
███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
"""

TAGLINE = "Enterprise Spec-Driven Development Toolkit"
```

**Alternative (Simpler Banner):**
```python
BANNER = """
╔═══════════════════════════════════════════╗
║   SPEC KIT SMART - ENTERPRISE EDITION     ║
╚═══════════════════════════════════════════╝
"""

TAGLINE = "Spec-Driven Development for Corporate Teams"
```

**To generate custom ASCII art:**
1. Visit: https://patorjk.com/software/taag/
2. Enter text: "SPEC KIT SMART"
3. Choose font: "ANSI Shadow" (current style) or "Big", "Standard", etc.
4. Copy output and paste into `BANNER` variable

---

## 3. Remove Script Type Selection (Auto-Detection Only)

### File: `src/specify_cli/__init__.py`

**Lines 998-1010: Script selection logic**

**Current:**
```python
if script_type:
    if script_type not in SCRIPT_TYPE_CHOICES:
        console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
        raise typer.Exit(1)
    selected_script = script_type
else:
    default_script = "ps" if os.name == "nt" else "sh"

    if sys.stdin.isatty():
        selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "Choose script type (or press Enter)", default_script)
    else:
        selected_script = default_script
```

**Change to:**
```python
if script_type:
    # Allow manual override if explicitly provided
    if script_type not in SCRIPT_TYPE_CHOICES:
        console.print(f"[red]Error:[/red] Invalid script type '{script_type}'. Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}")
        raise typer.Exit(1)
    selected_script = script_type
else:
    # Auto-detect based on OS (no interactive prompt)
    selected_script = "ps" if os.name == "nt" else "sh"
    console.print(f"[dim]Auto-detected script type:[/dim] {selected_script} ({SCRIPT_TYPE_CHOICES[selected_script]})")
```

**Result:**
- No interactive menu shown
- Auto-detects Windows → PowerShell, Linux/Mac → Bash
- Users can still override with `--script ps/sh` if needed
- Shows brief message: "Auto-detected script type: sh (POSIX Shell)"

**Lines 1022-1023: Remove script selection from tracker**

**Current:**
```python
tracker.add("script-select", "Select script type")
tracker.complete("script-select", selected_script)
```

**Change to:**
```python
tracker.add("script-detect", "Detect script type")
tracker.complete("script-detect", selected_script)
```

---

## 4. Fix Package Download Pattern (Unified Packages)

### Issue:
Current code downloads from `github/spec-kit` (original repo) and expects separate `-sh` or `-ps` packages. Your fork:
- Uses unified packages (one package with both sh and ps)
- Hosted at `veerabhadra-ponna/spec-kit-smart`
- Pattern changed from `spec-kit-template-{agent}-{script_type}` to `spec-kit-template-{agent}-{version}`

### File: `src/specify_cli/__init__.py`

**Lines 561-598: Download function**

**Current:**
```python
def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    repo_owner = "github"
    repo_name = "spec-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    # ... (fetch release data)

    assets = release_data.get("assets", [])
    pattern = f"spec-kit-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]
```

**Change to:**
```python
def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    # Changed to spec-kit-smart fork (unified packages with both sh and ps)
    repo_owner = "veerabhadra-ponna"
    repo_name = "spec-kit-smart"

    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    # ... (fetch release data)

    assets = release_data.get("assets", [])
    # Unified packages don't have -sh or -ps suffix, just version
    # Pattern: spec-kit-template-{agent}-{version}.zip
    pattern = f"spec-kit-template-{ai_assistant}-"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]
```

**Why this works:**
- Old pattern: `spec-kit-template-claude-sh-v0.1.0.zip` (separate packages)
- New pattern: `spec-kit-template-claude-v0.1.0.zip` (unified package)
- Matching `spec-kit-template-claude-` finds `spec-kit-template-claude-v0.1.0.zip`
- Package already contains both `scripts/bash/` and `scripts/powershell/`

**Alternative (Make repo configurable via environment variable):**

```python
def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    # Allow override for corporate GitHub Enterprise
    repo_owner = os.getenv("SPECKIT_REPO_OWNER", "veerabhadra-ponna")
    repo_name = os.getenv("SPECKIT_REPO_NAME", "spec-kit-smart")

    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print(f"[cyan]Fetching from {repo_owner}/{repo_name}...[/cyan]")

    # Support GitHub Enterprise URLs
    github_api_base = os.getenv("GITHUB_API_URL", "https://api.github.com")
    api_url = f"{github_api_base}/repos/{repo_owner}/{repo_name}/releases/latest"

    # ... rest of function
```

**Environment variable usage:**
```bash
# Default (public GitHub)
specify init myproject --ai claude

# GitHub Enterprise
export SPECKIT_REPO_OWNER=yourcompany
export SPECKIT_REPO_NAME=spec-kit-internal
export GITHUB_API_URL=https://github.company.com/api/v3
specify init myproject --ai claude
```

---

## 5. Package Structure Verification

### Current Package (Unified) - Already Correct!

Looking at `.github/workflows/scripts/create-release-packages.sh`:

**Lines 139-159: Package structure**
```bash
# Copy base structure with BOTH script directories
SPEC_DIR="$base_dir/.specify"
mkdir -p "$SPEC_DIR"

[[ -d memory ]] && { cp -r memory "$SPEC_DIR/"; echo "Copied memory -> .specify"; }
[[ -d .guidelines ]] && { cp -r .guidelines "$base_dir/"; echo "Copied .guidelines -> package root"; }

# Copy bash, powershell, and python script directories
if [[ -d scripts ]]; then
    mkdir -p "$SPEC_DIR/scripts"
    [[ -d scripts/bash ]] && {
        cp -r scripts/bash "$SPEC_DIR/scripts/"
        echo "Copied scripts/bash -> .specify/scripts"
    }
    [[ -d scripts/powershell ]] && {
        cp -r scripts/powershell "$SPEC_DIR/scripts/"
        echo "Copied scripts/powershell -> .specify/scripts"
    }
    # ...
fi
```

**Package structure after extraction:**
```
project-root/
├── .guidelines/                    ← Already copied to root!
│   ├── README.md
│   ├── java-guidelines.md
│   ├── reactjs-guidelines.md
│   └── ...
├── .specify/
│   ├── memory/
│   ├── scripts/
│   │   ├── bash/                   ← Both script types included!
│   │   │   ├── analyze-project.sh
│   │   │   ├── create-new-feature.sh
│   │   │   └── ...
│   │   └── powershell/
│   │       ├── analyze-project.ps1
│   │       ├── create-new-feature.ps1
│   │       └── ...
│   └── templates/
└── .claude/commands/               ← Agent-specific folder
    └── speckit.*.md
```

✅ **No changes needed!** Package already includes:
- `.guidelines/` at root
- Both `scripts/bash/` and `scripts/powershell/` under `.specify/scripts/`

---

## 6. Testing the Changes

### After making all changes:

1. **Test banner display:**
```bash
python src/specify_cli/__init__.py --help
```

2. **Test auto-detection:**
```bash
# Should NOT show interactive menu, just auto-detect
python src/specify_cli/__init__.py init test-project --ai claude
```

3. **Test package download:**
```bash
# Should download from veerabhadra-ponna/spec-kit-smart
python src/specify_cli/__init__.py init test-project --ai claude --debug
```

4. **Test with pipx:**
```bash
# Install in editable mode
pip install -e .

# Test installed version
specify init test-project --ai claude
```

5. **Verify extracted structure:**
```bash
cd test-project
ls -la .guidelines/  # Should exist at root
ls -la .specify/scripts/bash/  # Should exist
ls -la .specify/scripts/powershell/  # Should exist
```

---

## 7. Documentation Updates for Users

### Add to README.md (New Section)

**After line 1380 (Prerequisites section):**

```markdown
### Enterprise Installation Notes

#### For Companies That Block UV

This fork is designed to work without `uv`. Use standard `pip`/`pipx` instead:

```bash
# Install with pipx (recommended)
pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git

# Or with pip in a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
```

#### For GitHub Enterprise Environments

Set environment variables to point to your internal repository:

```bash
# Configure internal repository
export SPECKIT_REPO_OWNER=yourcompany
export SPECKIT_REPO_NAME=spec-kit-internal
export GITHUB_API_URL=https://github.company.com/api/v3

# Install and use
pipx install git+https://github.company.com/yourcompany/spec-kit-internal.git
specify init myproject --ai claude
```

#### Script Type Auto-Detection

The tool automatically detects your operating system:
- **Windows** → PowerShell scripts (`.ps1`)
- **Linux/Mac/WSL** → Bash scripts (`.sh`)

Both script types are always included in the package. Override if needed:
```bash
specify init myproject --ai claude --script ps  # Force PowerShell
specify init myproject --ai claude --script sh  # Force Bash
```
```

---

## 8. Summary of Changes

| File | Lines | Change | Reason |
|------|-------|--------|--------|
| `src/specify_cli/__init__.py` | 159-168 | Change banner and tagline | Branding for Spec Kit Smart |
| `src/specify_cli/__init__.py` | 562-563 | Change repo to `veerabhadra-ponna/spec-kit-smart` | Download from fork, not original |
| `src/specify_cli/__init__.py` | 594 | Change pattern to `spec-kit-template-{agent}-` | Support unified packages (no `-sh`/`-ps` suffix) |
| `src/specify_cli/__init__.py` | 998-1010 | Remove interactive script selection | Auto-detect only, no prompt |
| `src/specify_cli/__init__.py` | 13-24 | Update docstring examples | Replace UV with pipx |
| `README.md` | 164-194 | Replace UV with pip/pipx | Enterprise compatibility |
| `CONTRIBUTING.md` | 34-35, 62-63 | Replace UV with pip/venv | Developer setup without UV |
| `docs/local-development.md` | 34-53 | Replace UV with pip/pipx | Documentation consistency |
| `docs/quickstart.md` | 14-22 | Replace UV with pipx | Quick start without UV |
| `.devcontainer/post-create.sh` | 86-89 | Remove UV installation | Not needed anymore |

---

## 9. Release Checklist

Before releasing changes:

- [ ] Update banner in `src/specify_cli/__init__.py` (lines 159-168)
- [ ] Change repo owner/name in `download_template_from_github()` (lines 562-563)
- [ ] Fix package pattern matching (line 594)
- [ ] Remove interactive script selection (lines 998-1010)
- [ ] Update docstring in `__init__.py` (lines 13-24)
- [ ] Update README.md installation instructions (lines 164-194)
- [ ] Update CONTRIBUTING.md (lines 34-35, 62-63)
- [ ] Update docs/local-development.md (lines 34-53)
- [ ] Update docs/quickstart.md (lines 14-22)
- [ ] Remove UV from .devcontainer/post-create.sh (lines 86-89)
- [ ] Test banner display: `specify --help`
- [ ] Test auto-detection (should not prompt): `specify init test --ai claude`
- [ ] Test package download (should pull from spec-kit-smart)
- [ ] Verify extracted package has `.guidelines/` at root
- [ ] Verify extracted package has both `bash/` and `powershell/` scripts
- [ ] Test on Windows (PowerShell auto-detected)
- [ ] Test on Linux/Mac (Bash auto-detected)
- [ ] Test manual override: `--script ps` and `--script sh`
- [ ] Create release with unified packages using workflow

---

## 10. Migration Path for Existing Users

### For users currently using UV:

**Step 1: Uninstall UV version**
```bash
uv tool uninstall specify-cli
```

**Step 2: Install with pipx**
```bash
pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
```

**Step 3: Verify**
```bash
specify --help  # Should show new "SPEC KIT SMART" banner
```

### For corporate environments:

**Step 1: Fork to internal GitHub Enterprise**
```bash
# Clone public repo
git clone https://github.com/veerabhadra-ponna/spec-kit-smart.git

# Push to internal GitHub
cd spec-kit-smart
git remote add enterprise https://github.company.com/yourorg/spec-kit-internal.git
git push enterprise main
```

**Step 2: Create releases on internal GitHub**
```bash
# Trigger release workflow on your fork
# Workflow will create packages from your fork automatically
```

**Step 3: Configure environment (optional)**
```bash
export SPECKIT_REPO_OWNER=yourorg
export SPECKIT_REPO_NAME=spec-kit-internal
export GITHUB_API_URL=https://github.company.com/api/v3
```

**Step 4: Install**
```bash
pipx install git+https://github.company.com/yourorg/spec-kit-internal.git
```

---

## Notes

1. **Backward Compatibility:** The `--script` flag still works for users who want to manually override detection.

2. **Package Pattern:** The change from `spec-kit-template-{agent}-{script_type}` to `spec-kit-template-{agent}-{version}` is already implemented in your release workflow. The specify_cli just needs to match this pattern by removing the `-{script_type}` part from the pattern matching.

3. **GitHub Enterprise:** The optional environment variable approach (alternative solution in section 4) allows corporate users to point to internal repositories without code changes.

4. **.guidelines Folder:** Already copied to package root by `create-release-packages.sh` (line 140), no changes needed.

5. **Both Scripts Included:** Unified packages already include both bash and powershell directories (lines 145-152 of release script), no changes needed.

6. **Auto-Detection Logic:** Already exists in the code (line 1004: `default_script = "ps" if os.name == "nt" else "sh"`), just need to remove the interactive prompt.

---

**End of Enterprise Migration Guide**
