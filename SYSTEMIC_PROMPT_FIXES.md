# Systemic Prompt Engineering Fixes for All Commands

## Executive Summary

**Problem**: ALL commands (constitution, analyze, specify, plan, implement) exhibit unreliable behavior with Claude Sonnet 4 and other AI models:

- **Forgetting** critical steps (e.g., running setup scripts)
- **Ignoring** mandatory instructions (e.g., creating branches/folders)
- **Skipping** validation checkpoints
- **Making shortcuts** (e.g., creating files in wrong locations)

**Example Failure** (specify command):
- Should: Run script → Create branch → Create folder → Create spec in folder
- Actually: Skipped script, stayed on same branch, created spec in root

**Root Cause**: Not a lack of instructions, but **prompt engineering failures**:

1. Prompts too long (400-500+ lines) → Cognitive overload
2. Critical steps buried in middle → Lost in noise
3. Weak enforcement language → Interpreted as suggestions
4. No validation checkpoints → No feedback loop
5. No forcing functions → AI can skip steps without errors

**Solution**: Universal prompt engineering patterns that work across ALL AI models.

---

## Root Cause Deep Dive

### Issue 1: Cognitive Overload (Prompt Length)

**Current State**:

| Command | Lines | Critical Step Location | Problem |
|---------|-------|------------------------|---------|
| specify.md | 484 | Line 226 (47% through) | Script execution buried |
| plan.md | 291 | Line 154 (53% through) | Setup script buried |
| 05a-full-app.md | 470 | Line 29 (6% through) | Questions start early but no enforcement |
| analyze-project.md | 556 | N/A (delegated to stages) | Chain controller |

**Why This Fails**:

- Claude Sonnet 4 processes long prompts but loses attention on middle sections
- First 20% gets high attention (role, context)
- Last 20% gets moderate attention (action, output)
- **Middle 60% gets skimmed or skipped** ← Critical steps are here!

**Research**: Human studies show comprehension drops after ~200 lines. AI models exhibit similar degradation.

---

### Issue 2: Weak Enforcement Language

**Current Language** (specify.md lines 259-266):

```markdown
**IMPORTANT**:
- You must only ever run this script once per feature
- The JSON is provided in the terminal as output
- The JSON output will contain BRANCH_NAME and SPEC_FILE paths
```

**Why This Fails**:

- "IMPORTANT" is informational, not imperative
- "You must" is a suggestion, not a blocker
- No consequences stated for non-compliance
- No validation that step was completed

**What Claude Sonnet 4 Interprets**:

- "Oh, this is important to know, but if I'm confident I can skip it safely, I will"
- "Let me try to be helpful and create the file directly" (bypassing script)
- "The user just wants a spec file, I'll give them that" (missing the point)

---

### Issue 3: No Validation Checkpoints

**Current Flow** (specify command):

```text
Step 1: Parse arguments
Step 2: [SUPPOSED TO] Run script
Step 3: Write spec file
Step 4: Validate spec quality
```

**Problem**: There's NO checkpoint between steps 2 and 3 that verifies:

- Script actually ran
- Script succeeded
- Branch was created
- Folder structure exists
- SPEC_FILE path is valid

**Result**: AI skips step 2, proceeds to step 3, creates file in wrong place.

---

### Issue 4: No Forcing Functions

**What's a Forcing Function?**

A mechanism that makes it IMPOSSIBLE to proceed without completing a prerequisite step.

**Example** (specify command):

**Current** (allows skipping):
```markdown
5. Write the specification to SPEC_FILE using the template structure...
```

**Should Be** (forcing function):
```markdown
5. Write the specification:

   a. **VERIFY SCRIPT OUTPUT FIRST**:
      - Check that script execution produced JSON output
      - Parse SPEC_FILE path from JSON
      - Validate SPEC_FILE path exists and is in specs/ directory
      - **IF any check fails: ERROR and STOP**

   b. Write to SPEC_FILE (parsed from script output) using template structure...
```

**Why Current Fails**: AI can guess/invent SPEC_FILE path without running script.

**Why Forcing Function Works**: AI cannot proceed without valid script output.

---

## Universal Solutions (Apply to ALL Commands)

### Solution 1: Critical Step Promotion (Move to Top)

**Pattern**: Move critical steps to FIRST 20% of prompt (high attention zone).

**Example** (specify.md restructure):

