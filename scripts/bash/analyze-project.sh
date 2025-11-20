#!/usr/bin/env bash

#
# analyze-project.sh - AI-driven project analysis and modernization
#
# Usage:
#   ./analyze-project.sh [PROJECT_PATH] [--output DIR]
#
# This script enumerates a legacy project and prepares it for AI analysis.
# The AI agent will handle technology detection, file selection, and analysis.
#

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Auto-detect OS and redirect if needed
source "$SCRIPT_DIR/common.sh"

OS=$(detect_os)
if [[ "$OS" == "windows" ]]; then
    # Running bash on Windows - redirect to PowerShell
    exec pwsh -File "$SCRIPT_DIR/../powershell/analyze-project.ps1" "$@"
fi

# Continue with bash implementation for Unix/Linux/macOS

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
OUTPUT_DIR=""
PROJECT_PATH=""
ADDITIONAL_CONTEXT=""
ANALYSIS_SCOPE=""
CONCERN_TYPE=""
CURRENT_IMPL=""
TARGET_IMPL=""
REPO_ROOT="$(get_repo_root)"

# Functions

print_header() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

usage() {
    cat <<EOF
Usage: $0 [PROJECT_PATH] [OPTIONS]

AI-driven analysis of legacy projects for reverse engineering and modernization.

Arguments:
  PROJECT_PATH         Path to project root directory (default: current directory)

Options:
  --output DIR         Output directory (default: .analysis/PROJECT_NAME-TIMESTAMP)
  --context TEXT       Additional context for analysis (optional)
  --scope A|B          Analysis scope: A=Full App, B=Cross-Cutting (optional)
  --concern-type TEXT  Type of cross-cutting concern (required if scope=B)
  --current-impl TEXT  Current implementation (required if scope=B)
  --target-impl TEXT   Target implementation (required if scope=B)
  -h, --help           Show this help message

Examples:
  # Analyze current directory
  $0 .

  # Analyze specific project with context
  $0 /path/to/project --context "Migrate to microservices within 6 months"

  # Full application analysis
  $0 /path/to/project --scope A --context "Team prefers Spring Boot"

  # Cross-cutting concern migration
  $0 /path/to/project --scope B --concern-type "Authentication/Authorization" \\
     --current-impl "Custom JWT" --target-impl "Okta"

Workflow:
  1. Enumerate all files in the project (full recursive scan)
  2. Generate file manifest with metadata (JSON)
  3. Detect technology stack from indicator files (JSON)
  4. Analyze file structure and categorize files (JSON)
  5. Generate project metadata with all inputs (JSON)
  6. Create bootstrap state for AI chain workflow

Output:
  The script prepares an analysis workspace with:
  - file-manifest.json       Complete file inventory with metadata
  - tech-stack.json          Detected technologies and frameworks
  - file-structure.json      Directory tree and file categorization
  - project-metadata.json    Consolidated project information
  - 00-bootstrap.json        Chain state initialization

EOF
    exit 0
}

check_dependencies() {
    print_header "Checking Dependencies"

    local missing=0

    # Check jq (required for enumerate-project.sh)
    if ! command -v jq &> /dev/null; then
        print_error "jq is required but not installed"
        print_info "Why? It prevents JSON injection vulnerabilities"
        print_info "Install: sudo apt-get install jq  OR  brew install jq"
        print_info "Corporate? Download portable binary: https://github.com/jqlang/jq/releases"
        print_info "Alternative: Use PowerShell version (scripts/powershell/analyze-project.ps1)"
        missing=1
    else
        print_success "jq found: $(jq --version)"
    fi

    if [[ $missing -eq 1 ]]; then
        exit 1
    fi

    echo ""
}

validate_project_path() {
    print_header "Validating Project Path"

    if [ ! -d "$PROJECT_PATH" ]; then
        print_error "Project path does not exist: $PROJECT_PATH"
        exit 1
    fi

    PROJECT_PATH="$(cd "$PROJECT_PATH" && pwd)"
    print_success "Project path: $PROJECT_PATH"

    # Detect project name
    PROJECT_NAME=$(basename "$PROJECT_PATH")
    print_success "Project name: $PROJECT_NAME"

    echo ""
}

