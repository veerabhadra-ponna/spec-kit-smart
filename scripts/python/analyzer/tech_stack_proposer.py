"""
Tech stack proposer with LTS recommendations.

Generates proposed-tech-stack.md with latest LTS versions and detailed
rationale for each technology choice.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Handle both relative and absolute imports
try:
    from .scanner import ScanResult
    from .dependency_analyzer import DependencyReport
    from .scoring_engine import ProjectMetrics
except ImportError:
    from scanner import ScanResult
    from dependency_analyzer import DependencyReport
    from scoring_engine import ProjectMetrics


@dataclass
class TechRecommendation:
    """Recommendation for a specific technology component."""

    component_type: str  # "Language", "Framework", "Database", etc.
    current: str
    proposed: str
    lts_until: Optional[str]
    rationale: List[str]
    migration_complexity: str  # LOW, MEDIUM, HIGH
    migration_guide_url: Optional[str]
    alternatives: List[Tuple[str, str]]  # [(name, reason), ...]


class TechStackProposer:
    """
    Propose modernized tech stack with LTS versions and rationale.

    Recommends specific versions based on current stack, provides migration
    complexity assessment, and suggests alternatives.
    """

    # LTS version mappings (as of 2025-01)
    LTS_VERSIONS = {
        "python": ("3.12", "2028-10", "https://www.python.org/downloads/"),
        "node": ("20", "2026-04", "https://nodejs.org/en/about/releases/"),
        "java": ("21", "2029-09", "https://www.oracle.com/java/technologies/java-se-support-roadmap.html"),
        "dotnet": ("8", "2026-11", "https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core"),
        "go": ("1.21", "N/A", "https://go.dev/dl/"),
        "ruby": ("3.3", "N/A", "https://www.ruby-lang.org/en/downloads/"),
        "php": ("8.3", "2026-11", "https://www.php.net/supported-versions.php"),
        "rust": ("1.75", "N/A", "https://www.rust-lang.org/"),
    }

    FRAMEWORK_RECOMMENDATIONS = {
        "react": ("18", "Latest stable", "https://react.dev/"),
        "vue": ("3", "Latest stable", "https://vuejs.org/"),
        "angular": ("17", "Latest stable", "https://angular.io/"),
        "express": ("4", "Latest stable", "https://expressjs.com/"),
        "fastapi": ("0.104", "Latest stable", "https://fastapi.tiangolo.com/"),
        "django": ("5.0", "LTS until 2026-04", "https://www.djangoproject.com/"),
        "flask": ("3.0", "Latest stable", "https://flask.palletsprojects.com/"),
        "spring-boot": ("3.2", "Latest stable", "https://spring.io/projects/spring-boot"),
    }

    DATABASE_RECOMMENDATIONS = {
        "postgresql": ("16", "2028-11", "https://www.postgresql.org/support/versioning/"),
        "mysql": ("8.4", "2032-04", "https://www.mysql.com/support/"),
        "mongodb": ("7.0", "N/A", "https://www.mongodb.com/"),
        "redis": ("7.2", "2027-01", "https://redis.io/"),
        "mariadb": ("11.2", "N/A", "https://mariadb.org/"),
    }

    def __init__(
        self,
        scan_result: ScanResult,
        dependency_reports: List[DependencyReport],
        metrics: ProjectMetrics,
        project_name: str
    ):
        """
        Initialize tech stack proposer.

        Args:
            scan_result: Results from ProjectScanner
            dependency_reports: Results from DependencyAnalyzer
            metrics: ProjectMetrics from analysis
            project_name: Name of the project
        """
        self.scan_result = scan_result
        self.dependency_reports = dependency_reports
        self.metrics = metrics
        self.project_name = project_name
        self.date_only = datetime.now().strftime("%Y-%m-%d")

    def generate_proposed_stack(self, output_path: Path) -> Path:
        """
        Generate proposed-tech-stack.md file.

        Args:
            output_path: Path where the file should be written

        Returns:
            Path to the generated file
        """
        sections = []

        # Header
        sections.append(self._build_header())

        # Executive Summary
        sections.append(self._build_executive_summary())

        # Build recommendations
        recommendations = self._build_recommendations()

        # Language & Runtime
        if recommendations["language"]:
            sections.append(self._format_language_recommendation(recommendations["language"]))

        # Framework
        if recommendations["framework"]:
            sections.append(self._format_framework_recommendation(recommendations["framework"]))

        # Database
        if recommendations["database"]:
            sections.append(self._format_database_recommendation(recommendations["database"]))

        # Summary Table
        sections.append(self._build_summary_table(recommendations))

        # Migration Strategy
        sections.append(self._build_migration_strategy(recommendations))

        # How to Use
        sections.append(self._build_usage_guide())

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(sections))

        return output_path

    def _build_header(self) -> str:
        """Build header section."""
        return f"""# Proposed Tech Stack (with LTS + Rationale)

