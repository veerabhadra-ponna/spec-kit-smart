# React Base Guidelines

**Tech Stack**: React 18+, TypeScript 5+, Next.js 14+ / Vite 5+, Frontend Web Applications, SPAs, SSR
**Auto-detected from**: `package.json` with `"react"` dependency
**Version**: 3.0 (Profile-Based Architecture)
**Last Updated**: 2025-11-16

---

## Target Platform

**MUST**:

- Use React 18.2+ (stable, concurrent features, automatic batching)
- Use TypeScript 5.3+ for all new projects
- Use modern build tools: Next.js 14+ (full-stack) or Vite 5+ (SPA)
- Target modern browsers (ES2020+, no IE11 support)

**SHOULD**:

- Migrate to React 19 when stable and dependencies support it
- Use React Server Components (Next.js App Router)
- Adopt new React features (use hook, useFormStatus, useOptimistic)

**Rationale**: React 18 provides concurrent rendering, automatic batching, transitions, Suspense improvements; TypeScript provides type safety and better DX

---

## Framework Selection

**Framework Options**:

- **Next.js 14+**: Full-stack React framework, SSR/SSG, API routes, file-based routing (recommended for most projects)
- **Vite 5+**: Ultra-fast dev server, SPA, client-side routing with React Router (for pure frontend apps)
- **Remix**: Web fundamentals focused, progressive enhancement, nested routing
- **Astro**: Content-focused sites, partial hydration, bring-your-own-framework

**NEVER**:

- Use deprecated Create React App (CRA) - unmaintained since 2022

---

## State Management

**MUST** choose based on complexity:

- **Simple state**: React Context + useReducer (built-in)
- **Medium complexity**: Zustand 4.x (recommended, lightweight, minimal boilerplate)
- **Complex state**: Redux Toolkit 2.x (predictable, time-travel debugging, DevTools)
- **Server state**: TanStack Query (React Query) - handles server state, caching, sync

**NEVER**:

- Use legacy Redux (without Redux Toolkit)
- Use MobX (less popular, harder to debug)

**Zustand Example** (recommended for client state):

```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  total: number;
}

const useCartStore = create<CartState>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],
        addItem: (item) => set((state) => ({
          items: [...state.items, item]
        })),
        removeItem: (id) => set((state) => ({
          items: state.items.filter(i => i.id !== id)
        })),
        get total() {
          return get().items.reduce((sum, item) => sum + item.price, 0);
        }
      }),
      { name: 'cart-storage' }
    )
  )
);

// Usage
function Cart() {
  const { items, addItem, total } = useCartStore();
  return <div>Total: ${total}</div>;
}
```

**State Management Principles**:

- Server state (API data) → TanStack Query
- Client state (UI state, forms) → Zustand or Context
- URL state (filters, pagination) → URL search params
- Form state → React Hook Form or Formik

---

## Routing

**Next.js** (built-in file-based routing):

- Use App Router (app/ directory) for new projects
- Use Server Components by default, 'use client' when needed
- Use parallel routes, intercepting routes for advanced patterns

**Vite/SPA** (React Router 6.x):

```typescript
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <ErrorBoundary />,
    children: [
      { index: true, element: <Home /> },
      { path: 'users', element: <Users /> },
      { path: 'users/:id', element: <UserDetail /> }
    ]
  }
]);

function App() {
  return <RouterProvider router={router} />;
}
```

**TanStack Router**: Type-safe routing alternative (newer, growing adoption)

---

## Styling

**MUST** choose one approach (be consistent):

- **Tailwind CSS 3.x**: Utility-first CSS (recommended for most projects)
- **CSS Modules**: Scoped CSS, zero runtime (good for component libraries)
- **CSS-in-JS**: styled-components, Emotion (runtime cost, use cautiously)
- **Vanilla Extract**: Zero-runtime CSS-in-TS (best of both worlds)
- **Sass/SCSS**: Traditional preprocessor (legacy projects)

**Tailwind Best Practices**:

```typescript
// Use cn() helper for conditional classes
import { cn } from '@/lib/utils';

function Button({ variant, className, ...props }) {
  return (
    <button
      className={cn(
        'px-4 py-2 rounded-md font-medium transition-colors',
        variant === 'primary' && 'bg-blue-500 text-white hover:bg-blue-600',
        variant === 'secondary' && 'bg-gray-200 text-gray-900 hover:bg-gray-300',
        className
      )}
      {...props}
    />
  );
}
```

**NEVER**:

