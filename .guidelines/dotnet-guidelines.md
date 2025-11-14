# .NET Corporate Guidelines

**Tech Stack**: .NET 8 LTS, C# 12, ASP.NET Core, Backend Services, Microservices, APIs
**Auto-detected from**: `*.csproj`, `*.sln`, or `*.cs` files
**Version**: 2.0
**Last Updated**: 2025-01-15

---

## Target Framework

**MUST**:

- Use .NET 8 (LTS - Long Term Support until November 2026)
- Enable nullable reference types (`<Nullable>enable</Nullable>`)
- Target `net8.0` in project files

**SHOULD**:

- Plan migration to .NET 9+ when released as LTS
- Use preview features cautiously (flag with comments)

**Rationale**: .NET 8 provides 3 years of support, performance improvements, and enterprise stability

---

## Scaffolding

**MUST**:

- Use corporate dotnet templates (YOUR_ORG-webapi, YOUR_ORG-minimal-api, YOUR_ORG-worker, YOUR_ORG-blazor, YOUR_ORG-grpc)
- Install templates from corporate NuGet source

**NEVER**:

- Use default Microsoft templates (`dotnet new webapi`, `dotnet new mvc`)

**Alternative Templates**:

- **Minimal APIs**: For lightweight microservices, serverless functions
- **Traditional Controllers**: For complex APIs requiring filters, routing conventions
- **Worker Services**: For background processing, message consumers, scheduled jobs
- **gRPC Services**: For high-performance inter-service communication
- **Blazor**: For server-rendered or WebAssembly SPAs

**Rationale**: Corporate templates include security, logging, monitoring, compliance, health checks, observability from day one

---

## Package Registry

**MUST**:

- Configure `nuget.config` with corporate NuGet source (YOUR_ORG NuGet registry)
- All packages resolved through corporate registry only
- Use authenticated feeds for private packages

**NEVER**:

- Install packages from public NuGet.org directly without approval
- Use unvetted third-party packages

**Configuration**:

- Place `nuget.config` at solution root
- Include both corporate and approved public sources
- Use credential providers for authentication

---

## Mandatory Libraries

### ASP.NET Core Starter

**MUST** use: `YOUR_ORG.AspNetCore.Starter` package
**Includes**: Security, logging, monitoring, health checks, exception handling, CORS, rate limiting, distributed tracing
**Integration**: 

- Register services via `builder.Services.AddYourOrgServices()`
- Apply middleware via `app.UseYourOrgMiddleware()`
- Supports both minimal APIs and controller-based APIs

### Security & Authentication

**MUST** use: `YOUR_ORG.Security` package
**Requirements**:

- Decorate endpoints with `[SecuredEndpoint(Roles = "...")]` or equivalent minimal API filter
- Extract authenticated user context via `HttpContext.User.GetCurrentUser()`
- Pass user context to all service layer calls
- Support OAuth 2.0, OpenID Connect, JWT bearer tokens
- Implement token refresh mechanisms

**Features**:

- Multi-tenant authentication support
- Claims-based authorization
- API key authentication for service-to-service
- Certificate-based authentication for high-security scenarios

### HTTP Client & Resilience

**MUST** use: `YOUR_ORG.HttpClient` package (wraps `Microsoft.Extensions.Http.Resilience`)
**Requirements**:

- Inject via `IYourOrgHttpClientFactory`, never create HttpClient directly
- Use resilience pipelines with retry, circuit breaker, timeout policies
- All external API calls auto-instrumented for distributed tracing (OpenTelemetry)

**Features**:

- Service discovery integration
- Hedging strategies for critical calls
- Adaptive timeout calculation
- Request/response logging and metrics
- Support for gRPC and REST clients

**Cloud-Specific**:

- Azure Service Bus integration for reliable messaging
- AWS SQS/SNS support for cloud-agnostic messaging

**On-Premise**:

- RabbitMQ client wrappers with retry logic
- Kafka producer/consumer with exactly-once semantics

### Database - Entity Framework Core

**MUST** use: Entity Framework Core 8.x with `YOUR_ORG.EntityFrameworkCore.Extensions`
**Requirements**:

- Entities inherit from `AuditedEntity` for automatic audit trail (CreatedBy, CreatedAt, UpdatedBy, UpdatedAt, RowVersion)
- Use EF Core migrations for all schema changes (`dotnet ef migrations add`)
- Apply migrations on deployment (`dotnet ef database update` or via DbContext initialization)
- Use compiled models for production performance
- Enable query splitting for optimal performance with related data

**Advanced Features**:

- Temporal tables for audit history (SQL Server, PostgreSQL)
- Global query filters for soft deletes, multi-tenancy
- Interceptors for custom logging, performance monitoring
- Second-level caching integration (Redis, In-Memory)

**Supported Databases**:

- SQL Server (cloud: Azure SQL, on-premise: SQL Server 2019+)
- PostgreSQL (cloud: Azure PostgreSQL, AWS RDS, on-premise: PostgreSQL 14+)
- Oracle (on-premise: Oracle 19c+)
- MongoDB (via separate driver, not EF Core)

### Database - Dapper (High Performance)

**MAY** use: Dapper with `YOUR_ORG.Dapper.Extensions` for read-heavy scenarios
**Use Cases**:

- Complex reporting queries with performance requirements
- Bulk operations requiring raw SQL optimization
- Legacy database integration with stored procedures

**Requirements**:

- Use parameterized queries exclusively (SQL injection prevention)
- Apply same audit patterns as EF Core
- Document why Dapper chosen over EF Core

### Caching

**MUST** use: `YOUR_ORG.Caching` package (wraps `Microsoft.Extensions.Caching`)
**Requirements**:

- Use distributed cache (Redis, SQL Server) for multi-instance deployments
- Use in-memory cache only for single-instance scenarios
- Implement cache-aside pattern with appropriate TTL
- Use cache invalidation strategies (time-based, event-based)

**Cloud-Specific**:

- Azure Redis Cache for cloud deployments
- AWS ElastiCache for Redis compatibility

**On-Premise**:

- Redis Cluster or Redis Sentinel for high availability
- SQL Server distributed cache for simple scenarios

### Logging & Observability

**MUST** use: `YOUR_ORG.Logging` package (built on `Microsoft.Extensions.Logging` + OpenTelemetry)
**Requirements**:

- Inject `ILogger<T>` via dependency injection
- Use structured logging with named parameters
- Include correlation ID, trace ID, span ID in all log statements (auto-added by middleware)
- Export logs to corporate logging platform (Elasticsearch, Splunk, Azure Monitor)

**Log Levels**:

- **Trace**: Detailed diagnostic information (disabled in production)
- **Debug**: Development debugging (disabled in production)
- **Information**: General informational messages
- **Warning**: Unexpected behavior that doesn't prevent operation
- **Error**: Errors requiring investigation
- **Critical**: System failures requiring immediate attention

**NEVER**:

- Use `Console.WriteLine()` for logging
- Log PII, secrets, passwords, authentication tokens, credit card numbers, SSNs
- Log entire request/response bodies without sanitization

**Distributed Tracing**:

- Enable OpenTelemetry instrumentation for HTTP, database, messaging
- Export traces to Jaeger, Zipkin, Azure Application Insights, AWS X-Ray
- Implement trace sampling strategies for high-throughput systems

### Validation

**MUST** use: FluentValidation 11+ with `YOUR_ORG.Validators` extensions
**Requirements**:

- Create validator classes inheriting `AbstractValidator<T>`
- Use corporate validators for common patterns (CorporateEmail, PhoneNumber, PostalCode)
- Validate all API inputs before processing
- Return structured validation errors (field-level details)

**Advanced Patterns**:

- Async validation for database uniqueness checks
- Conditional validation based on business rules
- Cross-field validation for complex business logic

### Background Jobs & Scheduling

**MUST** use: Hangfire or `YOUR_ORG.BackgroundJobs` for persistent job scheduling
**Requirements**:

- Use persistent storage (SQL Server, PostgreSQL, Redis) for job state
- Implement idempotent job handlers (support retries)
- Use queues for prioritization
- Monitor job success/failure rates

