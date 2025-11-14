# Python Corporate Guidelines

**Tech Stack**: Python 3.11/3.12, FastAPI 0.110+, Django 5.0+, Flask 3.0+, Backend Services, APIs, Data Processing, ML/AI
**Auto-detected from**: `requirements.txt`, `pyproject.toml`, `setup.py`, `poetry.lock`, or `*.py` files
**Version**: 2.0
**Last Updated**: 2025-01-15

---

## Target Platform

**MUST**:

- Use Python 3.11 (stable) or Python 3.12 (latest stable, recommended)
- Use type hints for all function signatures
- Enable type checking with mypy or pyright

**SHOULD**:

- Upgrade to Python 3.13 when stable and dependencies support it
- Use modern Python features (pattern matching, structural pattern matching, tomllib)
- Use f-strings for string formatting (never % or .format())

**Rationale**: Python 3.11 provides 2x performance improvements, Python 3.12 adds per-interpreter GIL removal prep, better error messages, and performance gains

---

## Scaffolding

**MUST**:

- Use corporate scaffolding command (`YOUR_ORG.cli create-service`)
- Choose appropriate framework template:
  - **fastapi**: Modern async REST API (recommended for new APIs)
  - **fastapi-minimal**: Lightweight FastAPI service
  - **django**: Full-featured web framework with ORM, admin panel
  - **flask**: Lightweight traditional framework
  - **grpc**: gRPC service for inter-service communication
  - **celery-worker**: Background task worker
  - **data-pipeline**: ETL/data processing service

**NEVER**:

- Use public `django-admin startproject` or `flask init` directly without corporate template

**Rationale**: Corporate scaffolding includes security, logging, monitoring, compliance, observability, type stubs from day one

---

## Dependency Management

**MUST** use one of:

- **Poetry 1.7+**: Modern dependency management, lock file, virtual env (recommended)
- **uv**: Ultra-fast pip replacement, compatible with pip (new, very fast)
- **pip-tools**: Requirements pinning with pip-compile (traditional)
- **PDM**: Modern package manager with PEP 582 support

**NEVER**:

- Use `pip install` directly without lock file in production
- Mix multiple dependency managers in same project

**Poetry Best Practices**:

```toml
[tool.poetry]
name = "your-service"
version = "1.0.0"
python = "^3.11"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.110.0"
uvicorn = {extras = ["standard"], version = "^0.27.0"}

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
mypy = "^1.8.0"
ruff = "^0.2.0"
```

---

## Package Registry

**MUST**:

- Configure `pip.conf` or `poetry config` with corporate PyPI repository (Artifactory, Nexus, Azure Artifacts)
- All packages resolved through corporate registry only
- Use authentication tokens (never plaintext passwords)

**NEVER**:

- Install packages from public pypi.org directly without security scanning

**Configuration**:

- pip: `~/.config/pip/pip.conf` or project-level `pip.conf`
- Poetry: `poetry config repositories.corporate https://pypi.yourorg.com`
- Use environment variables for credentials in CI/CD

---

## Mandatory Libraries

### Framework Starter

**MUST** use one of: `YOUR_ORG-fastapi-starter`, `YOUR_ORG-django-starter`, or `YOUR_ORG-flask-starter`
**Includes**: Security middleware, logging, metrics, error handling, CORS, health checks, observability, OpenAPI docs
**Integration**: Use `create_app()` factory function with corporate configuration

**Framework Selection**:

- **FastAPI 0.110+**: Modern async framework, automatic OpenAPI, Pydantic validation, high performance (recommended for new APIs)
- **Django 5.0+**: Full-featured web framework, ORM, admin panel, authentication, large ecosystem (recommended for full web apps)
- **Flask 3.0+**: Lightweight, flexible, mature ecosystem (legacy projects, simple APIs)
- **Starlette**: ASGI framework, FastAPI's foundation (when you need minimal async framework)
- **Litestar**: Modern ASGI framework, OpenAPI, dependency injection (FastAPI alternative)

**Async vs Sync**:

