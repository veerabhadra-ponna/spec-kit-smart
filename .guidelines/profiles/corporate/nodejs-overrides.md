# Node.js Corporate Profile Overrides

**Profile**: Corporate
**Stack**: Node.js
**Version**: 3.0
**Last Updated**: 2025-11-16

> **Note**: This file contains only corporate-specific overrides. Base guidelines are inherited from `base/nodejs-base.md`.

---

## Scaffolding

**MUST**:

- Use corporate scaffolding command (`@YOUR_ORG/create-node-service`)
- Choose appropriate template:
  - **express-ts**: Traditional Express with TypeScript
  - **fastify-ts**: High-performance Fastify with TypeScript
  - **nestjs**: Enterprise NestJS framework
  - **minimal-api**: Lightweight API
  - **microservice**: Event-driven with messaging
  - **graphql**: GraphQL API with Apollo
  - **grpc**: gRPC for inter-service communication

**NEVER**:

- Use `npm init`, `npx express-generator`, or public templates directly

**Rationale**: Corporate scaffolding includes security, logging, monitoring, compliance, observability from day one

---

## Package Registry

**MUST**:

- Configure `.npmrc` with corporate npm registry
- All dependencies resolved through corporate registry only
- Use authentication tokens (never plaintext passwords)

**NEVER**:

- Install packages from public npmjs.org directly

**Configuration**:

```text
registry=https://npm.yourorg.com
@yourorg:registry=https://npm.yourorg.com
//npm.yourorg.com/:_authToken=${NPM_TOKEN}
always-auth=true
```

---

## Mandatory Libraries

### Framework Starter

**MUST** use: `@YOUR_ORG/express-starter`, `@YOUR_ORG/fastify-starter`, or `@YOUR_ORG/nestjs-starter`

**Includes**: Security middleware, logging, metrics, error handling, CORS, rate limiting, health checks, observability

**Usage**:

```typescript
import { createApp } from '@YOUR_ORG/express-starter';

const app = createApp({
  serviceName: 'user-service',
  version: '1.0.0',
  auth: {
    provider: 'jwt',
    secret: env.JWT_SECRET
  }
});
```

---

### Authentication & Authorization

**MUST** use: `@YOUR_ORG/auth-middleware`

**Requirements**:

- Apply `authMiddleware()` globally or per-route
- Use `authorize([roles])` for RBAC
- Extract user via `req.user`
- Support JWT, OAuth 2.0, API keys

**Example**:

```typescript
import { authMiddleware, authorize } from '@YOUR_ORG/auth-middleware';

app.use(authMiddleware());

app.get('/admin/users',
  authorize(['admin']),
  async (req, res) => {
    // Only admins can access
  }
);
```

**Cloud-Specific**:

- Azure AD / Entra ID integration
- AWS Cognito integration
- LDAP/Active Directory (on-premise)

---

### API Client & Resilience

**MUST** use: `@YOUR_ORG/api-client`

**Requirements**:

- Use `createApiClient()` for external service calls
- Configure timeout, retry, circuit breaker
- Never use raw `axios`, `fetch`, `got`, or `undici` directly
- Auto-instrumented for distributed tracing

**Example**:

```typescript
import { createApiClient } from '@YOUR_ORG/api-client';

const orderClient = createApiClient({
  baseURL: 'https://api.yourorg.com/orders',
  timeout: 5000,
  retries: 3,
  circuitBreaker: {
    threshold: 0.5,
    timeout: 30000
  }
});

const order = await orderClient.get(`/orders/${id}`);
```

---

### Database Integration

**MUST** use: `@YOUR_ORG/database-extensions` with your ORM

**Requirements**:

- Define schema with TypeScript types
- Use migrations for schema changes
- Apply migrations on deployment
- Include audit fields (createdAt, updatedAt, createdBy, updatedBy)

**Supported ORMs**:

- Prisma 5.x (recommended)
- TypeORM 0.3.x
- Drizzle ORM
- Mongoose 8.x (for MongoDB)

**Prisma Example with Corporate Extensions**:

```typescript
import { PrismaClient } from '@prisma/client';
import { withAudit, withSoftDelete } from '@YOUR_ORG/database-extensions';

const prisma = new PrismaClient();
withAudit(prisma);
withSoftDelete(prisma);

// Auto-populates createdBy, updatedBy
const user = await prisma.user.create({
  data: { email: 'user@yourorg.com' }
});
```

---

### Logging & Monitoring

**MUST** use: `@YOUR_ORG/logger`

**Requirements**:

- Use structured logging
- Include correlation IDs
- Never log sensitive data (passwords, tokens, PII)
- Send logs to corporate logging service (Splunk, ELK, Azure Monitor)

**Example**:

```typescript
import { logger } from '@YOUR_ORG/logger';

logger.info({ userId, orderId }, 'Order created');
logger.error({ err, userId }, 'Order creation failed');
```

**Log Levels**:

- debug: Development debugging
- info: Informational messages
- warn: Warning messages
- error: Error messages
- fatal: Critical errors

---

### Metrics & Observability

