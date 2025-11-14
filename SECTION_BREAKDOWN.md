# Analyze-Project.md - Section Breakdown for Chained Prompts

**File**: `/home/user/spec-kit-smart/templates/commands/analyze-project.md`
**Total Lines**: 2484
**Version**: v1.2.0-alpha

---

## 1. USER INPUT & SCOPE DEFINITION

**Lines**: 60-162 (103 lines)

### Key Content Summary

This section establishes the interactive entry point for the analysis command. It handles two scenarios:
- **Empty arguments**: Prompts user to provide `PROJECT_PATH`
- **Provided arguments**: Parses the path and proceeds with analysis

After obtaining PROJECT_PATH, the section presents two analysis scope options:
- **[A] Full Application Modernization** - Complete app analysis with specs generation
- **[B] Cross-Cutting Concern Migration** - Scoped analysis of specific technical areas

If user selects [B], follow-up questions gather:
- `CONCERN_TYPE` (1-9 options: Auth, Database, Caching, Message Bus, Logging, API Gateway, File Storage, Deployment, Other)
- `CURRENT_IMPLEMENTATION` - What's in use now
- `TARGET_IMPLEMENTATION` - What to migrate to

### Critical Instructions & Patterns

```text
VALIDATION PATTERNS:
- User must choose [A] or [B] - invalid selections are rejected with re-prompt
- If [B]: Ask 3 follow-up questions immediately (CONCERN_TYPE, CURRENT_IMPL, TARGET_IMPL)
- STORE all responses for later use in Steps 4.B, 5, 6

SCOPE DECISION TREE:
Choice [A] → Proceed to Modernization Preferences (Step 3)
Choice [B] → Capture concern details → Skip to Step 4.B after 4.A complete
```text

### Content Extraction for Prompt Chaining

- Interactive dialogue templates (exact prompts to display)
- Validation rules for user input
- Storage requirements for captured data
- Conditional branching logic based on scope selection

---

## 2. ESTIMATION & WORKFLOW

**Lines**: 235-550 (316 lines)

### Key Content Summary

This section outlines the complete workflow structure with conditional logic for:

**Step 1 - Setup & OS Detection** (Lines 245-277)
- Script invocation for bash/PowerShell
- OS auto-detection with config file override
- Arguments parsing (PROJECT_PATH)
- Output: file-manifest.json location

**Step 2 - Tech Stack Detection** (Lines 279-298)
- Detection heuristics for 5 major stacks (ReactJS, Java, .NET, Node.js, Python)
- Display detected stack to user
- Extract metadata: language, framework, database, package manager, build tool

**Step 3 - Modernization Preferences** (Lines 300-550)
- **Conditional**: Only for [A] Full Application
- **10 Progressive Questions** (some conditional based on earlier answers):
  1. Target Language/Framework
  2. Target Database
  3. Message Bus/Queue (conditional: only ask if not detected)
  4. Package Manager
  5. Deployment Target (critical - controls Q6 & Q7)
  6. Infrastructure as Code (conditional: skip if Q5=[A])
  7. Containerization Strategy (conditional: skip if Q5=[A])
  8. Observability Stack (conditional: only ask if not detected)
  9. Security & Authentication
  10. Testing Strategy

**Conditional Logic Patterns**:

```text
Q3 (Message Bus): Skip if HAS_MESSAGE_BUS = false
Q6 (IaC): Skip if Q5 answer = [A] (Dedicated server)
Q7 (Containers): Skip if Q5 answer = [A] (Dedicated server)
Q8 (Observability): Skip if HAS_OBSERVABILITY = false
```text

**Detection Flags**:
- `HAS_MESSAGE_BUS` - auto-detect Kafka, RabbitMQ, Azure SB, AWS SQS, Redis PubSub
- `HAS_OBSERVABILITY` - auto-detect logging frameworks, monitoring configs
- `IS_TRADITIONAL_DEPLOYMENT` - derived from Q5 answer

### Critical Instructions & Patterns

```text
MANDATORY: Store all 10 responses for later use in artifact generation
CONDITIONAL BRANCHING: Skip Questions 6-7 if user selects "Dedicated server"
VALIDATION: All questions require valid answer before proceeding
DETECTION: Pre-calculate HAS_MESSAGE_BUS and HAS_OBSERVABILITY before asking
```text

---

## 3. FILE ANALYSIS METHODOLOGY

**Lines**: 552-904 (353 lines)

### Key Content Summary

This is the concrete analysis approach for Phase 0 through Phase 2 generation. It follows a 4-step scanning methodology:

**Phase 0: Upfront Estimation & User Warning** (Lines 566-664)

Step 0.1: Count files by category from manifest

```text
- Controllers/Routes
- Services/Business Logic
- Models/Data
- Repositories/DAOs
- Configurations
- Security/Auth
- Middleware
- Utilities/Helpers
- Tests
```text

Step 0.2: Calculate chunks needed

```javascript
Total important files = Controllers + Services + Models + Repositories + Configs + Security + Middleware + Utilities

Chunk estimation:
- Phase 1 (Discovery): 1 chunk
- Phase 2 (Codebase Analysis): 1 chunk per 50 files or 1 per category (max)
- Phases 3-9: 1 chunk each
- Total chunks = 2 + ceil(important_files / 50) + 7
```text

Step 0.3: Display scope estimation with time range
- Small project (<50 files): 5-10 min, 3-5 chunks
- Medium project (50-150 files): 15-25 min, 6-10 chunks
- Large project (150-300 files): 30-50 min, 11-18 chunks
- Very large (300-500): 60-90 min, 19-25 chunks
- Extremely large (>500): 90+ min, 25+ chunks

Step 0.4: Confirmation prompt for >20 chunks projects
- [A] Full analysis
- [B] Narrow scope (specify categories)
- [C] Sampling mode (20% random sample)
- [D] Cancel

**Phase 1: Concrete Scanning Process** (Lines 668-887)

Step 1.1: Categorize ALL files from manifest
- File pattern matching rules for each category
- Examples provided for each category

Step 1.2: Read & Extract from EVERY file
**Critical**: Do NOT sample - read every file in each category

