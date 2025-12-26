"""
Interactive Mode Support

Provides interactive prompts for CLI commands when arguments are not provided.
Matches the interactive mode patterns from original main branch prompts.
"""

import re
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

console = Console()


def collect_specify_input() -> tuple[Optional[str], Optional[str]]:
    """
    Collect JIRA number and feature description interactively.

    Returns:
        Tuple of (jira_number, feature_description)
    """
    console.print(Panel.fit(
        "[bold]Interactive Mode[/bold]\n\n"
        "Please provide the following information:",
        title="[cyan]Specify[/cyan]",
    ))

    console.print("\n[bold]Format:[/bold]")
    console.print("  JIRA: C12345-7890 (optional - press Enter to skip)")
    console.print("  FEATURE: <your description> (required)")

    console.print("\n[bold]Good feature descriptions:[/bold]")
    console.print('  [green][ok][/green] "Add user authentication with email/password and OAuth2"')
    console.print('  [green][ok][/green] "Create analytics dashboard showing user signups and revenue"')
    console.print('  [green][ok][/green] "Implement CSV export for transaction history"')

    console.print("\n[bold]Bad feature descriptions (too vague):[/bold]")
    console.print('  [red][x][/red] "Make it better"')
    console.print('  [red][x][/red] "Add security"')
    console.print('  [red][x][/red] "Improve UI"\n')

    # Collect JIRA
    jira = Prompt.ask(
        "[bold]JIRA[/bold]",
        default="",
    )

    # Validate JIRA format if provided
    if jira and not re.match(r"^C\d{5}-\d{4}$", jira):
        console.print(f"[yellow]Warning:[/yellow] JIRA '{jira}' doesn't match expected format C12345-7890")
        if not Confirm.ask("Continue anyway?", default=False):
            return None, None

    # Collect feature description
    feature = Prompt.ask(
        "[bold]FEATURE[/bold]",
        default="",
    )

    if not feature:
        console.print("[red]Error:[/red] Feature description is required")
        return None, None

    return jira if jira else None, feature


def collect_plan_constraints() -> str:
    """
    Collect planning constraints interactively.

    Returns:
        Constraints string, or "$SKIP" if user chooses to skip
    """
    console.print(Panel.fit(
        "[bold]Planning Constraints[/bold]\n\n"
        "Provide any additional constraints for the implementation plan.",
        title="[cyan]Plan[/cyan]",
    ))

    console.print("\n[bold]Examples of valid constraints:[/bold]")
    console.print('  [green]*[/green] Technology: "Must use PostgreSQL", "Prefer Redis for caching"')
    console.print('  [green]*[/green] Architecture: "Prefer microservices", "Use event-driven architecture"')
    console.print('  [green]*[/green] Performance: "< 200ms response time", "Support 10,000 concurrent users"')
    console.print('  [green]*[/green] Integration: "Must integrate with existing auth system"')
    console.print('  [green]*[/green] Compliance: "Must be GDPR compliant", "PII must be encrypted at rest"')
    console.print('\n  Type "none" to proceed without additional constraints.\n')

    response = Prompt.ask(
        "[bold]CONSTRAINTS[/bold]",
        default="none",
    )

    if response.lower() == "none":
        console.print("[dim]Proceeding with standard best practices from the specification.[/dim]\n")
        return "$SKIP"

    return response


def collect_tasks_preferences() -> str:
    """
    Collect task generation preferences interactively.

    Returns:
        Preferences string, or "$SKIP" if user chooses to skip
    """
    console.print(Panel.fit(
        "[bold]Task Generation Preferences[/bold]\n\n"
        "Provide any preferences for how tasks should be generated.",
        title="[cyan]Tasks[/cyan]",
    ))

    console.print("\n[bold]Examples of valid preferences:[/bold]")
    console.print('  [green]*[/green] Task size: "Break into smaller tasks (< 2 hours each)"')
    console.print('  [green]*[/green] Grouping: "Group by feature area rather than technical layer"')
    console.print('  [green]*[/green] Priority: "Prioritize backend before frontend", "Focus on P1 and P2 only"')
    console.print('  [green]*[/green] Scope: "Include database migration tasks separately"')
    console.print('  [green]*[/green] Detail level: "Include detailed sub-tasks", "Keep high-level only"')
    console.print('\n  Type "none" to use standard task breakdown.\n')

    response = Prompt.ask(
        "[bold]PREFERENCES[/bold]",
        default="none",
    )

    if response.lower() == "none":
        console.print("[dim]Using standard task breakdown by user story with default sizing.[/dim]\n")
        return "$SKIP"

    return response


def collect_implement_notes() -> str:
    """
    Collect implementation notes interactively.

    Returns:
        Notes string, or "$SKIP" if user chooses to skip
    """
    console.print(Panel.fit(
        "[bold]Implementation Notes[/bold]\n\n"
        "Provide any notes to guide the implementation.",
        title="[cyan]Implement[/cyan]",
    ))

    console.print("\n[bold]Examples of valid notes:[/bold]")
    console.print('  [green]*[/green] Execution order: "Start with database migration first"')
    console.print('  [green]*[/green] Scope: "Focus on P1 user stories only", "Skip optional features for MVP"')
    console.print('  [green]*[/green] Testing: "Write tests first", "Skip tests for now (exploratory spike)"')
    console.print('  [green]*[/green] Priorities: "Prioritize error handling", "Focus on security validation"')
    console.print('  [green]*[/green] Constraints: "Use existing utility functions where possible"')
    console.print('\n  Type "none" to proceed with standard implementation.\n')

    response = Prompt.ask(
        "[bold]NOTES[/bold]",
        default="none",
    )

    if response.lower() == "none":
        console.print("[dim]Executing the task plan using standard best practices.[/dim]\n")
        return "$SKIP"

    return response


