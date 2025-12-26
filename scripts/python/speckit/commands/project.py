"""
Project analysis commands for speckitadv.

Ports functionality from:
- analyze-project.sh
- enumerate-project.sh
- verify-analysis-report.sh
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from speckit.core.utils import find_repo_root

console = Console()


def get_file_size(filepath: Path) -> int:
    """Get file size in bytes."""
    try:
        return filepath.stat().st_size
    except (OSError, IOError):
        return 0


def get_file_extension(filepath: Path) -> str:
    """Get file extension including dot."""
    suffix = filepath.suffix
    return suffix if suffix else ""


def get_file_category(extension: str) -> str:
    """Categorize file by extension."""
    ext = extension.lstrip(".").lower()

    CODE_EXTS = {
        "js", "ts", "jsx", "tsx", "mjs", "cjs",
        "cs", "fs", "vb",
        "java", "kt", "scala", "groovy",
        "py", "pyw", "pyx",
        "rb", "rake", "gemspec",
        "go", "rs", "php", "phtml",
        "c", "cpp", "cc", "cxx", "h", "hpp",
        "swift", "m", "mm",
    }

    CONFIG_EXTS = {
        "json", "yaml", "yml", "toml", "ini", "conf", "config",
        "xml", "plist", "env", "properties",
    }

    if ext in CODE_EXTS:
        return "code"
    if ext in {"html", "htm", "xhtml"}:
        return "markup"
    if ext in {"css", "scss", "sass", "less"}:
        return "style"
    if ext in {"vue", "svelte"}:
        return "component"
    if ext in CONFIG_EXTS:
        return "config"
    if ext in {"csproj", "sln", "fsproj", "vbproj", "gradle", "pom"}:
        return "project"
    if ext == "lock":
        return "lockfile"
    if ext in {"sql", "psql", "mysql"}:
        return "database"
    if ext in {"sh", "bash", "zsh", "fish", "ps1", "psm1", "psd1", "bat", "cmd"}:
        return "script"
    if ext in {"md", "markdown", "txt", "rst", "adoc"}:
        return "documentation"
    if ext in {"csv", "tsv", "dat"}:
        return "data"
    if ext in {"dll", "exe", "so", "dylib", "a", "o", "obj", "pdb", "class", "jar", "war", "ear", "pyc", "pyo"}:
        return "binary"
    if ext in {"jpg", "jpeg", "png", "gif", "svg", "ico", "webp", "bmp"}:
        return "image"
    if ext in {"zip", "tar", "gz", "bz2", "xz", "7z", "rar"}:
        return "archive"
    if not ext:
        return "no_extension"
    return "other"


def is_binary_file(filepath: Path) -> bool:
    """Check if file is binary by looking for null bytes."""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(8192)
            return b"\x00" in chunk
    except (OSError, IOError):
        return False


def enumerate_project(
    project_path: Path,
    output_file: Optional[Path] = None,
    max_file_size: int = 10 * 1024 * 1024,
    show_progress: bool = True,
) -> dict:
    """
    Enumerate all files in a project directory.

    Args:
        project_path: Path to project root
        output_file: Optional output file for JSON manifest
        max_file_size: Maximum file size to include (default 10MB)
        show_progress: Show progress output

    Returns:
        Dictionary with file manifest
    """
    project_path = project_path.resolve()
    scan_start = datetime.utcnow().isoformat() + "Z"

    files = []
    statistics = {
        "total_files": 0,
        "total_size_bytes": 0,
        "binary_files": 0,
        "oversized_files": 0,
        "unreadable_files": 0,
        "by_category": {},
        "by_extension": {},
        "largest_files": [],
    }

    file_count = 0

    for root, dirs, filenames in os.walk(project_path):
        # Skip hidden directories and common build artifacts
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {
            "node_modules", "bin", "obj", "target", "build", "dist",
            "__pycache__", "venv", ".venv", ".git",
        }]

        for filename in filenames:
            filepath = Path(root) / filename
            file_count += 1

            if show_progress and file_count % 100 == 0:
                console.print(f"[dim]Scanned {file_count} files...[/dim]")

            rel_path = str(filepath.relative_to(project_path))
            size = get_file_size(filepath)
            ext = get_file_extension(filepath)
            category = get_file_category(ext)

            # Track statistics
            statistics["total_files"] += 1
            statistics["total_size_bytes"] += size
            statistics["by_category"][category] = statistics["by_category"].get(category, 0) + 1
            if ext:
                statistics["by_extension"][ext] = statistics["by_extension"].get(ext, 0) + 1

            # Determine file properties
            readable = filepath.is_file() and os.access(filepath, os.R_OK)
            skip_reason = ""

            if not readable:
                statistics["unreadable_files"] += 1
                skip_reason = "permission_denied"
                is_bin = False
                size_category = "normal"
            elif size > max_file_size:
                statistics["oversized_files"] += 1
                skip_reason = "exceeds_max_size"
                is_bin = False
                size_category = "oversized"
            elif category in {"binary", "image", "archive"}:
                statistics["binary_files"] += 1
                is_bin = True
                size_category = "normal"
            elif is_binary_file(filepath):
                statistics["binary_files"] += 1
                is_bin = True
                size_category = "normal"
            else:
                is_bin = False
                if size < 10240:
                    size_category = "tiny"
                elif size < 102400:
                    size_category = "small"
                elif size < 1048576:
                    size_category = "medium"
                else:
                    size_category = "large"

            file_entry = {
                "path": rel_path,
                "absolute_path": str(filepath),
                "size_bytes": size,
                "extension": ext,
                "category": category,
                "size_category": size_category,
                "is_binary": is_bin,
                "readable": readable,
                "skip_reason": skip_reason,
            }
            files.append(file_entry)

            # Track largest files
            if len(statistics["largest_files"]) < 10:
                statistics["largest_files"].append({"path": rel_path, "size_bytes": size})
                statistics["largest_files"].sort(key=lambda x: x["size_bytes"], reverse=True)
            elif size > statistics["largest_files"][-1]["size_bytes"]:
                statistics["largest_files"][-1] = {"path": rel_path, "size_bytes": size}
                statistics["largest_files"].sort(key=lambda x: x["size_bytes"], reverse=True)

    scan_end = datetime.utcnow().isoformat() + "Z"

    manifest = {
        "scan_info": {
            "project_path": str(project_path),
            "scanner": "python-speckitadv",
            "script_version": "2.0.0",
            "scan_start": scan_start,
            "scan_end": scan_end,
            "max_file_size_bytes": max_file_size,
        },
        "files": files,
        "statistics": statistics,
    }

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    return manifest


def detect_tech_stack(manifest: dict, project_path: Path) -> dict:
    """Detect technology stack from project files."""
    tech_stack = {
        "schema_version": "1.0",
        "languages": [],
        "frameworks": {"backend": [], "frontend": []},
        "build_tools": [],
        "databases": [],
        "indicators_found": [],
    }

    files_by_name = {f["path"]: f for f in manifest.get("files", [])}

    # Node.js / JavaScript
    if any(f.endswith("package.json") for f in files_by_name):
        tech_stack["languages"].append("javascript")
        tech_stack["indicators_found"].append({
            "file": "package.json",
            "type": "nodejs",
            "confidence": "high",
        })

        # Check for frameworks
        for path in files_by_name:
            if path.endswith("package.json"):
                pkg_file = project_path / path
                if pkg_file.exists():
                    try:
                        content = pkg_file.read_text(encoding="utf-8")
                        if '"react"' in content:
                            tech_stack["frameworks"]["frontend"].append("react")
                        if '"express"' in content:
                            tech_stack["frameworks"]["backend"].append("express")
                        if '"next"' in content:
                            tech_stack["frameworks"]["frontend"].append("nextjs")
                    except (OSError, IOError):
                        pass
                break

    # Java / Maven
    if any(f.endswith("pom.xml") for f in files_by_name):
        tech_stack["languages"].append("java")
        tech_stack["build_tools"].append("maven")
        tech_stack["indicators_found"].append({
            "file": "pom.xml",
            "type": "java-maven",
            "confidence": "high",
        })

    # Java / Gradle
    if any(f.endswith("build.gradle") or f.endswith("build.gradle.kts") for f in files_by_name):
        if "java" not in tech_stack["languages"]:
            tech_stack["languages"].append("java")
        tech_stack["build_tools"].append("gradle")
        tech_stack["indicators_found"].append({
            "file": "build.gradle",
            "type": "java-gradle",
            "confidence": "high",
        })

    # Python
    if any(f.endswith(("requirements.txt", "setup.py", "pyproject.toml")) for f in files_by_name):
        tech_stack["languages"].append("python")
        tech_stack["indicators_found"].append({
            "file": "requirements.txt",
            "type": "python",
            "confidence": "high",
        })

        for path in files_by_name:
            if path.endswith("requirements.txt"):
                req_file = project_path / path
                if req_file.exists():
                    try:
                        content = req_file.read_text(encoding="utf-8").lower()
                        if "django" in content:
                            tech_stack["frameworks"]["backend"].append("django")
                        if "flask" in content:
                            tech_stack["frameworks"]["backend"].append("flask")
                    except (OSError, IOError):
                        pass
                break

    # .NET
    if any(f.endswith((".csproj", ".sln")) for f in files_by_name):
        tech_stack["languages"].append("csharp")
        tech_stack["build_tools"].append("dotnet")
        tech_stack["indicators_found"].append({
            "file": "*.csproj",
            "type": "dotnet",
            "confidence": "high",
        })

    # Ruby
    if any(f.endswith("Gemfile") for f in files_by_name):
        tech_stack["languages"].append("ruby")
        tech_stack["indicators_found"].append({
            "file": "Gemfile",
            "type": "ruby",
            "confidence": "high",
        })

    # Go
    if any(f.endswith("go.mod") for f in files_by_name):
        tech_stack["languages"].append("go")
        tech_stack["indicators_found"].append({
            "file": "go.mod",
            "type": "golang",
            "confidence": "high",
        })

    # Rust
    if any(f.endswith("Cargo.toml") for f in files_by_name):
        tech_stack["languages"].append("rust")
        tech_stack["indicators_found"].append({
            "file": "Cargo.toml",
            "type": "rust",
            "confidence": "high",
        })

    # Remove duplicates
    tech_stack["languages"] = list(set(tech_stack["languages"]))
    tech_stack["frameworks"]["backend"] = list(set(tech_stack["frameworks"]["backend"]))
    tech_stack["frameworks"]["frontend"] = list(set(tech_stack["frameworks"]["frontend"]))
    tech_stack["build_tools"] = list(set(tech_stack["build_tools"]))

    return tech_stack


def generate_file_structure(manifest: dict) -> dict:
    """Analyze file structure and categorize files."""
    files = manifest.get("files", [])

    categories = {
        "controllers": 0,
        "services": 0,
        "models": 0,
        "repositories": 0,
        "configs": 0,
        "security": 0,
        "middleware": 0,
        "utils": 0,
        "tests": 0,
        "docs": 0,
    }

    entry_points = []

    import re

    for f in files:
        path = f["path"].lower()

        if re.search(r"(controller|route|endpoint)", path):
            categories["controllers"] += 1
        if re.search(r"(service|manager|handler|usecase)", path):
            categories["services"] += 1
        if re.search(r"(model|entity|schema|domain)", path):
            categories["models"] += 1
        if re.search(r"(repository|repo|dao|data)", path):
            categories["repositories"] += 1
        if re.search(r"(config|settings|properties|yml|yaml|env)", path):
            categories["configs"] += 1
        if re.search(r"(auth|security|jwt|oauth|permission)", path):
            categories["security"] += 1
        if "middleware" in path:
            categories["middleware"] += 1
        if re.search(r"(util|helper|common|shared)", path):
            categories["utils"] += 1
        if re.search(r"(test|spec|__tests__)", path):
            categories["tests"] += 1
        if re.search(r"(readme|changelog|license|\.md$)", path):
            categories["docs"] += 1

        # Check for entry points
        if re.search(r"(main\.|index\.|app\.|application\.|server\.|start)", path):
            entry_points.append(f["path"])

    return {
        "schema_version": "1.0",
        "total_files": len(files),
        "categories": categories,
        "entry_points": entry_points[:10],  # Limit to 10
        "analysis_priority": {
            "critical": ["configs", "security", "entry_points"],
            "high": ["controllers", "services", "models", "repositories"],
            "medium": ["middleware", "utils"],
            "low": ["tests", "docs"],
        },
    }


def run_analyze_project_setup(
    project_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    context: Optional[str] = None,
    scope: Optional[str] = None,
    concern_type: Optional[str] = None,
    current_impl: Optional[str] = None,
    target_impl: Optional[str] = None,
) -> dict:
    """
    Set up analysis workspace for a project.

    Replaces analyze-project.sh functionality.

    Returns:
        Dictionary with workspace information
    """
    # Resolve paths
    project = Path(project_path).resolve() if project_path else Path.cwd()
    repo_root = find_repo_root(project)

    if not project.is_dir():
        console.print(f"[red]Error:[/red] Project path does not exist: {project}")
        return {"success": False, "error": "Project path not found"}

    project_name = project.name
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    # Determine output directory
    if output_dir:
        analysis_dir = Path(output_dir)
    else:
        analysis_dir = repo_root / ".analysis" / f"{project_name}-{timestamp}"

    analysis_dir.mkdir(parents=True, exist_ok=True)
    (analysis_dir / "checkpoints").mkdir(exist_ok=True)

    console.print(Panel(f"[bold]Project Analysis Setup[/bold]\n\nProject: {project}\nOutput: {analysis_dir}"))

    # Step 1: Enumerate files
    console.print("\n[bold]Step 1: Enumerating files...[/bold]")
    manifest_file = analysis_dir / "file-manifest.json"
    manifest = enumerate_project(project, manifest_file, show_progress=True)
    console.print(f"[green][ok][/green] Scanned {manifest['statistics']['total_files']} files")

    # Step 2: Detect tech stack
    console.print("\n[bold]Step 2: Detecting technology stack...[/bold]")
    tech_stack = detect_tech_stack(manifest, project)
    tech_stack_file = analysis_dir / "tech-stack.json"
    with open(tech_stack_file, "w", encoding="utf-8") as f:
        json.dump(tech_stack, f, indent=2)
    if tech_stack["languages"]:
        console.print(f"[green][ok][/green] Detected: {', '.join(tech_stack['languages'])}")
    else:
        console.print("[yellow]⚠[/yellow] No languages detected")

    # Step 3: Analyze file structure
    console.print("\n[bold]Step 3: Analyzing file structure...[/bold]")
    file_structure = generate_file_structure(manifest)
    structure_file = analysis_dir / "file-structure.json"
    with open(structure_file, "w", encoding="utf-8") as f:
        json.dump(file_structure, f, indent=2)
    console.print(f"[green][ok][/green] Categorized files")

    # Step 4: Generate project metadata
    console.print("\n[bold]Step 4: Generating project metadata...[/bold]")
    metadata = {
        "schema_version": "1.0",
        "project_path": str(project),
        "project_name": project_name,
        "timestamp": datetime.now().isoformat(),
        "user_inputs": {
            "analysis_scope": scope,
            "additional_context": context,
            "concern_details": {
                "type": concern_type,
                "current": current_impl,
                "target": target_impl,
            } if concern_type else None,
        },
        "workspace": {
            "analysis_dir": str(analysis_dir),
            "manifest_path": str(manifest_file),
            "tech_stack_path": str(tech_stack_file),
            "file_structure_path": str(structure_file),
        },
    }
    metadata_file = analysis_dir / "project-metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    console.print(f"[green][ok][/green] Metadata saved")

    # Create analysis report template
    report_file = analysis_dir / "analysis-report.md"
    report_file.write_text("""# Project Analysis Report

