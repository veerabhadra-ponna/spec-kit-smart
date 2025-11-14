# Node.js Corporate Guidelines

**Tech Stack**: Node.js 20/22 LTS, TypeScript 5+, Express 4.x/5.x, Fastify 4.x, Backend Services, APIs, Microservices
**Auto-detected from**: `package.json` with backend dependencies (express, fastify, koa, hapi)
**Version**: 2.0
**Last Updated**: 2025-01-15

---

## Target Platform

**MUST**:

- Use Node.js 20 LTS (Active until April 2026) or Node.js 22 LTS (Active until April 2027)
- Use TypeScript 5.3+ for all new projects
- Target ES2022 or ESNext in `tsconfig.json`

**SHOULD**:

- Upgrade to Node.js 22 LTS when your infrastructure supports it
- Use native Node.js test runner for simple test cases (experimental)
- Leverage new Node.js features (fetch API, native test runner, watch mode)

**Rationale**: Node.js LTS provides 3 years of active support + 18 months maintenance, TypeScript provides type safety and maintainability

---

## Scaffolding

**MUST**:

- Use corporate scaffolding command (`@YOUR_ORG/create-node-service`)
- Choose appropriate template:
  - **express-ts**: Traditional Express with TypeScript
  - **fastify-ts**: High-performance Fastify with TypeScript
  - **nestjs**: Enterprise NestJS framework (opinionated)
  - **minimal-api**: Lightweight API with minimal dependencies
  - **microservice**: Event-driven microservice with messaging
  - **graphql**: GraphQL API with Apollo Server
  - **grpc**: gRPC service for inter-service communication

**NEVER**:

- Use `npm init`, `npx express-generator`, or public templates directly

**Rationale**: Corporate scaffolding includes security, logging, monitoring, compliance, observability from day one

---

## Package Registry

**MUST**:

- Configure `.npmrc` with corporate npm registry (Artifactory, Nexus, Azure Artifacts, GitHub Packages)
- All dependencies resolved through corporate registry only
- Use authentication tokens (never plaintext passwords)

**NEVER**:

- Install packages from public npmjs.org directly without security scanning

**Configuration**:

- Place `.npmrc` at project root
- Use `npm_TOKEN` or `NODE_AUTH_TOKEN` environment variable for CI/CD
- Configure scoped packages (`@yourorg:registry=https://registry.yourorg.com`)

---

## Mandatory Libraries

### Framework Starter

**MUST** use one of: `@YOUR_ORG/express-starter`, `@YOUR_ORG/fastify-starter`, or `@YOUR_ORG/nestjs-starter`
**Includes**: Security middleware, logging, metrics, error handling, CORS, rate limiting, health checks, observability
**Integration**: Use `createApp()` factory function with corporate configuration

**Framework Selection**:

- **Express 4.x/5.x**: Most popular, largest ecosystem, traditional middleware approach
- **Fastify 4.x**: High performance (3x faster than Express), schema validation, plugin architecture
- **NestJS 10.x**: Opinionated, TypeScript-first, Angular-inspired, dependency injection, great for large teams
- **Koa 2.x**: Minimalist, async/await-first, Express successor (smaller ecosystem)
- **Hapi 21.x**: Configuration-driven, enterprise features (rarely used now)

**Recommendation**: Use Fastify for new high-performance APIs, NestJS for large enterprise applications, Express for legacy/standard projects

### Authentication & Authorization

**MUST** use: `@YOUR_ORG/auth-middleware` package
**Requirements**:

- Apply `authMiddleware()` globally or per-route
- Use `authorize([roles])` middleware for role-based access control
- Extract authenticated user via `req.user` property
- Support JWT bearer tokens, OAuth 2.0, API keys

**Advanced Features**:

- Multi-tenant authentication with tenant isolation
- Token refresh mechanisms with sliding expiration
- Certificate-based mutual TLS (mTLS) for service-to-service
- API key rotation and management
- Session management with Redis for stateful applications

