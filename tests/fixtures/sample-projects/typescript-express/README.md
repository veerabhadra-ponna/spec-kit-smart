# TypeScript Express Test Fixture

This is a test fixture project for the codebase indexing system.

## Purpose

Tests the indexing system's ability to extract:
- **Classes**: `User`, `AuthService`
- **Interfaces**: `IUser`
- **Functions**: `validateEmail`
- **REST Endpoints**: `/login`, `/register`, `/profile`
- **External APIs**: Stripe integration
- **Dependencies**: express, stripe imports

## Structure

```
src/
├── models/User.ts       - User model with class, interface, function
├── routes/auth.ts       - Express routes (3 REST endpoints)
└── services/AuthService.ts - Business logic with Stripe integration
```

## Expected Index Output

- 2 classes (User, AuthService)
- 1 interface (IUser)
- 1 function (validateEmail)
- 3 REST endpoints (POST /login, POST /register, GET /profile)
- 1 external service (Stripe)
- 1 environment variable (STRIPE_SECRET_KEY)
