---
stage: full_application_analysis
requires: 04-file-analysis.json
condition: state.analysis_scope == "A"
outputs: full_app_state
version: 1.0.0
---

# Stage 5A: Full Application Modernization Analysis

## Purpose

For Full Application Modernization (scope = A), ask 10 progressive questions about target stack and perform comprehensive modernization assessment with scoring matrices.

---

## Previous State

Load state from: `.analysis/.state/04-file-analysis.json`

Required fields:
- `analysis_scope` must be "A"
- `tech_stack` - Current technology stack
- `patterns_found` - Analysis patterns
- `dependencies` - Dependency audit results

---

## Step 1: 10 Progressive Modernization Questions

Ask user about target modernization stack based on detected legacy stack.

### Detection Flags (for conditional logic)

Based on file analysis, set these flags:
- `HAS_MESSAGE_BUS` - true if Kafka, RabbitMQ, Azure SB, AWS SQS, Redis Pub/Sub detected
- `HAS_OBSERVABILITY` - true if logging frameworks, monitoring configs, APM tools detected
- `IS_TRADITIONAL_DEPLOYMENT` - derived from Q5 answer

### Questions

**Question 1: Target Language/Framework**

```
Current: {detected language/framework}
Options:
- [A] {Same language, latest LTS version}
- [B] {Alternative popular option}
- [C] Other (please specify)
Your choice: ___
```

**Question 2: Target Database**

```
Current: {detected or "Unknown"}
Options:
- [A] {Same database vendor, latest version}
- [B] PostgreSQL {latest LTS}
- [C] MongoDB {latest stable}
- [D] Other (please specify)
Your choice: ___
```

**Question 3: Message Bus/Queue [CONDITIONAL]**

**IF** `!HAS_MESSAGE_BUS`:

```
[OPTIONAL - Not detected in legacy code]
Since your legacy app doesn't use message queues, you can skip this.
However, modernization could benefit from async messaging.

Options:
- [A] None / Not needed
- [B] Apache Kafka
- [C] RabbitMQ
- [D] Redis Pub/Sub
- [E] Cloud-native (Azure Service Bus / AWS SQS)
- [F] Other
Your choice (or press Enter to skip): ___
```

**ELSE**:

```
Current: {detected}
Options:
- [A] Keep current
- [B] Apache Kafka
- [C] RabbitMQ
- [D] Redis Pub/Sub
- [E] Cloud-native (Azure Service Bus / AWS SQS)
- [F] Other
Your choice: ___
```

**Question 4: Package Manager**

```
Current: {detected}
Options:
- [A] Keep current
- [B] {Alternative for stack}
- [C] Other
Your choice: ___
```

**Question 5: Deployment Target**

```
Current: {detected or "Unknown"}
Options:
- [A] Dedicated server (traditional VM/bare metal)
- [B] Kubernetes
- [C] Azure (App Service, AKS, Container Apps)
- [D] AWS (ECS, EKS, Elastic Beanstalk)
- [E] Google Cloud Platform (GKE, Cloud Run)
- [F] OpenShift
- [G] Other
Your choice: ___
```

**Set** `IS_TRADITIONAL_DEPLOYMENT = (answer == "A")`

**Question 6: Infrastructure as Code [CONDITIONAL]**

**IF** `IS_TRADITIONAL_DEPLOYMENT`:

```
[SKIPPED - Not applicable for traditional deployment]
IaC is typically used with cloud deployments.
```

**ELSE**:

```
Options:
- [A] Terraform
- [B] Helm charts (for Kubernetes)
- [C] Azure ARM/Bicep (if Azure)
- [D] AWS CloudFormation (if AWS)
- [E] Ansible / Puppet / Chef
- [F] None / Manual deployment
- [G] Other
Your choice: ___
```

**Question 7: Containerization Strategy [CONDITIONAL]**

**IF** `IS_TRADITIONAL_DEPLOYMENT`:

```
[SKIPPED - Not applicable for traditional deployment]
Containerization requires cloud/container platforms.
```

**ELSE**:

```
Options:
- [A] Docker with custom images
- [B] Docker with official base images
- [C] Buildpacks / Cloud-native buildpacks
- [D] Container registry: DockerHub
- [E] Container registry: Private (Azure ACR / AWS ECR)
- [F] Other
Your choice: ___
```

**Question 8: Observability Stack [CONDITIONAL]**

**IF** `!HAS_OBSERVABILITY`:

```
[OPTIONAL - Not detected in legacy code]
Options:
- [A] None / Keep simple
- [B] ELK Stack (Elasticsearch, Logstash, Kibana)
- [C] Prometheus + Grafana
- [D] Cloud-native (Azure Monitor / AWS CloudWatch)
- [E] Datadog / New Relic / APM SaaS
- [F] Other
Your choice (or press Enter to skip): ___
```

**ELSE**:

```
Current: {detected}
Options:
- [A] Keep current
- [B] ELK Stack
- [C] Prometheus + Grafana
- [D] Cloud-native (Azure Monitor / AWS CloudWatch)
- [E] Datadog / New Relic
- [F] Other
Your choice: ___
```

**Question 9: Security & Authentication**

```
Current: {detected auth mechanism}
Options:
- [A] Keep current (modernize implementation)
- [B] OAuth 2.0 / OpenID Connect
- [C] Azure AD / Okta / Auth0
- [D] AWS Cognito
- [E] Custom JWT (modernized)
- [F] Other
Your choice: ___
```

**Question 10: Testing Strategy**

```
Current: {detected test coverage}%
Target Test Coverage:
- [A] Maintain current level
- [B] 70%+ (industry standard)
- [C] 80%+ (high quality)
- [D] 90%+ (mission critical)
Your choice: ___

Test Framework Preference:
- [A] Keep current frameworks
- [B] Modernize to latest versions
- [C] Switch to {alternative framework}
- [D] Add E2E testing (Cypress / Playwright / Selenium)
Your choice: ___
```

**Store all responses** in state as `modernization_preferences`.

---

## Step 2: Modernization Complexity Scoring

Calculate complexity scores using scoring matrices.

### Scoring Matrix

**Factors**:
1. **Code Size** (0-20 points)
   - < 10K LOC: 2 points
   - 10K-50K LOC: 5 points
   - 50K-100K LOC: 10 points
   - 100K-500K LOC: 15 points
   - > 500K LOC: 20 points

2. **Tech Stack Gap** (0-20 points)
   - Same stack, version upgrade: 5 points
   - Same language, framework change: 10 points
   - Language change (compatible paradigm): 15 points
   - Language change (different paradigm): 20 points

3. **Database Migration** (0-15 points)
   - Same DB, version upgrade: 3 points
   - SQL to SQL (different vendor): 8 points
   - SQL to NoSQL or vice versa: 15 points

4. **Architecture Change** (0-15 points)
   - Minimal changes: 3 points
   - Modularization: 8 points
   - Monolith to microservices: 15 points

5. **Integration Complexity** (0-10 points)
   - Few integrations (< 5): 2 points
   - Moderate (5-10): 5 points
   - Many (10-20): 8 points
   - Extensive (> 20): 10 points

6. **Test Coverage Gap** (0-10 points)
   - High coverage (>70%): 2 points
   - Moderate (40-70%): 5 points
   - Low (< 40%): 10 points

7. **Technical Debt** (0-10 points)
   - Low debt: 2 points
   - Moderate debt: 5 points
   - High debt: 10 points

**Total Score**: 0-100 points

**Complexity Rating**:
- 0-30: **LOW** - Straightforward upgrade
- 31-60: **MEDIUM** - Moderate effort required
- 61-80: **HIGH** - Significant transformation
- 81-100: **VERY HIGH** - Consider greenfield rewrite

### Calculate Scores

