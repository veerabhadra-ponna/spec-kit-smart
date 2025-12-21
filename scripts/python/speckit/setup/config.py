"""
Agent configuration and launcher templates for speckitadv init.
"""

from pathlib import Path

# Agent configuration with name, folder structure, CLI requirements, and launcher format
AGENT_CONFIG = {
    "claude": {
        "name": "Claude Code",
        "folder": ".claude",
        "subfolder": "commands",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
        "launcher_format": "markdown",  # YAML frontmatter
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini",
        "subfolder": "commands",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
        "launcher_format": "toml",  # Gemini uses TOML commands
        "launcher_ext": ".toml",
    },
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github",
        "subfolder": "prompts",
        "install_url": None,
        "requires_cli": False,
        "launcher_format": "markdown",
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor",
        "subfolder": "commands",
        "install_url": None,
        "requires_cli": False,
        "launcher_format": "markdown",
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen",
        "subfolder": "commands",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
        "launcher_format": "toml",  # Qwen uses TOML commands
        "launcher_ext": ".toml",
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode",
        "subfolder": "command",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
        "launcher_format": "markdown",
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf",
        "subfolder": "workflows",
        "install_url": None,
        "requires_cli": False,
        "launcher_format": "markdown",
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex",
        "subfolder": "commands",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
        "launcher_format": "markdown",
    },
    "kilocode": {
        "name": "Kilo Code",
        "folder": ".kilocode",
        "subfolder": "rules",
        "install_url": None,
        "requires_cli": False,
        "launcher_format": "markdown",
    },
    "auggie": {
        "name": "Auggie CLI",
        "folder": ".augment",
        "subfolder": "rules",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
        "launcher_format": "markdown",
    },
    "roo": {
        "name": "Roo Code",
        "folder": ".roo",
        "subfolder": "rules",
        "install_url": None,
        "requires_cli": False,
        "launcher_format": "markdown",
    },
    "codebuddy": {
        "name": "CodeBuddy",
        "folder": ".codebuddy",
        "subfolder": "commands",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
        "launcher_format": "markdown",
    },
    "amp": {
        "name": "Amp",
        "folder": ".agents",
        "subfolder": "commands",
        "install_url": "https://ampcode.com/manual#install",
        "requires_cli": True,
        "launcher_format": "markdown",
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".amazonq",
        "subfolder": "prompts",
        "install_url": "https://aws.amazon.com/developer/learning/q-developer-cli/",
        "requires_cli": True,
        "launcher_format": "markdown",
    },
}

# Workflow commands with descriptions
WORKFLOW_COMMANDS = [
    ("analyze-project", "Analyze existing project for modernization"),
    ("constitution", "Create or update project constitution"),
    ("specify", "Create baseline specification"),
    ("plan", "Create implementation plan"),
    ("clarify", "Ask structured questions"),
    ("tasks", "Generate actionable tasks"),
    ("implement", "Execute implementation"),
    ("checklist", "Generate quality checklist"),
    ("analyze", "Cross-artifact consistency check"),
    ("orchestrate", "Orchestrate complete spec-driven workflow"),
    ("resume", "Resume workflow from saved state"),
    ("generate-guidelines", "Generate corporate coding guidelines"),
]

# Launcher templates by format
LAUNCHER_TEMPLATE_MARKDOWN = """---
description: {description}
---
Run: `speckitadv {command}`
Follow all instructions in the output.
"""

LAUNCHER_TEMPLATE_TOML = """# {description}
[command]
description = "{description}"
command = "speckitadv {command}"

[instructions]
run = "Execute the command above"
follow = "Follow all instructions in the output"
"""


def get_launcher_content(command: str, description: str, format: str = "markdown") -> str:
    """Generate launcher file content for a command."""
    if format == "toml":
        return LAUNCHER_TEMPLATE_TOML.format(command=command, description=description)
    return LAUNCHER_TEMPLATE_MARKDOWN.format(command=command, description=description)


def get_launcher_extension(agent: str) -> str:
    """Get the launcher file extension for an agent."""
    config = AGENT_CONFIG.get(agent, {})
    return config.get("launcher_ext", ".md")


def get_launcher_format(agent: str) -> str:
    """Get the launcher format for an agent."""
    config = AGENT_CONFIG.get(agent, {})
    return config.get("launcher_format", "markdown")


def get_agent_commands_path(agent: str) -> tuple[str, str]:
    """
    Get the folder and subfolder for an agent's commands.

    Returns:
        Tuple of (folder, subfolder) e.g. (".claude", "commands")
    """
    config = AGENT_CONFIG.get(agent)
    if not config:
        raise ValueError(f"Unknown agent: {agent}")
    return config["folder"], config["subfolder"]


def get_all_agents() -> list[str]:
    """Get list of all supported agent keys."""
    return list(AGENT_CONFIG.keys())