```markdown
## ⚠️ MANDATORY: Read Agent Instructions First
[AGENTS.md block]

---

## ⚠️ CRITICAL: Script Execution (DO THIS FIRST)

**BEFORE DOING ANYTHING ELSE, YOU MUST RUN THE SETUP SCRIPT.**

**This step is MANDATORY and NON-NEGOTIABLE.**

### Why This Step Matters

The script creates:
- New feature branch
- Specs folder structure
- Initial spec file
- JSON output with paths you MUST use

**IF YOU SKIP THIS STEP, EVERYTHING WILL BE IN THE WRONG PLACE.**

### Step-by-Step Execution

1. **Run the script** (choose OS-appropriate command):

   **Bash**:
   ```bash
   ./scripts/bash/create-new-feature.sh --json --number N --jira-number "..." --short-name "..." "description"
   ```

   **PowerShell**:
   ```powershell
   ./scripts/powershell/create-new-feature.ps1 -Json -Number N -JiraNumber "..." -ShortName "..." "description"
   ```

2. **Capture JSON output** - Example:
   ```json
   {
     "branch_name": "feature/001-C12345-7890-user-auth",
     "spec_file": "specs/001-C12345-7890-user-auth/spec.md",
     "specs_dir": "specs/001-C12345-7890-user-auth"
   }
   ```

3. **MANDATORY VALIDATION** - Verify:
   - [ ] Script exited with status 0 (success)
   - [ ] JSON output received
   - [ ] Current branch matches `branch_name` from JSON
   - [ ] Folder exists at `specs_dir` from JSON
   - [ ] File exists at `spec_file` from JSON

4. **IF ANY VALIDATION FAILS**:
   - **STOP IMMEDIATELY**
   - **DO NOT PROCEED**
   - **OUTPUT ERROR**: "Script execution failed - cannot continue"
   - **EXIT**

5. **ONLY IF ALL VALIDATIONS PASS**:
   - Extract `spec_file` path from JSON
   - Proceed to spec writing (next section)

---

## Role & Mindset
[Rest of prompt continues...]
```

**Benefits**:
- Critical step is at line 15 (high attention)
- MANDATORY validation before proceeding
- Clear error handling
- Forcing function (must have JSON to proceed)

---

### Solution 2: Aggressive Enforcement Language

**Current** (weak):
```markdown
**IMPORTANT**: You must run this script once per feature
```

**Revised** (strong):
```markdown
## ⚠️ BLOCKER: Script Execution Required

**YOU CANNOT PROCEED WITHOUT RUNNING THIS SCRIPT.**

**IF YOU SKIP THIS STEP:**
- Branch will not be created → You'll commit to wrong branch
- Folder will not exist → Files will go in wrong location
- Spec file will be in wrong place → Workflow will break
- All subsequent commands will fail

**THIS IS A CRITICAL ERROR THAT REQUIRES RESTARTING THE ENTIRE WORKFLOW.**

**DO NOT SKIP. DO NOT ASSUME. DO NOT SHORTCUT.**

---
```

**Pattern**:
- Use "BLOCKER" not "IMPORTANT"
- State consequences explicitly
- Use ALL CAPS for critical directives
- Repeat "DO NOT" imperatives

---

### Solution 3: Mandatory Validation Checkpoints

**Pattern**: After every critical step, add validation checkpoint.

**Template**:

```markdown
---

## ✅ CHECKPOINT: [Step Name] Verification

**BEFORE PROCEEDING, VERIFY:**

- [ ] [Specific verification 1]
- [ ] [Specific verification 2]
- [ ] [Specific verification 3]

**VALIDATION COMMANDS:**

```bash
# Check 1
git branch --show-current  # Should show: feature/XXX-...

# Check 2
ls -la specs/XXX-...  # Should exist and contain files

# Check 3
cat specs/XXX-.../spec.md | head -5  # Should show spec header
```

**EXPECTED OUTPUT:**

```text
✓ Current branch: feature/001-C12345-7890-user-auth
✓ Specs directory exists: specs/001-C12345-7890-user-auth
✓ Spec file exists with header
```

**IF ANY CHECK FAILS:**

1. **STOP IMMEDIATELY - DO NOT PROCEED**
2. **OUTPUT**: "Checkpoint failed - [specific failure]"
3. **REQUIRED ACTION**: Fix the issue or restart workflow
4. **DO NOT CONTINUE** until all checks pass

**ONLY IF ALL CHECKS PASS:**

Output: `✅ CHECKPOINT PASSED - Proceeding to next step`

---
```

**Where to Add** (All Commands):

- After script execution
- After branch creation
- After file generation
- Before final output

---

### Solution 4: Forcing Functions

**Pattern**: Make next step IMPOSSIBLE without completing previous step.