**Status**: Pending AI Analysis

---

## Instructions for AI Agent

This workspace has been prepared for comprehensive project analysis. Please:

1. **Read the file-manifest.json** to understand project structure
2. **Detect technology stack** from indicator files
3. **Generate inclusion/exclusion rules** based on detected technology
4. **Categorize files by priority**
5. **Read files based on priority and size**
6. **Generate comprehensive analysis**

---

## Analysis Output

<!-- AI agent will replace this with comprehensive analysis -->

""", encoding="utf-8")

    console.print(Panel(
        f"[green][ok][/green] Analysis workspace created\n\n"
        f"[bold]Location:[/bold] {analysis_dir}\n"
        f"[bold]Files:[/bold] {manifest['statistics']['total_files']}\n"
        f"[bold]Languages:[/bold] {', '.join(tech_stack['languages']) or 'Unknown'}\n\n"
        "[dim]Ready for AI analysis[/dim]",
        title="[bold green]Setup Complete[/bold green]",
    ))

    return {
        "success": True,
        "project_path": str(project),
        "project_name": project_name,
        "analysis_dir": str(analysis_dir),
        "manifest_path": str(manifest_file),
        "tech_stack": tech_stack,
        "file_count": manifest["statistics"]["total_files"],
    }


def verify_analysis_report(report_file: str) -> bool:
    """
    Verify analysis report meets quality gates.

    Replaces verify-analysis-report.sh functionality.

    Args:
        report_file: Path to analysis report

    Returns:
        True if all checks pass
    """
    report_path = Path(report_file)

    if not report_path.exists():
        console.print(f"[red][x][/red] Report file not found: {report_file}")
        return False

    content = report_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    failed = False

    console.print(Panel("[bold]Analysis Report Verification Gate[/bold]"))
    console.print(f"Report: {report_file}\n")

    # Check 1: All 9 phases present
    console.print("[bold]Checking for all 9 phases...[/bold]")
    for i in range(1, 10):
        phase = f"Phase {i}"
        if phase in content:
            console.print(f"[green][ok][/green] {phase} found")
        else:
            console.print(f"[red][x][/red] MISSING: {phase}")
            failed = True

    # Check 2: Minimum line count
    console.print()
    line_count = len(lines)
    if line_count >= 3000:
        console.print(f"[green][ok][/green] Line count: {line_count} (minimum: 3000)")
    else:
        console.print(f"[red][x][/red] Report too short: {line_count} lines (minimum: 3000)")
        failed = True

    # Check 3: File:line references
    console.print()
    import re
    ref_count = len(re.findall(r":\d+", content))
    if ref_count >= 50:
        console.print(f"[green][ok][/green] File:line references: {ref_count} (minimum: 50)")
    else:
        console.print(f"[yellow]⚠[/yellow] Few file:line references: {ref_count} (recommended: 50+)")

    # Check 4: No placeholders
    console.print()
    placeholders = re.findall(r"TODO|TBD|will be analyzed|\[TBD\]", content, re.IGNORECASE)
    if placeholders:
        console.print(f"[red][x][/red] Report contains placeholders ({len(placeholders)} found)")
        failed = True
    else:
        console.print("[green][ok][/green] No placeholders found")

    # Check 5: Severity ratings
    console.print()
    severity_count = len(re.findall(r"\b(HIGH|MEDIUM|LOW)\b", content))
    if severity_count >= 20:
        console.print(f"[green][ok][/green] Severity ratings: {severity_count} (minimum: 20)")
    else:
        console.print(f"[yellow]⚠[/yellow] Few severity ratings: {severity_count} (recommended: 20+)")

    # Final verdict
    console.print()
    console.print("=" * 40)
    if not failed:
        console.print("[bold green]✅ VERIFICATION PASSED[/bold green]")
        console.print("Report meets all quality gates.")
        return True
    else:
        console.print("[bold red][x] VERIFICATION FAILED[/bold red]")
        console.print("\nPlease fix issues and re-run verification.")
        return False
