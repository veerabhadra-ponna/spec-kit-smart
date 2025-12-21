"""
Agent configuration and launcher templates for speckitadv init.
"""

from pathlib import Path

# Agent configuration with name, folder structure, and CLI requirements
AGENT_CONFIG = {
    "claude": {
        "name": "Claude Code",
        "folder": ".claude",
        "subfolder": "commands",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini",
        "subfolder": "commands",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
    },
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github",
        "subfolder": "prompts",
        "install_url": None,
        "requires_cli": False,
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor",
        "subfolder": "commands",
        "install_url": None,
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen",
        "subfolder": "commands",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode",
        "subfolder": "command",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf",
        "subfolder": "workflows",
        "install_url": None,
        "requires_cli": False,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex",
        "subfolder": "commands",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    },
    "kilocode": {
        "name": "Kilo Code",
        "folder": ".kilocode",
        "subfolder": "rules",
        "install_url": None,
        "requires_cli": False,
    },
    "auggie": {
        "name": "Auggie CLI",
        "folder": ".augment",
        "subfolder": "rules",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
    },
    "roo": {
        "name": "Roo Code",
        "folder": ".roo",
        "subfolder": "rules",
        "install_url": None,
        "requires_cli": False,
    },
    "codebuddy": {
        "name": "CodeBuddy",
        "folder": ".codebuddy",
        "subfolder": "commands",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
    },
    "amp": {
        "name": "Amp",
        "folder": ".agents",
        "subfolder": "commands",
        "install_url": "https://ampcode.com/manual#install",
        "requires_cli": True,
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".amazonq",
        "subfolder": "prompts",
        "install_url": "https://aws.amazon.com/developer/learning/q-developer-cli/",
        "requires_cli": True,
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
]

# Launcher template (3 lines)
LAUNCHER_TEMPLATE = """---
description: {description}
---
Run: `speckitadv {command}`
Follow all instructions in the output.
"""


def get_launcher_content(command: str, description: str) -> str:
    """Generate launcher file content for a command."""
    return LAUNCHER_TEMPLATE.format(command=command, description=description)


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