**Project**: {self.project_name}
**Analysis Date**: {self.date_only}
**Purpose**: Technology recommendations for modernization

---

## Document Purpose

This document recommends specific technology versions for modernization,
with detailed rationale for each choice. All recommendations include:

- **Latest LTS version** (or latest stable if no formal LTS)
- **Rationale** for the choice (why this version, why this tech)
- **Migration complexity** assessment
- **Alternative options** for comparison
- **EOL dates** for planning future upgrades

---"""

    def _build_executive_summary(self) -> str:
        """Build executive summary."""
        current_stack = self._format_current_stack()
        proposed_stack = self._format_proposed_stack()

        return f"""## Executive Summary

### Current State

{current_stack}

### Proposed State

{proposed_stack}

### Overall Assessment

- **Migration Complexity**: {self._assess_overall_complexity()}
- **Estimated Effort**: {self._estimate_overall_effort()}
- **Risk Level**: {self._assess_overall_risk()}
- **Recommended Approach**: {self._recommend_approach()}

---"""

    def _build_recommendations(self) -> Dict[str, Optional[TechRecommendation]]:
        """Build all technology recommendations."""
        return {
            "language": self._recommend_language(),
            "framework": self._recommend_framework(),
            "database": self._recommend_database(),
        }

    def _recommend_language(self) -> Optional[TechRecommendation]:
        """Recommend language/runtime version."""
        current_lang = self.scan_result.tech_stack.primary_language.lower()
        current_version = self.scan_result.tech_stack.runtime_version or "Unknown"

        # Get LTS recommendation
        if current_lang in self.LTS_VERSIONS:
            lts_version, lts_until, docs_url = self.LTS_VERSIONS[current_lang]

            # Build rationale
            rationale = [
                f"Latest LTS version with support until {lts_until}" if lts_until != "N/A" else "Latest stable version",
                "Performance improvements over older versions",
                "Security updates and bug fixes",
                "Modern language features and better tooling",
                "Long-term support ensures stability"
            ]

            # Assess migration complexity
            complexity = self._assess_language_migration_complexity(current_version, lts_version)

            # Build alternatives
            alternatives = self._get_language_alternatives(current_lang)

            return TechRecommendation(
                component_type="Language & Runtime",
                current=f"{current_lang.title()} {current_version}",
                proposed=f"{current_lang.title()} {lts_version}",
                lts_until=lts_until if lts_until != "N/A" else None,
                rationale=rationale,
                migration_complexity=complexity,
                migration_guide_url=docs_url,
                alternatives=alternatives
            )

        return None

    def _recommend_framework(self) -> Optional[TechRecommendation]:
        """Recommend framework version."""
        if not self.scan_result.tech_stack.frameworks:
            return None

        # Get primary framework (first detected)
        current_framework = self.scan_result.tech_stack.frameworks[0].lower()

        # Check if we have recommendation
        for fw_key in self.FRAMEWORK_RECOMMENDATIONS:
            if fw_key in current_framework:
                version, lts_info, docs_url = self.FRAMEWORK_RECOMMENDATIONS[fw_key]

                # Build rationale based on framework
                rationale = self._get_framework_rationale(fw_key, version)

                # Assess complexity
                complexity = self._assess_framework_migration_complexity(fw_key)

                # Get alternatives
                alternatives = self._get_framework_alternatives(fw_key)

                return TechRecommendation(
                    component_type="Web Framework",
                    current=f"{current_framework.title()} (version unknown)",
                    proposed=f"{fw_key.title()} {version}",
                    lts_until=lts_info if "LTS" in lts_info else None,
                    rationale=rationale,
                    migration_complexity=complexity,
                    migration_guide_url=docs_url,
                    alternatives=alternatives
                )

        return None

    def _recommend_database(self) -> Optional[TechRecommendation]:
        """Recommend database version."""
        if not self.scan_result.tech_stack.databases:
            # Try to infer from config files
            inferred_db = self._infer_database()
            if not inferred_db:
                return None
        else:
            inferred_db = self.scan_result.tech_stack.databases[0].lower()

        # Check if we have recommendation
        for db_key in self.DATABASE_RECOMMENDATIONS:
            if db_key in inferred_db.lower():
                version, lts_until, docs_url = self.DATABASE_RECOMMENDATIONS[db_key]

                # Build rationale
                rationale = self._get_database_rationale(db_key, version)

                # Assess complexity
                complexity = self._assess_database_migration_complexity(db_key)

                # Get alternatives
                alternatives = self._get_database_alternatives(db_key)

                return TechRecommendation(
                    component_type="Database",
                    current=f"{inferred_db.title()} (version unknown)",
                    proposed=f"{db_key.title()} {version}",
                    lts_until=lts_until if lts_until != "N/A" else None,
                    rationale=rationale,
                    migration_complexity=complexity,
                    migration_guide_url=docs_url,
                    alternatives=alternatives
                )

        return None

    def _format_language_recommendation(self, rec: TechRecommendation) -> str:
        """Format language recommendation section."""
        return f"""## {rec.component_type}

