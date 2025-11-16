# .NET Corporate Profile Overrides

**Profile**: Corporate
**Stack**: .NET
**Version**: 3.0
**Last Updated**: 2025-11-16

> **Note**: This file contains only corporate-specific overrides. Base guidelines are inherited from `base/dotnet-base.md`.

---

## Scaffolding

**MUST**: Use corporate .NET templates via `dotnet new`

## Package Registry

**MUST**: Configure NuGet to use corporate feed

```xml
<!-- nuget.config -->
<configuration>
  <packageSources>
    <add key="CorporateFeed" value="https://nuget.yourorg.com/v3/index.json" />
  </packageSources>
</configuration>
```

## Mandatory Libraries

- **Framework**: Corporate ASP.NET starter templates
- **Authentication**: `YourOrg.Identity.Client`
- **Logging**: `YourOrg.Logging`
- **Metrics**: `YourOrg.Telemetry`
- **Database**: `YourOrg.Data.Extensions`

## Deployment

- Corporate Azure/AWS environments
- CI/CD via Azure DevOps
- Internal container registry

**Note**: Full content migration in progress. See `archive/dotnet-guidelines.md` for complete corporate requirements.
