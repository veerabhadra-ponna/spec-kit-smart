# State Management Simplification - Implementation Plan

## Overview

Replace the current chain ID system with a simpler, folder-based state management approach where natural identifiers (folder paths) serve as implicit chain IDs.

## Design Principles

1. **Folder as Chain ID** - No abstract 8-character hex IDs
2. **Single State File** - One `state.json` per workflow, not per-stage files
3. **CLI Controls State** - AI calls CLI helpers; CLI handles read/write
4. **Minimal CLI Arguments** - State file is communication channel between stages
5. **Config-Driven Naming** - Branching patterns from `config.json`

---

## Phase 1: Core State Module

### 1.1 New State Schema

**File:** `scripts/python/speckit/core/state_v2.py`

```python
@dataclass
class FeatureState:
    schema_version: int = 1
    feature: FeatureMetadata
    specify: PromptState
    plan: PromptState
    tasks: PromptState
    implement: PromptState

@dataclass
class FeatureMetadata:
    short_name: str
    description: str
    jira: Optional[str]
    created: str  # ISO timestamp

@dataclass
class PromptState:
    status: str  # "pending" | "in_progress" | "completed"
    current_stage: Optional[str]
    started: Optional[str]
    completed: Optional[str]
    artifacts: list[str]
```

### 1.2 State Operations

```python
class FeatureStateManager:
    def __init__(self, folder_path: Path):
        self.folder = folder_path
        self.state_file = folder_path / ".state" / "state.json"

    def initialize(self, metadata: FeatureMetadata) -> FeatureState
    def load(self) -> FeatureState
    def save(self, state: FeatureState) -> None
    def update_prompt(self, prompt: str, stage: str, status: str, artifacts: list = None)
    def get_prompt_context(self, prompt: str, stage: str) -> dict  # Only what prompt needs
```

### 1.3 Placeholder Detection

```python
def has_placeholders(content: str) -> bool:
    """Check for [UPPERCASE_WORD] patterns."""
    pattern = r'\[([A-Z][A-Z0-9_]*)\]'
    return bool(re.search(pattern, content))

def get_placeholders(content: str) -> list[str]:
    """Return list of placeholder names found."""
    pattern = r'\[([A-Z][A-Z0-9_]*)\]'
    return re.findall(pattern, content)
```

---

## Phase 2: CLI Helper Commands

### 2.1 Create Feature Command

**Purpose:** AI calls this to create feature folder with proper naming.

```bash
speckitadv create-feature --short-name "user-auth" --description "Add OAuth" [--jira PROJ-123]
```

**Implementation:** `scripts/python/speckit/commands/feature.py`

```python
@app.command("create-feature")
def create_feature(
    short_name: str,
    description: str,
    jira: Optional[str] = None,
    output_json: bool = True,
):
    """Create feature folder with proper naming from config."""
    config = load_config()
    folder_name = apply_branching_pattern(config, short_name, jira)
    folder_path = Path("specs") / folder_name

    if folder_path.exists():
        # Return existing folder info
        return {"success": True, "folder": str(folder_path), "existed": True}

    folder_path.mkdir(parents=True)

    # Initialize state
    state_manager = FeatureStateManager(folder_path)
    state_manager.initialize(FeatureMetadata(
        short_name=short_name,
        description=description,
        jira=jira,
        created=datetime.now().isoformat()
    ))

    # Create git branch if configured
    branch_name = get_branch_name(config, short_name, jira)
    if config.get("workflow", {}).get("auto_create_branch", False):
        create_git_branch(branch_name)

    return {
        "success": True,
        "folder": str(folder_path),
        "branch": branch_name,
        "state_file": str(folder_path / ".state" / "state.json")
    }
```

### 2.2 Branching Pattern Logic

```python
def apply_branching_pattern(config: dict, short_name: str, jira: str = None) -> str:
    """Apply config branching pattern to create folder name."""
    branching = config.get("branching", {})
    pattern = branching.get("pattern", "<shortname>")

    result = pattern

    # Handle <num> placeholder
    if "<num>" in result:
        next_num = get_next_feature_number()
        num_format = branching.get("number_format", {"digits": 3})
        formatted = str(next_num).zfill(num_format.get("digits", 3))
        result = result.replace("<num>", formatted)

    # Handle <jira> placeholder
    if "<jira>" in result:
        if jira:
            result = result.replace("<jira>", jira)
        else:
            # Remove jira and adjacent separator
            result = re.sub(r"<jira>[-_]?", "", result)
            result = re.sub(r"[-_]?<jira>", "", result)

    # Handle <shortname>
    result = result.replace("<shortname>", short_name)

    # Remove prefix for directory if configured
    if not branching.get("directory", {}).get("includes_prefix", False):
        prefix = branching.get("prefix", "")
        if result.startswith(prefix):
            result = result[len(prefix):]

    return result.strip("-_")
```

### 2.3 State Query Commands

```bash
# Show current state
speckitadv state show [folder]

# Reset a prompt to pending
speckitadv state reset <folder> <prompt>

# Get context for a specific prompt/stage (used internally)
speckitadv state context <folder> <prompt> <stage>
```

---

## Phase 3: Constitution Simplification

### 3.1 Remove Chain State for Constitution

**Changes to:** `scripts/python/speckit/core/stages.py`

