Import-Module Pester

Describe 'PowerShell helper scripts' {
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
    $featureName = '999-test-feature'
    $featureDir = Join-Path $repoRoot "specs/$featureName"
    $planPath = Join-Path $featureDir 'plan.md'
    $specPath = Join-Path $featureDir 'spec.md'

    BeforeAll {
        New-Item -ItemType Directory -Path $featureDir -Force | Out-Null
        Set-Content -LiteralPath $specPath -Value '# Temporary spec'
    }

    AfterAll {
        if (Test-Path $featureDir) { Remove-Item -Path $featureDir -Recurse -Force }
        Remove-Item Env:SPECIFY_FEATURE -ErrorAction SilentlyContinue
    }

    BeforeEach {
        Set-Content -LiteralPath $planPath -Value '# Temporary plan'
        $env:SPECIFY_FEATURE = $featureName
    }

    Context 'check-prerequisites.ps1' {
        It 'emits compact JSON when using -Json -PathsOnly' {
            $result = & pwsh -NoLogo -NoProfile -File (Join-Path $repoRoot 'scripts/powershell/check-prerequisites.ps1') -Json -PathsOnly
            $parsed = $result | ConvertFrom-Json
            $parsed.FEATURE_DIR | Should -Be $featureDir
            $parsed.FEATURE_SPEC | Should -Be (Join-Path $featureDir 'spec.md')
        }

        It 'returns structured JSON errors when plan is missing' {
            Remove-Item -LiteralPath $planPath -Force
            $result = & pwsh -NoLogo -NoProfile -File (Join-Path $repoRoot 'scripts/powershell/check-prerequisites.ps1') -Json 2>$null
            $parsed = $result | ConvertFrom-Json
            $parsed.status | Should -Be 'error'
            $parsed.message | Should -Match 'plan.md'
        }
    }

    Context 'setup-plan.ps1' {
        It 'copies template and emits JSON when -Json is specified' {
            Remove-Item -LiteralPath $planPath -Force -ErrorAction SilentlyContinue
            $result = & pwsh -NoLogo -NoProfile -File (Join-Path $repoRoot 'scripts/powershell/setup-plan.ps1') -Json
            $parsed = $result | ConvertFrom-Json
            $parsed.IMPL_PLAN | Should -Be $planPath
            Test-Path $planPath | Should -BeTrue
        }
    }
}
