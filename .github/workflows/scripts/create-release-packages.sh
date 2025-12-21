#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh (workflow-local)
# Build Spec Kit template release archives for each supported AI assistant.
# Generates packages with Python CLI launchers (no bash/PowerShell scripts).
# Usage: .github/workflows/scripts/create-release-packages.sh <version>
#   Version argument should include leading 'v'.
#   Optionally set AGENTS env var to limit which agents get built.
#     AGENTS  : space or comma separated subset of: claude gemini copilot cursor-agent qwen opencode windsurf codex kilocode auggie roo codebuddy amp q (default: all)
#   Examples:
#     AGENTS=claude $0 v0.2.0
#     AGENTS="copilot,gemini" $0 v0.2.0
#     $0 v0.2.0  # Build all agents

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi
NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release packages for $NEW_VERSION"

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

rewrite_paths() {
  sed -E \
    -e 's@(/?)memory/@.specify/memory/@g' \
    -e 's@(/?)templates/@.specify/templates/@g'
}

build_unified() {
  local agent=$1
  local base_dir="$GENRELEASES_DIR/sdd-${agent}-package-unified"
  echo "Building $agent package..."
  mkdir -p "$base_dir"

  # Copy base structure
  SPEC_DIR="$base_dir/.specify"
  mkdir -p "$SPEC_DIR"

  # Copy .specify/config.json if it exists
  [[ -f .specify/config.json ]] && { cp .specify/config.json "$SPEC_DIR/"; echo "Copied .specify/config.json"; }

  [[ -d memory ]] && { cp -r memory "$SPEC_DIR/"; echo "Copied memory -> .specify"; }
  [[ -d .guidelines ]] && { cp -r .guidelines "$base_dir/"; echo "Copied .guidelines -> package root"; }

  # Copy templates (excluding commands folder - commands are agent-specific launchers)
  [[ -d templates ]] && {
    mkdir -p "$SPEC_DIR/templates"
    find templates -type f -not -path "templates/commands/*" -not -name "vscode-settings.json" -not -name "*-monolithic.md" -exec cp --parents {} "$SPEC_DIR"/ \;
    echo "Copied templates -> .specify/templates"
  }

  # Copy chained prompts to .specify/prompts/ (workflow orchestration)
  [[ -d templates/commands/analyze ]] && {
    mkdir -p "$SPEC_DIR/prompts/analyze"
    cp -r templates/commands/analyze/* "$SPEC_DIR/prompts/analyze/"
    echo "Copied analyze prompts -> .specify/prompts/analyze"
  }

  # Copy AGENTS.md to package root for easy agent access
  [[ -f templates/AGENTS.md ]] && { cp templates/AGENTS.md "$base_dir/AGENTS.md"; echo "Copied AGENTS.md -> package root"; }

  # Copy launcher files from launchers/ directory based on agent
  local launcher_dir=""
  local dest_dir=""

  case $agent in
    claude)
      launcher_dir="launchers/claude"
      dest_dir="$base_dir/.claude/commands"
      ;;
    gemini)
      launcher_dir="launchers/gemini"
      dest_dir="$base_dir/.gemini/commands"
      [[ -f agent_templates/gemini/GEMINI.md ]] && cp agent_templates/gemini/GEMINI.md "$base_dir/GEMINI.md"
      ;;
    copilot)
      launcher_dir="launchers/copilot"
      dest_dir="$base_dir/.github/prompts"
      # Create VS Code workspace settings
      mkdir -p "$base_dir/.vscode"
      [[ -f templates/vscode-settings.json ]] && cp templates/vscode-settings.json "$base_dir/.vscode/settings.json"
      ;;
    cursor-agent)
      launcher_dir="launchers/cursor"
      dest_dir="$base_dir/.cursor/commands"
      ;;
    qwen)
      launcher_dir="launchers/qwen"
      dest_dir="$base_dir/.qwen/commands"
      [[ -f agent_templates/qwen/QWEN.md ]] && cp agent_templates/qwen/QWEN.md "$base_dir/QWEN.md"
      ;;
    opencode)
      launcher_dir="launchers/opencode"
      dest_dir="$base_dir/.opencode/command"
      ;;
    windsurf)
      launcher_dir="launchers/windsurf"
      dest_dir="$base_dir/.windsurf/workflows"
      ;;
    codex)
      launcher_dir="launchers/codex"
      dest_dir="$base_dir/.codex/commands"
      ;;
    kilocode)
      launcher_dir="launchers/kilocode"
      dest_dir="$base_dir/.kilocode/rules"
      ;;
    auggie)
      launcher_dir="launchers/auggie"
      dest_dir="$base_dir/.augment/rules"
      ;;
    roo)
      launcher_dir="launchers/roo"
      dest_dir="$base_dir/.roo/rules"
      ;;
    codebuddy)
      launcher_dir="launchers/codebuddy"
      dest_dir="$base_dir/.codebuddy/commands"
      ;;
    amp)
      launcher_dir="launchers/amp"
      dest_dir="$base_dir/.agents/commands"
      ;;
    q)
      launcher_dir="launchers/amazonq"
      dest_dir="$base_dir/.amazonq/prompts"
      ;;
  esac

  # Copy launcher files with speckitsmart prefix
  if [[ -d "$launcher_dir" ]]; then
    mkdir -p "$dest_dir"
    for file in "$launcher_dir"/*; do
      [[ -f "$file" ]] || continue
      local basename=$(basename "$file")
      local name="${basename%.*}"
      local ext="${basename##*.}"
      cp "$file" "$dest_dir/speckitsmart.$name.$ext"
    done
    echo "Copied launchers from $launcher_dir -> $dest_dir"
  else
    echo "Warning: No launcher directory found at $launcher_dir"
  fi

  ( cd "$base_dir" && zip -r "../spec-kit-template-${agent}-${NEW_VERSION}.zip" . )
  echo "Created $GENRELEASES_DIR/spec-kit-template-${agent}-${NEW_VERSION}.zip"
}

# Determine agent list
ALL_AGENTS=(claude gemini copilot cursor-agent qwen opencode windsurf codex kilocode auggie roo codebuddy amp q)

norm_list() {
  # convert comma+space separated -> newline separated unique while preserving order of first occurrence
  tr ',\n' '  ' | awk '{
    for(i=1;i<=NF;i++){
      if(!seen[$i]++){
        print $i
      }
    }
  }'
}

validate_subset() {
  local type=$1; shift; local -n allowed=$1; shift; local items=("$@")
  local ok=0
  for it in "${items[@]}"; do
    local found=0
    for a in "${allowed[@]}"; do [[ $it == "$a" ]] && { found=1; break; }; done
    if [[ $found -eq 0 ]]; then
      echo "Error: unknown $type '$it' (allowed: ${allowed[*]})" >&2
      ok=1
    fi
  done
  return $ok
}

if [[ -n ${AGENTS:-} ]]; then
  mapfile -t AGENT_LIST < <(printf '%s' "$AGENTS" | norm_list)
  validate_subset agent ALL_AGENTS "${AGENT_LIST[@]}" || exit 1
else
  AGENT_LIST=("${ALL_AGENTS[@]}")
fi

echo "Agents: ${AGENT_LIST[*]}"
echo "Building packages with Python CLI launchers (speckitadv)"

for agent in "${AGENT_LIST[@]}"; do
  build_unified "$agent"
done

echo "Archives in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/spec-kit-template-*-"${NEW_VERSION}".zip
