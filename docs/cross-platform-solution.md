# Cross-Platform Unified Package Solution

## Executive Summary

**Problem**: Developers need both sh and ps scripts when switching between Windows local environments and Unix cloud containers. Current approach generates 28 separate packages (14 agents × 2 script types), making it impractical.

**Solution**: Unified package containing both script types with intelligent OS detection at the AI agent level.

## Why Previous Launcher Approach Failed

The previous attempt created `.sh` launcher scripts in `scripts/launchers/` directory:
- ❌ `.sh` files don't execute properly on Windows (even with Git Bash)
- ❌ Required users to have bash available on Windows
- ❌ Path resolution issues in packaged releases
- ❌ Still OS-dependent (required sh-compatible environment)

## Recommended Solution: "Intelligent Unified Package"

### Three-Layer Approach

#### Layer 1: AI Agent OS Detection (Primary)
**The AI agents themselves detect OS and run appropriate scripts**

**Why this works:**
- ✅ No launcher scripts needed
- ✅ All AI agents already have OS detection capabilities
- ✅ Works across all platforms (Claude, Gemini, Copilot, etc.)
- ✅ Leverages existing AI environment awareness
- ✅ Simplest implementation

**How it works:**
1. Unified package contains BOTH `scripts/bash/` and `scripts/powershell/` directories
2. Prompts include OS detection instructions for the AI
3. AI detects platform using standard commands (`uname`, `$env:OS`, etc.)
4. AI executes the appropriate script based on detection

**Example prompt modification:**
```markdown
## Setup

**Detect your operating system and run the appropriate setup script:**

**On Unix/Linux/macOS:**
```bash
scripts/bash/setup-plan.sh --json
```

**On Windows (PowerShell):**
```powershell
scripts/powershell/setup-plan.ps1 -Json
```

**OS Detection:**
- Run `uname` - if it succeeds, you're on Unix/Linux/macOS
- Check `$env:OS` or `$IsWindows` - if "Windows_NT" or true, you're on Windows
- Use `scripts/bash/` for Unix-like systems
- Use `scripts/powershell/` for Windows systems

Parse the JSON output for: FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH
```

#### Layer 2: Environment Variable Override (Fallback)
**Support explicit OS specification via environment variable**

**Variable:** `SPEC_KIT_PLATFORM`

**Values:**
- `unix` - Force use of bash scripts
- `windows` - Force use of PowerShell scripts
- `auto` (default) - AI agent auto-detects OS

**Use cases:**
- Cloud environments where detection might be unreliable
- Testing both script types on same platform
- Explicit user preference

**How AI agents check:**
```bash
# In bash
if [[ "${SPEC_KIT_PLATFORM:-auto}" == "windows" ]]; then
  # User explicitly wants PowerShell
fi

# In PowerShell
if ($env:SPEC_KIT_PLATFORM -eq 'unix') {
  # User explicitly wants bash
}
```

#### Layer 3: Unified Package Structure
**Single package containing both script implementations**

**New package structure:**
```
spec-kit-template-{agent}-unified-{version}.zip
├── .specify/
│   ├── scripts/
│   │   ├── bash/              ← Both included!
│   │   │   ├── common.sh
│   │   │   ├── setup-plan.sh
│   │   │   ├── update-agent-context.sh
│   │   │   └── ... (all 11 bash scripts)
│   │   └── powershell/        ← Both included!
│   │       ├── common.ps1
│   │       ├── setup-plan.ps1
│   │       ├── update-agent-context.ps1
│   │       └── ... (all 6 PowerShell scripts)
│   ├── memory/
│   │   └── constitution.md
│   └── templates/
│       └── ... (existing templates)
└── .{agent}/
    └── commands/              # or prompts/, workflows/
        ├── speckit.plan.md
        ├── speckit.specify.md
        └── ... (all commands)
```

**Package count reduction:**
- Before: 28 packages (14 agents × 2 script types)
- After: 14 packages (14 agents × 1 unified)
- **50% reduction** in release artifacts

## Implementation Plan

### Step 1: Update Prompt Templates (10 files)

**Modify YAML frontmatter to include both scripts explicitly:**

```yaml
---
description: Execute the implementation planning workflow
scripts:
  bash: scripts/bash/setup-plan.sh --json
  powershell: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  bash: scripts/bash/update-agent-context.sh __AGENT__
  powershell: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---
```

**Add OS detection section to prompt body:**

```markdown
## Setup & OS Detection

**Step 1: Detect Operating System**

Check the environment variable first:
- If `SPEC_KIT_PLATFORM=unix` → Use bash scripts
- If `SPEC_KIT_PLATFORM=windows` → Use PowerShell scripts
- If `SPEC_KIT_PLATFORM=auto` or not set → Auto-detect below

**Auto-detection methods:**

On Unix/Linux/macOS, run:
```bash
uname
```
If successful, you're on a Unix-like system → Use bash scripts

On Windows, check:
```powershell
$env:OS
$IsWindows
```
If `$env:OS` equals "Windows_NT" or `$IsWindows` is true → Use PowerShell scripts

**Step 2: Run Setup Script**

**For Unix/Linux/macOS (bash):**
```bash
{SCRIPT_BASH}
```

**For Windows (PowerShell):**
```powershell
{SCRIPT_POWERSHELL}
```

Parse the JSON output for: FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH
```