For each category, extract specific details:
- **Controllers**: endpoints (HTTP method, path), DTOs, auth requirements, error handling
- **Services**: workflows, external integrations, data transforms, business rules, transaction boundaries
- **Models**: relationships, constraints, validation rules, computed properties, DB mappings
- **Repositories**: CRUD patterns, query complexity, SQL vs ORM, caching, transactions
- **Configurations**: connection strings (anonymized), API keys, environment configs, feature flags, timeouts
- **Security/Auth**: authentication mechanisms, authorization patterns, password hashing, token settings, CORS, rate limits
- **Middleware**: request processing, response transforms, logging, error handling, performance optimizations
- **Utilities**: shared functionality, data transforms, validation, date/time, string manipulation, crypto
- **Tests**: test coverage areas, frameworks, mocking strategies, integration/E2E patterns
- **Infrastructure**: deployment targets, environment configs, CI/CD, IaC patterns, scaling

Step 1.3: Categorize features by criticality

```text
CRITICAL - Must preserve exactly
STANDARD - Preserve but can modernize
LEGACY QUIRKS - Consider modernizing
```text

Step 1.4: Expected output volume (quality check)
- ✓ 50-200 feature descriptions with file:line references
- ✓ 20-50 technical debt items categorized by severity
- ✓ 10-30 security findings with risk scores
- ✓ Architecture patterns identified
- ✓ All configuration values documented
- ✓ All external dependencies mapped
- ✓ Test coverage analysis complete

**Examples of Good vs Bad Extraction** (Lines 857-886)

```text
❌ BAD: "User management feature"
✅ GOOD: "User registration with email verification (src/auth/RegisterController.ts:45-89)
         - POST /api/auth/register
         - Validates email format (RFC 5322), password strength
         - Sends verification email via SendGridService
         - Stores user with bcrypt-hashed password (cost factor: 10)
         - Returns JWT token (24h expiration)"
```text

### Critical Instructions & Patterns

```text
MANDATORY EXTRACTION PATTERNS:
1. File:line references for EVERY finding
2. Full depth analysis (not sampling - read EVERY file)
3. Concrete evidence (not abstract descriptions)
4. Three criticality levels (CRITICAL/STANDARD/LEGACY)
5. 50-200 feature descriptions minimum

QUALITY GATES:
- If output volume < expected → Return to Step 1.2 for more details
- All findings must be specific, evidenced, and actionable
- All files must be read (no sampling allowed)
```text

---

## 4. ANALYSIS REPORT GENERATION (COMPLETION-BASED CHUNKING)

**Lines**: 890-1343 (454 lines)

### Key Content Summary

Generates comprehensive 9-phase Project Analysis Report in 9 logical chunks (completion-based, not size-based).

**Chunk Strategy: Completion-Based** (NOT size-based)
- Generate complete logical phases/sections in each chunk
- Each chunk ends with a distinct completion point
- Progress display required after each chunk
- Checkpoint markers created after each chunk

**Chunk 1: Phase 1 - Project Discovery** (Completion: All config files analyzed)

```text
- Section 1.1: Technology Stack (from file analysis)
- Section 1.2: System Architecture (inferred from structure)
- Section 1.3: Project Statistics (LOC, file counts)
- Section 1.4: Configuration Analysis (all config files)
- Section 1.5: Build & Deployment (build tools, scripts)

Completion Criteria:
- ✓ All configuration files analyzed
- ✓ Tech stack fully identified
- ✓ Architecture pattern documented with evidence
- ✓ Project statistics calculated
- ✓ Build/deployment process understood
- ✓ NO placeholders

Progress Display:
✓ Chunk 1/[TOTAL] complete: Phase 1 (Project Discovery)
  - Analyzed: [COUNT] configuration files
  - Identified: [TECH STACK SUMMARY]
  - Lines generated: [COUNT]
```text

**Chunk 2: Phase 2.1 - Controllers & API Endpoints**

```text
Complete Section 2.1: Controllers Analysis
- EVERY controller file analyzed
- EVERY API endpoint documented (method, path, purpose)
- File:line references for all findings
- Auth requirements clear for each endpoint
- NO placeholders
```text

**Chunk 3: Phase 2.2 - Services & Business Logic**

```text
Complete Section 2.2: Services Analysis
- EVERY service file analyzed
- Business workflows documented with evidence
- External integrations identified
- Transaction patterns clear
- NO placeholders
```text

**Chunk 4: Phase 2.3 - Data Layer**

```text
Complete Section 2.3: Data Models & Repositories
- EVERY model/entity file analyzed
- Relationships documented (with cardinality)
- Validation rules extracted
- Database operations categorized
- NO placeholders
```text

**Chunk 5: Phase 3 - Positive Findings**

```text
- Section 3.1: What's Working Well
- 10-30 positive findings with file:line references
- Evidence-based (not generic praise)
- Specific examples of good practices
- NO placeholders
```text

**Chunk 6: Phase 4 - Negative Findings / Technical Debt**

```text
- Section 4.1: Technical Debt (HIGH/MEDIUM/LOW severity)
- Section 4.2: Security Vulnerabilities (with CVE references)
- Section 4.3: Code Quality Issues (smells, duplication, complexity)
- Section 4.4: Architecture Issues (coupling, abstractions, monolithic)
- 20-50 technical debt items categorized
- 10-30 security findings with risk scores
- NO placeholders
```text

**Chunk 7: Phase 5 - Upgrade Path Analysis**

```text
- Section 5.1: Runtime/Framework Upgrades (Current → Latest LTS)
- Section 5.2: Dependency Upgrades (outdated packages, security patches)
- Section 5.3: Database Migration Paths (schema changes, data migration)
- All upgrade paths evaluated
- Breaking changes identified with mitigation
- Effort estimates provided (hours/days/weeks)
- Risk assessment for each path
- NO placeholders
```text

**Chunk 8: Phases 6-7 - Modernization & Feasibility**

```text
- Section 6: Modernization Recommendations
  - Quick wins (low effort, high value)
  - Strategic improvements
  - Long-term goals
- Section 7: Feasibility Scoring
  - Inline upgrade feasibility (formula shown)
  - Greenfield rewrite feasibility (formula shown)
  - Hybrid approach feasibility
- Recommendations prioritized by value/effort
- Feasibility scores calculated with transparent formulas
- NO placeholders
```text