### Recommendation: {rec.proposed}

**Current**: {rec.current}
**Proposed**: {rec.proposed}
{f"**LTS Until**: {rec.lts_until}" if rec.lts_until else "**Status**: Latest Stable"}
**Migration Complexity**: {rec.migration_complexity}

#### Rationale

{chr(10).join([f"- {r}" for r in rec.rationale])}

#### Migration Complexity: {rec.migration_complexity}

{self._explain_language_complexity(rec.migration_complexity)}

{f"**Migration Guide**: {rec.migration_guide_url}" if rec.migration_guide_url else ""}

#### Alternative Options

{chr(10).join([f"- **{name}**: {reason}" for name, reason in rec.alternatives])}

---"""

    def _format_framework_recommendation(self, rec: TechRecommendation) -> str:
        """Format framework recommendation section."""
        return f"""## {rec.component_type}

### Recommendation: {rec.proposed}

**Current**: {rec.current}
**Proposed**: {rec.proposed}
{f"**LTS Until**: {rec.lts_until}" if rec.lts_until else "**Status**: Latest Stable"}
**Migration Complexity**: {rec.migration_complexity}

#### Rationale

{chr(10).join([f"- {r}" for r in rec.rationale])}

#### Migration Complexity: {rec.migration_complexity}

{self._explain_framework_complexity(rec.migration_complexity, rec.proposed)}

{f"**Documentation**: {rec.migration_guide_url}" if rec.migration_guide_url else ""}

#### Alternative Options

{chr(10).join([f"- **{name}**: {reason}" for name, reason in rec.alternatives])}

---"""

    def _format_database_recommendation(self, rec: TechRecommendation) -> str:
        """Format database recommendation section."""
        return f"""## {rec.component_type}

### Recommendation: {rec.proposed}

**Current**: {rec.current}
**Proposed**: {rec.proposed}
{f"**LTS Until**: {rec.lts_until}" if rec.lts_until else "**Status**: Latest Stable"}
**Migration Complexity**: {rec.migration_complexity}

#### Rationale

{chr(10).join([f"- {r}" for r in rec.rationale])}

#### Migration Complexity: {rec.migration_complexity}

{self._explain_database_complexity(rec.migration_complexity)}

{f"**Documentation**: {rec.migration_guide_url}" if rec.migration_guide_url else ""}

#### Alternative Options

{chr(10).join([f"- **{name}**: {reason}" for name, reason in rec.alternatives])}

