# Reverse Engineering & Modernization Guide

**Status**: EXPERIMENTAL (v1.0.0-alpha) | ~4,564 LOC Python + orchestration + templates

---

## Overview

Analyze existing codebases to assess current state, identify strengths/weaknesses, plan upgrades, and make data-driven modernization decisions.

**Use Cases:** Legacy modernization, technical debt assessment, security audits, migration planning, architecture reviews, cross-cutting concern migrations.

---

## Quick Start

```bash
/speckitadv.analyze-project
# Provide PROJECT_PATH when prompted
# Choose scope: [A] Full Application or [B] Cross-Cutting Concern
```

### Analysis Scopes

| Scope | Use Case | Time | Output |
|-------|----------|------|--------|
| **[A] Full Application** | Complete modernization | 2-4 hours | analysis-report.md, functional-spec.md, technical-spec.md, stage-prompts/ |
| **[B] Cross-Cutting Concern** | Targeted migration | 30-60 min | concern-analysis.md, concern-migration-plan.md |

---

## Full Application Analysis [A]

### Generated Artifacts

| File | Purpose |
|------|---------|
| `analysis-report.md` | Technical assessment with strengths/weaknesses, upgrade paths, recommendations |
| `EXECUTIVE-SUMMARY.md` | High-level overview for stakeholders |
| `functional-spec.md` | WHAT the system does (features from existing code) |
| `technical-spec.md` | HOW to build modernized system |
| `stage-prompts/` | Ready-to-use prompts for constitution, clarify, tasks, implement |
| `decision-matrix.md` | Comparison table for inline vs greenfield vs hybrid |

### Interactive Questions (10)

1. Target Language/Framework
2. Target Database
3. Message Bus/Queue [OPTIONAL if not detected]
4. Package Manager
5. Deployment Infrastructure
6. Infrastructure as Code [SKIPPED for traditional deployments]
7. Containerization Strategy [SKIPPED for traditional deployments]
8. Observability Stack [OPTIONAL if not detected]
9. Security & Authentication
10. Testing Strategy

### Feasibility Scoring (0-100)

**Inline Upgrade Score:**

```text
Score = (Code_Quality × 0.20) + (Test_Coverage × 0.15) + (Dependency_Health × 0.20) +
        (Architecture_Quality × 0.15) + (Team_Familiarity × 0.10) +
        (Documentation × 0.10) + (Breaking_Changes × 0.10)
```

| Score | Interpretation |
|-------|---------------|
| 80-100 | ✅ Highly feasible - proceed with inline upgrade |
| 60-79 | ⚠️ Feasible with caution |
| 40-59 | 🟡 Consider hybrid approach |
| 0-39 | 🔴 Consider greenfield rewrite |

### Decision Workflow

**INLINE UPGRADE** when: Inline score ≥70, adequate test coverage (≥60%), no critical architecture flaws

**GREENFIELD REWRITE** when: Greenfield score ≥60, inline score <50, critical tech debt, well-understood requirements

**HYBRID (Strangler Fig)** when: Both scores 50-69, can maintain parallel systems, gradual transition acceptable

---

## Cross-Cutting Concern Analysis [B]

### Supported Concern Types (9)

1. Authentication/Authorization (Custom JWT → Okta, SAML → OAuth 2.0)
2. Database/ORM Layer (Oracle → PostgreSQL, Raw SQL → ORM)
3. Caching Layer (Memcached → Redis)
4. Message Bus/Queue (TIBCO → Kafka, RabbitMQ → Azure Service Bus)
5. Logging/Observability (Custom → ELK Stack, Prometheus+Grafana)
6. API Gateway/Routing (Custom → Kong/Nginx)
7. File Storage/CDN (Local → S3/Azure Blob)
8. Deployment/Infrastructure (VM → OpenShift, On-premise → Cloud)
9. Other (user-specified)

### Generated Artifacts

| File | Contents |
|------|----------|
| `concern-analysis.md` | Files with evidence (file:line), abstraction level (HIGH/MEDIUM/LOW), blast radius (%), coupling degree |
| `abstraction-recommendations.md` | Refactoring guidance before migration |
| `concern-migration-plan.md` | Strategy, phased implementation (50/30/15/5), week-by-week plan, rollback procedures |
| `EXECUTIVE-SUMMARY.md` | Timeline and business impact |

### Migration Strategies

| Strategy | When to Use | Timeline |
|----------|-------------|----------|
| **STRANGLER_FIG** | HIGH abstraction + LOOSE coupling | 2-4 weeks |
| **ADAPTER_PATTERN** | MEDIUM abstraction | 4-8 weeks |
| **REFACTOR_FIRST** | LOW abstraction + small blast radius | 6-12 weeks |
| **BIG_BANG_WITH_FEATURE_FLAGS** | LOW abstraction + large blast radius | 3-6 months |