**Chunk 9: Phases 8-9 - Decision Matrix & Final Recommendations**

```text
- Section 8: Decision Matrix
  - Comparison table: Time, Cost, Risk, Business Disruption
  - Scoring for each approach
- Section 9: Final Recommendations
  - Primary recommendation with confidence score (0-100%)
  - Immediate actions (next steps)
  - Short-term roadmap (0-6 months)
  - Long-term roadmap (6-18 months)
- Decision matrix complete with justified scores
- Primary recommendation stated with confidence
- Roadmaps provided with milestones
- NO placeholders
```text

### Phase 3: Checkpoint & Resume Mechanism (Lines 1213-1244)

After each chunk completion:

```bash
echo "{ \"chunk\": N, \"phase\": \"X.Y\", \"timestamp\": \"$(date -Iseconds)\" }" > .analysis/.checkpoints/chunk-N-complete.json
```text

**Resume Logic** (if interrupted):
1. Check `.analysis/.checkpoints/` for last completed checkpoint
2. Identify last completed chunk
3. Resume from next chunk
4. Display resumption message to user

### Phase 4: Verification Gate (Lines 1248-1343)

**HARD STOP before proceeding to Step 4.B or Step 6**

Verification Checklist:

```text
- [ ] File exists at expected path
- [ ] All 9 phase headers present (Phase 1-9)
- [ ] Quality checks:
      [ ] 50+ file:line references present
      [ ] Technical debt items have severity ratings (HIGH/MEDIUM/LOW)
      [ ] Security vulnerabilities documented with risk scores
      [ ] Feasibility scores calculated with formulas shown
      [ ] Primary recommendation stated with confidence score (0-100%)
      [ ] No placeholders (TODO, TBD, "will be analyzed")
      [ ] All tables properly formatted
      [ ] All code blocks have syntax highlighting
- [ ] Completeness:
      [ ] Total lines: 3,000+ (minimum)
      [ ] Feature descriptions: 50-200 with evidence
      [ ] Technical debt items: 20-50 categorized
      [ ] Security findings: 10-30 with risk scores
```text

**If ANY checkbox fails**:
- Identify incomplete sections
- Regenerate ONLY missing phases using checkpoint system
- Enhance quality issues in problematic sections
- Re-run verification

**Only after PASSING verification**: Proceed to Step 4.B (if [B]) or Step 5 (if [A])

### Critical Instructions & Patterns

```text
COMPLETION-BASED CHUNKING:
- Generate complete logical phases/sections
- Do NOT split based on line counts
- Each chunk must be independently verifiable
- Create checkpoint marker after each chunk
- Display mandatory progress update after each chunk

VERIFICATION GATE (HARD STOP):
- Cannot proceed to Step 4.B or Step 6 until ALL phases complete
- Failure → identify issues and regenerate incomplete sections
- Success → proceed with confidence

NO PLACEHOLDERS ALLOWED:
- Every finding must have file:line reference
- Every estimate must be calculated (not "TBD")
- Every severity must be justified
- No "coming soon" or "will be analyzed later"
```text

---

## 5. BRANCH LOGIC FOR CROSS-CUTTING CONCERN (Step 4.B)

**Lines**: 1347-1719 (373 lines)

### Key Content Summary

Only executed if ANALYSIS_SCOPE = [B]. Provides deep-dive analysis of a specific technical concern (e.g., auth migration, database swap) with 6 analysis steps.

**PREREQUISITE**: Step 4.A must be complete (analysis-report.md verified) before starting 4.B

**Step 4.B.1: Identify Concern-Specific Files**

File pattern detection heuristics by concern type:

```text
[1] AUTHENTICATION/AUTHORIZATION:
- Patterns: auth*, login*, session*, jwt*, passport*, oauth*, security*, *guard*, *policy*
- Imports: jsonwebtoken, passport, bcrypt, oauth, jose, spring-security, ASP.NET Identity
- Decorators: @authenticated, @require_auth, @authorize, @Secured, @PreAuthorize
- Configs: auth.config.*, security.yml, passport.config.*, appsettings.json
- DB: Users, Roles, Permissions tables

[2] DATABASE/ORM LAYER:
- Patterns: *repository*, *model*, *entity*, *dao*, db*, database*, *schema*, migrations/*
- Imports: sequelize, mongoose, typeorm, prisma, knex, hibernate, Entity Framework, SQLAlchemy
- Configs: database.yml, ormconfig.*, knexfile.*, application.properties, appsettings.json
- SQL: *.sql, migrations/*, schema/*, seeds/*

[3] CACHING LAYER:
- Patterns: *cache*, *redis*, *memcached*, *session*
- Imports: redis, ioredis, node-cache, memcached, spring-cache, IMemoryCache, django-redis
- Decorators: @Cacheable, @CacheEvict, @CachePut, [ResponseCache]
- Configs: redis.conf, cache.config.*, appsettings.json (cache section)

[4] MESSAGE BUS/QUEUE:
- Patterns: *queue*, *message*, *event*, *consumer*, *producer*, *publisher*, *subscriber*, *listener*
- Imports: kafkajs, amqplib, rabbitmq, bull, kue, azure-service-bus, aws-sdk, spring-amqp, MassTransit
- Configs: kafka.config.*, rabbitmq.config.*, application.yml (messaging section)

[5] LOGGING/OBSERVABILITY:
- Patterns: *logger*, *logging*, *log*, *monitor*, *telemetry*, *metrics*, *tracing*
- Imports: winston, pino, log4js, bunyan, opentelemetry, prometheus, log4j, slf4j, Serilog, elastic-apm
- Configs: log4j.properties, log4j2.xml, logback.xml, nlog.config, serilog.config.json
- APM agents: DataDog, New Relic, Application Insights

[6] API GATEWAY/ROUTING:
- Patterns: *router*, *route*, *gateway*, *proxy*, routes/*, middleware/*
- Imports: express.Router, spring-cloud-gateway, Ocelot, Kong
- Configs: routes.config.*, gateway.yml, nginx.conf, ocelot.json

[7] FILE STORAGE/CDN:
- Patterns: *storage*, *upload*, *file*, *asset*, *media*, *document*
- Imports: multer, formidable, aws-sdk (S3), @azure/storage-blob, @google-cloud/storage
- Configs: storage.config.*, aws.config.*, azure-storage.config.*, cdn.config.*

[8] DEPLOYMENT/INFRASTRUCTURE:
- Patterns: Dockerfile, docker-compose.yml, *.tf, *.bicep, charts/*, *.yaml (k8s/)
- CI/CD: .github/workflows/*, .gitlab-ci.yml, azure-pipelines.yml, Jenkinsfile
- Deployment scripts: deploy.sh, deploy.ps1, ansible playbooks, release.sh

[9] OTHER (User-Specified):
- Semantic understanding based on user description
- Pattern and import matching for custom concerns
```text