### Step 2: Update Build Script

**Modify `create-release-packages.sh`:**

1. **Change function signature** to remove script variant:
```bash
# Before:
build_variant() {
  local agent=$1 script=$2

# After:
build_unified() {
  local agent=$1
```

2. **Copy BOTH script directories:**
```bash
# New implementation:
if [[ -d scripts ]]; then
  mkdir -p "$SPEC_DIR/scripts"
  # Copy both bash and powershell directories
  [[ -d scripts/bash ]] && {
    cp -r scripts/bash "$SPEC_DIR/scripts/"
    echo "Copied scripts/bash -> .specify/scripts"
  }
  [[ -d scripts/powershell ]] && {
    cp -r scripts/powershell "$SPEC_DIR/scripts/"
    echo "Copied scripts/powershell -> .specify/scripts"
  }
  # Copy any root-level scripts
  find scripts -maxdepth 1 -type f -exec cp {} "$SPEC_DIR/scripts/" \; 2>/dev/null || true
fi
```

3. **Update command generation** to include both script paths:
```bash
generate_commands() {
  local agent=$1 ext=$2 arg_format=$3 output_dir=$4
  # Remove script_variant parameter

  for template in templates/commands/*.md; do
    # Extract BOTH script commands
    script_bash=$(awk '/^[[:space:]]*bash:[[:space:]]*/ {...}')
    script_powershell=$(awk '/^[[:space:]]*powershell:[[:space:]]*/ {...}')

    # Replace placeholders
    body=$(sed "s|{SCRIPT_BASH}|${script_bash}|g" "$template")
    body=$(sed "s|{SCRIPT_POWERSHELL}|${script_powershell}|g" "$body")

    # Keep scripts section in frontmatter for AI reference
    # Don't remove it anymore
  done
}
```

4. **Update main loop** to build unified packages:
```bash
# Before:
for agent in "${AGENT_LIST[@]}"; do
  for script in "${SCRIPT_LIST[@]}"; do
    build_variant "$agent" "$script"
  done
done

# After:
for agent in "${AGENT_LIST[@]}"; do
  build_unified "$agent"
done

# Remove SCRIPTS env var support (no longer needed)
```

5. **Update package naming:**
```bash
# Before:
spec-kit-template-${agent}-${script}-${NEW_VERSION}.zip

# After:
spec-kit-template-${agent}-unified-${NEW_VERSION}.zip
# Or simply:
spec-kit-template-${agent}-${NEW_VERSION}.zip
```

### Step 3: Update Workflow Files

**Modify `.github/workflows/release.yml`:**

1. Remove script matrix:
```yaml
# Before:
strategy:
  matrix:
    agent: [claude, gemini, ...]
    script: [sh, ps]

# After:
strategy:
  matrix:
    agent: [claude, gemini, ...]
```

2. Update artifact paths:
```yaml
# Before:
path: .genreleases/spec-kit-template-*-sh-*.zip
path: .genreleases/spec-kit-template-*-ps-*.zip

# After:
path: .genreleases/spec-kit-template-*-unified-*.zip
# Or:
path: .genreleases/spec-kit-template-*-v*.zip
```

### Step 4: Documentation Updates

**Update README.md and release notes:**

```markdown
## Package Contents

Each package contains:
- **Cross-platform scripts**: Both bash and PowerShell implementations
- **AI agent commands**: Pre-configured for your AI assistant
- **Templates**: Specification and planning templates
- **Memory**: Constitution and context files

## OS Selection

The AI agent automatically detects your operating system and uses the appropriate scripts:
- **Unix/Linux/macOS**: Uses `scripts/bash/`
- **Windows**: Uses `scripts/powershell/`

### Manual Override

Set environment variable to override auto-detection:

```bash
# Force bash scripts
export SPEC_KIT_PLATFORM=unix

# Force PowerShell scripts
export SPEC_KIT_PLATFORM=windows
```

## Compatibility

- **Unix/Linux/macOS**: Requires bash 4.0+
- **Windows**: Requires PowerShell 5.1+ or PowerShell Core 7+
- **Git Bash on Windows**: Uses bash scripts automatically
```

## Benefits

### For Developers
- ✅ **One package for all environments** - Download once, use everywhere
- ✅ **Seamless switching** - Move between Windows laptop and Linux cloud without re-downloading
- ✅ **Explicit control** - Override detection with environment variable
- ✅ **Better DX** - No confusion about which package to download

### For Maintainers
- ✅ **50% fewer packages** - 14 instead of 28
- ✅ **Simpler releases** - Half the artifacts to upload and test
- ✅ **No launcher complexity** - AI handles OS detection
- ✅ **Future-proof** - Easy to add more platforms (e.g., Python scripts)

