# Node.js Base Guidelines

**Tech Stack**: Node.js 20/22 LTS, TypeScript 5+, Express/Fastify/NestJS, Backend Services, APIs
**Auto-detected from**: `package.json` with backend dependencies (express, fastify, koa, hapi)
**Version**: 3.0 (Profile-Based Architecture)
**Last Updated**: 2025-11-16

---

## Target Platform

**MUST**:

- Use Node.js 20 LTS (Active until April 2026) or Node.js 22 LTS (Active until April 2027)
- Use TypeScript 5.3+ for all new projects
- Target ES2022 or ESNext in `tsconfig.json`

**SHOULD**:

- Upgrade to Node.js 22 LTS when infrastructure supports it
- Use native Node.js test runner for simple cases
- Leverage new features (native fetch, test runner, watch mode)

**Rationale**: LTS provides 3 years active support + 18 months maintenance; TypeScript ensures type safety and maintainability

---

## Framework Selection

**Options**:

- **Express 4.x/5.x**: Most popular, largest ecosystem, traditional middleware
- **Fastify 4.x**: High performance (3x faster), schema validation, plugin architecture
- **NestJS 10.x**: TypeScript-first, Angular-inspired, DI, great for large teams
- **Koa 2.x**: Minimalist, async/await-first (smaller ecosystem)
- **Hapi 21.x**: Configuration-driven, enterprise features

**Recommendation**: Fastify for new high-performance APIs, NestJS for large applications, Express for standard projects

---

## Architecture

### Project Structure (Express/Fastify)

```text
src/
├── controllers/         # Request handlers
├── services/            # Business logic
├── repositories/        # Data access layer
├── middleware/          # Custom middleware
├── models/              # Data models/schemas
├── routes/              # Route definitions
├── config/              # Configuration
├── utils/               # Utilities
├── types/               # TypeScript types
└── server.ts            # Entry point
```

### Project Structure (NestJS)

```text
src/
├── modules/
│   ├── users/
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   ├── users.module.ts
│   │   └── dto/
│   └── auth/
├── common/              # Shared code
│   ├── guards/
│   ├── interceptors/
│   ├── filters/
│   └── pipes/
├── config/
└── main.ts
```

### Separation of Concerns

**MUST**:

- Controllers handle HTTP requests/responses only
- Services contain business logic
- Repositories handle data access
- Models define data structures
- Middleware handles cross-cutting concerns

---

## Security

### Input Validation

**MUST**:

- Validate all inputs with Zod, Joi, or class-validator
- Sanitize inputs to prevent injection attacks
- Use parameterized queries (SQL injection prevention)
- Validate request body, query params, headers

**Example (Zod)**:

```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().min(18).max(120)
});

app.post('/users', async (req, res) => {
  const validated = userSchema.parse(req.body);
  // Use validated data
});
```

### Environment Variables

**MUST**:

- Never hardcode secrets in code
- Use `.env` files (gitignored) for local development
- Validate environment variables at startup
- Use different `.env` files per environment

**Validation Example**:

```typescript
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32)
});

export const env = envSchema.parse(process.env);
```

### Authentication & Authorization

**MUST**:

- Use JWT or session-based authentication
- Store tokens securely (httpOnly cookies for browsers)
- Implement role-based access control (RBAC)
- Use bcrypt/argon2 for password hashing (never plain text)

**JWT Example**:

```typescript
import jwt from 'jsonwebtoken';

function generateToken(userId: string) {
  return jwt.sign({ userId }, env.JWT_SECRET, {
    expiresIn: '7d'
  });
}

function verifyToken(token: string) {
  return jwt.verify(token, env.JWT_SECRET);
}
```

### Rate Limiting

**MUST** implement rate limiting:

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later'
});

app.use('/api/', limiter);
```

### CORS

**MUST** configure CORS properly:

```typescript
import cors from 'cors';

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(','),
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
}));
```

---

## Database

### ORM Selection

**Recommended**:

- **Prisma 5.x**: Type-safe, excellent DX, migrations (recommended)
- **TypeORM 0.3.x**: Mature, Active Record or Data Mapper
- **Drizzle ORM**: Lightweight, SQL-like, performant
- **Mongoose 8.x**: For MongoDB, schema-based ODM

**Best Practices**:

- Use migrations for schema changes
- Never run raw SQL without parameterization
- Include audit fields (createdAt, updatedAt)
- Use transactions for multi-step operations

**Prisma Example**:

```typescript
// schema.prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

