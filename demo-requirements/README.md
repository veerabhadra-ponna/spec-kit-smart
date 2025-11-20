# Spec Kit Smart - Demo Requirements

## Why These Use Cases?

These 6 sample requirements demonstrate scenarios where **vibe coding fails** and **spec-driven development wins**. Each highlights a different critical failure mode of ad-hoc AI coding.

| Use Case | Vibe Coding Problem | Spec Kit Solution |
|----------|--------------------|--------------------|
| 1. Payment System | Context loss across sessions | Multi-session orchestration |
| 2. Healthcare Portal | Compliance drift | Corporate guidelines enforcement |
| 3. Legacy Migration | Blind refactoring | Data-driven modernization |
| 4. FX Options Pricing | Missing domain conventions | Domain specification |
| 5. Regulatory Reporting | Discovery through rejections | Complete regulatory schema |
| 6. FIX Broker Integration | Standalone code, no integration | Existing system analysis |

---

## Demo Scenarios

### General Purpose

#### [Use Case 1: Multi-Session Complex Feature](./use-case-1-payment-system.md)
**Problem:** Features too large for single AI sessions lose context
**Scenario:** Enterprise payment processing system with PCI-DSS compliance

#### [Use Case 2: Compliance-Critical Development](./use-case-2-healthcare-portal.md)
**Problem:** Standards enforcement happens post-development (expensive rework)
**Scenario:** Healthcare patient portal with HIPAA requirements

#### [Use Case 3: Legacy System Modernization](./use-case-3-legacy-migration.md)
**Problem:** AI rewrites without understanding existing architecture
**Scenario:** Monolithic e-commerce platform to microservices

---

### Finance / Capital Markets

#### [Use Case 4: FX Options Pricing & Risk](./use-case-4-fx-options-pricing.md)
**Problem:** Textbook formulas miss critical market conventions
**Scenario:** Real-time FX options pricing with Greeks calculation

**Key Differentiator:** Quant finance has decades of accumulated conventions (delta types, vol quoting, day counts). Vibe coding uses textbook Black-Scholes; Spec Kit extracts actual market conventions. Difference = $500K trading loss.

#### [Use Case 5: Regulatory Reporting (EMIR/MiFID II)](./use-case-5-fx-regulatory-reporting.md)
**Problem:** Discovers requirements through rejection emails
**Scenario:** Multi-jurisdiction derivatives reporting (EMIR, Dodd-Frank, MAS)

**Key Differentiator:** EMIR has 129 fields and 90 conditional rules. Vibe coding discovers them through 52 rejection cycles. Spec Kit extracts complete regulatory schema upfront. Difference = €500K in fines.

#### [Use Case 6: FIX Protocol Broker Integration](./use-case-6-fix-broker-integration.md)
**Problem:** Builds standalone code that doesn't integrate with existing system
**Scenario:** Adding Goldman Sachs to existing multi-broker trading platform

**Key Differentiator:** Integration requires understanding existing architecture. Vibe coding builds parallel systems. Spec Kit analyzes existing patterns then builds to fit. Difference = failed go-live vs same-day trading.

---

## Summary: Vibe Coding Failure Modes

| Failure Mode | Use Cases | Root Cause | Cost |
|--------------|-----------|------------|------|
| **Context Loss** | 1, 4 | Token limits across sessions | Inconsistent architecture |
| **Compliance Drift** | 2, 5 | Standards as afterthought | Fines, rework |
| **Blind Rewrite** | 3, 6 | No existing system analysis | Failed migrations |
| **Domain Ignorance** | 4, 5 | Missing specialized knowledge | Incorrect calculations |

---

## How to Demo

1. **Show the Problem**: Walk through how vibe coding would fail
2. **Show the Solution**: Demonstrate spec-kit workflow
3. **Quantify the Win**: Time saved, rework avoided, compliance guaranteed

Each use case includes:
- Complete requirements specification
- Vibe coding failure scenario
- Spec-kit success scenario
- Measurable outcomes
- 10-minute demo script

---

## Quick Reference: When to Use Each Demo

| Audience | Best Use Cases | Why |
|----------|---------------|-----|
| **General Tech** | 1, 2, 3 | Relatable domains |
| **Finance/Trading** | 4, 5, 6 | Domain-specific wins |
| **Compliance/Risk** | 2, 5 | Regulatory focus |
| **Architecture** | 3, 6 | Integration patterns |
| **Executives** | 1, 3 | Clear ROI numbers |
