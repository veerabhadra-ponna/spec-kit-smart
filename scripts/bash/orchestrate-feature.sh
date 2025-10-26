#!/usr/bin/env bash

set -euo pipefail

show_help() {
  cat <<'USAGE'
Usage: ./orchestrate-feature.sh [--json]

Ensures status directories exist and returns feature paths for /speckit.feature.
USAGE
}

JSON_OUTPUT=false
HELP=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json)
      JSON_OUTPUT=true
      shift
      ;;
    -h|--help)
      HELP=true
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ "$HELP" == true ]]; then
  show_help
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

eval $(get_feature_paths)

declare -a NOTES=()
if [[ "$HAS_GIT" == true ]]; then
  if [[ ! "$CURRENT_BRANCH" =~ ^[0-9]{3}- ]]; then
    NOTES+=("Not on a numbered feature branch.")
  fi
fi

STATUS_DIR="$FEATURE_DIR/status"
mkdir -p "$STATUS_DIR"

payload=$(jq -n \
  --arg ok "$( [[ "${NOTES[*]}" == "" ]] && echo true || echo false )" \
  --arg version "1.0.0" \
  --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --arg branch "$CURRENT_BRANCH" \
  --arg feature_dir "$FEATURE_DIR" \
  --arg spec "$FEATURE_SPEC" \
  --arg plan "$IMPL_PLAN" \
  --arg tasks "$TASKS" \
  --arg status_dir "$STATUS_DIR" \
  --arg status_spec "$STATUS_DIR/specify.md" \
  --arg status_plan "$STATUS_DIR/plan.md" \
  --arg status_tasks "$STATUS_DIR/tasks.md" \
  --arg status_feature "$STATUS_DIR/feature.md" \
  --argjson notes "$(printf '%s\n' "${NOTES[@]}" | jq -R . | jq -s .)" \
  '{ok: ($ok|test("true")), version: $version, timestamp: $timestamp, branch: $branch, paths: {feature_dir: $feature_dir, spec: $spec, plan: $plan, tasks: $tasks, status_dir: $status_dir, status_spec: $status_spec, status_plan: $status_plan, status_tasks: $status_tasks, status_feature: $status_feature}, notes: $notes}')

if [[ "$JSON_OUTPUT" == true ]]; then
  echo "$payload" | jq -c .
  if jq -e '.ok' <<<"$payload" >/dev/null; then
    exit 0
  else
    exit 1
  fi
fi

echo "FEATURE_DIR: $FEATURE_DIR"
echo "STATUS_DIR: $STATUS_DIR"
if [[ ${#NOTES[@]} -gt 0 ]]; then
  printf 'NOTE: %s\n' "${NOTES[@]}"
fi