```
Complexity Score = {calculated_score}
Complexity Rating = {LOW|MEDIUM|HIGH|VERY HIGH}
```

---

## Step 3: Feasibility Analysis

Calculate three feasibility scores:

### 3.1: Inline Upgrade Feasibility

```
Formula:
Inline_Score = 100 - (Complexity_Score * 0.7) - (Tech_Debt_Score * 0.3)

Where:
- Complexity_Score = from Step 2 (0-100)
- Tech_Debt_Score = normalized from tech debt items (0-100)
```

**Rating**:
- 70-100%: **HIGHLY FEASIBLE** - Recommended approach
- 50-69%: **FEASIBLE** - Manageable with planning
- 30-49%: **CHALLENGING** - Requires significant effort
- 0-29%: **NOT RECOMMENDED** - Consider alternatives

### 3.2: Greenfield Rewrite Feasibility

```
Formula:
Rewrite_Score = (Complexity_Score * 0.5) + (Tech_Debt_Score * 0.3) + (Coverage_Gap * 0.2)

Where:
- Complexity_Score = from Step 2 (0-100)
- Tech_Debt_Score = normalized (0-100)
- Coverage_Gap = (100 - test_coverage_percentage)
```

**Rating**:
- 70-100%: **RECOMMENDED** - Rewrite is justified
- 50-69%: **CONSIDER** - Cost-benefit analysis needed
- 30-49%: **QUESTIONABLE** - Likely more expensive
- 0-29%: **NOT JUSTIFIED** - Upgrade instead

### 3.3: Hybrid Approach Feasibility

```
Formula:
Hybrid_Score = 100 - abs(Inline_Score - Rewrite_Score)

Rationale: Hybrid works best when inline and rewrite are equally viable
```

**Rating**:
- 70-100%: **VIABLE** - Good candidate for phased approach
- 50-69%: **POSSIBLE** - Consider if timeline is flexible
- 0-49%: **NOT OPTIMAL** - Choose inline or rewrite

---

## Step 4: Modernization Recommendations

Based on scores, generate prioritized recommendations:

### Quick Wins (Low Effort, High Value)

- Update dependencies to latest LTS versions
- Add missing indexes to database
- Implement caching for frequently accessed data
- Fix critical security vulnerabilities

### Strategic Improvements (Medium Effort, High Value)

- Migrate to {target framework} {version}
- Implement automated testing to reach {target coverage}%
- Add observability stack (logging, metrics, tracing)
- Refactor high-complexity modules

### Long-term Goals (High Effort, High Value)

- Migrate to {target deployment platform}
- Implement {containerization strategy}
- Migrate to {target database}
- Adopt {IaC tool} for infrastructure

---

## Output State

```json
{
  ...previous_state,
  "stage": "full_application_analysis",
  "timestamp": "2025-11-14T11:00:00Z",
  "stages_complete": [..., "full_application_analysis"],
  "modernization_preferences": {
    "target_language": "Java 17 LTS",
    "target_database": "PostgreSQL 15",
    "message_bus": "Apache Kafka",
    "deployment_target": "Kubernetes",
    "iac_tool": "Terraform",
    "containerization": "Docker with official images",
    "observability": "Prometheus + Grafana",
    "auth_strategy": "OAuth 2.0 / OpenID Connect",
    "target_test_coverage": "80%"
  },
  "scoring": {
    "complexity_score": 58,
    "complexity_rating": "MEDIUM",
    "feasibility": {
      "inline_upgrade": 62,
      "greenfield_rewrite": 45,
      "hybrid_approach": 77
    }
  },
  "recommendations": {
    "primary_approach": "hybrid",
    "confidence": 75,
    "quick_wins": [...],
    "strategic_improvements": [...],
    "long_term_goals": [...]
  }
}
```

---

## Completion Marker

```
STAGE_COMPLETE:FULL_APP
STATE_PATH: .analysis/.state/05a-full-app.json
```

---

## Next Stage

Proceed to: **Stage 6: 06-report-generation.md**