- Mix multiple styling approaches in same component
- Use inline styles for complex styling
- Use !important (refactor specificity instead)

---

## Form Handling

**MUST** use one of:

- **React Hook Form 7.x**: Performance, minimal re-renders (recommended)
- **Formik 2.x**: Popular, full-featured (more re-renders)
- **Native HTML forms**: Next.js Server Actions (progressive enhancement)

**React Hook Form Example**:

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema)
  });

  const onSubmit = async (data: FormData) => {
    await apiClient.post('/login', data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```

---

## Architecture

### Project Structure - Feature-Based (Recommended)

**SHOULD** use: Feature/domain-based organization

```text
src/
├── app/                     # Next.js App Router
│   ├── (auth)/              # Route groups
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/
│   │   ├── page.tsx
│   │   └── layout.tsx
│   └── layout.tsx
├── features/                # Feature modules
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── types.ts
│   ├── users/
│   └── orders/
├── shared/                  # Shared code
│   ├── components/
│   │   ├── ui/              # Base UI components
│   │   └── layout/
│   ├── hooks/
│   ├── utils/
│   └── types/
├── lib/                     # Third-party integrations
│   ├── api-client.ts
│   └── auth.ts
└── styles/
    └── globals.css
```

### Project Structure - Vite/SPA

```text
src/
├── features/
│   ├── auth/
│   └── dashboard/
├── shared/
│   ├── components/
│   ├── hooks/
│   └── utils/
├── routes/                  # React Router routes
├── App.tsx
├── main.tsx
└── index.css
```

### Separation of Concerns

**MUST**:

- Keep components focused on presentation
- Extract business logic to custom hooks
- Extract API calls to service files
- Use custom hooks for complex state logic
- Separate server and client code (Next.js App Router)

**Component Patterns**:

```typescript
// ❌ Bad - everything in component
function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/user')
      .then(res => res.json())
      .then(setUser)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}

// ✅ Good - separated concerns
function UserProfile() {
  const { user, isLoading } = useUser();

  if (isLoading) return <Spinner />;
  return <UserCard user={user} />;
}

// Custom hook handles data fetching
function useUser() {
  return useQuery({
    queryKey: ['user'],
    queryFn: () => apiClient.get('/user')
  });
}
```

### Component Organization

**MUST**:

- One component per file (except small, tightly coupled components)
- Co-locate tests, styles, types with components
- Use named exports (avoid default exports for better refactoring)

```text
components/
├── UserCard/
│   ├── UserCard.tsx
│   ├── UserCard.test.tsx
│   ├── UserCard.module.css
│   ├── types.ts
│   └── index.ts            # Re-export
```

### Server vs Client Components (Next.js App Router)

**MUST**:

- Use Server Components by default (no 'use client' directive)
- Use 'use client' only when needed:
  - useState, useEffect, event handlers
  - Browser APIs (localStorage, window)
  - Context providers
  - Third-party libraries that use client-only features

```typescript
// ✅ Server Component (default)
async function UserList() {
  const users = await db.user.findMany();
  return <List items={users} />;
}

// ✅ Client Component (when needed)
'use client';
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

---

## Security

### XSS Prevention

**MUST**:

- Never use `dangerouslySetInnerHTML` unless absolutely necessary
- Sanitize HTML with DOMPurify if you must render user HTML
- Validate and escape user inputs
- Use Content Security Policy (CSP) headers

**Safe HTML Rendering**:

```typescript
import DOMPurify from 'isomorphic-dompurify';

function SafeHTML({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

### Environment Variables

**MUST**:

- Prefix public env vars with `NEXT_PUBLIC_` (Next.js) or `VITE_` (Vite)
- Never expose secrets to client-side code
- Use `.env.local` for local development (gitignored)
- Validate environment variables at build time

**Environment Variable Validation**:

```typescript
import { z } from 'zod';

const envSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
  DATABASE_URL: z.string(), // Server-only
  SECRET_KEY: z.string().min(32) // Server-only
});

const env = envSchema.parse(process.env);

export { env };
```

**NEVER**:

- Hardcode API keys or secrets in code
- Commit `.env` files to version control
- Expose server-side secrets to client code

### Authentication & Authorization

**MUST**:

- Validate user session on every protected page
- Use middleware for route protection (Next.js)
- Store tokens securely (httpOnly cookies, not localStorage)
- Implement CSRF protection for state-changing operations
- Use secure, sameSite cookies

### Content Security Policy (CSP)

**MUST** configure in Next.js:

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-eval' 'unsafe-inline'", // Adjust based on needs
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self' data:",
      "connect-src 'self' https://api.example.com"
    ].join('; ')
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY'
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin'
  }
];

module.exports = {
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  }
};
```

