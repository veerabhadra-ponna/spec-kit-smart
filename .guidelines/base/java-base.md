# Java Base Guidelines

**Tech Stack**: Java 21 LTS, Spring Boot 3.2+, Maven/Gradle, Backend Services, Microservices
**Auto-detected from**: `pom.xml`, `build.gradle`, or `build.gradle.kts`
**Version**: 3.0 (Profile-Based Architecture)
**Last Updated**: 2025-11-16

---

## Target Platform

**MUST**:

- Use Java 21 LTS (Long-Term Support until September 2028)
- Use Spring Boot 3.2+ for new projects
- Use Maven 3.9+ or Gradle 8.5+

**Rationale**: Java 21 LTS provides long-term support and modern features (virtual threads, pattern matching, records)

---

## Framework Selection

**Spring Boot 3.2+**: Enterprise-grade, comprehensive ecosystem (recommended)
**Quarkus 3.x**: Cloud-native, fast startup, low memory
**Micronaut 4.x**: Lightweight, compile-time DI, fast startup

---

## Architecture & Best Practices

- Follow SOLID principles
- Use dependency injection (Spring, CDI)
- Implement layered architecture (Controller → Service → Repository)
- Use DTOs for API contracts
- Implement comprehensive error handling
- Use proper exception hierarchy

---

## Security

- Validate all inputs
- Use parameterized queries (prevent SQL injection)
- Implement authentication and authorization
- Use BCrypt for password hashing
- Configure CORS properly
- Enable HTTPS in production

---

## Testing

- Unit tests with JUnit 5
- Integration tests with Spring Boot Test
- Aim for 80%+ code coverage
- Use mocking frameworks (Mockito, MockMvc)

---

## Database

- Use JPA/Hibernate for ORM
- Implement proper transaction management
- Use connection pooling (HikariCP)
- Write migrations (Flyway, Liquibase)

---

**Note**: This is a base guideline. Full content migration from `archive/java-guidelines.md` in progress. Project-specific requirements (corporate libraries, registries) are defined in profile overrides.

**TODO**: Expand with full content from archived guideline including: logging, monitoring, deployment, coding standards, performance optimization, and detailed framework guides.
