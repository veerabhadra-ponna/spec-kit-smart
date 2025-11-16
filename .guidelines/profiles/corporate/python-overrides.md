# Python Corporate Profile Overrides

**Profile**: Corporate
**Stack**: Python
**Version**: 3.0
**Last Updated**: 2025-11-16

> **Note**: This file contains only corporate-specific overrides. Base guidelines are inherited from `base/python-base.md`.

---

## Scaffolding

**MUST**: Use `@YOUR_ORG/python-template` or corporate cookiecutter templates

## Package Registry

**MUST**: Configure pip to use corporate PyPI mirror

```ini
# pip.conf or .pypirc
[global]
index-url = https://pypi.yourorg.com/simple
trusted-host = pypi.yourorg.com
```

## Mandatory Libraries

- **Framework**: Corporate FastAPI/Django starter
- **Authentication**: `yourorg-auth-client`
- **Logging**: `yourorg-logger`
- **Metrics**: `yourorg-metrics`
- **Database**: `yourorg-db-extensions`

## Deployment

- Corporate Kubernetes/Docker
- CI/CD via Jenkins/GitLab CI
- Internal container registry

**Note**: Full content migration in progress. See `archive/python-guidelines.md` for complete corporate requirements.