```python
def run_constitution_command(stage: int, path: str = None):
    """Run constitution without chain state."""
    project_path = Path(path) if path else Path.cwd()
    constitution_path = project_path / "memory" / "constitution.md"

    # Check if already complete
    if constitution_path.exists():
        content = constitution_path.read_text()
        if not has_placeholders(content):
            console.print(
                "[yellow]Constitution already exists and is complete.[/yellow]\n"
                "To regenerate, delete: memory/constitution.md"
            )
            return

    # Run stage without chain state
    context = {
        "project_path": str(project_path),
        "constitution_path": str(constitution_path),
    }

    fragment = get_prompt_fragment("constitution", get_stage_name(stage))
    rendered = render_prompt(fragment, context)
    emit_stage(rendered, ...)
```

### 3.2 Update Constitution Prompts

Remove chain-related instructions from constitution prompt files.

---

## Phase 4: Feature-Scoped Commands

### 4.1 Specify Command Flow

```python
def run_specify_command(stage: int, description: str = None, jira: str = None):
    """Run specify with folder-based state."""

    if stage == 1:
        # Stage 1: Gather requirements, AI will call create-feature
        context = {
            "description": description,
            "jira": jira,
        }
        # Prompt instructs AI to call create-feature when ready

    else:
        # Later stages: Load state from folder
        folder = find_active_feature_folder()  # Latest or explicit
        state_manager = FeatureStateManager(folder)
        state = state_manager.load()

        context = state_manager.get_prompt_context("specify", stage)
        # Run stage...

        # Update state after completion
        state_manager.update_prompt("specify", stage, "completed", artifacts=[...])
```

### 4.2 Plan/Tasks/Implement Commands

```python
def run_plan_command(stage: int, folder: str = None):
    """Run plan using feature state."""
    folder_path = resolve_feature_folder(folder)  # Explicit or from state
    state_manager = FeatureStateManager(folder_path)
    state = state_manager.load()

    # Verify specify is complete
    if state.specify.status != "completed":
        console.print("[red]Error: specify must be completed before plan[/red]")
        return

    context = state_manager.get_prompt_context("plan", stage)
    # context includes: feature metadata, spec.md path, etc.

    # Run stage...
```

---

## Phase 5: Analyze-Project Simplification

### 5.1 Folder as Chain ID

```python
def run_analyze_project_command(stage: int, resume_folder: str = None):
    """Run analyze-project with folder-based state."""

    if resume_folder:
        folder = Path(resume_folder)
    elif stage == 1:
        # Create new analysis folder
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        username = get_username()
        folder = Path(".analysis") / f"{username}-{timestamp}"
        folder.mkdir(parents=True)
        initialize_analysis_state(folder)
    else:
        # Find latest analysis folder
        folder = find_latest_analysis_folder()

    state = load_analysis_state(folder)
    context = get_analysis_context(state, stage)
    # Run stage...
```

### 5.2 Resume Support

```bash
speckitadv analyze-project resume                           # Latest folder
speckitadv analyze-project resume .analysis/user-20251115   # Specific folder
```

---

## Phase 6: Resume and Orchestrate

### 6.1 Resume Command

```python
def run_resume_command(folder: str = None):
    """Resume from feature state."""
    folder_path = resolve_feature_folder(folder)
    state = FeatureStateManager(folder_path).load()

    # Find prompt with in_progress status
    for prompt in ["specify", "plan", "tasks", "implement"]:
        prompt_state = getattr(state, prompt)
        if prompt_state.status == "in_progress":
            console.print(f"Resuming {prompt} at stage {prompt_state.current_stage}")
            run_prompt_command(prompt, prompt_state.current_stage, folder_path)
            return

    # Find next pending prompt
    for prompt in ["specify", "plan", "tasks", "implement"]:
        prompt_state = getattr(state, prompt)
        if prompt_state.status == "pending":
            console.print(f"Starting {prompt}")
            run_prompt_command(prompt, 1, folder_path)
            return

    console.print("[green]All prompts completed![/green]")
```

### 6.2 Orchestrate Command

```python
def run_orchestrate_command(folder: str = None):
    """Orchestrate full workflow using feature state."""
    folder_path = resolve_feature_folder(folder)

    while True:
        state = FeatureStateManager(folder_path).load()
        next_prompt, next_stage = determine_next_action(state)

        if next_prompt is None:
            console.print("[green]Workflow complete![/green]")
            break

        run_prompt_command(next_prompt, next_stage, folder_path)
```

---

## Phase 7: Cleanup

### 7.1 Remove Old Chain Code

- Delete chain ID generation in `state.py`
- Remove `--chain` arguments from CLI
- Remove `.pending/` directory logic
- Remove per-stage state files
- Remove chain ID from prompt contexts

### 7.2 Update Tests

- Update all chain-related tests to use folder-based state
- Add tests for new CLI helper commands
- Add tests for placeholder detection
- Add tests for branching pattern application

### 7.3 Update Documentation

- Update README with new workflow
- Document config.json branching patterns
- Document CLI helper commands
- Update prompt files to reference new CLI commands

---

## Migration Notes

- No backward compatibility required (per user decision)
- Old `.state/` directories can be deleted
- Old chain IDs in prompts should be removed

---

## Implementation Order

1. **Phase 1:** Core state module (foundation)
2. **Phase 2:** CLI helper commands (create-feature, state commands)
3. **Phase 3:** Constitution simplification (standalone, low risk)
4. **Phase 4:** Feature-scoped commands (main workflow)
5. **Phase 5:** Analyze-project (similar pattern)
6. **Phase 6:** Resume and orchestrate (depends on Phase 4)
7. **Phase 7:** Cleanup old code and update docs

---

## Success Criteria

- [ ] No chain ID concept in codebase
- [ ] Single state.json per workflow
- [ ] CLI helper commands work for AI invocation
- [ ] Config-driven folder naming works
- [ ] Constitution skips if complete
- [ ] Resume works from any entry point
- [ ] All tests pass
- [ ] Documentation updated
