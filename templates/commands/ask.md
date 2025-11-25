# Query Codebase with Natural Language

Ask questions about your codebase using natural language. The system searches the index and provides answers with code references.

## Overview

The `/speckitsmart.ask` command enables natural language queries like:
- "Where is user authentication handled?"
- "What API endpoints exist for orders?"
- "How is the database connected?"
- "Which services integrate with Stripe?"

## Prerequisites

**Hard Requirement**: Codebase index must exist

```bash
# Check if index exists
if [[ ! -d ".analysis/index" ]]; then
    echo "Error: Codebase index not found."
    echo "Run /speckitsmart.index first to build the index."
    exit 1
fi
```

## Usage

```bash
/speckitsmart.ask "<your question>"
```

## Supported Question Categories

1. **Architecture & Patterns**: "What design patterns are used?", "How is the app structured?"
2. **Data Models**: "What database tables exist?", "Show me the User model"
3. **API Endpoints**: "List all REST endpoints", "What GraphQL queries are available?"
4. **External Integrations**: "What third-party services are used?", "Where is Stripe integrated?"
5. **Authentication Flows**: "How does login work?", "Where is JWT validated?"
6. **Business Logic**: "Where is payment processing handled?", "How are emails sent?"

## Examples

```bash
# Find authentication logic
/speckitsmart.ask "Where is user authentication handled?"

# Discover API endpoints
/speckitsmart.ask "What API endpoints exist for managing users?"

# Understand data models
/speckitsmart.ask "Show me the database schema for orders"

# Find external integrations
/speckitsmart.ask "Which services use environment variables?"

# Locate business logic
/speckitsmart.ask "How is email sending implemented?"
```

## Output Format

```
Answer: <concise answer based on index>

Relevant Code:
- src/routes/auth.ts:12 - POST /auth/login endpoint
- src/services/AuthService.ts:25 - login() method
- src/models/User.ts:8 - User class with authentication methods

Confidence: 85%

Related Files:
- src/middleware/auth.ts
- src/config/jwt.ts
```

## Search Strategy

The system searches across:
1. **Code structure**: Classes, functions, interfaces matching keywords
2. **Data models**: Database tables and ORM entities
3. **API endpoints**: REST routes, GraphQL resolvers matching path/name
4. **External APIs**: Third-party service names and API calls
5. **Dependencies**: Import/export relationships

## Performance

- Query response time: <5 seconds (95th percentile)
- Concurrent queries supported
- Results ranked by relevance

## Tips for Better Results

- **Be specific**: "Where is Stripe payment processing?" vs "payment"
- **Use domain terms**: "authentication", "endpoints", "models", "integrations"
- **Ask about patterns**: "What classes extend BaseModel?"
- **Reference technologies**: "Where is Express routing configured?"

## Next Steps

After getting answers:
- Navigate to referenced files with line numbers
- Refine questions based on initial results
- Use `/speckitsmart.wiki` for comprehensive documentation

---

## Implementation

**Prerequisites Check**: Use hard prerequisite validation

```bash
# Platform detection
PLATFORM=$(bash scripts/bash/detect-os.sh 2>/dev/null || echo "unix")

# Check index exists
if [[ "$PLATFORM" == "windows" ]]; then
    INDEX_CHECK=$(powershell.exe -ExecutionPolicy Bypass -File scripts/powershell/Check-IndexPrerequisite.ps1)
else
    INDEX_CHECK=$(bash scripts/bash/check-index-prerequisite.sh)
fi

INDEX_EXISTS=$(echo "$INDEX_CHECK" | jq -r '.index_exists')

if [[ "$INDEX_EXISTS" != "true" ]]; then
    echo "Error: $(echo "$INDEX_CHECK" | jq -r '.error')"
    exit 1
fi

# Show staleness warning
IS_STALE=$(echo "$INDEX_CHECK" | jq -r '.is_stale // false')
AGE_DAYS=$(echo "$INDEX_CHECK" | jq -r '.age_days // 0')

if [[ "$IS_STALE" == "true" ]]; then
    echo "⚠️  Warning: Index is $AGE_DAYS days old. Results may be outdated."
    echo "Tip: Run /speckitsmart.index --incremental to update"
    echo ""
fi
```

**Parse Question and Route**:

```bash
# Get question from arguments
QUESTION="$*"

if [[ -z "$QUESTION" ]]; then
    echo "Error: No question provided"
    echo "Usage: /speckitsmart.ask \"<your question>\""
    exit 1
fi

# Route to platform script
if [[ "$PLATFORM" == "windows" ]]; then
    powershell.exe -ExecutionPolicy Bypass -File .specify/scripts/powershell/Search-KnowledgeBase.ps1 -Question "$QUESTION"
else
    bash .specify/scripts/bash/search-knowledge-base.sh "$QUESTION"
fi
```

The command delegates to:
- **Bash**: `.specify/scripts/bash/search-knowledge-base.sh`
- **PowerShell**: `.specify/scripts/powershell/Search-KnowledgeBase.ps1`

Both scripts:
1. Load index files from `.analysis/index/`
2. Parse question to extract keywords
3. Search across all index data structures
4. Rank results by relevance
5. Format answer with code references
6. Calculate confidence score
