# React Corporate Profile Overrides

**Profile**: Corporate
**Stack**: React
**Version**: 3.0
**Last Updated**: 2025-11-16

> **Note**: This file contains only corporate-specific overrides. Base guidelines are inherited from `base/reactjs-base.md`.

---

## Scaffolding

**MUST**:

- Use corporate scaffolding command (`@YOUR_ORG/create-react-app`)
- Choose appropriate template:
  - **nextjs-app**: Next.js 14+ with App Router, Server Components (recommended for new projects)
  - **nextjs-pages**: Next.js with Pages Router (legacy, existing projects)
  - **vite-spa**: Vite + React SPA with client-side routing
  - **remix**: Remix framework for progressive enhancement
  - **microfrontend**: Module Federation setup for microfrontends

**NEVER**:

- Use public scaffolding tools without corporate security review

**Rationale**: Corporate scaffolding includes security, authentication, logging, monitoring, accessibility, observability from day one

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
- Use `NPM_TOKEN` or `NODE_AUTH_TOKEN` environment variable for CI/CD
- Configure scoped packages (`@yourorg:registry=https://registry.yourorg.com`)

**Example .npmrc**:

```text
registry=https://npm.yourorg.com
@yourorg:registry=https://npm.yourorg.com
//npm.yourorg.com/:_authToken=${NPM_TOKEN}
always-auth=true
```

---

## Mandatory Libraries

### UI Components

**MUST** use: `@YOUR_ORG/ui-components` package

**Includes**: Buttons, Modals, DataTables, Forms, Navigation, Dialogs with built-in accessibility (WCAG 2.1 AA)

**Benefits**: Consistent design system, built-in security, accessibility compliance, internationalization support

**Component Library Architecture**:

- Built on Radix UI primitives or Headless UI for accessibility
- Styled with Tailwind CSS or CSS Modules
- TypeScript definitions for all components
- Storybook documentation

**Usage Example**:

```typescript
import { Button, Modal, DataTable } from '@YOUR_ORG/ui-components';

function MyComponent() {
  return (
    <div>
      <Button variant="primary" size="lg">
        Click Me
      </Button>
      <Modal title="Confirm Action">
        Are you sure?
      </Modal>
    </div>
  );
}
```

**NEVER**:

- Use public UI libraries without approval (Material-UI, Ant Design, Chakra UI)
- Build custom UI components that duplicate corporate library functionality

---

### Authentication

**MUST** use: `@YOUR_ORG/auth-client` package

**Requirements**:

- Wrap app with `<AuthProvider>` at root level
- Use `<ProtectedRoute>` or middleware for authenticated pages
- Access user context via `useAuth()` hook
- Pass authentication token to all API calls automatically
- Support OAuth 2.0, OpenID Connect, SAML SSO

**Next.js Authentication**:

```typescript
// app/layout.tsx (App Router)
import { AuthProvider } from '@YOUR_ORG/auth-client';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}

// Using auth in components
'use client';
import { useAuth } from '@YOUR_ORG/auth-client';

export function UserProfile() {
  const { user, isAuthenticated, signOut } = useAuth();

  if (!isAuthenticated) return <LoginButton />;

  return <div>Welcome, {user.name}</div>;
}
```

**Route Protection** (Next.js App Router):

```typescript
// middleware.ts
import { authMiddleware } from '@YOUR_ORG/auth-client/next';

export default authMiddleware({
  publicRoutes: ['/login', '/signup'],
  afterAuth: (auth, req) => {
    // Custom logic after auth check
  }
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
};
```

**Cloud-Specific Integrations**:

- Azure AD / Entra ID integration
- AWS Cognito integration
- Auth0, Clerk, Supabase Auth (if approved)

---

### API Client & Data Fetching

**MUST** use: `@YOUR_ORG/api-client` package

**Requirements**:

- Use `useQuery()` hook for GET requests (data fetching)
- Use `useMutation()` hook for POST/PUT/DELETE (data mutations)
- Never use raw `fetch()` or `axios` directly
- Automatic token injection from auth context
- Built-in retry logic, error handling, caching

