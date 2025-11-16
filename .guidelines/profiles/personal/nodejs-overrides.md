# Node.js Personal/Public Profile Overrides

**Profile**: Personal/Public Open Source
**Stack**: Node.js
**Version**: 3.0
**Last Updated**: 2025-11-16

> **Note**: This file contains only personal/public project-specific overrides. Base guidelines are inherited from `base/nodejs-base.md`.

---

## Scaffolding

**RECOMMENDED**:

- **Express**: `npx express-generator --view=ejs --git`
- **Fastify**: `npm init fastify`
- **NestJS**: `npm i -g @nestjs/cli && nest new project-name`
- **Minimal**: Manual setup with express/fastify

**Starter Templates**:

- Express + TypeScript: <https://github.com/microsoft/TypeScript-Node-Starter>
- Fastify + TypeScript: <https://github.com/fastify/fastify-typescript-starter>
- NestJS: <https://docs.nestjs.com>

**Quick Start**:

```bash
# Express + TypeScript
npm create vite@latest my-api -- --template vanilla-ts
npm install express @types/express

# Fastify
npm init fastify

# NestJS
npm i -g @nestjs/cli
nest new my-api
```

---

## Package Registry

**RECOMMENDED**:

- Use official npm registry (<https://registry.npmjs.org>)
- Run `npm audit` regularly for security
- Consider `pnpm` for faster installs
- Consider `bun` for ultra-fast package management

**Security**:

```bash
# Check for vulnerabilities
npm audit

# Auto-fix
npm audit fix

# Use Dependabot for automated updates (GitHub)
```

---

## Recommended Libraries

### Framework Selection

**Express** (Most Popular):

```bash
npm install express
npm install -D @types/express
```

**Fastify** (High Performance):

```bash
npm install fastify
npm install -D @types/node
```

**NestJS** (Enterprise-Ready):

```bash
npm i -g @nestjs/cli
nest new project-name
```

---

### Authentication

**RECOMMENDED OPTIONS**:

1. **Passport.js** (Most flexible)
   - `npm install passport passport-jwt passport-local`
   - Multiple strategies (JWT, OAuth, local)
   - Website: <https://www.passportjs.org>

2. **express-jwt** (Simple JWT)
   - `npm install express-jwt jsonwebtoken`
   - Lightweight JWT middleware

3. **NextAuth.js** (If using Next.js)
   - `npm install next-auth`
   - OAuth providers, email, credentials
   - Website: <https://authjs.dev>

**Example (Passport.js + JWT)**:

```typescript
import passport from 'passport';
import { Strategy as JwtStrategy, ExtractJwt } from 'passport-jwt';

passport.use(new JwtStrategy({
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  secretOrKey: process.env.JWT_SECRET
}, (payload, done) => {
  // Verify user
  const user = await findUser(payload.userId);
  return done(null, user);
}));

app.use(passport.initialize());
app.use('/api', passport.authenticate('jwt', { session: false }));
```

---

### Database & ORM

**RECOMMENDED OPTIONS**:

1. **Prisma** (Recommended for SQL)
   - `npm install prisma @prisma/client`
   - Type-safe, excellent DX
   - Website: <https://www.prisma.io>

2. **Drizzle ORM** (Lightweight)
   - `npm install drizzle-orm`
   - SQL-like syntax
   - Website: <https://orm.drizzle.team>

3. **Mongoose** (For MongoDB)
   - `npm install mongoose`
   - Schema-based ODM
   - Website: <https://mongoosejs.com>

4. **Sequelize** (Mature ORM)
   - `npm install sequelize`
   - Supports multiple databases

**Quick Setup (Prisma)**:

```bash
npm install prisma @prisma/client
npx prisma init
```

```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id    String @id @default(cuid())
  email String @unique
  name  String?
}
```

```bash
npx prisma migrate dev
npx prisma generate
```

---

### Free Database Options

**PostgreSQL**:

- **Supabase**: 500MB database, free tier - <https://supabase.com>
- **Neon**: 10GB storage, free tier - <https://neon.tech>
- **Railway**: Free tier available - <https://railway.app>
- **ElephantSQL**: 20MB free tier - <https://www.elephantsql.com>

**MongoDB**:

- **MongoDB Atlas**: 512MB free tier - <https://www.mongodb.com/cloud/atlas>

**MySQL**:

- **PlanetScale**: 5GB storage free - <https://planetscale.com>

---

### HTTP Client

**RECOMMENDED**:

- **axios**: `npm install axios` - Battle-tested, popular
- **undici**: Built-in Node.js 18+ - Fast, standards-compliant
- **got**: `npm install got` - Promise-based

**Example (axios)**:

```typescript
import axios from 'axios';

const client = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 5000
});

const data = await client.get('/users');
```

---

### Validation

**RECOMMENDED**:

- **Zod**: `npm install zod` - TypeScript-first (recommended)
- **Joi**: `npm install joi` - Popular, mature
- **class-validator**: `npm install class-validator` - For NestJS

**Example (Zod)**:

```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().int().positive()
});

app.post('/users', async (req, res) => {
  const validated = userSchema.parse(req.body);
  // Use validated data
});
```

---

### Logging

**RECOMMENDED**:

- **Pino**: `npm install pino` - Fast, structured (recommended)
- **Winston**: `npm install winston` - Feature-rich
- **Morgan**: `npm install morgan` - HTTP request logger (Express)

**Example (Pino)**:

```typescript
import pino from 'pino';

const logger = pino({
  transport: {
    target: 'pino-pretty'
  }
});

logger.info('Server started');
logger.error({ err }, 'Database connection failed');
```

---

### Error Tracking

**RECOMMENDED OPTIONS**:

1. **Sentry** (Most popular)
   - `npm install @sentry/node`
   - Free tier: 5,000 events/month
   - Website: <https://sentry.io>

2. **Bugsnag**
   - `npm install @bugsnag/js`
   - Free tier: 7,500 events/month
   - Website: <https://www.bugsnag.com>

**Quick Setup (Sentry)**:

```bash
npm install @sentry/node
```

```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV
});

app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.errorHandler());
```

---

### Testing

**RECOMMENDED**:

- **Vitest**: `npm install -D vitest` - Fast, modern (recommended)
- **Jest**: `npm install -D jest ts-jest` - Popular, mature
- **Supertest**: `npm install -D supertest` - HTTP testing

**Example (Vitest + Supertest)**:

```bash
npm install -D vitest supertest @types/supertest
```

```typescript
import { describe, it, expect } from 'vitest';
import supertest from 'supertest';
import { app } from './app';

describe('GET /users', () => {
  it('should return users', async () => {
    const response = await supertest(app)
      .get('/users')
      .expect(200);

    expect(response.body).toBeInstanceOf(Array);
  });
});
```

---

## Deployment Platforms

**RECOMMENDED**:

1. **Railway** (Easiest, full-stack)
   - Free tier: $5 credit/month
   - Supports PostgreSQL, Redis
   - Website: <https://railway.app>

2. **Render** (Great free tier)
   - Free static sites
   - PostgreSQL databases
   - Website: <https://render.com>

3. **Fly.io** (Edge deployment)
   - Global deployment
   - Free tier available
   - Website: <https://fly.io>

4. **Vercel** (For Next.js/serverless)
   - Zero-config for Next.js
   - Serverless functions
   - Website: <https://vercel.com>

5. **Heroku** (Classic PaaS)
   - Eco dynos: $5/month
   - Easy deployment
   - Website: <https://heroku.com>

**Quick Deploy (Railway)**:

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

---

## Environment Management

**RECOMMENDED**:

```bash
npm install dotenv
```

```javascript
// .env (gitignored)
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://localhost:5432/mydb
JWT_SECRET=your-secret-key

// .env.example (committed)
NODE_ENV=
PORT=
DATABASE_URL=
JWT_SECRET=
```

```typescript
import 'dotenv/config';
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  DATABASE_URL: z.string(),
  JWT_SECRET: z.string().min(32)
});

export const env = envSchema.parse(process.env);
```

---

## Middleware

**RECOMMENDED**:

- **cors**: `npm install cors` - CORS handling
- **helmet**: `npm install helmet` - Security headers
- **express-rate-limit**: `npm install express-rate-limit` - Rate limiting
- **compression**: `npm install compression` - Response compression
- **morgan**: `npm install morgan` - HTTP logging

**Quick Setup**:

```typescript
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import compression from 'compression';
import morgan from 'morgan';

const app = express();

app.use(helmet());
app.use(cors());
app.use(compression());
app.use(morgan('combined'));
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));
app.use(express.json());
```

---

## Free Tier Services

### Databases

- **Supabase**: PostgreSQL, 500MB - <https://supabase.com>
- **PlanetScale**: MySQL, 5GB - <https://planetscale.com>
- **MongoDB Atlas**: 512MB - <https://www.mongodb.com/atlas>
- **Neon**: PostgreSQL, 10GB - <https://neon.tech>

### Hosting

- **Railway**: $5 credit/month - <https://railway.app>
- **Render**: Free static sites - <https://render.com>
- **Fly.io**: Free tier - <https://fly.io>
- **Vercel**: Unlimited personal projects - <https://vercel.com>

### Caching

- **Upstash Redis**: 10,000 commands/day free - <https://upstash.com>
- **Redis Labs**: 30MB free - <https://redis.com>

### Monitoring

- **Sentry**: 5,000 events/month - <https://sentry.io>
- **Better Stack**: 1GB logs/month - <https://betterstack.com>

---

## Licensing

**RECOMMENDED** for Open Source:

- **MIT**: Most permissive
- **Apache 2.0**: Patent protection
- **GPL v3**: Copyleft

**package.json**:

```json
{
  "license": "MIT"
}
```

---

## Community Resources

### Documentation

- Node.js: <https://nodejs.org/docs>
- Express: <https://expressjs.com>
- Fastify: <https://fastify.dev>
- NestJS: <https://docs.nestjs.com>
- TypeScript: <https://www.typescriptlang.org>

### Learning

- Node.js Best Practices: <https://github.com/goldbergyoni/nodebestpractices>
- TypeScript Handbook: <https://www.typescriptlang.org/docs>

### Communities

- Node.js Discord: <https://discord.gg/nodejs>
- Reddit: r/node, r/typescript

---

**Philosophy**: Personal and open-source projects prioritize developer experience, community packages, and cost-effective solutions. Start simple, scale as needed!

---

**Last Updated**: 2025-11-16
**Maintained by**: Open Source Community
**Contributing**: PRs welcome!