**Cloud-Specific**:

- Azure AD / Entra ID integration with Passport.js
- AWS Cognito with `amazon-cognito-identity-js`
- Google Identity Platform support

**On-Premise**:

- LDAP/Active Directory integration with `passport-ldapauth`
- SAML 2.0 SSO with `passport-saml`
- Custom JWT validation with `jsonwebtoken`

### API Client & Resilience

**MUST** use: `@YOUR_ORG/api-client` package
**Requirements**:

- Use `createApiClient()` factory for external service calls
- Configure timeout, retry attempts (exponential backoff), circuit breaker
- Never use raw `axios`, `node-fetch`, `got`, or `undici` directly
- All external calls auto-instrumented for distributed tracing

**Features**:

- Automatic retry with jitter and exponential backoff
- Timeout handling with graceful degradation
- Circuit breaker patterns (open, half-open, closed states)
- Distributed tracing with OpenTelemetry
- Request/response interceptors for logging, authentication
- Connection pooling and keep-alive
- Request deduplication for idempotent operations

**Recommended Base Library**:
- `undici` (Node.js 18+): Fast, standards-compliant HTTP/1.1 client
- `axios` 1.x: Battle-tested, large ecosystem (slower than undici)

**Cloud-Specific**:

- Azure Service Bus SDK for reliable messaging
- AWS SDK v3 for SQS/SNS/EventBridge

**On-Premise**:

- `amqplib` for RabbitMQ (reliable delivery patterns)
- `kafkajs` for Apache Kafka (exactly-once semantics)

### Database - SQL (PostgreSQL, MySQL)

**SHOULD** use one of:

- **Prisma 5.x**: Type-safe ORM with excellent DX, migrations, schema introspection (recommended)
- **TypeORM 0.3.x**: Mature ORM, Active Record or Data Mapper pattern
- **Drizzle ORM**: Lightweight, SQL-like API, excellent performance
- **Sequelize 6.x**: Mature ORM (falling out of favor due to maintenance issues)
- **Knex.js**: SQL query builder (not ORM), flexible, good for complex queries

**MUST** use with `@YOUR_ORG/database-extensions`
**Requirements**:

- Define schema with TypeScript types
- Use migrations for schema changes (never manual SQL)
- Apply migrations on deployment automatically
- Entities include audit fields (createdAt, updatedAt, createdBy, updatedBy)

**Prisma Best Practices**:

- Use Prisma schema for single source of truth
- Generate Prisma Client after schema changes
- Use `prisma migrate dev` for development, `prisma migrate deploy` for production
- Use Prisma Studio for database exploration
- Enable query logging in development

**Supported Databases**:

- PostgreSQL 14+ (cloud: Azure Database, AWS RDS, on-premise)
- MySQL 8+ / MariaDB 10.6+ (cloud: Azure, AWS, on-premise)
- SQL Server (via `tedious` driver)
- SQLite (development/testing only)

**Cloud-Specific**:

- Use connection pooling with PgBouncer (PostgreSQL)
- Use managed identity authentication (Azure, AWS)
- Use read replicas for read-heavy workloads

### Database - NoSQL (MongoDB)

**SHOULD** use:
- **Mongoose 8.x**: Schema-based ODM with validation, middleware, plugins (recommended)
- **MongoDB Native Driver 6.x**: Low-level driver for performance-critical scenarios
- **Prisma with MongoDB connector**: Type-safe MongoDB access

**MUST** use with `@YOUR_ORG/mongoose-plugins`
**Requirements**:

- Apply `auditPlugin` to schemas for automatic timestamps
- Define schemas with TypeScript types or interfaces
- Use connection pooling and retry logic
- Use indexes for frequently queried fields

**Cloud-Specific**:

- Azure Cosmos DB (MongoDB API)
- AWS DocumentDB (MongoDB-compatible)
- MongoDB Atlas (fully managed)

**On-Premise**:

- MongoDB 6.0+ with replica sets for high availability
- Sharding for horizontal scalability