**Features**:

- Request/response interceptors
- Automatic token refresh
- Request deduplication
- Optimistic updates
- Infinite queries for pagination
- WebSocket support

**Based on**: TanStack Query (React Query) v5+

**Example Usage**:

```typescript
import { useQuery, useMutation, useQueryClient } from '@YOUR_ORG/api-client';

// Fetch data
function UserList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    endpoint: '/users'
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error error={error} />;

  return <List items={data} />;
}

// Mutate data
function CreateUser() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    endpoint: '/users',
    method: 'POST',
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });

  return (
    <button onClick={() => mutation.mutate({ name: 'John' })}>
      Create User
    </button>
  );
}
```

**Next.js Server Components** (App Router):

```typescript
// Server Component - use corporate API client
import { apiClient } from '@YOUR_ORG/api-client/server';

async function UserList() {
  const users = await apiClient.get('/users', {
    revalidate: 3600 // Cache for 1 hour
  });

  return <List items={users} />;
}
```

---

### Logging & Error Tracking

**MUST** use: `@YOUR_ORG/logger` package

**Requirements**:

- Log user actions for audit trail (button clicks, navigation, errors)
- Include correlation ID in all logs
- Never log sensitive data (passwords, tokens, PII, credit cards)
- Send errors to corporate monitoring service (Sentry, Azure Monitor, AWS CloudWatch)

**Usage Example**:

```typescript
import { logger } from '@YOUR_ORG/logger';

function UserActions() {
  const handleDelete = (userId: string) => {
    logger.info('User initiated delete', {
      action: 'user.delete',
      userId,
      timestamp: new Date().toISOString()
    });

    // Perform delete
  };

  return <button onClick={() => handleDelete('123')}>Delete</button>;
}
```

**Error Boundary**:

```typescript
import { ErrorBoundary as ReactErrorBoundary } from 'react-error-boundary';
import { logger } from '@YOUR_ORG/logger';

function ErrorFallback({ error, resetErrorBoundary }) {
  logger.error('Component error', {
    error: error.message,
    stack: error.stack,
    component: 'ErrorBoundary'
  });

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

**Log Levels**:

- `logger.debug()` - Development debugging
- `logger.info()` - Informational messages
- `logger.warn()` - Warning messages
- `logger.error()` - Error messages
- `logger.fatal()` - Critical errors

---

### Analytics

**MUST** use: `@YOUR_ORG/analytics` package

**Requirements**:

- Track page views, user interactions, conversions
- Comply with GDPR, CCPA (cookie consent)
- Use privacy-friendly analytics when possible
- Never track PII without consent

**Usage Example**:

```typescript
import { analytics } from '@YOUR_ORG/analytics';

function ProductPage({ product }) {
  useEffect(() => {
    analytics.track('Page Viewed', {
      page: 'product',
      productId: product.id,
      category: product.category
    });
  }, [product]);

  const handlePurchase = () => {
    analytics.track('Product Purchased', {
      productId: product.id,
      price: product.price,
      currency: 'USD'
    });
  };

  return <button onClick={handlePurchase}>Buy Now</button>;
}
```

**Cookie Consent**:

```typescript
import { CookieConsent } from '@YOUR_ORG/analytics';

