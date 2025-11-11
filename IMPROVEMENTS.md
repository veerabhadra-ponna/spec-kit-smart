# Future Improvements

This document tracks all planned improvements and known limitations for the Spec Kit project.

**⚠️ IMPORTANT:** Never add TODO comments to prompt files or templates! They can confuse AI agents. Always add improvements here instead.

---

## 🔴 High Priority

### Scripts (create-new-feature.sh / .ps1)

- [ ] Add automated tests for regex patterns and edge cases
- [ ] Add environment variable for enforcing Jira requirement (`REQUIRE_JIRA=true`)
- [ ] Improve error messages with examples and suggestions
- [ ] Add validation examples to help text

### Interactive Prompts

- [ ] Add validation of interactive input format with clear error messages
  - Constitution: Validate PRINCIPLES/PROJECT METADATA structure
  - Specify: Validate JIRA:/FEATURE: line format
- [ ] Add retry logic if user input is malformed
- [ ] Add feature description quality checks (minimum length, keyword detection)
- [ ] Add confirmation step showing what will be created before proceeding

---

## 🟡 Medium Priority

### Testing & Quality

- [ ] Create test suite for branch detection regex patterns
- [ ] Add integration tests for script execution with various inputs
- [ ] Add smoke tests for common scenarios
- [ ] Test edge cases:
  - Very long branch names (near 244 char limit)
  - Special characters in Jira numbers
  - Empty/whitespace inputs
  - Concurrent branch creation

### Documentation

- [ ] Replace `[PLACEHOLDER_CONSTITUTION_EXAMPLES_LINK]` with real URL
- [ ] Add inline constitution examples (remove external dependency)
- [ ] Create troubleshooting guide for common errors
- [ ] Document branch naming convention in README

### User Experience

- [ ] Add progress indicators for long-running operations
- [ ] Improve error messages with actionable suggestions
- [ ] Add `--dry-run` flag to preview branch creation
- [ ] Add `--force` flag to override validations when needed

---

## 🟢 Low Priority / Nice to Have

### AGENTS.md Enforcement

- [ ] Explore technical enforcement alternatives (currently guidance-only)
- [ ] Add verification token system (if feasible)
- [ ] IDE plugin to auto-inject AGENTS.md into context
- [ ] Add reminder if AGENTS.md exists but not acknowledged

### Interactive Mode Enhancements

- [ ] Add autocomplete for common patterns
- [ ] Add interactive help/examples on demand
- [ ] Support multiple input formats (JSON, YAML, key-value)
- [ ] Add template library for common project types

### Branch Management

- [ ] Add command to list all feature branches
- [ ] Add command to cleanup old/merged branches
- [ ] Add branch naming validation before creation

### Corporate Guidelines - Future Enhancements

**Note**: Phase 1-4 completed. See "Completed Improvements" section below.

Additional nice-to-have features:

- [ ] Interactive guideline compliance checker
- [ ] Guideline diff tool (compare project vs template)
- [ ] Auto-fix common guideline violations
- [ ] Guideline analytics (compliance metrics)
- [ ] Enhanced CI/CD integration for guideline checking
- [ ] Guideline version management and migration tools
- [ ] Team-specific guideline overrides

### PowerShell Script

- [ ] Improve regex matching (mirror bash improvements)
- [ ] Add better error handling for Windows-specific issues
- [ ] Test on PowerShell Core (cross-platform)

### Reverse Engineering & Modernization Feature

**Current Status**: v1.0.0-alpha (EXPERIMENTAL) - Redesign Required

**Note**: Phases 1-4 complete (see "Completed Improvements" section). Phase 7 completed but requires redesign based on user feedback. Phase 8 (new) addresses core issues.

**Phases 2-5 Status**: See "Completed Improvements" section for details.

---

### Phase 8 - Interactive AI-Driven Analysis Workflow (HIGH PRIORITY) 🔴

**Current Problem** (User Feedback 2025-11-09):

The existing Python generators (`functional_spec_generator.py`, `tech_stack_proposer.py`, `prompt_generator.py`) produce **template-only artifacts** without real analysis of legacy code. This results in:

- ❌ `functional-spec.md` is just a template (no actual features from legacy code)
- ❌ `proposed-tech-stack.md` is just a template (no real tech stack analysis)
- ❌ Stage prompts are generic templates (no legacy code references)
- ❌ No interactive workflow to gather modernization requirements
- ❌ Cannot ask about target stack preferences, deployment infrastructure, IaC choices
- ❌ Generated artifacts don't provide useful feedback to Toolkit workflow

**Root Cause**: Python cannot perform semantic analysis like AI agents. The current approach has Python generating templates that should be filled by AI analysis + legacy code understanding.

**Solution**: Redesign to use **Interactive AI-Driven Workflow** with AI analysis + prompt templates (similar to meta-prompt approach used in regular Toolkit workflow).

---

#### 8.1 Interactive Workflow Design (CRITICAL)

**Objective**: Make analyze-project **INTERACTIVE-ONLY** with multi-step guided analysis.

**Workflow Steps**:

##### Step 1: Initial Inputs (Required)

```text
PROJECT_PATH: /path/to/legacy/project
ANALYSIS_DEPTH: QUICK | STANDARD | COMPREHENSIVE
FOCUS_AREAS: ALL | SECURITY | PERFORMANCE | ARCHITECTURE | DEPENDENCIES
```

##### Step 2: Quick Tech Stack Sampling

Scan codebase to identify current stack (language, framework, database,
enterprise bus, caching, etc.). Display findings to user:

```text
Detected Stack:
- Frontend: React 16.8 (JavaScript)
- Backend: Java 8 (Spring Boot 2.1)
- Database: Oracle 11g
- Message Bus: TIBCO EMS
- Caching: Memcached 1.4
- Build Tool: Maven 3.6
```

##### Step 3: Modernization Target Questions

Ask user about target stack preferences:

```text
MODERNIZATION PREFERENCES:

1. Backend Language:
   Current: Java 8
   Options:
   - [A] Java 21 LTS (same language, latest LTS)
   - [B] Python 3.12 LTS (different language)
   - [C] Other (specify)
   Your choice: ___

2. Database:
   Current: Oracle 11g
   Options:
   - [A] Oracle 21c (same vendor, latest)
   - [B] PostgreSQL 16 LTS (open source RDBMS)
   - [C] MongoDB 7.0 (NoSQL)
   - [D] Other (specify)
   Your choice: ___

3. Message Bus:
   Current: TIBCO EMS
   Options:
   - [A] TIBCO EMS (latest version)
   - [B] Apache Kafka (open source)
   - [C] Solace (cloud-native)
   - [D] Other (specify)
   Your choice: ___

4. Package Manager (for Java):
   Options:
   - [A] Maven (current)
   - [B] Gradle
   Your choice: ___

5. Target Deployment Infrastructure:
   Options:
   - [A] Dedicated server (physical/VM)
   - [B] Kubernetes cluster
   - [C] OpenShift
   - [D] Azure (App Service, AKS, etc.)
   - [E] AWS (ECS, EKS, Lambda, etc.)
   - [F] Google Cloud (GKE, Cloud Run, etc.)
   Your choice: ___

6. Infrastructure as Code (IaC):
   Options:
   - [A] Helm charts (for Kubernetes)
   - [B] Terraform
   - [C] OpenShift templates
   - [D] CloudFormation (AWS)
   - [E] ARM templates (Azure)
   - [F] None / Manual
   Your choice: ___

7. Containerization:
   Options:
   - [A] Docker containers
   - [B] Kubernetes (orchestration)
   - [C] Docker + Kubernetes
   - [D] No containerization
   Your choice: ___

8. Observability Stack:
   Options:
   - [A] ELK Stack (Elasticsearch, Logstash, Kibana)
   - [B] Prometheus + Grafana
   - [C] Azure Monitor / Application Insights
   - [D] AWS CloudWatch
   - [E] Google Cloud Operations
   - [F] OpenTelemetry (vendor-neutral)
   - [G] Other (specify)
   Your choice: ___

9. Security Requirements:
   Options:
   - [A] OAuth 2.0 / OpenID Connect
   - [B] JWT tokens
   - [C] SAML
   - [D] API Keys
   - [E] Mutual TLS
   - [F] Keep current auth mechanism
   Your choice: ___

10. Testing Strategy:
    Options:
    - [A] Unit tests only
    - [B] Unit + Integration tests
    - [C] Unit + Integration + E2E tests (full coverage)
    - [D] Minimal testing
    Your choice: ___
```

##### Step 4: Deep Legacy Analysis

**Scan ALL code files** to understand functionality. Analyze legacy codebase thoroughly:

- Controllers, services, models, repositories
- Configuration files (application.properties, XML configs)
- Database schemas (DDL, migrations)
- API endpoints and contracts
- Business logic and workflows
- Security implementations (auth, authorization, encryption)
- Integration points (external APIs, message queues)
- Deployment scripts and infrastructure code
- Containerization configs (Dockerfile, docker-compose.yml)
- Observability configs (logging, monitoring, tracing)
- Testing suites (unit, integration, E2E tests)

##### Step 5: Clarification Questions (If Needed)

After deep analysis, ask user for any missing details:

```text
CLARIFICATIONS NEEDED:

  1. Your legacy app uses custom encryption for PII fields.
     Should we:
     - [A] Preserve exact encryption algorithm (AES-256-CBC with custom key derivation)
     - [B] Upgrade to modern encryption (AES-256-GCM with industry standard KDF)

  2. Found hardcoded API timeout of 30 seconds in multiple places.
     Should we:
     - [A] Preserve 30 second timeout
     - [B] Make configurable via environment variable

  ... (other clarifications based on analysis findings)
  ```

##### Step 6: Generate Artifacts

Using AI analysis of legacy code + user's modernization preferences, generate:

- ✅ `analysis-report.md` - Comprehensive findings
- ✅ `EXECUTIVE-SUMMARY.md` - High-level overview for stakeholders
- ✅ `functional-spec.md` - BA document (WHAT system does) with REAL features
- ✅ `technical-spec.md` - Architecture document (HOW to build) with target stack
- ✅ Stage prompts for Toolkit workflow (6 stages):
  - `constitution-prompt.md` - Principles for new system
  - `specify-prompt.md` - Requirements for specify stage (uses functional-spec.md)
  - `plan-prompt.md` - Architecture for plan stage (uses technical-spec.md)
  - `clarify-prompt.md` - Clarification guidance + "consult legacy app as source of truth"
  - `tasks-prompt.md` - Task breakdown guidance
  - `implement-prompt.md` - Implementation guidance + "consult legacy app as source of truth"

**Artifacts NOT Generated** (User Feedback):

- ❌ `recommended-constitution.md` - Not needed (replaced by constitution-prompt)
- ❌ `upgrade-plan.md` - Not needed (inline upgrade not goal; full modernization)
- ❌ `proposed-tech-stack.md` - Not needed (embedded in technical-spec.md)

---

#### 8.2 Implementation Tasks

##### Task 1: Create Interactive Analysis Prompt Template

- [x] ~~Create `templates/commands/analyze-project-interactive.md`~~ **Updated `analyze-project.md` directly instead**
- [x] Define multi-step workflow with clear sections
- [x] Add tech stack detection logic (sampling approach)
- [x] Add modernization preference questionnaire (10 questions)
- [x] Add deep analysis guidance (what to look for in legacy code)
- [x] Add artifact generation instructions with real examples

**Completed**: 2025-11-09 - Implemented in `templates/commands/analyze-project.md`

##### Task 2: Create Artifact Generation Templates

**Reference**: Used structure from `tmp/Meta-Prompt - Universal Meta-Prompt to Gen
BA_ARCH_EXEC_AIB_SPEC_JSON docs.md` (reference file later removed to fix markdownlint errors)

- [x] Create `templates/analysis/functional-spec-template.md`
  - **Base structure**: Meta-prompt Section A (Business Analysis)
  - **Adapt for legacy**: Add "Evidence" column with file:line references
  - **Sections**:
    - Executive Summary (WHAT/WHO/WHY extracted from code)
    - Problem & Goals (current state KPIs from legacy)
    - Personas & Journeys (from auth/user roles in code)
    - Functional Requirements (extracted with evidence: file:line)
    - Data Models (from DB schemas/migrations)
    - Configuration Mapping (all config files)
    - Known Quirks & Legacy Behaviors
  - **Placeholders**: `<<EXTRACT_FEATURES_FROM>>`, `<<EXTRACT_DATA_MODELS>>`,
    `<<EXTRACT_CONFIG>>`, etc.
- [x] Create `templates/analysis/technical-spec-template.md`
  - **Base structure**: Meta-prompt Section B (Architecture)
  - **Adapt for modernization**: Add "Legacy vs. Target" comparison
  - **Sections**:
    - Architectural Principles (extracted from legacy + new)
    - Why This Pattern (legacy pattern → target pattern + rationale)
    - Capabilities by Phase (50/30/15/5 with legacy features mapped)
    - High-Level Architecture (phase-colored Mermaid from meta-prompt)
    - Target Tech Stack (from user Q1-Q10 answers)
    - NFR Targets (SLO/SLI based on legacy + improvements)
    - Migration Path (strangler fig/big bang/hybrid)
  - **Placeholders**: `<<USER_CHOICE_LANGUAGE>>`, `<<USER_CHOICE_DATABASE>>`,
    `<<USER_CHOICE_DEPLOYMENT>>`, `<<LEGACY_PAIN_POINTS>>`, etc.
  - **Mermaid**: Use meta-prompt phase colors + adapt pattern for target infra
- [x] Create `templates/analysis/stage-prompt-templates/`
  - 6 template files: constitution, specify, plan, clarify, tasks, implement
  - Structure: Legacy Context + Modernization Guidance + Ready-to-Paste Prompt
  - Clarify & Implement prompts include: "Consult legacy app <<path>> as source of
    truth if specification is underspecified, ambiguous, or requires clarification"

**Completed**: 2025-11-09 - All templates created and markdownlint errors fixed

##### Task 3: Update analyze-project Command

- [x] Modify `templates/commands/analyze-project.md` to be INTERACTIVE-ONLY
- [x] ~~Remove non-interactive mode (arguments mode)~~ **Kept for script passthrough, removed confusing messaging**
- [x] Add "Act as senior developer and architect" guidance (already in Role & Mindset)
- [x] Add instruction to use Python analyzer for metrics only
- [x] Add instruction to use AI for semantic analysis and artifact generation

**Completed**: 2025-11-09 - Interactive workflow with 10 modernization questions implemented

##### Task 4: Remove Template-Only Python Generators

- [x] Remove `functional_spec_generator.py`
- [x] Remove `tech_stack_proposer.py`
- [x] Remove `prompt_generator.py`
- [x] Remove `principle_extractor.py`
- [x] Keep `report_generator.py` for analysis-report.md and metrics
- [x] Update `report_generator.py` imports to remove deleted generators

**Completed**: 2025-11-09 - All template-only generators removed, cleanup complete

##### Task 5: Update Python Analyzer Role

Python analyzer already focuses on **metrics and structure**:

- ✅ Tech stack detection (languages, frameworks, tools)
- ✅ Code metrics (LOC, complexity, test coverage)
- ✅ Dependency analysis (vulnerable packages, outdated versions)
- ✅ File structure analysis (directories, patterns)
- ✅ Generate `analysis-report.md` with technical findings

Python analyzer does NOT generate:

- ❌ Functional specifications (requires semantic understanding)
- ❌ Tech stack proposals (requires business context)
- ❌ Stage prompts (requires understanding of Toolkit workflow)

**Status**: Already correct - No changes needed

##### Task 6: Create Meta-Prompt Style Templates

**Reference**: Studied `tmp/Meta-Prompt - Universal Meta-Prompt to Gen
BA_ARCH_EXEC_AIB_SPEC_JSON docs.md` (file later removed)

- [x] Analyze meta-prompt structure and adapt for legacy code analysis:
  - **Section A (Business Analysis)** → Used for `functional-spec-template.md`
  - **Section B (Architecture)** → Used for `technical-spec-template.md`
  - **Mermaid patterns** → Adapted for target infrastructure (K8s, AWS, etc.)
  - **Phase coloring (50/30/15/5)** → Implemented in technical-spec template
  - **NFR measurability** → Convert legacy configs to SLO/SLI targets guidance added
  - **R→C→T traceability** → Mentioned in technical-spec template
  - **Determinism guardrails** → Use AI knowledge base for LTS (not hardcoded)
- [x] ~~Create `functional-spec-generator-prompt.md`~~ **Embedded in analyze-project.md Step 6**
- [x] ~~Create `technical-spec-generator-prompt.md`~~ **Embedded in analyze-project.md Step 6**

**Completed**: 2025-11-09 - Templates created with meta-prompt structure, guidance integrated into main prompt

##### Task 7: Integration Testing

- [ ] Test on real legacy project (e.g., Java 8 Spring Boot app)
- [ ] Validate that functional-spec.md contains REAL features (not templates)
- [ ] Validate that technical-spec.md contains target stack based on preferences
- [ ] Validate that stage prompts contain actual legacy code references
- [ ] Ensure artifacts can feed into Toolkit workflow successfully

**Status**: ⏳ User tested on ASP.NET project, identified UX issues (Phase 8.1)

---

#### 8.3 Implementation Plan (Phased Approach)

##### Week 1-2: Foundation & Design ✅ COMPLETED

- [x] Document current issues with detailed examples
- [x] Design new interactive workflow (state machine diagram)
- [x] Create wireframes for questionnaires (modernization preferences)
- [x] Study `tmp/Meta-Prompt - Universal Meta-Prompt...` thoroughly
  - Understand Section A (Business Analysis) structure
  - Understand Section B (Architecture) structure
  - Study Mermaid patterns and phase coloring
  - Study NFR measurability approach (SLO/SLI)
- [x] Design template structure for functional-spec.md (based on Section A)
- [x] Design template structure for technical-spec.md (based on Section B)
- [x] Get user approval on design before implementation

**Completed**: 2025-11-09

##### Week 3-4: Template Creation ✅ COMPLETED

- [x] Create `analyze-project-interactive.md` prompt template (updated `analyze-project.md` instead)
- [x] Create `functional-spec-template.md` with clear structure
- [x] Create `technical-spec-template.md` with clear structure
- [x] Create 6 stage-prompt templates
- [x] Add detailed examples in each template

**Completed**: 2025-11-09

##### Week 5-6: Refactoring ✅ COMPLETED

- [x] Update `analyze-project.md` command to use new workflow
- [x] Refactor or remove Python generators
- [x] Update Python analyzer to focus on metrics only (no changes needed)
- [x] Update `report_generator.py` to generate only technical reports
- [x] Test on sample legacy project (ASP.NET tested by user)