setup_output_directory() {
    print_header "Setting Up Analysis Workspace"

    if [ -z "$OUTPUT_DIR" ]; then
        TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
        # Always create .analysis folder at repo root for consistency
        OUTPUT_DIR="$REPO_ROOT/.analysis/$PROJECT_NAME-$TIMESTAMP"
    fi

    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR/checkpoints"
    print_success "Output directory: $OUTPUT_DIR"

    # Define output file paths (for AI agent reference)
    ANALYSIS_REPORT="$OUTPUT_DIR/analysis-report.md"
    RECOMMENDED_SPEC="$OUTPUT_DIR/recommended-spec.md"
    DEPENDENCY_AUDIT="$OUTPUT_DIR/dependency-audit.json"
    METRICS_SUMMARY="$OUTPUT_DIR/metrics-summary.json"
    DECISION_MATRIX="$OUTPUT_DIR/decision-matrix.md"

    echo ""
}

run_enumeration() {
    print_header "Enumerating Project Files"

    print_info "Running full recursive scan..."
    print_info "AI will determine which files to analyze based on detected technology"

    # Run enumeration script
    local MANIFEST_FILE="$OUTPUT_DIR/file-manifest.json"

    if ! "$SCRIPT_DIR/enumerate-project.sh" \
        --project "$PROJECT_PATH" \
        --output "$MANIFEST_FILE" \
        --max-size 10485760; then
        print_error "File enumeration failed"
        exit 1
    fi

    print_success "File manifest generated: $MANIFEST_FILE"

    # Display summary
    if [ -f "$MANIFEST_FILE" ]; then
        local total_files=$(jq -r '.statistics.total_files' "$MANIFEST_FILE" 2>/dev/null || echo "unknown")
        local total_size=$(jq -r '.statistics.total_size_bytes' "$MANIFEST_FILE" 2>/dev/null || echo "0")
        local total_size_mb=$((total_size / 1024 / 1024))

        print_info "Total files: $total_files"
        print_info "Total size: ${total_size_mb}MB"
    fi

    echo ""
}