def collect_analyze_focus() -> str:
    """
    Collect analysis focus areas interactively.

    Returns:
        Focus string, or "$SKIP" for comprehensive analysis
    """
    console.print(Panel.fit(
        "[bold]Analysis Focus[/bold]\n\n"
        "What should the cross-artifact analysis prioritize?",
        title="[cyan]Analyze[/cyan]",
    ))

    console.print("\n[bold]Examples of valid focus areas:[/bold]")
    console.print('  [green]*[/green] Security: "Focus on security requirements coverage"')
    console.print('  [green]*[/green] Compliance: "Check constitution compliance carefully"')
    console.print('  [green]*[/green] Testing: "Verify all user stories have acceptance tests"')
    console.print('  [green]*[/green] Performance: "Look for performance bottlenecks"')
    console.print('  [green]*[/green] Data: "Check data model consistency"')
    console.print('\n  Type "none" for comprehensive analysis.\n')

    response = Prompt.ask(
        "[bold]FOCUS[/bold]",
        default="none",
    )

    if response.lower() == "none":
        console.print("[dim]Running comprehensive cross-artifact analysis.[/dim]\n")
        return "$SKIP"

    return response


def collect_analyze_project_input() -> dict:
    """
    Collect analyze-project inputs interactively.

    Returns:
        Dict with path, scope, context, and concern details
    """
    result = {
        "path": None,
        "scope": None,
        "context": None,
        "concern_type": None,
        "current_impl": None,
        "target_impl": None,
    }

    # Input 1: Project Path
    console.print(Panel.fit(
        "[bold]PROJECT PATH[/bold]\n\n"
        "Please provide the absolute path to the existing project\n"
        "you want to analyze.\n\n"
        "[dim]Examples:[/dim]\n"
        "  Linux/Mac: /home/user/my-legacy-app\n"
        "  Windows:   C:\\Users\\user\\my-legacy-app",
        title="[cyan]Analyze Project[/cyan]",
    ))

    while True:
        path = Prompt.ask("\n[bold]Your path[/bold]", default=".")
        project_path = Path(path).resolve()

        if not project_path.exists():
            console.print(f"[red]Error:[/red] Path does not exist: {project_path}")
            continue
        if not project_path.is_dir():
            console.print(f"[red]Error:[/red] Not a directory: {project_path}")
            continue

        result["path"] = str(project_path)
        break

    # Input 2: Additional Context
    console.print(Panel.fit(
        "[bold]ADDITIONAL CONTEXT[/bold] (Optional)\n\n"
        "Do you want to provide any additional context to help\n"
        "with the analysis?\n\n"
        "[dim]This could include:[/dim]\n"
        "  * Known pain points or issues\n"
        "  * Business requirements or constraints\n"
        "  * Deployment environment details\n"
        "  * Team preferences or standards\n\n"
        "Type your context below, or 'none' to skip:",
        title="[cyan]Context[/cyan]",
    ))

    context = Prompt.ask("\n[bold]Context[/bold]", default="none")
    if context.lower() != "none":
        result["context"] = context

    # Input 3: Analysis Scope
    console.print(Panel.fit(
        "[bold]ANALYSIS SCOPE[/bold]\n\n"
        "[bold][A][/bold] Full Application Modernization\n"
        "    -> Analyze entire codebase comprehensively\n"
        "    -> Generate complete functional/technical specs\n"
        "    -> Suitable for legacy app migration\n\n"
        "[bold][B][/bold] Cross-Cutting Concern Migration\n"
        "    -> Analyze entire application context FIRST\n"
        "    -> THEN deep-dive into specific concern\n"
        "    -> Suitable for: auth migration, database swap,\n"
        "                    caching layer, observability, etc.",
        title="[cyan]Scope[/cyan]",
    ))

    while True:
        scope = Prompt.ask("\n[bold]Your choice [A/B][/bold]", default="A")
        scope = scope.upper()
        if scope in ("A", "B"):
            result["scope"] = scope
            break
        console.print("[red]Invalid selection.[/red] Please choose [A] or [B].")

    # Input 4: Concern Details (only if scope B)
    if result["scope"] == "B":
        console.print(Panel.fit(
            "[bold]CONCERN DETAILS[/bold]\n\n"
            "You selected Cross-Cutting Concern Migration.\n"
            "Please provide details about the concern:\n\n"
            "[dim]Examples of concern types:[/dim]\n"
            "  * Authentication/Authorization\n"
            "  * Database/ORM Layer\n"
            "  * Caching Layer\n"
            "  * Message Bus/Queue\n"
            "  * Logging/Observability",
            title="[cyan]Concern[/cyan]",
        ))

        result["concern_type"] = Prompt.ask("\n[bold]Concern type[/bold]")
        result["current_impl"] = Prompt.ask("[bold]Current implementation[/bold]", default="")
        result["target_impl"] = Prompt.ask("[bold]Target implementation[/bold]")

    return result
