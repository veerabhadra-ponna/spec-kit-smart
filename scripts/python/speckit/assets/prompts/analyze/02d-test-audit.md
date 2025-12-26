---
stage: file_analysis_phase4
requires: 02c-config-analysis complete
outputs: test_and_dependency_audit
version: 3.4.0
next: 02e-quality-gates.md
time_allocation: 20%
---

# Stage 2D: Test Coverage & Dependency Audit (Phase 4)

## Purpose

Analyze test coverage, test patterns, and perform comprehensive dependency audit for security vulnerabilities and outdated packages.

**Time Allocation:** 20% of file analysis effort

---

## How Context Is Provided

The CLI manages state and provides all context. **Do not read state.json directly.**

Values available in this prompt (already substituted by CLI):
- Project path, analysis directory, scope, context
- Concern type, current/target implementation (Scope B only)

---

## Pre-Check: Verify Previous Substage

1. Verify `{data_dir}/config-analysis.json` exists
2. Load configuration analysis results

**IF not complete:** STOP - Return to 02c-config-analysis

---

## Step 1: Test Framework Detection

---
[PAUSE] **[STOP: DETECT_TEST_FRAMEWORK]**

Identify the testing frameworks in use:

**Detection Patterns:**

| Framework | Language | Indicators |
|-----------|----------|------------|
| JUnit 4/5 | Java | `org.junit`, `@Test`, `junit-*.jar` |
| TestNG | Java | `org.testng`, `@Test`, `testng.xml` |
| Jest | JavaScript | `jest.config.js`, `@jest`, `describe/it/test` |
| Mocha | JavaScript | `mocha.opts`, `mocharc.*`, `describe/it` |
| pytest | Python | `pytest.ini`, `conftest.py`, `test_*.py` |
| unittest | Python | `unittest`, `TestCase` |
| RSpec | Ruby | `_spec.rb`, `spec_helper.rb` |
| xUnit | .NET | `xunit`, `[Fact]`, `[Theory]` |
| NUnit | .NET | `nunit`, `[Test]`, `[TestCase]` |
| Go testing | Go | `*_test.go`, `testing.T` |

**Output:**

```text
Test Framework Detection:

Primary Framework: {framework}
Version: {version if detectable}
Configuration File: {path if exists}
Additional Frameworks: {list if multiple}

```

---

## Step 2: Test Coverage Analysis

---
[PAUSE] **[STOP: ANALYZE_TEST_COVERAGE]**

Analyze test files and estimate coverage:

**Metrics to Extract:**

1. **Test File Count:**
   - Unit tests
   - Integration tests
   - E2E tests
   - Performance tests

2. **Test Distribution:**
   - Tests per module/package
   - Coverage by category (controllers, services, models)

3. **Test Patterns:**
   - Naming conventions
   - Setup/teardown patterns
   - Mock usage
   - Data factories/fixtures

4. **Test Quality Indicators:**
   - Assertions per test (average)
   - Test isolation (mocking external deps)
   - Parameterized/data-driven tests
   - Negative tests (error cases)

**Output Format:**

```text
Test Coverage Analysis:

Test Files: {count}
  Unit Tests: {count}
  Integration Tests: {count}
  E2E Tests: {count}

Test Distribution by Module:
  {module1}: {test_count} tests
  {module2}: {test_count} tests
  ...

Coverage Estimate:
  Controllers: {percentage}% covered
  Services: {percentage}% covered
  Models: {percentage}% covered
  Repositories: {percentage}% covered
  Overall: {percentage}% estimated

Test Quality:
  Avg Assertions/Test: {n}
  Mocking Used: {yes/no}
  Parameterized Tests: {count}
  Error Case Tests: {count}

```

---

## Step 3: Coverage Gaps Identification

---
[PAUSE] **[STOP: IDENTIFY_COVERAGE_GAPS]**

Identify files and modules WITHOUT corresponding tests:

**Gap Analysis:**

1. **Source files without test files:**
   - List files in `src/` without corresponding test
   - Prioritize by criticality

2. **Critical untested code:**
   - Security-related code
   - Payment/financial logic
   - Authentication flows
   - Error handling paths

**Output Format:**

