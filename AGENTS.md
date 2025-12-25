# AGENTS.md

Spec Kit is a toolkit for Spec-Driven Development. See [README.md](README.md) for details.

---

## General Practices

- Changes to `__init__.py` require version rev in `pyproject.toml` and `CHANGELOG.md` entry.

### Chunked File Generation for Large Outputs

**RULE:** Files >1500 lines → use chunked generation to prevent token limit errors.

**Strategy:**

1. Estimate size before generation
2. Generate in logical sections (300-800 lines per chunk)
3. First chunk: Write tool. Subsequent: Edit tool (append)
4. Continue automatically between chunks

**Chunk Size:** Small (300-500), Medium (500-800), Large (800-1200 for simple content)

**When to Use:** Function specs >1000 lines, technical specs >1500 lines, implementation >2000 lines, any uncertain size.

**Failure Recovery:** Resume from last successful chunk, don't restart.

### Never Use TODOs in Prompts

**RULE:** No TODO comments in prompt/template files. Use `/IMPROVEMENTS.md` for tracking.

### Pre-Commit Quality Checks

**Required:**

1. **Markdown lint**: `npx markdownlint-cli2 '**/*.md'` → must return `Summary: 0 error(s)`
2. **Spell check**: Review for typos
3. **Test CLI**: If modifying Python CLI, run `pytest tests/`

**Checklist:**

- [ ] Ran markdownlint with 0 errors
- [ ] No TODOs in prompt files
- [ ] Tested script changes
- [ ] Clear commit message

### Corporate Guidelines System

- **Auto-detection**: Prompts detect tech stack and load applicable guidelines
- **Priority**: Constitution > Corporate Guidelines > Spec Kit Defaults
- **Non-blocking**: Violations create `.guidelines-todo.md` but don't block workflow

See [.guidelines/README.md](.guidelines/README.md) for complete documentation.

---

## Adding New Agent Support

### Supported Agents

| Agent | Directory | Format | CLI Tool |
| ------- | ----------- | -------- | ---------- |
| Claude Code | `.claude/commands/` | Markdown | `claude` |
| Gemini CLI | `.gemini/commands/` | TOML | `gemini` |
| GitHub Copilot | `.github/prompts/` | Markdown | N/A (IDE) |
| Cursor | `.cursor/commands/` | Markdown | `cursor-agent` |
| Qwen Code | `.qwen/commands/` | TOML | `qwen` |
| opencode | `.opencode/command/` | Markdown | `opencode` |
| Codex CLI | `.codex/commands/` | Markdown | `codex` |
| Windsurf | `.windsurf/workflows/` | Markdown | N/A (IDE) |
| Kilo Code | `.kilocode/rules/` | Markdown | N/A (IDE) |
| Auggie CLI | `.augment/rules/` | Markdown | `auggie` |
| Roo Code | `.roo/rules/` | Markdown | N/A (IDE) |
| CodeBuddy | `.codebuddy/commands/` | Markdown | `codebuddy` |
| Amazon Q | `.amazonq/prompts/` | Markdown | `q` |
| Amp | `.agents/commands/` | Markdown | `amp` |

### Integration Checklist

1. **AGENT_CONFIG** (`scripts/python/speckit/setup/config.py`): Add entry with `name`, `folder`, `install_url`, `requires_cli`
2. **CLI help text**: Update `--ai` parameter in `init()` command
3. **README.md**: Add to Supported AI Agents table
4. **Release scripts**: Add to `ALL_AGENTS` array and `gh release create`
5. **workflow.py**: Add to `AGENT_FILES` dict
6. **Devcontainer** (optional): Add extensions/CLI tools

**Critical**: Use actual CLI executable name as key (e.g., `cursor-agent` not `cursor`).

**Formats**: Markdown uses `$ARGUMENTS`, TOML uses `{{args}}`

---

## Markdown Style

Run `npx markdownlint-cli2 '**/*.md'` before commit (must return 0 errors). Uses `.markdownlint.json` config.

---

## Documentation Structure

- **`docs/`**: User documentation (guides, reference, workflows)
- **`AGENTS.md`**: Repo dev instructions; toolkit AGENTS.md embedded in CLI