**Output Table Format**:

```markdown
| File Path | Type | Evidence | LOC | Criticality |
| ----------- | ------ | ---------- | ----- | ------------- |
| src/auth/AuthService.ts:15 | Core Implementation | Exports authenticate(), uses jsonwebtoken | 247 | CRITICAL |
...
**Total**: [COUNT] files, [COUNT] LOC (~X% of codebase)
```text

**Step 4.B.2: Assess Abstraction Level**

Scoring 0-10:

```text
HIGH (8-10): Interface/contract defines all operations, DI used, config externalized,
             no direct coupling, easy to swap (hours of work)

MEDIUM (4-7): Some interfaces exist, mix of DI and direct instantiation, some hardcoding,
              moderate coupling, swappable with refactoring (days/weeks)

LOW (0-3): No interfaces, direct instantiation everywhere, heavy hardcoding,
           tight coupling, very difficult to swap (months of refactoring)
```text

**Analysis Checklist**:
- [ ] Are there interface/contract definitions?
- [ ] Is dependency injection used?
- [ ] Are configuration values externalized?
- [ ] Can the implementation be swapped without changing consumers?
- [ ] Are there direct imports of implementation classes?

**Output Section**:

```markdown
### Abstraction Level Assessment

**Score**: [0-10] ([HIGH/MEDIUM/LOW])

**Evidence**:
- Interface definitions: [Yes/Partial/No] ([file:line references])
- Dependency injection: [Yes/Partial/No] ([file:line references])
- Configuration externalization: [Yes/Partial/No] ([file:line references])
- Direct coupling instances: [Count] ([file:line references])

**Assessment**: [Detailed explanation]

**Migration Impact**:
- HIGH: Can swap implementation directly (1-2 weeks)
- MEDIUM: Need interface extraction first (4-6 weeks total)
- LOW: Major refactoring required (2-4 months total)
```text

**Step 4.B.3: Calculate Blast Radius**

Metrics to calculate:

```text
1. Direct usage count: How many files directly import/use the concern?
2. Lines of code: Total LOC in concern files + consumer files
3. Percentage of codebase: (Concern LOC + Consumer LOC) / Total Project LOC * 100
4. Criticality distribution: CRITICAL vs STANDARD vs LOW priority files affected
5. Test coverage: Do tests exist? Will tests need major rewrites?
```text

**Output Section**:

```markdown
### Blast Radius Analysis

**Total Files Affected**: [COUNT]
- Core concern files: [COUNT] ([X] LOC)
- Direct consumers: [COUNT] ([X] LOC)
- Indirect consumers: [COUNT] ([X] LOC)

**Percentage of Codebase**: [X]%

**Criticality Breakdown**:
- CRITICAL: [COUNT] files ([list key files])
- STANDARD: [COUNT] files
- LOW: [COUNT] files

**Test Impact**:
- Tests exist: [YES/NO]
- Tests needing updates: [COUNT]
- Test rewrite estimate: [TIME]

**Key Consumers** (Top 10 by usage):
| File Path | Usage Count | Type | Impact |
| ----------- | ------------- | ------ | -------- |
| [file:line] | [COUNT] | [Controller/Service/etc] | [HIGH/MED/LOW] |
```text

**Step 4.B.4: Analyze Coupling Degree**

Scoring 0-10:

```text
LOOSE (8-10): Communication via interfaces only, no circular deps, clear module boundaries,
              minimal shared state, independent deployment possible

MODERATE (4-7): Some interface usage, some direct deps, few circular deps,
                blurred boundaries, some shared state, requires coordinated deployment

TIGHT (0-3): Extensive direct dependencies, circular deps present, no module boundaries,
             extensive shared state, cannot deploy independently
```text

**Output Section**:

```markdown
### Coupling Degree Analysis

**Coupling Score**: [0-10] ([LOOSE/MODERATE/TIGHT])

**Dependency Analysis**:
- Direct dependencies: [COUNT] ([file:line references])
- Circular dependencies: [None | List with file:line]

**Isolation Score**: [0-10, where 10 = fully isolated]
- Module boundaries: [Clear/Blurred]
- Shared state: [None/Some/Extensive]
- Bidirectional deps: [Yes/No]

**Evidence**:
- [Evidence 1 with file:line references]
- [Evidence 2 with file:line references]
```text

**Step 4.B.5: Recommend Migration Strategy**

Decision tree logic:

```text
IF high_abstraction AND loose_coupling:
   → STRANGLER_FIG (Recommended)
      Low risk, 2-4 weeks effort
      Implement new provider alongside old one
      Gradually switch consumers via feature flags

ELSE IF medium_abstraction:
   → ADAPTER_PATTERN (Recommended)
      Medium risk, 4-8 weeks effort
      Create adapter interface wrapping new implementation
      Refactor consumers to use adapter
      Swap adapter internals when confident

ELSE IF low_abstraction AND blast_radius < 20%:
   → REFACTOR_FIRST (Recommended)
      Medium risk, 6-12 weeks effort
      Phase 1: Extract interfaces, introduce DI (2-4 weeks)
      Phase 2: Implement new provider (2-3 weeks)
      Phase 3: Migrate consumers (2-5 weeks)

ELSE:
   → BIG_BANG_WITH_FEATURE_FLAGS (Recommended)
      High risk, 3-6 months effort
      Low abstraction + large blast radius = significant refactoring
      Use feature flags for gradual rollout
      Extensive testing required
```text

**Output Section**:

```markdown
### Migration Strategy Recommendation

**Recommended Approach**: [STRANGLER_FIG | ADAPTER_PATTERN | REFACTOR_FIRST | BIG_BANG_WITH_FEATURE_FLAGS]

**Rationale**:
- Abstraction level: [HIGH/MEDIUM/LOW] → [Implication]
- Blast radius: [X% of codebase] → [Implication]
- Coupling degree: [LOOSE/MODERATE/TIGHT] → [Implication]
- **Conclusion**: [Why this strategy is best fit]

**Effort Estimate**: [Time range]
**Risk Level**: [LOW | MEDIUM | HIGH]

**Phasing** (50/30/15/5 value delivery):

### Phase 1 (50% value) - [Timeline]
- [Key deliverable 1]
- [Key deliverable 2]
- **Value**: [Benefit to business]

### Phase 2 (30% value) - [Timeline]
### Phase 3 (15% value) - [Timeline]
### Phase 4 (5% value) - [Timeline]
```text

**Step 4.B.6: Abstraction Improvement Recommendations (if LOW/MEDIUM abstraction)**

Provide specific guidance on improving abstractions before migration:

```markdown
### Abstraction Improvement Recommendations

**Current State**: [Summary of low abstraction issues]

**Target State**: [Description of improved abstraction]

**Recommended Abstractions to Introduce**:

1. **Interface/Contract Definition**:
   - Create: `I[ConcernName]Service` interface
   - Location: `src/interfaces/` or `src/contracts/`
   - Methods: [List key methods]
   - **Example**: `IAuthService` with methods: authenticate(), validateToken(), refreshToken()

2. **Dependency Injection Setup**:
   - Framework: [Recommend DI framework for tech stack]
   - Pattern: Constructor injection
   - Registration: [Where to register services]

3. **Configuration Externalization**:
   - Move hardcoded values to config files
   - Environment-specific configs (dev/staging/prod)
   - **Example**: JWT secret, token expiration, provider endpoints

4. **Adapter/Wrapper Layer** (if needed):
   - Wrap current implementation in adapter
   - Future migrations just swap adapter internals
   - Consumers remain unchanged

**Refactoring Roadmap** (if user wants to improve abstractions first):
- Week 1-2: Extract interfaces, define contracts
- Week 3-4: Implement DI, refactor consumers
- Week 5-6: Externalize configuration
- Week 7+: Ready for migration to new implementation

**Future Migration Benefit**:
After refactoring, next migration will be [STRANGLER_FIG/ADAPTER_PATTERN] with [LOW/MEDIUM] risk.
```text

### Critical Instructions & Patterns

```text
PREREQUISITE: Step 4.A (analysis-report.md) must be COMPLETE before starting 4.B

REUSE FROM ANALYSIS-REPORT:
- Reference Section 1.1 "Technology Stack" for current implementation
- Reference Section 4.1 "Technical Debt" for concern-related issues
- Reference Section 4.2 "Vulnerable Dependencies" for security concerns
- Reference Section 3 "Positive Findings" for existing abstractions

PATTERN DETECTION:
- Use file pattern matching for each concern type
- Look for specific imports and decorators
- Analyze configuration files for settings
- Check database schema for tables/columns

SCORING METHODOLOGY:
- Abstraction: 0-10 scale with HIGH/MEDIUM/LOW categories
- Coupling: 0-10 scale with LOOSE/MODERATE/TIGHT categories
- Blast Radius: Percentage of codebase affected
- Migration Strategy: Decision tree based on three factors

EVIDENCE REQUIREMENT:
- ALL findings must include file:line references
- Specific counts (not estimates)
- Actionable recommendations tied to assessment
```text

---

## 6. REPORT GENERATION - analysis-report.md

**Lines**: 890-1343 (embedded in Section 3 above)

**See Section 3 for complete details** - this covers the Phase 2 chunk generation and completion-based workflow.

---

## 7. ARTIFACT GENERATION

**Lines**: 1849-2310 (462 lines)

### Key Content Summary

Generates output artifacts based on ANALYSIS_SCOPE. Two conditional paths:
- **Path A**: Full Application (ANALYSIS_SCOPE = [A])
- **Path B**: Cross-Cutting Concern (ANALYSIS_SCOPE = [B])

**PREREQUISITE CHECK** (Lines 1849-1861):
Before generating ANY artifact:
- ✓ analysis-report.md EXISTS
- ✓ analysis-report.md is COMPLETE (all 9 phases)

If analysis-report.md missing/incomplete → STOP, RETURN to Step 4.A, DO NOT proceed

---

### STEP 6.A: FULL APPLICATION ARTIFACTS (ANALYSIS_SCOPE = [A])

**REQUIRED ARTIFACTS**:

#### 1. **EXECUTIVE-SUMMARY.md** (Small - 1 chunk)

**Source**: Extract key findings from analysis-report.md

**Sections**:
1. Executive Summary (2-3 paragraphs)
2. Key Metrics (table)
3. Primary Recommendation (1 paragraph)
4. Next Steps (bullet list)

**Completion Criteria**:
- ✓ Extracts key findings from analysis-report.md (cite phases)
- ✓ Metrics match analysis-report.md values
- ✓ Recommendation aligns with Phase 9
- ✓ No placeholders

**Progress Display**:

```text
✓ EXECUTIVE-SUMMARY.md complete
  - Extracted from: analysis-report.md
  - Lines: [COUNT]
```text

#### 2. **functional-spec.md** (2,000-4,000 lines - 5 chunks)

**Source**: Extract features from analysis-report.md Phase 1-2

**Template**: `templates/analysis/functional-spec-template.md`

**Chunk 1: Introduction + Summary + Scope**
- Section 1: Introduction
- Section 2: Executive Summary
- Section 3: Scope
- Content: Project overview, high-level purpose, in/out of scope
- Completion: All 3 sections complete, no placeholders

```text
Progress: ✓ functional-spec.md Chunk 1/5 complete: Introduction + Summary + Scope
          - Lines: [COUNT]
```text

**Chunk 2: User Stories (Part 1) - CRITICAL Features**
- Section 4.1: User Stories - CRITICAL
- Content: All CRITICAL features from analysis-report.md Phase 2
- Every feature MUST have file:line reference
- Completion: All CRITICAL features documented with evidence