function App() {
  return (
    <>
      <CookieConsent
        onAccept={() => analytics.enable()}
        onDecline={() => analytics.disable()}
      />
      <YourApp />
    </>
  );
}
```

---

## Banned Libraries

**NEVER** use without explicit approval:

- **UI Libraries**: Material-UI, Ant Design, Chakra UI → Use `@YOUR_ORG/ui-components`
- **Authentication**: Public auth libraries → Use `@YOUR_ORG/auth-client`
- **API Clients**: axios, fetch wrappers → Use `@YOUR_ORG/api-client`
- **Logging**: console.log, custom loggers → Use `@YOUR_ORG/logger`
- **Analytics**: Google Analytics without wrapper → Use `@YOUR_ORG/analytics`

**Security Concerns**:

- Avoid packages with known vulnerabilities (`npm audit`, Snyk)
- Avoid unmaintained packages (check last publish date)
- All packages must be approved through corporate security review
- All packages must be available in corporate registry

**Rationale**: Corporate libraries enforce security, accessibility, compliance, brand consistency, audit trail

---

## Deployment

### Corporate CI/CD

**MUST** use:

- Corporate CI/CD pipeline (Jenkins, Azure DevOps, GitLab CI, GitHub Actions)
- Automated security scanning (Snyk, SonarQube)
- Automated testing (unit, integration, E2E)
- Code review requirements (minimum 2 approvers)

**Pipeline Stages**:

1. Lint & Type Check
2. Unit Tests (80%+ coverage required)
3. Integration Tests
4. Security Scan
5. Build
6. Deploy to Dev/Staging
7. E2E Tests
8. Deploy to Production (approval required)

### Environment Management

**MUST**:

- Use corporate environment management (AWS, Azure, GCP accounts)
- Follow corporate naming conventions for resources
- Tag all resources with cost center, project, environment
- Use infrastructure as code (Terraform, CDK, Bicep)

### Monitoring & Observability

**MUST** integrate:

- **APM**: New Relic, Datadog, Dynatrace (corporate standard)
- **Logging**: Splunk, ELK, Azure Monitor
- **Error Tracking**: Sentry (corporate instance)
- **Alerts**: PagerDuty, OpsGenie integration

---

## Compliance

### Security Requirements

**MUST**:

- Pass corporate security review before deployment
- Implement OWASP Top 10 protections
- Use corporate SSL/TLS certificates
- Implement rate limiting and DDoS protection
- Enable WAF (Web Application Firewall)

### Audit & Logging

**MUST**:

- Log all authentication attempts
- Log all data access (read, write, delete)
- Retain logs per corporate retention policy (typically 90 days minimum)
- Enable tamper-proof logging
- Implement log forwarding to SIEM

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

1. Document violation in `.guidelines-todo.md` with:
   - Justification
   - Business impact
   - Temporary workaround
   - Timeline for resolution
2. Create JIRA ticket for permanent solution (target: next sprint)
3. Get approval from Architecture Review Board
4. Proceed with alternative, mark with `// GUIDELINE-VIOLATION: Ticket #XXX` comment
5. Schedule tech debt review within 30 days
6. Add item to architecture decision records (ADR)

**Escalation Process**:

1. Team Lead (< 1 day deviation)
2. Engineering Manager (< 1 week deviation)
3. Architecture Review Board (> 1 week deviation or security impact)
4. CTO (compliance or legal impact)

---

## Support & Resources

### Corporate Resources

- **Internal Wiki**: <https://wiki.yourorg.com/react-guidelines>
- **Component Library**: <https://storybook.yourorg.com>
- **API Documentation**: <https://api-docs.yourorg.com>
- **Slack Channel**: #frontend-support
- **Office Hours**: Tuesdays 2-3 PM EST

### Training

- **Required**: React Security Training (annual)
- **Required**: Corporate Component Library Workshop (for new hires)
- **Recommended**: Advanced React Patterns
- **Recommended**: Performance Optimization Workshop

### Code Review Checklist

Before submitting PR:

- [ ] Uses `@YOUR_ORG/ui-components` for all UI elements
- [ ] Uses `@YOUR_ORG/auth-client` for authentication
- [ ] Uses `@YOUR_ORG/api-client` for API calls
- [ ] Uses `@YOUR_ORG/logger` for logging (no console.log)
- [ ] No banned libraries imported
- [ ] Security scan passed (npm audit)
- [ ] Tests written and passing (80%+ coverage)
- [ ] Accessibility tested (axe DevTools)
- [ ] Performance budget met (bundle size < 500KB)
- [ ] `.npmrc` configured for corporate registry
- [ ] Environment variables validated
- [ ] No secrets committed to code

---

**Last Review**: 2025-11-16
**Next Review**: 2025-02-16 (quarterly)
**Owner**: Frontend Architecture Team
**Contact**: <frontend-arch@yourorg.com>
