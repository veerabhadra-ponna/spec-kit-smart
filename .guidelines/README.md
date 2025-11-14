# Corporate Guidelines System

**Version**: 2.0  
**Last Updated**: 2025-01-15

Corporate/organizational guidelines for AI agents implementing Spec-Driven Development with modern technology stacks, cloud-native architectures, and industry best practices.

---

## Overview

This guidelines system provides technology-stack-specific best practices, security requirements, and architectural patterns for AI-driven software development. Guidelines are **principle-based** (defining WHAT and WHY, not HOW) to remain version-agnostic and adaptable across framework versions.

### Key Features

- ✅ **Modern Tech Stacks**: Latest LTS versions (Java 21, .NET 8, Python 3.12, Node.js 20/22, React 18+)
- ✅ **Cloud & On-Premise**: Deployment strategies for Azure, AWS, Kubernetes, self-hosted
- ✅ **Security First**: Authentication, secrets management, input validation, OWASP compliance
- ✅ **Observability**: OpenTelemetry, distributed tracing, metrics, structured logging
- ✅ **Performance**: Caching, connection pooling, async patterns, performance budgets
- ✅ **Compliance**: GDPR, WCAG 2.1 AA accessibility, audit logging, data protection
- ✅ **Framework-Specific**: Auto-detects Next.js, FastAPI, Spring Boot, NestJS, etc.
- ✅ **Monorepo Support**: Workspace detection, per-package guidelines

---

## Hierarchy

Priority order when making decisions:

1. **Constitution** (`/memory/constitution.md`) - **HIGHEST PRIORITY**
2. **Corporate Guidelines** (this directory) - **MEDIUM PRIORITY**
3. **Spec Kit Defaults** - **LOWEST PRIORITY**

**Rule**: Constitution always wins. If constitution says "MUST use PostgreSQL" but guidelines suggest MySQL, use PostgreSQL.

---

## File Structure

```text
.guidelines/
├── README.md                    # This file - system documentation
├── stack-mapping.json           # Multi-stack detection and routing
│
├── # Language-Specific Guidelines (Principle-Based)
├── reactjs-guidelines.md        # React 18+, Next.js 14+, TypeScript 5+
├── java-guidelines.md           # Java 21 LTS, Spring Boot 3.2+
├── dotnet-guidelines.md         # .NET 8 LTS, C# 12, ASP.NET Core
├── nodejs-guidelines.md         # Node.js 20/22 LTS, TypeScript 5+, Express/Fastify
├── python-guidelines.md         # Python 3.11/3.12, FastAPI, Django 5, Flask 3
│
└── # Configuration (Optional)
    └── branch-config.json       # Branch naming (handled by scripts)
```

---

## Technology Stacks

### Supported Stacks (v2.0)

| Stack | Version | Frameworks | Status |
| ------- | --------- | ------------ | -------- |
| **React** | 18+ | Next.js 14+, Vite 5+, Remix | ✅ Active |
| **Java** | 21 LTS | Spring Boot 3.2+, Quarkus, Micronaut | ✅ Active |
| **.NET** | 8 LTS | ASP.NET Core, Blazor, gRPC | ✅ Active |
| **Node.js** | 20/22 LTS | Express 5, Fastify 4, NestJS 10 | ✅ Active |
| **Python** | 3.11/3.12 | FastAPI, Django 5, Flask 3 | ✅ Active |
| **Go** | 1.21+ | Gin, Echo, Fiber | 🚧 Planned |
| **Rust** | Latest | Actix, Rocket, Axum | 🚧 Planned |

### Framework Detection

The system automatically detects specific frameworks within each stack:

**React Ecosystem**:
- Next.js (detects `next.config.js`, App Router vs Pages Router)
- Vite (detects `vite.config.ts`)
- Remix (detects `remix.config.js`)

**Python Ecosystem**:
- FastAPI (detects `fastapi`, `uvicorn` dependencies)
- Django (detects `manage.py`, `INSTALLED_APPS`)
- Flask (detects `Flask(__name__)` patterns)

**Node.js Ecosystem**:
- Express (detects `express` dependency)
- Fastify (detects `fastify` dependency)
- NestJS (detects `nest-cli.json`, `@nestjs/core`)