---"""

    def _build_summary_table(self, recommendations: Dict[str, Optional[TechRecommendation]]) -> str:
        """Build summary comparison table."""
        rows = []

        for key, rec in recommendations.items():
            if rec:
                rows.append(
                    f"| {rec.component_type} | {rec.current} | {rec.proposed} | "
                    f"{rec.migration_complexity} | "
                    f"{self._prioritize_component(rec.component_type)} |"
                )

        if not rows:
            table = "No specific recommendations generated."
        else:
            table = """| Component | Current | Proposed (LTS) | Complexity | Priority |
|-----------|---------|----------------|------------|----------|
""" + "\n".join(rows)

        return f"""## Summary Table

{table}

**Priority Levels**:
- **CRITICAL**: Must be addressed (security, EOL)
- **HIGH**: Should be addressed soon (performance, support)
- **MEDIUM**: Address during modernization
- **LOW**: Optional upgrade

---"""

    def _build_migration_strategy(self, recommendations: Dict[str, Optional[TechRecommendation]]) -> str:
        """Build migration strategy section."""
        total_complexity = self._calculate_total_complexity(recommendations)

        return f"""## Migration Strategy

### Recommended Approach

{self._describe_migration_approach(total_complexity)}

### Migration Phases

#### Phase 1: Foundation (Week 1-2)

1. **Set up new project structure** with proposed tech stack
2. **Configure build tools** and development environment
3. **Set up CI/CD pipeline** with new versions
4. **Create testing infrastructure** (80%+ coverage target)

#### Phase 2: Core Migration (Varies)

**Effort**: {self._estimate_core_effort()}

{self._describe_core_migration_strategy()}

#### Phase 3: Testing & Validation (Week 1-2)

1. **Run full test suite** (target: 80%+ coverage)
2. **Performance testing** (meet or exceed legacy benchmarks)
3. **Security scanning** (no critical vulnerabilities)
4. **Manual QA** for critical workflows

#### Phase 4: Deployment (Week 1)

1. **Deploy to staging** environment
2. **Smoke testing** and validation
3. **Deploy to production** with rollback plan ready
4. **Monitor** and address issues

### Risk Mitigation

{self._describe_risk_mitigation(total_complexity)}

---"""

    def _build_usage_guide(self) -> str:
        """Build usage guide."""
        return """## How to Use This Document

### For Planning

1. **Review Recommendations**: Understand proposed tech stack
2. **Assess Complexity**: Review migration complexity for each component
3. **Check Alternatives**: Consider if alternatives better fit your needs
4. **Plan Timeline**: Use complexity to estimate migration effort

### For Implementation

1. **Follow LTS Versions**: Use exact versions specified (or newer LTS if available)
2. **Read Migration Guides**: Follow official migration documentation
3. **Test Incrementally**: Don't upgrade everything at once
4. **Monitor Performance**: Ensure no regressions

### For `/speckit.plan` Command

Use this document as input when running `/speckit.plan`:

```
Target Tech Stack:
- [Language]: [Proposed Version] (LTS until [Date])
- [Framework]: [Proposed Version]
- [Database]: [Proposed Version] (LTS until [Date])

Rationale: See proposed-tech-stack.md for detailed reasoning

Migration Complexity: [Overall Assessment]
Estimated Effort: [Time Estimate]
```

### Version Updates

**Note**: This document is generated based on LTS information as of {self.date_only}.
Always verify latest LTS versions before starting migration:

- Check official project websites
- Review end-of-life dates
- Consider newer LTS releases if available

---

