# Troubleshooting

This guide covers common issues you may encounter when using Spec Kit Smart and their solutions.

## Common Issues

### Issue: Command not found `/speckitsmart.constitution`

**Symptoms**: AI agent reports command doesn't exist

**Solution**:

1. Ensure you ran `speckitsmart init` in the project directory
2. Check that the agent command directory exists (e.g., `.claude/commands/`, `.gemini/commands/`)
3. Verify you're using the correct AI agent specified during init
4. Run `speckitsmart check` to verify prerequisites

### Issue: Cannot push to branch `claude/xxx`

**Symptoms**: `403 Forbidden` or similar error when pushing

**Solution**:

1. Ensure branch name starts with `claude/` and ends with matching session ID
2. Check branch name format: `claude/<feature-name>-<sessionId>`
3. Verify remote repository permissions
4. Try: `git push -u origin <branch-name>` with full branch name

### Issue: State file corrupted after token limit

**Symptoms**: `/speckitsmart.resume` fails to load state

**Solution**:

1. Check if `.speckitsmart-state.json.backup` exists and restore it
2. If no backup, restart with `/speckitsmart.orchestrate --reset`
3. Future prevention: Commit `.speckitsmart-state.json` regularly

### Issue: Guidelines not loading in prompts

**Symptoms**: Corporate guidelines seem ignored by AI agent

**Solution**:

1. Verify `.guidelines/` directory exists with appropriate files
2. Check `.guidelines/stack-mapping.json` exists and paths match your project structure
3. Ensure guidelines files follow naming convention: `<stack>-guidelines.md`
4. Run `./scripts/bash/check-guidelines-compliance.sh` to validate setup

### Issue: `pipx install` fails with SSL errors

**Symptoms**: Certificate verification errors during installation

**Solution**:

```bash
# Option 1: Use --skip-tls flag (not recommended for production)
speckitsmart init my-project --skip-tls

# Option 2: Update certificates (recommended)
pip install --upgrade certifi truststore

# Option 3: Use corporate proxy settings
export HTTPS_PROXY=http://proxy.company.com:8080
pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
```

### Issue: Orchestrator skips phases unexpectedly

**Symptoms**: `/speckitsmart.orchestrate` jumps over constitution or other phases

**Solution**:

1. Check if artifacts already exist from previous runs (`.specify/specs/`)
2. Orchestrator skips phases with existing artifacts unless `--force` is used
3. Review `.speckitsmart-state.json` to see completed phases
4. To restart: Delete state file and artifact directories

### Issue: Cross-platform scripts fail on Windows

**Symptoms**: Bash scripts don't work on Windows

**Solution**:

1. Set environment variable: `set SPEC_KIT_PLATFORM=windows` (CMD) or `$env:SPEC_KIT_PLATFORM="windows"` (PowerShell)
2. Ensure PowerShell scripts have `.ps1` extension
3. Check execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
4. Use Git Bash as alternative for bash scripts on Windows

## Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```

## Getting Help

If you encounter an issue not covered in this guide:

1. **Check the documentation**: Browse the [full documentation](../) for detailed guides
2. **Search existing issues**: Check [GitHub Issues](https://github.com/veerabhadra-ponna/spec-kit-smart/issues) for similar problems
3. **Open a new issue**: If you can't find a solution, [open a new issue](https://github.com/veerabhadra-ponna/spec-kit-smart/issues/new) with:
   - Description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

## Related Documentation

- [Getting Started Guide](../getting-started.md)
- [CLI Reference](cli-reference.md)
- [Orchestrator Workflow](../workflows/orchestrator.md)
- [Glossary](../README.md#-glossary)