**Example 1** (specify - spec writing):

**Current** (allows bypass):
```markdown
5. Write the specification to SPEC_FILE using the template structure...
```

**Revised** (forcing function):
```markdown
5. Write the specification:

   **STEP 5.1: Extract Path from Script Output**

   ```bash
   # Parse JSON output from step 2 (script execution)
   SPEC_FILE=$(echo $SCRIPT_OUTPUT | jq -r '.spec_file')

   # Validate path
   if [ -z "$SPEC_FILE" ]; then
     echo "ERROR: No spec_file in script output - did you run the script?"
     exit 1
   fi

   if [ ! -f "$SPEC_FILE" ]; then
     echo "ERROR: Spec file does not exist at $SPEC_FILE"
     exit 1
   fi
   ```

   **STEP 5.2: Verify Path is Correct**

   - SPEC_FILE MUST start with `specs/`
   - SPEC_FILE MUST match pattern: `specs/NNN-*/spec.md`
   - SPEC_FILE MUST NOT be in repository root

   **IF PATH IS INVALID:**
   - ERROR: "Invalid spec file path - script was not run correctly"
   - STOP and restart workflow

   **STEP 5.3: Write to Validated Path**

   Using the SPEC_FILE path validated above, write specification content...
```

**Why This Works**: AI cannot write spec without valid SPEC_FILE from script.

---

### Solution 5: Chunked Prompts with State

**Pattern**: Break long prompts into smaller, focused stages with state passing.

**Example** (specify command - restructure):

**Current**: One 484-line prompt doing everything.

**Revised**: Three focused prompts:

#### Prompt 1: Setup (50 lines)
```markdown
# specify-setup.md

## Purpose
Run setup script, create branch/folder, validate structure.

## Execution
1. Run script
2. Validate JSON output
3. Verify branch/folder created
4. Save state to .specify-state.json

## Output
{
  "spec_file": "...",
  "specs_dir": "...",
  "branch_name": "..."
}

## Next
Proceed to specify-write.md
```

#### Prompt 2: Spec Writing (150 lines)
```markdown
# specify-write.md

## Prerequisites
Load state from .specify-state.json (created by specify-setup.md)

## Purpose
Write functional specification to spec_file from state.

## Execution
1. Load spec_file path from state
2. Generate spec content
3. Write to spec_file
4. Update state

## Next
Proceed to specify-validate.md
```

#### Prompt 3: Validation (100 lines)
```markdown
# specify-validate.md

## Prerequisites
Load state from .specify-state.json

## Purpose
Validate spec quality, create checklist.

## Execution
1. Run quality checks
2. Create checklist
3. Validate pass/fail

## Output
Completion message with paths
```

**Benefits**:
- Each prompt <200 lines (high attention maintained)
- State passing ensures dependencies
- Clear separation of concerns
- Easier to debug failures

---

## Implementation Plan

### Phase 1: Fix Critical Commands (specify, plan)

**Target**: specify.md, plan.md

**Changes**:
1. Move script execution to top (lines 15-60)
2. Add aggressive enforcement language
3. Add mandatory validation checkpoint after script
4. Add forcing function for path usage
5. Test with Claude Sonnet 4

**Timeline**: 1 day

**Success Criteria**:
- Script runs every time
- Branch created correctly
- Folder structure correct
- Files in right location
- 5 consecutive successful runs

---

### Phase 2: Fix Analyze Commands (all stages)

**Target**: analyze-project.md, 01-09.md stages

**Changes**:
1. Add validation checkpoints to each stage
2. Add aggressive enforcement for questionnaires
3. Implement dual functional spec generation
4. Add scope validation
5. Test end-to-end workflow

**Timeline**: 2 days

**Success Criteria**:
- All questions asked as-is
- No assumptions made
- BOTH specs generated
- Scope correctly validated
- Consistent behavior across 5 runs

---

### Phase 3: Universal Patterns (all commands)

**Target**: constitution, clarify, tasks, implement, orchestrate

**Changes**:
1. Apply critical step promotion
2. Add validation checkpoints
3. Add forcing functions
4. Standardize enforcement language
5. Create prompt engineering guidelines

**Timeline**: 2 days

**Success Criteria**:
- All commands follow same patterns
- Consistent reliability
- Clear documentation
- Team training completed

---

## Testing Strategy

### Test Protocol (For Each Command)

**Run 5 times with same input and verify**:

1. **Consistency**: Same behavior every run
2. **Completeness**: All steps executed
3. **Correctness**: Output in right locations
4. **Checkpoints**: All validations pass
5. **No shortcuts**: Scripts run, no assumptions