**Use Cases**:

- Scheduled reports generation
- Data synchronization tasks
- Email/notification sending
- Batch processing operations

**Cloud-Specific**:

- Azure Functions with Durable Functions for orchestration
- AWS Lambda with Step Functions for workflows

**On-Premise**:

- Hangfire with SQL Server for job persistence
- Quartz.NET for complex scheduling requirements

### API Documentation

**MUST**:

- Enable OpenAPI/Swagger documentation for all APIs
- Use XML documentation comments for endpoint descriptions
- Include request/response examples
- Document error responses and status codes

**Requirements**:

- Configure Swagger UI for development environments only
- Export OpenAPI spec for API gateway registration
- Version APIs explicitly (URL versioning or header-based)

---

## Banned Libraries

**NEVER** use:

- `HttpClient` directly without factory → Use `IHttpClientFactory` or `YOUR_ORG.HttpClient`
- Serilog without corporate wrapper → Use `YOUR_ORG.Logging`
- `Console.WriteLine()` → Use `ILogger<T>`
- Newtonsoft.Json → Use `System.Text.Json` (built-in, faster)
- AutoMapper without justification → Prefer explicit mapping for maintainability

**Rationale**: Corporate wrappers add security, monitoring, compliance, circuit breaking, distributed tracing

---

## Architecture

### Project Structure - Vertical Slice (Recommended for New Projects)

**SHOULD** use: Feature-based organization for better cohesion