- Use async frameworks (FastAPI, Starlette) for I/O-bound workloads with high concurrency
- Use sync frameworks (Django, Flask) for traditional request-response patterns
- Use async database drivers (asyncpg, motor) with async frameworks

### Authentication & Authorization

**MUST** use: `YOUR_ORG-auth` package
**Requirements**:

- Decorate endpoints with `@require_auth` and `@require_roles()` decorators
- Extract authenticated user via `get_current_user()` dependency (FastAPI) or decorator (Django/Flask)
- Pass user context to all service layer calls
- Support OAuth 2.0, JWT bearer tokens, OpenID Connect

**Advanced Features**:

- Multi-tenant authentication with tenant isolation
- API key authentication for service-to-service communication
- Certificate-based mutual TLS (mTLS) for high-security scenarios
- Session management with Redis for stateful applications
- Token refresh mechanisms with sliding expiration

**Cloud-Specific**:

- Azure AD / Entra ID integration with MSAL
- AWS Cognito with boto3 SDK
- Google Identity Platform support

**On-Premise**:

- LDAP/Active Directory integration with python-ldap
- SAML 2.0 SSO with python3-saml
- Custom JWT validation with PyJWT

**FastAPI Example**:

```python
from fastapi import Depends, HTTPException
from yourorg_auth import get_current_user, require_roles

@app.get("/admin")
@require_roles(["admin"])
async def admin_endpoint(user = Depends(get_current_user)):
    return {"user": user.username}
```

### API Client & Resilience

**MUST** use: `YOUR_ORG-http-client` package
**Requirements**:

- Use `YourOrgHttpClient` class for external API calls
- Configure timeout, retry attempts (exponential backoff), circuit breaker
- Never use raw `requests`, `httpx`, `aiohttp` directly
- All external calls auto-instrumented for distributed tracing

**Features**:

- Automatic retry with jitter and exponential backoff
- Timeout handling with graceful degradation
- Circuit breaker patterns (open, half-open, closed states)
- Distributed tracing with OpenTelemetry
- Request/response interceptors for logging, authentication
- Connection pooling and keep-alive
- Async and sync clients

**Recommended Base Library**:

- **httpx**: Modern HTTP client, sync and async, HTTP/2 support (recommended)
- **requests**: Battle-tested, sync-only (legacy projects)
- **aiohttp**: Async HTTP client (FastAPI with async)

**Cloud-Specific**:

- Azure SDK for Python (azure-*)
- AWS SDK for Python (boto3)

**On-Premise**:

- `pika` for RabbitMQ with retry patterns
- `confluent-kafka` or `aiokafka` for Apache Kafka

### Database - SQL (SQLAlchemy)

**MUST** use: SQLAlchemy 2.0+ with Alembic for migrations
**MUST** use: `YOUR_ORG-sqlalchemy-utils` for corporate extensions
**Requirements**:

- Use SQLAlchemy 2.0 style (new query API)
- Entities inherit from `AuditMixin` for automatic audit trail (created_by, created_at, updated_by, updated_at, version)
- Use Alembic for schema migrations
- Apply migrations on deployment automatically
- Use async drivers for async frameworks (asyncpg, aiomysql)

**SQLAlchemy 2.0 Best Practices**:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from yourorg_sqlalchemy import AuditMixin

class Base(DeclarativeBase):
    pass

class User(Base, AuditMixin):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]