### Input Validation

**MUST**:

- Validate all user inputs with Zod or Yup
- Validate on both client and server (Next.js Server Actions)
- Sanitize inputs before rendering
- Use TypeScript for compile-time type safety

---

## Coding Standards

### TypeScript

**MUST**:

- Use TypeScript for all new code
- Enable strict mode in `tsconfig.json`
- Define types/interfaces for all props, state, API responses
- Use type inference where possible (don't over-annotate)

**TypeScript Configuration**:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**NEVER**:

- Use `any` type (use `unknown` if type is truly unknown)
- Disable TypeScript checks with `@ts-ignore` (use `@ts-expect-error` with explanation)
- Use type assertions (`as`) unless necessary

### Component Patterns

**MUST**:

- Use functional components (no class components)
- Use hooks for state and side effects
- Define prop types with TypeScript interfaces

**Component Example**:

```typescript
interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  className?: string;
}

export function UserCard({ user, onEdit, className }: UserCardProps) {
  return (
    <div className={cn('rounded-lg border p-4', className)}>
      <h3>{user.name}</h3>
      {onEdit && (
        <button onClick={() => onEdit(user)}>Edit</button>
      )}
    </div>
  );
}
```

### Naming Conventions

**MUST** follow:

- Components: `PascalCase` (UserProfile.tsx)
- Hooks: `camelCase` with `use` prefix (useAuth.ts, useUsers.ts)
- Utilities: `camelCase` (formatDate.ts)
- Constants: `UPPER_SNAKE_CASE`
- Types/Interfaces: `PascalCase` (User, UserProfile)
- Files: Match export name (UserProfile.tsx exports UserProfile)

### Hooks Best Practices

**MUST**:

- Follow Rules of Hooks (only at top level, only in function components/hooks)
- Use dependency arrays correctly in useEffect, useMemo, useCallback
- Extract complex logic to custom hooks
- Use useCallback for functions passed to children (prevent re-renders)
- Use useMemo for expensive computations

**Common Mistakes to Avoid**:

```typescript
// ❌ Bad - missing dependencies
useEffect(() => {
  fetchUser(userId);
}, []); // userId should be in deps

// ✅ Good
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// ❌ Bad - unnecessary useEffect
const [count, setCount] = useState(0);
const [doubled, setDoubled] = useState(0);

useEffect(() => {
  setDoubled(count * 2);
}, [count]);

// ✅ Good - derived state
const doubled = count * 2;
```

### Performance Optimization

**SHOULD**:

- Use React.memo for expensive components
- Use useCallback for functions passed to memoized children
- Use useMemo for expensive computations
- Use React.lazy for code splitting
- Use dynamic imports for large components/libraries
- Avoid premature optimization (profile first)

**Code Splitting**:

```typescript
// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <Suspense fallback={<ChartSkeleton />}>
      <HeavyChart data={data} />
    </Suspense>
  );
}

// Dynamic import for conditional features
async function loadEditor() {
  const { Editor } = await import('heavy-editor-library');
  return Editor;
}
```

### Accessibility (a11y)

**MUST**:

- Meet WCAG 2.1 Level AA compliance
- Use semantic HTML elements (button, nav, main, article)
- Provide alt text for images
- Support keyboard navigation (tab, enter, escape)
- Use ARIA attributes when semantic HTML insufficient
- Test with screen readers (NVDA, JAWS, VoiceOver)

**Accessibility Checklist**:

```typescript
// ✅ Good accessibility
<button onClick={handleClick} aria-label="Close dialog">
  <XIcon />
</button>

<img src={avatar} alt={`Profile picture of ${user.name}`} />

<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

// Form labels
<label htmlFor="email">Email</label>
<input id="email" type="email" required aria-invalid={!!errors.email} />
```

**Testing Tools**:

- axe DevTools browser extension
- Lighthouse accessibility audit
- eslint-plugin-jsx-a11y

---

## Testing

### Unit Testing

**MUST**:

- Write unit tests for components and hooks
- Use Vitest (recommended, faster) or Jest
- Use React Testing Library (not Enzyme - deprecated)
- Aim for 80%+ coverage on critical paths

**React Testing Library Example**:

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('displays user name', () => {
    const user = { id: 1, name: 'John Doe', email: 'john@example.com' };
    render(<UserProfile user={user} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('calls onEdit when edit button clicked', async () => {
    const handleEdit = vi.fn();
    const user = { id: 1, name: 'John Doe', email: 'john@example.com' };

    render(<UserProfile user={user} onEdit={handleEdit} />);

    fireEvent.click(screen.getByRole('button', { name: /edit/i }));

    await waitFor(() => {
      expect(handleEdit).toHaveBeenCalledWith(user);
    });
  });
});
```

**Testing Best Practices**:

- Test behavior, not implementation
- Use semantic queries (getByRole, getByLabelText) over test IDs
- Mock external dependencies (API calls, browser APIs)
- Use user-centric queries (what users see/interact with)

### Integration Testing

**SHOULD**:

- Test complete user flows
- Use Playwright or Cypress for E2E testing
- Test critical paths (authentication, checkout, data entry)

**Playwright Example**:

```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('http://localhost:3000/login');

  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('http://localhost:3000/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

### Visual Regression Testing

**SHOULD**:

- Use Chromatic, Percy, or Playwright screenshots
- Catch unintended UI changes
- Integrate with Storybook for component testing

---

## Build & Deployment

### Build Optimization (Next.js)

**MUST**:

- Enable SWC compiler (default in Next.js 12+)
- Use Image Optimization (next/image)
- Use Font Optimization (next/font)
- Enable bundle analysis to identify large dependencies

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['cdn.example.com'],
    formats: ['image/avif', 'image/webp']
  },
  experimental: {
    optimizePackageImports: ['lodash-es']
  }
});
```

### Build Optimization (Vite)

**MUST**:

- Enable tree shaking and minification
- Use code splitting
- Configure chunk size warnings

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        }
      }
    },
    chunkSizeWarningLimit: 500
  }
});
```