```text
Progress: ✓ functional-spec.md Chunk 2/5 complete: User Stories (CRITICAL)
          - Features: [COUNT]
          - Lines: [COUNT]
```text

**Chunk 3: User Stories (Part 2) - STANDARD Features + Business Rules**
- Section 4.2: User Stories - STANDARD
- Section 5: Business Rules
- Content: STANDARD features + validation rules
- Completion: All STANDARD features + rules documented

```text
Progress: ✓ functional-spec.md Chunk 3/5 complete: STANDARD Features + Rules
          - Features: [COUNT]
          - Lines: [COUNT]
```text

**Chunk 4: NFRs + Data Requirements**
- Section 6: Non-Functional Requirements
- Section 7: Data Requirements
- Content: Performance, security, scalability, data entities
- Completion: NFRs defined, data models documented

```text
Progress: ✓ functional-spec.md Chunk 4/5 complete: NFRs + Data
          - Lines: [COUNT]
```text

**Chunk 5: Acceptance Criteria + Assumptions + Constraints**
- Section 8: Acceptance Criteria
- Section 9: Assumptions
- Section 10: Constraints
- Content: Testing criteria, assumptions, limitations
- Completion: All sections complete, no placeholders

```text
Progress: ✅ functional-spec.md COMPLETE (5/5 chunks)
          - Total features: [COUNT]
          - Total lines: [COUNT]
```text

#### 3. **technical-spec.md** (2,000-3,000 lines - 5 chunks)

**Source**: analysis-report.md Phase 5-6 + user's modernization preferences (from 10 questions)

**Template**: `templates/analysis/technical-spec-template.md`

**Chunk 1: Architecture Overview + Legacy vs Target Comparison**
- Section 1: Introduction
- Section 2: Architecture Overview
- Section 3: Legacy vs Target Comparison
- Content: System architecture, comparison tables, Mermaid diagrams
- Completion: Architecture patterns documented, comparison complete

```text
Progress: ✓ technical-spec.md Chunk 1/5 complete: Architecture + Comparison
          - Diagrams: [COUNT]
          - Lines: [COUNT]
```text

**Chunk 2: Target Tech Stack + Data Architecture**
- Section 4: Target Tech Stack
- Section 5: Data Architecture
- Content: User's chosen stack (from Q1-Q10), database design, ORM
- Include user's answers from modernization preference questions
- Completion: All tech choices documented, data layer designed

```text
Progress: ✓ technical-spec.md Chunk 2/5 complete: Tech Stack + Data
          - Lines: [COUNT]
```text

**Chunk 3: API Design + Integration Points**
- Section 6: API Design
- Section 7: Integration Architecture
- Content: REST/GraphQL design, external APIs, message queues
- Completion: API contracts defined, integrations documented

```text
Progress: ✓ technical-spec.md Chunk 3/5 complete: API + Integrations
          - Endpoints: [COUNT]
          - Lines: [COUNT]
```text

**Chunk 4: Security + Authentication + Deployment**
- Section 8: Security
- Section 9: Deployment Strategy
- Content: User's chosen auth (Q9), deployment target (Q5), IaC (Q6), containers (Q7)
- Completion: Security measures defined, deployment plan complete

```text
Progress: ✓ technical-spec.md Chunk 4/5 complete: Security + Deployment
          - Lines: [COUNT]
```text

**Chunk 5: Testing Strategy + Observability + Migration Risks**
- Section 10: Testing Strategy
- Section 11: Observability Stack
- Section 12: Migration Risks
- Content: User's testing choice (Q10), observability stack (Q8), risk mitigation
- Completion: All sections complete, no placeholders

```text
Progress: ✅ technical-spec.md COMPLETE (5/5 chunks)
          - Total lines: [COUNT]
```text

#### 4. **stage-prompts/** (4 files - Generate individually)

**Source**: Templates from `templates/analysis/stage-prompt-templates/`

**Files to generate**:

**1. constitution-prompt.md**
- Principles for new system
- Extracted from analysis-report.md Phase 6 (Modernization Recommendations)
- Include: Core values, technical principles, what to preserve, what to change

**2. clarify-prompt.md**
- **CRITICAL**: Must include "When clarifying requirements, consult legacy app at <<[PROJECT_PATH]>> as source of truth"
- Guidance for clarifying ambiguous requirements
- Reference functional-spec.md for feature details

**3. tasks-prompt.md**
- Task breakdown guidance
- Use 50/30/15/5 phasing from technical-spec.md
- Include priority guidance from functional-spec.md (CRITICAL first)

**4. implement-prompt.md**
- **CRITICAL**: Must include "When implementing features, consult legacy app at <<[PROJECT_PATH]>> for behavioral details"
- Implementation best practices
- Reference technical-spec.md for patterns

**Progress Display**:

```text
✅ stage-prompts/ COMPLETE (4 files)
   - constitution-prompt.md
   - clarify-prompt.md
   - tasks-prompt.md
   - implement-prompt.md
```text

**ARTIFACTS NOT GENERATED**:
- ❌ recommended-constitution.md (replaced by constitution-prompt.md)
- ❌ upgrade-plan.md (not goal for modernization path)
- ❌ proposed-tech-stack.md (embedded in technical-spec.md)

**SUPPORTING FILES** (Optional):
- `dependency-audit.json` - Package inventory
- `metrics-summary.json` - Code metrics
- `decision-matrix.md` - Strategy comparison

---

### STEP 6.B: CROSS-CUTTING CONCERN ARTIFACTS (ANALYSIS_SCOPE = [B])

**REQUIRED ARTIFACTS**:

#### 1. **concern-analysis.md** (1,500-3,000 lines - 3 chunks)

**Source**: Analysis from Step 4.B + analysis-report.md context

**Template**: `templates/analysis/concern-analysis-template.md`

**Chunk 1: Introduction + Context + File Identification**
- Section 1: Introduction
- Section 2: Context from analysis-report.md
- Section 3: Identified Files
- Content: Concern overview, reference to analysis-report.md, all concern files with evidence
- Completion: Context clear, all files identified with file:line refs