### Example Migrations

| Migration | Strategy | Timeline |
|-----------|----------|----------|
| Custom JWT → Okta | STRANGLER_FIG | 3 weeks |
| Oracle → PostgreSQL | ADAPTER_PATTERN | 6 weeks |
| VM → OpenShift | REFACTOR_FIRST | 8 weeks |
| Memcached → Redis | STRANGLER_FIG | 2 weeks |

---

## Analysis Depths

| Depth | Time | Use Case | Output |
|-------|------|----------|--------|
| **QUICK** | 30 min | Initial assessment, health check | Executive summary, critical issues |
| **STANDARD** | 2-4 hours | Most use cases, migration planning | Complete analysis, upgrade plan, constitution |
| **COMPREHENSIVE** | 1-2 days | Mission-critical, compliance requirements | All STANDARD + performance, security hardening, ROI |

---

## What Gets Analyzed

| Category | Analysis |
|----------|----------|
| **Tech Stack** | Languages, frameworks, databases, build tools, runtime versions, EOL dates |
| **Dependencies** | Direct/transitive, outdated packages, CVEs, license compatibility |
| **Code Quality** | LOC, test coverage, complexity, code smells, anti-patterns |
| **Architecture** | Pattern (MVC, microservices), layer separation, coupling, circular deps |
| **Security** | CVEs (CRITICAL → LOW), input validation, auth patterns, exposed secrets |
| **Performance** | Response times, query efficiency, bundle sizes (if data available) |

---

## State Management & Resumption

Progress tracked in `.analysis/{project}-{timestamp}/state.json`:

```bash
# Resume latest analysis
speckitadv analyze-project

# Resume specific analysis
speckitadv analyze-project --analysis-dir=.analysis/project-20251224-164004
```

---

## Workflow After Analysis

### For Inline Upgrade

1. Review `analysis-report.md` for findings
2. Review `technical-spec.md` for target architecture
3. Use `stage-prompts/` for Toolkit workflow
4. Implement incrementally with testing

### For Greenfield Rewrite

1. Review `functional-spec.md` for features to preserve
2. Use `stage-prompts/constitution-prompt.md` for principles
3. Run `/speckitadv.constitution` → `/speckitadv.specify` → `/speckitadv.plan`

### For Cross-Cutting Concern

1. Review `concern-analysis.md` for current implementation
2. Review `abstraction-recommendations.md` if LOW/MEDIUM abstraction
3. Follow `concern-migration-plan.md` step-by-step
4. Implement phased rollout (50/30/15/5)

---

## Best Practices

| Practice | Why |
|----------|-----|
| Run analysis early | Don't wait until deadlines are tight |
| Choose appropriate depth | QUICK for health checks, STANDARD for most, COMPREHENSIVE for critical |
| Involve stakeholders | Share decision-matrix.md with leadership |
| Follow the plan | Don't skip phases, validate at checkpoints |
| Test thoroughly | Full test suite after each phase |
| Monitor post-deployment | Watch error rates 48 hours, compare metrics |

---

## Known Limitations

| Limitation | Workaround |
|------------|------------|
| Tool dependencies (npm audit, cloc) | Falls back to manual analysis if unavailable |
| Large codebases (>500K LOC) | Analyze subdirectories separately |
| Language depth varies | Best: JS/Python, Good: Java/.NET/Ruby/PHP, Basic: others |
| Scoring calibration | Adjust thresholds for your organization's risk tolerance |
| AI-guided workflow | Requires human review of recommendations |

---

## FAQ

| Question | Answer |
|----------|--------|
| How long does analysis take? | QUICK: 30min, STANDARD: 2-4hr, COMPREHENSIVE: 1-2 days |
| Non-JavaScript projects? | Yes - JS, Python, Java, C#, Ruby, PHP, Go, Rust supported |
| No tests in project? | Flagged as critical issue, lowers feasibility score |
| Monorepo analysis? | Analyze each project separately |
| Is code sent anywhere? | No - runs entirely locally |
| Re-run after changes? | Yes - track progress and validate improvements |

---

## Requirements

- AI coding agent (Claude Code, GitHub Copilot, etc.)
- Python 3.10+
- Optional tools (enhance automation): `npm audit`, `pip-audit`, `cloc`, `tokei`, Snyk

---

## Contributing

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [AGENTS.md](../AGENTS.md)
- [GitHub Issues](https://github.com/veerabhadra-ponna/spec-kit-smart/issues)
