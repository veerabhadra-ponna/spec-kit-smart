---
stage: branch-setup
requires: input-collection
outputs: branch_name, spec_dir
version: 1.0.0
next: 04-generate-spec.md
---

# Stage 3: Branch Setup

## Purpose

Create the feature branch and initialize the spec directory.

---

## Step 1: Generate Short Name

Analyze the feature description and create a 2-4 word short name:

**Guidelines:**
- Use action-noun format: "add-user-auth", "fix-payment-bug"
- Preserve technical terms: OAuth2, API, JWT
- Keep concise but descriptive

**Examples:**
- "Add user authentication" → `user-auth`
- "Implement OAuth2 for API" → `oauth2-api-integration`
- "Create analytics dashboard" → `analytics-dashboard`
- "Fix payment timeout bug" → `fix-payment-timeout`

---

## Step 2: Find Next Branch Number

Check all sources for the highest existing number:

```bash
# Fetch latest
git fetch --all --prune

# Check remote branches
git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'

# Check local branches
git branch | grep -E '^[* ]*[0-9]+-<short-name>$'

# Check specs directories
ls specs/ | grep -E '^[0-9]+-<short-name>$'
```

Use N+1 for the new branch number.

---

## Step 3: Run Create Feature Command

Execute the speckitadv create-feature command (cross-platform):

```bash
speckitadv create-feature "{{feature}}" --json --number N+1 \
  --jira "{{jira}}" --short-name "{{short_name}}"
```

**Parse JSON output** for BRANCH_NAME and SPEC_FILE paths.

JSON output format:

```json
{
  "BRANCH_NAME": "feature/001-C12345-7890-user-auth",
  "SPEC_FILE": "specs/001-C12345-7890-user-auth/spec.md",
  "FEATURE_NUM": "001"
}
```

---

## Output

```text

✓ Branch created
  - Branch: feature/{{number}}-{{jira}}-{{short_name}}
  - Spec dir: specs/{{number}}-{{jira}}-{{short_name}}/
```

---

## NEXT

```text

speckitadv specify --stage=4 --chain={{chain_id}}
```

**Note:** The feature directory is auto-detected from the created spec folder.