### Database - Redis (Caching, Sessions)

**MUST** use:
- **ioredis 5.x**: Feature-rich Redis client with Cluster, Sentinel, TypeScript support (recommended)
- **redis 4.x**: Official Node Redis client (simpler API)

**Requirements**:

- Use connection pooling
- Implement error handling and reconnection logic
- Use Redis for caching, session storage, rate limiting, pub/sub

**Use Cases**:

- Response caching with TTL
- Session storage for stateful apps
- Rate limiting counters
- Pub/Sub for real-time features
- Job queues with BullMQ

**Cloud-Specific**:

- Azure Cache for Redis (managed)
- AWS ElastiCache for Redis (managed)

**On-Premise**:

- Redis 7+ with Sentinel for high availability
- Redis Cluster for horizontal scalability

### Logging & Observability

**MUST** use: `@YOUR_ORG/logger` package (wraps Pino or Winston)
**Requirements**:

- Use structured logging with JSON format
- Include correlation ID, trace ID in all log statements
- Never log PII, secrets, passwords, tokens, credit card numbers, SSNs
- Export logs to corporate logging platform (Elasticsearch, Splunk, Azure Monitor, AWS CloudWatch)

**Recommended Logger**:
- **Pino 8.x**: Ultra-fast JSON logger, child loggers, transport streams (recommended)
- **Winston 3.x**: Feature-rich, multiple transports (slower than Pino)

**Log Levels**:

- **trace**: Detailed diagnostic information (disabled in production)
- **debug**: Development debugging (disabled in production)
- **info**: General informational messages
- **warn**: Unexpected behavior that doesn't prevent operation
- **error**: Errors requiring investigation
- **fatal**: System failures requiring immediate attention

**NEVER**:

- Use `console.log()`, `console.error()`, `console.warn()` for logging
- Log synchronously (blocks event loop)

**Distributed Tracing**:

- Enable OpenTelemetry instrumentation for HTTP, database, messaging
- Export traces to Jaeger, Zipkin, Azure Application Insights, AWS X-Ray
- Use trace context propagation (W3C Trace Context standard)
- Implement trace sampling strategies for high-throughput systems

### Validation

**MUST** use one of:

- **Zod 3.x**: TypeScript-first schema validation, type inference (recommended for TypeScript)
- **Joi 17.x**: Feature-rich validation, widely adopted (JavaScript-friendly)
- **Ajv 8.x**: JSON Schema validator, fastest validation (good for high-performance APIs)
- **class-validator**: Decorator-based validation (NestJS default)

**Requirements**:

- Define validation schemas for all API requests
- Validate inputs in middleware or route handlers
- Return 400 Bad Request with structured errors for validation failures
- Use schema coercion for type conversion (string to number, etc.)

**Zod Best Practices**:

- Export schemas and infer TypeScript types (`z.infer<typeof schema>`)
- Use schema composition for reusability
- Use `refine()` for custom validation logic
- Use `transform()` for data transformation

### Background Jobs & Scheduling

**MUST** use one of:

- **BullMQ 5.x**: Redis-based job queue, reliable, distributed, rate limiting (recommended)
- **Agenda 5.x**: MongoDB-based job scheduling
- **node-cron**: Simple cron-like scheduler (no persistence)
- **node-schedule**: Time-based job scheduler (no persistence)

**Requirements**:

- Use persistent storage (Redis, MongoDB) for job state
- Implement idempotent job handlers (support retries)
- Use queues for prioritization
- Monitor job success/failure rates
- Use worker processes for CPU-intensive jobs

**Use Cases**:

- Scheduled report generation
- Email/notification sending (with retry)
- Data synchronization tasks
- Image/video processing
- Batch data imports

**Cloud-Specific**:

- Azure Functions with Durable Functions for orchestration
- AWS Lambda with EventBridge Scheduler
- AWS SQS + Lambda for event-driven processing

**On-Premise**:

- BullMQ with Redis for job persistence
- Kubernetes CronJobs for scheduled tasks

