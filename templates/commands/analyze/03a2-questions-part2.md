---
stage: full_app_questions_2
requires: 03a1-questions-complete checkpoint
condition: state.analysis_scope == "A"
outputs: modernization_prefs_6_10
version: 3.1.0
next: 03a3-validation-scoring.md
---

# Stage 3A-2: Modernization Questions (Part 2)

## Purpose

Ask questions 6-10 to complete the modernization preferences. These cover infrastructure as code, containerization, observability, security, and testing.

---

## Pre-Check: Verify Previous Substage

1. Read `.analysis/.checkpoints/03a1-questions-complete.json`
2. Confirm `status` = "complete"
3. Load Q1-Q5 responses

**IF not complete:** STOP - Return to 03a1-questions-part1.md

---

## Question 6: Infrastructure as Code

---
⏸️ **[STOP: USER_INPUT_REQUIRED - Q6]**

Present this question EXACTLY as written:

```
════════════════════════════════════════════════════════════
QUESTION 6 of 10: Infrastructure as Code (IaC)

What infrastructure as code tool do you want to use?

Current detected: {detected_iac from Stage 2, or "None detected"}

Options (based on deployment: {q5_deployment.value}):

For Kubernetes:
  [A] Helm charts
  [B] Kustomize
  [C] Kubernetes YAML only

For AWS:
  [A] Terraform
  [B] AWS CDK
  [C] CloudFormation
  [D] Pulumi

For Azure:
  [A] Terraform
  [B] Bicep
  [C] ARM Templates
  [D] Pulumi

For GCP:
  [A] Terraform
  [B] Deployment Manager
  [C] Pulumi

General:
  [X] None (manual deployment)
  [Y] Ansible
  [Z] Other (please specify)

Your choice: ___

TIP: Type "skip" to proceed without IaC.
════════════════════════════════════════════════════════════
```

**WAIT for user response. DO NOT proceed until answered.**

---

### Record Q6 Response

```json
{
  "q6_iac": {
    "choice": "{letter or custom}",
    "value": "{resolved IaC tool or 'none'}",
    "rationale": "{user's reason if provided}"
  }
}
```

---

## Question 7: Containerization Strategy

---
⏸️ **[STOP: USER_INPUT_REQUIRED - Q7]**

Present this question EXACTLY as written:

```
════════════════════════════════════════════════════════════
QUESTION 7 of 10: Containerization Strategy

What containerization approach do you want to use?

Current detected: {detected_containerization from Stage 2}

Options:
  [A] Docker + Kubernetes
  [B] Docker + Docker Compose
  [C] Podman
  [D] Buildpacks (Cloud Native)
  [E] Serverless containers (Fargate, Cloud Run)
  [F] No containers (traditional deployment)

Your choice: ___

TIP: Type "skip" to use current approach.
════════════════════════════════════════════════════════════
```

**WAIT for user response. DO NOT proceed until answered.**

---

### Record Q7 Response

```json
{
  "q7_containerization": {
    "choice": "{letter or custom}",
    "value": "{resolved strategy}",
    "rationale": "{user's reason if provided}"
  }
}
```

---

## Question 8: Observability Stack

---
⏸️ **[STOP: USER_INPUT_REQUIRED - Q8]**

Present this question EXACTLY as written:

```
════════════════════════════════════════════════════════════
QUESTION 8 of 10: Observability Stack

What observability tools do you want to use?

Current detected: {detected_observability from Stage 2}

Options:

Metrics:
  [A] Prometheus + Grafana
  [B] Datadog
  [C] New Relic
  [D] CloudWatch / Azure Monitor / Cloud Monitoring
  [E] Other (please specify)

Logging:
  [A] ELK Stack (Elasticsearch, Logstash, Kibana)
  [B] Loki + Grafana
  [C] Splunk
  [D] Cloud-native logging
  [E] Other (please specify)

Tracing:
  [A] Jaeger
  [B] Zipkin
  [C] OpenTelemetry
  [D] Commercial APM (Datadog, New Relic)
  [E] Other (please specify)

Your choice (format: metrics/logging/tracing): ___

Example: "A/B/C" for Prometheus, Loki, Jaeger
         Or describe your preferred stack

TIP: Type "skip" to determine based on deployment target.
════════════════════════════════════════════════════════════
```

**WAIT for user response. DO NOT proceed until answered.**

---

### Record Q8 Response

```json
{
  "q8_observability": {
    "choice": "{user input}",
    "value": {
      "metrics": "{resolved tool}",
      "logging": "{resolved tool}",
      "tracing": "{resolved tool}"
    },
    "rationale": "{user's reason if provided}"
  }
}
```

---

## Question 9: Security & Authentication

---
⏸️ **[STOP: USER_INPUT_REQUIRED - Q9]**