**Generated**: {self.date_only}
**Status**: Recommendations based on automated analysis and LTS version data"""

    # Helper methods

    def _format_current_stack(self) -> str:
        """Format current stack description."""
        parts = [
            f"- **Language**: {self.scan_result.tech_stack.primary_language.title()} {self.scan_result.tech_stack.runtime_version or '(version unknown)'}",
        ]

        if self.scan_result.tech_stack.frameworks:
            parts.append(f"- **Framework**: {', '.join(self.scan_result.tech_stack.frameworks)}")

        if self.scan_result.tech_stack.databases:
            parts.append(f"- **Database**: {', '.join(self.scan_result.tech_stack.databases)}")

        if self.scan_result.tech_stack.build_tools:
            parts.append(f"- **Build Tools**: {', '.join(self.scan_result.tech_stack.build_tools)}")

        return "\n".join(parts)

    def _format_proposed_stack(self) -> str:
        """Format proposed stack description."""
        parts = []

        # Language
        lang = self.scan_result.tech_stack.primary_language.lower()
        if lang in self.LTS_VERSIONS:
            version, lts_until, _ = self.LTS_VERSIONS[lang]
            parts.append(f"- **Language**: {lang.title()} {version} (LTS until {lts_until})")

        # Framework
        if self.scan_result.tech_stack.frameworks:
            fw = self.scan_result.tech_stack.frameworks[0].lower()
            for fw_key, (version, lts_info, _) in self.FRAMEWORK_RECOMMENDATIONS.items():
                if fw_key in fw:
                    parts.append(f"- **Framework**: {fw_key.title()} {version} ({lts_info})")
                    break

        # Database (inferred or detected)
        db = self._infer_database()
        if db:
            for db_key, (version, lts_until, _) in self.DATABASE_RECOMMENDATIONS.items():
                if db_key in db.lower():
                    lts_str = f"LTS until {lts_until}" if lts_until != "N/A" else "Latest stable"
                    parts.append(f"- **Database**: {db_key.title()} {version} ({lts_str})")
                    break

        return "\n".join(parts) if parts else "- See detailed recommendations below"

    def _assess_overall_complexity(self) -> str:
        """Assess overall migration complexity."""
        loc = self.metrics.lines_of_code
        debt = self.metrics.technical_debt_percentage
        tests = self.metrics.test_coverage

        score = 0
        if loc > 50000:
            score += 2
        elif loc > 10000:
            score += 1

        if debt > 60:
            score += 2
        elif debt > 40:
            score += 1

        if tests < 40:
            score += 1

        if score >= 4:
            return "HIGH"
        elif score >= 2:
            return "MEDIUM"
        else:
            return "LOW"

    def _estimate_overall_effort(self) -> str:
        """Estimate overall migration effort."""
        complexity = self._assess_overall_complexity()

        if complexity == "HIGH":
            return "4-6 months"
        elif complexity == "MEDIUM":
            return "2-3 months"
        else:
            return "2-4 weeks"

    def _assess_overall_risk(self) -> str:
        """Assess overall risk level."""
        if self.metrics.test_coverage < 40:
            return "HIGH (low test coverage)"
        elif self.metrics.technical_debt_percentage > 60:
            return "HIGH (high technical debt)"
        elif self.metrics.test_coverage >= 80:
            return "LOW (good test coverage)"
        else:
            return "MEDIUM"

    def _recommend_approach(self) -> str:
        """Recommend migration approach."""
        if self.metrics.lines_of_code > 50000 or self.metrics.technical_debt_percentage > 60:
            return "Incremental (Strangler Fig pattern)"
        elif self.metrics.test_coverage >= 80:
            return "Big Bang (high test coverage supports full migration)"
        else:
            return "Phased (module by module)"

    def _assess_language_migration_complexity(self, current: str, proposed: str) -> str:
        """Assess language migration complexity."""
        # This is simplified - in reality would parse versions
        if "unknown" in current.lower():
            return "MEDIUM"
        elif "2." in current and "3." in proposed:  # Python 2 -> 3
            return "HIGH"
        else:
            return "LOW"

    def _get_language_alternatives(self, lang: str) -> List[Tuple[str, str]]:
        """Get alternative language options."""
        if lang == "python":
            return [
                ("Python 3.11", "Previous LTS, stable but shorter support"),
                ("Go 1.21", "Better performance, but team learning curve"),
            ]
        elif lang == "javascript":
            return [
                ("Node.js 18 LTS", "Previous LTS, still supported until 2025-04"),
                ("Deno 1.x", "Modern runtime, but ecosystem less mature"),
            ]
        elif lang == "java":
            return [
                ("Java 17 LTS", "Previous LTS, supported until 2026"),
                ("Kotlin", "Modern JVM language, but team learning curve"),
            ]
        else:
            return [("Current version", "If team prefers familiarity over latest LTS")]

    def _get_framework_rationale(self, framework: str, version: str) -> List[str]:
        """Get framework-specific rationale."""
        if framework == "react":
            return [
                "Latest stable version with concurrent features",
                "Server components support",
                "Improved performance",
                "Large ecosystem and community",
                "Team likely already familiar"
            ]
        elif framework == "django":
            return [
                "Latest LTS with extended support until 2026",
                "Security updates and bug fixes",
                "Async support for better performance",
                "Strong ORM and admin interface",
                "Batteries-included approach"
            ]
        elif framework == "fastapi":
            return [
                "Modern async Python framework",
                "Automatic OpenAPI documentation",
                "Type validation with Pydantic",
                "High performance (comparable to Node.js/Go)",
                "Growing ecosystem"
            ]
        else:
            return [
                f"Latest stable {framework} version",
                "Modern features and improvements",
                "Active community support"
            ]

    def _assess_framework_migration_complexity(self, framework: str) -> str:
        """Assess framework migration complexity."""
        # Most framework upgrades are MEDIUM complexity
        if framework in ["angular", "django"]:
            return "MEDIUM"
        else:
            return "LOW"

    def _get_framework_alternatives(self, framework: str) -> List[Tuple[str, str]]:
        """Get alternative framework options."""
        if framework in ["flask", "fastapi"]:
            return [
                ("Django 5.0", "More batteries-included, but heavier"),
                ("Flask 3.0", "Lighter weight, but less features"),
            ]
        elif framework == "react":
            return [
                ("Vue 3", "Easier learning curve, similar features"),
                ("Solid.js", "Better performance, smaller bundle"),
            ]
        else:
            return [("Current framework", "If team is productive and satisfied")]

    def _infer_database(self) -> Optional[str]:
        """Infer database from config files."""
        for config_file in self.scan_result.structure.config_files:
            lower = config_file.lower()
            if "postgres" in lower or "pg" in lower:
                return "postgresql"
            elif "mysql" in lower:
                return "mysql"
            elif "mongo" in lower:
                return "mongodb"
            elif "redis" in lower:
                return "redis"

        return None

    def _get_database_rationale(self, database: str, version: str) -> List[str]:
        """Get database-specific rationale."""
        if database == "postgresql":
            return [
                f"Latest LTS version (PostgreSQL {version})",
                "JSONB support for flexible schemas",
                "Excellent performance and reliability",
                "Strong ACID compliance",
                "Active development and community"
            ]
        elif database == "mysql":
            return [
                f"Latest LTS version (MySQL {version})",
                "Wide compatibility and support",
                "Good performance for most workloads",
                "Familiar to most developers"
            ]
        else:
            return [
                f"Latest stable {database} version",
                "Modern features and performance",
                "Active community support"
            ]

    def _assess_database_migration_complexity(self, database: str) -> str:
        """Assess database migration complexity."""
        # Database migrations are typically LOW if schema is compatible
        return "LOW"

    def _get_database_alternatives(self, database: str) -> List[Tuple[str, str]]:
        """Get alternative database options."""
        if database == "postgresql":
            return [
                ("MySQL 8.4 LTS", "More familiar, less feature-rich"),
                ("MongoDB 7.0", "NoSQL flexibility, lose ACID guarantees"),
            ]
        elif database == "mysql":
            return [
                ("PostgreSQL 16", "More features, better JSON support"),
                ("MariaDB 11.2", "MySQL fork with additional features"),
            ]
        else:
            return [("Current database", "If performance and features are adequate")]

    def _calculate_total_complexity(self, recommendations: Dict) -> str:
        """Calculate total migration complexity."""
        complexities = [rec.migration_complexity for rec in recommendations.values() if rec]

        if "HIGH" in complexities:
            return "HIGH"
        elif complexities.count("MEDIUM") >= 2:
            return "MEDIUM-HIGH"
        elif "MEDIUM" in complexities:
            return "MEDIUM"
        else:
            return "LOW"

    def _describe_migration_approach(self, complexity: str) -> str:
        """Describe migration approach based on complexity."""
        if complexity == "HIGH":
            return """**Incremental Migration (Strangler Fig Pattern)**

