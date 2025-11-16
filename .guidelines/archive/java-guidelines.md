# Java Corporate Guidelines

**Tech Stack**: Java 21 LTS, Spring Boot 3.2+, Spring Framework 6.1+, Backend Services, Microservices, APIs
**Auto-detected from**: `pom.xml`, `build.gradle`, or `*.java` files
**Version**: 2.0
**Last Updated**: 2025-01-15

---

## Target Platform

**MUST**:

- Use Java 21 (LTS - Long Term Support until September 2028)
- Target Java 21 in build configuration (`java.version` property)
- Use Spring Boot 3.2+ (requires Java 17 minimum)

**SHOULD**:

- Adopt virtual threads (Project Loom) for high-concurrency scenarios
- Use pattern matching and records for cleaner code
- Leverage sequenced collections (Java 21)

**Rationale**: Java 21 provides 8 years of support, significant performance improvements, and modern language features

---

## Scaffolding

**MUST**:

- Use corporate scaffolding command (`@YOUR_ORG/create-spring-app`)
- Choose appropriate template:
  - **microservice**: Standard REST API with Spring Boot
  - **reactive**: WebFlux-based reactive services
  - **batch**: Spring Batch for data processing
  - **grpc**: gRPC service template
  - **event-driven**: Kafka/RabbitMQ consumer/producer

**NEVER**:

- Use public Spring Initializr (`https://start.spring.io`) without approval

**Alternative**: Internal Spring Initializr at `https://spring-init.YOUR_DOMAIN.com` with corporate defaults

**Rationale**: Corporate scaffolding includes security, logging, monitoring, compliance, observability from day one

---

## Build Tools

**MUST** choose one:

- **Maven 3.9+**: For established projects, enterprise compatibility
- **Gradle 8.5+**: For modern projects, faster builds, better dependency management

**SHOULD**:

- Use Gradle for new projects (better performance, flexibility)
- Use Maven wrapper (`mvnw`) or Gradle wrapper (`gradlew`) for consistent builds
- Define dependency versions in BOM (Bill of Materials) or platform

**NEVER**:

- Mix Maven and Gradle in same repository
- Commit build artifacts (target/, build/) to version control

---

## Package Registry

**MUST**:

- Configure Maven/Gradle with corporate artifact repository (Artifactory, Nexus, Azure Artifacts)
- All dependencies resolved through corporate repository only
- Authenticate via `~/.m2/settings.xml` or `~/.gradle/gradle.properties`
- Use encrypted passwords or tokens (never plaintext)

**NEVER**:

- Download packages from public Maven Central directly without security scanning

**Configuration**:

- Maven: Configure mirrors in `settings.xml`
- Gradle: Configure repositories in `build.gradle` or `settings.gradle`
- Use credential helpers for secure authentication

---

## Mandatory Libraries

### Spring Boot Starter

**MUST** use: Corporate Spring Boot parent POM (`YOUR_ORG-spring-boot-starter-parent`) or BOM
**MUST** use: `YOUR_ORG-spring-boot-starter-web` for web applications
**Includes**: Security, logging, monitoring, health checks, exception handling, CORS, observability

**Starter Variants**:

- **web**: Spring MVC REST APIs
- **webflux**: Reactive REST APIs with Project Reactor
- **data-jpa**: Spring Data JPA for relational databases
- **data-mongodb**: Spring Data MongoDB
- **data-redis**: Redis integration
- **amqp**: RabbitMQ messaging
- **kafka**: Apache Kafka integration
- **batch**: Spring Batch for ETL jobs
- **security**: OAuth2, JWT, Spring Security

### Security & Authentication

**MUST** use: `YOUR_ORG-security-spring-boot-starter` package
**Requirements**:

- Decorate endpoints with `@SecuredEndpoint(roles = {...})` annotation
- Extract authenticated user via `SecurityContextHolder.getCurrentUser()`
- Pass user context to all service layer calls
- Support OAuth 2.0 Resource Server, JWT bearer tokens, OpenID Connect

**Advanced Features**:

- Multi-tenant authentication with tenant isolation
- API key authentication for service-to-service communication
- Certificate-based mutual TLS (mTLS) for high-security scenarios
- Method-level security with `@PreAuthorize`, `@PostAuthorize`
- Dynamic role evaluation with SpEL expressions

**Cloud-Specific**:

- Azure AD / Entra ID integration
- AWS Cognito integration
- Google Identity Platform support

**On-Premise**:

- LDAP/Active Directory integration
- SAML 2.0 SSO with corporate identity provider
- Custom JWT token validation

### API Client & Resilience

**MUST** use: `YOUR_ORG-api-client` package (wraps Spring Cloud OpenFeign or WebClient)
**Requirements**:

- Inject `ApiClient<T>` for external service calls
- Use `@CircuitBreaker` annotation with fallback methods (Resilience4j integration)
- Never create RestTemplate, RestClient, or WebClient manually
- All external calls auto-instrumented for distributed tracing (Micrometer Tracing)

**Features**:

- Service discovery integration (Eureka, Consul, Kubernetes)
- Load balancing with Spring Cloud LoadBalancer
- Circuit breaker patterns (open, half-open, closed states)
- Bulkhead isolation for fault tolerance
- Rate limiting for outbound requests
- Retry with exponential backoff and jitter
- Timeout handling with graceful degradation

**Reactive Support**:

- WebClient for reactive applications (non-blocking I/O)
- Reactive circuit breakers with Project Reactor

**Cloud-Specific**:

- Azure Service Bus for reliable messaging
- AWS SQS/SNS with Spring Cloud AWS

**On-Premise**:

- RabbitMQ with Spring AMQP (guaranteed delivery)
- Apache Kafka with Spring Kafka (exactly-once semantics)

### Database - Spring Data JPA

**MUST** use: Spring Data JPA 3.2+ with `YOUR_ORG-jpa-extensions`
**Requirements**:

- Entities extend `AuditedEntity` for automatic audit trail (createdBy, createdAt, lastModifiedBy, lastModifiedAt, version)
- Use repositories extending `JpaRepository` or `CrudRepository`
- Use Flyway or Liquibase for database migrations
- Enable second-level cache (Hibernate + Redis/Ehcache) for read-heavy workloads
- Use `@EntityGraph` or fetch joins to avoid N+1 queries

**Advanced Features**:

- Projections for optimized queries (interface-based, DTO-based)
- Specifications for dynamic query building
- Query by Example (QBE) for simple filtering
- Auditing with `@CreatedBy`, `@LastModifiedBy` (Spring Data JPA)
- Soft deletes with `@Where` annotation
- Optimistic locking with `@Version`

**Supported Databases**:

- PostgreSQL 14+ (cloud: Azure Database, AWS RDS, on-premise)
- MySQL 8+ / MariaDB 10.6+ (cloud: Azure, AWS, on-premise)
- Oracle 19c+ (on-premise, Oracle Cloud)
- SQL Server 2019+ (cloud: Azure SQL, on-premise)
- H2 (in-memory for testing only)

**Cloud-Specific**:

- Azure SQL Database with managed identity authentication
- AWS RDS with IAM authentication
- Connection pooling optimized for cloud environments (HikariCP)

### Database - jOOQ (Type-Safe SQL)

**MAY** use: jOOQ 3.18+ with `YOUR_ORG-jooq-extensions` for complex SQL scenarios
**Use Cases**:

- Complex reporting queries with joins, CTEs, window functions
- Legacy database integration with complex stored procedures
- Performance-critical queries requiring SQL optimization
- Type-safe SQL generation from schema

**Requirements**:

- Generate jOOQ classes from database schema
- Use parameterized queries exclusively (SQL injection prevention)
- Apply same audit patterns as Spring Data JPA
- Document why jOOQ chosen over Spring Data JPA

### Database - MongoDB

**SHOULD** use: Spring Data MongoDB 4.2+ for NoSQL workloads
**Requirements**:

- Use repositories extending `MongoRepository`
- Define document models with `@Document` annotation
- Use aggregation pipeline for complex queries
- Implement proper indexing strategy

**Cloud-Specific**:

- Azure Cosmos DB (MongoDB API)
- AWS DocumentDB (MongoDB-compatible)
- MongoDB Atlas

**On-Premise**:

- MongoDB 6.0+ with replica sets for high availability
- Sharding for horizontal scalability

### Caching

**MUST** use: Spring Cache abstraction with `YOUR_ORG-cache-extensions`
**Requirements**:

- Use `@Cacheable`, `@CachePut`, `@CacheEvict` annotations
- Use distributed cache (Redis, Hazelcast) for multi-instance deployments
- Use local cache (Caffeine) only for single-instance or read-only data
- Implement cache-aside pattern with appropriate TTL
- Use cache invalidation strategies (time-based, event-based, manual)

**Cloud-Specific**:

- Azure Cache for Redis (managed)
- AWS ElastiCache for Redis (managed)

**On-Premise**:

- Redis 7+ with Sentinel/Cluster for high availability
- Hazelcast for embedded distributed cache

### Logging & Observability

**MUST** use: SLF4J 2.0+ + Logback 1.4+ (included in Spring Boot starter)
**Requirements**:

- Use `@Slf4j` annotation (Lombok) or inject `Logger` via constructor
- Use structured logging with MDC (Mapped Diagnostic Context) for correlation IDs
- Use `@LogExecution` annotation for method-level logging with aspect-oriented programming
- Export logs to corporate logging platform (Elasticsearch, Splunk, Azure Monitor, AWS CloudWatch)

**Log Levels**:

- **TRACE**: Detailed diagnostic information (disabled in production)
- **DEBUG**: Development debugging (disabled in production)
- **INFO**: General informational messages
- **WARN**: Unexpected behavior that doesn't prevent operation
- **ERROR**: Errors requiring investigation
- **FATAL**: System failures requiring immediate attention

**NEVER**:

- Use `System.out.println()` or `System.err.println()` for logging
- Log PII, secrets, passwords, authentication tokens, credit card numbers, SSNs
- Log entire request/response bodies without sanitization

**Distributed Tracing**:

- Enable Micrometer Tracing (OpenTelemetry) for HTTP, database, messaging
- Export traces to Zipkin, Jaeger, Azure Application Insights, AWS X-Ray
- Use TraceId and SpanId for request correlation
- Implement trace sampling strategies for high-throughput systems

**Structured Logging**:

- Use Logstash Encoder for JSON logging format
- Include contextual information (userId, tenantId, requestId, operation)
- Use log aggregation tools (ELK Stack, Splunk, Datadog)

### Validation

**MUST** use: Jakarta Bean Validation 3.0+ (Hibernate Validator) with `YOUR_ORG-validators`
**Requirements**:

- Use `@Valid` or `@Validated` annotation on request objects
- Define validation rules using Jakarta annotations (`@NotBlank`, `@Email`, `@Pattern`, etc.)
- Use custom corporate validators (e.g., `@ValidCorporateEmail`, `@ValidPhoneNumber`)
- Return structured validation errors (field-level details)

**Advanced Patterns**:

- Validation groups for context-specific validation
- Cross-field validation with custom validators
- Conditional validation based on business rules
- Async validation for database uniqueness checks

### Background Jobs & Scheduling

**MUST** use: Spring @Scheduled or `YOUR_ORG-scheduler` for periodic tasks
**SHOULD** use: Spring Batch 5.0+ for complex batch processing
**MAY** use: Quartz Scheduler for advanced scheduling (cron, triggers, persistence)

**Requirements**:

- Use persistent job store (database) for critical jobs
- Implement idempotent job handlers (support retries)
- Use job execution logs and monitoring
- Support distributed job execution (only one instance executes)

**Use Cases**:

- Scheduled report generation
- Data synchronization and ETL
- Cleanup jobs (old data, expired sessions)
- Batch processing of large datasets

**Cloud-Specific**:

- Azure Functions with Durable Functions
- AWS Lambda with EventBridge Scheduler
- Spring Cloud Data Flow for orchestration

**On-Premise**:

- Spring Batch with RDBMS for job repository
- Quartz Scheduler with clustering support

### API Documentation

**MUST**:

- Use SpringDoc OpenAPI 2.3+ (Swagger 3.0 / OpenAPI 3.1)
- Generate OpenAPI/Swagger documentation automatically from code
- Use `@Operation`, `@ApiResponse` annotations for endpoint descriptions
- Include request/response examples with `@Schema` annotations
- Document error responses and status codes

**Requirements**:

- Expose Swagger UI at `/swagger-ui.html` (development only)
- Export OpenAPI spec at `/v3/api-docs` for API gateway registration
- Version APIs explicitly (URL versioning `/api/v1/...` or header-based)
- Group endpoints by domain/feature with tags

---

## Banned Libraries

**NEVER** use:

- Apache HttpClient, OkHttp directly → Use Spring WebClient or `YOUR_ORG-api-client`
- Log4j 1.x (security vulnerabilities) → Use SLF4J + Logback
- `java.util.logging` (JUL) → Use SLF4J facade
- `System.out.println()` or `printStackTrace()` → Use proper logging
- Date/Time classes from `java.util.Date` → Use `java.time` API (JSR-310)
- Apache Commons Lang 2.x → Use Apache Commons Lang 3.x or Java standard library

