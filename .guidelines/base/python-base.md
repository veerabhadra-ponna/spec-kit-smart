# Python Base Guidelines

**Tech Stack**: Python 3.11/3.12, FastAPI, Django 5, Flask 3, Backend Services, APIs, ML/AI
**Auto-detected from**: `requirements.txt`, `pyproject.toml`, `setup.py`
**Version**: 3.0 (Profile-Based Architecture)
**Last Updated**: 2025-11-16

---

## Target Platform

**MUST**:

- Use Python 3.11+ or Python 3.12+ for new projects
- Use virtual environments (venv, conda, poetry)
- Use type hints for better code quality

**Rationale**: Python 3.11+ provides significant performance improvements and better error messages

---

## Framework Selection

**FastAPI**: Modern, fast, automatic API docs, type-based validation (recommended for APIs)
**Django 5.x**: Full-featured, ORM, admin panel, batteries-included (recommended for full-stack)
**Flask 3.x**: Lightweight, flexible, minimalist

---

## Architecture & Best Practices

- Follow PEP 8 style guide
- Use type hints (mypy for static checking)
- Implement proper package structure
- Use dataclasses or Pydantic models
- Handle exceptions properly
- Write docstrings for functions and classes

---

## Security

- Validate all inputs (Pydantic, marshmallow)
- Use parameterized queries (prevent SQL injection)
- Implement authentication (JWT, OAuth)
- Use secure password hashing (bcrypt, argon2)
- Configure CORS properly
- Sanitize user inputs

---

## Testing

- pytest for testing (recommended)
- unittest for standard testing
- Aim for 80%+ code coverage
- Use fixtures for test data
- Mock external dependencies

---

## Database

**SQLAlchemy**: ORM for SQL databases (PostgreSQL, MySQL)
**Django ORM**: Built-in with Django
**Motor**: Async MongoDB driver
**Tortoise ORM**: Async ORM

---

## Dependency Management

**Poetry**: Modern dependency management (recommended)
**pip + requirements.txt**: Traditional approach
**Pipenv**: Virtual env + dependency management

---

**Note**: This is a base guideline. Full content migration from `archive/python-guidelines.md` in progress. Project-specific requirements (corporate libraries, registries) are defined in profile overrides.

**TODO**: Expand with full content including: async programming, logging, monitoring, deployment, coding standards, performance optimization, and ML/AI specific guidelines.
