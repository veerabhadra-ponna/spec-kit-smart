# Java Corporate Profile Overrides

**Profile**: Corporate
**Stack**: Java
**Version**: 3.0
**Last Updated**: 2025-11-16

> **Note**: This file contains only corporate-specific overrides. Base guidelines are inherited from `base/java-base.md`.

---

## Scaffolding

**MUST**: Use `@YOUR_ORG/spring-boot-starter` or corporate archetypes

## Package Registry

**MUST**: Configure Maven/Gradle to use corporate Artifactory/Nexus

```xml
<!-- settings.xml -->
<mirrors>
  <mirror>
    <id>corporate-maven</id>
    <url>https://maven.yourorg.com/repository/maven-public</url>
    <mirrorOf>*</mirrorOf>
  </mirror>
</mirrors>
```

## Mandatory Libraries

- **Framework**: `@YOUR_ORG/spring-boot-starter-parent`
- **Authentication**: `@YOUR_ORG/security-starter`
- **Logging**: `@YOUR_ORG/logging-starter`
- **Metrics**: `@YOUR_ORG/metrics-starter`
- **Database**: `@YOUR_ORG/data-jpa-starter`

## Deployment

- Corporate Kubernetes clusters
- CI/CD via Jenkins/Azure DevOps
- Docker images in corporate registry

**Note**: Full content migration in progress. See `archive/java-guidelines.md` for complete corporate requirements.
