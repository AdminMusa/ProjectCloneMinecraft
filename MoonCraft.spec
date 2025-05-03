# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MoonCraft.py'],
    pathex=[],
    binaries=[],
    datas=[('Sky0.png', '.'), ('grass.png', '.'), ('brick.png', '.'), ('stoneBricks.png', '.'), ('sand.png', '.'), ('wood.png', '.'), ('obsidian.png', '.'), ('cactus.png', '.'), ('tnt.png', '.'), ('C:/Users/Muhammad Musa/AppData/Local/Programs/Python/Python312/Lib/site-packages/panda3d/etc', 'etc')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MoonCraft',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Minecraft69.ico'],
)