### For AI Agents
- ✅ **Platform-aware execution** - Use existing OS detection capabilities
- ✅ **Fallback support** - Environment variable override for edge cases
- ✅ **Clear instructions** - Prompts explain exactly what to do
- ✅ **Universal compatibility** - Works in any container or environment

## Migration Path

### Phase 1: Dual Support (Transition Period)
- Generate BOTH old (sh/ps) and new (unified) packages
- Users can test unified packages while old ones still work
- Deprecation notice in old package README

### Phase 2: Unified Only
- Stop generating sh/ps packages
- Only unified packages in releases
- Update all documentation

### Phase 3: Cleanup
- Remove sh/ps build logic from scripts
- Archive old packages
- Finalize documentation

## Testing Strategy

1. **Test unified package on Windows:**
   - Extract package
   - Verify PowerShell scripts execute correctly
   - Verify AI agent detects Windows

2. **Test unified package on Linux:**
   - Extract package
   - Verify bash scripts execute correctly
   - Verify AI agent detects Linux

3. **Test unified package on macOS:**
   - Extract package
   - Verify bash scripts execute correctly
   - Verify AI agent detects macOS

4. **Test environment variable override:**
   - Set `SPEC_KIT_PLATFORM=windows` on Linux
   - Verify PowerShell scripts are used
   - Set `SPEC_KIT_PLATFORM=unix` on Windows
   - Verify bash scripts are used

5. **Test in CI/CD:**
   - GitHub Actions (Ubuntu runner)
   - GitHub Actions (Windows runner)
   - Docker container

## Alternative Solutions Considered

### Alternative 1: Node.js Launcher
**Pros:**
- Node.js widely available
- Easy to write cross-platform code
- Single launcher file

**Cons:**
- ❌ Requires Node.js installed
- ❌ Not all environments have Node
- ❌ Adds external dependency
- ❌ Slower than direct script execution

### Alternative 2: Python Launcher
**Pros:**
- Python commonly available
- Cross-platform by design
- Standard library has OS detection

**Cons:**
- ❌ Requires Python installed
- ❌ Not always available on minimal containers
- ❌ Adds external dependency

### Alternative 3: Dual Launcher Files
**Pros:**
- No external dependencies
- Platform-native execution

**Cons:**
- ❌ Still requires OS-specific files (.sh + .cmd)
- ❌ Similar to failed previous approach
- ❌ More files to maintain

### Alternative 4: Compiled Binary
**Pros:**
- No runtime dependencies
- Fast execution

**Cons:**
- ❌ Need separate binaries for each platform
- ❌ Defeats purpose of unified package
- ❌ Complex build process

## Why AI Agent Detection is Superior

The recommended solution (AI agent OS detection) beats all alternatives:

| Criteria | AI Detection | Node.js | Python | Dual Files | Binary |
|----------|--------------|---------|---------|------------|--------|
| No external dependencies | ✅ | ❌ | ❌ | ✅ | ✅ |
| Single launcher file | ✅ | ✅ | ✅ | ❌ | ❌ |
| Works in all environments | ✅ | ❌ | ❌ | ⚠️ | ❌ |
| Simple implementation | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| Fast execution | ✅ | ⚠️ | ⚠️ | ✅ | ✅ |
| Maintainability | ✅ | ⚠️ | ⚠️ | ❌ | ❌ |

## Rollout Plan

### Week 1: Implementation
- [ ] Update all 10 prompt templates with OS detection sections
- [ ] Modify build script to generate unified packages
- [ ] Update workflow to build unified packages
- [ ] Add environment variable documentation

### Week 2: Testing
- [ ] Test on Windows 10/11 with PowerShell 5.1
- [ ] Test on Windows with PowerShell Core 7
- [ ] Test on Ubuntu 20.04/22.04
- [ ] Test on macOS (Intel and Apple Silicon)
- [ ] Test with Claude, Gemini, Copilot agents

### Week 3: Dual Release
- [ ] Generate both old (sh/ps) and new (unified) packages
- [ ] Add deprecation notice to old packages
- [ ] Update documentation with migration guide
- [ ] Announce unified packages

### Week 4: Monitor & Iterate
- [ ] Collect user feedback
- [ ] Fix any edge cases
- [ ] Improve OS detection instructions if needed
- [ ] Plan for full migration

### Week 5+: Full Migration
- [ ] Remove old package generation
- [ ] Update all documentation
- [ ] Archive old packages
- [ ] Celebrate! 🎉

## Success Metrics

- ✅ Package count reduced from 28 to 14
- ✅ Package works on Windows and Unix without modification
- ✅ AI agents successfully detect OS in 95%+ of cases
- ✅ Environment variable override works in edge cases
- ✅ Zero reported issues with cross-platform execution
- ✅ Developer satisfaction improves (survey after 1 month)

## Conclusion

The **AI Agent OS Detection** approach is the simplest, most maintainable solution that requires:
- ✅ No launcher scripts
- ✅ No external dependencies
- ✅ Minimal code changes
- ✅ Maximum compatibility

It leverages the AI agents' existing capabilities and provides explicit control via environment variables when needed.
