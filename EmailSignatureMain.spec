# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['EmailSignatureMain.py'],
    pathex=['.',
            '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/google/oauth2/',
            '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/imapclient/__init__.py'
            ],
    binaries=[],
    datas=[('./Logo.png', '.'),('./credentials.json', '.')],
    hiddenimports=[
    "PySide6", "requests", "google.auth", "google.oauth2", "googleapiclient.discovery", 
    "cryptography", "imapclient"
    ],
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
    name='EmailSignatureMain',
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
)
app = BUNDLE(
    exe,
    name='EmailSignatureMain.app',
    icon='./Icon.icns',
    bundle_identifier=None,
)
