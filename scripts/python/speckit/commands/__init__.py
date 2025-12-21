"""
Spec Kit Smart Commands

Each command implements a progressive workflow with staged prompt injection.
"""

from speckit.commands.constitution import constitution
from speckit.commands.analyze import analyze_project

__all__ = ["constitution", "analyze_project"]
