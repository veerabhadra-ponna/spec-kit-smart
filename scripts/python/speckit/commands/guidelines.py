"""
Guidelines generation and artifactory checking for speckitadv.

Ports functionality from:
- generate-guidelines.sh
- check-artifactory.sh
"""

import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel

console = Console()


def find_repo_root(start_path: Optional[Path] = None) -> Path:
    """Find repository root by searching for .git or memory directory."""
    current = (start_path or Path.cwd()).resolve()
    while current != current.parent:
        if (current / ".git").exists() or (current / "memory").exists():
            return current
        current = current.parent
    return Path.cwd()


def enumerate_documents(docs_dir: Path) -> list:
    """Enumerate document files in directory."""
    documents = []
    doc_extensions = {".pdf", ".md", ".docx", ".txt", ".doc"}

    if not docs_dir.exists():
        return documents

    for root, _, files in os.walk(docs_dir):
        for filename in files:
            filepath = Path(root) / filename
            if filepath.suffix.lower() in doc_extensions:
                try:
                    size = filepath.stat().st_size
                except (OSError, IOError):
                    size = 0

                documents.append({
                    "path": str(filepath),
                    "relative_path": str(filepath.relative_to(docs_dir)),
                    "filename": filename,
                    "size_bytes": size,
                })

    return documents


def enumerate_project_files(project_path: Path, project_name: str, output_dir: Path) -> int:
    """Enumerate files in a reference project."""
    files = []
    skip_dirs = {"node_modules", "bin", "obj", "target", "build", "dist", ".git", "__pycache__", "venv", ".venv"}
    max_size = 10 * 1024 * 1024  # 10MB

    for root, dirs, filenames in os.walk(project_path):
        # Skip common build/dependency directories
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]

        for filename in filenames:
            filepath = Path(root) / filename
            try:
                size = filepath.stat().st_size
            except (OSError, IOError):
                size = 0

            if size > max_size:
                continue

            files.append({
                "path": str(filepath),
                "relative_path": str(filepath.relative_to(project_path)),
                "filename": filename,
                "size_bytes": size,
                "extension": filepath.suffix,
            })

    manifest = {
        "project_name": project_name,
        "project_path": str(project_path),
        "files": files,
        "file_count": len(files),
    }

    output_file = output_dir / f"{project_name}-files.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return len(files)


def run_generate_guidelines(sources_path: str) -> bool:
    """
    Generate guidelines from corporate documents and reference projects.

    Replaces generate-guidelines.sh functionality.

    Args:
        sources_path: Path to folder containing docs/ and reference-projects/

    Returns:
        True if successful
    """
    sources = Path(sources_path).resolve()
    repo_root = find_repo_root()

    if not sources.is_dir():
        console.print(f"[red]Error:[/red] Sources path does not exist: {sources}")
        return False

    # Output directory (fixed location)
    output_dir = repo_root / ".guidelines-analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(Panel("[bold]Corporate Guideline Generation[/bold]"))

    # Check structure
    docs_dir = sources / "docs" if (sources / "docs").exists() else sources
    projects_dir = sources / "reference-projects" if (sources / "reference-projects").exists() else sources

    # Enumerate documents
    console.print("\n[bold]Enumerating Corporate Documents...[/bold]")
    documents = enumerate_documents(docs_dir)

    docs_manifest = {
        "documents": documents,
        "count": len(documents),
        "base_path": str(docs_dir),
    }

    docs_manifest_file = output_dir / "documents-manifest.json"
    with open(docs_manifest_file, "w", encoding="utf-8") as f:
        json.dump(docs_manifest, f, indent=2)

    if documents:
        console.print(f"[green]✓[/green] Found {len(documents)} documents")
    else:
        console.print("[yellow]⚠[/yellow] No documents found")

    # Enumerate reference projects
    console.print("\n[bold]Enumerating Reference Projects...[/bold]")
    projects = []

    if projects_dir.is_dir():
        for item in projects_dir.iterdir():
            if item.is_dir() and not item.name.startswith(".") and item.name != "docs":
                project_name = item.name

                console.print(f"[dim]  Enumerating {project_name}...[/dim]")
                file_count = enumerate_project_files(item, project_name, output_dir)

                projects.append({
                    "path": str(item),
                    "relative_path": project_name,
                    "name": project_name,
                    "file_count": file_count,
                })
                console.print(f"[green]✓[/green] {project_name}: {file_count} files")

    projects_manifest = {
        "projects": projects,
        "count": len(projects),
        "base_path": str(projects_dir),
    }

    projects_manifest_file = output_dir / "projects-manifest.json"
    with open(projects_manifest_file, "w", encoding="utf-8") as f:
        json.dump(projects_manifest, f, indent=2)

    if not documents and not projects:
        console.print("[red]Error:[/red] No documents or projects found!")
        return False

    console.print(Panel(
        f"[green]✓[/green] Workspace created\n\n"
        f"[bold]Location:[/bold] {output_dir}\n"
        f"[bold]Documents:[/bold] {len(documents)}\n"
        f"[bold]Projects:[/bold] {len(projects)}\n\n"
        "[dim]Ready for AI analysis[/dim]",
        title="[bold green]Guidelines Analysis Ready[/bold green]",
    ))

    return True