// Usage
const user = await prisma.user.create({
  data: { email: 'user@example.com', name: 'John' }
});
```

### Connection Pooling

**MUST**:

- Configure connection pools
- Set min/max connections
- Handle connection errors gracefully
- Use connection retry logic

---

## Error Handling

### Global Error Handler

**MUST** implement centralized error handling:

```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);

  if (err instanceof ValidationError) {
    return res.status(400).json({ error: err.message });
  }

  if (err instanceof UnauthorizedError) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  res.status(500).json({
    error: 'Internal server error',
    ...(env.NODE_ENV === 'development' && { details: err.message })
  });
});
```

### Custom Error Classes

```typescript
class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(message: string) {
    super(400, message);
  }
}
```

---

## Logging

**MUST** use structured logging:

**Recommended Libraries**:

- **Pino**: Fast, structured logging (recommended)
- **Winston**: Feature-rich, transports, formatters
- **Bunyan**: Structured logging (older)

**Pino Example**:

```typescript
import pino from 'pino';

const logger = pino({
  level: env.LOG_LEVEL || 'info',
  transport: env.NODE_ENV === 'development' ? {
    target: 'pino-pretty'
  } : undefined
});

logger.info({ userId: '123' }, 'User logged in');
logger.error({ err }, 'Database connection failed');
```

**Best Practices**:

- Log at appropriate levels (debug, info, warn, error, fatal)
- Include context (userId, requestId, timestamp)
- Never log sensitive data (passwords, tokens, PII)
- Use correlation IDs for request tracing

---

## Testing

### Unit Testing

**MUST** use:

- **Vitest** (recommended, fast)
- **Jest** (popular, mature)

**Example**:

```typescript
import { describe, it, expect } from 'vitest';

describe('UserService', () => {
  it('should create user', async () => {
    const user = await userService.create({
      email: 'test@example.com'
    });

    expect(user).toHaveProperty('id');
    expect(user.email).toBe('test@example.com');
  });
});
```

### Integration Testing

**Test API endpoints**:

```typescript
import supertest from 'supertest';
import { app } from './app';

const request = supertest(app);

describe('POST /users', () => {
  it('should create user', async () => {
    const response = await request
      .post('/users')
      .send({ email: 'test@example.com', password: 'secret123' })
      .expect(201);

    expect(response.body).toHaveProperty('id');
  });
});
```

---

## Performance

### Async/Await Best Practices

**MUST**:

- Use async/await over callbacks
- Handle errors with try/catch
- Avoid blocking the event loop
- Use Promise.all() for parallel operations

**Example**:

```typescript
// ❌ Bad - sequential
const user = await getUser(id);
const posts = await getPosts(user.id);
const comments = await getComments(user.id);

// ✅ Good - parallel
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
```

### Caching

**SHOULD** implement caching:

- **Redis**: Distributed caching
- **Node-cache**: In-memory caching
- **HTTP caching**: ETags, Cache-Control headers

### Connection Pooling

**MUST** configure properly:

```typescript
// Database connection pool
const pool = {
  min: 2,
  max: 10,
  idleTimeoutMillis: 30000
};
```

---

## API Design

### RESTful Best Practices

**MUST**:

- Use proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Use plural resource names (`/users`, not `/user`)
- Use HTTP status codes correctly
- Version APIs (`/v1/users`)

**Status Codes**:

- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

### Request/Response Format

**MUST** use consistent format:

```typescript
// Success
{
  "data": { ... },
  "meta": {
    "timestamp": "2025-11-16T00:00:00Z"
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": { ... }
  }
}
```

---

## Deployment

### Process Management

**MUST** use:

- **PM2**: Production process manager
- **Docker**: Containerization
- **systemd**: Linux service management

**PM2 Example**:

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'api',
    script: './dist/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
```

### Health Checks

**MUST** implement:

```typescript
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

app.get('/ready', async (req, res) => {
  try {
    await db.ping();
    res.json({ status: 'ready' });
  } catch (error) {
    res.status(503).json({ status: 'not ready' });
  }
});
```

### Graceful Shutdown

**MUST** handle shutdown gracefully:

```typescript
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, closing server...');

  server.close(async () => {
    await db.disconnect();
    await redis.quit();
    process.exit(0);
  });
});
```

---

## TypeScript Configuration

**MUST**:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

---

## Coding Standards

### Naming Conventions

- Files: kebab-case (`user-service.ts`)
- Classes: PascalCase (`UserService`)
- Functions/variables: camelCase (`getUserById`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- Interfaces: PascalCase (`IUserRepository` or `UserRepository`)

### Code Organization

**MUST**:

- One class/function per file (for large classes)
- Group related files in folders
- Export from index files for clean imports

---

## Recommended Libraries

### Utilities

- **date-fns**: Date manipulation
- **lodash-es**: Utility functions (tree-shakeable)
- **zod**: Schema validation
- **dotenv**: Environment variables

### HTTP Clients

- **undici**: Fast HTTP/1.1 client (Node.js 18+)
- **axios**: Popular HTTP client

### Testing

- **vitest**: Fast testing framework
- **supertest**: HTTP assertion library
- **nock**: HTTP mocking

---

**Note**: These are base guidelines applicable to all Node.js projects. Project-specific requirements (corporate libraries, registries, deployment targets) are defined in profile overrides.