**Completed**: 2025-11-09

##### Week 7-8: Testing & Documentation ⏳ IN PROGRESS

- [ ] Test on 3 diverse legacy projects (Java, Python, Node.js)
- [x] Validate artifact quality (real content vs templates) - User confirmed good output
- [ ] Document new workflow in `docs/reverse-engineering.md`
- [ ] Create video walkthrough (optional)
- [x] Collect user feedback and iterate - **UX issues identified (see Phase 8.1)**

**Status**: User testing complete on ASP.NET project, UX improvements needed

---

#### 8.4 Success Criteria

##### Functional Requirements

- ✅ Analyze-project is INTERACTIVE-ONLY (no non-interactive mode)
- ✅ AI asks for PROJECT_PATH, ANALYSIS_DEPTH, FOCUS_AREAS upfront
- ✅ AI performs quick tech stack sampling and displays findings
- ✅ AI asks user about modernization preferences (target stack, deployment, IaC)
- ✅ AI performs deep analysis of legacy code (all files)
- ✅ AI asks clarification questions if needed
- ✅ AI generates artifacts with REAL content (not templates)

##### Artifact Quality

- ✅ `functional-spec.md` contains actual features from legacy code (with references)
- ✅ `technical-spec.md` contains target stack based on user preferences
- ✅ Stage prompts contain real legacy code references (file paths + line numbers)
- ✅ `analysis-report.md` contains technical metrics and findings
- ✅ `EXECUTIVE-SUMMARY.md` provides high-level overview for stakeholders

##### Integration

- ✅ Generated artifacts feed seamlessly into Toolkit workflow
- ✅ `specify` stage can use functional-spec.md as input
- ✅ `plan` stage can use technical-spec.md as input
- ✅ `constitution` stage can use extracted principles
- ✅ Other stages can use corresponding stage prompts

##### User Experience (Phase 8)

- ✅ Clear guidance at each step of the workflow
- ✅ Reasonable defaults for modernization choices
- ✅ Ability to skip optional questions
- ✅ Progress indicators during analysis
- ✅ Estimated time for each phase
- ✅ Ability to resume if interrupted

---

#### 8.5 Key Design Principles

##### Principle 1: Python for Structure, AI for Semantics

Python analyzer detects tech stack, calculates metrics, finds vulnerabilities.
AI agent understands business logic, extracts requirements, proposes solutions.
Clear separation of responsibilities.

##### Principle 2: Interactive Over Automatic