```text
Progress: ✓ concern-analysis.md Chunk 1/3 complete: Intro + Files
          - Files identified: [COUNT]
          - Lines: [COUNT]
```text

**Chunk 2: Abstraction + Blast Radius + Coupling**
- Section 4: Abstraction Assessment (from Step 4.B.2)
- Section 5: Blast Radius (from Step 4.B.3)
- Section 6: Coupling Analysis (from Step 4.B.4)
- Content: All findings with file:line evidence
- Completion: All metrics calculated, evidence provided

```text
Progress: ✓ concern-analysis.md Chunk 2/3 complete: Analysis Metrics
          - Abstraction score: [SCORE]
          - Blast radius: [PERCENT]%
          - Lines: [COUNT]
```text

**Chunk 3: Migration Strategy + Risks + Recommendations**
- Section 7: Recommended Strategy (from Step 4.B.5)
- Section 8: Risks & Mitigation
- Section 9: Recommendations & Next Steps
- Content: Strategy, risk analysis, action items
- Completion: All sections complete, no placeholders

```text
Progress: ✅ concern-analysis.md COMPLETE (3/3 chunks)
          - Strategy: [APPROACH]
          - Total lines: [COUNT]
```text

#### 2. **abstraction-recommendations.md** (As needed)

**Source**: Step 4.B.6

**Conditional Generation**:
- **IF** abstraction level = LOW or MEDIUM:
  - Generate comprehensive recommendations
  - Include refactoring roadmap
  - Generate in 1-2 chunks
- **ELSE** (HIGH abstraction):
  - Generate brief recommendations
  - Generate in 1 chunk

**Progress Display**:

```text
✓ abstraction-recommendations.md complete
  - Lines: [COUNT]
```text

#### 3. **concern-migration-plan.md** (1-2 chunks)

**Source**: Step 4.B.5 with detailed phasing

**Chunk 1: Strategy + Phasing**
- Migration approach
- 50/30/15/5 phasing with specific deliverables
- Content: Detailed from Step 4.B.5

**Chunk 2: Risks + Testing + Rollback** (if needed)
- Risk mitigation strategies
- Testing strategy for migration
- Rollback procedures

**Progress Display**:

```text
✅ concern-migration-plan.md COMPLETE
   - Phases: 4
   - Lines: [COUNT]
```text

#### 4. **EXECUTIVE-SUMMARY.md** (1 chunk)

**Source**: Key findings from concern analysis

**Content**:
- Concern type and current/target implementations
- Key findings (abstraction quality, blast radius, risk)
- Recommended approach and timeline
- Business impact and value delivery
- Reference key metrics from analysis-report.md

**Progress Display**:

```text
✓ EXECUTIVE-SUMMARY.md complete
  - Lines: [COUNT]
```text

**SUPPORTING FILES** (Optional):
- `concern-files-inventory.json` - List of all concern-related files with metadata
- `dependency-graph.md` - Visual dependency map for the concern (if complex)

**CRITICAL NOTE**: All concern-specific artifacts should reference the analysis-report.md for broader project context. This ensures decisions are informed by the full technical landscape.

---

## 8. FINAL REPORT & SUMMARY

**Lines**: 2313-2372 (60 lines)

### Key Content Summary

After artifact generation completes, display comprehensive final report to user:

**Required Elements**:
1. Legacy stack detected (language, framework, database, dependencies)
2. User's chosen target stack (from 10 questions) OR Target concern implementation
3. Key findings (security, technical debt, complexity)
4. Generated artifacts and their locations
5. Next steps (review artifacts, start constitution stage, etc.)

**Example Final Report Template**:

```text
═══════════════════════════════════════════════════════════
ANALYSIS COMPLETE
═══════════════════════════════════════════════════════════

**Legacy Stack Detected**:
- Language: [LANGUAGE VERSION]
- Framework: [FRAMEWORK VERSION]
- Database: [DATABASE VERSION]
- Dependencies: [COUNT] packages ([COUNT] outdated, [COUNT] vulnerable)

**Target Stack** (from user preferences):
- Language: [TARGET LANGUAGE VERSION]
- Framework: [TARGET FRAMEWORK]
- Database: [TARGET DATABASE]
- Deployment: [TARGET DEPLOYMENT]
- [... other choices from 10 questions ...]

**Key Findings**:
- Technical Debt: [COUNT] HIGH, [COUNT] MEDIUM, [COUNT] LOW severity items
- Security Vulnerabilities: [COUNT] findings
- Code Quality: [ASSESSMENT]
- Test Coverage: [PERCENT]%
- Complexity Score: [SCORE]/10

**Primary Recommendation**: [RECOMMENDATION]
**Confidence**: [PERCENT]%
**Rationale**: [1-2 sentences]

**Generated Artifacts** (in .analysis/[PROJECT]-[TIMESTAMP]/):
- ✅ analysis-report.md ([SIZE] lines) - Comprehensive analysis
- ✅ EXECUTIVE-SUMMARY.md - Stakeholder overview
- ✅ functional-spec.md ([SIZE] lines) - Features with evidence
- ✅ technical-spec.md ([SIZE] lines) - Architecture & target stack
- ✅ stage-prompts/ (4 files) - Workflow guidance
- ✅ dependency-audit.json - Package inventory
- ✅ metrics-summary.json - Code metrics

**Next Steps**:
1. Review analysis-report.md for detailed findings
2. Share EXECUTIVE-SUMMARY.md with stakeholders
3. Use functional-spec.md and technical-spec.md as modernization blueprint
4. Start Spec Kit workflow with: `specify constitution` (uses constitution-prompt.md)

**Analysis Time**: [DURATION]
**Files Analyzed**: [COUNT]
**Total Output**: [SIZE] lines across [COUNT] artifacts
═══════════════════════════════════════════════════════════
```text

### Critical Information for Prompt Chaining

- Display all artifact file paths (absolute paths)
- Provide time taken for analysis
- Summarize legacy and target stacks
- State primary recommendation with confidence
- Direct user to next steps (constitution stage, etc.)
- Reference artifact locations for easy access

---

## CROSS-SECTION DEPENDENCIES

### Data Flow Between Sections