### Docker - Cloud Deployments

**MUST**:

- Use multi-stage builds
- Use official Node.js Alpine images
- Run as non-root user
- Copy only build artifacts to production image

**Next.js Dockerfile**:

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

**Vite/SPA Dockerfile** (nginx):

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Cloud Deployment Platforms

**Recommended**:

- **Vercel**: Zero-config Next.js deployment, edge functions (best for Next.js)
- **Netlify**: Static sites, serverless functions
- **AWS Amplify**: AWS-native hosting, CI/CD
- **Azure Static Web Apps**: Azure-native hosting, serverless APIs
- **Cloudflare Pages**: Edge deployment, ultra-fast
- **Self-hosted**: Docker + Kubernetes, AWS ECS, Azure Container Apps

### Static Site Generation (SSG)

**SHOULD** use for:

- Marketing pages
- Blog posts
- Documentation
- Content that changes infrequently

```typescript
// Next.js App Router - Static generation
export const dynamic = 'force-static';

export default async function BlogPost({ params }) {
  const post = await getPost(params.slug);
  return <Article post={post} />;
}
```

### Server-Side Rendering (SSR)

**SHOULD** use for:

- Personalized content
- Real-time data
- SEO-critical pages with dynamic content

```typescript
// Next.js App Router - Dynamic rendering
export const dynamic = 'force-dynamic';

export default async function Dashboard() {
  const user = await getCurrentUser();
  return <UserDashboard user={user} />;
}
```

---

## Performance

### Core Web Vitals

**MUST** meet Google's Core Web Vitals:

- **LCP (Largest Contentful Paint)**: < 2.5s (good)
- **FID (First Input Delay)**: < 100ms (good) - replaced by INP in 2024
- **INP (Interaction to Next Paint)**: < 200ms (good)
- **CLS (Cumulative Layout Shift)**: < 0.1 (good)

**Monitoring Tools**:

- Lighthouse CI
- Web Vitals library
- Chrome User Experience Report (CrUX)
- Vercel Analytics, Cloudflare Web Analytics

### Performance Budget

**SHOULD** set limits:

- Initial bundle size: < 500KB gzipped (entire app)
- Total page weight: < 2MB
- Time to Interactive: < 5 seconds (3G network)

### Image Optimization

**MUST**:

- Use next/image (Next.js) or optimized image components
- Use modern formats (WebP, AVIF) with fallbacks
- Lazy load images below the fold
- Provide width/height to prevent layout shift
- Use responsive images (srcset)