detect_tech_stack() {
    print_header "Detecting Technology Stack"

    local TECH_STACK_FILE="$OUTPUT_DIR/tech-stack.json"
    local MANIFEST_FILE="$OUTPUT_DIR/file-manifest.json"

    print_info "Analyzing indicator files..."

    # Initialize tech stack JSON
    local tech_stack='{"schema_version":"1.0","languages":[],"frameworks":{"backend":[],"frontend":[]},"build_tools":[],"databases":[],"indicators_found":[]}'

    # Check for various tech stack indicators
    if [ -f "$MANIFEST_FILE" ]; then
        # Node.js / JavaScript
        if jq -e '.files[] | select(.path | endswith("package.json"))' "$MANIFEST_FILE" > /dev/null 2>&1; then
            tech_stack=$(echo "$tech_stack" | jq '.languages += ["javascript"] | .indicators_found += [{"file":"package.json","type":"nodejs","confidence":"high"}]')

            # Check if package.json exists in project to detect frameworks
            local package_json=$(jq -r '.files[] | select(.path | endswith("package.json")) | .path' "$MANIFEST_FILE" | head -1)
            if [ -n "$package_json" ] && [ -f "$PROJECT_PATH/$package_json" ]; then
                # Detect React
                if grep -q '"react"' "$PROJECT_PATH/$package_json" 2>/dev/null; then
                    local react_version=$(grep '"react"' "$PROJECT_PATH/$package_json" | sed 's/.*"react": *"\^*\([0-9.]*\).*/\1/')
                    tech_stack=$(echo "$tech_stack" | jq ".frameworks.frontend += [\"react-$react_version\"]")
                fi
                # Detect Express
                if grep -q '"express"' "$PROJECT_PATH/$package_json" 2>/dev/null; then
                    tech_stack=$(echo "$tech_stack" | jq '.frameworks.backend += ["express"]')
                fi
                # Detect Next.js
                if grep -q '"next"' "$PROJECT_PATH/$package_json" 2>/dev/null; then
                    tech_stack=$(echo "$tech_stack" | jq '.frameworks.frontend += ["nextjs"]')
                fi
            fi
        fi

        # Java / Maven
        if jq -e '.files[] | select(.path | endswith("pom.xml"))' "$MANIFEST_FILE" > /dev/null 2>&1; then
            tech_stack=$(echo "$tech_stack" | jq '.languages += ["java"] | .build_tools += ["maven"] | .indicators_found += [{"file":"pom.xml","type":"java-maven","confidence":"high"}]')

            # Check for Spring Boot
            local pom_xml=$(jq -r '.files[] | select(.path | endswith("pom.xml")) | .path' "$MANIFEST_FILE" | head -1)
            if [ -n "$pom_xml" ] && [ -f "$PROJECT_PATH/$pom_xml" ]; then
                if grep -q "spring-boot" "$PROJECT_PATH/$pom_xml" 2>/dev/null; then
                    local spring_version=$(grep -oP 'spring-boot.*?<version>\K[^<]+' "$PROJECT_PATH/$pom_xml" | head -1)
                    tech_stack=$(echo "$tech_stack" | jq ".frameworks.backend += [\"spring-boot-${spring_version:-unknown}\"]")
                fi
            fi
        fi

        # Java / Gradle
        if jq -e '.files[] | select(.path | endswith("build.gradle") or endswith("build.gradle.kts"))' "$MANIFEST_FILE" > /dev/null 2>&1; then
            tech_stack=$(echo "$tech_stack" | jq '.languages += ["java"] | .build_tools += ["gradle"] | .indicators_found += [{"file":"build.gradle","type":"java-gradle","confidence":"high"}]')
        fi

        # Python
        if jq -e '.files[] | select(.path | endswith("requirements.txt") or endswith("setup.py") or endswith("pyproject.toml"))' "$MANIFEST_FILE" > /dev/null 2>&1; then
            tech_stack=$(echo "$tech_stack" | jq '.languages += ["python"] | .indicators_found += [{"file":"requirements.txt","type":"python","confidence":"high"}]')

            # Check for Django/Flask
            local req_file=$(jq -r '.files[] | select(.path | endswith("requirements.txt")) | .path' "$MANIFEST_FILE" | head -1)
            if [ -n "$req_file" ] && [ -f "$PROJECT_PATH/$req_file" ]; then
                if grep -qi "django" "$PROJECT_PATH/$req_file" 2>/dev/null; then
                    tech_stack=$(echo "$tech_stack" | jq '.frameworks.backend += ["django"]')
                fi
                if grep -qi "flask" "$PROJECT_PATH/$req_file" 2>/dev/null; then
                    tech_stack=$(echo "$tech_stack" | jq '.frameworks.backend += ["flask"]')
                fi
            fi
        fi

        # .NET
        if jq -e '.files[] | select(.path | endswith(".csproj") or endswith(".sln"))' "$MANIFEST_FILE" > /dev/null 2>&1; then
            tech_stack=$(echo "$tech_stack" | jq '.languages += ["csharp"] | .build_tools += ["dotnet"] | .indicators_found += [{"file":"*.csproj","type":"dotnet","confidence":"high"}]')
        fi

        # Ruby
        if jq -e '.files[] | select(.path | endswith("Gemfile"))' "$MANIFEST_FILE" > /dev/null 2>&1; then
            tech_stack=$(echo "$tech_stack" | jq '.languages += ["ruby"] | .indicators_found += [{"file":"Gemfile","type":"ruby","confidence":"high"}]')
        fi

        # Go
        if jq -e '.files[] | select(.path | endswith("go.mod"))' "$MANIFEST_FILE" > /dev/null 2>&1; then
            tech_stack=$(echo "$tech_stack" | jq '.languages += ["go"] | .indicators_found += [{"file":"go.mod","type":"golang","confidence":"high"}]')
        fi
    fi

    # Remove duplicates from arrays
    tech_stack=$(echo "$tech_stack" | jq '.languages |= unique | .frameworks.backend |= unique | .frameworks.frontend |= unique | .build_tools |= unique')

    # Write to file
    echo "$tech_stack" | jq '.' > "$TECH_STACK_FILE"
    print_success "Tech stack detected: $TECH_STACK_FILE"

    # Display detected technologies
    if [ -f "$TECH_STACK_FILE" ]; then
        local languages=$(jq -r '.languages | join(", ")' "$TECH_STACK_FILE")
        local backend=$(jq -r '.frameworks.backend | join(", ")' "$TECH_STACK_FILE")
        local frontend=$(jq -r '.frameworks.frontend | join(", ")' "$TECH_STACK_FILE")

        [ -n "$languages" ] && [ "$languages" != "" ] && print_info "Languages: $languages"
        [ -n "$backend" ] && [ "$backend" != "" ] && print_info "Backend: $backend"
        [ -n "$frontend" ] && [ "$frontend" != "" ] && print_info "Frontend: $frontend"
    fi

    echo ""
}