# Modern query API
stmt = select(User).where(User.username == "john")
result = await session.execute(stmt)
user = result.scalar_one()
```

**Supported Databases**:

- PostgreSQL 14+ (cloud: Azure Database, AWS RDS, on-premise) - **Recommended**
- MySQL 8+ / MariaDB 10.6+ (cloud: Azure, AWS, on-premise)
- SQLite (development/testing only, not production)
- Oracle (on-premise: Oracle 19c+)
- SQL Server (cloud: Azure SQL, on-premise)

**Async Drivers**:

- PostgreSQL: `asyncpg` (fastest) or `psycopg3` (async mode)
- MySQL: `aiomysql` or `asyncmy`
- SQLite: `aiosqlite`

**Cloud-Specific**:

- Use connection pooling with SQLAlchemy async engine
- Use managed identity authentication (Azure, AWS)
- Use read replicas for read-heavy workloads

### Database - NoSQL (MongoDB)

**SHOULD** use one of:

- **Motor 3.x**: Async MongoDB driver for Python (recommended with FastAPI)
- **PyMongo 4.x**: Sync MongoDB driver (traditional, use with Flask/Django)
- **Beanie**: Async ODM built on Motor and Pydantic (recommended for FastAPI)
- **MongoEngine**: Sync ODM (legacy Django projects)

**Requirements**:

- Define Pydantic models for documents (when using Beanie)
- Use indexes for frequently queried fields
- Implement proper error handling and retry logic

**Cloud-Specific**:

- Azure Cosmos DB (MongoDB API)
- AWS DocumentDB (MongoDB-compatible)
- MongoDB Atlas (fully managed)

**On-Premise**:

- MongoDB 6.0+ with replica sets for high availability
- Sharding for horizontal scalability

### Caching

**MUST** use: `YOUR_ORG-cache` package (wraps Redis client)
**Requirements**:

- Use async Redis client (redis-py with async support or aioredis)
- Use distributed cache (Redis) for multi-instance deployments
- Use in-memory cache (cachetools, functools.lru_cache) only for single-instance or immutable data
- Implement cache-aside pattern with appropriate TTL
- Use cache invalidation strategies (time-based, event-based, manual)

**Redis Clients**:

- **redis-py 5.x**: Official Redis client, sync and async support (recommended)
- **aioredis**: Deprecated, merged into redis-py
- **hiredis**: C parser for redis-py (performance boost)

**Use Cases**:

- Response caching with TTL
- Session storage
- Rate limiting counters
- Pub/Sub for real-time features
- Distributed locks

**Cloud-Specific**:

- Azure Cache for Redis (managed)
- AWS ElastiCache for Redis (managed)

**On-Premise**:

- Redis 7+ with Sentinel for high availability
- Redis Cluster for horizontal scalability

### Logging & Observability

**MUST** use: Python standard logging with `YOUR_ORG-logging` extensions
**Requirements**:

- Use structured logging with JSON formatter (python-json-logger)
- Include correlation ID, trace ID in all log statements
- Never log PII, secrets, passwords, tokens, credit card numbers, SSNs
- Export logs to corporate logging platform (Elasticsearch, Splunk, Azure Monitor, AWS CloudWatch)

**Recommended Setup**:

```python
import logging
from pythonjsonlogger import jsonlogger
from yourorg_logging import configure_logging

logger = logging.getLogger(__name__)

# Corporate logger with structured logging
configure_logging(
    level="INFO",
    format_json=True,
    include_trace_context=True
)

logger.info("User login", extra={
    "user_id": user.id,
    "ip_address": request.client.host,
    "user_agent": request.headers.get("user-agent")
})
```

**Log Levels**:

- **DEBUG**: Development debugging (disabled in production)
- **INFO**: General informational messages
- **WARNING**: Unexpected behavior that doesn't prevent operation
- **ERROR**: Errors requiring investigation
- **CRITICAL**: System failures requiring immediate attention

**NEVER**:

- Use `print()` statements for logging
- Use `logging.basicConfig()` directly (use corporate configuration)

**Distributed Tracing**:

- Enable OpenTelemetry instrumentation for HTTP, database, caching
- Export traces to Jaeger, Zipkin, Azure Application Insights, AWS X-Ray
- Use trace context propagation (W3C Trace Context)
- Implement trace sampling strategies for high-throughput systems

### Validation

**MUST** use: Pydantic 2.x for request/response validation
**Requirements**:

- Define Pydantic models for all API requests and responses
- Use field validators for custom validation logic
- Return 422 Unprocessable Entity for validation errors
- Use Pydantic's JSON Schema generation for OpenAPI docs

**Pydantic 2.x Best Practices**:

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Annotated

class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    age: Annotated[int, Field(gt=0, lt=150)]
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username": "johndoe",
                "email": "john@example.com",
                "age": 30
            }]
        }
    }
```

