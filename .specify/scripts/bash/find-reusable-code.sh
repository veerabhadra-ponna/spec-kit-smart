#!/usr/bin/env bash
#
# find-reusable-code.sh - Find reusable code from the codebase index
#
# Analyzes task description and searches for:
# - Similar existing implementations
# - Reusable utility functions
# - Architecture patterns to follow
# - Test examples as templates
#
# Usage: bash find-reusable-code.sh "<task_description>" [--format json|text] [--threshold <0-100>]
#
# Exit codes:
#   0 - Success
#   1 - Index not found
#   2 - No matches found
#

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX_DIR="${REPO_ROOT}/.analysis/index"
FORMAT="text"
THRESHOLD=60
TASK=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --threshold)
            THRESHOLD="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 \"<task_description>\" [--format json|text] [--threshold <0-100>]"
            exit 0
            ;;
        *)
            if [[ -z "$TASK" ]]; then
                TASK="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$TASK" ]]; then
    echo "Error: Task description required" >&2
    exit 2
fi

# Check prerequisites
if [[ ! -d "$INDEX_DIR" ]]; then
    echo '{"error": "Index not found. Run /speckitsmart.index first."}' >&2
    exit 1
fi

# Extract keywords from task
extract_keywords() {
    local text="$1"
    # Remove common words and extract meaningful terms
    echo "$text" | tr '[:upper:]' '[:lower:]' | \
        tr -cs '[:alnum:]' '\n' | \
        grep -vE '^(the|a|an|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|could|should|may|might|must|shall|can|need|want|to|of|in|for|on|with|at|by|from|as|into|through|during|before|after|above|below|between|under|again|further|then|once|here|there|when|where|why|how|all|each|every|both|few|more|most|other|some|such|no|not|only|own|same|so|than|too|very|just|also|now|new|old|first|last|long|great|little|own|make|made|get|got|give|gave|take|took|come|came|go|went|know|knew|see|saw|think|thought|look|looked|want|wanted|use|used|find|found|tell|told|ask|asked|work|worked|seem|seemed|feel|felt|try|tried|leave|left|call|called|keep|kept|let|put|begin|began|help|helped|show|showed|hear|heard|play|played|run|ran|move|moved|live|lived|believe|believed|hold|held|bring|brought|happen|happened|write|wrote|provide|provided|sit|sat|stand|stood|lose|lost|pay|paid|meet|met|include|included|continue|continued|set|learn|learned|change|changed|lead|led|understand|understood|watch|watched|follow|followed|stop|stopped|create|created|speak|spoke|read|allow|allowed|add|added|spend|spent|grow|grew|open|opened|walk|walked|win|won|offer|offered|remember|remembered|love|loved|consider|considered|appear|appeared|buy|bought|wait|waited|serve|served|die|died|send|sent|expect|expected|build|built|stay|stayed|fall|fell|cut|reach|reached|kill|killed|remain|remained|suggest|suggested|raise|raised|pass|passed|sell|sold|require|required|report|reported|decide|decided|pull|pulled|develop|developed|and|or|but|if|then|else|when|where|while|which|that|this|these|those|what|who|whom|whose)$' | \
        grep -E '^[a-z]{3,}$' | \
        sort -u
}

# Calculate simple word overlap similarity
calculate_similarity() {
    local text1="$1"
    local text2="$2"

    local words1=$(echo "$text1" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '\n' | sort -u)
    local words2=$(echo "$text2" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '\n' | sort -u)

    local common=$(echo -e "$words1\n$words2" | sort | uniq -d | wc -l)
    local total1=$(echo "$words1" | wc -l)
    local total2=$(echo "$words2" | wc -l)

    if [[ $total1 -eq 0 || $total2 -eq 0 ]]; then
        echo "0"
        return
    fi

    # Jaccard similarity
    local union=$((total1 + total2 - common))
    local similarity=$((common * 100 / union))
    echo "$similarity"
}

KEYWORDS=$(extract_keywords "$TASK")
TASK_LOWER=$(echo "$TASK" | tr '[:upper:]' '[:lower:]')

# Results arrays
declare -a SIMILAR_IMPLEMENTATIONS
declare -a UTILITIES
declare -a PATTERNS
declare -a TEST_EXAMPLES

# Search for similar implementations (classes and functions)
if [[ -f "${INDEX_DIR}/structure.json" ]]; then
    STRUCTURE=$(cat "${INDEX_DIR}/structure.json")

    # Search classes
    echo "$STRUCTURE" | jq -c '.classes[]?' 2>/dev/null | while read -r class; do
        if [[ -n "$class" ]]; then
            name=$(echo "$class" | jq -r '.name')
            file=$(echo "$class" | jq -r '.file')
            line=$(echo "$class" | jq -r '.line')

            # Check if keywords match
            for keyword in $KEYWORDS; do
                if echo "$name" | grep -qi "$keyword"; then
                    similarity=$(calculate_similarity "$TASK" "$name")
                    if [[ $similarity -ge $THRESHOLD ]]; then
                        SIMILAR_IMPLEMENTATIONS+=("$(jq -n --arg name "$name" --arg file "$file" --argjson line "$line" --argjson score "$similarity" '{name: $name, file: $file, line: $line, similarity: $score, type: "class"}')")
                    fi
                    break
                fi
            done
        fi
    done

    # Search functions
    echo "$STRUCTURE" | jq -c '.functions[]?' 2>/dev/null | while read -r func; do
        if [[ -n "$func" ]]; then
            name=$(echo "$func" | jq -r '.name')
            file=$(echo "$func" | jq -r '.file')
            line=$(echo "$func" | jq -r '.line')

            # Check for utility patterns (helpers, utils)
            if echo "$file" | grep -qiE "util|helper|common|shared|lib"; then
                UTILITIES+=("$(jq -n --arg name "$name" --arg file "$file" --argjson line "$line" '{name: $name, file: $file, line: $line, type: "utility"}')")
            fi

            # Check if keywords match
            for keyword in $KEYWORDS; do
                if echo "$name" | grep -qi "$keyword"; then
                    similarity=$(calculate_similarity "$TASK" "$name")
                    SIMILAR_IMPLEMENTATIONS+=("$(jq -n --arg name "$name" --arg file "$file" --argjson line "$line" --argjson score "$similarity" '{name: $name, file: $file, line: $line, similarity: $score, type: "function"}')")
                    break
                fi
            done
        fi
    done