generate_file_structure() {
    print_header "Analyzing File Structure"

    local STRUCTURE_FILE="$OUTPUT_DIR/file-structure.json"
    local MANIFEST_FILE="$OUTPUT_DIR/file-manifest.json"

    print_info "Categorizing files..."

    if [ ! -f "$MANIFEST_FILE" ]; then
        print_error "Manifest file not found: $MANIFEST_FILE"
        return 1
    fi

    # Count files by category using jq
    local controllers=$(jq '[.files[] | select(.path | test("(controller|route|endpoint)"; "i"))] | length' "$MANIFEST_FILE")
    local services=$(jq '[.files[] | select(.path | test("(service|manager|handler|usecase)"; "i"))] | length' "$MANIFEST_FILE")
    local models=$(jq '[.files[] | select(.path | test("(model|entity|schema|domain)"; "i"))] | length' "$MANIFEST_FILE")
    local repositories=$(jq '[.files[] | select(.path | test("(repository|repo|dao|data)"; "i"))] | length' "$MANIFEST_FILE")
    local configs=$(jq '[.files[] | select(.path | test("(config|settings|properties|yml|yaml|env)"; "i"))] | length' "$MANIFEST_FILE")
    local security=$(jq '[.files[] | select(.path | test("(auth|security|jwt|oauth|permission)"; "i"))] | length' "$MANIFEST_FILE")
    local middleware=$(jq '[.files[] | select(.path | test("middleware"; "i"))] | length' "$MANIFEST_FILE")
    local utils=$(jq '[.files[] | select(.path | test("(util|helper|common|shared)"; "i"))] | length' "$MANIFEST_FILE")
    local tests=$(jq '[.files[] | select(.path | test("(test|spec|__tests__)"; "i"))] | length' "$MANIFEST_FILE")
    local docs=$(jq '[.files[] | select(.path | test("(README|CHANGELOG|LICENSE|\.md$)"; "i"))] | length' "$MANIFEST_FILE")

    local total_files=$(jq '.statistics.total_files' "$MANIFEST_FILE")

    # Find entry points (common patterns)
    local entry_points=$(jq -r '[.files[] | select(.path | test("(main\\.|index\\.|app\\.|application\\.|server\\.|start)"; "i")) | .path] | unique | .[]' "$MANIFEST_FILE" | head -10)

    # Convert entry points to JSON array
    local entry_points_json="[]"
    if [ -n "$entry_points" ]; then
        entry_points_json=$(echo "$entry_points" | jq -R . | jq -s .)
    fi

    # Create file structure JSON
    cat > "$STRUCTURE_FILE" <<EOF
{
  "schema_version": "1.0",
  "total_files": $total_files,
  "categories": {
    "controllers": $controllers,
    "services": $services,
    "models": $models,
    "repositories": $repositories,
    "configs": $configs,
    "security": $security,
    "middleware": $middleware,
    "utils": $utils,
    "tests": $tests,
    "docs": $docs
  },
  "entry_points": $entry_points_json,
  "analysis_priority": {
    "critical": ["configs", "security", "entry_points"],
    "high": ["controllers", "services", "models", "repositories"],
    "medium": ["middleware", "utils"],
    "low": ["tests", "docs"]
  }
}
EOF

    print_success "File structure generated: $STRUCTURE_FILE"
    print_info "Core application files: $((controllers + services + models + repositories))"
    print_info "Configuration files: $configs"
    print_info "Test files: $tests"

    echo ""
}