Always ask user for preferences (don't assume). Provide reasonable defaults but
allow customization. Explain why each question matters.

##### Principle 3: Evidence-Based Analysis

Every finding includes file path + line number reference. Features extracted
from actual code, not guessed. Configurations mapped from actual config files.

##### Principle 4: Template + AI = Real Content

Templates provide structure and guidance. AI fills templates with real analysis
of legacy code. Similar to meta-prompt approach in regular Toolkit workflow.

##### Principle 5: Toolkit Workflow Integration

Generated artifacts must be usable by downstream stages. Stage prompts must be
ready-to-paste. Functional-spec.md must be consumable by specify stage.
Technical-spec.md must be consumable by plan stage.

---

**Note on Phase 7**: Phase 7 (Analysis-to-Spec Workflow Integration) was completed on 2025-11-08 but has been superseded by Phase 8 redesign based on user feedback. The Python generators created in Phase 7 produced template-only artifacts without real legacy code analysis. See "Completed Improvements" section for Phase 7 historical record.

---

### Phase 8.1 - UX Enhancements: Conditional Questions (MEDIUM PRIORITY) 🟡

**Current Problem** (User Feedback 2025-11-09):

After Phase 8 implementation, user testing revealed UX issues with the 10 modernization questions:

#### Issue 1: Confusing "Enter INTERACTIVE MODE" Message

**Problem**: The prompt says "Now I need to enter INTERACTIVE MODE since no specific arguments were provided" which is confusing because there's only one mode.

**Root Cause**: Legacy code from when we had both interactive and non-interactive modes. The `$ARGUMENTS` check is kept for bash/PowerShell script passthrough, but the messaging is outdated.

**Solution**:

- Remove "entering INTERACTIVE MODE" announcement
- Keep `$ARGUMENTS` parsing silently for script compatibility
- Directly say: "Please provide the following information:" (no mode explanation)

**Priority**: LOW - Minor UX polish, doesn't affect functionality

---

#### Issue 2: Irrelevant Questions

**Problem**: Asking questions that don't make sense based on detected stack or previous answers.

**Examples**:

- **Q3 (Message Bus)**: Code analysis shows "None detected" yet we ask 6 options
  - Why bad: Wastes time, feels like AI didn't pay attention
- **Q5 = "Keep traditional (IIS on Windows Server)"** then asking:
  - **Q6 (IaC)**: "Terraform? Kubernetes Helm charts?" (irrelevant for IIS)
  - **Q7 (Containerization)**: "Docker? Kubernetes?" (can't use with IIS)
  - Why absurd: IIS on Windows Server doesn't use these modern cloud tools

**Analysis** (Senior Architect Perspective):

#### Approach A: Ask Everything (Current - Simple but Poor UX)

Pros:

- ✓ Simple, consistent flow
- ✓ Might spark ideas ("I didn't know I could add message queue!")
- ✓ "None / Not needed" handles opt-out

Cons:

- ✗ Wastes time on irrelevant questions
- ✗ Poor UX - feels like AI isn't listening
- ✗ Asking about K8s after "keep traditional" is jarring

#### Approach B: Conditional Skip Logic (Smart but Complex)

Pros:

- ✓ Smart, context-aware
- ✓ Great UX - only relevant questions
- ✓ Faster workflow

Cons:

- ✗ Complex to implement (nested conditionals in prompts)
- ✗ Risk of skipping questions user wanted
- ✗ Harder to maintain

#### Approach C: Hybrid - Mark Optional + Conditional ⭐ RECOMMENDED

Question structure:

1. **Always ask**: Language, Database, Package Manager, Deployment
2. **Mark optional**: Questions for features not detected (Message Bus, Observability if none found)
3. **Conditional skip**: Q6-Q7 (IaC, Containerization) if Q5 = "traditional deployment"
4. **Educational notes**: Explain why we're skipping and when it might become relevant

Example:

```text
3. Message Bus/Queue [OPTIONAL - Not detected in legacy code]
   Current: None (email processing appears polling-based)

   Since your legacy app doesn't use message queues, you can skip this.
   However, modernization could benefit from async messaging for:
   - Email processing (background jobs instead of polling)
   - Future event-driven features

   Options:
   - [A] None / Not needed - Keep simple
   - [B] Redis Pub/Sub - Lightweight, also useful for caching
   - [C] Azure Service Bus - If going Azure
   - [D] Other (specify)
   Your choice (or press Enter to skip): ___

5. Target Deployment Infrastructure
   [Selected: A - Dedicated server (IIS) - Keep traditional]

6. Infrastructure as Code (IaC) [SKIPPED - Not applicable for traditional IIS]
   Note: If you later migrate to cloud, IaC becomes relevant.
   For Windows Server, deployment scripts or DSC are alternatives.

7. Containerization Strategy [SKIPPED - Not applicable for IIS]
   Note: Containerization requires migrating away from IIS.
   This becomes relevant if you choose cloud deployment in future.
```

**Benefits**:

- ✓ Respects user time (skip obviously irrelevant)
- ✓ Still allows discovery (optional = user can opt-in)
- ✓ Provides education (explain why question matters)
- ✓ Flexible (can still add message bus even if not detected)

---

#### Implementation Tasks

##### Task 1: Remove "Interactive Mode" Messaging ✅ COMPLETED (2025-11-09)

- [x] Update `templates/commands/analyze-project.md` User Input section
- [x] Remove "Enter INTERACTIVE MODE:" announcement
- [x] Keep `$ARGUMENTS` parsing for script compatibility
- [x] Change to direct: "Please provide the following information:"

**Complexity**: LOW (simple text change)

##### Task 2: Implement Conditional Question Logic ✅ COMPLETED (2025-11-09)

- [x] Add detection flags after tech stack analysis:
  - `HAS_MESSAGE_BUS`: true/false (from code analysis)
  - `HAS_OBSERVABILITY`: true/false (logging, monitoring configs detected)
  - `IS_TRADITIONAL_DEPLOYMENT`: true/false (based on Q5 answer)
- [x] Update Step 3 (Modernization Questions):
  - **Q1-Q2**: Always ask (Language, Database)
  - **Q3**: Mark `[OPTIONAL - Not detected]` if `!HAS_MESSAGE_BUS`
  - **Q4**: Always ask (Package Manager)
  - **Q5**: Always ask (Deployment)
  - **Q6-Q7**: Skip with `[Not applicable]` note if `IS_TRADITIONAL_DEPLOYMENT`
  - **Q8**: Mark `[OPTIONAL - Not detected]` if `!HAS_OBSERVABILITY`
  - **Q9-Q10**: Always ask (Auth, Testing)
- [x] Add educational notes explaining:
  - Why question is optional/skipped
  - When it might become relevant
  - Alternatives for current choice

**Complexity**: MEDIUM (conditional logic in prompts)

##### Task 3: Add "Press Enter to Skip" UX ✅ COMPLETED (2025-11-09)

- [x] For optional questions, add: `Your choice (or press Enter to skip): ___`
- [x] For skipped questions, show: `[SKIPPED - Reason]` with future guidance
- [x] Validate that AI handles empty/skipped responses gracefully

**Complexity**: MEDIUM (requires prompt flow testing)

---

#### Implementation Priority

**Phase 8.1a (Quick Win - Days)**: ✅ COMPLETED (2025-11-09)

- [x] Fix "Enter INTERACTIVE MODE" messaging
- [x] Add `[OPTIONAL]` and `[SKIPPED]` markers based on detection

**Phase 8.1b (Full Solution - Weeks)**: ✅ COMPLETED (2025-11-09)

- [x] Implement full conditional logic
- [x] Add educational notes
- [ ] Test on multiple scenarios (traditional vs cloud deployments) - **Requires user testing**

**Recommendation**: Phase 8.1a and 8.1b implementation complete. User testing recommended on real projects.

---

**Status**: ✅ IMPLEMENTED (2025-11-09) - Ready for user testing

---

### Phase 9 - Cross-Cutting Concern Analysis (HIGH PRIORITY) 🔴

**Status**: 📋 DESIGN PHASE - Ready for Implementation

**User Requirement** (2025-11-11):

Extend analyze-project to support **targeted cross-cutting concern migration** in addition to full application modernization.

**Business Context**:

Modern applications need to migrate specific cross-cutting concerns without rewriting the entire app:

- **Auth migration**: Custom JWT → Okta/Auth0/Azure AD
- **Database migration**: RDBMS → NoSQL (PostgreSQL → MongoDB)
- **Caching**: Add/replace caching layer (Memcached → Redis)
- **Messaging**: Migrate message bus (TIBCO → Kafka, RabbitMQ → Azure Service Bus)
- **Observability**: Custom logging → ELK/Prometheus/DataDog

**Current Gap**:

The analyze-project feature analyzes **entire applications** for full modernization. It cannot:

- ❌ Analyze only authentication code while ignoring other features
- ❌ Assess abstraction quality of a specific concern
- ❌ Recommend migration strategies for isolated concerns
- ❌ Provide concern-specific impact analysis
- ❌ Check if proper abstractions exist for easy swapping

---

#### 9.1 Architecture Assessment & Design

**Senior Developer/Architect Analysis**:

##### Current Architecture Strengths

1. **Interactive Workflow** (Phase 8)
   - 10-question modernization preference gathering
   - Conditional logic for relevant questions
   - Real content generation (not templates)

2. **Comprehensive Analysis**
   - Scanner.py detects tech stack, metrics, structure
   - Dependency analyzer finds vulnerabilities
   - Scoring engine calculates feasibility (0-100)

3. **Corporate Guidelines Integration**
   - Checks compliance with organizational standards
   - Multi-stack support (React+Java, Node+Python)

4. **Extensible Template System**
   - functional-spec-template.md (WHAT system does)
   - technical-spec-template.md (HOW to build)
   - stage-prompts/ for Toolkit workflow integration

##### Extension Points for Cross-Cutting Concerns

**Extension Point 1: Scope Selection (analyze-project.md:60-85)**

Current:

```text
## User Input & Interactive Mode

$ARGUMENTS

**IF** `$ARGUMENTS` is empty or contains the literal text "$ARGUMENTS":
   Please provide the following information:
   PROJECT_PATH: /path/to/existing/project
```

Proposed Enhancement:

```text
## User Input & Interactive Mode

$ARGUMENTS

**IF** `$ARGUMENTS` is empty:
   Please provide the following information:

   PROJECT_PATH: /path/to/existing/project

   ANALYSIS_SCOPE:
   - [A] Full Application Modernization (entire codebase)
   - [B] Cross-Cutting Concern Migration (specific area)
   Your choice: ___

   **IF CHOICE = [B]**, ask follow-up:

   CONCERN_TYPE:
   - [1] Authentication/Authorization
   - [2] Database/ORM Layer
   - [3] Caching Layer
   - [4] Message Bus/Queue
   - [5] Logging/Observability
   - [6] API Gateway/Routing
   - [7] File Storage/CDN
   - [8] Other (specify)
   Your choice: ___

   CURRENT_IMPLEMENTATION: ___  (detected from code, user confirms)
   TARGET_IMPLEMENTATION: ___   (e.g., "Migrate to Okta", "PostgreSQL → MongoDB")
```

**Extension Point 2: Scanner Module (scanner.py)**

Current: Scans entire codebase

Proposed Enhancement: Add concern-specific filtering

```python
class Scanner:
    def scan_project(self, project_path, concern_filter=None):
        """
        Args:
            concern_filter: Optional[ConcernFilter]
                - concern_type: "auth" | "database" | "cache" | etc.
                - patterns: List of file/import patterns to match
        """
        if concern_filter:
            # Use heuristics to identify concern-specific files
            # - File naming: auth*, login*, session*, jwt*
            # - Imports: passport, jsonwebtoken, bcrypt, oauth
            # - Decorators: @require_auth, @authenticated
            # - Config files: auth.config.js, security.yml
```

**Extension Point 3: New Module - concern_analyzer.py**

Proposed: Specialized analyzer for cross-cutting concerns

```python
class ConcernAnalyzer:
    """Analyzes a specific cross-cutting concern for migration readiness."""

    def analyze_abstraction_level(self, concern_code):
        """
        Returns: "HIGH" | "MEDIUM" | "LOW"

        HIGH:
            - Single entry point (e.g., AuthService interface)
            - Dependency injection used
            - Clean boundaries, no direct imports of implementation

        MEDIUM:
            - Multiple entry points but consistent pattern
            - Some direct dependencies
            - Mixed abstraction levels

        LOW:
            - Scattered across codebase
            - Direct implementation dependencies everywhere
            - No interfaces or contracts
        """

    def calculate_blast_radius(self, concern_code):
        """
        Returns:
            files_affected: int
            loc_affected: int
            percentage_of_codebase: float
        """

    def assess_coupling_degree(self, concern_code):
        """
        Returns: "LOOSE" | "MODERATE" | "TIGHT"

        Analyzes:
            - Direct vs indirect dependencies
            - Interface vs implementation coupling
            - Cyclic dependencies
        """

    def recommend_migration_strategy(self, abstraction_level, blast_radius, coupling):
        """
        Returns:
            strategy: "STRANGLER_FIG" | "ADAPTER_PATTERN" | "REFACTOR_FIRST" | "BIG_BANG"
            phasing: List[Phase]
            risk: "LOW" | "MEDIUM" | "HIGH"
            effort_estimate: str (e.g., "2-4 weeks")
        """
```

**Extension Point 4: New Templates**

Proposed templates for concern-specific analysis:

1. **concern-analysis-template.md**

```markdown
# Cross-Cutting Concern Analysis: <<CONCERN_TYPE>>

## Executive Summary

**Concern**: <<e.g., Authentication/Authorization>>
**Current**: <<e.g., Custom JWT implementation>>
**Target**: <<e.g., Migrate to Okta>>
**Recommendation**: <<STRANGLER_FIG | ADAPTER_PATTERN | etc.>>
**Risk**: <<LOW/MEDIUM/HIGH>>
**Effort**: <<2-4 weeks>>

## Current Implementation Analysis

### Entry Points (file:line references)

| Entry Point | Type | Usage Count | Evidence |
|-------------|------|-------------|----------|
| AuthService.authenticate() | Interface | 47 callsites | src/auth/AuthService.ts:23 |
| verifyToken() | Direct function | 12 callsites | src/middleware/auth.js:45 |

### Abstraction Assessment

**Level**: <<HIGH/MEDIUM/LOW>>

**Rationale**:
- <<Evidence 1>> (file:line)
- <<Evidence 2>> (file:line)

### Coupling Analysis

**Degree**: <<LOOSE/MODERATE/TIGHT>>

**Dependencies**:
- Database: User table (tight coupling - schema changes needed)
- API: 23 endpoints depend on auth middleware
- Frontend: 15 components check auth state

### Blast Radius

- Files affected: <<N>> files (<<X>>% of codebase)
- LOC affected: <<M>> lines
- Tests to update: <<T>> test files

## Missing Abstractions

**What's Missing**:
1. <<Abstraction 1>>: <<Why needed>> (file:line showing problem)
2. <<Abstraction 2>>: <<Why needed>> (file:line showing problem)

**Recommended Abstractions**:
- Create IAuthProvider interface
- Extract TokenService for token management
- Add AuthContext for dependency injection

## Migration Strategy

**Approach**: <<STRANGLER_FIG>>

**Phasing** (50/30/15/5):

### Phase 1 (50% value): Core Migration
- Week 1-2: Implement OktaAuthProvider with IAuthProvider interface
- Week 3: Dual-auth mode (support both JWT and Okta)
- Week 4: Route 10% traffic to Okta (canary)

### Phase 2 (30% value): Rollout
- Week 5: Route 50% traffic to Okta
- Week 6: Full cutover with feature flag

### Phase 3 (15% value): Cleanup
- Week 7: Remove legacy JWT code
- Week 8: Update tests and documentation

### Phase 4 (5% value): Future-Proofing
- Add abstraction layer for easy provider swapping
- Document migration lessons learned

## Rollback Strategy

- Feature flag: `USE_OKTA_AUTH` (instant rollback)
- Database: No schema changes (rollback safe)
- API: Backward compatible tokens during transition

## Impact on Other Concerns

| Concern | Impact | Mitigation |
|---------|--------|------------|
| Database | None | Auth tokens in separate table |
| Caching | Session cache keys change | Update cache prefix |
| Logging | Auth events format changes | Update log parsers |

## Testing Strategy

- Unit tests: Update 47 auth-related tests
- Integration tests: Add Okta mock server
- E2E tests: Test both auth flows during transition

## Success Criteria

- ✅ Zero downtime during migration
- ✅ 100% feature parity with legacy auth
- ✅ < 5% performance degradation
- ✅ Instant rollback capability

---

## Appendix: Detailed Evidence

### File-by-File Analysis
...
```

2. **abstraction-recommendations-template.md**

```markdown
# Abstraction Recommendations: <<CONCERN_TYPE>>

## Current Architecture Gaps

### Gap 1: <<Gap Name>>
**Problem**: <<Description with file:line>>
**Impact**: <<Why this makes migration harder>>
**Recommendation**: <<How to fix>>

## Recommended Abstraction Patterns

### Pattern 1: Repository Pattern (for Database concern)
**Why**: Isolates data access logic
**Implementation**:
- Create IRepository<T> interface
- Implement PostgresRepository and MongoRepository
- Swap at runtime via dependency injection

### Pattern 2: Strategy Pattern (for Auth concern)
**Why**: Allows swapping auth providers
**Implementation**:
- Create IAuthProvider interface
- Implement JWTProvider, OktaProvider, Auth0Provider
- Select via configuration

## Refactoring Roadmap

### Phase 1: Extract Interfaces (1-2 weeks)
- [ ] Define IAuthProvider interface
- [ ] Define ITokenService interface
- [ ] Add dependency injection container

### Phase 2: Migrate to Interfaces (2-3 weeks)
- [ ] Update all callsites to use interfaces
- [ ] Remove direct implementation dependencies
- [ ] Add integration tests

### Phase 3: Implement New Provider (1-2 weeks)
- [ ] Create OktaAuthProvider implementing IAuthProvider
- [ ] Add configuration management
- [ ] Test side-by-side with legacy

## Future-Proofing

**Design for Change**:
- Use interfaces, not concrete classes
- Inject dependencies, don't hardcode
- Config-driven provider selection
- Feature flags for gradual rollout

**Next Migration Will Be Easy**:
- Okta → Auth0: Just implement Auth0Provider
- PostgreSQL → MongoDB: Just implement MongoRepository
- Redis → Memcached: Just implement MemcachedCache
```

---

#### 9.2 Implementation Tasks

##### Task 1: Enhance analyze-project.md Prompt ✨ DESIGN COMPLETE

**Changes**:

1. Add "ANALYSIS_SCOPE" question (Full App vs Cross-Cutting Concern)
2. Add "CONCERN_TYPE" follow-up question (8 common concerns)
3. Add "CURRENT_IMPLEMENTATION" and "TARGET_IMPLEMENTATION" inputs
4. Modify Step 4 (Deep Analysis) to focus on concern-specific code if [B] chosen

**Complexity**: MEDIUM (prompt template update)

**Estimated Effort**: 2-4 hours

##### Task 2: Create concern_analyzer.py Module ✨ DESIGN COMPLETE

**Purpose**: Specialized analyzer for cross-cutting concern migration

**Functions**:

- `analyze_abstraction_level()` - HIGH/MEDIUM/LOW scoring
- `calculate_blast_radius()` - Files/LOC affected
- `assess_coupling_degree()` - LOOSE/MODERATE/TIGHT
- `recommend_migration_strategy()` - Strategy selection algorithm
- `detect_missing_abstractions()` - Gap analysis
- `generate_refactoring_roadmap()` - Phased plan

**Complexity**: HIGH (new module, complex algorithms)

**Estimated Effort**: 2-3 weeks

##### Task 3: Extend scanner.py for Concern Filtering ✨ DESIGN COMPLETE

**Changes**:

1. Add `concern_filter` parameter to `scan_project()`
2. Implement heuristics for each concern type:
   - **Auth**: Files matching `auth*`, `login*`, `session*`, imports like `passport`, `jwt`
   - **Database**: Files with DB imports, ORM models, migration files
   - **Cache**: Files with cache imports, `@Cacheable` decorators
   - **Messaging**: Queue/topic files, message handlers
   - **Logging**: Logger config, log middleware

3. Build concern-specific dependency graph

**Complexity**: MEDIUM (extend existing module)

**Estimated Effort**: 1-2 weeks

##### Task 4: Create New Templates ✨ DESIGN COMPLETE

**Templates to Create**:

1. `concern-analysis-template.md` (comprehensive concern assessment)
2. `abstraction-recommendations-template.md` (refactoring guidance)
3. `concern-migration-plan-template.md` (detailed phased rollout)

**Complexity**: MEDIUM (template creation with clear structure)

**Estimated Effort**: 1 week

##### Task 5: Update Artifacts Generation ✨ DESIGN COMPLETE

**Changes to analyze-project.md Step 6**:

- If ANALYSIS_SCOPE = [A], generate existing artifacts (current behavior)
- If ANALYSIS_SCOPE = [B], generate concern-specific artifacts:
  - `concern-analysis.md` (instead of functional-spec.md)
  - `abstraction-recommendations.md` (new)
  - `concern-migration-plan.md` (instead of technical-spec.md)
  - `stage-prompts/` adapted for concern migration

**Complexity**: LOW (conditional artifact generation)

**Estimated Effort**: 1-2 days

##### Task 6: Integration Testing ⏳ FUTURE

- Test on real projects with different concern types
- Validate abstraction detection accuracy
- Validate migration strategy recommendations
- Ensure generated artifacts are actionable

**Complexity**: HIGH (requires diverse test cases)

**Estimated Effort**: 2-3 weeks

---

#### 9.3 Decision Algorithms

##### Algorithm 1: Abstraction Level Scoring

```python
def score_abstraction_level(concern_code):
    """
    Returns: "HIGH" | "MEDIUM" | "LOW"
    """
    score = 0

    # Check for single entry point (interface/class)
    if has_single_interface(concern_code):
        score += 40
    elif has_multiple_consistent_entry_points(concern_code):
        score += 20

    # Check for dependency injection
    if uses_dependency_injection(concern_code):
        score += 30
    elif has_factory_pattern(concern_code):
        score += 15

    # Check for clean boundaries
    if no_direct_implementation_imports(concern_code):
        score += 30
    elif limited_direct_imports(concern_code):
        score += 10

    # Classification
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"
```

##### Algorithm 2: Migration Strategy Selection

```python
def recommend_migration_strategy(abstraction_level, blast_radius, coupling_degree):
    """
    Returns: {
        strategy: str,
        phasing: List[Phase],
        risk: str,
        effort: str
    }
    """

    # Decision tree
    if abstraction_level == "HIGH" and coupling_degree == "LOOSE":
        return {
            "strategy": "STRANGLER_FIG",
            "phasing": generate_strangler_fig_phases(),
            "risk": "LOW",
            "effort": "2-4 weeks"
        }

    elif abstraction_level == "MEDIUM":
        return {
            "strategy": "ADAPTER_PATTERN",
            "phasing": generate_adapter_pattern_phases(),
            "risk": "MEDIUM",
            "effort": "4-8 weeks"
        }

    elif abstraction_level == "LOW" and blast_radius < 20:  # < 20% of codebase
        return {
            "strategy": "REFACTOR_FIRST",
            "phasing": generate_refactor_first_phases(),
            "risk": "MEDIUM",
            "effort": "6-12 weeks"
        }

    else:  # LOW abstraction + HIGH blast radius
        return {
            "strategy": "BIG_BANG_WITH_FEATURE_FLAGS",
            "phasing": generate_big_bang_phases(),
            "risk": "HIGH",
            "effort": "3-6 months"
        }
```

---

#### 9.4 Example User Scenarios

##### Scenario 1: Auth Migration (High Abstraction) ✅ IDEAL CASE

**User Input**:

```text
ANALYSIS_SCOPE: [B] Cross-Cutting Concern Migration
CONCERN_TYPE: [1] Authentication/Authorization
CURRENT_IMPLEMENTATION: Custom JWT with PassportJS
TARGET_IMPLEMENTATION: Migrate to Okta
```

**AI Analysis Result**:

```text
Detected Auth Implementation:
- Entry Point: src/auth/AuthService.ts (single interface)
- Pattern: Clean interface, dependency injection used
- Abstraction Level: HIGH
- Files Affected: 15 files import IAuthProvider interface
- Blast Radius: 8% of codebase
- Coupling: LOOSE (no direct dependencies on JWT implementation)

Recommendation:
- Strategy: STRANGLER_FIG
- Risk: LOW
- Effort: 2-3 weeks

Phasing:
- P1 (50%): Implement OktaAuthProvider with IAuthProvider interface (Week 1-2)
- P2 (30%): Canary rollout (10% → 50% → 100%) with feature flag (Week 3)
- P3 (15%): Remove legacy JWT code (Week 4)
- P4 (5%): Documentation and future-proofing

Rollback: Feature flag `USE_OKTA_AUTH` allows instant rollback
```

##### Scenario 2: Database Migration (Low Abstraction) ⚠️ COMPLEX CASE

**User Input**:

```text
ANALYSIS_SCOPE: [B] Cross-Cutting Concern Migration
CONCERN_TYPE: [2] Database/ORM Layer
CURRENT_IMPLEMENTATION: PostgreSQL with raw SQL queries
TARGET_IMPLEMENTATION: Migrate to MongoDB
```

**AI Analysis Result**:

```text
Detected Database Implementation:
- Entry Points: 47 files with direct SQL queries (no ORM, no repository pattern)
- Pattern: Raw SQL scattered throughout services and controllers
- Abstraction Level: LOW
- Files Affected: 47 files (68% of codebase)
- Blast Radius: 80% of codebase (includes tests)
- Coupling: TIGHT (direct SQL in business logic)

Recommendation:
- Strategy: REFACTOR_FIRST + STRANGLER_FIG
- Risk: HIGH
- Effort: 3-6 months

Missing Abstractions:
1. No IRepository interface
2. No data access layer
3. No domain models (anemic data classes)

Phasing:
- P1 (40%): Extract data access layer with IRepository interface (Month 1-2)
  - Create Repository pattern for each entity
  - Migrate services to use repositories
  - Add integration tests
- P2 (40%): Implement dual-write (Postgres + Mongo) (Month 3-4)
  - Implement MongoRepository for each entity
  - Add schema mapping layer
  - Sync data bidirectionally
- P3 (15%): Gradual read cutover (Month 5)
  - Route reads to Mongo with Postgres fallback
  - Monitor data consistency
  - Fix schema mismatches
- P4 (5%): Decommission Postgres (Month 6)
  - Remove Postgres repositories
  - Clean up migration code

Rollback: Dual-write allows rollback until P4 complete
Critical: Schema mapping required (Postgres relational → Mongo document)
```

##### Scenario 3: Adding Caching (Greenfield) ✨ NEW FEATURE

**User Input**:

```text
ANALYSIS_SCOPE: [B] Cross-Cutting Concern Migration
CONCERN_TYPE: [3] Caching Layer
CURRENT_IMPLEMENTATION: None (no caching detected)
TARGET_IMPLEMENTATION: Add Redis caching layer
```

**AI Analysis Result**:

```text
Detected Caching Implementation:
- Entry Points: None (no caching currently)
- Hot Paths Identified: 12 endpoints with direct DB queries on every request
  - getUserProfile() - 1.2s average (file:line)
  - getProductList() - 800ms average (file:line)
  - searchOrders() - 2.1s average (file:line)

Recommendation:
- Strategy: DECORATOR_PATTERN + GRADUAL_ROLLOUT
- Risk: LOW (additive change, no breaking changes)
- Effort: 2-4 weeks

Phasing:
- P1 (20%): Create caching abstraction (Week 1)
  - Define ICacheService interface
  - Implement RedisCacheService
  - Add cache configuration
- P2 (60%): Add @Cacheable decorator to hot paths (Week 2-3)
  - Start with getUserProfile (highest impact)
  - Add cache invalidation on updates
  - Monitor cache hit rates
- P3 (15%): Tune and expand (Week 4)
  - Adjust TTLs based on hit rate data
  - Add caching to more endpoints
  - Implement cache warming for critical data
- P4 (5%): Documentation and monitoring
  - Add cache metrics dashboard
  - Document caching strategy

Rollback: Feature flag `ENABLE_REDIS_CACHE` allows instant disable
No data migration needed (cache is ephemeral)
```

---

#### 9.5 Design Principles

**Principle 1: Concern Identification via Multiple Signals**

Use layered detection:

1. **Naming Patterns**: Files/classes with concern keywords (auth*, cache*, db*, queue*)
2. **Import Analysis**: Libraries used (jsonwebtoken, mongoose, redis, kafka-node)
3. **Decorator/Annotation Patterns**: @Authenticated, @Transactional, @Cacheable
4. **Configuration Files**: auth.config.js, database.yml, redis.conf
5. **Call Graph Analysis**: Which functions call the concern's functions?

**Principle 2: Abstraction Quality Assessment**

Three-level taxonomy:

- **HIGH Abstraction**:
  - Single interface/contract
  - Dependency injection used
  - No direct implementation imports
  - Easy to swap implementations

- **MEDIUM Abstraction**:
  - Multiple entry points but consistent
  - Some direct dependencies
  - Mixed abstraction levels
  - Requires adapter layer

- **LOW Abstraction**:
  - Scattered across codebase
  - Direct implementation dependencies
  - No interfaces or contracts
  - Requires refactoring before migration

**Principle 3: Risk-Based Strategy Selection**

Migration strategy based on abstraction + coupling + blast radius:

```
IF high_abstraction AND loose_coupling THEN
    strategy = STRANGLER_FIG (low risk, incremental)
ELSE IF medium_abstraction THEN
    strategy = ADAPTER_PATTERN (moderate risk, add abstraction layer first)
ELSE IF low_abstraction AND small_blast_radius (<20%) THEN
    strategy = REFACTOR_FIRST (moderate risk, worth refactoring)
ELSE
    strategy = BIG_BANG_WITH_FEATURE_FLAGS (high risk, extensive changes)
END IF
```

**Principle 4: Phased Rollout with Rollback Points**

Every migration strategy includes:

- **Dual-running phase**: Old and new implementations coexist
- **Feature flags**: Instant rollback capability
- **Canary rollout**: Gradual traffic shifting (10% → 50% → 100%)
- **Monitoring**: Metrics to detect regressions
- **Rollback triggers**: Automated rollback on error rate spike

**Principle 5: Future-Proofing via Abstraction**

Every concern migration should:

- Add missing abstractions (interfaces, contracts)
- Use dependency injection
- Make provider selection config-driven
- Document migration lessons learned
- Ensure next migration is easier

---

#### 9.6 Success Criteria

##### Functional Requirements

- ✅ User can select "Cross-Cutting Concern" scope
- ✅ User can specify concern type (8 common concerns)
- ✅ AI detects concern-specific code accurately (>90% precision)
- ✅ AI assesses abstraction level (HIGH/MEDIUM/LOW)
- ✅ AI calculates blast radius (files/LOC affected)
- ✅ AI recommends migration strategy with rationale
- ✅ AI identifies missing abstractions with evidence
- ✅ AI generates actionable phased rollout plan

##### Artifact Quality

- ✅ `concern-analysis.md` contains real analysis (not template)
  - File:line references for all findings
  - Evidence-based abstraction assessment
  - Accurate blast radius calculation

- ✅ `abstraction-recommendations.md` provides actionable refactoring guidance
  - Clear gap identification with evidence
  - Recommended patterns with rationale
  - Phased refactoring roadmap

- ✅ `concern-migration-plan.md` includes detailed strategy
  - Risk assessment with mitigation
  - Phased rollout (50/30/15/5 value delivery)
  - Rollback procedures
  - Testing strategy

##### Integration

- ✅ Seamless integration with existing analyze-project workflow
- ✅ Backward compatible (full app analysis still works)
- ✅ Generated artifacts feed into Toolkit workflow
- ✅ Corporate guidelines checking for concern-specific code

---

#### 9.7 Implementation Plan (Phased Approach)

##### Week 1-2: Foundation & Prompt Enhancement ⏳ NEXT

- [ ] Update `templates/commands/analyze-project.md` with scope selection
- [ ] Add concern type question with 8 common concerns
- [ ] Add current/target implementation inputs
- [ ] Modify deep analysis step for concern filtering
- [ ] Test prompt flow with dummy responses

**Deliverable**: Updated analyze-project.md with concern-specific workflow

##### Week 3-5: Core Module Development ⏳ FUTURE

- [ ] Create `concern_analyzer.py` module
- [ ] Implement abstraction level scoring algorithm
- [ ] Implement blast radius calculation
- [ ] Implement coupling degree assessment
- [ ] Implement migration strategy recommendation engine
- [ ] Add unit tests for all algorithms

**Deliverable**: concern_analyzer.py with 85%+ test coverage

##### Week 6-7: Scanner Extension ⏳ FUTURE

- [ ] Extend `scanner.py` with concern_filter parameter
- [ ] Implement heuristics for 8 concern types
- [ ] Build concern-specific dependency graph
- [ ] Add unit tests for filtering logic

**Deliverable**: Extended scanner.py with concern detection

##### Week 8: Template Creation ⏳ FUTURE

- [ ] Create `concern-analysis-template.md`
- [ ] Create `abstraction-recommendations-template.md`
- [ ] Create `concern-migration-plan-template.md`
- [ ] Add examples and clear structure to all templates

**Deliverable**: 3 new templates with comprehensive structure

##### Week 9-10: Integration & Testing ⏳ FUTURE

- [ ] Update artifact generation logic (analyze-project.md Step 6)
- [ ] Test on 5 real projects with different concerns
  - [ ] Auth migration (high abstraction)
  - [ ] Database migration (low abstraction)
  - [ ] Adding caching (greenfield)
  - [ ] Message bus migration (medium abstraction)
  - [ ] Logging migration (various)
- [ ] Validate analysis accuracy
- [ ] Collect user feedback

**Deliverable**: Fully integrated concern analysis feature

##### Week 11: Documentation ⏳ FUTURE

- [ ] Update `docs/reverse-engineering.md` with concern analysis section
- [ ] Add examples for each concern type
- [ ] Create video walkthrough (optional)
- [ ] Update README.md with new capability

**Deliverable**: Complete documentation

---

#### 9.8 Quick Wins (Can Start Immediately)

**Week 1**:

- [ ] Add "ANALYSIS_SCOPE" question to analyze-project.md (2 hours)
- [ ] Add "CONCERN_TYPE" follow-up question (2 hours)
- [ ] Draft concern-analysis-template.md structure (4 hours)

**Impact**: Users can start providing concern-specific inputs (manual analysis still required)

---

#### 9.9 Dependencies & Risks

**Dependencies**:

- Phase 8 completion (✅ DONE - Interactive AI workflow)
- Phase 8.1 completion (✅ DONE - Conditional questions)
- Python 3.10+ (✅ EXISTING)
- Scanner.py module (✅ EXISTING)

**Risks**:

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Concern detection accuracy <90% | Medium | High | Add manual override, improve heuristics |
| Abstraction scoring algorithm inaccurate | Medium | High | Test on diverse codebases, tune weights |
| Migration strategy recommendations incorrect | Low | High | Include confidence score, show rationale |
| Complexity overwhelms users | Low | Medium | Provide clear examples, step-by-step guidance |

---

#### 9.10 Future Enhancements (Post-v1.0)

**Advanced Features**:

- [ ] Machine learning for concern detection (train on labeled data)
- [ ] Automated refactoring suggestions (generate code for missing abstractions)
- [ ] Cost estimation (cloud costs for new providers)
- [ ] Performance impact prediction (before/after benchmarks)
- [ ] Security analysis (comparative security assessment)
- [ ] Compliance checking (GDPR, SOX, HIPAA impact)

**Additional Concern Types**:

- [ ] Error handling/logging migration
- [ ] Configuration management (hardcoded → env vars)
- [ ] Secret management (code → vault)
- [ ] API versioning strategy
- [ ] Rate limiting/throttling
- [ ] Circuit breaker pattern

---

**Status**: 📋 DESIGN PHASE COMPLETE - Ready for Implementation

**Next Steps**:

1. Review design with stakeholders
2. Prioritize implementation tasks
3. Start with Week 1-2 quick wins
4. Iterate based on user feedback

---

### Phase 6 - Production Readiness (v1.0.0-alpha → v1.0.0)

**Goal**: Move from EXPERIMENTAL to PRODUCTION-READY status

**Current Blockers**:

- ❌ No unit tests (0% coverage)
- ❌ Not tested on real-world projects (0 validations)
- ❌ AI-guided workflow requires manual intervention
- ❌ No beta testing or user feedback
- ❌ No security audit completed

**Timeline**: 4-6 months (16-23 weeks) with 1-2 FTE developers

#### 6.1 Testing & Validation (4-6 weeks) - HIGH PRIORITY

**Unit Tests**:

- [ ] Create `tests/` directory structure
- [ ] Write unit tests for all Python modules:
  - [ ] `test_scanner.py` - Tech stack detection, metrics
  - [ ] `test_dependency_analyzer.py` - npm/pip parsing
  - [ ] `test_scoring_engine.py` - Feasibility algorithms
  - [ ] `test_report_generator.py` - Report generation
  - [ ] `test_security.py` - Path validation edge cases
  - [ ] `test_config.py` - Configuration validation
- [ ] Add pytest configuration (`pytest.ini`, `pyproject.toml`)
- [ ] Add coverage reporting (`pytest-cov`)
- [ ] Achieve 85%+ code coverage
- [ ] Add CI/CD workflow for automated testing

**Integration Tests**:

- [ ] Test against 10+ real-world projects:
  - [ ] 3x Node.js projects (React, Vue, Express)
  - [ ] 2x Python projects (Django, Flask)
  - [ ] 2x Java projects (Spring Boot)
  - [ ] 2x .NET projects (ASP.NET Core)
  - [ ] 1x Go project
  - [ ] 1x Rust project
- [ ] Validate analysis accuracy vs manual audits (target: 95%+)
- [ ] Document edge cases and failure modes
- [ ] Add regression tests for discovered issues

**Performance Testing**:

- [ ] Test varying project sizes:
  - [ ] Small (< 10K LOC)
  - [ ] Medium (10K-100K LOC)
  - [ ] Large (100K-500K LOC)
  - [ ] Very Large (500K+ LOC)
- [ ] Measure and document:
  - [ ] Analysis time vs project size
  - [ ] Memory usage
  - [ ] CPU utilization
- [ ] Fix performance bottlenecks
- [ ] Add timeout handling for very large projects
- [ ] Target: < 30 minutes for 500K LOC, < 2GB RAM

**Error Handling**:

- [ ] Test error scenarios:
  - [ ] Missing/corrupted package.json
  - [ ] Inaccessible files/directories
  - [ ] Mixed language projects
  - [ ] Monorepos
  - [ ] Binary files in codebase
- [ ] Improve error messages with actionable guidance
- [ ] Add graceful degradation for all failure modes
- [ ] Log errors with context for debugging

#### 6.2 Automation Improvements (3-4 weeks) - HIGH PRIORITY

**Reduce AI Manual Intervention**:

- [ ] Implement full automated report generation
- [ ] Auto-populate all template sections from analysis data
- [ ] Add CLI mode for non-interactive execution:

  ```bash
  python -m analyzer.main --project /path --depth STANDARD --output json
  ```

- [ ] Implement automated decision-making:
  - [ ] Auto-recommend inline vs greenfield based on scores
  - [ ] Auto-prioritize issues by severity
  - [ ] Auto-generate upgrade roadmap
- [ ] Target: Complete analysis without AI agent intervention

**External Tool Integration**:

- [ ] Add automatic tool detection and installation suggestions
- [ ] Improve fallback analysis quality (< 10% difference)
- [ ] Add support for more package managers:
  - [ ] Cargo (Rust) - full support
  - [ ] Go modules - full support
  - [ ] Composer (PHP) - full support
  - [ ] Bundler (Ruby) - full support
  - [ ] NuGet (.NET) - upgrade from "unsupported"
  - [ ] Maven/Gradle (Java) - upgrade from "unsupported"
- [ ] Add CVE database integration (offline mode)

**Structured Output Formats**:

- [x] JSON output format - Already exists
- [ ] YAML output format
- [ ] HTML report generation
- [ ] PDF export (optional)
- [ ] CSV for metrics

#### 6.3 User Validation (6-8 weeks) - MEDIUM PRIORITY

**Beta Testing Program**:

- [ ] Recruit 20+ beta testers:
  - [ ] Enterprise developers
  - [ ] Open source maintainers
  - [ ] Consultants/agencies
  - [ ] Individual developers
- [ ] Provide testing guidelines and feedback forms
- [ ] Collect structured feedback:
  - [ ] Analysis accuracy
  - [ ] Report usefulness
  - [ ] Time savings
  - [ ] Missing features
  - [ ] Bugs/issues
- [ ] Iterate based on feedback (minimum 2 cycles)
- [ ] Target: 80%+ satisfaction, < 5 critical bugs

**Case Studies**:

- [ ] Create 5+ detailed case studies:
  - [ ] Legacy Node.js app modernization
  - [ ] Java monolith assessment
  - [ ] Python Django upgrade
  - [ ] .NET framework → .NET 8 migration
  - [ ] React 16 → React 18 upgrade
- [ ] Document before/after metrics
- [ ] Create video walkthroughs (optional)
- [ ] Publish case studies with real data

#### 6.4 Production Hardening (2-3 weeks) - MEDIUM PRIORITY

**Security Audit**:

- [ ] Security review of path validation logic
- [ ] Test against malicious inputs:
  - [ ] Path traversal attacks
  - [ ] Symlink attacks
  - [ ] Command injection via subprocess
  - [ ] Resource exhaustion (DoS)
- [ ] Add rate limiting for subprocess calls
- [ ] Implement sandboxing for untrusted projects
- [ ] Add security scanning to CI/CD (Bandit, Safety)
- [ ] Target: Pass audit with 0 high/critical findings

**Dependency Management**:

- [ ] Create `requirements.txt` with pinned versions
- [ ] Create `requirements-dev.txt` for dev tools
- [ ] Test with minimum supported Python versions
- [ ] Document Python version compatibility (3.10+)
- [ ] Add dependency vulnerability scanning (Dependabot, Snyk)
- [ ] Add `setup.py` or `pyproject.toml` for distribution

**Cross-Platform Testing**:

- [ ] Test on Linux (Ubuntu, Debian, Fedora, Arch)
- [ ] Test on macOS (Intel + Apple Silicon)
- [ ] Test on Windows (10, 11)
- [ ] Test on Python versions (3.10, 3.11, 3.12)
- [ ] Fix platform-specific issues
- [ ] Document compatibility matrix

#### 6.5 Documentation & Support (2 weeks) - MEDIUM PRIORITY

**Documentation**:

- [ ] API documentation for Python modules (Sphinx)
- [ ] Developer guide for contributors
- [ ] Detailed troubleshooting guide
- [ ] FAQ based on beta testing feedback
- [ ] Architecture diagrams (system design, data flow)
- [ ] Performance tuning guide
- [ ] Migration guide (alpha → v1.0)

**Support Infrastructure**:

- [ ] Create GitHub issue templates:
  - [ ] Bug report
  - [ ] Feature request
  - [ ] Analysis accuracy issue
- [ ] Set up GitHub Discussions for Q&A
- [ ] Update contributing guidelines
- [ ] Add code of conduct
- [ ] Set up automated issue triage

#### 6.6 Release Engineering (1 week) - LOW PRIORITY

**Version Management**:

- [ ] Update version: v1.0.0-alpha → v1.0.0-beta1 (after 6.1)
- [ ] Update version: v1.0.0-beta1 → v1.0.0-rc1 (after 6.2-6.3)
- [ ] Update version: v1.0.0-rc1 → v1.0.0 (after 6.4-6.5)
- [ ] Update all documentation references
- [ ] Create release notes for each version
- [ ] Tag releases in Git
- [ ] Publish to PyPI (optional)
- [ ] Update README badges

**Success Criteria for v1.0.0**:

- ✅ 85%+ unit test coverage
- ✅ 95%+ accuracy on 10+ real projects
- ✅ Full automation (no AI intervention)
- ✅ 80%+ beta tester satisfaction
- ✅ 5+ published case studies
- ✅ Pass security audit
- ✅ Cross-platform compatibility verified
- ✅ Complete documentation

---

### Quick Wins (Can Start Immediately)

**Week 1-2**:

- [ ] Create `tests/` directory + basic test structure
- [ ] Add pytest + pytest-cov to project
- [ ] Create `requirements.txt` with pinned dependencies
- [ ] Set up GitHub Actions for CI/CD
- [ ] Test on 3 diverse real projects

**Week 3-4**:

- [ ] Write unit tests for scanner.py, scoring_engine.py
- [ ] Improve error messages with examples
- [ ] Add CLI mode for non-interactive execution
- [ ] Create troubleshooting guide
- [ ] Add security scanning (Bandit)

**Impact**: These 10 items enable **v1.0.0-beta1** release

---

## 🐛 Known Limitations

### By Design

- **Jira number is optional:** Can be made required via env var (future)
- **AGENTS.md enforcement is guidance-only:** Technical enforcement not feasible with current architecture
- **Interactive mode detection fragile:** Relies on literal `$ARGUMENTS` string matching
- **Branch numbering race condition:** Possible if multiple users create branches simultaneously

### Technical Constraints

- **No real-time validation:** Can't validate input until agent processes it
- **IDE-dependent behavior:** Some IDEs may not support interactive prompts well
- **Git fetch required:** Branch detection needs network access to check remote branches

---

## 📝 Maintenance

### Review Schedule

- **Monthly:** Review this document and prioritize items
- **Per sprint:** Pick 1-2 high priority items to implement
- **As needed:** Add new items as they're discovered

### Adding New Items

When adding improvements:

1. Choose priority level (🔴 High / 🟡 Medium / 🟢 Low)
2. Add checkbox with clear description
3. Include why it's needed and impact if not done
4. Link to related issues/PRs if applicable

### Completing Items

When completing improvements:

1. Mark checkbox as complete: `- [x]`
2. Add completion date and PR link
3. Move to "Completed" section at bottom (optional)
4. Update related documentation

---

## ✅ Completed Improvements

Track completed items here for reference.

### 2025-01-15

- [x] Add Jira number validation (regex format check) - PR #X
- [x] Fix branch detection regex to be more precise - PR #X
- [x] Clarify interactive input formats with templates - PR #X
- [x] Fix all markdownlint errors (multiple PRs) - PR #X
- [x] Create centralized improvements document - PR #X
- [x] Fix interactive mode detection in prompts (plan, implement, tasks, analyze) - PR #X
- [x] Implement Corporate Guidelines Phase 1 (Foundation) - PR #X
  - Created 7 guideline template files
  - Integrated guidelines into plan/implement/analyze/tasks prompts
  - Added tech stack auto-detection
  - Implemented multi-stack support
  - Added non-compliance handling
  - Updated AGENTS.md with guidelines documentation
- [x] Implement Corporate Guidelines Phase 2 (Configurable Branch Naming) - PR #18 (commit 98195d8)
  - Created `branch-config.json` schema
  - Refactored `create-new-feature.sh` to read from config file
  - Refactored `create-new-feature.ps1` to read from config file
  - Made Jira format configurable with regex patterns
  - Made Jira optional for teams without ticket systems
  - Maintained backward compatibility with defaults
  - Added documentation for branch configuration
- [x] Implement Corporate Guidelines Phase 3 (Multi-Stack Coordination) - PR #19 (commit 8f51529)
  - Implemented guideline precedence rules for multi-stack projects
  - Created `stack-mapping.json` for file-to-stack mapping
  - Added contextual guideline application logic
  - Optimized token usage with selective loading
  - Updated templates for multi-stack detection
  - Added examples for common combinations (React+Java, etc.)
- [x] Implement Corporate Guidelines Phase 4 (Advanced Features) - PR #21 (commit 13fd910)
  - Enhanced analysis capabilities
  - Added comprehensive testing suite for critical paths
  - Implemented advanced guideline features
  - Completed full corporate customization system
- [x] Implement Reverse Engineering Phase 1 (Core Implementation) - (commits f0eff30, 9f5629a)
  - Created scoring_engine.py for feasibility scoring (inline/greenfield) - 423 lines
  - Created dependency_analyzer.py for npm/pip security analysis - 524 lines
  - Created scanner.py for tech stack detection and metrics - 661 lines
  - Created report_generator.py for markdown report generation - ~800 lines
  - Created security.py for path validation - 118 lines
  - Created config.py for configuration management - 99 lines
  - Created analyze-project.sh bash orchestration script
  - Created analyze-project-setup.sh for cross-platform setup
  - Created analyze-project-setup.ps1 for PowerShell support
  - Full end-to-end analysis workflow operational
  - Total implementation: ~4,564 lines of Python + orchestration scripts
- [x] Implement Reverse Engineering Phase 2 (Language Analyzers) - (commit c414e65)
  - Created languages/javascript.py for Node.js/JavaScript analysis - ~661 lines
  - Created languages/python.py for Python-specific analysis - ~524 lines
  - Created languages/java.py for Java/Maven/Gradle analysis - ~423 lines
  - Created languages/dotnet.py for .NET/NuGet analysis - ~400 lines
  - 4 core language analyzers complete (Ruby/PHP deferred to Phase 6)
  - Framework detection, build tool detection, version detection
  - Graceful degradation when package managers unavailable
- [x] Implement Reverse Engineering Phase 3 (Checkpointing) - (commit verified 2025-11-08)
  - Created checkpoint.py for incremental analysis
  - Resume capability for interrupted analysis
  - Progress tracking and ETA estimation
  - Streaming report generation
  - Support for 500K+ LOC projects
- [x] Implement Reverse Engineering Phase 4 (CI/CD & Advanced Features) - (commit verified 2025-11-08)
  - Created GitHub Actions workflow template
  - Created GitLab CI configuration template
  - Created Jenkins pipeline template
  - Implemented customizable scoring weights (config.py)
  - JSON output format support
  - Complete documentation in templates
- [x] Deep analysis and documentation accuracy update - (commit c18c770, 2025-11-08)
  - Analyzed complete implementation (~4,564 LOC Python)
  - Updated reverse-engineering.md with accurate status
  - Clarified EXPERIMENTAL status with transparent reasons
  - Added comprehensive parameter documentation to README
  - Fixed Mermaid diagram rendering errors

---

## 📚 Historical Records

### Corporate Guidelines Implementation (2025-01-06 to 2025-11-06)

**Original Planning Document**: `GUIDELINES-IMPLEMENTATION-PLAN.md` (archived - content preserved below)

**Purpose**: Enable corporate customization of Spec Kit through configurable guidelines for tech stack standards, branch naming conventions, and multi-stack project support.

**Implementation Approach**: 4-phase rollout with clear deliverables and success criteria at each phase.

**Final Status**: ✅ **FULLY IMPLEMENTED** - All 4 phases completed successfully.

**Key Deliverables**:

1. `.guidelines/` directory with comprehensive templates (ReactJS, Java, .NET, Node.js, Python)
2. `branch-config.json` for configurable branch naming patterns
3. `stack-mapping.json` for multi-stack project coordination
4. Integration into all command templates (plan, implement, analyze, tasks)
5. Tech stack auto-detection and contextual guideline application
6. Priority system: Constitution > Corporate Guidelines > Spec Kit Defaults

**Results**:

- Teams can now customize Spec Kit to match corporate standards
- Supports corporate package registries (Artifactory, Nexus)
- Configurable branch naming without code changes
- Multi-stack projects (React+Java, etc.) properly supported
- Backward compatible - works with existing projects

**Lessons Learned**:

- Phased approach worked well for managing complexity
- Template-based guidelines provided good flexibility
- JSON configuration files easier than hardcoded scripts
- Token usage optimization critical for multi-stack support
- Clear priority hierarchy (Constitution > Guidelines > Defaults) prevented conflicts

**Reference PRs**:

- Phase 1: Foundation - TBD
- Phase 2: Branch Configuration - PR #18 (commit 98195d8)
- Phase 3: Multi-Stack Coordination - PR #19 (commit 8f51529)
- Phase 4: Advanced Features - PR #21 (commit 13fd910)

**Implementation Plan Archive**: For detailed phase breakdown, technical architecture, and original planning rationale, see Git history: `GUIDELINES-IMPLEMENTATION-PLAN.md` (removed 2025-11-07 after completion).

---

## 🤝 Contributing

To propose a new improvement:

1. Add it to the appropriate priority section above
2. Create a GitHub issue for discussion (for major changes)
3. Submit PR with implementation
4. Update this document when merged

**Remember:** Never add TODOs directly in prompt files!