**Java Ecosystem**:
- Spring Boot (detects `spring-boot-starter`)
- Quarkus (detects `quarkus-` dependencies)
- Micronaut (detects `micronaut-` dependencies)

**.NET Ecosystem**:
- ASP.NET Core (detects `Microsoft.AspNetCore.App`)
- Blazor (detects WebAssembly components)
- .NET MAUI (detects `Microsoft.Maui`)

---

## Auto-Detection System

### Detection Priority (Highest to Lowest)

1. **Explicit Path Mapping** (`stack-mapping.json` paths)
   - Example: `frontend/**/*.ts` → React guidelines

2. **Framework-Specific Markers**
   - Example: `next.config.js` → Next.js-specific React guidelines

3. **Dependency Analysis** (`package.json`, `requirements.txt`, `pom.xml`)
   - Example: `"react": "^18.0.0"` → React guidelines

4. **File Extension**
   - Example: `*.tsx` → React (if no conflicting path)

5. **Directory Convention**
   - Example: `frontend/` → React, `backend/` → Backend stack

6. **Content Analysis** (Last Resort)
   - Analyzes imports and patterns in file content

### Auto-Detection Examples

```bash
# Scenario 1: Monorepo with frontend + backend
apps/
  web/              # Has package.json with "react"
    → React guidelines
  api/              # Has package.json with "express"
    → Node.js guidelines

# Scenario 2: Full-stack Next.js
app/
  (auth)/           # Next.js App Router
    → React guidelines (Server Components)
  api/              # Next.js API routes
    → Node.js guidelines (API behavior)

# Scenario 3: Ambiguous TypeScript file
src/
  utils/
    math.ts         # In frontend/ → React guidelines
                    # In backend/ → Node.js guidelines
                    # In shared/ → Both guidelines apply
```

---

## Multi-Stack Support

### Monorepo Architecture

Automatically detects monorepo tools:
- **Lerna** (`lerna.json`)
- **Nx** (`nx.json`)
- **Turborepo** (`turbo.json`)
- **pnpm Workspaces** (`pnpm-workspace.yaml`)
- **Yarn Workspaces** (`package.json` with `workspaces`)

Guidelines are applied **per workspace/package** based on dependencies and structure.

### Path Precedence Rules

```json
{
  "explicit_beats_implicit": true,
  "path_beats_extension": true,
  "higher_priority_wins": true,
  "framework_specific_wins": true,
  "constitution_beats_all": true
}
```

**Example Conflict Resolution**:

```typescript
// File: frontend/utils/api-client.ts
// Matches: 
//   - frontend/** (React, priority 10)
//   - *.ts (Node.js, priority 5)
// Winner: React guidelines (path beats extension, higher priority)
```

---

## Guideline Structure

### Principle-Based Format

**Philosophy**: Guidelines define **WHAT** and **WHY**, not **HOW**.

AI agents adapt principles to the target language/framework version, preventing:
- ❌ Build errors from outdated syntax
- ❌ Version incompatibilities (React 16 vs 18, .NET 6 vs 8)
- ❌ Stale code examples that don't match project setup

**Format**:

```markdown
### Category

**MUST** use: `@YOUR_ORG/package-name` package
**Requirements**:
- Requirement stated as principle (no code)
- Another principle-based requirement

**Features**: Auto-included features, benefits

**NEVER**:
- Prohibited action or library
```

### Requirement Keywords (RFC 2119 Style)

- **MUST**: Mandatory requirement (non-compliance requires documentation)
- **MUST NOT** / **NEVER**: Prohibited (security, compliance, or architectural reasons)
- **SHOULD**: Recommended (deviation acceptable with justification)
- **SHOULD NOT**: Not recommended (deviation acceptable with justification)
- **MAY**: Optional (discretionary)

---

## Version Management

### Guideline Versioning

Each guideline file includes version metadata:

```markdown
**Version**: 2.0
**Last Updated**: 2025-01-15
```

Configuration files include:

```json
{
  "version": "2.0",
  "last_updated": "2025-01-15"
}
```

### Technology Version Support

Guidelines specify **target versions**:

| Stack | Target Version | LTS Until | Next LTS |
| ------- | --------------- | ----------- | ---------- |
| Java | 21 LTS | Sep 2028 | Sep 2025 (Java 23 LTS) |
| .NET | 8 LTS | Nov 2026 | Nov 2025 (.NET 10 LTS) |
| Node.js | 20 LTS | Apr 2026 | Oct 2024 (Node.js 22 LTS) |
| Python | 3.12 | Oct 2028 | Oct 2025 (Python 3.13) |
| React | 18.2+ | Ongoing | 2025 (React 19) |

---

## Customization

### Replacing Placeholders

**Find and replace** across all `*-guidelines.md` files:

| Placeholder | Replace With |
| ------------- | -------------- |
| `@YOUR_ORG` | Your organization's package scope (e.g., `@acmecorp`) |
| `YOUR_ORG` | Your organization name (e.g., `acmecorp`) |
| `YOUR_DOMAIN` | Your organization domain (e.g., `acmecorp.com`) |

### Adding New Stacks

1. Create `{stack}-guidelines.md` following principle-based format
2. Add stack entry to `stack-mapping.json`:

```json
{
  "name": "rust",
  "guideline": "rust-guidelines.md",
  "paths": ["backend/**", "services/**"],
  "extensions": [".rs"],
  "markers": ["Cargo.toml"],
  "priority": 10
}
```

1. Update `README.md` with stack information

### Custom Path Mappings

Edit `stack-mapping.json` to add project-specific paths:

```json
{
  "stacks": [
    {
      "name": "reactjs",
      "paths": [
        "frontend/**",
        "client/**",
        "web/**",           // Add custom path
        "apps/storefront/**" // Monorepo-specific
      ]
    }
  ]
}
```

---

## Usage for AI Agents

### Loading Guidelines

**Decision Tree**:

```text
1. Is there a Constitution? 
   → YES: Load constitution (highest priority)
   → NO: Continue

2. Detect project structure:
   → Monorepo? Load per workspace
   → Single project? Load for entire project

3. For each file/directory:
   → Check explicit path mappings in stack-mapping.json
   → Check framework-specific markers
   → Check dependency markers
   → Check file extensions
   → Fall back to content analysis

4. Apply precedence rules to resolve conflicts

5. Load applicable guideline(s) and apply principles
```

### Principle Application

**When analyzing code**:

1. ✅ **Extract principles** from guidelines (MUST, SHOULD, NEVER)
2. ✅ **Adapt to project version** (React 18 vs 19, Java 17 vs 21)
3. ✅ **Apply contextually** (cloud vs on-premise, dev vs prod)
4. ❌ **Don't copy code examples verbatim** (guidelines don't include them)
5. ❌ **Don't apply outdated patterns** (adapt to target version)

**Example Adaptation**:

```text
Guideline Principle:
"MUST use async/await for all I/O operations"

✅ Java 21 (Virtual Threads):
Use virtual threads for high-concurrency I/O

✅ Python 3.11 (AsyncIO):
Use async/await with asyncio for non-blocking I/O

✅ Node.js 20 (Native Async):
Use async/await with proper error handling
```

### Non-Compliance Handling

When a guideline cannot be followed:

1. **Document** violation in `.guidelines-todo.md`:

```markdown
# Guideline Violations

## Node.js: Cannot use corporate HTTP client

**Guideline**: MUST use @YOUR_ORG/api-client
**Actual**: Using axios directly
**Reason**: Corporate package not compatible with Node.js 22
**Ticket**: TECH-1234
**Target Resolution**: Sprint 24
**Workaround**: Wrapped axios with retry logic and logging
```

1. **Mark in code** with tracking comment:

```typescript
// TODO: GUIDELINE-VIOLATION - Ticket #TECH-1234
// Using axios directly until @YOUR_ORG/api-client supports Node 22
import axios from 'axios';
```

1. **Create ticket** for resolution (target: next sprint)
1. **Schedule review** within 30 days

---

## Constitution vs Guidelines

### Constitution (`/memory/constitution.md`)

- **Purpose**: Project-specific principles and architectural decisions
- **Priority**: HIGHEST (overrides all guidelines)
- **Change Process**: Requires team vote or architect approval
- **Examples**:
  - "MUST use PostgreSQL for all databases"
  - "MUST use event-driven architecture for service communication"
  - "MUST support offline-first mobile experience"

