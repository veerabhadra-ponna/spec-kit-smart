# .NET Base Guidelines

**Tech Stack**: .NET 8 LTS, C# 12, ASP.NET Core, Backend Services, Web APIs, Blazor
**Auto-detected from**: `*.csproj`, `*.sln` files
**Version**: 3.0 (Profile-Based Architecture)
**Last Updated**: 2025-11-16

---

## Target Platform

**MUST**:

- Use .NET 8 LTS (Long-Term Support until November 2026)
- Use C# 12 for new projects
- Use ASP.NET Core for web applications

**Rationale**: .NET 8 LTS provides long-term support and modern features (native AOT, performance improvements)

---

## Framework Selection

**ASP.NET Core**: Web APIs, MVC applications (recommended)
**Blazor**: Web UI with C# (Server or WebAssembly)
**.NET MAUI**: Cross-platform mobile/desktop apps
**gRPC**: High-performance RPC framework

---

## Architecture & Best Practices

- Follow SOLID principles
- Use dependency injection (built-in DI container)
- Implement layered architecture (Controller → Service → Repository)
- Use DTOs for API contracts
- Implement proper exception handling
- Use async/await for I/O operations

---

## Security

- Validate all inputs (FluentValidation, DataAnnotations)
- Use parameterized queries (Entity Framework Core)
- Implement authentication (JWT, Identity, Azure AD)
- Use Identity for user management
- Configure CORS properly
- Enable HTTPS

---

## Testing

- xUnit (recommended)
- NUnit or MSTest
- Moq for mocking
- Integration tests with WebApplicationFactory
- Aim for 80%+ code coverage

---

## Database

**Entity Framework Core 8.x**: ORM (recommended)
**Dapper**: Lightweight micro-ORM
**ADO.NET**: Low-level database access

---

## Dependency Management

**NuGet**: Package manager (nuget.org)
**dotnet CLI**: Command-line tools

---

**Note**: This is a base guideline. Full content migration from `archive/dotnet-guidelines.md` in progress. Project-specific requirements (corporate libraries, registries) are defined in profile overrides.

**TODO**: Expand with full content including: logging, monitoring, deployment, coding standards, performance optimization, and detailed framework guides.