```typescript
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // Above the fold
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

### Code Splitting & Lazy Loading

**SHOULD**:

- Lazy load routes (automatic with Next.js, manual with React Router)
- Lazy load heavy components (charts, editors, modals)
- Lazy load third-party scripts
- Use Suspense boundaries effectively

### Bundle Size Analysis

**MUST** regularly:

- Run bundle analyzer (`npm run analyze`)
- Identify and remove unused dependencies
- Replace large libraries with smaller alternatives
- Use tree-shaking friendly imports

```typescript
// ❌ Bad - imports entire library
import _ from 'lodash';

// ✅ Good - tree-shakeable import
import { debounce } from 'lodash-es';

// ✅ Better - native alternative
const debounce = (fn, delay) => { /* implementation */ };
```

---

## Observability

### Error Monitoring

**SHOULD**:

- Integrate error tracking (Sentry, Bugsnag, Azure Application Insights)
- Track error boundaries
- Log client-side errors
- Include user context (non-PII)

**Error Boundary**:

```typescript
import { ErrorBoundary as ReactErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  console.error('Component error', { error, stack: error.stack });

  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ReactErrorBoundary FallbackComponent={ErrorFallback}>
      <YourApp />
    </ReactErrorBoundary>
  );
}
```

**Client-Side Error Tracking**:

- **Sentry**: Error tracking, performance monitoring (most popular)
- **Bugsnag**: Error monitoring
- **Azure Application Insights**: Microsoft ecosystem
- **AWS CloudWatch RUM**: AWS ecosystem

### Performance Monitoring

**SHOULD**:

- Track Core Web Vitals
- Monitor bundle size changes
- Track API response times
- Use Real User Monitoring (RUM)

### Analytics

**SHOULD**:

- Track page views, user interactions, conversions
- Implement funnel analysis
- Track feature usage
- Respect user privacy (GDPR, CCPA)

**Analytics Providers**:

- Google Analytics 4 (GA4)
- Mixpanel
- Amplitude
- Plausible (privacy-friendly)
- PostHog (open-source, self-hosted)

---

## Internationalization (i18n)

**SHOULD** use for multi-language support:

- **next-intl**: Next.js i18n (App Router compatible)
- **react-i18next**: React i18n library
- **Format.js**: ICU message format

```typescript
// next-intl example
import { useTranslations } from 'next-intl';

export function Welcome() {
  const t = useTranslations('Home');

  return <h1>{t('title')}</h1>;
}
```

---

## Compliance & Governance

### Data Protection

**MUST**:

- Implement cookie consent (GDPR, CCPA)
- Provide privacy policy and terms of service
- Support Do Not Track (DNT) signals
- Implement data deletion requests

### Accessibility Compliance

**MUST**:

- Meet WCAG 2.1 Level AA
- Provide skip links
- Support keyboard navigation
- Test with screen readers
- Provide alternative text for images

### Security Audits

**SHOULD**:

- Run npm audit regularly
- Use Snyk or Dependabot for dependency scanning
- Perform penetration testing
- Conduct code reviews with security focus

---

## Recommended Libraries

### Date/Time Handling

**RECOMMENDED**:

- **date-fns**: Functional, tree-shakeable (recommended)
- **dayjs**: Lightweight, similar API to moment.js
- **Luxon**: DateTime handling by Moment.js team

**NEVER**:

- moment.js (deprecated, large bundle size)

### Utility Libraries

**RECOMMENDED**:

- **lodash-es**: Tree-shakeable version of lodash
- **ramda**: Functional programming utilities
- Native JavaScript methods (preferred when possible)

**NEVER**:

- Full lodash library (not tree-shakeable)
- jQuery (use native DOM APIs or React patterns)

### Icons

**RECOMMENDED**:

- **lucide-react**: Modern, customizable icons
- **react-icons**: Large icon library collection
- **heroicons**: Beautiful hand-crafted SVG icons
- **tabler-icons**: Free and open-source icons

### Validation

**RECOMMENDED**:

- **Zod**: TypeScript-first schema validation (recommended)
- **Yup**: Object schema validation
- **joi**: Powerful validation library

---

## Additional Resources

### Documentation

- React Documentation: <https://react.dev>
- Next.js Documentation: <https://nextjs.org/docs>
- TypeScript Documentation: <https://www.typescriptlang.org/docs>
- TanStack Query: <https://tanstack.com/query>
- Tailwind CSS: <https://tailwindcss.com>

### Learning Resources

- React Patterns: <https://reactpatterns.com>
- JavaScript.info: <https://javascript.info>
- Web.dev (Performance): <https://web.dev/learn>

---

**Note**: These are base guidelines applicable to all React projects. Project-specific requirements (corporate libraries, authentication providers, deployment targets) are defined in profile overrides.