### API Documentation

**MUST**:

- Generate OpenAPI/Swagger documentation automatically
- Use one of:
  - **swagger-jsdoc + swagger-ui-express**: JSDoc comments → OpenAPI (Express/Fastify)
  - **@fastify/swagger + @fastify/swagger-ui**: Native Fastify plugin with JSON Schema
  - **@nestjs/swagger**: Decorator-based OpenAPI generation (NestJS)
  - **tsoa**: TypeScript decorators → OpenAPI + Express routes (generates routes from decorators)

**Requirements**:

- Include request/response examples with schemas
- Document error responses and status codes
- Expose Swagger UI at `/api-docs` (development only)
- Export OpenAPI spec at `/api-docs/json` for API gateway registration
- Version APIs explicitly (URL versioning `/api/v1/...`)

### Process Management

**MUST** use for production:

- **PM2**: Process manager with clustering, auto-restart, monitoring, log management
- **Docker + Orchestration**: Kubernetes, Docker Swarm, ECS (containerized deployments)

**PM2 Features**:

- Process clustering (utilize all CPU cores)
- Zero-downtime reloads
- Automatic restart on crashes
- Log rotation and management
- Startup scripts for system boot

**NEVER**:

- Run Node.js apps directly with `node index.js` in production

---

## Banned Libraries

**NEVER** use:

- Raw `axios`, `node-fetch`, `got`, `request` (deprecated) → Use `@YOUR_ORG/api-client`
- `express-jwt` without wrapper → Use `@YOUR_ORG/auth-middleware`
- `bcrypt` → Use `bcryptjs` (pure JS, no native deps) or `argon2` (more secure)
- `moment.js` (discontinued) → Use `date-fns`, `dayjs`, or `luxon`
- `console.log()` → Use proper logging (`@YOUR_ORG/logger`)
- `nodemon` in production → Use PM2 or container orchestration

**Security Concerns**:

- Avoid packages with known vulnerabilities (run `npm audit`)
- Avoid unmaintained packages (check last publish date, GitHub activity)
- Prefer packages with TypeScript support

**Rationale**: Corporate libraries enforce security, observability, compliance; deprecated libraries lack support

---

## Architecture

### Project Structure - Feature-Based (Recommended)

**SHOULD** use: Domain/feature-based organization for better cohesion

```text
src/
├── features/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.repository.ts
│   │   ├── auth.types.ts
│   │   └── auth.routes.ts
│   ├── users/
│   └── orders/
├── shared/
│   ├── middleware/
│   ├── utils/
│   └── types/
├── infrastructure/
│   ├── database/
│   ├── cache/
│   └── messaging/
├── config/
└── app.ts
```

**Benefits**: Better encapsulation, easier navigation, clearer boundaries

### Project Structure - Layered (Acceptable)

**MAY** use: Traditional layered architecture for simple applications

```text
src/
├── routes/          # Route definitions
├── controllers/     # Request/response handling
├── services/        # Business logic
├── repositories/    # Data access
├── models/          # Database schemas, types
├── middleware/      # Custom middleware
├── utils/           # Utility functions
├── config/          # Configuration
└── app.ts
```

### Separation of Concerns

**MUST**:

- Keep route handlers thin (routing only)
- Keep controllers thin (validation, serialization, error handling)
- Put business logic in service layer
- Use repositories or models for database access
- Never put business logic in controllers or repositories

### Type Safety

**MUST**:

- Use TypeScript for all new code
- Define types/interfaces for:
  - Request/response bodies
  - Database models
  - Service method signatures
  - Configuration objects
- Enable strict mode in `tsconfig.json`:
  - `"strict": true`
  - `"noUncheckedIndexedAccess": true`
  - `"noImplicitOverride": true`