- **Features/**: Each feature contains handlers, validators, models
  - **UserRegistration/**: Command, handler, validator, response
  - **OrderProcessing/**: Query, handler, repository
- **Shared/**: Cross-cutting concerns (logging, auth, validation)
- **Infrastructure/**: Database, external services, messaging

**Benefits**: Better encapsulation, easier testing, clearer boundaries

### Project Structure - Traditional Layered (Acceptable)

**MAY** use: Layered architecture for large, established codebases

- **API Layer**: Controllers, Program.cs, middleware configuration
- **Application Layer**: Services, commands, queries, business logic
- **Domain Layer**: Entities, value objects, domain events, interfaces
- **Infrastructure Layer**: Data access, repositories, external integrations

### Separation of Concerns

**MUST**:

- Keep controllers/endpoints thin (routing, validation, serialization only)
- Put business logic in service layer or handlers
- Use repository pattern or direct DbContext for data access
- Never put business logic in controllers or repositories
- Use MediatR or similar for CQRS pattern implementation

### API Patterns

**SHOULD** choose based on use case:

- **REST**: Standard CRUD operations, public APIs
- **GraphQL**: Complex data fetching, mobile APIs (use HotChocolate)
- **gRPC**: High-performance inter-service communication
- **SignalR**: Real-time bidirectional communication

### DTOs (Data Transfer Objects)

**MUST**:

- Use separate DTOs for API contracts (never expose entities directly)
- Keep sensitive fields (PasswordHash, InternalId, AuditFields) in entities only
- Use `record` types for immutable DTOs
- Implement mapping explicitly or use source generators

**Pattern**:

- Request DTOs for input validation
- Response DTOs for output serialization
- Internal DTOs for service-to-service communication

### Exception Handling

**MUST**:

- Use centralized exception handling middleware
- Map domain exceptions to appropriate HTTP status codes
- Return generic error messages to clients (no internal details, stack traces)
- Log full exception details server-side with correlation ID
- Implement ProblemDetails (RFC 7807) for error responses

**Status Code Mapping**:

- ValidationException → 400 Bad Request
- UnauthorizedException → 401 Unauthorized
- ForbiddenException → 403 Forbidden
- NotFoundException → 404 Not Found
- ConflictException → 409 Conflict
- DomainException → 422 Unprocessable Entity
- InfrastructureException → 500 Internal Server Error

---

## Security

### Input Validation

**MUST**:

- Validate all API inputs (ModelState, FluentValidation)
- Return 400 Bad Request with structured errors for validation failures
- Reject requests before reaching business logic
- Validate file uploads (type, size, content)
- Sanitize HTML inputs to prevent XSS

### SQL Injection Prevention

**MUST**:

- Use Entity Framework Core (parameterized queries automatic)
- Use Dapper with parameterized queries only
- Never concatenate strings for SQL queries
- Use stored procedures with parameters if required

### Secrets Management

**MUST**:

- Store secrets in Azure Key Vault, AWS Secrets Manager, or corporate secrets manager
- Access secrets via configuration (`builder.Configuration["YourOrg:ApiKey"]`)
- Use managed identities (Azure, AWS) for authentication
- Rotate secrets regularly (automated via secret manager)

**NEVER**:

- Hardcode secrets in code or appsettings.json
- Commit secrets to source control
- Store secrets in environment variables without encryption (production)

**Configuration Hierarchy** (lowest to highest priority):

1. appsettings.json (defaults, non-sensitive)
2. appsettings.{Environment}.json (environment-specific)
3. User secrets (development only)
4. Environment variables
5. Azure Key Vault / AWS Secrets Manager (production)

### Authentication & Authorization

**MUST**:

- Validate user roles before resource access
- Use `[SecuredEndpoint]` attribute or authorization policies on all protected endpoints
- Implement principle of least privilege
- Use role-based access control (RBAC) or claims-based authorization
- Support multi-factor authentication (MFA) for sensitive operations

**Cloud-Specific**:

- Azure AD / Entra ID for identity management
- AWS Cognito for user authentication
- Integrate with corporate SSO (SAML, OIDC)

**On-Premise**:

- Active Directory integration via Windows Authentication
- Custom JWT-based authentication with refresh tokens

### API Security

**MUST**:

- Implement rate limiting per user/IP (AspNetCoreRateLimit or built-in)
- Use API versioning for backward compatibility
- Implement CORS policies restrictively
- Validate content-type headers
- Implement request size limits
- Use HTTPS exclusively (enforce HSTS)

### Security Headers

**MUST** include:

- Content-Security-Policy
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security (HSTS)
- Referrer-Policy: no-referrer

---

## Coding Standards

### .NET Version & Features

**MUST**:

- Target .NET 8 (LTS version)
- Enable nullable reference types (`<Nullable>enable</Nullable>`)
- Use modern C# 12 features: primary constructors, collection expressions, alias any type

**SHOULD** use modern features:

- Record types for immutable data
- Pattern matching for cleaner conditionals
- Global using directives for common namespaces
- File-scoped namespaces
- Init-only properties
- Required properties (C# 11+)

### Async/Await

**MUST**:

- Use async/await for all I/O operations (database, HTTP, file system, message queues)
- Never block on async calls (no `.Result`, `.Wait()`, `.GetAwaiter().GetResult()`)
- Use `ConfigureAwait(false)` in library code (not in ASP.NET Core controllers)
- Use `ValueTask<T>` for hot paths with synchronous fast-path

**Async Best Practices**:

- Use `CancellationToken` for long-running operations
- Propagate cancellation tokens through call chain
- Implement timeout policies for external calls

### Dependency Injection

**MUST**:

- Use constructor injection for all dependencies
- Register services with appropriate lifetime:
  - **Singleton**: Stateless services, shared configuration
  - **Scoped**: Per-request services, DbContext
  - **Transient**: Lightweight, stateful services
- Never use `new` for services (except POCOs, DTOs, value objects)

**Advanced DI**:

- Use keyed services (NET 8+) for multiple implementations
- Use factory pattern for complex object creation
- Avoid service locator pattern (prefer constructor injection)

### Naming Conventions

**MUST** follow:

- Classes, Methods, Properties, Records: `PascalCase`
- Local variables, parameters: `camelCase`
- Private fields: `_camelCase` with underscore prefix
- Constants: `PascalCase` (not UPPER_SNAKE_CASE)
- Interfaces: `IPascalCase` with I prefix
- Async methods: `MethodNameAsync` suffix

### Code Quality & SOLID Principles

**SHOULD**:

- Keep methods under 50 lines (extract to helper methods)
- Limit cyclomatic complexity (< 10 per method, measure with tools)
- Follow SOLID principles:
  - **S**ingle Responsibility: One reason to change
  - **O**pen/Closed: Open for extension, closed for modification
  - **L**iskov Substitution: Subtypes must be substitutable
  - **I**nterface Segregation: Many specific interfaces > one general
  - **D**ependency Inversion: Depend on abstractions, not concretions
- Write meaningful names (avoid abbreviations, no single letters except loop counters)
- Use expression-bodied members for simple properties/methods
- Prefer composition over inheritance

### Performance Optimization

**SHOULD**:

- Use `Span<T>` and `Memory<T>` for high-performance scenarios
- Use object pooling (`ObjectPool<T>`) for frequently allocated objects
- Use `System.Text.Json` with source generators for serialization
- Profile hot paths with BenchmarkDotNet
- Use `ref struct` for stack-only types when appropriate
- Minimize allocations in hot paths (measure with dotMemory, PerfView)

---

## Testing

### Unit Testing

**MUST**:

- Write unit tests using xUnit, NUnit, or MSTest
- Aim for 80%+ coverage on business logic
- Use AAA pattern (Arrange, Act, Assert)
- Mock external dependencies (Moq, NSubstitute)

**SHOULD**:

- Use FluentAssertions for readable assertions
- Use AutoFixture for test data generation
- Use Bogus for realistic fake data

### Integration Testing

**MUST**:

- Write integration tests for API endpoints (WebApplicationFactory)
- Test database interactions with test containers (Testcontainers for .NET)
- Use separate test databases (never production)

**SHOULD**:

- Use Respawn for database cleanup between tests
- Use Docker for consistent test environments

### E2E Testing

**SHOULD**:

- Use Playwright or Selenium for UI testing
- Run E2E tests in CI/CD pipeline
- Test critical user journeys only (expensive to maintain)

### Test Naming

**MUST** follow:

- Method: `MethodName_Scenario_ExpectedBehavior`
- Example: `CreateOrder_WithInvalidProduct_ThrowsValidationException`

---

## Build & Deployment

### Build Process

**MUST**:

- Use `dotnet build` for compilation
- Use `dotnet publish -c Release --self-contained false` for deployment packages
- Run tests before deployment (`dotnet test`)
- Use deterministic builds (`<Deterministic>true</Deterministic>`)

**CI/CD**:

- Run linters (Roslyn analyzers, StyleCop)
- Run security scanning (Snyk, SonarQube)
- Generate code coverage reports
- Publish NuGet packages to corporate registry

### Docker - Cloud Deployments

**MUST**:

- Use multi-stage builds (SDK for build, aspnet runtime for runtime)
- Use official Microsoft base images:
  - Build: `mcr.microsoft.com/dotnet/sdk:8.0`
  - Runtime: `mcr.microsoft.com/dotnet/aspnet:8.0-alpine` (smaller) or `-jammy` (full Ubuntu)
- Run as non-root user in container
- Copy only necessary files (use .dockerignore)
- Use layer caching for faster builds

**SHOULD**:

- Keep container images small (< 200MB for API services)
- Use health checks in Dockerfile
- Set resource limits (CPU, memory)
- Use read-only root filesystem when possible

**Cloud-Specific**:

- **Azure**: Deploy to Azure Container Apps, Azure Kubernetes Service (AKS), Azure App Service
- **AWS**: Deploy to ECS, EKS, Elastic Beanstalk
- Use managed identity for cloud resource access

### Docker - On-Premise Deployments

**MUST**:

- Use Docker Compose or Kubernetes for orchestration
- Configure persistent volumes for data storage
- Implement backup strategies for stateful services
- Use private container registry (Harbor, Artifactory)

**SHOULD**:

- Use Kubernetes for complex multi-service deployments
- Implement blue-green or canary deployment strategies
- Use service mesh (Istio, Linkerd) for advanced traffic management

### Kubernetes Best Practices

**MUST**:

- Define resource requests and limits
- Implement liveness and readiness probes
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Use Horizontal Pod Autoscaling (HPA) for load management

**SHOULD**:

- Use Helm charts for deployment templates
- Implement network policies for pod-to-pod communication
- Use Ingress controllers (NGINX, Traefik) for external access

---

## Observability

### Health Checks

**MUST** include:

- Liveness probe (`/health/live`): Indicates if app is running
- Readiness probe (`/health/ready`): Indicates if app can accept traffic
- Check dependencies: database, message queue, external APIs

**Implementation**:

- Use `Microsoft.Extensions.Diagnostics.HealthChecks`
- Include custom health checks for critical dependencies
- Return 200 OK for healthy, 503 Service Unavailable for unhealthy

### Metrics

**MUST** include:

- Expose metrics endpoint (`/metrics`) in Prometheus format
- Track request rate, error rate, duration (RED metrics)
- Track resource utilization (CPU, memory, connections)
- Use custom metrics for business KPIs

**Tools**:

- Prometheus for metric collection
- Grafana for visualization
- Azure Monitor, AWS CloudWatch for cloud deployments

### Distributed Tracing

**MUST**:

- Enable OpenTelemetry instrumentation
- Export traces to Jaeger, Zipkin, Azure Application Insights, AWS X-Ray
- Include trace context in all outgoing requests
- Implement custom spans for critical operations

**Note**: Corporate ASP.NET Core starter includes all observability features by default

### Application Performance Monitoring (APM)

**SHOULD** use:

- Application Insights (Azure)
- AWS X-Ray (AWS)
- New Relic, Datadog, Dynatrace (multi-cloud)
- Elastic APM (on-premise)

---

## Microservices Patterns

### Service Communication

**MUST** choose based on use case:

- **Synchronous**: HTTP/REST, gRPC for request/response
- **Asynchronous**: Message queues (RabbitMQ, Azure Service Bus, AWS SQS) for event-driven

**SHOULD**:

- Use saga pattern for distributed transactions
- Implement compensation logic for failures
- Use outbox pattern for reliable message publishing

### Service Discovery

**Cloud**:

- Azure: Azure Service Fabric, Azure Kubernetes Service
- AWS: AWS Cloud Map, ECS Service Discovery

**On-Premise**:

- Consul for service registry
- Kubernetes DNS for container-based services

### API Gateway

**SHOULD** use:

- Azure API Management (Azure)
- AWS API Gateway (AWS)
- Kong, Tyk, Ocelot (self-hosted)

**Features**: Rate limiting, authentication, request routing, load balancing

---

## Performance & Scalability

### Caching Strategy

**SHOULD**:

- Cache frequently accessed, rarely changed data
- Use distributed cache (Redis) for multi-instance deployments
- Implement cache warming for critical data
- Use cache invalidation strategies (time-based, event-based)

### Database Optimization

**SHOULD**:

- Use indexes on frequently queried columns
- Use compiled queries for hot paths
- Use read replicas for read-heavy workloads
- Implement connection pooling
- Use database sharding for extreme scale

### Horizontal Scaling

**MUST**:

- Design stateless services (store session in Redis, database)
- Use load balancers (Azure Load Balancer, AWS ELB, NGINX)
- Implement auto-scaling based on metrics

---

## Compliance & Governance

### Data Protection

**MUST**:

- Implement GDPR, CCPA compliance for personal data
- Encrypt data at rest and in transit
- Implement data retention policies
- Support data export and deletion requests

### Audit Logging

**MUST**:

- Log all data access and modifications
- Include user identity, timestamp, operation type
- Store audit logs separately from application logs
- Retain audit logs per regulatory requirements

### Code Analysis

**SHOULD**:

- Enable Roslyn analyzers for code quality
- Use SonarQube for static code analysis
- Use dependency scanning (Snyk, Dependabot)
- Run security scanning in CI/CD pipeline

---

## Non-Compliance

If corporate library unavailable or causes blocking issue:

1. Document violation in `.guidelines-todo.md` with justification and business impact
2. Create ticket to resolve (target: next sprint)
3. Proceed with alternative, mark with `// TODO: GUIDELINE-VIOLATION - Ticket #XXX` comment for tracking
4. Schedule tech debt review within 30 days
