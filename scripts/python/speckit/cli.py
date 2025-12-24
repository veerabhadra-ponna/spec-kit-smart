"""
Spec Kit Smart CLI

Main entry point for the speckit command-line interface.
Implements the zero-prompt architecture with progressive stage injection.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from speckit import __version__

# Create console for rich output
console = Console()

# Create main Typer app
app = typer.Typer(
    name="speckitadv",
    help="Spec Kit Smart - Zero-Prompt Architecture CLI for AI-powered development",
    add_completion=True,
    # Note: no_args_is_help removed - commands default to stage 1 with current directory
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"speckitadv version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug output",
    ),
) -> None:
    """
    Spec Kit Smart - Zero-Prompt Architecture CLI

    This CLI provides progressive prompt injection for AI agents.
    All prompts, templates, and logic are embedded in this tool.
    """
    pass


# ============================================================================
# ANALYZE-PROJECT Command
# ============================================================================


@app.command("analyze-project")
def analyze_project(
    stage: int = typer.Option(1, "--stage", "-s", help="Current workflow stage (1-16)"),
    chunk: Optional[int] = typer.Option(None, "--chunk", "-c", help="Report chunk number for chunked stages"),
    analysis_dir: Optional[str] = typer.Option(None, "--analysis-dir", "-a", help="Analysis folder path (auto-created on stage 1)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path to analyze"),
    scope: Optional[str] = typer.Option(None, "--scope", help="Analysis scope: A (full) or B (cross-cutting)"),
    context: Optional[str] = typer.Option(None, "--context", help="Additional context"),
    concern_type: Optional[str] = typer.Option(None, "--concern-type", help="Cross-cutting concern type"),
    current_impl: Optional[str] = typer.Option(None, "--current-impl", help="Current implementation"),
    target_impl: Optional[str] = typer.Option(None, "--target-impl", help="Target implementation"),
    verify: bool = typer.Option(False, "--verify", help="Run verification after final stage completes"),
) -> None:
    """
    Analyze an existing project for modernization.

    This command implements a progressive workflow with enforced chunking.
    AI agents receive focused prompts (50-80 lines) at each stage.

    Uses folder-based state management. Analysis folder is auto-created on stage 1.
    Runs interactively if no --path/--scope provided at stage 1.
    """
    from speckit.commands.analyze import run_analyze_project

    # Interactive mode for stage 1 if required inputs missing
    if stage == 1 and not analysis_dir:
        from speckit.core.interactive import collect_analyze_project_input

        if not path:
            # No path provided - collect all inputs interactively
            inputs = collect_analyze_project_input()
            path = inputs.get("path")
            scope = inputs.get("scope")
            context = inputs.get("context")
            concern_type = inputs.get("concern_type")
            current_impl = inputs.get("current_impl")
            target_impl = inputs.get("target_impl")
        elif not scope:
            # Path provided but scope missing - require scope
            console.print("[red]Error:[/red] --scope is required when --path is provided")
            console.print("  Use --scope A for full application analysis")
            console.print("  Use --scope B for cross-cutting concern migration")
            raise typer.Exit(1)

    run_analyze_project(
        stage=stage,
        chunk=chunk,
        analysis_dir=analysis_dir,
        path=path,
        scope=scope,
        context=context,
        concern_type=concern_type,
        current_impl=current_impl,
        target_impl=target_impl,
        verify=verify,
    )


# ============================================================================
# CONSTITUTION Command
# ============================================================================


@app.command("constitution")
def constitution(
    stage: int = typer.Option(1, "--stage", "-s", help="Current workflow stage (1-3)"),
    principles: Optional[str] = typer.Option(None, "--principles", help="User-provided principles"),
    defaults: bool = typer.Option(False, "--defaults", help="Use default principles"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
) -> None:
    """
    Create or update the project constitution.

    Defines non-negotiable project principles and governance.
    Runs interactively if no --principles or --defaults provided.

    Note: If constitution.md exists and has no placeholders, it's considered complete.
    To regenerate, delete memory/constitution.md first.
    """
    from speckit.commands.constitution import run_constitution

    run_constitution(stage=stage, principles=principles, defaults=defaults, path=path)


# ============================================================================
# SPECIFY Command
# ============================================================================


@app.command("specify")
def specify(
    stage: int = typer.Option(1, "--stage", "-s", help="Current workflow stage (1-6)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
    feature_dir: Optional[str] = typer.Option(None, "--feature-dir", help="Feature directory path (for stage 3+)"),
    jira: Optional[str] = typer.Option(None, "--jira", "-j", help="JIRA number (format: C12345-7890)"),
    feature: Optional[str] = typer.Option(None, "--feature", "-f", help="Feature description"),
) -> None:
    """
    Create baseline specification.

    Defines what needs to be built before planning how.
    Runs interactively if no --jira/--feature provided at stage 2.

    Uses folder-based state management. Feature folder is created via
    'speckitadv create-feature' command during the workflow.
    """
    from speckit.core.stages import run_staged_command

    context = {}

    # Stage 3 requires --feature (collected in stage 2, passed here since state is stateless)
    if stage == 3 and not feature:
        console.print("[red]Error:[/red] --feature is required for stage 3")
        console.print("  Stage 2 should have collected this value. Run stage 3 with:")
        console.print("  speckitadv specify --stage=3 --feature='your feature description'")
        console.print("  (--jira is optional)")
        raise typer.Exit(1)

    # Interactive mode for stage 2 (input collection)
    if stage == 2 and not jira and not feature:
        from speckit.core.interactive import collect_specify_input

        collected_jira, collected_feature = collect_specify_input()
        if collected_feature:
            context["jira"] = collected_jira or ""
            context["feature"] = collected_feature
        else:
            console.print("[red]Error:[/red] Feature description is required")
            raise typer.Exit(1)
    elif jira or feature:
        # Validate that feature is provided when using CLI args
        if not feature:
            console.print("[red]Error:[/red] --feature is required when using CLI arguments")
            console.print("  Example: speckitadv specify --stage 2 --feature 'Build user auth'")
            raise typer.Exit(1)
        context["jira"] = jira or ""
        context["feature"] = feature

    run_staged_command(command="specify", stage=stage, path=path, feature_dir=feature_dir, context=context if context else None)


# ============================================================================
# PLAN Command
# ============================================================================


@app.command("plan")
def plan(
    stage: int = typer.Option(1, "--stage", "-s", help="Current workflow stage (1-4)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
    feature_dir: Optional[str] = typer.Option(None, "--feature-dir", help="Feature directory path"),
    constraints: Optional[str] = typer.Option(None, "--constraints", "-c", help="Planning constraints"),
) -> None:
    """
    Create implementation plan.

    Designs how to build what was specified.
    Uses folder-based state management from the feature directory.
    """
    from speckit.core.stages import run_staged_command

    context = {}

    # Pass constraints to context if provided via CLI
    if constraints:
        context["constraints"] = constraints

    run_staged_command(command="plan", stage=stage, path=path, feature_dir=feature_dir, context=context if context else None)


# ============================================================================
# TASKS Command
# ============================================================================


@app.command("tasks")
def tasks(
    stage: int = typer.Option(1, "--stage", "-s", help="Current workflow stage (1-4)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
    feature_dir: Optional[str] = typer.Option(None, "--feature-dir", help="Feature directory path"),
    preferences: Optional[str] = typer.Option(None, "--preferences", help="Task generation preferences"),
) -> None:
    """
    Generate actionable tasks.

    Breaks down the plan into implementable units.
    Uses folder-based state management from the feature directory.
    """
    from speckit.core.stages import run_staged_command

    context = {}

    # Pass preferences to context if provided via CLI
    if preferences:
        context["preferences"] = preferences

    run_staged_command(command="tasks", stage=stage, path=path, feature_dir=feature_dir, context=context if context else None)


# ============================================================================
# IMPLEMENT Command
# ============================================================================


@app.command("implement")
def implement(
    stage: int = typer.Option(1, "--stage", "-s", help="Current workflow stage (1-5)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
    feature_dir: Optional[str] = typer.Option(None, "--feature-dir", help="Feature directory path"),
    notes: Optional[str] = typer.Option(None, "--notes", "-n", help="Implementation notes"),
) -> None:
    """
    Execute implementation.

    Implements tasks with quality checks.
    Uses folder-based state management from the feature directory.
    """
    from speckit.core.stages import run_staged_command

    context = {}

    # Pass notes to context if provided via CLI
    if notes:
        context["notes"] = notes

    run_staged_command(command="implement", stage=stage, path=path, feature_dir=feature_dir, context=context if context else None)


# ============================================================================
# CLARIFY Command
# ============================================================================


@app.command("clarify")
def clarify(
    stage: int = typer.Option(1, "--stage", "-s", help="Current workflow stage (1-3)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
    feature_dir: Optional[str] = typer.Option(None, "--feature-dir", help="Feature directory path"),
) -> None:
    """
    Ask structured questions.

    Resolves ambiguities before implementation.
    """
    from speckit.core.stages import run_staged_command

    run_staged_command(command="clarify", stage=stage, path=path, feature_dir=feature_dir)


# ============================================================================
# CHECKLIST Command
# ============================================================================


@app.command("checklist")
def checklist(
    stage: int = typer.Option(1, "--stage", "-s", help="Current workflow stage (1-3)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
    feature_dir: Optional[str] = typer.Option(None, "--feature-dir", help="Feature directory path"),
) -> None:
    """
    Generate quality checklist.

    Creates validation checklists for requirements.
    """
    from speckit.core.stages import run_staged_command

    run_staged_command(command="checklist", stage=stage, path=path, feature_dir=feature_dir)


# ============================================================================
# ORCHESTRATE Command
# ============================================================================


@app.command("orchestrate")
def orchestrate(
    description: Optional[str] = typer.Argument(None, help="Feature description to orchestrate"),
) -> None:
    """
    Orchestrate complete spec-driven workflow.

    Runs the entire workflow from constitution to implementation.
    Use 'resume' to continue after interruptions.
    """
    from speckit.core.prompts import get_prompt_fragment

    fragment = get_prompt_fragment("orchestrate", "")
    if description:
        fragment = fragment.replace("$ARGUMENTS", description)
    console.print(fragment)


# ============================================================================
# RESUME Command
# ============================================================================


@app.command("resume")
def resume() -> None:
    """
    Resume workflow from saved state.

    Restores context after interruptions, chat limits, or shutdowns.
    """
    from speckit.core.prompts import get_prompt_fragment

    fragment = get_prompt_fragment("resume", "")
    console.print(fragment)


# ============================================================================
# ANALYZE Command (cross-artifact consistency check)
# ============================================================================


@app.command("analyze")
def analyze(
    focus: Optional[str] = typer.Argument(None, help="Focus areas for analysis (e.g., 'security', 'constitution')"),
    stage: int = typer.Option(1, "--stage", "-s", help="Analysis stage (1-3)"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
) -> None:
    """
    Cross-artifact consistency and quality analysis.

    Performs non-destructive analysis across spec.md, plan.md, and tasks.md
    to identify inconsistencies, gaps, and quality issues before implementation.
    Run after /speckitadv.tasks and before /speckitadv.implement.
    Focus areas are collected by the AI agent via the stage prompt.

    Stages:
      1 - Setup and artifact loading
      2 - Detection passes
      3 - Report generation
    """
    from speckit.core.prompts import get_prompt_fragment

    stage_map = {1: "01-setup", 2: "02-detection", 3: "03-report"}
    stage_key = stage_map.get(stage, "01-setup")

    fragment = get_prompt_fragment("cross-analyze", stage_key)
    if focus and stage == 1:
        fragment = fragment.replace("{ARGS}", focus)
    else:
        fragment = fragment.replace("{ARGS}", "")
    console.print(fragment)


# ============================================================================
# INIT Command
# ============================================================================


@app.command("init")
def init(
    project_name: Optional[str] = typer.Argument(None, help="Project name or '.' for current directory"),
    ai: Optional[str] = typer.Option(None, "--ai", help="AI assistant: claude, copilot, gemini, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, roo, codebuddy, amp, q"),
    here: bool = typer.Option(False, "--here", help="Initialize in current directory"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git initialization"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files"),
) -> None:
    """
    Initialize a new Spec Kit project.

    Creates project structure with embedded launchers - no network required.

    Examples:
        speckitadv init my-project --ai claude
        speckitadv init . --ai copilot
        speckitadv init --here --ai gemini
    """
    from speckit.setup.config import AGENT_CONFIG, get_all_agents
    from speckit.setup.init_cmd import create_project_structure, show_success_message

    # Handle '.' as current directory
    if project_name == ".":
        here = True
        project_name = None

    # Validate arguments
    if here and project_name:
        console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]Error:[/red] Must specify project name, use '.' for current directory, or --here")
        raise typer.Exit(1)

    # Determine project path
    if here:
        project_path = Path.cwd()
        project_name = project_path.name
        is_current_dir = True
    else:
        project_path = Path(project_name).resolve()
        is_current_dir = False

    # Check if directory exists (for new projects)
    if not is_current_dir and project_path.exists():
        console.print(f"[red]Error:[/red] Directory '{project_name}' already exists")
        console.print("Use --here to initialize in an existing directory")
        raise typer.Exit(1)

    # Validate or prompt for AI assistant
    if ai:
        if ai not in AGENT_CONFIG:
            console.print(f"[red]Error:[/red] Unknown AI assistant '{ai}'")
            console.print(f"Available: {', '.join(get_all_agents())}")
            raise typer.Exit(1)
    else:
        # List available agents
        console.print("[bold]Available AI assistants:[/bold]")
        for key, config in AGENT_CONFIG.items():
            console.print(f"  [cyan]{key}[/cyan] - {config['name']}")
        console.print()
        console.print("Use --ai <name> to select an assistant")
        raise typer.Exit(1)

    # Create project
    console.print(f"\n[bold]Initializing project:[/bold] {project_name}")
    console.print(f"[bold]AI assistant:[/bold] {AGENT_CONFIG[ai]['name']}")
    console.print()

    success = create_project_structure(
        project_path=project_path,
        agent=ai,
        no_git=no_git,
        force=force,
    )

    if success:
        show_success_message(project_path, ai, is_current_dir)
    else:
        raise typer.Exit(1)


# ============================================================================
# CHECK Command
# ============================================================================


@app.command("check")
def check(
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    paths_only: bool = typer.Option(False, "--paths-only", help="Only output paths"),
    require_tasks: bool = typer.Option(False, "--require-tasks", help="Require tasks.md to exist"),
    include_tasks: bool = typer.Option(False, "--include-tasks", help="Include tasks content in output"),
) -> None:
    """
    Check that required tools are installed and find feature paths.

    Verifies git and AI agent CLI tools.
    Also discovers current feature directory for workflow commands.
    """
    from speckit.setup.check_cmd import run_check

    _result, success = run_check(
        output_json=json_output,
        paths_only=paths_only,
        require_tasks=require_tasks,
        include_tasks=include_tasks,
    )

    if not success:
        raise typer.Exit(1)


# ============================================================================
# CREATE-FEATURE Command
# ============================================================================


@app.command("create-feature")
def create_feature(
    description: str = typer.Argument(..., help="Feature description"),
    jira: Optional[str] = typer.Option(None, "--jira", "-j", help="JIRA ticket number"),
    short_name: Optional[str] = typer.Option(None, "--short-name", "-s", help="Custom short name (auto-generated if not provided)"),
    number: Optional[int] = typer.Option(None, "--number", "-n", help="Feature number (auto-incremented if not provided)"),
    no_branch: bool = typer.Option(False, "--no-branch", help="Skip git branch creation"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
) -> None:
    """
    Create a new feature branch and spec directory.

    Replaces scripts/bash/create-new-feature.sh with full functionality.

    Examples:
        speckitadv create-feature "Add user authentication"
        speckitadv create-feature "OAuth2 integration" --jira C12345-7890
        speckitadv create-feature "Fix payment bug" --short-name fix-payment --number 5
    """
    from speckit.commands.feature import run_create_feature

    run_create_feature(
        description=description,
        jira=jira,
        short_name=short_name,
        number=number,
        no_branch=no_branch,
        output_json=json_output,
    )


# ============================================================================
# DEBUG Commands
# ============================================================================


@app.command("list-fragments")
def list_fragments_cmd(
    command: str = typer.Argument(..., help="Command name (e.g., analyze-project)"),
) -> None:
    """
    List available prompt fragments for a command.

    Debug utility to inspect available stages.
    """
    from speckit.core.prompts import list_fragments, get_stage_order, count_fragment_lines

    fragments = list_fragments(command)
    ordered = get_stage_order(command)

    console.print(f"\n[bold]Prompt fragments for '{command}':[/bold]\n")

    for stage in ordered:
        lines = count_fragment_lines(command, stage)
        status = "[green]✓[/green]" if lines > 0 else "[red]✗[/red]"
        console.print(f"  {status} {stage} ({lines} lines)")

    console.print(f"\n[dim]Total: {len(fragments)} fragments[/dim]\n")


@app.command("show-fragment")
def show_fragment_cmd(
    command: str = typer.Argument(..., help="Command name"),
    stage: str = typer.Argument(..., help="Stage identifier"),
) -> None:
    """
    Show content of a prompt fragment.

    Debug utility to inspect fragment content.
    """
    from speckit.core.prompts import get_prompt_fragment

    try:
        content = get_prompt_fragment(command, stage)
        console.print(f"\n[bold]Fragment: {command}/{stage}[/bold]\n")
        console.print(content)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


# ============================================================================
# SETUP-PLAN Command
# ============================================================================


@app.command("setup-plan")
def setup_plan(
    arguments: Optional[str] = typer.Option(None, "--arguments", "-a", help="User description to record in plan"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
) -> None:
    """
    Set up plan file from template.

    Copies plan template and prepares feature directory.
    """
    from speckit.commands.workflow import run_setup_plan

    run_setup_plan(arguments=arguments, output_json=json_output)


# ============================================================================
# UPDATE-AGENT-CONTEXT Command
# ============================================================================


@app.command("update-agent-context")
def update_agent_context(
    agent: Optional[str] = typer.Argument(None, help="Agent type: claude, gemini, copilot, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, roo, codebuddy, amp, q"),
) -> None:
    """
    Update agent context files with plan information.

    Parses plan.md and updates agent-specific context files.
    """
    from speckit.commands.workflow import run_update_agent_context

    success = run_update_agent_context(agent_type=agent)
    if not success:
        raise typer.Exit(1)


# ============================================================================
# GENERATE-GUIDELINES Command
# ============================================================================


@app.command("generate-guidelines")
def generate_guidelines(
    sources_path: str = typer.Argument(..., help="Path to folder with docs/ and reference-projects/"),
) -> None:
    """
    Generate coding guidelines from corporate documents and reference projects.

    Analyzes documents and code to extract principles for guidelines.
    """
    from speckit.commands.guidelines import run_generate_guidelines

    success = run_generate_guidelines(sources_path)
    if not success:
        raise typer.Exit(1)


# ============================================================================
# CHECK-ARTIFACTORY Command
# ============================================================================


@app.command("check-artifactory")
def check_artifactory(
    url: str = typer.Argument(..., help="Artifactory URL"),
    library: str = typer.Argument(..., help="Library name to check"),
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="API key (or use ARTIFACTORY_API_KEY env var)"),
    repos: Optional[str] = typer.Option(None, "--repos", "-r", help="Comma-separated repository list"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output"),
) -> None:
    """
    Check if a library is available in Artifactory.

    Validates library availability for dependency whitelisting.
    """
    from speckit.commands.guidelines import check_artifactory as do_check

    exit_code, message = do_check(url, library, api_key, repos, debug)

    if exit_code == 0:
        console.print(f"[green]✅ {message}[/green]")
    elif exit_code == 1:
        console.print(f"[yellow]❌ {message}[/yellow]")
        raise typer.Exit(1)
    elif exit_code == 2:
        console.print(f"[red]⚠️ {message}[/red]")
        raise typer.Exit(2)
    elif exit_code == 4:
        console.print(f"[yellow]⊘ SKIPPED: {message}[/yellow]")
    else:
        console.print(f"[red]⚠️ ERROR: {message}[/red]")
        raise typer.Exit(3)


# ============================================================================
# VERIFY-REPORT Command
# ============================================================================


@app.command("verify-report")
def verify_report(
    report_file: str = typer.Argument(..., help="Path to analysis report file"),
) -> None:
    """
    Verify analysis report meets quality gates.

    Checks for all phases, minimum lines, references, and no placeholders.
    """
    from speckit.commands.project import verify_analysis_report

    success = verify_analysis_report(report_file)
    if not success:
        raise typer.Exit(1)


# ============================================================================
# ENUMERATE-PROJECT Command
# ============================================================================


@app.command("enumerate-project")
def enumerate_project_cmd(
    project_path: str = typer.Argument(".", help="Path to project root"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output JSON file"),
    max_size: int = typer.Option(10485760, "--max-size", help="Maximum file size in bytes (default 10MB)"),
) -> None:
    """
    Enumerate all files in a project for AI analysis.

    Generates a JSON manifest of all files with metadata.
    """
    from speckit.commands.project import enumerate_project

    project = Path(project_path).resolve()
    output_file = Path(output) if output else None

    manifest = enumerate_project(project, output_file, max_size)

    if not output:
        import json
        print(json.dumps(manifest, indent=2))
    else:
        console.print(f"[green]✓[/green] Manifest saved to {output}")
        console.print(f"  Total files: {manifest['statistics']['total_files']}")


# ============================================================================
# CHAIN-STATE Command
# ============================================================================


@app.command("chain-state")
def chain_state(
    command: str = typer.Argument(..., help="Command: generate-id, init, save, load, load-latest, last-stage, is-complete, chain-id, init-state, validate"),
    stage: Optional[str] = typer.Argument(None, help="Stage name or chain ID (for some commands)"),
    state_json: Optional[str] = typer.Option(None, "--state", "-s", help="State JSON (for save/validate)"),
    cmd: Optional[str] = typer.Option(None, "--cmd", help="Workflow command (analyze-project, constitution, specify, plan, tasks, implement)"),
    feature_dir: Optional[str] = typer.Option(None, "--feature-dir", help="Feature directory for feature-scoped commands"),
) -> None:
    """
    Manage chain state for workflow persistence.

    Tracks progress through multi-stage workflows.
    """
    from speckit.commands.chain import run_chain_state_command

    run_chain_state_command(command, stage, state_json, cmd=cmd, feature_dir=feature_dir)


if __name__ == "__main__":
    app()