generate_project_metadata() {
    print_header "Generating Project Metadata"

    local METADATA_FILE="$OUTPUT_DIR/project-metadata.json"
    local timestamp=$(date -Iseconds)

    # Escape JSON strings
    local context_json="null"
    if [ -n "$ADDITIONAL_CONTEXT" ]; then
        context_json=$(echo "$ADDITIONAL_CONTEXT" | jq -R -s .)
    fi

    local scope_json="null"
    if [ -n "$ANALYSIS_SCOPE" ]; then
        scope_json="\"$ANALYSIS_SCOPE\""
    fi

    # Build concern details if provided
    local concern_json="null"
    if [ -n "$CONCERN_TYPE" ]; then
        concern_json=$(cat <<EOF
{
  "type": "$CONCERN_TYPE",
  "current": "$CURRENT_IMPL",
  "target": "$TARGET_IMPL"
}
EOF
)
    fi

    # Create metadata JSON
    cat > "$METADATA_FILE" <<EOF
{
  "schema_version": "1.0",
  "project_path": "$PROJECT_PATH",
  "project_name": "$PROJECT_NAME",
  "timestamp": "$timestamp",
  "user_inputs": {
    "analysis_scope": $scope_json,
    "additional_context": $context_json,
    "concern_details": $concern_json
  },
  "workspace": {
    "analysis_dir": "$OUTPUT_DIR",
    "manifest_path": "$OUTPUT_DIR/file-manifest.json",
    "tech_stack_path": "$OUTPUT_DIR/tech-stack.json",
    "file_structure_path": "$OUTPUT_DIR/file-structure.json"
  }
}
EOF

    print_success "Project metadata generated: $METADATA_FILE"
    print_info "Project: $PROJECT_NAME"
    [ -n "$ANALYSIS_SCOPE" ] && print_info "Scope: $ANALYSIS_SCOPE"
    [ -n "$ADDITIONAL_CONTEXT" ] && print_info "Context provided: Yes"

    echo ""
}

create_analysis_workspace() {
    print_header "Preparing Analysis Workspace"

    # Create placeholder for AI-generated analysis
    cat > "$ANALYSIS_REPORT" <<'EOF'
# Project Analysis Report

**Status**: Pending AI Analysis

**Project**: <!-- AI will fill this -->
**Analysis Date**: <!-- AI will fill this -->

---

## Instructions for AI Agent

This workspace has been prepared for comprehensive project analysis. Please:

1. **Read the file-manifest.json** to understand project structure
2. **Detect technology stack** from indicator files (package.json, *.csproj, etc.)
3. **Generate inclusion/exclusion rules** based on detected technology
   - Example: .NET projects exclude bin/, obj/, packages/
   - Example: Node.js projects exclude node_modules/, dist/, build/
4. **Categorize files by priority**:
   - Critical: package files, entry points, configs
   - Important: main source code
   - Supporting: tests, docs, scripts
5. **Read files based on priority and size**:
   - Full read: <100KB or critical files
   - Sampled: 100KB-1MB (first + last portions)
   - Metadata only: >1MB or binary files
6. **Generate comprehensive analysis** including:
   - Technology stack and versions
   - Project structure and architecture
   - Dependencies and their health
   - Code quality indicators
   - Modernization recommendations
   - Feasibility assessment (inline upgrade vs greenfield rewrite)

---

## Analysis Output

<!-- AI agent will replace this entire file with comprehensive analysis -->

EOF

    print_success "Created analysis workspace"
    print_info "Analysis report template: $ANALYSIS_REPORT"
    print_info "Additional artifacts will be generated by AI:"
    print_info "  - $RECOMMENDED_SPEC"
    print_info "  - $DEPENDENCY_AUDIT"
    print_info "  - $METRICS_SUMMARY"
    print_info "  - $DECISION_MATRIX"

    echo ""
}