**Features**:

- Type coercion and validation
- Custom validators with decorators
- Nested models and complex types
- JSON Schema generation
- Serialization and deserialization
- Performance improvements in v2 (Rust core)

### Background Jobs & Task Queues

**MUST** use one of:

- **Celery 5.x**: Distributed task queue, mature, feature-rich (recommended for complex workflows)
- **Dramatiq**: Simple, reliable, Redis/RabbitMQ backends
- **RQ (Redis Queue)**: Simple Redis-based queue (good for simple use cases)
- **Arq**: Async task queue for asyncio (FastAPI integration)
- **Huey**: Lightweight task queue (SQLite/Redis backends)

**Requirements**:

- Use persistent broker (Redis, RabbitMQ, AWS SQS) for job state
- Implement idempotent task handlers (support retries)
- Use task priorities and routing
- Monitor task success/failure rates
- Use flower (Celery) or web UI for monitoring

**Use Cases**:

- Scheduled report generation
- Email/notification sending with retry
- Image/video processing
- Data synchronization and ETL
- Machine learning model training

**Cloud-Specific**:

- Azure Functions with Durable Functions
- AWS Lambda with SQS triggers
- Google Cloud Tasks

**On-Premise**:

- Celery with Redis or RabbitMQ broker
- Kubernetes CronJobs for scheduled tasks

### API Documentation

**MUST**:

- FastAPI: OpenAPI docs generated automatically at `/docs` (Swagger UI) and `/redoc` (ReDoc)
- Django: Use drf-spectacular for Django REST Framework OpenAPI generation
- Flask: Use flask-swagger-ui or flasgger for Swagger integration

**Requirements**:

- Include request/response examples with Pydantic models
- Document error responses and status codes
- Expose Swagger UI at `/docs` or `/api-docs` (development only in production)
- Export OpenAPI spec at `/openapi.json` for API gateway registration
- Version APIs explicitly (URL versioning `/api/v1/...`)

**FastAPI Automatic Documentation**:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Your Service API",
    description="API for managing resources",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json"
)

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """
    Create a new user.
    
    - **username**: unique username (3-50 chars)
    - **email**: valid email address
    - **age**: user age (must be positive)
    """
    # Implementation
    pass
```

---

## Banned Libraries

**NEVER** use:

- Raw `requests` without wrapper → Use `YOUR_ORG-http-client`
- `urllib` or `urllib3` directly → Use httpx or requests wrapper
- Direct JWT handling → Use `YOUR_ORG-auth`
- `print()` statements → Use proper logging
- `eval()` or `exec()` → Security risk
- `pickle` for untrusted data → Use JSON or Protobuf
- Old async libraries (asyncore, asynchat) → Use asyncio

**Security Concerns**:

- Avoid packages with known vulnerabilities (run `pip-audit` or `safety check`)
- Avoid unmaintained packages (check PyPI last update date)
- Prefer packages with type stubs (py.typed marker)

**Rationale**: Corporate libraries enforce security, observability, compliance; deprecated libraries lack support

---

## Architecture

### Project Structure - Domain-Driven Design (Recommended)

**SHOULD** use: Domain/feature-based organization for better cohesion

```text
src/
├── domain/
│   ├── users/
│   │   ├── models.py        # Domain models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── service.py       # Business logic
│   │   ├── repository.py    # Data access
│   │   └── router.py        # API routes
│   ├── orders/
│   └── products/
├── infrastructure/
│   ├── database.py          # DB connection
│   ├── cache.py             # Redis connection
│   └── messaging.py         # Message queue
├── shared/
│   ├── middleware/
│   ├── dependencies.py      # FastAPI dependencies
│   └── exceptions.py        # Custom exceptions
├── config.py                # Configuration
└── main.py                  # Application entry
```

**Benefits**: Clear bounded contexts, better encapsulation, easier testing

### Project Structure - Layered (Acceptable)

**MAY** use: Traditional layered architecture for simple applications

```text
src/
├── api/
│   ├── routes/
│   └── dependencies.py
├── services/            # Business logic
├── repositories/        # Data access
├── models/             # Database models
├── schemas/            # Pydantic schemas
├── core/
│   ├── config.py
│   └── security.py
└── main.py
```

### Separation of Concerns

**MUST**:

- Keep route handlers thin (routing, validation only)
- Put business logic in service layer
- Use repository pattern for database access
- Never put business logic in routes or repositories
- Use dependency injection (FastAPI dependencies)

### Type Safety

**MUST**:

- Use type hints for all function signatures
- Define return types explicitly
- Use `typing` module for complex types (List, Dict, Optional, Union, TypedDict)
- Enable strict mode in mypy or pyright

**Type Checking Configuration** (pyproject.toml):

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.11"
```