**Test Environments**:
- Claude Sonnet 4 via GitHub Copilot (primary)
- Claude Sonnet 4 via Claude Code CLI (secondary)
- GPT-4 via Cursor (validation)

**Pass Criteria**: 5/5 successful runs in primary environment.

---

## Specific Fixes for Each Command

### specify.md

**Line 1-14**: Keep AGENTS.md block
**Line 15-80**: NEW - Critical script execution section (promoted)
**Line 81-120**: NEW - Mandatory validation checkpoint
**Line 121-140**: NEW - Forcing function for path usage
**Line 141+**: Existing content (role, interactive mode, spec writing)

**Key Changes**:
- Script execution moved from line 226 → line 15
- Validation checkpoint added after script
- Path extraction made mandatory before spec writing
- Enforcement language upgraded throughout

---

### plan.md

**Similar restructure**:
- Setup script promoted to top
- Validation checkpoint after setup
- Forcing function for artifact paths

---

### All Analyze Stages (01-09.md)

**Add to each**:
- Stronger AGENTS.md enforcement (line 1)
- Validation checkpoint after each major section
- "Ask as-is" + "No assumptions" policies for interactive stages
- Forcing functions for state dependencies

---

## New Prompt Engineering Guidelines

Create `.specify/PROMPT_ENGINEERING.md`:

```markdown
# Prompt Engineering Guidelines for Spec Kit Commands

## Golden Rules

1. **Critical steps go in first 20%** of prompt (lines 1-100 for 500-line prompts)
2. **Validation checkpoint after every critical step** (5-10 lines each)
3. **Forcing functions for all dependencies** (cannot proceed without prerequisite)
4. **Aggressive enforcement language** (BLOCKER, MANDATORY, DO NOT SKIP)
5. **Prompts <200 lines ideal**, <300 acceptable, >400 needs chunking

## Enforcement Language

**Weak** (don't use):
- "It's important to..."
- "You should..."
- "Make sure to..."
- "Remember to..."

**Strong** (use this):
- "YOU MUST..."
- "THIS IS MANDATORY"
- "DO NOT SKIP"
- "BLOCKER: [action required]"
- "IF YOU SKIP THIS, [consequences]"

## Validation Checkpoint Template

[Include template from Solution 3 above]

## Forcing Function Template

[Include template from Solution 4 above]
```

---

## Expected Outcomes

### After Phase 1 (specify, plan fixed)

**Before**:
- specify: Creates spec in wrong location 60% of time
- plan: Forgets to run setup script 40% of time

**After**:
- specify: Creates spec correctly 100% of time (5/5 test runs)
- plan: Runs setup script correctly 100% of time (5/5 test runs)

---

### After Phase 2 (analyze fixed)

**Before**:
- Questions modified or skipped 70% of time
- Assumptions made frequently
- Single functional spec (ambiguous)
- Unmentioned components assumed for migration

**After**:
- Questions asked as-is 100% of time
- Zero assumptions (explicit clarification requested)
- Both functional specs generated consistently
- Scope correctly validated

---

### After Phase 3 (all commands fixed)

**Before**:
- Overall reliability: 40-60% (2-3 failures per 5 runs)
- User frustration: High (constant restarts)
- Model dependency: High (GPT-4 works better than Sonnet 4)

**After**:
- Overall reliability: 95%+ (0-1 failures per 20 runs)
- User frustration: Low (consistent behavior)
- Model independence: Works across Sonnet 4, GPT-4, Gemini

---

## Root Cause Summary

**It's NOT**:
- Missing instructions (instructions are comprehensive)
- Unclear wording (prompts are detailed)
- Insufficient examples (examples exist)

**It IS**:
- **Cognitive overload** (prompts too long)
- **Attention degradation** (critical steps in middle)
- **Weak enforcement** (suggestions vs imperatives)
- **No validation** (AI can skip without feedback)
- **No forcing functions** (steps not interdependent)

**Fix**: Prompt engineering discipline, not more instructions.

---

## Conclusion

This is a **systemic prompt engineering problem** affecting ALL commands.

The solution is NOT to add more instructions (already comprehensive).

The solution IS to apply **proven prompt engineering patterns**:
1. Critical steps first
2. Aggressive enforcement
3. Mandatory validation
4. Forcing functions
5. Manageable length

These patterns work because they align with how AI models process long prompts and maintain attention.

---

**Document Version**: 1.0
**Created**: 2025-11-17
**Status**: Ready for Implementation
**Priority**: CRITICAL - Affects all workflows