**TypeScript Configuration**:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true
  }
}
```

### Error Handling

**MUST**:

- Use centralized error handling middleware
- Create custom error classes extending `Error`
- Return generic error messages to clients (no internal details, stack traces)
- Log full error details server-side with stack traces and correlation IDs
- Return RFC 7807 Problem Details for API errors

**Status Code Mapping**:

- ValidationError → 400 Bad Request
- UnauthorizedError → 401 Unauthorized
- ForbiddenError → 403 Forbidden
- NotFoundError → 404 Not Found
- ConflictError → 409 Conflict
- UnprocessableEntityError → 422 Unprocessable Entity
- InternalServerError → 500 Internal Server Error
- ServiceUnavailableError → 503 Service Unavailable

**Express Error Middleware**:

```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  logger.error({ err, req }, 'Unhandled error');
  
  if (err instanceof ValidationError) {
    return res.status(400).json({ error: err.message, details: err.errors });
  }
  
  // Generic error response (don't leak details)
  res.status(500).json({ error: 'Internal server error', requestId: req.id });
});
```

---

## Security

### Input Validation

**MUST**:

- Validate all API inputs using Zod, Joi, or Ajv
- Return 400 Bad Request with structured errors for validation failures
- Sanitize user inputs before processing (XSS prevention)
- Validate file uploads (type, size, content)
- Use `express-validator` or schema validation middleware

**XSS Prevention**:

- Use `helmet` middleware for security headers
- Use `xss-clean` middleware to sanitize user input
- Never use `dangerouslySetInnerHTML` in frontend (if applicable)

### SQL/NoSQL Injection Prevention

**MUST**:

- Use ORM/ODM (Prisma, TypeORM, Mongoose) for parameterized queries
- Never concatenate strings for database queries
- Use query parameters for all dynamic values
- Use Prisma's type-safe query API to prevent SQL injection

**MongoDB Injection Prevention**:

- Use Mongoose schema validation
- Never pass user input directly to MongoDB queries
- Sanitize inputs with `mongo-sanitize`

### Secrets Management

**MUST**:

- Store secrets in environment variables or corporate secrets manager
- Load secrets via `process.env` (never hardcode)
- Use `.env` files for local development (gitignored)
- Use `dotenv` package to load environment variables
- Rotate secrets regularly (automated via secret manager)

**NEVER**:

- Hardcode secrets in code or configuration files
- Commit secrets to source control (use `.gitignore` for `.env`)
- Store secrets in plain text environment variables (production)

**Configuration Hierarchy** (lowest to highest priority):

1. Default config file (non-sensitive defaults)
2. Environment-specific config files
3. `.env` file (local development)
4. Environment variables
5. Azure Key Vault / AWS Secrets Manager / HashiCorp Vault (production)

**Cloud-Specific**:

- Azure Key Vault with managed identity
- AWS Secrets Manager with IAM roles
- Use `@azure/keyvault-secrets` or AWS SDK for secret retrieval

**Best Practice**: Use `dotenv-safe` to enforce required environment variables

### Rate Limiting

**MUST**:

- Implement rate limiting on public endpoints
- Use `@YOUR_ORG/rate-limiter` or `express-rate-limit` / `@fastify/rate-limit`
- Configure limits based on:
  - IP address (anonymous users)
  - User ID (authenticated users)
  - API key (service accounts)
- Return 429 Too Many Requests when limits exceeded

**Strategies**:

- Token bucket algorithm
- Sliding window counter
- Fixed window counter
- Redis-based distributed rate limiting

### HTTPS & Security Headers

**MUST**:

- Use HTTPS in production environments (TLS 1.3)
- Use `helmet` middleware for security headers (Express)
- Use `@fastify/helmet` for security headers (Fastify)

**Security Headers** (helmet provides):

- Content-Security-Policy (CSP)
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY or SAMEORIGIN
- X-XSS-Protection: 0 (rely on CSP)
- Strict-Transport-Security (HSTS)
- Referrer-Policy: no-referrer
- Permissions-Policy

### CORS Configuration

**MUST**:

- Configure CORS restrictively (don't use `*` for origins)
- Use `cors` middleware (Express) or `@fastify/cors` (Fastify)
- Whitelist specific origins
- Configure credentials, methods, headers appropriately

### Authentication Best Practices

**SHOULD**:

- Use bcrypt or argon2 for password hashing (min 12 rounds for bcrypt)
- Implement password complexity requirements
- Support multi-factor authentication (MFA) for sensitive operations
- Use JWTs with short expiration (15 min) + refresh tokens (7 days)
- Store refresh tokens in database (allow revocation)
- Use secure, httpOnly, sameSite cookies for tokens (if cookie-based auth)

---

## Coding Standards

### Node.js & TypeScript Version

**MUST**:

- Use Node.js 20 LTS or Node.js 22 LTS
- Use TypeScript 5.3+ with strict mode enabled
- Target ES2022 or ESNext for modern features

### Code Style

**MUST**:

- Use ESLint 8.x+ for linting (with TypeScript plugin)
- Use Prettier 3.x for formatting
- Follow Airbnb TypeScript style guide or Google TypeScript style guide
- Use `eslint-config-prettier` to avoid conflicts

**ESLint Configuration**:

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json"
  }
}
```