### Corporate Guidelines (This Directory)

- **Purpose**: Organization-wide technology standards
- **Priority**: MEDIUM (overrides spec kit defaults)
- **Change Process**: Updated as standards evolve
- **Examples**:
  - "MUST use corporate authentication library"
  - "MUST log to corporate Elasticsearch cluster"
  - "SHOULD use corporate UI component library"

### Spec Kit Defaults

- **Purpose**: General best practices and fallback guidance
- **Priority**: LOWEST
- **Change Process**: Updated with spec kit releases
- **Examples**:
  - "SHOULD write unit tests for business logic"
  - "SHOULD use semantic versioning"
  - "SHOULD document public APIs"

---

## Best Practices

### For Teams

1. **Review Guidelines Quarterly**: Update for new LTS versions, security patches
2. **Customize Thoughtfully**: Add organization-specific requirements in moderation
3. **Document Exceptions**: Use `.guidelines-todo.md` for tracking deviations
4. **Share Learnings**: Feed real-world issues back to guideline improvements
5. **Version Lock**: Reference specific guideline version in project docs

### For AI Agents

1. **Load Once, Cache**: Parse guidelines at start, cache decisions per file/directory
2. **Respect Hierarchy**: Constitution > Guidelines > Defaults
3. **Be Version-Aware**: Detect project versions, adapt syntax accordingly
4. **Handle Conflicts**: Use precedence rules, document ambiguous cases
5. **Stay Current**: Check for guideline updates, flag outdated patterns

### For Developers

1. **Read Relevant Guidelines**: Familiarize yourself with applicable stack guidelines
2. **Question Thoughtfully**: Guidelines are principles, not absolute rules
3. **Propose Improvements**: Submit PRs for guideline enhancements
4. **Track Violations**: Use `.guidelines-todo.md` for transparency
5. **Educate Team**: Share guideline updates during tech talks

---

## Advanced Features

### Framework-Specific Guidance

Guidelines adapt based on detected framework:

```json
{
  "framework_detection": {
    "nextjs": {
      "markers": ["next.config.js"],
      "guidance": "Use Server Components by default, 'use client' when needed"
    },
    "django": {
      "markers": ["manage.py"],
      "guidance": "Use Django ORM with migrations, not raw SQL"
    }
  }
}
```

### Version-Specific Adaptations

Guidelines provide version-aware recommendations:

```json
{
  "version_detection": {
    "react": {
      "18.x": "Use concurrent features, automatic batching",
      "19.x": "Use React Compiler, new hooks (use, useFormStatus)"
    }
  }
}
```

### Special Case Handling

Guidelines cover complex scenarios:

- **Full-Stack Apps**: Both frontend + backend in one repo
- **Microfrontends**: Module federation, independent deployment
- **Serverless**: AWS Lambda, Azure Functions patterns
- **Mobile**: React Native, Flutter, native integration

---

## Migration Guide

### Upgrading from v1.0 to v2.0

**Major Changes**:

1. **Language Versions Updated**:
   - Java: 17 → 21 LTS
   - .NET: 6 → 8 LTS
   - Python: 3.10 → 3.12
   - Node.js: 18 → 20/22 LTS
   - React: 17 → 18+

2. **New Framework Support**:
   - Next.js 14+ App Router
   - FastAPI async patterns
   - Spring Boot 3.2+ native images
   - .NET 8 Blazor enhancements

3. **Enhanced Security**:
   - Secrets management expanded
   - mTLS support documented
   - Security headers mandated
   - OWASP Top 10 coverage

4. **Cloud-Native Focus**:
   - Azure/AWS deployment patterns
   - Kubernetes best practices
   - Observability with OpenTelemetry
   - Service mesh integration

**Migration Steps**:

1. **Review Dependencies**: Update to supported LTS versions
2. **Check Deprecations**: Remove banned libraries (CRA, moment.js, etc.)
3. **Update Patterns**: Adopt async patterns, server components
4. **Test Thoroughly**: Run full test suite after guideline updates
5. **Document Changes**: Update project docs with new patterns

---

## Troubleshooting

### Common Issues