Due to high complexity, recommend gradual migration:
- Run old and new systems in parallel
- Migrate module by module
- Validate each module before moving to next
- Reduce risk by limiting scope of each change"""
        elif "MEDIUM" in complexity:
            return """**Phased Migration (Module by Module)**

Moderate complexity suggests phased approach:
- Divide system into logical modules
- Migrate 1-2 modules per sprint
- Test thoroughly after each phase
- Maintain parallel testing of old/new"""
        else:
            return """**Big Bang Migration (All at Once)**

Low complexity supports full migration:
- Create new system with modern stack
- Migrate all code in single effort
- Leverage high test coverage for validation
- Deploy when all tests pass"""

    def _estimate_core_effort(self) -> str:
        """Estimate core migration effort."""
        return self._estimate_overall_effort()

    def _describe_core_migration_strategy(self) -> str:
        """Describe core migration strategy."""
        if self.metrics.lines_of_code > 50000:
            return """**Large Codebase Strategy**:
1. Prioritize by business value (critical features first)
2. Migrate 5-10K LOC per sprint
3. Maintain feature parity validation
4. Use automated refactoring tools where possible"""
        else:
            return """**Standard Migration Strategy**:
1. Set up new project structure
2. Migrate utilities and shared code first
3. Migrate business logic module by module
4. Migrate UI/API layer last
5. Validate with existing test suite"""

    def _describe_risk_mitigation(self, complexity: str) -> str:
        """Describe risk mitigation strategies."""
        return f"""**For {complexity} Complexity Migration**:

1. **Feature Flags**: Control rollout of new code
2. **Parallel Running**: Run old and new side-by-side initially
3. **Automated Testing**: Minimum 80% coverage required
4. **Rollback Plan**: Be able to revert within 1 hour
5. **Monitoring**: Track performance, errors, and user experience
6. **Incremental Rollout**: Deploy to 10% → 50% → 100% of users"""

    def _prioritize_component(self, component_type: str) -> str:
        """Prioritize component for migration."""
        if component_type == "Language & Runtime":
            # Check if EOL
            vulnerable = sum(r.vulnerable_count for r in self.dependency_reports)
            if vulnerable > 10:
                return "CRITICAL"
            return "HIGH"
        elif component_type == "Database":
            return "HIGH"
        else:
            return "MEDIUM"

    def _explain_language_complexity(self, complexity: str) -> str:
        """Explain language migration complexity."""
        if complexity == "HIGH":
            return """**Why HIGH?**:
- Major version upgrade with breaking changes
- Significant syntax differences
- Many dependencies need updating
- Extensive testing required

**Effort**: 40-60% of total migration time"""
        elif complexity == "MEDIUM":
            return """**Why MEDIUM?**:
- Minor version upgrade with some breaking changes
- Most syntax compatible
- Some dependency updates needed
- Moderate testing required

**Effort**: 20-30% of total migration time"""
        else:
            return """**Why LOW?**:
- Minor version upgrade, mostly compatible
- Few or no breaking changes
- Dependencies likely compatible
- Limited testing needed

**Effort**: 5-10% of total migration time"""

    def _explain_framework_complexity(self, complexity: str, framework: str) -> str:
        """Explain framework migration complexity."""
        if complexity == "HIGH":
            return f"""**Why HIGH?**:
- {framework} has significant API changes
- Requires architectural adjustments
- Migration guide extensive

**Effort**: 30-40% of total migration time"""
        elif complexity == "MEDIUM":
            return f"""**Why MEDIUM?**:
- {framework} has some breaking changes
- Most patterns still work
- Follow official migration guide

**Effort**: 15-25% of total migration time"""
        else:
            return f"""**Why LOW?**:
- {framework} upgrade mostly compatible
- Deprecation warnings to address
- Straightforward migration

**Effort**: 5-10% of total migration time"""

    def _explain_database_complexity(self, complexity: str) -> str:
        """Explain database migration complexity."""
        return f"""**Why {complexity}?**:
- Schema compatibility: {complexity}
- Data migration tools available
- Testing required: {complexity}

**Effort**: 10-15% of total migration time"""


def main():
    """Example usage of TechStackProposer."""
    print("TechStackProposer module loaded successfully")
    print("This module is called by ReportGenerator during analysis")


if __name__ == "__main__":
    main()
