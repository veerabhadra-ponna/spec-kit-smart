Import-Module Pester

Describe 'PowerShell script JSON contracts' {
    BeforeAll {
        $script:RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..' '..')).Path
    }

    It 'create-new-feature emits structured JSON' {
        $testRoot = Join-Path $TestDrive 'feature-repo'
        New-Item -ItemType Directory -Path $testRoot -Force | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $testRoot '.specify/templates') -Force | Out-Null
        Copy-Item (Join-Path $RepoRoot 'templates/spec-template.md') (Join-Path $testRoot '.specify/templates/spec-template.md')
        Push-Location $testRoot
        try {
            $encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('Sample feature for tests'))
            $json = & (Join-Path $RepoRoot 'scripts/powershell/create-new-feature.ps1') -Json -EncodedArgs $encoded
            $obj = $json | ConvertFrom-Json
            $obj.ok | Should -BeTrue
            $obj.paths.feature_dir | Should -Match 'specs/001-'
            Test-Path $obj.paths.spec | Should -BeTrue
        }
        finally {
            Pop-Location
        }
    }

    It 'check-prerequisites paths-only mode returns JSON payload' {
        $testRoot = Join-Path $TestDrive 'prereq-repo'
        New-Item -ItemType Directory -Path $testRoot -Force | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $testRoot 'specs/001-test-feature') -Force | Out-Null
        Set-Content -Path (Join-Path $testRoot 'specs/001-test-feature/spec.md') -Value '# Spec' -Encoding utf8
        Set-Content -Path (Join-Path $testRoot 'specs/001-test-feature/plan.md') -Value '# Plan' -Encoding utf8
        $env:SPECIFY_FEATURE = '001-test-feature'
        Push-Location $testRoot
        try {
            $json = & (Join-Path $RepoRoot 'scripts/powershell/check-prerequisites.ps1') -Json -PathsOnly
            $obj = $json | ConvertFrom-Json
            $obj.paths.feature_dir | Should -Match '001-test-feature'
        }
        finally {
            Pop-Location
            Remove-Item Env:SPECIFY_FEATURE
        }
    }

    It 'setup-plan emits JSON with plan path' {
        $testRoot = Join-Path $TestDrive 'plan-repo'
        New-Item -ItemType Directory -Path (Join-Path $testRoot '.specify/templates') -Force | Out-Null
        Copy-Item (Join-Path $RepoRoot 'templates/plan-template.md') (Join-Path $testRoot '.specify/templates/plan-template.md')
        New-Item -ItemType Directory -Path (Join-Path $testRoot 'specs/001-test-feature') -Force | Out-Null
        Set-Content -Path (Join-Path $testRoot 'specs/001-test-feature/spec.md') -Value '# Spec' -Encoding utf8
        $env:SPECIFY_FEATURE = '001-test-feature'
        Push-Location $testRoot
        try {
            $json = & (Join-Path $RepoRoot 'scripts/powershell/setup-plan.ps1') -Json
            $obj = $json | ConvertFrom-Json
            $obj.paths.plan | Should -Match 'plan.md'
            Test-Path $obj.paths.plan | Should -BeTrue
        }
        finally {
            Pop-Location
            Remove-Item Env:SPECIFY_FEATURE
        }
    }

    It 'orchestrate-feature surfaces status paths' {
        $testRoot = Join-Path $TestDrive 'orchestrate-repo'
        New-Item -ItemType Directory -Path (Join-Path $testRoot 'specs/001-test-feature') -Force | Out-Null
        Set-Content -Path (Join-Path $testRoot 'specs/001-test-feature/spec.md') -Value '# Spec' -Encoding utf8
        Set-Content -Path (Join-Path $testRoot 'specs/001-test-feature/plan.md') -Value '# Plan' -Encoding utf8
        $env:SPECIFY_FEATURE = '001-test-feature'
        Push-Location $testRoot
        try {
            $json = & (Join-Path $RepoRoot 'scripts/powershell/orchestrate-feature.ps1') -Json
            $obj = $json | ConvertFrom-Json
            $obj.paths.status_feature | Should -Match 'status/feature.md'
        }
        finally {
            Pop-Location
            Remove-Item Env:SPECIFY_FEATURE
        }
    }

    It 'update-agent-context outputs JSON summary' {
        $testRoot = Join-Path $TestDrive 'agent-repo'
        New-Item -ItemType Directory -Path (Join-Path $testRoot '.specify/templates') -Force | Out-Null
        Copy-Item (Join-Path $RepoRoot 'templates/plan-template.md') (Join-Path $testRoot '.specify/templates/plan-template.md')
        Copy-Item (Join-Path $RepoRoot 'templates/agent-file-template.md') (Join-Path $testRoot '.specify/templates/agent-file-template.md')
        $featureDir = Join-Path $testRoot 'specs/001-test-feature'
        New-Item -ItemType Directory -Path $featureDir -Force | Out-Null
        Set-Content -Path (Join-Path $featureDir 'spec.md') -Value '# Spec' -Encoding utf8
        $plan = @'
---
feature_id: 001-test-feature
title: "Test"
status: Draft
branch: 001-test-feature
semver: 0.1.0
created_at: 2024-01-01
source_commit: HEAD
generator: spec-kit
constitution_version: 1.0.0
---

# Implementation Plan Overview

## Constitution Gate Summary
| Gate | Description | Status | Notes |
|------|-------------|--------|-------|
| G1 | Constitution compliance | PASS | |
| G2 | Clarifications resolved | PASS | |
| G3 | High risks mitigated | PASS | |

## Technical Context
| Field | Decision |
|-------|----------|
| Language/Version | Python 3.12 |
| Primary Dependencies | FastAPI |
| Storage | PostgreSQL |
| Testing Strategy | pytest |
| Target Platform | Linux |
| Project Type | service |
| Performance Goals | 95th percentile <= 400 ms |
| Constraints | N/A |

## Phase Breakdown & Exit Criteria
- Placeholder
'@
        Set-Content -Path (Join-Path $featureDir 'plan.md') -Value $plan -Encoding utf8
        $env:SPECIFY_FEATURE = '001-test-feature'
        Push-Location $testRoot
        try {
            $json = & (Join-Path $RepoRoot 'scripts/powershell/update-agent-context.ps1') -Json
            $obj = $json | ConvertFrom-Json
            $obj.ok | Should -BeTrue
            $obj.updated_files.Count | Should -BeGreaterThan 0
        }
        finally {
            Pop-Location
            Remove-Item Env:SPECIFY_FEATURE
        }
    }
}