```text
Section 1 (User Input)
  → Capture PROJECT_PATH, ANALYSIS_SCOPE, CONCERN_TYPE (if [B])
  ↓
Section 2 (Estimation & Workflow)
  → Run setup scripts, detect tech stack, ask 10 questions (if [A])
  → Store modernization preferences
  ↓
Section 3 (File Analysis)
  → Read file-manifest.json, categorize files, extract features
  → Store 50-200 feature descriptions with criticality
  ↓
Section 4 (Analysis Report Generation)
  → Generate 9-phase analysis-report.md in 9 chunks
  → Verification gate (HARD STOP)
  ↓
Section 5 (Optional: Step 4.B)
  → IF ANALYSIS_SCOPE = [B]: Deep-dive concern analysis
  → Abstraction assessment, blast radius, coupling, migration strategy
  ↓
Section 7 (Artifact Generation)
  → Prerequisite: analysis-report.md must exist and be COMPLETE
  → Generate conditional artifacts based on ANALYSIS_SCOPE
  ↓
Section 8 (Final Report)
  → Summarize findings, list artifacts, next steps
```text

### Critical Prerequisites

```text
Step 4.A → Step 4.B:
  - BEFORE starting 4.B, Step 4.A must be COMPLETE
  - analysis-report.md must PASS verification gate
  - Cannot proceed without passing verification

Step 4.A OR 4.B → Step 6:
  - analysis-report.md must EXIST and be COMPLETE
  - CANNOT generate artifacts without verified analysis report
  - Hard stop if analysis-report.md missing/incomplete

Step 3 → Step 4:
  - Modernization preferences from 10 questions must be STORED
  - Used during artifact generation (technical-spec.md, stage-prompts)
```text

---

## CHUNKING STRATEGY SUMMARY

### Completion-Based Chunking (Not Size-Based)

**Analysis Report (9 chunks)**:
- Each chunk = complete logical phase/section
- Not based on line count
- Chunk ends when phase is fully complete and verified
- Checkpoint marker created after each chunk
- Mandatory progress display after each chunk

**Functional Spec (5 chunks)**:
- Chunk 1: Intro/Summary/Scope
- Chunk 2: CRITICAL features
- Chunk 3: STANDARD features + rules
- Chunk 4: NFRs + Data
- Chunk 5: Acceptance criteria + Assumptions + Constraints

**Technical Spec (5 chunks)**:
- Chunk 1: Architecture + Comparison
- Chunk 2: Tech Stack + Data
- Chunk 3: API + Integrations
- Chunk 4: Security + Deployment
- Chunk 5: Testing + Observability + Risks

**Concern Analysis (3 chunks)**:
- Chunk 1: Intro + Context + Files
- Chunk 2: Abstraction + Blast Radius + Coupling
- Chunk 3: Strategy + Risks + Recommendations

### Progress Display Pattern

After each chunk:

```text
✓ [ARTIFACT] Chunk [N]/[TOTAL] complete: [PHASE/SECTION NAME]
  - [Key metric 1]: [VALUE]
  - [Key metric 2]: [VALUE]
  - Lines generated: [COUNT]
```text

After all chunks:

```text
✅ [ARTIFACT] COMPLETE ([N]/[N] chunks)
   - [Summary metric 1]: [VALUE]
   - [Summary metric 2]: [VALUE]
   - Total lines: [COUNT]
```text

---

## VALIDATION & QUALITY GATES

### Hard Stops (Cannot Proceed Without)

1. **Step 4.A Verification Gate**:
   - All 9 phases present
   - 50+ file:line references
   - No placeholders
   - 3,000+ lines minimum
   - HARD STOP if ANY check fails

2. **Analysis Report Complete**:
   - REQUIRED before generating ANY artifact
   - HARD STOP if missing or incomplete

3. **10 Questions Storage (if [A])**:
   - All user responses must be stored
   - REQUIRED before generating technical-spec.md

### Quality Checks (Per Artifact)

**Analysis Report**:
- All 9 phase headers present
- 50+ file:line references
- Technical debt categorized by severity
- Security vulnerabilities with risk scores
- Feasibility scores with formulas shown
- Primary recommendation with confidence (0-100%)
- No placeholders

**Functional Spec**:
- All features have file:line references
- Features categorized by criticality
- NFRs defined with metrics
- Data models documented with relationships
- No placeholders

**Technical Spec**:
- User's modernization choices reflected
- Architecture comparison complete
- Deployment strategy matches Q5 choice
- IaC/Containerization matches Q6/Q7 choices
- No placeholders

**Stage Prompts**:
- clarify-prompt.md includes legacy app reference
- implement-prompt.md includes legacy app reference
- All reference functional/technical specs

---

## RECOMMENDED PROMPT CHAIN STRUCTURE

Based on the sections identified, create these individual stage prompts:

1. **phase-0-user-input.md** (Lines 60-162)
   - Interactive dialogue templates
   - Validation rules
   - Data storage requirements

2. **phase-1-estimation.md** (Lines 235-550)
   - Setup script execution
   - Tech stack detection
   - Modernization preference questions
   - Conditional branching logic

3. **phase-2-file-analysis.md** (Lines 552-904)
   - 4-step analysis methodology
   - File categorization patterns
   - Feature extraction standards
   - Quality gates & validation

4. **phase-3-analysis-generation.md** (Lines 890-1343)
   - 9-phase analysis report structure
   - Completion-based chunking strategy
   - Checkpoint/resume mechanism
   - Verification gate (HARD STOP)

5. **phase-4-concern-analysis.md** (Lines 1347-1719)
   - 6-step concern deep-dive
   - File identification patterns
   - Abstraction/Blast Radius/Coupling assessments
   - Migration strategy decision tree

6. **phase-5-clarifications.md** (Lines 1723-1843)
   - Clarification question templates
   - Artifactory validation (optional)
   - User decision handling

7. **phase-6-artifact-generation.md** (Lines 1849-2310)
   - Conditional artifact generation (Path A vs B)
   - Section-by-section chunking for large artifacts
   - Progress display patterns
   - Prerequisite validation

8. **phase-7-final-report.md** (Lines 2313-2372)
   - Summary template
   - Key findings format
   - Next steps guidance
   - Artifact listing

---

END OF SECTION BREAKDOWN