**Modern Type Hints**:

```python
from typing import Annotated
from collections.abc import Sequence

# Use Annotated for metadata
UserId = Annotated[int, "Unique user identifier"]

# Use new union syntax (Python 3.10+)
def get_user(user_id: int) -> User | None:
    pass

# Use Sequence instead of List for immutability
def process_items(items: Sequence[Item]) -> list[Result]:
    pass
```

### Error Handling

**MUST**:

- Use exception handling middleware or exception handlers
- Create custom exception classes inheriting from built-in exceptions
- Return generic error messages to clients (no internal details, stack traces)
- Log full exception details server-side with stack traces and correlation IDs
- Return RFC 7807 Problem Details for API errors

**Status Code Mapping**:

- ValidationError → 422 Unprocessable Entity (Pydantic default)
- ValueError → 400 Bad Request
- UnauthorizedError → 401 Unauthorized
- ForbiddenError → 403 Forbidden
- NotFoundError → 404 Not Found
- ConflictError → 409 Conflict
- InternalServerError → 500 Internal Server Error
- ServiceUnavailableError → 503 Service Unavailable

**FastAPI Exception Handling**:

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=exc, extra={"request_id": request.state.request_id})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "request_id": request.state.request_id}
    )
```

---

## Security

### Input Validation

**MUST**:

- Validate all API inputs using Pydantic models
- Return 422 Unprocessable Entity for validation errors
- Sanitize user inputs before processing (XSS prevention)
- Validate file uploads (type, size, content, virus scan)
- Use Pydantic's field validators for custom validation

### SQL Injection Prevention

**MUST**:

- Use SQLAlchemy ORM (parameterized queries automatic)
- Never concatenate strings for SQL queries
- Use query parameters for all dynamic values
- Use SQLAlchemy's text() with bound parameters if raw SQL needed

**Safe Raw SQL**:

```python
from sqlalchemy import text

# Safe - parameterized query
stmt = text("SELECT * FROM users WHERE username = :username")
result = await session.execute(stmt, {"username": username})
```

### NoSQL Injection Prevention

**MUST**:

- Use ODM (Beanie, MongoEngine) for query construction
- Validate user inputs with Pydantic before database queries
- Never pass user input directly to MongoDB queries
- Use query builders, not string concatenation

### Secrets Management

**MUST**:

- Store secrets in environment variables or corporate secrets manager
- Load secrets via configuration management (never hardcode)
- Use `.env` files for local development (gitignored)
- Use pydantic-settings for configuration management
- Rotate secrets regularly (automated via secret manager)

**NEVER**:

- Hardcode secrets in code or configuration files
- Commit secrets to source control
- Store secrets in plain text environment variables (production)

**Configuration Management** (Pydantic Settings):

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    api_key: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
```

**Cloud-Specific**:

- Azure Key Vault with `azure-keyvault-secrets`
- AWS Secrets Manager with boto3
- Use managed identities (Azure, AWS) for authentication

### Authentication Best Practices

**SHOULD**:

