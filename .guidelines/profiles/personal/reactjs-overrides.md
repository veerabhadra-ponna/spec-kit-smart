# React Personal/Public Profile Overrides

**Profile**: Personal/Public Open Source
**Stack**: React
**Version**: 3.0
**Last Updated**: 2025-11-16

> **Note**: This file contains only personal/public project-specific overrides. Base guidelines are inherited from `base/reactjs-base.md`.

---

## Scaffolding

**RECOMMENDED**:

- **Vite + React**: `npm create vite@latest my-app -- --template react-ts`
  - Ultra-fast dev server
  - Modern build tooling
  - Excellent TypeScript support
- **Next.js**: `npx create-next-app@latest`
  - Choose App Router for new projects
  - Built-in TypeScript support
  - Automatic routing and optimization
- **Remix**: `npx create-remix@latest`
  - Web fundamentals focused
  - Great for full-stack apps
  - Progressive enhancement

**Starter Templates**:

- **Vite**: <https://github.com/vitejs/vite/tree/main/packages/create-vite>
- **Next.js**: <https://github.com/vercel/next.js/tree/canary/examples>
- **shadcn/ui + Next.js**: <https://ui.shadcn.com>
- **T3 Stack**: <https://create.t3.gg> (Next.js + tRPC + Prisma + Tailwind)

**Quick Start**:

```bash
# Vite + React + TypeScript
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev

# Next.js with TypeScript and Tailwind
npx create-next-app@latest my-app --typescript --tailwind --app
cd my-app
npm run dev

# With shadcn/ui
npx create-next-app@latest my-app --typescript --tailwind --app
npx shadcn-ui@latest init
```

**NEVER**:

- Use deprecated Create React App (CRA) - unmaintained since 2022

---

## Package Registry

**RECOMMENDED**:

- Use official npm registry (<https://registry.npmjs.org>)
- Enable npm audit for security scanning: `npm audit`
- Consider using `pnpm` for faster installs and disk space savings
- Consider using `bun` for ultra-fast package management

**Configuration**:

```bash
# Standard npm (default)
npm install <package>

# pnpm (faster, more efficient)
npm install -g pnpm
pnpm install <package>

# bun (fastest)
npm install -g bun
bun install <package>
```

**Security**:

- Run `npm audit` regularly to check for vulnerabilities
- Use `npm audit fix` to automatically fix issues
- Consider Dependabot for automated dependency updates
- Review package.json for unused dependencies

---

## Recommended Libraries

### UI Components

**RECOMMENDED OPTIONS**:

1. **shadcn/ui** (Recommended for flexibility)
   - Copy-paste components built on Radix UI + Tailwind
   - Full customization control
   - No package dependency
   - Installation: <https://ui.shadcn.com>

2. **Radix UI** (Unstyled primitives)
   - Accessible, unstyled components
   - Bring your own styles
   - Perfect for design systems
   - Installation: `npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu`

3. **Headless UI** (by Tailwind Labs)
   - Unstyled, accessible components
   - Designed for Tailwind CSS
   - Installation: `npm install @headlessui/react`

4. **MUI (Material-UI v5+)**
   - Comprehensive component library
   - Material Design implementation
   - Installation: `npm install @mui/material @emotion/react @emotion/styled`

5. **Chakra UI**
   - Component library with built-in theming
   - Excellent accessibility
   - Installation: `npm install @chakra-ui/react @emotion/react @emotion/styled`

6. **Mantine**
   - 100+ customizable components
   - Built-in dark mode
   - Installation: `npm install @mantine/core @mantine/hooks`

**Quick Setup (shadcn/ui)**:

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add form
```

**Usage Example**:

```typescript
// shadcn/ui components (copied to your project)
import { Button } from '@/components/ui/button';
import { Dialog } from '@/components/ui/dialog';

function MyComponent() {
  return (
    <div>
      <Button variant="default" size="lg">
        Click Me
      </Button>
    </div>
  );
}
```

---

### Authentication

**RECOMMENDED OPTIONS**:

1. **Clerk** (Easiest, full-featured)
   - Drop-in authentication
   - Beautiful pre-built UI
   - Free tier available
   - Installation: `npm install @clerk/nextjs`
   - Website: <https://clerk.com>

2. **Supabase Auth**
   - Open-source authentication
   - Integrates with Supabase database
   - Email, OAuth, magic links
   - Installation: `npm install @supabase/supabase-js`
   - Website: <https://supabase.com>

3. **NextAuth.js** (now Auth.js)
   - Open-source, flexible
   - Supports many providers (Google, GitHub, Email)
   - Self-hosted
   - Installation: `npm install next-auth`
   - Website: <https://authjs.dev>

4. **Firebase Auth**
   - Google's authentication service
   - Free tier available
   - Installation: `npm install firebase`
   - Website: <https://firebase.google.com>

5. **Auth0**
   - Enterprise-grade authentication
   - Free tier available
   - Installation: `npm install @auth0/nextjs-auth0`
   - Website: <https://auth0.com>

**Quick Setup (Clerk + Next.js)**:

```bash
npm install @clerk/nextjs
```

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}

// middleware.ts
import { authMiddleware } from '@clerk/nextjs';

export default authMiddleware({
  publicRoutes: ['/'],
});

export const config = {
  matcher: ['/((?!.+\\.[\\w]+$|_next).*)', '/', '/(api|trpc)(.*)'],
};
```

---

### API Client & Data Fetching

**RECOMMENDED**:

**For Client Components**:

- **TanStack Query (React Query)**: Industry standard for server state
  - Installation: `npm install @tanstack/react-query`
  - Documentation: <https://tanstack.com/query>

**For Server Components (Next.js)**:

- **Built-in fetch with caching**: Use native fetch API
- **Server Actions**: Use Next.js server actions for mutations

**Quick Setup (TanStack Query)**:

```bash
npm install @tanstack/react-query
```

```typescript
// app/providers.tsx
'use client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export function Providers({ children }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

// Usage
import { useQuery } from '@tanstack/react-query';

function Users() {
  const { data, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await fetch('/api/users');
      return res.json();
    }
  });

  if (isLoading) return <div>Loading...</div>;
  return <div>{data.map(u => u.name)}</div>;
}
```

**For Simple Projects**:

```typescript
// Next.js Server Component - native fetch
async function Users() {
  const res = await fetch('https://api.example.com/users', {
    next: { revalidate: 3600 } // Cache for 1 hour
  });
  const users = await res.json();

  return <div>{users.map(u => u.name)}</div>;
}
```

---

### Database & ORM

**RECOMMENDED OPTIONS**:

1. **Prisma** (Most popular)
   - Type-safe ORM
   - Excellent TypeScript support
   - Supports PostgreSQL, MySQL, SQLite, MongoDB
   - Installation: `npm install prisma @prisma/client`
   - Website: <https://www.prisma.io>

2. **Drizzle ORM** (Newer, lightweight)
   - TypeScript-first ORM
   - SQL-like syntax
   - Lightweight and fast
   - Installation: `npm install drizzle-orm`
   - Website: <https://orm.drizzle.team>

3. **Supabase** (Backend as a Service)
   - PostgreSQL database
   - Auto-generated APIs
   - Real-time subscriptions
   - Installation: `npm install @supabase/supabase-js`
   - Website: <https://supabase.com>

**Quick Setup (Prisma)**:

```bash
npm install prisma @prisma/client
npx prisma init
```

```prisma
// prisma/schema.prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  posts Post[]
}

model Post {
  id        Int     @id @default(autoincrement())
  title     String
  content   String?
  published Boolean @default(false)
  author    User    @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

```bash
npx prisma generate
npx prisma db push
```

---

### Logging & Error Tracking

**RECOMMENDED OPTIONS**:

1. **Sentry** (Industry standard)
   - Error tracking and performance monitoring
   - Free tier available
   - Installation: `npm install @sentry/nextjs`
   - Website: <https://sentry.io>

2. **LogRocket** (Session replay + logging)
   - Session replay
   - Error tracking
   - Performance monitoring
   - Installation: `npm install logrocket`
   - Website: <https://logrocket.com>

3. **BetterStack (formerly Logtail)** (Logging)
   - Modern logging platform
   - Excellent search and filtering
   - Installation: `npm install @logtail/browser`
   - Website: <https://betterstack.com>

**Quick Setup (Sentry)**:

```bash
npx @sentry/wizard@latest -i nextjs
```

```typescript
// Automatic instrumentation already configured by wizard

// Manual error logging
import * as Sentry from '@sentry/nextjs';

try {
  // Your code
} catch (error) {
  Sentry.captureException(error);
}

// Add context
Sentry.setUser({ id: user.id, email: user.email });
Sentry.setTag('feature', 'checkout');
```

**For Simple Projects (console)**:

```typescript
// Simple console logging for development
const logger = {
  info: (message: string, meta?: any) => console.log('[INFO]', message, meta),
  warn: (message: string, meta?: any) => console.warn('[WARN]', message, meta),
  error: (message: string, meta?: any) => console.error('[ERROR]', message, meta),
};

logger.info('User logged in', { userId: 123 });
```

---

### Analytics

**RECOMMENDED OPTIONS**:

1. **Vercel Analytics** (For Next.js on Vercel)
   - Zero-config
   - Privacy-friendly
   - Installation: `npm install @vercel/analytics`
   - Website: <https://vercel.com/analytics>

2. **Plausible** (Privacy-friendly)
   - GDPR compliant
   - No cookies
   - Self-hosted or cloud
   - Website: <https://plausible.io>

3. **Posthog** (Open-source, feature-rich)
   - Product analytics
   - Session replay
   - Feature flags
   - Installation: `npm install posthog-js`
   - Website: <https://posthog.com>

4. **Google Analytics 4**
   - Free, comprehensive
   - Requires cookie consent
   - Installation: `npm install react-ga4`

**Quick Setup (Vercel Analytics)**:

```bash
npm install @vercel/analytics
```

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

**Quick Setup (Plausible)**:

```typescript
// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Script
          defer
          data-domain="yourdomain.com"
          src="https://plausible.io/js/script.js"
        />
      </body>
    </html>
  );
}
```

---

## Deployment Platforms

**RECOMMENDED**:

1. **Vercel** (Best for Next.js)
   - Zero-config deployment
   - Automatic HTTPS
   - Edge functions
   - Free tier: Unlimited personal projects
   - Website: <https://vercel.com>

2. **Netlify** (Great for static sites)
   - Drag-and-drop deployment
   - Serverless functions
   - Form handling
   - Free tier: 100GB bandwidth/month
   - Website: <https://netlify.com>

3. **Cloudflare Pages** (Fast, global)
   - Edge deployment
   - Unlimited bandwidth (free tier)
   - Great performance
   - Website: <https://pages.cloudflare.com>

4. **Railway** (Full-stack)
   - Deploy databases and apps
   - Simple pricing
   - Free tier: $5 credit/month
   - Website: <https://railway.app>

5. **Render** (Full-stack)
   - Free static sites
   - PostgreSQL databases
   - Background workers
   - Website: <https://render.com>

**Quick Setup (Vercel)**:

```bash
npm install -g vercel
vercel