Present this question EXACTLY as written:

```
════════════════════════════════════════════════════════════
QUESTION 9 of 10: Security & Authentication

What authentication/authorization approach do you want?

Current detected: {detected_auth from Stage 2}

Options:
  [A] Keep current approach (upgrade if needed)
  [B] OAuth 2.0 / OpenID Connect (self-hosted)
  [C] Okta
  [D] Auth0
  [E] AWS Cognito
  [F] Azure AD / Entra ID
  [G] Keycloak
  [H] Firebase Auth
  [I] Custom JWT (modernized)
  [J] Other (please specify)

Your choice: ___

TIP: Type "skip" to keep current auth approach.
════════════════════════════════════════════════════════════
```

**WAIT for user response. DO NOT proceed until answered.**

---

### Record Q9 Response

```json
{
  "q9_security": {
    "choice": "{letter or custom}",
    "value": "{resolved auth provider}",
    "rationale": "{user's reason if provided}"
  }
}
```

---

## Question 10: Testing Strategy

---
⏸️ **[STOP: USER_INPUT_REQUIRED - Q10]**

Present this question EXACTLY as written:

```
════════════════════════════════════════════════════════════
QUESTION 10 of 10: Testing Strategy

What testing approach do you want for the modernized app?

Current detected: {detected_testing from Stage 2}

Options:
  [A] Keep current testing approach
  [B] Unit + Integration tests only
  [C] Unit + Integration + E2E tests
  [D] Full pyramid (Unit > Integration > E2E)
  [E] Contract testing (Pact, etc.)
  [F] BDD with Cucumber/SpecFlow
  [G] Property-based testing
  [H] Custom combination (please specify)

Coverage target: ___% (enter a number, e.g., 80)

Your choice: ___

TIP: Type "skip" to use current approach.
════════════════════════════════════════════════════════════
```

**WAIT for user response. DO NOT proceed until answered.**

---

### Record Q10 Response

```json
{
  "q10_testing": {
    "choice": "{letter or custom}",
    "value": "{resolved testing strategy}",
    "coverage_target": "{percentage or default 80}",
    "rationale": "{user's reason if provided}"
  }
}
```

---

## Compile All Preferences

Merge all Q1-Q10 responses into modernization preferences:

```json
{
  "modernization_preferences": {
    "target_language": "{q1_language.value}",
    "target_database": "{q2_database.value}",
    "message_bus": "{q3_message_bus.value}",
    "package_manager": "{q4_package_manager.value}",
    "deployment_target": "{q5_deployment.value}",
    "iac_tool": "{q6_iac.value}",
    "containerization": "{q7_containerization.value}",
    "observability": {
      "metrics": "{q8 metrics}",
      "logging": "{q8 logging}",
      "tracing": "{q8 tracing}"
    },
    "security": "{q9_security.value}",
    "testing": {
      "strategy": "{q10_testing.value}",
      "coverage_target": "{q10_testing.coverage_target}"
    }
  }
}
```

---

## Checkpoint: Questions 6-10 Complete

### Create Checkpoint

Write checkpoint file: `.analysis/.checkpoints/03a2-questions-complete.json`

```json
{
  "substage": "03a2-questions-part2",
  "timestamp": "{ISO-8601}",
  "questions_completed": [6, 7, 8, 9, 10],
  "responses": {
    "q6_iac": "{value}",
    "q7_containerization": "{value}",
    "q8_observability": "{value}",
    "q9_security": "{value}",
    "q10_testing": "{value}"
  },
  "all_questions_complete": true,
  "status": "complete"
}
```

### Verify Checkpoint

1. Read `.analysis/.checkpoints/03a2-questions-complete.json`
2. Confirm all 5 questions have responses
3. Confirm `all_questions_complete` = true

---
⏸️ **[STOP: CHECKPOINT_VERIFY]**

**IF checkpoint verified:** Output: `✓ Checkpoint verified: 03a2-questions-part2`
**IF checkpoint failed:** Retry checkpoint creation once, then STOP if still failing

---

## Progress Summary

```
═══════════════════════════════════════════════════════════
  SUBSTAGE COMPLETE: 03a2-questions-part2

  All 10 Questions Completed ✓

  Modernization Preferences Summary:
  ─────────────────────────────────────────────────────────
    Language: {q1 value}
    Database: {q2 value}
    Message Bus: {q3 value}
    Build Tool: {q4 value}
    Deployment: {q5 value}
    IaC: {q6 value}
    Containers: {q7 value}
    Observability: {q8 value}
    Security: {q9 value}
    Testing: {q10 value}
  ─────────────────────────────────────────────────────────

  Proceeding to Scope Validation & Scoring...
═══════════════════════════════════════════════════════════
```

---

## Next Substage

Proceed immediately to: **03a3-validation-scoring.md**