```text
Test Coverage Gaps:

Untested Files: {count}/{total} ({percentage}%)

Critical Gaps (HIGH priority):
  [!] {SecurityConfig.java} - No test file
  [!] {PaymentService.java} - No test file
  [!] {AuthController.java} - Only {n} tests

Moderate Gaps (MEDIUM priority):
  [!] {UserService.java} - Partial coverage
  [!] {OrderRepository.java} - Missing edge cases

Low Priority Gaps:
  [ok] {UtilityHelper.java} - Utility class

```

---

## Step 4: Dependency Audit

---
[PAUSE] **[STOP: AUDIT_DEPENDENCIES]**

Perform comprehensive dependency security and freshness audit:

**For Each Dependency:**

1. **Version Status:**
   - Current version
   - Latest stable version
   - Latest LTS version (if applicable)
   - Version age

2. **Security Check:**
   - Known CVEs
   - Severity (CRITICAL/HIGH/MEDIUM/LOW)
   - Affected versions
   - Fixed version

3. **Maintenance Status:**
   - Last publish date
   - Active maintenance
   - Deprecation status

**Data Sources to Reference:**
- NPM audit / npm outdated
- Maven dependency:check
- pip-audit / safety
- cargo audit
- OWASP Dependency Check patterns
- Snyk database patterns

**Output Format:**

```text
Dependency Audit:

Total Dependencies: {count}
  Direct: {count}
  Transitive: {count}

===========================================================
SECURITY VULNERABILITIES
===========================================================

[!] CRITICAL ({count}):
  {package} v{current}
    CVE: {CVE-YYYY-NNNNN}
    Description: {brief description}
    Fix: Upgrade to v{fixed_version}

[!] HIGH ({count}):
  {package} v{current}
    CVE: {CVE-YYYY-NNNNN}
    Description: {brief description}
    Fix: Upgrade to v{fixed_version}

[!] MEDIUM ({count}):
  {package} v{current} - {issue}

[ok] LOW ({count}):
  {package} v{current} - {issue}

===========================================================
OUTDATED DEPENDENCIES
===========================================================

Major Version Behind ({count}):
  {package}: v{current} -> v{latest} (major update)

Minor Version Behind ({count}):
  {package}: v{current} -> v{latest} (minor update)

Patch Behind ({count}):
  {package}: v{current} -> v{latest} (patch update)

===========================================================
DEPRECATED PACKAGES
===========================================================

{package} - Deprecated, use {replacement}

```

---

## Step 5: Compile Audit Results

Create comprehensive audit summary:

```json
{
  "test_audit": {
    "framework": "{framework}",
    "framework_version": "{version}",
    "test_files": {
      "unit": {count},
      "integration": {count},
      "e2e": {count},
      "total": {count}
    },
    "coverage_estimate": {
      "controllers": "{percentage}%",
      "services": "{percentage}%",
      "models": "{percentage}%",
      "overall": "{percentage}%"
    },
    "quality_metrics": {
      "avg_assertions": {n},
      "mocking_used": true,
      "parameterized_tests": {count}
    },
    "gaps": {
      "untested_files": {count},
      "critical_gaps": ["{list}"],
      "moderate_gaps": ["{list}"]
    }
  },
  "dependency_audit": {
    "total": {count},
    "direct": {count},
    "transitive": {count},
    "vulnerabilities": {
      "critical": {count},
      "high": {count},
      "medium": {count},
      "low": {count},
      "total": {count}
    },
    "outdated": {
      "major": {count},
      "minor": {count},
      "patch": {count}
    },
    "deprecated": {count},
    "vulnerable_packages": [
      {
        "name": "{package}",
        "version": "{current}",
        "severity": "CRITICAL",
        "cve": "{CVE}",
        "fixed_in": "{version}"
      }
    ]
  }
}

```

---

## Output Summary

```text
===========================================================
  SUBSTAGE COMPLETE: 02d-test-audit (Phase 4)

  Time Used: 20% allocation

  Test Analysis:
    Framework: {framework}
    Test Files: {count}
    Coverage Estimate: {percentage}%
    Critical Gaps: {count}

  Dependency Audit:
    Total Dependencies: {count}
    Vulnerabilities: {count} ({critical} critical)
    Outdated: {count}

  Proceeding to Quality Gates
===========================================================

```

---

## Next Substage

Run: `speckitadv analyze-project`

The CLI will auto-detect the current stage and emit the next prompt.
