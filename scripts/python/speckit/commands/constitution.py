"""
Constitution Command

Creates and manages project constitution with non-negotiable principles.
Implements a 3-stage workflow: gather, structure, finalize.
"""

from pathlib import Path
from typing import Optional

from speckit.core.emit import emit_stage, emit_complete, emit_error
from speckit.core.prompts import get_prompt_fragment, render_prompt, fragment_exists
from speckit.core.templates import get_embedded_template, template_exists
from speckit.core.utils import get_repo_root


# Default principles when --defaults is used
DEFAULT_PRINCIPLES = """
1. Code Quality: All code must pass linting and type checking
2. Testing: Minimum 80% test coverage for new code
3. Documentation: Public APIs must have docstrings
4. Security: No secrets in code, use environment variables
5. Compatibility: Support latest stable version of dependencies
"""

# Stage configuration
TOTAL_STAGES = 3

STAGE_MAP = {
    1: "01-gather-principles",
    2: "02-structure",
    3: "03-finalize",
}


def run_constitution(
    stage: int = 1,
    principles: Optional[str] = None,
    defaults: bool = False,
) -> None:
    """
    Execute constitution workflow at specified stage.

    Stage 1: Gather principles (from user or defaults)
    Stage 2: Structure into formal constitution format
    Stage 3: Finalize and write constitution file

    Args:
        stage: Current workflow stage (1-3)
        principles: User-provided principles text
        defaults: Use default principles
    """
    # Validate stage
    if stage < 1 or stage > TOTAL_STAGES:
        emit_error(
            "Invalid stage",
            f"Stage must be between 1 and {TOTAL_STAGES}",
            recovery_cmd="speckitadv constitution --stage=1",
        )
        return

    # Determine project root
    repo_root = get_repo_root()
    if not repo_root:
        repo_root = Path.cwd()

    # Build context
    context = {
        "stage": stage,
        "total_stages": TOTAL_STAGES,
        "project_path": str(repo_root),
        "principles": "",
    }

    # Handle principles input
    if defaults:
        context["principles"] = DEFAULT_PRINCIPLES.strip()
    elif principles:
        context["principles"] = principles

    # Stage 1: Gather principles
    if stage == 1:
        _emit_stage_1(context)
        return

    # Stage 2: Structure principles
    if stage == 2:
        if not context["principles"]:
            emit_error(
                "No principles provided",
                "Stage 2 requires principles from stage 1",
                recovery_cmd="speckitadv constitution --stage=1 --defaults",
            )
            return
        _emit_stage_2(context)
        return

    # Stage 3: Finalize
    if stage == 3:
        _emit_stage_3(context)
        return


def _emit_stage_1(context: dict) -> None:
    """Stage 1: Gather project principles."""
    content = """# Gather Project Principles

You are creating a project constitution - the non-negotiable rules.

## Task

Review the project and identify core principles:

1. **Code Standards**
   - Linting rules
   - Type checking requirements
   - Naming conventions

2. **Quality Gates**
   - Test coverage requirements
   - Documentation requirements
   - Review requirements

3. **Security Requirements**
   - Secret handling
   - Dependency policies
   - Access controls

4. **Architecture Constraints**
   - Required patterns
   - Forbidden anti-patterns
   - Integration rules

## Output

List 5-10 non-negotiable principles for this project.
Format each as: "CATEGORY: Principle statement"

## Example

```
CODE_QUALITY: All functions must have type hints
TESTING: No PR merges without 80% coverage
SECURITY: No hardcoded secrets, use .env files
```
"""

    emit_stage(
        stage_num=1,
        total_stages=context["total_stages"],
        title="Gather Project Principles",
        content=content,
        next_cmd="speckitadv constitution --stage=2 --principles='<paste-principles-here>'",
        alt_cmd="speckitadv constitution --stage=2 --defaults",
    )


def _emit_stage_2(context: dict) -> None:
    """Stage 2: Structure principles into constitution format."""
    principles = context.get("principles", "")

    content = f"""# Structure Constitution

Take the gathered principles and structure them formally.

## Input Principles

{principles}

## Task

Create a formal constitution with:

1. **Preamble** - Project mission and scope
2. **Article I: Code Standards** - Formatting, linting, types
3. **Article II: Quality Gates** - Testing, coverage, reviews
4. **Article III: Security** - Secrets, dependencies, access
5. **Article IV: Architecture** - Patterns, constraints
6. **Article V: Amendments** - How to update this constitution

## Format

Use this markdown structure:

```markdown
# Project Constitution

## Preamble
[Project mission]

## Article I: Code Standards
- 1.1 [First principle]
- 1.2 [Second principle]

## Article II: Quality Gates
...
```

## Output

Write the complete constitution to: `.speckit/constitution.md`
"""

    emit_stage(
        stage_num=2,
        total_stages=context["total_stages"],
        title="Structure Constitution",
        content=content,
        next_cmd="speckitadv constitution --stage=3",
    )


def _emit_stage_3(context: dict) -> None:
    """Stage 3: Finalize and verify constitution."""
    content = """# Finalize Constitution

Review and finalize the constitution.

## Task

1. **Read** `.speckit/constitution.md`
2. **Verify** all principles are covered
3. **Check** formatting is consistent
4. **Add** timestamp and version

## Required Additions

Add this footer to the constitution:

```markdown
---

## Metadata

- Version: 1.0.0
- Created: [DATE]
- Last Updated: [DATE]
- Approved By: [NAME or "Pending Review"]
```

## Validation Checklist

- [ ] All 5 articles present
- [ ] Each article has at least 2 principles
- [ ] Language is clear and unambiguous
- [ ] No contradictions between principles
- [ ] Metadata section added

## Output

Confirm the constitution is complete and ready for use.
"""

    emit_stage(
        stage_num=3,
        total_stages=context["total_stages"],
        title="Finalize Constitution",
        content=content,
        next_cmd=None,  # Workflow complete
    )


# Export for CLI
constitution = run_constitution
