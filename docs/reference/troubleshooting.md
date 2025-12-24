# Troubleshooting

This guide covers common issues you may encounter when using Spec Kit Smart and their solutions.

## Common Issues

### Issue: Command not found `/speckitadv.constitution`

**Symptoms**: AI agent reports command doesn't exist

**Solution**:

1. Ensure you ran `speckitadv init` in the project directory
2. Check that the agent command directory exists (e.g., `.claude/commands/`, `.gemini/commands/`)
3. Verify you're using the correct AI agent specified during init
4. Run `speckitadv check` to verify prerequisites

### Issue: Cannot push to branch `claude/xxx`

**Symptoms**: `403 Forbidden` or similar error when pushing

**Solution**:

1. Ensure branch name starts with `claude/` and ends with matching session ID
2. Check branch name format: `claude/<feature-name>-<sessionId>`
3. Verify remote repository permissions
4. Try: `git push -u origin <branch-name>` with full branch name

### Issue: State file corrupted after token limit

**Symptoms**: `/speckitadv.resume` fails to detect progress

**Solution**:

1. Check that feature directory exists in `specs/`
2. Check `specs/{feature}/.state/state.json` exists and is valid JSON
3. Run `speckitadv check --json` to see current workflow state
4. If state.json is corrupted, delete it and the CLI will reinitialize from artifacts
5. If artifacts are corrupted, re-run the specific phase command (e.g., `/speckitadv.plan`)

### Issue: Guidelines not loading in prompts

**Symptoms**: Corporate guidelines seem ignored by AI agent

**Solution**:

1. Verify `.guidelines/` directory exists with appropriate files
2. Check `.guidelines/stack-mapping.json` exists and paths match your project structure
3. Ensure guidelines files follow naming convention: `<stack>-guidelines.md`
4. Manually verify guidelines file structure matches your stack

### Issue: `pipx install` fails with SSL errors

**Symptoms**: Certificate verification errors during installation

**Solution**:

```bash
# Option 1: Update certificates (recommended)
pip install --upgrade certifi truststore

# Option 2: Use corporate proxy settings
export HTTPS_PROXY=http://proxy.company.com:8080
pipx install git+https://github.com/veerabhadra-ponna/spec-kit-smart.git
```

### Issue: Orchestrator skips phases unexpectedly

**Symptoms**: `/speckitadv.orchestrate` jumps over constitution or other phases

**Solution**:

1. Check state.json for workflow progress: `speckitadv check --json`
2. Orchestrator reads `specs/{feature}/.state/state.json` to determine current phase
3. Phases marked as completed in state.json are skipped
4. To restart: Delete `specs/{feature}/.state/state.json` or the entire feature directory

### Issue: Analyze-project cannot resume workflow

**Symptoms**: `speckitadv analyze-project` starts a new analysis instead of resuming

**Solution**:

1. Check that `.analysis/` directory exists with your analysis folder
2. Verify `{analysis_dir}/state.json` exists and is valid JSON
3. Resume specific analysis: `speckitadv analyze-project --analysis-dir=.analysis/project-20251224-164004`
4. If state.json is corrupted, delete it and re-run from the beginning
5. Auto-detect latest analysis: `speckitadv analyze-project` (no args)

### Issue: Analyze-project skips stages unexpectedly

**Symptoms**: Analysis workflow skips over completed stages

**Solution**:

1. Check state.json in your analysis folder: `cat .analysis/{folder}/state.json`
2. The `stages_complete` list shows which stages are done
3. The `current_stage` field shows where to resume
4. To restart: Delete the analysis folder in `.analysis/`

### Issue: speckitadv command not found

**Symptoms**: The `speckitadv` CLI binary is not in PATH

**Solution**:

1. Download the platform-specific binary from the releases page
2. Add the binary location to your PATH
3. Alternatively, use full path in launcher files: `/path/to/speckitadv`
4. Verify with: `speckitadv --version`

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
- [Glossary](../README.md#glossary)