def check_artifactory(
    artifactory_url: str,
    library_name: str,
    api_key: Optional[str] = None,
    repos: Optional[str] = None,
    debug: bool = False,
) -> tuple[int, str]:
    """
    Query Artifactory for library availability.

    Replaces check-artifactory.sh functionality.

    Args:
        artifactory_url: URL of Artifactory instance
        library_name: Name of library to check
        api_key: Optional API key for authentication
        repos: Optional comma-separated list of repositories
        debug: Enable debug output

    Returns:
        Tuple of (exit_code, message)
        Exit codes:
          0: Library found
          1: Library not found
          2: Authentication error
          3: API error
          4: Artifactory URL not configured
    """
    if not library_name:
        return 3, "Library name is required"

    # Check if URL is configured
    if not artifactory_url or artifactory_url in ("Not configured", "null", ""):
        return 4, f"Artifactory URL not configured - skipping validation for {library_name}"

    # Normalize URL
    artifactory_url = artifactory_url.rstrip("/")
    if artifactory_url.endswith("/api"):
        artifactory_url = artifactory_url[:-4]

    # Build API endpoint
    api_endpoint = f"{artifactory_url}/api/search/artifact?name={library_name}"
    if repos:
        api_endpoint += f"&repos={repos}"

    if debug:
        console.print(f"[dim]DEBUG: API Endpoint: {api_endpoint}[/dim]")

    # Prepare request
    headers = {"X-Result-Detail": "info"}

    if api_key:
        # Try Bearer token first
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        req = urllib.request.Request(api_endpoint, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode("utf-8")

            try:
                data = json.loads(body)
                results = data.get("results", [])

                if results:
                    download_uri = results[0].get("downloadUri", "")
                    return 0, f"FOUND: {library_name} available in Artifactory\n{download_uri}"
                else:
                    return 1, f"NOT FOUND: {library_name} not found in Artifactory"
            except json.JSONDecodeError:
                if "downloadUri" in body:
                    return 0, f"FOUND: {library_name} available in Artifactory"
                return 1, f"NOT FOUND: {library_name} not found in Artifactory"

    except urllib.error.HTTPError as e:
        if e.code == 401:
            # Try with X-JFrog-Art-Api header
            if api_key:
                headers.pop("Authorization", None)
                headers["X-JFrog-Art-Api"] = api_key
                try:
                    req = urllib.request.Request(api_endpoint, headers=headers)
                    with urllib.request.urlopen(req, timeout=5) as response:
                        body = response.read().decode("utf-8")
                        data = json.loads(body)
                        if data.get("results"):
                            return 0, f"FOUND: {library_name} available"
                        return 1, f"NOT FOUND: {library_name}"
                except Exception:
                    pass
            return 2, "Authentication failed (401 Unauthorized)"
        elif e.code == 403:
            return 2, "Access forbidden (403 Forbidden)"
        elif e.code == 404:
            return 3, "API endpoint not found (404)"
        else:
            return 3, f"Artifactory API returned HTTP {e.code}"

    except urllib.error.URLError:
        return 3, "Network error or timeout (Artifactory may be unreachable)"

    except Exception as e:
        return 3, f"Error: {str(e)}"


def run_check_artifactory_cli(
    url: str,
    library: str,
    api_key: Optional[str] = None,
    repos: Optional[str] = None,
    debug: bool = False,
) -> None:
    """CLI wrapper for check_artifactory."""
    # Get API key from environment if not provided
    if not api_key:
        api_key = os.environ.get("ARTIFACTORY_API_KEY")

    exit_code, message = check_artifactory(url, library, api_key, repos, debug)

    if exit_code == 0:
        console.print(f"[green]✅ {message}[/green]")
    elif exit_code == 1:
        console.print(f"[yellow]❌ {message}[/yellow]")
    elif exit_code == 2:
        console.print(f"[red]⚠️ {message}[/red]")
    elif exit_code == 4:
        console.print(f"[yellow]⊘ SKIPPED: {message}[/yellow]")
    else:
        console.print(f"[red]⚠️ ERROR: {message}[/red]")
