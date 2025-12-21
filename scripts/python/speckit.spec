# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Spec Kit Smart CLI

Builds a single-file executable with all prompts and templates embedded.
Usage: pyinstaller speckit.spec
"""

import os
from pathlib import Path

# Get the spec file directory
spec_dir = Path(SPECPATH)
repo_root = spec_dir.parent.parent

# Define paths
speckit_pkg = spec_dir / 'speckit'
templates_dir = repo_root / 'templates'

# Collect all template files to embed
templates_data = []
if templates_dir.exists():
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.md'):
                src = Path(root) / file
                # Destination path relative to templates/
                rel_path = src.relative_to(templates_dir)
                dest_dir = Path('templates') / rel_path.parent
                templates_data.append((str(src), str(dest_dir)))

# Analysis
a = Analysis(
    ['speckit/__main__.py'],
    pathex=[str(spec_dir)],
    binaries=[],
    datas=templates_data,
    hiddenimports=[
        'typer',
        'rich',
        'rich.console',
        'rich.panel',
        'rich.table',
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