# Or use GitHub integration (recommended)
# 1. Push code to GitHub
# 2. Import project on vercel.com
# 3. Automatic deployments on push
```

---

## Development Tools

### Code Quality

**RECOMMENDED**:

- **ESLint**: `npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin`
- **Prettier**: `npm install -D prettier eslint-config-prettier`
- **Husky**: `npm install -D husky lint-staged` (Git hooks)

**Quick Setup**:

```bash
# ESLint + Prettier
npm install -D eslint prettier eslint-config-prettier
npx eslint --init

# .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}

# Husky + lint-staged
npx husky-init && npm install
npx husky add .husky/pre-commit "npx lint-staged"
```

### Testing

**RECOMMENDED**:

- **Vitest**: `npm install -D vitest @testing-library/react @testing-library/jest-dom`
- **Playwright**: `npm install -D @playwright/test`

**Quick Setup (Vitest)**:

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
  },
});
```

---

## Environment Management

**RECOMMENDED**:

```bash
# .env.local (gitignored - local development)
NEXT_PUBLIC_API_URL=http://localhost:3000/api
DATABASE_URL=postgresql://localhost:5432/mydb
SECRET_KEY=your-secret-key

# .env.example (committed - template)
NEXT_PUBLIC_API_URL=
DATABASE_URL=
SECRET_KEY=
```