### Naming Conventions

**MUST** follow:

- Functions, variables, parameters: `camelCase`
- Classes, Interfaces, Types, Enums: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Files: `kebab-case.ts` or `camelCase.ts` (be consistent)
- Private class members: `_leadingUnderscore` (optional, prefer TypeScript `private`)

### Async/Await

**MUST**:

- Use async/await for all asynchronous operations (no callbacks)
- Handle promise rejections with try/catch or `.catch()`
- Never use callback-style APIs for new code (use `util.promisify()` if needed)
- Use `Promise.all()` for parallel operations
- Use `Promise.allSettled()` when some promises may fail

**NEVER**:

- Mix callbacks and promises in the same codebase
- Use nested callbacks (callback hell)
- Ignore unhandled promise rejections

**Unhandled Rejection Handling**:

```typescript
process.on('unhandledRejection', (reason, promise) => {
  logger.error({ reason, promise }, 'Unhandled Promise Rejection');
  // Consider exiting process in production
  process.exit(1);
});
```

### Code Quality

**SHOULD**:

- Keep functions under 50 lines (extract to helper functions)
- Limit cyclomatic complexity (< 10 per function)
- Write meaningful names (avoid abbreviations, no single letters except loops)
- Use functional programming patterns (immutability, pure functions)
- Use `const` by default, `let` only when reassignment needed, avoid `var`
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Use template literals for string interpolation
- Use destructuring for cleaner code

### Performance Optimization

**SHOULD**:

- Use streams for large file processing (avoid loading entire file in memory)
- Use worker threads for CPU-intensive tasks (avoid blocking event loop)
- Use connection pooling for databases
- Use caching strategies (in-memory, Redis) for frequently accessed data
- Profile hot paths with Node.js profiler or clinic.js
- Monitor event loop lag with `perf_hooks`

**Avoid Event Loop Blocking**:

- Use asynchronous I/O operations
- Use `setImmediate()` for breaking up CPU-intensive work
- Use worker threads for heavy computation
- Monitor event loop delay (target < 10ms)

---

## Dependency Management

**MUST**:

- Use `package-lock.json` (npm) or `yarn.lock` (yarn) or `pnpm-lock.yaml` (pnpm) for deterministic installs
- Pin versions for production dependencies
- Use `~` (tilde) or `^` (caret) for development dependencies only
- Use `npm ci` or `yarn install --frozen-lockfile` in CI/CD (not `npm install`)

**SHOULD**:

- Keep dependencies up to date (security patches)
- Audit dependencies regularly (`npm audit`, `yarn audit`)
- Use `npm-check-updates` or Renovate bot for dependency updates
- Remove unused dependencies (`depcheck` tool)

**Package Manager Choice**:

- **npm 10.x**: Standard, bundled with Node.js
- **yarn 4.x (Berry)**: Faster, better monorepo support, Plug'n'Play
- **pnpm 8.x**: Most efficient disk usage, fastest install (recommended for monorepos)

---

## Testing

### Unit Testing

**MUST**:

- Write unit tests using Jest 29.x or Vitest 1.x
- Aim for 80%+ coverage on business logic
- Use AAA pattern (Arrange, Act, Assert)
- Mock external dependencies (databases, HTTP calls)

**SHOULD**:

- Use `jest.mock()` for mocking modules
- Use `jest.spyOn()` for spying on functions
- Use `@faker-js/faker` for generating test data
- Use `ts-jest` for TypeScript support in Jest

**Testing Framework Choice**:

- **Jest 29.x**: Most popular, snapshot testing, built-in mocking (slower startup)
- **Vitest 1.x**: Vite-powered, faster, Jest-compatible API (recommended for new projects)
- **Mocha + Chai**: Flexible, requires more setup (legacy projects)

### Integration Testing

**MUST**:

- Write integration tests for API endpoints
- Use Supertest for HTTP endpoint testing (Express, Fastify)
- Test database interactions with test containers (Testcontainers for Node.js)
- Use separate test databases (never production)

**SHOULD**:

- Use `@testcontainers/postgresql`, `@testcontainers/mongodb` for realistic test environments
- Use `nock` for mocking external HTTP APIs
- Use `dockerode` for Docker-based integration tests
- Reset database state between tests

### E2E Testing

**SHOULD**:

- Use Playwright or Cypress for UI testing (if applicable)
- Run E2E tests in CI/CD pipeline
- Test critical user journeys only (expensive to maintain)

### Test Naming

**MUST** follow:

- Describe: `describe('FeatureName', () => { ... })`
- Test: `it('should do something when condition', () => { ... })`
- Use descriptive test names (no abbreviations)

---

## Build & Deployment

### Build Process

**MUST**:

- Use TypeScript compiler (`tsc`) for production build
- Run tests before deployment (`npm test` or `yarn test`)
- Run linters before deployment (`npm run lint`)
- Generate source maps for debugging

**Build Scripts** (package.json):

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "test": "jest",
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix",
    "format": "prettier --write src/**/*.ts"
  }
}
```

**CI/CD**:

- Run linters (ESLint, Prettier)
- Run security scanning (npm audit, Snyk, Trivy)
- Generate code coverage reports (Istanbul, c8)
- Publish packages to corporate npm registry

### Docker - Cloud Deployments

**MUST**:

- Use multi-stage builds (build dependencies in build stage)
- Use official Node.js Alpine base images:
  - Build: `node:20-alpine` or `node:22-alpine`
  - Runtime: Same as build (Node.js includes runtime)
- Run as non-root user in container
- Copy only necessary files (use `.dockerignore`)
- Use layer caching for faster builds

**Dockerfile Example**:

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package*.json ./
USER nodejs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**SHOULD**:

- Keep container images small (< 150MB for simple services)
- Use health checks in Dockerfile (`HEALTHCHECK` instruction)
- Set resource limits (CPU, memory) in container runtime
- Use `.dockerignore` to exclude node_modules, tests, dev dependencies

**Cloud-Specific**:

- **Azure**: Deploy to Azure Container Apps, Azure Kubernetes Service (AKS), Azure App Service
- **AWS**: Deploy to ECS, EKS, Elastic Beanstalk, Lambda (serverless)
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
- Implement liveness and readiness probes (`/health/live`, `/health/ready`)
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
- Check critical dependencies: database, cache, message queue, external APIs

**Implementation**:

```typescript
app.get('/health/live', (req, res) => {
  res.status(200).json({ status: 'UP' });
});