**MUST** use: `@YOUR_ORG/metrics`

**Requirements**:

- Track request duration, throughput, error rate
- Custom business metrics (orders created, payments processed)
- Send to corporate APM (New Relic, Datadog, Dynatrace)

**Example**:

```typescript
import { metrics } from '@YOUR_ORG/metrics';

// Counter
metrics.increment('orders.created', { region: 'us-east' });

// Histogram
metrics.histogram('http.request.duration', duration, {
  method: 'GET',
  path: '/users'
});

// Gauge
metrics.gauge('database.connections', connectionPool.size);
```

---

## Banned Libraries

**NEVER** use without approval:

- **Public auth libraries**: passport.js, express-jwt → Use `@YOUR_ORG/auth-middleware`
- **Public HTTP clients**: axios, got, undici (raw) → Use `@YOUR_ORG/api-client`
- **Public loggers**: winston, bunyan → Use `@YOUR_ORG/logger`
- **Public monitoring**: No New Relic SDK directly → Use `@YOUR_ORG/metrics`

**Security Concerns**:

- All packages must pass corporate security review
- All packages must be available in corporate registry
- Avoid packages with known vulnerabilities

**Rationale**: Corporate libraries enforce security, compliance, audit trail, consistent monitoring

---

## Deployment

### Corporate CI/CD

**MUST**:

- Use corporate CI/CD pipeline (Jenkins, Azure DevOps, GitLab CI, GitHub Actions)
- Automated security scanning (Snyk, SonarQube)
- Automated testing (unit, integration)
- Code review (minimum 2 approvers)

**Pipeline Stages**:

1. Lint & Type Check
2. Unit Tests (80%+ coverage required)
3. Integration Tests
4. Security Scan
5. Build Docker Image
6. Deploy to Dev/Staging
7. E2E Tests
8. Deploy to Production (approval required)

### Environment Management

**MUST**:

- Use corporate cloud accounts (AWS, Azure, GCP)
- Tag all resources (cost center, project, environment)
- Use infrastructure as code (Terraform, CDK, Bicep)

### Process Management

**MUST** use:

- **Kubernetes**: Container orchestration (corporate standard)
- **PM2**: For VM-based deployments
- **Docker**: Containerization

**Dockerfile Example**:

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nodeapp
COPY --from=builder --chown=nodeapp:nodejs /app/dist ./dist
COPY --from=builder --chown=nodeapp:nodejs /app/node_modules ./node_modules
USER nodeapp
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

---

## Compliance

### Security Requirements

**MUST**:

- Pass corporate security review
- Implement OWASP Top 10 protections
- Enable WAF (Web Application Firewall)
- Use corporate SSL/TLS certificates
- Implement rate limiting and DDoS protection

### Audit & Logging

**MUST**:

- Log all authentication attempts
- Log all data access (read, write, delete)
- Retain logs per corporate policy (typically 90 days minimum)
- Enable tamper-proof logging
- Forward logs to SIEM

### Data Handling

**MUST**:

- Classify data per corporate data classification policy
- Encrypt sensitive data at rest and in transit
- Implement data masking for PII
- Support data export and deletion requests (GDPR)
- Never store payment card data (use tokenization)

---

## Non-Compliance

If corporate library unavailable or causes blocking issue:

1. Document in `.guidelines-todo.md` with justification and business impact
2. Create JIRA ticket for resolution (target: next sprint)
3. Get approval from Architecture Review Board
4. Proceed with alternative, mark with `// GUIDELINE-VIOLATION: Ticket #XXX`
5. Schedule tech debt review within 30 days

**Escalation**:

1. Team Lead (< 1 day deviation)
2. Engineering Manager (< 1 week deviation)
3. Architecture Review Board (> 1 week or security impact)
4. CTO (compliance or legal impact)

---

## Support & Resources

### Corporate Resources

- **Internal Wiki**: <https://wiki.yourorg.com/nodejs-guidelines>
- **API Documentation**: <https://api-docs.yourorg.com>
- **Slack Channel**: #backend-support
- **Office Hours**: Wednesdays 2-3 PM EST

### Training

- **Required**: Node.js Security Training (annual)
- **Required**: Corporate Libraries Workshop (for new hires)
- **Recommended**: Microservices Patterns
- **Recommended**: Performance Optimization

### Code Review Checklist

- [ ] Uses `@YOUR_ORG/express-starter` or equivalent
- [ ] Uses `@YOUR_ORG/auth-middleware` for auth
- [ ] Uses `@YOUR_ORG/api-client` for external calls
- [ ] Uses `@YOUR_ORG/logger` (no console.log)
- [ ] Uses `@YOUR_ORG/metrics` for monitoring
- [ ] No banned libraries
- [ ] Security scan passed (npm audit)
- [ ] Tests written and passing (80%+ coverage)
- [ ] `.npmrc` configured for corporate registry
- [ ] Environment variables validated
- [ ] No secrets in code

---

**Last Review**: 2025-11-16
**Next Review**: 2026-02-16 (quarterly)
**Owner**: Backend Architecture Team
**Contact**: <backend-arch@yourorg.com>