fi

# Detect patterns from class/file names
if [[ -f "${INDEX_DIR}/structure.json" ]]; then
    # Look for common patterns
    if echo "$STRUCTURE" | jq -e '.classes[]? | select(.name | test("Service$"))' > /dev/null 2>&1; then
        PATTERNS+=('{"pattern": "Service Layer", "description": "Use *Service classes for business logic", "examples": []}')
    fi
    if echo "$STRUCTURE" | jq -e '.classes[]? | select(.name | test("Controller$"))' > /dev/null 2>&1; then
        PATTERNS+=('{"pattern": "Controller Pattern", "description": "Use *Controller classes for request handling", "examples": []}')
    fi
    if echo "$STRUCTURE" | jq -e '.classes[]? | select(.name | test("Repository$"))' > /dev/null 2>&1; then
        PATTERNS+=('{"pattern": "Repository Pattern", "description": "Use *Repository classes for data access", "examples": []}')
    fi
fi

# Search for test examples
if [[ -f "${INDEX_DIR}/dependencies.json" ]]; then
    DEPENDENCIES=$(cat "${INDEX_DIR}/dependencies.json")
    TEST_FILES=$(echo "$DEPENDENCIES" | jq -r '.files[]? | select(.source_file | test("test|spec"; "i")) | .source_file' 2>/dev/null | sort -u | head -5)

    for test_file in $TEST_FILES; do
        if [[ -n "$test_file" ]]; then
            TEST_EXAMPLES+=("$(jq -n --arg file "$test_file" '{file: $file, type: "test_example"}')")
        fi
    done
fi

# Count results
TOTAL_SIMILAR=${#SIMILAR_IMPLEMENTATIONS[@]}
TOTAL_UTILITIES=${#UTILITIES[@]}
TOTAL_PATTERNS=${#PATTERNS[@]}
TOTAL_TESTS=${#TEST_EXAMPLES[@]}
TOTAL_RESULTS=$((TOTAL_SIMILAR + TOTAL_UTILITIES + TOTAL_PATTERNS + TOTAL_TESTS))

# Output
if [[ "$FORMAT" == "json" ]]; then
    jq -n \
        --arg task "$TASK" \
        --argjson similar_count "$TOTAL_SIMILAR" \
        --argjson utility_count "$TOTAL_UTILITIES" \
        --argjson pattern_count "$TOTAL_PATTERNS" \
        --argjson test_count "$TOTAL_TESTS" \
        '{
            task: $task,
            summary: {
                similar_implementations: $similar_count,
                utilities: $utility_count,
                patterns: $pattern_count,
                test_examples: $test_count
            }
        }'
else
    echo ""
    echo "Task: $TASK"
    echo "Keywords: $(echo $KEYWORDS | tr '\n' ', ')"
    echo ""

    if [[ $TOTAL_RESULTS -eq 0 ]]; then
        echo "No reusable code suggestions found."
        echo ""
        echo "This may be a new feature with no existing similar implementations."
        exit 2
    fi

    if [[ $TOTAL_SIMILAR -gt 0 ]]; then
        echo "=== Similar Implementations ==="
        for impl in "${SIMILAR_IMPLEMENTATIONS[@]}"; do
            name=$(echo "$impl" | jq -r '.name')
            file=$(echo "$impl" | jq -r '.file')
            line=$(echo "$impl" | jq -r '.line')
            score=$(echo "$impl" | jq -r '.similarity')
            type=$(echo "$impl" | jq -r '.type')

            if [[ $score -ge 90 ]]; then
                echo "  [HIGH MATCH] $name ($type)"
                echo "    Similarity: ${score}%"
                echo "    Location: $file:$line"
                echo "    Recommendation: Reuse this instead of reimplementing"
            else
                echo "  $name ($type) - ${score}% similar"
                echo "    Location: $file:$line"
            fi
            echo ""
        done
    fi

    if [[ $TOTAL_UTILITIES -gt 0 ]]; then
        echo "=== Reusable Utilities ==="
        for util in "${UTILITIES[@]}"; do
            name=$(echo "$util" | jq -r '.name')
            file=$(echo "$util" | jq -r '.file')
            echo "  $name"
            echo "    File: $file"
        done
        echo ""
    fi

    if [[ $TOTAL_PATTERNS -gt 0 ]]; then
        echo "=== Architecture Patterns ==="
        for pattern in "${PATTERNS[@]}"; do
            pname=$(echo "$pattern" | jq -r '.pattern')
            pdesc=$(echo "$pattern" | jq -r '.description')
            echo "  $pname"
            echo "    $pdesc"
        done
        echo ""
    fi

    if [[ $TOTAL_TESTS -gt 0 ]]; then
        echo "=== Test Examples ==="
        for test in "${TEST_EXAMPLES[@]}"; do
            file=$(echo "$test" | jq -r '.file')
            echo "  $file"
        done
        echo ""
    fi
fi

exit 0
