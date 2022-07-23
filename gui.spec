# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(['main.py'],
     pathex=['C:\\Users\\pxsong\\miniconda3\\envs\\ti4all\\Lib\\site-packages\\paddleocr', 'C:\\Users\\pxsong\\miniconda3\\envs\\ti4all\\Lib\\site-packages\\paddle\\libs'],
     binaries=[('C:\\Users\\pxsong\\miniconda3\\envs\\ti4all\\Lib\\site-packages\\paddle\\libs', '.')],
     datas=[],
     hiddenimports=["skimage", "skimage.filters.edges"],
     hookspath=['.'],
     runtime_hooks=[],
     excludes=['matplotlib'],
     win_no_prefer_redirects=False,
     win_private_assemblies=False,
     cipher=block_cipher,
     noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
     cipher=block_cipher)
exe = EXE(pyz,
     a.scripts,
     [],
     exclude_binaries=True,
     name='ti4all',
     debug=False,
     bootloader_ignore_signals=False,
     strip=False,
     upx=True,
     console=True)
coll = COLLECT(exe,
     a.binaries,
     a.zipfiles,
     a.datas,
     strip=False,
     upx=False,
     upx_exclude=[],
     name='main')