- Use bcrypt or argon2 for password hashing
  - **argon2-cffi**: More secure, recommended for new projects
  - **bcrypt**: Well-tested, industry standard
- Implement password complexity requirements
- Support multi-factor authentication (MFA) for sensitive operations
- Use JWTs with short expiration (15 min) + refresh tokens (7 days)
- Store refresh tokens in database (allow revocation)
- Use secure, httpOnly, sameSite cookies for tokens (if cookie-based auth)

**Password Hashing**:

```python
from argon2 import PasswordHasher

ph = PasswordHasher()

# Hash password
hashed = ph.hash(password)

# Verify password
try:
    ph.verify(hashed, password)
except:
    raise ValueError("Invalid password")
```

### Rate Limiting

**MUST**:

- Implement rate limiting on public endpoints
- Use `slowapi` (FastAPI) or `flask-limiter` (Flask)
- Configure limits based on:
  - IP address (anonymous users)
  - User ID (authenticated users)
  - API key (service accounts)
- Return 429 Too Many Requests when limits exceeded

**FastAPI Rate Limiting**:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/resource")
@limiter.limit("10/minute")
async def get_resource(request: Request):
    return {"data": "resource"}
```

### Security Headers & CORS

**MUST**:

- Configure CORS restrictively (don't use `*` for origins)
- Use security middleware for headers

**FastAPI Security**:

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.yourorg.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.yourorg.com", "yourorg.com"]
)
```

---

## Coding Standards

### Python Version & Modern Features

**MUST**:

- Use Python 3.11 or Python 3.12
- Use type hints for all public APIs
- Use f-strings for string formatting

**SHOULD** use modern features:

- Pattern matching (match/case) - Python 3.10+
- Structural pattern matching
- Union types with `|` operator - Python 3.10+
- `TypedDict` for dictionary typing
- `dataclasses` or Pydantic models for data structures
- Context managers (`with` statement)
- Generator expressions and comprehensions

### Code Style & Quality

**MUST**:

- Follow PEP 8 style guide
- Use **Ruff** 0.2+ for linting and formatting (fastest, replaces Black + isort + Flake8)
- Use mypy or pyright for type checking

**Alternative** (traditional):

- Black for formatting
- isort for import sorting
- Flake8 or Pylint for linting

**Ruff Configuration** (pyproject.toml):

```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = ["E501"]  # line too long (handled by formatter)

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Naming Conventions

**MUST** follow PEP 8:

- Functions, variables, parameters: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods/attributes: `_leading_underscore`
- Modules: `lowercase` or `snake_case`
- Packages: `lowercase` (no underscores)

### Async/Await (AsyncIO)

**SHOULD** use for I/O-bound operations:

- Use async/await with FastAPI, aiohttp, asyncio
- Use async database drivers (asyncpg, motor, aioredis)
- Use `asyncio.gather()` for parallel operations
- Use `asyncio.create_task()` for background tasks
- Use `async with` for async context managers

**NEVER**:

- Mix blocking code in async functions (blocks event loop)
- Use `asyncio.run()` inside async functions
- Use threading for I/O operations (use asyncio instead)

**Async Best Practices**:

```python
import asyncio
from typing import Sequence

async def fetch_user(user_id: int) -> User:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
        return User(**response.json())

async def fetch_multiple_users(user_ids: Sequence[int]) -> list[User]:
    tasks = [fetch_user(user_id) for user_id in user_ids]
    return await asyncio.gather(*tasks)