show_summary() {
    print_header "Analysis Workspace Ready"

    print_success "Workspace created successfully!"
    echo ""
    print_info "Workspace location: $OUTPUT_DIR"
    print_info "File manifest: $OUTPUT_DIR/file-manifest.json"
    echo ""
    print_info "Next steps:"
    print_info "1. AI agent will analyze the file manifest"
    print_info "2. AI will detect technology and generate filter rules"
    print_info "3. AI will read relevant files and generate comprehensive analysis"
    print_info "4. Results will be saved to analysis-report.md"
    echo ""
    print_success "🤖 Ready for AI analysis!"
}

initialize_chain_state() {
    print_header "Initializing Chain State"

    # Initialize state directory
    "$SCRIPT_DIR/chain-state.sh" init

    # Generate chain ID
    CHAIN_ID=$("$SCRIPT_DIR/chain-state.sh" generate-id)
    print_success "Chain ID: $CHAIN_ID"

    # Create bootstrap state with project info
    local timestamp=$(date -Iseconds)
    local bootstrap_state=$(cat <<EOF
{
  "chain_id": "$CHAIN_ID",
  "start_time": "$timestamp",
  "timestamp": "$timestamp",
  "stage": "bootstrap",
  "stages_complete": [],
  "project_path": "$PROJECT_PATH",
  "project_name": "$PROJECT_NAME",
  "analysis_dir": "$OUTPUT_DIR",
  "manifest_path": "$OUTPUT_DIR/file-manifest.json"
}
EOF
)

    # Save bootstrap state
    "$SCRIPT_DIR/chain-state.sh" save 00-bootstrap "$bootstrap_state"

    # Export chain ID for AI to use
    echo ""
    print_success "Chain state initialized"
    print_info "Chain ID: $CHAIN_ID"
    print_info "State directory: .analysis/.state/"
    echo ""
}

# Main script

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                ;;
            --output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            --context)
                ADDITIONAL_CONTEXT="$2"
                shift 2
                ;;
            --scope)
                ANALYSIS_SCOPE="$2"
                if [[ "$ANALYSIS_SCOPE" != "A" && "$ANALYSIS_SCOPE" != "B" ]]; then
                    print_error "Invalid scope: $ANALYSIS_SCOPE (must be A or B)"
                    exit 1
                fi
                shift 2
                ;;
            --concern-type)
                CONCERN_TYPE="$2"
                shift 2
                ;;
            --current-impl)
                CURRENT_IMPL="$2"
                shift 2
                ;;
            --target-impl)
                TARGET_IMPL="$2"
                shift 2
                ;;
            *)
                if [ -z "$PROJECT_PATH" ]; then
                    PROJECT_PATH="$1"
                else
                    print_error "Unknown option: $1"
                    usage
                fi
                shift
                ;;
        esac
    done

    # Default project path to current directory
    if [ -z "$PROJECT_PATH" ]; then
        PROJECT_PATH="."
    fi

    # Validate scope B requirements
    if [ "$ANALYSIS_SCOPE" = "B" ]; then
        if [ -z "$CONCERN_TYPE" ] || [ -z "$CURRENT_IMPL" ] || [ -z "$TARGET_IMPL" ]; then
            print_error "Scope B requires --concern-type, --current-impl, and --target-impl"
            exit 1
        fi
    fi

    # Welcome message
    print_header "AI-Driven Project Analysis"
    echo ""

    # Run workflow
    check_dependencies
    validate_project_path
    setup_output_directory
    run_enumeration
    detect_tech_stack
    generate_file_structure
    generate_project_metadata
    create_analysis_workspace
    initialize_chain_state
    show_summary

    exit 0
}

main "$@"