**Issue**: AI applies wrong guidelines to file  
**Solution**: Check `stack-mapping.json` path precedence, add explicit mapping

**Issue**: Guidelines conflict with constitution  
**Solution**: Constitution always wins, document in `.guidelines-todo.md`

**Issue**: Corporate package not available  
**Solution**: Follow non-compliance process, use alternative, create ticket

**Issue**: Multiple stacks detected for same file  
**Solution**: Review `precedence_rules` in `stack-mapping.json`, add exclusion

**Issue**: Framework not detected  
**Solution**: Add framework markers to `framework_detection` in `stack-mapping.json`

---

## Contributing

### Proposing Guideline Changes

1. **Fork Repository**: Create feature branch (`feature/improve-react-security`)
2. **Make Changes**: Update guidelines with clear rationale
3. **Test Impact**: Validate against sample projects
4. **Submit PR**: Include justification, examples, migration notes
5. **Review Process**: Tech leads review, approve, merge

### Guideline Quality Checklist

- [ ] Principle-based (WHAT/WHY, not HOW)
- [ ] Version-agnostic (works across minor versions)
- [ ] Security-focused (OWASP, input validation, secrets)
- [ ] Cloud + on-premise coverage
- [ ] RFC 2119 keywords (MUST, SHOULD, MAY)
- [ ] Rationale provided for requirements
- [ ] Examples use placeholders (@YOUR_ORG)
- [ ] Non-compliance process documented

---

## References

### External Standards

- **OWASP Top 10**: <https://owasp.org/www-project-top-ten/>
- **WCAG 2.1**: <https://www.w3.org/WAI/WCAG21/quickref/>
- **GDPR**: <https://gdpr.eu/>
- **RFC 2119** (Requirement Levels): <https://www.rfc-editor.org/rfc/rfc2119>
- **OpenTelemetry**: <https://opentelemetry.io/>
- **12-Factor App**: <https://12factor.net/>

### Framework Documentation

- **React**: <https://react.dev/>
- **Next.js**: <https://nextjs.org/docs>
- **Spring Boot**: <https://spring.io/projects/spring-boot>
- **FastAPI**: <https://fastapi.tiangolo.com/>
- **.NET**: <https://learn.microsoft.com/en-us/dotnet/>

---

## Changelog

### Version 2.0 (2025-01-15)

**Added**:
- ✨ Next.js 14+ App Router support
- ✨ React Server Components guidance
- ✨ Java 21 LTS with virtual threads
- ✨ Python 3.12 with performance improvements
- ✨ .NET 8 LTS features
- ✨ Node.js 20/22 LTS support
- ✨ Framework-specific detection (Next.js, FastAPI, Spring Boot)
- ✨ Monorepo support (Nx, Turborepo, pnpm workspaces)
- ✨ Cloud-native deployment patterns (Azure, AWS, Kubernetes)
- ✨ OpenTelemetry distributed tracing
- ✨ Version detection system

**Changed**:
- 🔄 All guidelines updated to latest LTS versions
- 🔄 Enhanced security sections (secrets, mTLS, headers)
- 🔄 Improved observability guidance (metrics, logging, tracing)
- 🔄 Expanded performance optimization sections
- 🔄 Updated testing frameworks (Vitest, Playwright, Testcontainers)

**Deprecated**:
- ⚠️ Create React App (unmaintained)
- ⚠️ Log4j 1.x (security vulnerabilities)
- ⚠️ moment.js (discontinued, use date-fns/dayjs)

**Removed**:
- ❌ Code examples (principle-based approach)
- ❌ Version-specific syntax (adaptable to any version)

### Version 1.0 (2024-01-01)

- 🎉 Initial release
- Basic guidelines for React, Java, .NET, Node.js, Python

---

## License

Copyright © 2025 Your Organization. All rights reserved.

**Usage**: Internal use only. Do not distribute outside organization without approval.

---

## Support

**Questions?** Contact the Architecture Team:
- **Email**: <architecture@yourorg.com>
- **Slack**: #guidelines-support
- **Wiki**: <https://wiki.yourorg.com/guidelines>

**Issues?** File a ticket:
- **Jira Project**: GUIDELINES
- **GitHub Issues**: (if applicable)
