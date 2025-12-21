#!/usr/bin/env python3
"""
Generate launcher files for all AI agents.

Creates minimal 3-line launcher files that invoke the speckitadv CLI.
"""

from pathlib import Path

# Commands and their descriptions
COMMANDS = {
    "analyze-project": "Analyze existing project for modernization",
    "analyze": "Analyze existing project (alias)",
    "constitution": "Create project constitution with guiding principles",
    "specify": "Create baseline specification from requirements",
    "plan": "Create implementation plan from specification",
    "tasks": "Generate actionable tasks from plan",
    "implement": "Execute implementation with quality checks",
    "clarify": "Ask structured clarification questions",
    "checklist": "Generate quality validation checklist",
    "orchestrate": "Orchestrate complete spec-driven workflow",
    "resume": "Resume workflow from saved state",
}

# Agent configurations
MARKDOWN_AGENTS = {
    "claude": ".claude/commands",
    "copilot": ".github/prompts",
    "cursor": ".cursor/commands",
    "opencode": ".opencode/command",
    "codex": ".codex/commands",
    "windsurf": ".windsurf/workflows",
    "kilocode": ".kilocode/rules",
    "auggie": ".augment/rules",
    "roo": ".roo/rules",
    "codebuddy": ".codebuddy/commands",
    "amazonq": ".amazonq/prompts",
    "amp": ".agents/commands",
}

TOML_AGENTS = {
    "gemini": ".gemini/commands",
    "qwen": ".qwen/commands",
}


def markdown_launcher(command: str, description: str) -> str:
    """Generate markdown launcher content."""
    return f"""---
description: {description}
---
Run: speckitadv {command} $ARGUMENTS
"""


def toml_launcher(command: str, description: str) -> str:
    """Generate TOML launcher content."""
    return f'''description = "{description}"
prompt = "Run: speckitadv {command} {{{{args}}}}"
'''


def main():
    base_dir = Path(__file__).parent.parent / "launchers"
    base_dir.mkdir(exist_ok=True)

    # Generate markdown launchers
    for agent, dest_path in MARKDOWN_AGENTS.items():
        agent_dir = base_dir / agent
        agent_dir.mkdir(exist_ok=True)

        for command, description in COMMANDS.items():
            launcher_file = agent_dir / f"{command}.md"
            launcher_file.write_text(markdown_launcher(command, description))

        print(f"Generated {len(COMMANDS)} launchers for {agent} → {dest_path}")

    # Generate TOML launchers
    for agent, dest_path in TOML_AGENTS.items():
        agent_dir = base_dir / agent
        agent_dir.mkdir(exist_ok=True)

        for command, description in COMMANDS.items():
            launcher_file = agent_dir / f"{command}.toml"
            launcher_file.write_text(toml_launcher(command, description))

        print(f"Generated {len(COMMANDS)} launchers for {agent} → {dest_path}")

    total = len(COMMANDS) * (len(MARKDOWN_AGENTS) + len(TOML_AGENTS))
    print(f"\nTotal: {total} launcher files generated")


if __name__ == "__main__":
    main()