**Environment Variable Validation**:

```typescript
import { z } from 'zod';

const envSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
  DATABASE_URL: z.string(),
  SECRET_KEY: z.string().min(32),
});

export const env = envSchema.parse(process.env);
```

---

## Free Tier Resources

### Hosting

- **Vercel**: Unlimited personal projects, 100GB bandwidth
- **Netlify**: 100GB bandwidth, 300 build minutes
- **Cloudflare Pages**: Unlimited bandwidth, 500 builds/month
- **Railway**: $5 credit/month
- **Render**: Free static sites, limited databases

### Databases

- **Supabase**: 500MB database, 1GB file storage
- **PlanetScale**: 5GB storage, 1 billion row reads/month
- **Neon**: 10GB storage, unlimited projects
- **MongoDB Atlas**: 512MB storage

### Authentication

- **Clerk**: 10,000 monthly active users
- **Supabase Auth**: 50,000 monthly active users
- **Auth0**: 7,000 monthly active users
- **Firebase Auth**: Unlimited

### Error Tracking

- **Sentry**: 5,000 events/month
- **BugSnag**: 7,500 events/month

### Analytics

- **Vercel Analytics**: 2,500 events/month
- **Plausible**: Self-hosted (free)
- **PostHog**: 1 million events/month

---

## Licensing

**RECOMMENDED** for Open Source:

- **MIT**: Most permissive, allows commercial use
- **Apache 2.0**: Patent protection, requires attribution
- **GPL v3**: Copyleft, derivatives must be open source
- **ISC**: Similar to MIT, simpler wording

**Quick Setup**:

```bash
# Add LICENSE file to project root
# Update package.json
{
  "license": "MIT"
}
```

**README Requirements**:

```markdown
# Project Name

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
```

---

## Community Resources

### Documentation

- React: <https://react.dev>
- Next.js: <https://nextjs.org/docs>
- Vite: <https://vitejs.dev>
- TypeScript: <https://www.typescriptlang.org>

### Component Libraries

- shadcn/ui: <https://ui.shadcn.com>
- Radix UI: <https://www.radix-ui.com>
- Headless UI: <https://headlessui.com>
- MUI: <https://mui.com>

### Learning Resources

- React Tutorial: <https://react.dev/learn>
- TypeScript Handbook: <https://www.typescriptlang.org/docs/handbook/intro.html>
- Next.js Learn: <https://nextjs.org/learn>
- Web.dev: <https://web.dev>

### Communities

- React Discord: <https://discord.gg/react>
- Reactiflux: <https://www.reactiflux.com>
- Next.js Discord: <https://nextjs.org/discord>
- Reddit: r/reactjs, r/nextjs

---

**Philosophy**: Personal and open-source projects prioritize developer experience, community packages, and cost-effective solutions. Choose tools based on project needs, not corporate mandates.

**Remember**: Start simple, add complexity as needed. Don't over-engineer early projects. Learn by building!

---

**Last Updated**: 2025-11-16
**Maintained by**: Open Source Community
**Contributing**: PRs welcome! See CONTRIBUTING.md