**Deprecated Spring Components**:

- `RestTemplate` → Use `RestClient` (Spring 6.1+) or `WebClient` (reactive)
- `AsyncRestTemplate` → Use `WebClient`
- Spring Cloud Netflix (Eureka, Hystrix) → Use Spring Cloud LoadBalancer, Resilience4j

**Rationale**: Corporate libraries enforce security, observability, compliance; deprecated libraries lack support

---

## Architecture

### Project Structure - Hexagonal Architecture (Recommended)

**SHOULD** use: Ports and Adapters (Hexagonal Architecture) for better testability

- **domain/**: Core business logic (entities, value objects, domain services)
- **application/**: Application services, use cases, DTOs
- **adapter/**: External interfaces
  - **web/**: REST controllers, GraphQL resolvers
  - **persistence/**: JPA repositories, database adapters
  - **messaging/**: Kafka consumers/producers, RabbitMQ listeners
- **config/**: Configuration classes, beans, properties

**Benefits**: Clear boundaries, testable core logic, framework independence

### Project Structure - Traditional Layered (Acceptable)

**MAY** use: Layered architecture for large, established codebases

- **Controller**: REST endpoints, request/response handling, validation
- **Service**: Business logic layer, orchestration
- **Repository**: Data access layer (Spring Data JPA, MongoDB)
- **Model/Entity**: Domain models, database entities, value objects
- **DTO**: Data transfer objects for API contracts, mappers

**Package Organization**:

- **Feature-based** (preferred): `com.yourorg.orders`, `com.yourorg.users`
- **Layer-based**: `com.yourorg.controller`, `com.yourorg.service`, `com.yourorg.repository`

### Separation of Concerns

**MUST**:

- Keep controllers thin (routing, validation, response formatting only)
- Put business logic in service layer or domain services
- Use repository interfaces for database access
- Never put business logic in controllers or repositories
- Use mapper classes or MapStruct for DTO-entity conversion

### API Patterns

**SHOULD** choose based on use case:

- **REST**: Standard CRUD operations, public APIs (Spring MVC)
- **GraphQL**: Complex data fetching, mobile APIs (Spring for GraphQL)
- **gRPC**: High-performance inter-service communication (gRPC-Spring-Boot-Starter)
- **WebSockets**: Real-time bidirectional communication (Spring WebSocket, STOMP)
- **Server-Sent Events (SSE)**: Unidirectional real-time updates

### DTOs vs Entities

**MUST**:

- Use separate DTOs for API contracts (never expose entities directly)
- Keep sensitive fields (passwordHash, internalId, auditFields) in entities only
- Use Java records for immutable DTOs (Java 16+)
- Implement mapping explicitly or use MapStruct (compile-time type-safe mapping)

**Pattern**:

- Request DTOs for input validation
- Response DTOs for output serialization
- Internal DTOs for service-to-service communication

### Exception Handling

**MUST**:

- Use `@RestControllerAdvice` or `@ControllerAdvice` for centralized exception handling
- Map domain exceptions to appropriate HTTP status codes
- Return RFC 7807 ProblemDetail responses (Spring 6+)
- Return generic error messages to clients (no internal details, stack traces)
- Log full exception details server-side with stack traces and correlation IDs

**Status Code Mapping**:

- ValidationException → 400 Bad Request
- AuthenticationException → 401 Unauthorized
- AccessDeniedException → 403 Forbidden
- ResourceNotFoundException → 404 Not Found
- ConflictException → 409 Conflict
- BusinessException → 422 Unprocessable Entity
- InfrastructureException → 500 Internal Server Error
- ServiceUnavailableException → 503 Service Unavailable

---

## Security

### Input Validation

**MUST**:

- Validate all API inputs using `@Valid` or `@Validated` annotation
- Return 400 Bad Request with structured errors for validation failures
- Reject requests before reaching business logic
- Validate file uploads (type, size, content, virus scan)
- Sanitize HTML inputs to prevent XSS attacks

### SQL Injection Prevention

**MUST**:

- Use Spring Data JPA or jOOQ (parameterized queries automatic)
- Use `@Query` annotation with named parameters (`:paramName`) or positional (`?1`)
- Never concatenate strings for SQL queries
- Use `Pageable` and `Sort` from Spring Data (injection-safe)

### Secrets Management

**MUST**:

- Store secrets in corporate secrets manager, Azure Key Vault, AWS Secrets Manager, or HashiCorp Vault
- Access secrets via Spring's `@Value` annotation, `Environment`, or Spring Cloud Config
- Use Spring Cloud Config for centralized configuration management
- Rotate secrets regularly (automated via secret manager)

**NEVER**:

- Hardcode secrets in code or application.properties/yml
- Commit secrets to source control
- Store secrets in plain text environment variables (production)

**Configuration Hierarchy** (lowest to highest priority):

1. application.properties/yml (defaults, non-sensitive)
2. Profile-specific files (application-{profile}.properties)
3. Environment variables
4. Cloud config server (Spring Cloud Config)
5. Azure Key Vault / AWS Secrets Manager / HashiCorp Vault (production)

**Cloud-Specific**:

- Use Managed Identities (Azure) or IAM Roles (AWS) for authentication
- Spring Cloud Azure / Spring Cloud AWS for seamless integration

### Authentication & Authorization

**MUST**:

- Validate user roles before resource access
- Use `@SecuredEndpoint` annotation or `@PreAuthorize` on all protected endpoints
- Implement principle of least privilege
- Use role-based access control (RBAC) or claims-based authorization
- Support multi-factor authentication (MFA) for sensitive operations

**Spring Security Configuration**:

- Use `SecurityFilterChain` bean (modern approach, not `WebSecurityConfigurerAdapter`)
- Configure OAuth2 Resource Server for JWT validation
- Implement custom authentication providers for legacy systems
- Use method security with `@EnableMethodSecurity`

**Cloud-Specific**:

- Azure AD / Entra ID with Spring Boot Starter
- AWS Cognito with Spring Security
- Integrate with corporate SSO (SAML, OIDC)

**On-Premise**:

- LDAP/Active Directory integration
- Custom JWT-based authentication with refresh tokens
- Session management with Redis for distributed sessions

### API Security

**MUST**:

- Implement rate limiting per user/IP (Bucket4j, Spring Cloud Gateway)
- Use API versioning for backward compatibility
- Implement CORS policies restrictively
- Validate content-type headers (`application/json` only for JSON APIs)
- Implement request size limits (prevent DoS attacks)
- Use HTTPS exclusively (enforce Strict-Transport-Security header)
- Implement CSRF protection for stateful applications

### Security Headers

**MUST** include (Spring Security auto-configures many):

- Content-Security-Policy (CSP)
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY or SAMEORIGIN
- X-XSS-Protection: 0 (modern browsers rely on CSP)
- Strict-Transport-Security (HSTS)
- Referrer-Policy: no-referrer or strict-origin-when-cross-origin
- Permissions-Policy (formerly Feature-Policy)

---

## Coding Standards

### Java Version & Modern Features

**MUST**:

- Use Java 21 (LTS version)
- Enable preview features cautiously (`--enable-preview` flag)

**SHOULD** use modern Java features:

- **Records** (Java 16+): Immutable data carriers
- **Sealed Classes** (Java 17+): Restricted inheritance hierarchies
- **Pattern Matching** (Java 21): instanceof patterns, switch expressions
- **Text Blocks** (Java 15+): Multi-line strings, SQL/JSON literals
- **Virtual Threads** (Java 21): Lightweight concurrency (Project Loom)
- **Sequenced Collections** (Java 21): Ordered collection operations
- **String Templates** (Preview in Java 21): Safe string interpolation

**Virtual Threads Example Use Cases**:

- High-concurrency web servers (100k+ concurrent requests)
- I/O-bound operations (database, HTTP calls)
- Spring Boot 3.2+ with virtual threads enabled

### Code Style & Quality

**MUST**:

- Use Lombok to reduce boilerplate (`@Data`, `@Builder`, `@RequiredArgsConstructor`, `@Slf4j`)
- Follow Google Java Style Guide or corporate style guide
- Use Checkstyle for style enforcement
- Use SpotBugs (successor to FindBugs) for bug detection
- Use PMD for code quality checks

**SHOULD**:

- Use Spotless or Prettier for consistent formatting
- Use ArchUnit for architectural rules enforcement
- Use JaCoCo for code coverage measurement

### Naming Conventions

**MUST** follow:

- Classes, Interfaces, Records, Enums: `PascalCase`
- Methods, variables, parameters: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Packages: `lowercase` (e.g., `com.yourorg.userservice`)
- Test classes: `ClassNameTest` or `ClassNameIT` (integration tests)

### Dependency Injection

**MUST**:

- Use constructor injection (recommended over field injection)
- Use `@RequiredArgsConstructor` (Lombok) for automatic constructor generation
- Avoid `@Autowired` on fields (use constructor injection instead)
- Use `@Primary` and `@Qualifier` for multiple bean candidates

**Advanced DI**:

- Use `@Conditional` annotations for conditional bean registration
- Use `@Profile` for environment-specific beans
- Avoid circular dependencies (refactor if detected)
- Use factory methods (`@Bean`) for complex object creation

### Functional Programming

**SHOULD**:

- Use Stream API for collection processing (Java 8+)
- Use Optional for null safety
- Use method references and lambda expressions
- Avoid mutable state in stream operations
- Use parallel streams cautiously (measure performance)

### Code Quality & SOLID Principles

**SHOULD**:

- Keep methods under 50 lines (extract to helper methods)
- Limit cyclomatic complexity (< 10 per method, measure with SonarQube)
- Follow SOLID principles:
  - **S**ingle Responsibility: One reason to change
  - **O**pen/Closed: Open for extension, closed for modification
  - **L**iskov Substitution: Subtypes must be substitutable
  - **I**nterface Segregation: Many specific interfaces > one general
  - **D**ependency Inversion: Depend on abstractions, not concretions
- Write meaningful names (avoid abbreviations, no single letters except loops)
- Prefer composition over inheritance

---

## Testing

### Unit Testing

**MUST**:

- Write unit tests using JUnit 5 (Jupiter)
- Aim for 80%+ coverage on business logic
- Use AAA pattern (Arrange, Act, Assert)
- Mock external dependencies (Mockito, EasyMock)

**SHOULD**:

- Use AssertJ for fluent assertions (more readable than JUnit assertions)
- Use Mockito's `@Mock`, `@InjectMocks` annotations
- Use `@ExtendWith(MockitoExtension.class)` or `@SpringBootTest` annotations
- Test edge cases and error conditions

### Integration Testing

**MUST**:

- Write integration tests for API endpoints (`@SpringBootTest` with `WebEnvironment.RANDOM_PORT`)
- Test database interactions with Testcontainers (Docker-based test databases)
- Use separate test profiles (`application-test.yml`)
- Use `@Transactional` for test data cleanup (automatic rollback)

**SHOULD**:

- Use REST Assured or MockMvc for HTTP endpoint testing
- Use WireMock for external API mocking
- Use embedded databases (H2) for simple tests, Testcontainers for realistic tests
- Test security configurations (authentication, authorization)

### Contract Testing

**SHOULD**:

- Use Spring Cloud Contract for consumer-driven contract testing
- Define contracts in Groovy or YAML
- Generate tests from contracts automatically

### Performance Testing

**SHOULD**:

- Use JMH (Java Microbenchmark Harness) for microbenchmarking
- Use Gatling or JMeter for load testing
- Profile hot paths with JProfiler, YourKit, or VisualVM

### Test Naming

**MUST** follow:

- Method: `methodName_scenario_expectedBehavior`
- Example: `createOrder_withInvalidProduct_throwsValidationException`
- Use `@DisplayName` for readable test descriptions

---

## Build & Deployment

### Build Process

**MUST**:

- Use Maven (`mvn clean install`) or Gradle (`gradle build`)
- Run tests before deployment (`mvn test` or `gradle test`)
- Use CI/CD pipeline for automated testing and deployment
- Use Maven/Gradle wrapper for consistent builds

**CI/CD**:

- Run linters (Checkstyle, PMD, SpotBugs)
- Run security scanning (Snyk, OWASP Dependency Check, Trivy)
- Generate code coverage reports (JaCoCo)
- Publish artifacts to corporate artifact repository

### Docker - Cloud Deployments

**MUST**:

- Use multi-stage builds (Maven/Gradle build stage + JRE runtime stage)
- Use official Eclipse Temurin base images:
  - Build: `eclipse-temurin:21-jdk-alpine` (smaller) or `-jammy` (Ubuntu-based)
  - Runtime: `eclipse-temurin:21-jre-alpine` (production)
- Run as non-root user in container
- Copy only JAR file to runtime image (use .dockerignore)
- Use layer optimization (Spring Boot layered JARs)

**SHOULD**:

- Keep container images small (< 200MB for simple services)
- Use health checks in Dockerfile (`HEALTHCHECK` instruction)
- Set resource limits (CPU, memory) in container runtime
- Use read-only root filesystem when possible (`--read-only` flag)

**Spring Boot Optimization**:

- Use `spring-boot-maven-plugin` with `layers` configuration
- Extract layers for better caching (dependencies change less than code)
- Use `-Dspring.profiles.active=prod` for production profile

**Cloud-Specific**:

- **Azure**: Deploy to Azure Container Apps, Azure Kubernetes Service (AKS), Azure App Service
- **AWS**: Deploy to ECS, EKS, Elastic Beanstalk
- Use managed identity for cloud resource access

### Docker - On-Premise Deployments

**MUST**:

- Use Docker Compose or Kubernetes for orchestration
- Configure persistent volumes for data storage
- Implement backup strategies for stateful services
- Use private container registry (Harbor, Artifactory, Nexus)

**SHOULD**:

- Use Kubernetes for complex multi-service deployments
- Implement blue-green or canary deployment strategies
- Use service mesh (Istio, Linkerd) for advanced traffic management

### Kubernetes Best Practices

**MUST**:

- Define resource requests and limits (CPU, memory)
- Implement liveness and readiness probes (`/actuator/health/liveness`, `/actuator/health/readiness`)
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Use Horizontal Pod Autoscaling (HPA) for load management

**SHOULD**:

- Use Helm charts for deployment templates
- Implement network policies for pod-to-pod communication
- Use Ingress controllers (NGINX, Traefik) for external access
- Use persistent volumes for stateful applications

---

## Observability

### Health Checks (Spring Boot Actuator)

**MUST** include:

- Liveness probe (`/actuator/health/liveness`): Indicates if app is running
- Readiness probe (`/actuator/health/readiness`): Indicates if app can accept traffic
- Custom health indicators for critical dependencies (database, message queue, external APIs)

**Implementation**:

- Use Spring Boot Actuator (`spring-boot-starter-actuator`)
- Implement custom `HealthIndicator` for business-critical checks
- Return 200 OK for healthy, 503 Service Unavailable for unhealthy
- Include detailed health information in development (hide in production)

### Metrics (Micrometer)

**MUST** include:

- Expose metrics endpoint (`/actuator/metrics`) in Prometheus format
- Track request rate, error rate, duration (RED metrics)
- Track JVM metrics (heap, GC, threads, CPU)
- Track database connection pool metrics
- Use custom metrics for business KPIs (orders/sec, revenue, user signups)

**Tools**:

- Micrometer for metrics collection (vendor-neutral)
- Prometheus for metric storage
- Grafana for visualization
- Azure Monitor, AWS CloudWatch for cloud deployments

**Custom Metrics**:

- Use `@Timed` annotation for method-level timing
- Use `Counter`, `Gauge`, `Timer`, `DistributionSummary` from Micrometer
- Tag metrics appropriately (endpoint, status, method)

### Distributed Tracing (Micrometer Tracing)

**MUST**:

- Enable Micrometer Tracing (formerly Spring Cloud Sleuth)
- Export traces to Zipkin, Jaeger, Azure Application Insights, AWS X-Ray
- Include trace context (traceId, spanId) in all outgoing requests
- Implement custom spans for critical operations

**Configuration**:

- Use `spring-boot-starter-actuator` + `micrometer-tracing-bridge-otel` (OpenTelemetry)
- Configure trace sampling rate (1.0 for dev, 0.1 for production)
- Propagate trace context across services (HTTP headers, messaging)

### Application Performance Monitoring (APM)

**SHOULD** use:

- Application Insights (Azure)
- AWS X-Ray (AWS)
- New Relic, Datadog, Dynatrace (multi-cloud)
- Elastic APM (on-premise)
- Instana (automatic instrumentation)

**Note**: Corporate Spring Boot starter includes Spring Boot Actuator with all observability features by default

---

## Microservices Patterns

### Service Communication

**MUST** choose based on use case:

- **Synchronous**: HTTP/REST (Spring MVC/WebClient), gRPC (high performance)
- **Asynchronous**: Message queues (RabbitMQ, Kafka, Azure Service Bus, AWS SQS) for event-driven

**SHOULD**:

- Use saga pattern for distributed transactions (orchestration or choreography)
- Implement compensation logic for failures
- Use outbox pattern for reliable message publishing (transactional messaging)
- Use idempotency keys for exactly-once processing

### Service Discovery

**Cloud**:

- **Azure**: Azure Service Fabric, Azure Kubernetes Service (DNS-based)
- **AWS**: AWS Cloud Map, ECS Service Discovery

**On-Premise**:

- Spring Cloud Consul for service registry
- Kubernetes DNS for container-based services
- Spring Cloud LoadBalancer for client-side load balancing

### API Gateway

**SHOULD** use:

- **Azure**: Azure API Management
- **AWS**: AWS API Gateway, AWS App Mesh
- **Self-hosted**: Spring Cloud Gateway (reactive), Kong, Tyk

**Features**: Rate limiting, authentication, request routing, load balancing, circuit breaking, caching

### Configuration Management

**SHOULD** use:

- **Spring Cloud Config**: Centralized configuration server (Git-backed)
- **Azure App Configuration**: Cloud-native config management
- **AWS Systems Manager Parameter Store**: Secure parameter storage
- **HashiCorp Consul**: KV store for configuration

---

## Performance & Scalability

### JVM Tuning

**SHOULD**:

- Use G1GC (default in Java 9+) or ZGC (ultra-low latency) garbage collector
- Set appropriate heap sizes (`-Xms`, `-Xmx`) based on workload
- Enable JVM metrics export to monitoring systems
- Use container-aware JVM settings (`-XX:+UseContainerSupport`)
- Profile garbage collection patterns (GC logs, analysis tools)

### Caching Strategy

**SHOULD**:

- Cache frequently accessed, rarely changed data
- Use distributed cache (Redis) for multi-instance deployments
- Implement cache warming for critical data
- Use cache invalidation strategies (time-based, event-based)
- Use Spring Cache annotations (`@Cacheable`, `@CachePut`, `@CacheEvict`)

### Database Optimization

**SHOULD**:

- Use indexes on frequently queried columns
- Use database connection pooling (HikariCP - default in Spring Boot)
- Use read replicas for read-heavy workloads
- Implement database sharding for extreme scale
- Use `@EntityGraph` or fetch joins to avoid N+1 queries
- Use projections instead of fetching full entities

### Horizontal Scaling

**MUST**:

- Design stateless services (store session in Redis, database)
- Use load balancers (Azure Load Balancer, AWS ELB, NGINX, HAProxy)
- Implement auto-scaling based on metrics (CPU, memory, request rate)
- Use sticky sessions cautiously (prefer stateless design)

### Virtual Threads (Project Loom)

**MAY** use in Java 21+:

- Enable with `spring.threads.virtual.enabled=true` (Spring Boot 3.2+)
- Suitable for I/O-bound workloads with high concurrency
- Not suitable for CPU-bound workloads
- Monitor virtual thread performance with JFR (Java Flight Recorder)

---

## Reactive Programming (Optional)

### Spring WebFlux

**MAY** use for reactive, non-blocking applications:

- Use `WebClient` instead of `RestTemplate` or `RestClient`
- Use `R2DBC` for reactive database access
- Use Project Reactor (`Mono`, `Flux`) for reactive streams
- Choose reactive for high-concurrency I/O-bound workloads

**Trade-offs**:

- **Pros**: Better scalability, non-blocking I/O, backpressure support
- **Cons**: Steeper learning curve, debugging complexity, ecosystem maturity

**When to Use**:

- Streaming data applications
- High-concurrency APIs (> 10k concurrent requests)
- Real-time event processing

---

## Compliance & Governance

### Data Protection

**MUST**:

- Implement GDPR, CCPA, LGPD compliance for personal data
- Encrypt data at rest and in transit (TLS 1.3, AES-256)
- Implement data retention policies (automated cleanup)
- Support data export (JSON, CSV) and deletion requests (right to be forgotten)

### Audit Logging

**MUST**:

- Log all data access and modifications with `@Audited` entities
- Include user identity, timestamp, operation type, changed fields
- Store audit logs separately from application logs
- Retain audit logs per regulatory requirements (7 years for financial)

### Code Analysis

**SHOULD**:

- Enable Maven Enforcer or Gradle build-time checks
- Use SonarQube for static code analysis (quality gates)
- Use dependency scanning (Snyk, OWASP Dependency Check, Dependabot)
- Run security scanning in CI/CD pipeline (SAST, DAST)
- Use Trivy for container image scanning

---

## Non-Compliance

If corporate library unavailable or causes blocking issue:

1. Document violation in `.guidelines-todo.md` with justification and business impact
2. Create JIRA/ticket to resolve (target: next sprint)
3. Proceed with alternative, mark with `// TODO: GUIDELINE-VIOLATION - Ticket #XXX` comment for tracking
4. Schedule tech debt review within 30 days