```

### Code Quality

**SHOULD**:

- Keep functions under 50 lines (extract to helper functions)
- Limit cyclomatic complexity (< 10 per function, measure with radon)
- Write docstrings for public functions and classes (Google style or NumPy style)
- Use meaningful names (avoid abbreviations, no single letters except loops)
- Prefer composition over inheritance
- Use dataclasses or Pydantic models instead of raw dictionaries
- Use context managers for resource management
- Use list comprehensions for simple transformations
- Avoid mutable default arguments

**Docstring Example** (Google style):

```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculate discounted price.
    
    Args:
        price: Original price of the item
        discount_rate: Discount rate as decimal (0.0 to 1.0)
        
    Returns:
        Discounted price
        
    Raises:
        ValueError: If discount_rate is not between 0 and 1
    """
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")
    return price * (1 - discount_rate)
```

---

## Testing

### Unit Testing

**MUST**:

- Write unit tests using pytest 8.x
- Aim for 80%+ coverage on business logic
- Use fixtures for test data and setup
- Mock external dependencies (databases, HTTP calls)

**SHOULD**:

- Use `pytest-asyncio` for async tests
- Use `pytest-cov` for coverage reports
- Use `pytest-mock` for mocking
- Use `factory_boy` or `faker` for test data generation
- Use `hypothesis` for property-based testing

**Pytest Best Practices**:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
```

### Integration Testing

**MUST**:

- Write integration tests for API endpoints
- Test database interactions with test databases
- Use TestContainers for realistic test environments

**SHOULD**:

- Use `testcontainers-python` for Docker-based test dependencies
- Use separate test databases (never production)
- Reset database state between tests
- Use `pytest-docker` for Docker Compose integration

### Test Naming

**MUST** follow:

- Test functions: `test_<function_name>_<scenario>_<expected>`
- Example: `test_create_user_with_invalid_email_returns_422`
- Use descriptive names (no abbreviations)

---

## Build & Deployment

### Build Process

**MUST**:

- Run tests before deployment (`pytest`)
- Run linters before deployment (`ruff check`)
- Run formatters before deployment (`ruff format`)
- Run type checkers before deployment (`mypy`)
- Use CI/CD pipeline for automated testing

**CI/CD**:

- Run linters (Ruff, mypy)
- Run security scanning (pip-audit, safety, bandit)
- Generate code coverage reports (coverage.py, pytest-cov)
- Publish packages to corporate PyPI registry

### Docker - Cloud Deployments

**MUST**:

- Use multi-stage builds (build dependencies in build stage)
- Use official Python base images:
  - Build: `python:3.12-slim` (Debian-based, smaller)
  - Runtime: Same as build
- Run as non-root user in container
- Copy only necessary files (use `.dockerignore`)
- Use layer caching for faster builds

**Dockerfile Example**:

```dockerfile
# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 appuser \
    && adduser --system --uid 1001 --gid 1001 appuser

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**SHOULD**:

- Keep container images small (< 200MB for simple services)
- Use health checks in Dockerfile (`HEALTHCHECK` instruction)
- Set resource limits (CPU, memory) in container runtime
- Use `.dockerignore` to exclude tests, dev dependencies, .venv

**Cloud-Specific**:

- **Azure**: Deploy to Azure Container Apps, Azure Kubernetes Service (AKS), Azure App Service
- **AWS**: Deploy to ECS, EKS, Lambda (with container image support)
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

### ASGI Servers

**MUST** use for production:

- **Uvicorn with Gunicorn**: `gunicorn -k uvicorn.workers.UvicornWorker` (recommended)
- **Uvicorn**: Standalone (development, single worker)
- **Hypercorn**: Alternative ASGI server, HTTP/2 support

**Configuration**:

```bash
# Production with multiple workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

---

## Observability

### Health Checks

**MUST** include:

- Liveness probe (`/health/live`): Indicates if app is running
- Readiness probe (`/health/ready`): Indicates if app can accept traffic
- Check critical dependencies: database, cache, message queue, external APIs

**FastAPI Health Checks**:

```python
@app.get("/health/live")
async def liveness():
    return {"status": "UP"}

@app.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        await redis.ping()
        return {"status": "UP", "checks": {"db": "UP", "redis": "UP"}}
    except Exception as e:
        logger.error("Readiness check failed", exc_info=e)
        return JSONResponse(
            status_code=503,
            content={"status": "DOWN", "error": str(e)}
        )
```

### Metrics

**MUST** include:

- Expose metrics endpoint (`/metrics`) in Prometheus format
- Track request rate, error rate, duration (RED metrics)
- Track Python runtime metrics (memory, GC, threads)
- Track custom business metrics

**Tools**:

- **prometheus-client**: Official Prometheus Python client
- **prometheus-fastapi-instrumentator**: FastAPI middleware for metrics
- Prometheus for metric collection
- Grafana for visualization
- Azure Monitor, AWS CloudWatch for cloud deployments

**FastAPI Metrics**:

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)
```

### Distributed Tracing

**MUST**:

- Enable OpenTelemetry instrumentation
- Export traces to Jaeger, Zipkin, Azure Application Insights, AWS X-Ray
- Include trace context in all outgoing requests
- Implement custom spans for critical operations

**OpenTelemetry Setup**:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Configure tracer
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
```

### Application Performance Monitoring (APM)

**SHOULD** use:

- Application Insights (Azure)
- AWS X-Ray (AWS)
- New Relic, Datadog, Dynatrace (multi-cloud)
- Elastic APM (on-premise)

---

## Performance & Scalability

### Concurrency Models

**CHOOSE** based on use case:

- **AsyncIO**: I/O-bound workloads, high concurrency (FastAPI)
- **Threading**: I/O-bound workloads, moderate concurrency (Flask, Django)
- **Multiprocessing**: CPU-bound workloads, parallel processing
- **Celery**: Distributed task processing

**NEVER**:

- Use threading for CPU-bound tasks (GIL limitation)
- Mix async and sync code incorrectly (use `asyncio.to_thread()` for sync calls in async code)

### Caching Strategy

**SHOULD**:

- Cache frequently accessed, rarely changed data
- Use functools.lru_cache for function-level caching
- Use Redis for distributed caching
- Implement cache warming for critical data
- Use cache invalidation strategies

### Database Optimization

**SHOULD**:

- Use connection pooling (SQLAlchemy engine configuration)
- Use indexes on frequently queried columns
- Use async drivers for async frameworks
- Use read replicas for read-heavy workloads
- Use query optimization (avoid N+1 queries)
- Use database-specific optimizations (PostgreSQL EXPLAIN ANALYZE)

### Horizontal Scaling

**MUST**:

- Design stateless services (store session in Redis, database)
- Use load balancers (Azure Load Balancer, AWS ELB, NGINX)
- Implement auto-scaling based on metrics
- Use Gunicorn with multiple workers for ASGI apps

---

## Machine Learning & Data Science

### ML Frameworks (If Applicable)

**SHOULD** use:

- **PyTorch 2.x**: Deep learning, research, production
- **TensorFlow 2.x**: Deep learning, production deployment
- **scikit-learn 1.x**: Classical ML algorithms
- **XGBoost / LightGBM**: Gradient boosting
- **Hugging Face Transformers**: NLP, pre-trained models

### Data Processing

**SHOULD** use:

- **Pandas 2.x**: Data manipulation and analysis
- **Polars**: Fast DataFrame library (Rust-based, faster than Pandas)
- **NumPy**: Numerical computing
- **Apache Arrow**: Columnar data format, interoperability

### ML Model Serving

**SHOULD** use:

- **FastAPI**: REST API for model serving (recommended)
- **TorchServe**: PyTorch model serving
- **TensorFlow Serving**: TensorFlow model serving
- **MLflow**: ML lifecycle management
- **BentoML**: Model serving framework

---

## Compliance & Governance

### Data Protection

**MUST**:

- Implement GDPR, CCPA, LGPD compliance for personal data
- Encrypt data at rest and in transit
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
- Use pip-audit, safety, or Snyk for dependency scanning
- Use bandit for security scanning
- Run security scanning in CI/CD pipeline (SAST)
- Use Trivy for container image scanning

---

## Non-Compliance

If corporate library unavailable or causes blocking issue:

1. Document violation in `.guidelines-todo.md` with justification and business impact
2. Create ticket to resolve (target: next sprint)
3. Proceed with alternative, mark with `# TODO: GUIDELINE-VIOLATION - Ticket #XXX` comment for tracking
4. Schedule tech debt review within 30 days