app.get('/health/ready', async (req, res) => {
  try {
    await db.ping();
    await redis.ping();
    res.status(200).json({ status: 'UP', checks: { db: 'UP', redis: 'UP' } });
  } catch (err) {
    res.status(503).json({ status: 'DOWN', error: err.message });
  }
});
```

### Metrics

**MUST** include:

- Expose metrics endpoint (`/metrics`) in Prometheus format
- Track request rate, error rate, duration (RED metrics)
- Track Node.js runtime metrics (event loop lag, heap usage, GC)
- Track custom business metrics (orders/sec, revenue)

**Tools**:

- **prom-client**: Prometheus client for Node.js
- Prometheus for metric collection
- Grafana for visualization
- Azure Monitor, AWS CloudWatch for cloud deployments

**Example Metrics**:

- HTTP request duration histogram
- HTTP request total counter (by status code, method, endpoint)
- Active connections gauge
- Event loop lag gauge
- Heap memory usage gauge

### Distributed Tracing

**MUST**:

- Enable OpenTelemetry instrumentation
- Export traces to Jaeger, Zipkin, Azure Application Insights, AWS X-Ray
- Include trace context (traceId, spanId) in all outgoing requests
- Implement custom spans for critical operations

**OpenTelemetry Setup**:

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';

const sdk = new NodeSDK({
  traceExporter: new JaegerExporter(),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

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
- **Asynchronous**: Message queues (RabbitMQ, Kafka, Azure Service Bus, AWS SQS/SNS) for event-driven

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

- Consul for service registry
- Kubernetes DNS for container-based services

### API Gateway

**SHOULD** use:

- **Azure**: Azure API Management
- **AWS**: AWS API Gateway, AWS App Mesh
- **Self-hosted**: Express Gateway, Kong, Tyk

**Features**: Rate limiting, authentication, request routing, load balancing, caching

---

## Performance & Scalability

### Clustering (Multi-Core Utilization)

**MUST** use for production:

- PM2 with cluster mode (`pm2 start app.js -i max`)
- Node.js native cluster module (manual management)
- Kubernetes with multiple replicas (horizontal scaling)

**Worker Threads**:

- Use for CPU-intensive tasks (image processing, cryptography, data transformation)
- Don't use for I/O-bound tasks (use async/await instead)

### Caching Strategy

**SHOULD**:

- Cache frequently accessed, rarely changed data
- Use in-memory cache (`node-cache`, `lru-cache`) for single-instance apps
- Use distributed cache (Redis) for multi-instance deployments
- Implement cache-aside pattern with appropriate TTL
- Use cache invalidation strategies (time-based, event-based)

### Database Optimization

**SHOULD**:

- Use connection pooling (configured in ORM/driver)
- Use indexes on frequently queried fields
- Use read replicas for read-heavy workloads
- Implement database sharding for extreme scale
- Use query optimization (avoid N+1 queries)

### Horizontal Scaling

**MUST**:

- Design stateless services (store session in Redis, database)
- Use load balancers (Azure Load Balancer, AWS ELB, NGINX, HAProxy)
- Implement auto-scaling based on metrics (CPU, memory, request rate)

---

## Compliance & Governance

### Data Protection

**MUST**:

- Implement GDPR, CCPA, LGPD compliance for personal data
- Encrypt data at rest and in transit (TLS 1.3, AES-256)
- Implement data retention policies (automated cleanup)
- Support data export and deletion requests (right to be forgotten)

### Audit Logging

**MUST**:

- Log all data access and modifications
- Include user identity, timestamp, operation type, IP address
- Store audit logs separately from application logs
- Retain audit logs per regulatory requirements

### Code Analysis

**SHOULD**:

- Use SonarQube for static code analysis
- Use npm audit, Snyk, or Dependabot for dependency scanning
- Run security scanning in CI/CD pipeline (SAST, DAST)
- Use Trivy for container image scanning

---

## Non-Compliance

If corporate library unavailable or causes blocking issue:

1. Document violation in `.guidelines-todo.md` with justification and business impact
2. Create ticket to resolve (target: next sprint)
3. Proceed with alternative, mark with `// TODO: GUIDELINE-VIOLATION - Ticket #XXX` comment for tracking
4. Schedule tech debt review within 30 days
