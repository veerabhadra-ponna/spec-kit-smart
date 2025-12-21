# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Spec Kit Smart CLI (speckitadv)

Builds a single-file executable with all prompts, templates, and launchers embedded.
Usage: pyinstaller speckit.spec
"""

import os
from pathlib import Path

# Get the spec file directory
spec_dir = Path(SPECPATH)

# Define paths - assets are now in speckit/assets/
assets_dir = spec_dir / 'speckit' / 'assets'

# Collect all asset files to embed
assets_data = []

# Collect prompts
prompts_dir = assets_dir / 'prompts'
if prompts_dir.exists():
    for root, dirs, files in os.walk(prompts_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.json'):
                src = Path(root) / file
                rel_path = src.relative_to(assets_dir)
                dest_dir = Path('assets') / rel_path.parent
                assets_data.append((str(src), str(dest_dir)))

# Collect templates
templates_dir = assets_dir / 'templates'
if templates_dir.exists():
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.json'):
                src = Path(root) / file
                rel_path = src.relative_to(assets_dir)
                dest_dir = Path('assets') / rel_path.parent
                assets_data.append((str(src), str(dest_dir)))

# Collect AGENTS.md
agents_md = assets_dir / 'AGENTS.md'
if agents_md.exists():
    assets_data.append((str(agents_md), 'assets'))

# Analysis
a = Analysis(
    ['speckit/__main__.py'],
    pathex=[str(spec_dir)],
    binaries=[],
    datas=assets_data,
    hiddenimports=[
        'typer',
        'rich',
        'rich.console',
        'rich.panel',
        'rich.table',
        'rich.tree',
        'pydantic',
        'speckit.commands',
        'speckit.commands.analyze',
        'speckit.commands.constitution',
        'speckit.core',
        'speckit.core.emit',
        'speckit.core.state',
        'speckit.core.config',
        'speckit.core.utils',
        'speckit.core.templates',
        'speckit.core.prompts',
        'speckit.core.stages',
        'speckit.setup',
        'speckit.setup.config',
        'speckit.setup.init_cmd',
        'speckit.setup.check_cmd',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'cv2',
    ],
    noarchive=False,
)

# Package
pyz = PYZ(a.pure)

# Single-file executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='speckitadv',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
